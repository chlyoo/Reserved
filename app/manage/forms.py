from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField, SelectField,DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Optional
from datetime import datetime
from wtforms import ValidationError
from .. import db
from wtforms import FileField

class ConfirmForm(FlaskForm):
    EstimatedEndTime=DateTimeField("Input estimated progress ending time",validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    EstimatedPrice=IntegerField("Please input estimated price",validators=[DataRequired()])
    Confirm=SubmitField('Confirm')
    #def validate_EstimatedPrice:
     #   validators=Regexp
class EquipRegisterForm(FlaskForm):
    Equipid=StringField("Input Equip id")
    Equipname=StringField("Input Equip name")
    Equipspec=StringField("Input equip spec")
    equipImagefile = FileField('Register Equip image here', validators=[DataRequired()])
    Register=SubmitField('Register')

class EquipModifyForm(FlaskForm):
    Equipid=StringField("Input Equip id")
    Equipname=StringField("Input Equip name")
    Equipspec=StringField("Input equip spec")
    file = FileField('Register Equip image here', validators=[DataRequired()])
    Register=SubmitField('Modify')

class EquipDeleteForm(FlaskForm):
    Equipid=StringField("Input Equip id")
    Equipname=StringField("Input Equip name")
    Equipspec=StringField("Input equip spec")
    file = FileField('Register Equip image here', validators=[DataRequired()])
    Register=SubmitField('Delete')

