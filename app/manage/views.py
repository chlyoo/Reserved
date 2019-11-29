from datetime import datetime
from flask import render_template, session, redirect, url_for, flash

from . import main

from ..models import User, Permission

from flask_login import login_user, login_required, logout_user
from ..decorators import admin_required, permission_required


@login_required
@admin_required

pass
