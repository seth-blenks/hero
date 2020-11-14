from flask import Flask,g,request
from config import config
from database import db,User,Statistics
from flask_migrate import Migrate
from display.blueprint import main
from admin.blueprint import admin
from admin.views import login_manager
import os
from datetime import datetime,timedelta
from auth.blueprint import auth




migration = Migrate()

def create_app(config_name):

	app = Flask(__name__)
	app.config.from_object(config[config_name])
	app.register_blueprint(main)
	app.register_blueprint(admin)
	app.register_blueprint(auth)
	

	#initializations
	db.init_app(app)

	login_manager.init_app(app)
	migration.init_app(app,db)
	
	return app


app = create_app('Basic')


@app.cli.command("initdb")
def init_db():
        db.drop_all()
        db.create_all()

        admin = User()
        admin.first_name = os.environ.get("ADMIN_FIRSTNAME")
        admin.last_name = os.environ.get("ADMIN_LASTNAME")
        admin.username = os.environ.get("ADMIN_USERNAME")
        admin.email = os.environ.get("ADMIN_EMAIL")
        admin.password = os.environ.get("ADMIN_PASSWORD")
        admin.permission = os.environ.get("ADMIN_PERM_VALUE")
        admin.confirmed = True

        db.session.add(admin)
        db.session.commit()

	


if __name__ == '__main__':
	
	app.run(host="0.0.0.0",port=8000,debug=True)
