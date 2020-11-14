from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app
from datetime import datetime
import os
db = SQLAlchemy()

class Subscribers(db.Model):
	__tablename__ = "subcribers"
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(225),unique=True)

class Statistics(db.Model):
	__tablename__ = "statistics"
	id = db.Column(db.Integer,primary_key=True)
	page_title = db.Column(db.String(40))
	date = db.Column(db.DateTime,unique=True,default=datetime.utcnow)

class User_statistics(db.Model):
	__tablename__ = "user_statistics"
	id = db.Column(db.Integer,primary_key=True)
	general_progress = db.Column(db.Integer)
	analytical_chemistry_progress = db.Column(db.Integer)
	organic_chemistry_progress = db.Column(db.Integer)
	physical_chemistry_progress = db.Column(db.Integer)
	practical_chemistry_progress = db.Column(db.Integer)
	user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

class Comments(db.Model):
	__tablename__ = "comments"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(32))
	email = db.Column(db.String(225))
	message = db.Column(db.Text)
	time = db.Column(db.DateTime,default=datetime.utcnow)
	document_id = db.Column(db.Integer,db.ForeignKey("articles.id"))

class Document(db.Model):
	__tablename__ = "articles"
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String(30),unique = True,nullable=False)
	brief_desc = db.Column(db.Text,nullable=False)
	location = db.Column(db.String(225),default=os.environ["WEBSITE_FILES_LOCATION"])
	category = db.Column(db.String(225))
	time_of_production = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	time_of_last_modification = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	comments = db.relationship("Comments",backref="document",lazy="dynamic",cascade="all, delete-orphan")
	image_id = db.Column(db.Integer,db.ForeignKey("images.id"))
	

class Images(db.Model):
	__tablename__ = "images"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(40),unique=True)
	location = db.Column(db.String(225),unique=True)
	document = db.relationship("Document",backref="thubnail",lazy="dynamic")
	


class User(db.Model,UserMixin):
	__tablename__ = "users"
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	first_name = db.Column(db.String(30),nullable=False)
	last_name  = db.Column(db.String(30),nullable=False)
	username = db.Column(db.String(30),nullable=False)
	hashed_password = db.Column(db.String(225),nullable=False)
	email = db.Column(db.String(40),unique = True,nullable=False)
	permission = db.Column(db.Integer,default=0)
	authenticated = db.Column(db.Boolean,default=False)
	active = db.Column(db.Boolean,default=True)
	confirmed = db.Column(db.Boolean,default=False)
	registration_date = db.Column(db.DateTime,default=datetime.utcnow)
	documents = db.relationship("Document",cascade="all",backref="user")
	statistics = db.relationship("User_statistics",cascade="all, delete-orphan",backref="user_statistics")


	#This piece of code ensure the password stored in the database is not assessable but can be redefined
	@property
	def password(self):
		raise AttributeError("password cannot be read")

	@password.setter
	def password(self,new_password):
		self.hashed_password = generate_password_hash(new_password)

	def check_password(self,new_password):
		return check_password_hash(self.hashed_password, new_password)

	@property
	def is_authenticated(self):
		return self.authenticated
	
	@is_authenticated.setter
	def is_authenticated(self,state):
		self.authenticated = state
		db.session.add(self)
		db.session.commit()

	
	
	@property
	def is_active(self):
 		return self.active

	@is_active.setter
	def is_active(self,state):
		self.active = state


	def has_permission(self,number):
		return self.permission == number

	def generate_confirmation_token(self):
		s = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"])
		return s.dumps({"confirm":self.id}).decode("utf8")
		
		

	def confirm(self,token,expiration=3600):
		s = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"],expiration)

		try:
			user_dic = s.loads(token.encode("utf8"))
		except:
			return False

		if user_dic.get("confirm") != self.id:
			return False

		self.confirmed = True
		db.session.add(self)
		db.session.commit()

		return True

		
	

