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
from datetime import datetime, timedelta, time
import calendar

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
            #return redirect(url_for('reserve.set_rdate', equipid=form.equip.data))
            return redirect(url_for('reserve.table', equipid=form.equip.data))
        return render_template('reserve/reserve_selectequip.html', lst=[url_for('manage.equipimage', filename=file) for file in fsresource.list()] ,
                               form=form)

@reserve.route('/<equipid>/table',methods=['GET','POST'])
@login_required
def table(equipid):
    collection = db.get_collection('equip')
    results = collection.find_one({'equipid':equipid})
    result = results.pop('rdate')
    return render_template('reserve/rdatetable.html',equipid=equipid, datetime=datetime, calendar=calendar,d=datetime.today(),timedelta=timedelta, time=time, avoid=result)

@reserve.route('/<equipid>/<d>/nwtable',methods=['GET','POST'])
@login_required
def tablenext(equipid,d):
    return render_template('reserve/rdatetable.html',equipid=equipid, datetime=datetime, calendar=calendar,d=datetime.today()+timedelta(days=7),timedelta=timedelta, time=time)

@reserve.route('/<equipid>/<d>/pwtable',methods=['GET','POST'])
@login_required
def tableprevious(equipid,d):
    return render_template('reserve/rdatetable.html',equipid=equipid, datetime=datetime, calendar=calendar,d=datetime.today(),timedelta=timedelta, time=time)






@reserve.route('/<equipid>/<datetimeval>',methods=['GET','POST'])
@login_required
def set_rdate(equipid,datetimeval):
    form =SetRdateForm(equipid,datetimeval)
    collection = db.get_collection('equip')
    results = collection.find_one({'equipid': equipid})
    result = results.pop('rdate')
    if form.rdate.data in result.keys():
        flash("Already Resrved")
        return redirect(url_for('reserve.table',equipid=equipid))
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        oid = fsworkfile.put(form.file.data, content_type=form.file.data.content_type, filename=filename)
        flash(str(equipid)+" is Reserved on "+str(form.rdate.data))
        progress = Progress(equipid, datetimeval, current_user.id,form.usermemo.data,filename) #Progress 할당
        selected_equip=Equip(equipid,"","")
        result=collection.find_one({'equipid':equipid})
        selected_equip.from_dict(result)
        rdate=selected_equip.return_rdate() #Equip 클래스에서 rdate반환
        rdate[datetimeval]=1# rdate 업데이트
        selected_equip.update_equiprdate(equipid,rdate)
        send_email(current_app.config['ADMIN'], 'Confirm Reservation', 'reserve/email/confirm', progress=progress, token=progress.taskid)  # admin에게 메일 보내야함
        return redirect(url_for('mypage.show_reservation', username=current_user.username))
    return render_template('reserve/reserve_main.html',equipid=equipid, form=form,calendar=calendar)


@reserve.route('/workspace/<filename>')
def workfile(filename):
    gridout = fsworkfile.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)

