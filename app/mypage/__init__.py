from flask import Blueprint

mypage = Blueprint('mypage', __name__)

from . import views
