from datetime import datetime
from flask import render_template, session, redirect, url_for, flash

from . import main

from ..models import User, Permission

# 20191122
from .. import db
from flask_login import current_user

@main.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html', name=session.get('name'),known=session.get('known', False), current_time=datetime.utcnow())
# 20191122

