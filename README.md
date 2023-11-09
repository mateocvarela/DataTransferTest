# DataTransferTest

This repository contains scripts for managing data, including uploading CSV files to Amazon S3 and populating a SQL Server database. Additionally, it provides API endpoints for querying specific cases using Flask.

# Scripts
# 1. api.py
This script is responsible for uploading a local CSV file to Amazon S3.

Usage:
bash
python api.py /path/to/local/file.csv s3://your-s3-bucket/your-s3-key/file.csv

# 2. db_upload.py
This script retrieves CSV files from Amazon S3 and uploads them to a SQL Server database.

# Prerequisites:
SQL Server database connection settings configured in the script.
Usage:
bash
python db_upload.py
# 3. output_api.py
This script provides Flask API endpoints for querying specific cases on the populated SQL Server database.

Prerequisites:
Flask installed (pip install Flask)
API Endpoints:
Case 1: Number of employees for each job and department in 2021 divided by quarters

Endpoint: /api/case1
Method: GET
Case 2: List of IDs, name, and number of employees hired for each department

Endpoint: /api/case2
Method: GET
# SQL Queries
The sql.txt file contains SQL queries used by the Flask API for querying the database.

# Getting Started
Clone the repository:

git clone https://github.com/mateocvarela/DataTransferTest.git
Navigate to the repository:


cd your-repository
Install dependencies:

pip install -r requirements.txt
Run the scripts as described in the individual sections above.

