import os
WEBSITE_FILES_LOCATION = os.environ.get("WEBSITE_FILES_LOCATION")
WEBSITE_IMAGES_LOCATION = os.environ.get("WEBSITE_IMAGES_LOCATION")

class Basic:
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
	SECRET_KEY = os.environ.get("SECRET_KEY")
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	

class Production(Basic):
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_PRODUCTION")


	
	
config = {"Basic":Basic,"Production":Production}