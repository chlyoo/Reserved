from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import Progress, Equip
from .forms import ConfirmForm, EquipRegisterForm, EquipDeleteForm, EquipModifyForm
from werkzeug import secure_filename
from .. import fsresource, fsworkfile
from flask import send_file
from . import manage
from .. import db
from ..decorators import admin_required, permission_required
from ..email import send_email  # added 20191108
from datetime import datetime


@manage.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def main():
	collection = db.get_collection('progress')
	results = collection.find()
	if results!=None:
		p_lst = [(result['task_id'], result['user_id'], result['equip_id'], result['rdate'], result['usermemo'],
				  result['estimated_end_time'], result['estimated_price'], result['confirmed'], result['paid'],
				  result['complete'], result['filename']) for result in results]
		collection = db.get_collection('equip')
		results = collection.find()
		e_lst = [e for e in enumerate([(result['equipid'], result['equipname'], result['spec'], result['usingcount'], result['rdate'], result['filename']) for result in results],start=1)]
		return render_template('manage/main.html', progress_list=p_lst, equip_list=e_lst, lene=len(e_lst), lenp=len(p_lst))


@manage.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
@admin_required
def confirm(token):  # 관리자가 메일을 통해서 접속하는 페이지
	pr = Progress("", "", "", "", "")
	collection = db.get_collection('progress')
	result = collection.find_one({'task_id': int(token)})
	if result==None:
		flash("Already Canceled Reservation")
		return redirect(url_for("manage.main"))

	pr.from_dict(result)
	if pr.confirmed:
		flash("Has already been confirmed")
		return redirect(url_for("manage.main"))
	else:
		form = ConfirmForm()
		if form.validate_on_submit():
			pr.confirmed = True
			pr.estimated_price = form.EstimatedPrice.data
			pr.estimated_end_time = form.EstimatedEndTime.data
			collection.update_one({"task_id": int(token)}, {
				"$set": {'confirmed': True, "estimated_end_time": pr.estimated_end_time,
						 "estimated_price": pr.estimated_price}})
			collection=db.get_collection('equip')
			usingcount=collection.find_one({'equipid':pr.equipid})["usingcount"]+1
			collection.update_one({'equipid':pr.equipid},{"$set":{"usingcount":usingcount}})
			if pr.confirmed:
				flash("The progress has been confirmed")
				send_email(pr.userid, "Reservation Confirmed", 'manage/mail/confirm_complete', progress=pr)
				flash("Sending E-mail...")
				return redirect(url_for("manage.main"))

		return render_template('manage/do_confirm.html', form=form, progress=pr)

@manage.route('/complete/<taskid>', methods=['GET', 'POST'])
@login_required
@admin_required
def complete(taskid):  # 링크 통해서 접속하는 페이지
	pr = Progress("", "", "", "", "")
	collection = db.get_collection('progress')
	result = collection.find_one({'task_id': int(taskid)})
	pr.from_dict(result)
	if pr.complete:
		flash("Completed already")
		return redirect(url_for("manage.main"))
	else:
		pr.complete = True
		collection.find_one_and_update({"task_id": int(taskid)}, {
				"$set": {'complete': True}})
		collection=db.get_collection('equip')
		result = collection.find_one({'equipid': pr.equipid})
		xrdate=result['rdate']
		xrdate.pop(pr.rdate,None)
		collection.find_one_and_update({'equipid':pr.equipid},{'$set':{'rdate':xrdate}})
		if pr.complete:
			flash("Completed")
			send_email(pr.userid, "Work Complete", 'manage/mail/work_complete',datetime=datetime, progress=pr)
			flash("Sending E-mail...")

			return redirect(url_for("manage.main"))

@manage.route('/paid/<taskid>', methods=['GET', 'POST'])
@login_required
@admin_required
def pay(taskid):  # 링크 통해서 접속하는 페이지
	pr = Progress("", "", "", "", "")
	collection = db.get_collection('progress')
	result = collection.find_one({'task_id': int(taskid)})
	pr.from_dict(result)
	if pr.paid:
		flash("Paid already")
		return redirect(url_for("manage.main"))
	else:
		pr.paid = True
		collection.update_one({"task_id": int(taskid)}, {
				"$set": {'paid': pr.paid}})
		if pr.paid:
			flash("Paid Successfully")
			#pay까지 완료된 작업 -> History에 추가하고 Progress에서 삭제
			return redirect(url_for("manage.main"))




@manage.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register_equip():
	form = EquipRegisterForm()
	if form.validate_on_submit():
		collection = db.get_collection('equip')
		result =collection.find_one({'equipid':form.Equipid.data})
		if result!=None:
			flash("Already have same Equipid")
			return redirect(url_for('manage.register_equip'))
		equip = Equip(form.Equipid.data, form.Equipname.data, form.Equipspec.data)  # rdate intialize as well
		filename = secure_filename(form.equipImagefile.data.filename)
		oid = fsresource.put(form.equipImagefile.data, content_type=form.equipImagefile.data.content_type,
							 filename=filename)
		equip.filename=filename
		equip.oid=oid
		collection.insert(equip.to_dict())
		flash("Registered")
		return redirect(url_for('manage.main'))
	return render_template('manage/register_equip.html', form=form)


@manage.route('/modify', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_equip():
	# equip=Equip(equipid,equipname,spec)
	pass
	form=EquipModifyForm()
	if form.validate_on_submit():
		equip = Equip(form.Equipid.data, form.Equipname.data, form.Equipspec.data)  # rdate intialize as well
		filename = secure_filename(form.equipImagefile.data.filename)
		oid = fsresource.put(form.equipImagefile.data, content_type=form.equipImagefile.data.content_type,
							 filename=filename)
		equip.filename=filename
		equip.oid = oid
		collection = db.get_collection('equip')
		collection.remove({'equipid': form.equip.data})
		oid = collection.find_one({'equipid': form.equip.data})['oid']
		fsresource.delete(oid)
		collection.insert(equip.to_dict())
		flash("Modified")
		return redirect(url_for('manage.main'))
	return render_template('manage/modify_equip.html', form=form)

@manage.route('/delete', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_equip():
	form=EquipDeleteForm()
	if form.validate_on_submit():
		collection = db.get_collection('equip')
		oid=collection.find_one({'equipid':form.equip.data})['oid']
		fsresource.delete(oid)
		collection.remove({'equipid':form.equip.data})
		collection = db.get_collection('equip')
#Have to remove file also
		flash("Deleted")
		return redirect(url_for('manage.main'))
	return render_template('manage/delete_equip.html', form=form)

@manage.route('/resource/<filename>')
def equipimage(filename):
	gridout = fsresource.get_last_version(filename=filename)
	return send_file(gridout, mimetype=gridout.content_type)
