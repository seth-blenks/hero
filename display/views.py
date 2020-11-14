from .blueprint import main
from flask import render_template,redirect,g,abort,flash,url_for,send_from_directory,request
from database import Document,User,Comments,db,Subscribers,Statistics
from flask_login import current_user
import os
from markdown import markdown
import bleach
from datetime import datetime,timedelta




@main.route("/analytic chemistry")
def analytic_chemistry():
	page = request.args.get("page",1,type=int)

	pagination = Document.query.filter_by(category="Analytic Chemistry").order_by(Document.id.desc()).paginate(page,6,error_out=False)
	articles = pagination.items
	more_content = Document.query.session.execute(""" select * from articles  order by time_of_production limit 8 """)
	if articles == []:
		if current_user.is_authenticated:	
			if current_user.has_permission(os.environ.get("ADMIN_PERM_VALUE")):
				
				flash("No article yet upload one")
				return redirect("admin.dashboard")
	return render_template("user_templates/templates/homepage.html",contents=articles,pagination=pagination,more_content=more_content)

@main.route("/physical chemistry")
def physical_chemistry():
	page = request.args.get("page",1,type=int)

	pagination = Document.query.filter_by(category="Physical Chemistry").order_by(Document.id.desc()).paginate(page,6,error_out=False)
	articles = pagination.items
	more_content = Document.query.session.execute(""" select * from articles  order by time_of_production limit 8 """)
	if articles == []:
		if current_user.is_authenticated:	
			if current_user.has_permission(os.environ.get("ADMIN_PERM_VALUE")):
				
				flash("No article yet upload one")
				return redirect("admin.dashboard")
	return render_template("user_templates/templates/homepage.html",contents=articles,pagination=pagination,more_content=more_content)

@main.route("/organic chemistry")
def organic_chemistry():
	page = request.args.get("page",1,type=int)

	pagination = Document.query.filter_by(category="Organic Chemistry").order_by(Document.id.desc()).paginate(page,6,error_out=False)
	articles = pagination.items
	more_content = Document.query.session.execute(""" select * from articles  order by time_of_production limit 8 """)
	if articles == []:
		if current_user.is_authenticated:	
			if current_user.has_permission(os.environ.get("ADMIN_PERM_VALUE")):
				
				flash("No article yet upload one")
				return redirect("admin.dashboard")
	return render_template("user_templates/templates/homepage.html",contents=articles,pagination=pagination,more_content=more_content)

@main.route("/practical chemistry")
def practical_chemistry():
	page = request.args.get("page",1,type=int)

	pagination = Document.query.filter_by(category="Practical Chemistry").order_by(Document.id.desc()).paginate(page,6,error_out=False)
	articles = pagination.items
	more_content = Document.query.session.execute(""" select * from articles  order by time_of_production limit 8 """)
	if articles == []:
		if current_user.is_authenticated:	
			if current_user.has_permission(os.environ.get("ADMIN_PERM_VALUE")):
				
				flash("No article yet upload one")
				return redirect("admin.dashboard")
	return render_template("user_templates/templates/homepage.html",contents=articles,pagination=pagination,more_content=more_content)


@main.route("/")
def cover():
	return render_template("user_templates/templates/cover.html")


	

@main.route("/articles/<filename>",methods=["GET","POST"])
def getfile(filename):

	file = Document.query.filter_by(title=filename.split(".",1)[0]).first()
	
	more_content = Document.query.session.execute(""" select articles.title,articles.brief_desc,images.location,articles.time_of_production from articles inner join images where articles.image_id = images.id order by time_of_production limit 5 """)

	if not file:
		abort(404)

	if request.method == "POST":
		if not current_user.is_authenticated :
			flash("You need to login to be able to post comments",category="alert-warning")
			comments = Comments.query.filter_by(document_id = file.id).all()
			
			
			return render_template("user_templates/templates/post.html",comments=comments)
			return redirect("url_for")

		message = request.form["message"]
		

		if message:
			new_comment = Comments()
			new_comment.name = current_user.username
			new_comment.email = current_user.email
			new_comment.message = message
			new_comment.document_id = file.id
			
			db.session.add(new_comment)
			db.session.commit()

			comments = Comments.query.filter_by(document_id = file.id).all()
			
			flash("Comment posted",category="alert-success")
			return render_template("user_templates/templates/post.html",comments=comments)
		else:
			flash("Fill all fields")
			return redirect(url_for("main.getfile",filename=filename))
	
	
	
	

	comment = Comments.query.filter_by(document_id = file.id).all()
	content = ""
	filename = file.title + ".txt"
	with open(os.path.join(file.location,filename),"r") as rfile:
		allowed_attributes = {"img":["src","alt"]}
		allowed_TAGS = ["p","h1","h2","h3","h4","h5","h6","ol","li","ul","b","br","hr","i","img","src","alt"]
		content = bleach.clean(markdown(rfile.read(),output_format="html"),tags=allowed_TAGS,attributes=allowed_attributes,strip=True)

	return render_template("user_templates/templates/blog-details.html",comments=comment, document=file,content=content,more_content=more_content)
@main.route("/lookup/")
def search():
	keyword = request.args.get("search")
	search_result = Document.query.filter_by(title=str(keyword).lower()).all()

	if not search_result:
		flash("not Found")
		return redirect(url_for("main.homepage"))
	
	return render_template("user_templates/templates/search.html",contents=search_result)

@main.route("/subscribe",methods=["POST"])
def subscribe():
	email = request.form.get("email")
	if email:
		if Subscribers.query.filter_by(email=email).first():
			flash("Already a subscriber of this service")
			return redirect(url_for("main.homepage"))
		new_subscriber = Subscribers()
		new_subscriber.email = email
		
		db.session.add(new_subscriber)
		db.session.commit()

		return redirect(url_for("main.homepage"))


@main.route("/stats/")
def stats():
	new_stats = Statistics()
	new_stats.page_title = request.args.get("title")
	db.session.add(new_stats)
	db.session.commit()
	return "Done"

@main.route('/shutdown')
def server_shutdown():
	shutdown = request.environ.get('werkzeug.server.shutdown')
	if shutdown:
		shutdown()
	return 'Shutting down...'

@main.app_errorhandler(404)
def page_not_found_error(e):
	return render_template("user_templates/templates/404.html"),404

