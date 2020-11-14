from flask import Blueprint


admin = Blueprint("admin",__name__,url_prefix="/u0123gg1/ab12345/admin",static_folder="assets")

from . import views