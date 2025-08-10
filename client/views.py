from flask import Blueprint,  render_template, redirect, url_for, session

views_bp = Blueprint("views_bp", __name__, 
                     template_folder ="templates",  
                     static_folder='static')


#-------------------------------------------------
# ----- Index 
#-------------------------------------------------
@views_bp.route("/")
def index():    
    return render_template("index.html")

#-------------------------------------------------
# ----- Create Account 
#-------------------------------------------------
@views_bp.route("/create_account")
def create_account():
    return render_template("create_account.html")

#-------------------------------------------------
# ----- home 
#-------------------------------------------------
@views_bp.route("/home")
def home(): 
    return render_template("home.html")

#-------------------------------------------------
# ----- Upload file 
#-------------------------------------------------
@views_bp.route("/upload_file")
def upload_file(): 
    return render_template("upload_file.html")

#-------------------------------------------------
# ----- View Data 
#-------------------------------------------------
@views_bp.route("/view_data")
def view_Data(): 
    return render_template("view_data.html")

#-------------------------------------------------
# ----- logout  
#-------------------------------------------------
@views_bp.route("/logout")
def logout(): 
    
    #remove session variables
    session.pop("name", None)
    session.pop("role", None)
    print("logout")
    return redirect(url_for("views_bp.index"))


