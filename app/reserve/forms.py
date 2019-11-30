from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo

from wtforms import ValidationError
from ..models import User
from .. import db

from wtforms import FileField

class ReserveRequestForm(FlaskForm):
    file = FileField('Upload an 3D printing file', validators=[Required()])
    submit = SubmitField('Submit')
    def validate_rdate(self):
        # 예약날짜가 사용가능한지 체크
        pass