import pandas as pd
from encryption_utils import encrypt_text, decrypt_text
import os
from flask import Flask, request, jsonify, send_file, session
from google.cloud import storage
from datetime import timedelta
from google.oauth2 import service_account

#import client routes
from client.views import views_bp
from connect import connect_bp

 
#-----------file for project
file_name = "patient.csv"
encrypted_filename = "encrypted_" + file_name
download_filename = "download_"+ file_name

#----------files path for files
#upload path for GCS
local_encrypted_path = os.path.join("uploads", encrypted_filename)

#download path for GCS
local_download_path = os.path.join("downloads", download_filename)


#--------------GCS config
GCS_CREDENTIALS = "summer25project-6eb8d5472350.json"
GCS_BUCKET_NAME = "summer25project"

#-------------Initialize GCS client variables ------ see gcs_init() 
storage_client = ""
bucket = ""
credentials = ""


#-------------Flask app init ---- relocate static folder in client.views
app = Flask(__name__, static_folder=None)

#------------Sessions variable key 
app.secret_key = "secret_key_cloud_test" 

#--------------import routes
app.register_blueprint(views_bp)
app.register_blueprint(connect_bp)


#------------------------------------------------------
#----------- initialize to GCS client variables
#--------------GCS config
#------------------------------------------------------

def gcs_init():
 
    try: 
        #----- set global GCS variables
        storage_client = storage.Client.from_service_account_json(GCS_CREDENTIALS)
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        credentials = service_account.Credentials.from_service_account_file(GCS_CREDENTIALS)

        return True

    except: 
        print("GCS Init fail")
        return False

#-------------------------------------------------
# ------------- Download file from GCS 
#-------------------------------------------------
def download_blob(bucket, local_path):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(f"encrypted/{encrypted_filename}")

    if not blob.exists():
        print("GCS Init fail")
        return False 

    
    try: 
        blob.download_to_filename(local_path) 
        print("Download from GCS success")
        return True
    except:
        return False
   

#------------------------------------------------------
#---------Retrieve Data from GCS or local folder
#------------------------------------------------------
@app.route("/retrieve_data")
def get_static_data():
    
    if(gcs_init()):
   
      #retrieve data from GCS
      try:
          download_blob(bucket, local_download_path)
          
          #convert file from "downloads" folder to dataframe
          df = pd.read_csv(local_download_path)
          print("Success! Retrieved from GCS")
      except:
          return jsonify({"message": f"File '{file_name}' not found in GCS"}), 404
      
        
      
    else:
      #open encrypted file locally
      df = pd.read_csv(local_encrypted_path)
      print("Retrieve from local file")
    
    
    #decrypt file
    columns_to_decrypt = [
        'Name', 'Gender', 'Blood Type', 'Medical Condition',
        'Doctor', 'Insurance Provider', 'Billing Amount',
        'Room Number', 'Medication', 'Test Results'
    ]
    

    for col in columns_to_decrypt:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(decrypt_text)


    #fix the dates after decrypt
    dates = ["Date of Admission", "Discharge Date"]
    for col in dates:
        df[col] = df[col].str.replace('/', '-')

    #filter data by user
    if(session['role'] == "Patient"):
        final_df = df[df['Name'].str.lower() == session['name'].lower()]
          
    elif(session['role'] == "Doctor"):
        final_df = df[df['Doctor'].str.lower() == session['name'].lower()]
        
    elif(session['role'] == "Admin"):
        final_df = df.copy()
        
    else:
        #data not found = empty dataset
        final_df = pd.Dataframe()
        
    #display uploaded file
    json_output_path = os.path.join('json', 'decrypt_output.json')
    final_df.to_json(json_output_path, orient='records', indent=2)
    
    return  send_file(json_output_path)
    
    

#------------------------------------------------------
#---------Upload data to GCS or local folder
#------------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload_file():


    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    #convert file to dataframe
    df = pd.read_csv(file)
    
    columns_to_encrypt = [
        'Name', 'Gender', 'Blood Type', 'Medical Condition',
        'Doctor', 'Insurance Provider', 'Billing Amount',
        'Room Number', 'Medication', 'Test Results'
    ]

    for col in columns_to_encrypt:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(encrypt_text)

   
    df.to_csv(local_encrypted_path, index=False)

    # ⬆️ Upload original + encrypted to GCS

    if(gcs_init()):
        
        encrypted_blob = bucket.blob(f"encrypted/{encrypted_filename}")

        encrypted_blob.upload_from_filename(local_encrypted_path)

        return jsonify({
        "message": "File encrypted and uploaded to GCS!",
        "encrypted_file_gcs_path": f"gs://{GCS_BUCKET_NAME}/encrypted/{encrypted_filename}",
        }), 200

    else:
        #gcs error - use local folder
        return jsonify({
            "message": "File encrypted and uploaded to local file!",
            "encrypted_file_gcs_path": None
        }), 200


#------------------------------------------------------
#--------- download link function
#------------------------------------------------------

@app.route("/download", methods=["GET"])
def generate_download_link():
 
    credentials = service_account.Credentials.from_service_account_file(GCS_CREDENTIALS)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(f"encrypted/{encrypted_filename}")

    if not blob.exists():
        return jsonify({"error": f"File '{encrypted_filename}' not found"}), 404


    url = blob.generate_signed_url(
        version="v4",  # ✅ THIS MATTERS
        expiration=timedelta(minutes=15),
        method="GET",
        credentials=credentials  # ✅ Make sure it uses the same creds
    )
    
    
    return url, 200, {'Content-Type': 'text/plain'}



if __name__ == "__main__":
    app.run(debug=True)
  

  