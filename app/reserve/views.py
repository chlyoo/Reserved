from flask import render_template, redirect, session, url_for, flash, send_file
from flask_login import login_user, login_required, logout_user
from ..models import User, Progress
from .forms import EquipListForm, SetRdateForm
from . import reserve

from werkzeug import secure_filename
from .. import fs
from flask import send_file
from .. import db
from ..decorators import admin_required, permission_required
from ..email import send_email  # added 20191108

from flask_login import current_user

"""@reserve.route('/', methods=['GET', 'POST'])
def reserve_main():
	return "Hello"
"""
from werkzeug import secure_filename
from .. import fs
from datetime import datetime


"""@login_required
@reserve.route('/', methods=['GET', 'POST'])
<<<<<<< HEAD
def show_equips():메인페이지
    #이부분을 프린터 띄우는 코드로 수정하기
    #프린터를 보여주고 프린트가 사용가능한 날짜,시간 표시하기
	return render_template('reserve/img_lst.html',
		file_lst = [url_for('img.image', filename=file) for file in fs.list()])
=======
def show_equips():
    collection = db.get_collection('users')  # 메인페이지
    result = collection.find_one({'id': current_user.id})  # 이부분을 프린터 띄우는 코드로 수정하기
    if result != None:  # 프린터를 보여주고 프린트가 사용가능한 날짜,시간 표시하기
        user = User(current_user.id, "", "", "")
        user.from_dict(result)
        return render_template('reserve/reserve_main.html', equip_lst=['a', 'b', 'c'],
                               file_lst=[url_for('reserve.workfile', filename=file) for file in fs.list()],
                               form=ReserveRequestForm(), name=session.get('name'),
                               known=session.get('known', False),
                               current_time=datetime.utcnow())"""
>>>>>>> 49c50c47bc9876ab6ce48ac11768c1ec448827c8


@login_required
@reserve.route('/', methods=['GET', 'POST'])
def make_reserve():
    form1 = EquipListForm()
    collection = db.get_collection('users')  # 메인페이지
    result = collection.find_one({'id': current_user.id})  # 이부분을 프린터 띄우는 코드로 수정하기

    if result != None:  # 프린터를 보여주고 프린트가 사용가능한 날짜,시간 표시하기
        user = User(current_user.id, "", "", "")
        user.from_dict(result)

    if form1.validate_on_submit():
        form2 = SetRdateForm(form1.equip.data)
        if form2.validate_on_submit():
            filename = secure_filename(form2.file.data.filename)
            oid = fs.put(form2.file.data, content_type=form1.file.data.content_type, filename=filename)
            print(filename)
            # 메일
            progress = Progress(form1.equip.data, form2.rdate.data, current_user.id)
            token = progress.generate_token(False)  # 유저로 만드는게아니라 프로그레스로 만들어야함
            send_email(user.id, 'Confirm Reservation', 'reserve/email/confirm', equip=form1.equip.data, user=user,
                       token=token)  # admin에게 메일 보내야함
        return render_template('reserve/reserve_main.html',
                                   file_lst=[url_for('reserve.workfile', filename=file) for file in fs.list()],
                                   form1=form1, form2=form2)
    return render_template('reserve/reserve_selectequip.html',form1=form1)







@reserve.route('/workspace/<filename>')
def workfile(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)


"""
@reserve.route('/confirm/<token>')
@login_required
@admin_required
"""
