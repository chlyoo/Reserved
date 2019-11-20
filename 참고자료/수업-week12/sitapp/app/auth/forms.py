from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo

from wtforms import ValidationError
from ..models import User
from .. import db

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
							'Usernames must have only letters, '
							'numbers, dots or underscores')])
	password = PasswordField('Password', validators=[Required(), 
													EqualTo('password2', 
													message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')

	def validate_email(self, field):
		collection = db.get_collection('users')
		results = collection.find_one({'id':field.data})
		if results is not None:
			raise ValidationError('Email already registered.')
		pass
	
	def validate_username(self, field):
		collection = db.get_collection('users')
		results = collection.find_one({'username':field.data})
		if results is not None:
			raise ValidationError('Username already registered.')
		pass