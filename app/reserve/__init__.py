from flask import Blueprint

reserve = Blueprint('reserve', __name__)

from . import views
