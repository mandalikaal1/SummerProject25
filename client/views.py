from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
import sqlite3

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
    session.pop("name", None)
    session.pop("role", None)
    print("logout")
    return redirect(url_for("views_bp.index"))


