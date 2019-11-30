from flask import render_template, redirect, session, url_for, flash, send_file, current_app
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

from datetime import datetime


"""@login_required
@reserve.route('/', methods=['GET', 'POST'])
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
            #usermemo   update하기
            filename = secure_filename(form2.file.data.filename)
            oid = fs.put(form2.file.data, content_type=form1.file.data.content_type, filename=filename)
            print(filename)
            # 메일
            progress = Progress(form1.equip.data, form2.rdate.data, current_user)
            token = progress.generate_token(False)  # 유저로 만드는게아니라 프로그레스로 만들어야함
            app=current_app()._get_current_object()
            send_email(app.config['ADMIN'], 'Confirm Reservation', 'reserve/email/confirm', equip=form1.equip.data, user=user,
                       token=token)  # admin에게 메일 보내야함
            #return redirect(url_for('mypage', username=current_user.username))
        return render_template('reserve/reserve_main.html',form1=form1, form2=form2, file_lst=[url_for('reserve.workfile', filename=file) for file in fs.list()])

    return render_template('reserve/reserve_selectequip.html', form=form1)

@reserve.route('/workspace/<filename>')
def workfile(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)


"""
@reserve.route('/confirm/<token>')
@login_required
@admin_required
"""
