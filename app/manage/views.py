from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import Progress
from .forms import ConfirmForm
from . import manage
from .. import fsresource,fsworkfile
from flask import send_file
from .. import db
from ..decorators import admin_required, permission_required
from ..email import send_email # added 20191108

@manage.route('/',methods=['GET','POST'])
@login_required
@admin_required
def main():
	#progress표시
	collection = db.get_collection('progress')
	results = collection.find()
	p_lst = [(result['task_id'], result['user_id'], result['equip_id'], result['rdate'], result['usermemo'],
			result['estimated_end_time'], result['estimated_price'], result['confirmed'], result['paid'],
			result['complete'], result['filename']) for result in results]
	collection=db.get_collection('equip')
	results=collection.find()
	e_lst=[(result['equipid'], result['equipname'], result['spec'], result['usingcount'], result['rdate']) for result in results]
	return render_template('manage/main.html', progress_list=p_lst,equip_list=e_lst)

@manage.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
@admin_required
def confirm(token): #관리자가 메일을 통해서 접속하는 페이지
	pr=Progress("","","","","")
	collection = db.get_collection('progress')
	result = collection.find_one({'task_id':int(token)})
	pr.from_dict(result)
	if pr.confirmed:
		flash("Has already been confirmed")
		return redirect(url_for("manage.show_all_progresses"))
	else:
		form = ConfirmForm()
		if form.validate_on_submit():
			pr.confirmed=True
			pr.estimated_price=form.EstimatedPrice.data
			pr.estimated_end_time = form.EstimatedEndTime.data
			collection.update_one({ "task_id":int(token)},{ "$set": {'confirmed':True, "estimated_end_time": pr.estimated_end_time,"estimated_price":pr.estimated_price } })
			print(pr.confirmed)
			if pr.confirmed:
				flash("The progress has been confirmed")
				send_email(pr.userid,"Reservation Confirmed",'manage/mail/confirm_complete',progress=pr)
				flash("Sending E-mail...")
				return redirect(url_for("manage.show_all_progresses"))

		return render_template('manage/do_confirm.html',form=form, progress=pr)


@manage.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register_equip():
	pass

@manage.route('/modify', methods=['GET', 'POST'])
@login_required
@admin_required
def modify_equip():
	pass

@manage.route('/resource/<filename>')
def equipimage(filename):
	gridout = fsworkfile.get_last_version(filename=filename)
	return send_file(gridout, mimetype=gridout.content_type)