import requests

res = requests.get("http://127.0.0.1:5000/download?filename=encrypted_sample.csv")
print(res.text)  # prints the full JSON response with the full signed URL
