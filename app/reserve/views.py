from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User
from .forms import ReserveRequestForm
from . import reserve

from .. import db
from ..email import send_email # added 20191108

from flask_login import current_user

"""@reserve.route('/', methods=['GET', 'POST'])
def reserve_main():
	return "Hello"
"""
from werkzeug import secure_filename
from .. import fs
from flask import send_file

@login_required
@reserve.route('/', methods=['GET', 'POST'])
def show_equips():#메인페이지
    # 이부분을 프린터 띄우는 코드로 수정하기
    #프린터를 보여주고 프린트가 사용가능한 날짜,시간 표시하기
	return render_template('reserve/equip_lst.html',
		file_lst = [url_for('reserve.image', filename=file) for file in fs.list()])

@reserve.route('/reserve', methods=['GET', 'POST'])
def make_reserve():
    form = ReserveRequestForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        oid = fs.put(form.file.data, content_type=form.file.data.content_type, filename=filename)
        print(filename)
        token = user.generate_confirmation_token()#유저로 만드는게아니라 프로그레스로 만들어야함
        send_email(user.id, 'Confirm Reservation', 'auth/email/confirm', user=user, token=token)
        return redirect(url_for('reserve.show_equips'))
    return render_template('reserve/workfile_register.html', form=form)


@reserve.route('/workspace/<filename>')
def workfile(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)
