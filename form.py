from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo

class New_article(FlaskForm):
    title = StringField("Title",validators=[DataRequired(),])
    article = StringField("Article",validators=[DataRequired(),])
    post = SubmitField("send")

class Login_Form(FlaskForm):
    email = StringField("email address",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("send")

class Registration_Form(FlaskForm):
    first_name = StringField("First Name",validators=[DataRequired()])
    last_name = StringField("Last Name",validators=[DataRequired()])
    username = StringField("Username",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),EqualTo("confirm_password",message="Password must match")])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),])
    submit = SubmitField("Register")