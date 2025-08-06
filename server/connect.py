from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from client.views import views_bp
connect_bp = Blueprint("connect_bp", __name__)



#database table

db_locale = 'db.sqlite'

@connect_bp.route("/checkUser", methods=["POST"])
def checkUser():    
    if request.method =='POST':
      
      name = request.form["username"]
      password = request.form["password"]
      result = sqlite_test(name, password)
      
      if result: 

        session['name'] = result['first_name'] + ' ' + result['last_name']
        print(session['name'])
        session['role'] = result['role']
        print(session['role'])
        
        return jsonify({
            "message": "Success",
        }), 200
          

      else:
          return jsonify({
              "message": "Username/Password is Incorrect. Please try again.",
          }), 200

        
     

def sqlite_test(formName, formPassword): 
    conn = sqlite3.connect(db_locale)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
   
    
    query = "SELECT * FROM ids WHERE username='"+formName+"' and password='"+formPassword+"'"
    c.execute(query)
    results = c.fetchone()
    
    conn.close()
    
    return results


# def check_password(db_password, form_password):
#     if check_password_hash(db_password, form_password):
#        # Passwords match, user is authenticated
#        print("Login successful!")
#        return True
#     else:
#        # Passwords do not match
#        print("Invalid credentials.")
#        return False


