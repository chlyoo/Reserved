from flask import render_template, redirect, session, url_for, flash
from flask_login import login_user, login_required, logout_user
from flask_login import current_user
from ..models import User, Progress
from . import mypage
from .. import db
from ..decorators import admin_required, permission_required
from ..email import send_email # added 20191108
from .forms import EditProfileForm

@mypage.route('/', methods=['GET','POST'])
@login_required
def show_reservation():
	collection = db.get_collection('progress')
	result = collection.find({'user_id': current_user.id})
	if result != None:
		results = collection.find({'user_id':current_user.id},sort=[("task_id",-1)])
		table=[(result["equip_id"],result["usermemo"],result["rdate"],result["estimated_end_time"],result["estimated_price"],result["confirmed"],result["complete"],result["filename"]) for result in results]
		p_lst=[e for e in enumerate(table,start=1)]
		reservation_form=["Equipid","Memo","Rdate","estimated ending time","estimated price","Confirmed","Completed","File"]
		# #아래처럼 render template에 list반환
		return render_template('mypage/myreserve.html', template=reservation_form, lst=p_lst)
	else:
		return render_template('mypage/noreservation.html')
#return render_template('mypage/myreserve.html',
	#progress = Progress(form1.equip.data, form2.rdate.data, current_user.id)
"""
@mypage.route('/', methods=['GET', 'POST'])
def show_images():
	return render_template('img/img_lst.html', 
		file_lst = [url_for('img.image', filename=file) for file in fs.list()])
"""
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
		return redirect(url_for('.user', username=current_user.username))
	form.username.data = current_user.username
	return render_template('mypage/edit_profile.html', form=form)