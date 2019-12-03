from datetime import datetime
from flask import render_template, session, redirect, url_for, flash

from . import main

from ..models import User, Permission

from flask_login import login_user, login_required, logout_user
from ..decorators import admin_required, permission_required

# 20191122
from .. import db
from flask_login import current_user
from .forms import EditProfileForm, EditProfileAdminForm
@main.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html', name=session.get('name'),known=session.get('known', False), current_time=datetime.utcnow())
# 20191122
@main.route('/user/<username>')
def user(username):
	collection = db.get_collection('users')
	results = collection.find_one({'username':username})
	if results is not None:
		user = User("", "", "", "")
		user.from_dict(results)
		return render_template('user.html', user=user)
	else:
		abort(404)

@main.route('/edit-profile', methods=['GET', 'POST'])
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

@main.route('/edit-profile/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	collection = db.get_collection('users')
	result = collection.find_one({'id':id})
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
			return redirect(url_for('.user', username=user.username))
		form.id.data = user.id
		form.username.data = user.username
		form.confirmed.data = user.confirmed
		form.role.data = user.role.name
		return render_template('mypage/edit_profile.html', form=form, user=user)
	else:
		abort(404)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
	return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
	return "For comment moderators!"

'''
@main.route('/reserve')
@login_required
def reserve_equip():
	collection = db.get_collection('users')
	result = collection.find_one({'id': id})
	if result != None:
		user = User(id, "", "", "")
		user.from_dict(result)
'''

