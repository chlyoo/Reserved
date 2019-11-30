from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User
#from .forms import ReserveRequestForm
#from . import reserve

from .. import db
from ..decorators import admin_required, permission_required
from ..email import send_email # added 20191108


@mypage.route('/', methods=['GET','POST'])
@login_required
def show_reservation():
	return render_template('mypage/myreserve.html',
		 progress = Progress(form1.equip.data, form2.rdate.data, current_user.id))
	 collection = db.get_collection('prosess')
	 print(collection)

@img.route('/', methods=['GET', 'POST'])
def show_images():
	return render_template('img/img_lst.html', 
		file_lst = [url_for('img.image', filename=file) for file in fs.list()])


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
	return render_template('edit_profile.html', form=form)