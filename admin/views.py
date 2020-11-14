from flask import render_template,redirect,abort,g,flash,request,url_for
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from database import User,Document,db,Images,Subscribers,Statistics,Comments
from flask.views import MethodView
from form import New_article,Login_Form
from datetime import datetime,timedelta
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from PIL import Image
from sqlalchemy.exc import IntegrityError
from config import WEBSITE_FILES_LOCATION,WEBSITE_IMAGES_LOCATION
from functools import wraps
from .blueprint import admin



def admin_decorator(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		if current_user.is_authenticated and current_user.has_permission(10):
			return func(*args,**kwargs)
		else:
			abort(401)
	return wrapper

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))



@admin.route("/",methods=["GET","POST"])
def homepage():
	form = Login_Form()

	if form.validate_on_submit():
		user_admin = User.query.filter_by(email=form.email.data).first()
		if user_admin:
			if user_admin.check_password(form.password.data):
				flash("Logged in")
				user_admin.is_authenticated = True
				login_user(user_admin)
				return redirect(url_for("admin.dashboard"))
			else:
				flash("Incorrect Password And Email")
				return redirect(url_for("admin.homepage"))
		else:
			flash("Incorrect Password And Email")
			return redirect(url_for("admin.homepage"))
	
	return render_template("admin/templates/contact.html",form=form)

@admin.route("/dashboard")
@admin_decorator
def dashboard():
	return render_template("admin/templates/index.html")

@admin.route("/logout")
@admin_decorator
def logout():
	logout_user()
	flash("logged out")
	return redirect(url_for("main.homepage"))


class Article_view(MethodView):
	
	def __init__(self):
		self.form = New_article()

	def get(self):
		content = Document.query.order_by(Document.id.desc()).all()
		return render_template("admin/templates/dashboard_templates/database_display.html",contents=content)


posting_view = admin_decorator(Article_view.as_view("posting"))
admin.add_url_rule("/posts/",view_func=posting_view)

@admin.route("/subscribers/")
@admin_decorator
def subscribers():
	content = Subscribers.query.order_by(Subscribers.id.desc()).all()
	return render_template("admin/templates/dashboard_templates/subscribers_display.html",contents=content)

def save_file(file,brief_desc,thubnail,category):
	filename_with_txt_extension = secure_filename(file.filename)
	file_extension = filename_with_txt_extension.split('.',1)[-1].lower()

	filename = filename_with_txt_extension

	if file_extension in ["txt"] and brief_desc != None:
		file_absolute_directory = os.path.join(WEBSITE_FILES_LOCATION,filename.lower())
		if Path(file_absolute_directory).exists():
			flash("a file with this name already exists")
			return False

		

		new_document = Document()
		new_document.title = filename.split(".",1)[0].lower()
		new_document.location = WEBSITE_FILES_LOCATION
		new_document.user_id = current_user._get_current_object().id
		new_document.brief_desc = brief_desc
		new_document.category = category

		img = Images.query.filter_by(name=thubnail).first()

		new_document.image_id = img.id

		db.session.add(new_document)

		try:
			db.session.commit()

			with open(file_absolute_directory,"w") as wfile:
				wfile.write(file.read().decode("utf8"))
			
		except IntegrityError:
			flash("Choose another display image",category="alert-info")
			return False


		return True
	else:
		return False

@admin.route("/upload/",methods=["POST","GET"])
@admin_decorator
def upload():
    if request.method == "POST":
        brief_desc = request.form.get("description")
        file = request.files["file"]
        thubnail = request.form.get("thubnail")
        category = request.form.get("category")

        if not Images.query.filter_by(name=thubnail).first():
            flash("Image not found in database")
            return redirect(url_for("admin.dashboard"))

        if file.filename and brief_desc and (category in ['Analytic Chemistry','Practical Chemistry','Organic Chemistry','Physical Chemistry']):
            if save_file(file,brief_desc,thubnail,category):
                flash("file successfully uploaded",category="alert-success")
                return redirect(url_for("admin.dashboard"))
            else:
                flash("File not save",category="alert-danger")
                return redirect("admin.dashboard")
        else:
            abort(400)

    return render_template("admin/templates/dashboard_templates/upload.html")

@admin.route("/upload/images/",methods=["POST","GET"])
@admin_decorator
def get_images():

	if request.method == "POST":
		file = request.files.get("image")
		
		if file:
			filename = secure_filename(file.filename)

			if filename.split(".",1)[-1] not in ["png","jpg","gif"]:
				flash("Support image format include png, jpg and gif",category="alert-info")
				return redirect(url_for("admin.dashboard"))
			
			if Path(os.path.join(WEBSITE_IMAGES_LOCATION,filename)).exists():
				flash("an image with this name already exists",category="alert-danger")
				return redirect(url_for("admin.dashboard"))
			else:
				img = Image.open(file)
				img = img.resize((500,500))
				img.save(os.path.join(WEBSITE_IMAGES_LOCATION,filename))
				
				#adding image to database
				new_image = Images()
				new_image.name = filename
				new_image.location = os.path.join("/static/assets/images",filename)

				db.session.add(new_image)
				db.session.commit()
				
				flash("Image successfully saved",category="alert-success")
				return redirect(url_for(("admin.dashboard")))
		else:
			flash("No image selected",category="alert-info")
			return redirect(url_for("admin.dashboard"))
	images = Images.query.all()
	return render_template("admin/templates/dashboard_templates/images.html",contents=images)

