from flask import Flask, request, jsonify
from waitress import serve
import boto3
import os

app = Flask(__name__)

# AWS S3 configuration
AWS_BUCKET_NAME = "config-bucket-550514509590"
AWS_BUCKET_FOLDER = "DataTests"  # The folder where files will be stored in S3

s3 = boto3.client('s3')

@app.route('/upload', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Get the filename from the request
        file_name = file.filename

        # Upload the file to the specified S3 bucket and folder
        s3_key = f"{AWS_BUCKET_FOLDER}/{file_name}"
        s3.upload_fileobj(file, AWS_BUCKET_NAME, s3_key)

        return jsonify({"message": "File uploaded to S3 successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use Waitress to serve the Flask app
    serve(app, host='0.0.0.0', port=8080)

