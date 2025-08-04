from flask import Blueprint, render_template, redirect, url_for

views_bp = Blueprint("views_bp", __name__, 
                     template_folder ="templates",  
                     static_folder='static')


@views_bp.route("/")
def index():
    return render_template("index.html")

@views_bp.route("/create_account")
def create_account():
    return render_template("create_account.html")

@views_bp.route("/home")
def home(): 
    return render_template("home.html")

@views_bp.route("/upload_file")
def upload_file(): 
    return render_template("upload_file.html")


@views_bp.route("/view_data")
def view_Data(): 
    return render_template("view_data.html")

@views_bp.route("/logout")
def logout(): 
    return redirect(url_for("views_bp.index"))


