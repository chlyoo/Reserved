from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField, SelectField,DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Optional
from datetime import datetime
from wtforms import ValidationError
from .. import db
from wtforms import FileField

class ConfirmForm(FlaskForm):
    EstimatedEndTime=DateTimeField("Input estimated progress ending time",validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    EstimatedPrice=IntegerField("Please input estimated price",validators=[DataRequired()])
    Confirm=SubmitField('Confirm')
    #def validate_EstimatedPrice:
     #   validators=Regexp