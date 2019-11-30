from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User
#from .forms import ReserveRequestForm
#from . import reserve

from .. import db
from ..decorators import admin_required, permission_required
from ..email import send_email # added 20191108