from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField, SelectField,DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Optional, Required
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
    Equipid = StringField("Input Equip id", validators=[Required()])
    Equipname = StringField("Input Equip name", validators=[Required()])
    Equipspec=StringField("Input equip spec")
    equipImagefile = FileField('Register Equip image here', validators=[DataRequired()])
    Register=SubmitField('Register')
    def validate_Equipid(self,field):
        collection = db.get_collection('equip')
        results = collection.find_one({'equipid': field.data})
        if results is not None:
            raise ValidationError('Equipid already registered.')
        pass
    def validate_Equipname(self,field):
        collection = db.get_collection('equip')
        results = collection.find_one({'equipname': field.data})
        if results is not None:
            raise ValidationError('Equipname already registered.')
        pass

class EquipModifyForm(FlaskForm):
    equip=SelectField("Select Equip to modify")
    Equipid=StringField("Input New Equip id",validators=[Required()])
    Equipname=StringField("Input New Equip name",validators=[Required()])
    Equipspec=StringField("Input equip spec")
    equipImagefile = FileField('Register Equip image here', validators=[DataRequired()])
    Register=SubmitField('Modify')
    def __init__(self, *args, **kwargs):
        super(EquipModifyForm, self).__init__(*args, **kwargs)
        collection = db.get_collection('equip')
        results = collection.find()
        lst = [(result["equipname"], result["equipid"]) for result in results]
        equip_lst = [(equipname, equipid) for equipid, equipname in lst]
        self.equip.choices=equip_lst
    def validate_Equipid(self,field):
        collection = db.get_collection('equip')
        results = collection.find_one({'equipid': field.data})
        if results is not None:
            raise ValidationError('Equipid already registered.')
        pass
    def validate_Equipname(self,field):
        collection = db.get_collection('equip')
        results = collection.find_one({'equipname': field.data})
        if results is not None:
            raise ValidationError('Equipname already registered.')
        pass

class EquipDeleteForm(FlaskForm):
    equip = SelectField("Select Equip to delete")
    Delete=SubmitField('Delete')
    def __init__(self, *args, **kwargs):
        super(EquipDeleteForm, self).__init__(*args, **kwargs)
        collection = db.get_collection('equip')
        results = collection.find()
        lst = [(result["equipname"], result["equipid"]) for result in results]
        equip_lst = [(equipname, str(equipid)+" - "+str(equipname)) for equipid, equipname in lst]
        self.equip.choices=equip_lst
