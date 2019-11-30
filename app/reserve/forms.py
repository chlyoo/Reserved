from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Optional
from datetime import datetime
from wtforms import ValidationError
from .. import db
from wtforms import FileField

class EquipListForm(FlaskForm):
    equip = SelectField('Equip')
    submit = SubmitField('Select')
    def __init__(self, *args, **kwargs):
        super(EquipListForm, self).__init__(*args, **kwargs)
        collection = db.get_collection('equip')
        results = collection.find()
        lst = [(result["equipname"], result["equipid"]) for result in results]
        equip_lst = [(equipname, equipid) for equipid, equipname in lst]
        self.equip.choices=equip_lst


class SetRdateForm(FlaskForm):
    rdate = SelectField('Time',validators=[Optional()])
    usermemo = StringField("Leave a memo here:")
    file = FileField('Upload a 3D printing file', validators=[DataRequired()])
    submit = SubmitField('Reserve')
    def __init__(self, equipid, *args, **kwargs):
        super(SetRdateForm, self).__init__(*args, **kwargs)
        collection = db.get_collection('equip')
        results = collection.find_one({'equipid': equipid})
        lst={}
        lst=results['rdate']
        choices=[(key, key) for key in lst.keys() if lst[key]==0]
        self.rdate.choices=choices
