from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField, SelectField,DateTimeField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
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
        equip_lst = [(equipname, equipid) for equipid, equipname in lst][0]
        self.equip.choices=equip_lst

    def validate_equip(self, field):
        collection = db.get_collection('equip')
        results = collection.find({'equipid': field.data})
        dict = [result["rdate"] for result in results]

        print("\n\n")
        print()
        # if dict[]!=0:
        #   raise ValidationError('Already Reserved')
        pass


class SetRdateForm(FlaskForm):
    rdate = SelectField('Time')
    file = FileField('Upload a 3D printing file', validators=[Required()])
    submit = SubmitField('Reserve')
    def __init__(self, equipid, *args, **kwargs):
        print(equipid)
        super(SetRdateForm, self).__init__(*args, **kwargs)
        collection = db.get_collection('equip')
        results = collection.find({'equipid': equipid})
        lst = [(result["equipid"], result["rdate"])] #for result in results]
        rdate_lst = [(rdate, rdate) for equipid, rdate in lst if rdate != 0]
        print(lst, "lst")
        print(rdate_lst)
        print("\n")
        self.rdate.choices = rdate_lst



    # 필드#예약날짜가 사용가능한지 체크
"""
    def validate_rdate(self, field):
        collection = db.get_collection('equip')
        results = collection.find({"equipname":self.equip.data})
        dictionary = results["rdate"]
        print(dictionary)
        for key in dictionary:
            if dictionary[key] == 0:
                rdate.choices = (key, key)
"""
"""
    collection = db.get_collection('equip')
    results = collection.find({'equipid': ReserveRequestForm().data['equip']})
    dict = [result["rdate"] for result in results][0]
    lst = []
    for i in dict:
        if dict[i] == 0:
            lst.append(i)
    rdate.choices = lst
"""






"""
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')"""
    # pickrdate = SelectField('rdate')
    #pickrdate를 equip에 맞게 불러오기
    #select = request.form.get('equip')
    #results = collection.find({"equipname": select})
    #time_lst = [result['rdate'] for result in results]
    #pickrdate.choices=
  #  av_time = [(key, key) for key in rdict.key() if rdict[key] == False]
  #  rdate.choices = av_time

#        self.user = user


""" def pre_validate(self,field):  #사전검사
     collection = db.get_collection('equip')
     results = collection.find({'equipid': ReserveRequestForm().data['equip']})
     dict = [result["rdate"] for result in results][0]
     lst = []
     for i in dict:
         if dict[i] == 0:
             lst.append(i)
     rdate.choices = lst"""