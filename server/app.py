import pandas as pd
from encryption_utils import encrypt_text
import os
from flask import Flask, request, jsonify
from google.cloud import storage

# GCS config
GCS_CREDENTIALS = "secrets/summer25project-6eb8d5472350.json"
GCS_BUCKET_NAME = "summer25project"

# Initialize GCS client
storage_client = storage.Client.from_service_account_json(GCS_CREDENTIALS)
bucket = storage_client.bucket(GCS_BUCKET_NAME)

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save file locally (temp)
    local_upload_path = os.path.join("uploads", file.filename)
    file.save(local_upload_path)

   # file_path = os.path.join("uploads", file.filename)
   # file.save(file_path)

    #df = pd.read_csv(file_path)

    df = pd.read_csv(local_upload_path)

    columns_to_encrypt = [
        'Name', 'Gender', 'Blood Type', 'Medical Condition',
        'Doctor', 'Insurance Provider', 'Billing Amount',
        'Room Number', 'Medication', 'Test Results'
    ]

    for col in columns_to_encrypt:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(encrypt_text)

    #encrypted_path = os.path.join("uploads", "encrypted_" + file.filename)
    #df.to_csv(encrypted_path, index=False)
    encrypted_filename = "encrypted_" + file.filename
    local_encrypted_path = os.path.join("uploads", encrypted_filename)
    df.to_csv(local_encrypted_path, index=False)

    # ⬆️ Upload original + encrypted to GCS
    original_blob = bucket.blob(f"originals/{file.filename}")
    encrypted_blob = bucket.blob(f"encrypted/{encrypted_filename}")

    original_blob.upload_from_filename(local_upload_path)
    encrypted_blob.upload_from_filename(local_encrypted_path)

    return jsonify({
        "message": "File encrypted and uploaded to GCS!",
        "encrypted_file_gcs_path": f"gs://{GCS_BUCKET_NAME}/encrypted/{encrypted_filename}",
    }), 200
if __name__ == "__main__":
    app.run(debug=True)