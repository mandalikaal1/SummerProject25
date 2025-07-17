import pandas as pd
from encryption_utils import encrypt_text
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    df = pd.read_csv(file_path)

    columns_to_encrypt = [
        'Name', 'Gender', 'Blood Type', 'Medical Condition',
        'Doctor', 'Insurance Provider', 'Billing Amount',
        'Room Number', 'Medication', 'Test Results'
    ]

    for col in columns_to_encrypt:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(encrypt_text)

    encrypted_path = os.path.join("uploads", "encrypted_" + file.filename)
    df.to_csv(encrypted_path, index=False)

    return jsonify({"message": "File encrypted successfully", "encrypted_file": encrypted_path}), 200

if __name__ == "__main__":
    app.run(debug=True)