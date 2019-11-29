from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User
from .forms import LoginForm, RegistrationForm
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

@reserve.route('/', methods=['GET', 'POST'])
def show_images():# 이부분을 프린터 띄우는 코드로 수정하기
	return render_template('reserve/img_lst.html',
		file_lst = [url_for('img.image', filename=file) for file in fs.list()])

@reserve.route('/register', methods=['GET', 'POST'])
def register_images():
    form = RequestRegisterForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        oid = fs.put(form.file.data, content_type=form.file.data.content_type, filename=filename)
        print(filename)
        return redirect(url_for('img.show_images'))
    return render_template('img/img_register.html', form=form)


@reserve.route('/workspace/<filename>')
def image(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)
