from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField, SelectField, DateTimeField
from wtforms.validators import Required, Length, Regexp, EqualTo, Optional
from datetime import datetime
from wtforms import ValidationError
from .. import db
from wtforms import FileField

class EquipListForm(FlaskForm):
    equip = SelectField('Equip',validators=[Required()])
    select = SubmitField('Select')
    def __init__(self, *args, **kwargs):
        super(EquipListForm, self).__init__(*args, **kwargs)
        collection = db.get_collection('equip')
        results = collection.find()
        lst = [(result["equipname"], result["equipid"]) for result in results]
        equip_lst = [(equipname, equipid) for equipid, equipname in lst]
        self.equip.choices=equip_lst


class SetRdateForm(FlaskForm):
    rdate = DateTimeField('Time')
    usermemo = StringField("Leave a memo here:")
    file = FileField('Upload a 3D printing file', validators=[Required()])
    submit = SubmitField('Reserve')
    def __init__(self, equipid,datetimeval, *args, **kwargs):
        super(SetRdateForm, self).__init__(*args, **kwargs)
        collection = db.get_collection('equip')
        results = collection.find_one({'equipid': str(equipid)})
        lst=results.pop('rdate')

        self.rdate.data=datetime.strptime(datetimeval,"%Y-%m-%d %H:%M:%S")

""" def validate_rdate(self,field):
        pass
    def validate_usermemo(self,field):
        pass
      def validate_equip(self,field):
    pass
"""
