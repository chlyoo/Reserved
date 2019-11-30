from flask import Blueprint

manage = Blueprint('mypage', __name__)

from . import views
