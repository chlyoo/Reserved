from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User
from .forms import LoginForm, RegistrationForm
from . import reserve

from .. import db
from ..email import send_email # added 20191108

from flask_login import current_user

@reserve.route('/', methods=['GET', 'POST'])
def reserve_main():
	return "Hello"
