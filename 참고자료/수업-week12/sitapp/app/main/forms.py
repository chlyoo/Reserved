from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length

######
class NameForm(FlaskForm):    
    name = StringField('What is your name?', validators=[Required()])    
    submit = SubmitField('Submit') 
######