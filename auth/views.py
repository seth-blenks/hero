from .blueprint import auth
from form import Registration_Form,Login_Form
from database import db,User
from flask_login import login_required,login_user,logout_user,current_user
from flask import redirect,abort
from flask import render_template,flash,url_for
from threading import Thread
import time
from functools import wraps

def confirmation_decorator(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		if current_user.is_authenticated:
			if current_user.confirmed:
				return func(*args,**kwargs)
			else:
		            return redirect(url_for("auth.confirmation"))
		else:
			return redirect(url_for('auth.login_page'))
	return wrapper

def send_confirmation_token():
	messages = (message for message in ["Sending confirmation","go ing","now"])
	for a in messages:
		print(a)
		time.sleep(2)

@auth.route("/register",methods=["GET","POST"])
def registration_page():
	form = Registration_Form()

	if form.validate_on_submit():



		email = form.email.data

		if User.query.filter_by(email=email).first():
			flash("This email is already linked to an account")
			return redirect(url_for("auth.login_page"))

		first_name = form.first_name.data
		last_name = form.last_name.data
		username = form.username.data
		password = form.password.data

		new_user = User()
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.username = username
		new_user.email = email
		new_user.password = password

		token = new_user.generate_confirmation_token()
		print(token)

		Thread(target=send_confirmation_token).start()

		db.session.add(new_user)
		db.session.commit()

		flash("A confirmation mail has been sent to your email address. Go confirm your account")

		return redirect(url_for("auth.login_page"))


	return render_template("auth/register.html",form=form)

@auth.route("/login",methods=["GET","POST"])
def login_page():
	form = Login_Form()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = User.query.filter_by(email=email).first()

		if user and user.check_password(password):

			#This line of code should be removed
			user.is_authenticated = True
			if not user.is_active:
				flash("Account not yet confirmed. Ensure you confirm your account")
				login_user(user)
				return redirect(url_for('auth.confirmation'))
			
			login_user(user)
			
			return redirect(url_for("main.cover"))
		else:
			flash("Email and Password incorrect",category="alert-warning")
			return redirect(url_for("auth.login_page"))


	return render_template("auth/login.html",form=form)

@auth.route("/confirmation/auth/<token>")
@login_required
def confirmation_token(token): 
	print(current_user.confirm(token))
	print(token)

	if current_user.confirm(token):
		flash("Account confirmed")
	else:
		flash("Account  not confimed. Confirm account ")
		return redirect(url_for("auth.login_page"))

	return redirect ("main.cover")

@auth.route("/confirmation/")
@login_required
def confirmation():
	token = current_user.generate_confirmation_token()
	print(token)
	return render_template("auth/confirmation.html")

@auth.route("/profile")
@confirmation_decorator
def profile_page():
	
	return render_template("auth/profile.html",user=current_user)

@auth.route("/logout")
@login_required
def logout_page():
	logout_user()
	return redirect(url_for("main.cover"))
