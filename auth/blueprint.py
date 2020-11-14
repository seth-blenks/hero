from flask import Blueprint

auth = Blueprint("auth",__name__,url_prefix="/u0/user/auth/a112/")

from . import views

