from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


#------------create route for file
connect_bp = Blueprint("connect_bp", __name__)



#-------------------------------------------------
# ---- SQLite Database file
#-------------------------------------------------
db_locale = 'db.sqlite'


#-------------------------------------------------
# ------------- Download file from GCS 
#-------------------------------------------------
@connect_bp.route("/checkUser", methods=["POST"])
def checkUser():    
    if request.method =='POST':
      
      name = request.form["username"]
      password = request.form["password"]
  
      result = sqlite_test(name)
      
      if result: 
        if(check_password_hash(result['password'], password)):
            session['name'] = result['first_name'] + ' ' + result['last_name']
            session['role'] = result['role']
            
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


      
     
#-------------------------------------------------
# ------------- check if user is in database
#-------------------------------------------------
def sqlite_test(formName): 
    conn = sqlite3.connect(db_locale)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
   
    
    query = "SELECT * FROM ids WHERE username='"+formName+"'"
    c.execute(query)
    results = c.fetchone()
    
    #close database connection
    conn.close()
    
    return results

#---------------------------------------------------------
# ----------- retrieve data from "Create Account" page
#---------------------------------------------------------

@connect_bp.route("/createUser", methods=["POST"])
def createUser():    
    if request.method =='POST':
      username = request.form["username"]
      password = request.form["password"]
      firstName = request.form["firstname"]
      lastName = request.form["lastname"]
      role = request.form["role"]
 
      results = sqlite_addUser(username, password, firstName, lastName, role)
      if results: 
      
        return jsonify({
                  "message": "Success! Please login with new account.",
              }), 200
      else: 
         
        return jsonify({
            "message": "Username already exists. Please try another username.",
        }), 200
      
    else:
      return jsonify({
          "message": "Form error. Please try again.",
      }), 200
  

#---------------------------------------------------------
# -------- Add new user to SQLite database
#---------------------------------------------------------

def sqlite_addUser(username, password, firstName, lastName, role): 
    conn = sqlite3.connect(db_locale)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
   
    hashed_password = generate_password_hash(password)
    
    try: 
        #insert new user into database
        query = "INSERT INTO ids(username, password, first_name, last_name, role) VALUES('"+username+"', '"+hashed_password+"', '"+firstName+"', '"+lastName+"', '"+role+"')"
        c.execute(query)
        conn.commit()
    
        #check user is in the database
        query2 = "SELECT * FROM ids WHERE username='"+username+"'"
        c.execute(query2)
        results = c.fetchone()
  
        #close database connection
        conn.close()
        return results
    
    except sqlite3.Error as e: # Catch specific database errors
        print(f"Error during commit: {e}")
        if conn:
            conn.rollback() # Rollback changes if commit fails
            print("Transaction rolled back.")
        return False

    finally:
        if conn:
            conn.close() # Ensure the connection is closed
       
    