@admin.route("/images/delete/")
@admin_decorator
def delete_image():
	iid = request.args.get("id")
	iid = Images.query.get(int(iid))
	if iid:
		os.remove(os.path.join(WEBSITE_IMAGES_LOCATION,iid.name))
		db.session.delete(iid)
		db.session.commit()

		flash("image deleted successfully",category="alert-success")
		return redirect(url_for("admin.homepage"))
	flash("Image not found in database",category="alert-warning")
	return redirect(url_for("admin.homepage"))

@admin.route("/upload/edit/",methods=["GET","POST"])
@admin_decorator
def editing():
	id = request.args.get("id")

	if request.method == "POST":
		if request.form.get("id") and request.form.get("content") and request.form.get("image") and request.form.get("description") and request.form.get("title"):
			document = Document.query.get(int(request.form.get("id")))
			filename = request.form.get("title")
			image = request.form.get("image")

			if not Path(os.path.join(WEBSITE_IMAGES_LOCATION,image)).exists():
				flash("Image doesn't exist in database",category="alert-warning")
				return redirect(url_for("admin.dashboard"))

			document.image_id = Images.query.filter_by(name=image).first().id
			document.title = filename
			document.brief_desc = request.form.get("description")
			
			db.session.add(document)
			try:
				db.session.commit()
				with open(os.path.join(WEBSITE_FILES_LOCATION,filename+".txt"),"w") as wfile:
					wfile.write(request.form.get("content"))
			except IntegrityError:
				db.session.rollback()
				flash("Filename already in use",category="alert-info")
				return redirect(url_for("admin.dashboard"))

			flash("Done",category="alert-success")

			return redirect(url_for("admin.dashboard"))
		else:
			flash("All fields must be filled",category="alert-info")
			return redirect(url_for("admin.dashboard"))
	if id:
		document = Document.query.get(int(id))
		if document:
			description = document.brief_desc
			title = document.title
			image = document.thubnail.name

			content = ""
			with open(os.path.join(WEBSITE_FILES_LOCATION,document.title+".txt"),"r") as rfile:
				content = rfile.read().encode("utf8")

			return render_template("/admin/templates/dashboard_templates/editing_view.html",content=content,title=title,description=description,image=image,id=id)
	
	flash(f"Document with id {id} not found")
	return redirect(url_for("admin.dashboard"))


@admin.route("/upload/delete/")
@admin_decorator
def delete():
	iid = request.args.get("id")
	if iid:
		obj = Document.query.get(int(iid))
		os.remove(os.path.join(os.environ.get("WEBSITE_FILES_LOCATION"),obj.title+".txt"))

		db.session.delete(obj)
		db.session.commit()
	return redirect(url_for("admin.homepage"))


@admin.route("/statistics/")
@admin_decorator
def statistics():
	top_ten = Statistics.query.session.execute(""" select page_title as title,count(*) as num from statistics group by title order by num desc limit 10""") 
	last_7_days = datetime.utcnow() - timedelta(days=8)
	visitors_this_week = Statistics.query.session.execute(""" select count(*) as num from statistics where date > :param """,{"param":last_7_days.isoformat()})
	stats = {"top_ten":top_ten,"visitors_this_week":visitors_this_week}
	stats = {"visitors_this_week":visitors_this_week.fetchone(),"top_ten":top_ten.fetchall()}

	return render_template("/admin/templates/dashboard_templates/statistics_display.html",stats=stats)

@admin.route("/comments/",methods=["GET","POST"])
@admin_decorator
def comments():

	

	article = request.args.get("title")
	comments = None
	if article:
		document = Document.query.filter_by(title=article).first()
		if document:
			comments = Comments.query.filter_by(document_id=document.id).all()
		else:
			comments = []
	else:
		comments = Comments.query.all()
	
	return render_template("admin/templates/dashboard_templates/comments.html",contents=comments)

@admin.route("/comments/delete/")
@admin_decorator
def delete_comment():
	comment_id = request.args.get("id")
	
	if comment_id:
		comment_obj = Comments.query.get(int(comment_id))
		db.session.delete(comment_obj)
		db.session.commit()
		
		flash("Comment deleted",category="alert-success")
		
	return "Done"

@admin.route("/customers/")
@admin_decorator
def customers():
	customer_id = request.args.get("id")
	if customer_id:
		user = User.query.get(customer_id)
		if user:
			return render_template("admin/templates/user_profile.html",user=user)

	customers = User.query.session.execute("select id,first_name,last_name,username,registration_date from Users where first_name != 'admin' ")
	
	return render_template("admin/templates/dashboard_templates/customers.html",contents=customers)

@admin.route("/customers/delete/")
@admin_decorator
def delete_customer():
	customer_id = request.args.get("id")
	
	if customer_id:
		customer_obj = Users.query.get(int(comment_id))
		db.session.delete(customer_obj)
		db.session.commit()
		
		flash("Comment deleted",category="alert-success")
		
	return "Done"