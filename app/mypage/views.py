from flask import render_template, redirect, session, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user
from flask_login import current_user
from ..models import User, Progress
from . import mypage
from .. import db,fsworkfile
from ..decorators import admin_required, permission_required
from ..email import send_email # added 20191108
from .forms import EditProfileForm, EditProfileAdminForm

@mypage.route('/', methods=['GET','POST'])
@login_required
def show_reservation():
	collection = db.get_collection('progress')
	resultif = collection.find_one({'user_id': current_user.id})
	if resultif != None:
		results = collection.find({'user_id':current_user.id},sort=[("task_id",-1)])
		table=[(result["equip_id"],result["usermemo"],result["rdate"],result["estimated_end_time"],result["estimated_price"],result["confirmed"],result["complete"],result["filename"]) for result in results]
		t_ble=[result["task_id"] for result in  collection.find({'user_id':current_user.id},sort=[("task_id",-1)])]
		p_lst = [e for e in enumerate(table, start=1)]
		reservation_form=["Equipid","Memo","Rdate","estimated ending time","estimated price","Confirmed","Completed","File","Modify"]
		# #아래처럼 render template에 list반환
		return render_template('mypage/myreserve.html', template=reservation_form, lst=p_lst,table=t_ble)
	else:
		return render_template('mypage/noreservation.html')
#return render_template('mypage/myreserve.html',
	#progress = Progress(form1.equip.data, form2.rdate.data, current_user.id)

@mypage.route('/cancel/<taskid>', methods=['GET', 'POST'])
@login_required
def cancel(taskid):
	pr = Progress("", "", "", "", "")
	collection = db.get_collection('progress')
	result = collection.find_one({'task_id': int(taskid)})
	pr.from_dict(result)
	if pr.confirmed:
		flash("Cannot Cancel")
		return redirect(url_for('mypage.show_reservation'))
	else:
		collection.delete_one({'task_id':int(taskid)})
		collection = db.get_collection('equip')
		result = collection.find_one({'equipid': pr.equipid})
		if result != None:
			xrdate = result['rdate']
			xrdate.pop(pr.rdate, None)
			collection.find_one_and_update({'equipid': pr.equipid}, {'$set': {'rdate': xrdate}})
			send_email(current_app.config['ADMIN'], 'Reservation Canceled', 'reserve/email/cancel', progress=pr)  # admin에게 메일 보내야함
			oid=result['oid']
			fsworkfile.delete(oid)
	return redirect(url_for('mypage.show_reservation'))

@mypage.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		# db update
		collection = db.get_collection('users')
		collection.delete_one({'id':current_user.id})
		collection.insert_one(current_user.to_dict())

		flash('Your profile has been updated.')
		return redirect(url_for('mypage.show_reservation'))
	form.username.data = current_user.username
	return render_template('mypage/edit_profile.html', form=form)


@mypage.route('/edit-profile/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	collection = db.get_collection('users')
	result = collection.find_one({'id': id})
	if result != None:
		user = User(id, "", "", "")
		user.from_dict(result)
		form = EditProfileAdminForm(user=user)
		if form.validate_on_submit():
			user.id = form.id.data
			user.username = form.username.data
			user.confirmed = form.confirmed.data
			# db update
			collection = db.get_collection('users')
			collection.update_one({'id': user.id}, {'$set': {'role_id': form.role.data}})

			flash('The profile has been updated.')
			return redirect(url_for('main.user', username=user.username))
		form.id.data = user.id
		form.username.data = user.username
		form.confirmed.data = user.confirmed
		form.role.data = user.role.name
		return render_template('mypage/edit_profile.html', form=form, user=user)
	else:
		abort(404)