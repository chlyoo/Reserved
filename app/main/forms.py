from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length

# 20191122
from wtforms import SelectField, ValidationError
from wtforms.validators import Regexp, EqualTo

from .. import db

######
class NameForm(FlaskForm):    
    name = StringField('What is your name?', validators=[Required()])    
    submit = SubmitField('Submit') 
######

# 20191122
class EditProfileForm(FlaskForm):
	username = StringField('Real name', validators=[Length(0, 64)])
	submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
	id = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('Username', validators=[Required(), Length(1, 64), 
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, ''numbers, dots or underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role')
	username = StringField('Real name', validators=[Length(0, 64)])
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		collection = db.get_collection('roles')
		results = collection.find({ } , { "name": True })
		
		lst = [result['name'] for result in results] 
		print(lst)
		r_lst = [(num, role) for num, role in enumerate(lst)]

		self.role.choices = r_lst
		self.user = user

	def validate_email(self, field):
		collection = db.get_collection('users')
		results = collection.find_one({'id':field.data})
		if results is not None:
			raise ValidationError('Email already registered.')
		pass