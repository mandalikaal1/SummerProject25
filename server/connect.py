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
        if(check_password_hash(result['password'], password)):
            session['name'] = result['first_name'] + ' ' + result['last_name']
            print(session['name'])
            session['role'] = result['role']
            print(session['role'])
            
            return jsonify({
                "message": "Success",
            }), 200
        else:
          return jsonify({
              "message": "Password is Incorrect. Please try again.",
          }), 200
  
         
      else:
          return jsonify({
              "message": "Username/Password is Incorrect. Please try again.",
          }), 200

        
     

def sqlite_test(formName, formPassword): 
    conn = sqlite3.connect(db_locale)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
   
    
    query = "SELECT * FROM ids WHERE username='"+formName+"'"
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


@connect_bp.route("/createUser", methods=["POST"])
def createUser():    
    if request.method =='POST':
      username = request.form["username"]
      password = request.form["password"]
      firstName = request.form["firstname"]
      lastName = request.form["lastname"]
      role = request.form["role"]
      print(username, password, firstName, lastName, role)
      results = sqlite_addUser(username, password, firstName, lastName, role)
      if results: 
      
        return jsonify({
                  "message": "Success",
              }), 200
      
    else:
      return jsonify({
          "message": "Data error. Please try again.",
      }), 200
  


def sqlite_addUser(username, password, firstName, lastName, role): 
    conn = sqlite3.connect(db_locale)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    
    query = "INSERT INTO ids(username, password, first_name, last_name, role) VALUES('"+username+"', '"+hashed_password+"', '"+firstName+"', '"+lastName+"', '"+role+"')"
    c.execute(query)
    c.commit()
    
    #check if username was inserted into database
    query2 = "SELECT * FROM ids WHERE username='"+username+"'"
    c.execute(query2)
    results = c.fetchone()
 
    conn.close()
    return results
