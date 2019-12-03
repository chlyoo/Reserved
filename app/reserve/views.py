from flask import render_template, redirect, session, url_for, flash, send_file, current_app
from flask_login import login_user, login_required, logout_user
from ..models import User, Progress,Equip
from .forms import EquipListForm, SetRdateForm
from . import reserve

from werkzeug import secure_filename
from .. import fsresource,fsworkfile
from flask import send_file
from .. import db
from ..decorators import admin_required, permission_required
from ..email import send_email  # added 20191108

from flask_login import current_user
from datetime import datetime


@reserve.route('/', methods=['GET', 'POST'])
@login_required
def select_equip():
    form = EquipListForm()
    collection = db.get_collection('users')  # 메인페이지
    result = collection.find_one({'id': current_user.id})  # 이부분을 프린터 띄우는 코드로 수정하기
    if result != None:  # 프린터를 보여주고 프린트가 사용가능한 날짜,시간 표시하기
        user = User(current_user.id, "", "", "")
        user.from_dict(result)
        if form.validate_on_submit():
            return redirect(url_for('reserve.set_rdate', equipid=form.equip.data))

        return render_template('reserve/reserve_selectequip.html', equip_lst=[name for equipid,name in form.equip.choices],
                               file_lst=[url_for('manage.equipimage', filename=file) for file in fsresource.list()],
                               form=form, name=session.get('name'),
                               known=session.get('known', False),
                               current_time=datetime.utcnow())


@reserve.route('/<equipid>',methods=['GET','POST'])
@login_required
def set_rdate(equipid):
    form =SetRdateForm(equipid)
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        oid = fsworkfile.put(form.file.data, content_type=form.file.data.content_type, filename=filename)
        flash(str(equipid)+" is Reserved on "+str(form.rdate.data))
        # 메일
        progress = Progress(equipid, form.rdate.data, current_user.id,form.usermemo.data,filename) #Progress 할당
        selected_equip=Equip(equipid)
        rdate=selected_equip.return_rdate() #Equip 클래스에서 rdate반환
        rdate[form.rdate.data]=1# rdate 업데이트
        print(rdate)
        selected_equip.update_equiprdate(equipid,rdate)
        send_email(current_app.config['ADMIN'], 'Confirm Reservation', 'reserve/email/confirm', progress=progress, token=progress.taskid)  # admin에게 메일 보내야함
        return redirect(url_for('mypage.show_reservation', username=current_user.username))
    return render_template('reserve/reserve_main.html',form=form)


@reserve.route('/workspace/<filename>')
def workfile(filename):
    gridout = fsworkfile.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)


"""
@reserve.route('/confirm/<token>')
@login_required
@admin_required


@login_required
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
                               current_time=datetime.utcnow())
"""
"""col_progress = db.get_collection('progress')
        try:
            tot_count = col_progress.find_one(sort=[("task_id", -1)])['task_id']
        except:
            tot_count = 0

        col_progress.insert_one(
            {'task_id': tot_count + 1, 'user_id': current_user.id, 'equip_id': equipid, 'rdate': form.rdate.data, 'estimated_end_time': '0000-00-00 00:00:00', 'estimated_price': -1, 'confirmed': 'false', 'paid': 'false', 'complete':'false'})"""