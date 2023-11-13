from flask import Flask, request, jsonify
import pandas as pd
import pyodbc
import numpy as np
from sqlalchemy import create_engine
# import boto3
from io import StringIO

app = Flask(__name__)

# Function to handle CSV file upload and database insertion
def process_csv_and_upload(csv_file, table_name):
    # RDS database connection settings
    server = 'localhost'
    database = 'DataTestDB'
    db_port = '1433'
    username = 'master'
    password = 'Complexpasw1993*'

    # S3 settings
    # s3_bucket_name = 'config-bucket-550514509590'
    # s3_folder_path = 'DataTests/'
    # s3 = boto3.client('s3')

    # Database connection
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
    )
    connection = pyodbc.connect(connection_string)

    # Retrieve the uploaded CSV file
    csv_data = request.files['file']
    csv_string = csv_data.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string), header=None)

    # Additional data processing logic
    if table_name == 'employes':
        df.iloc[:, -2:] = df.iloc[:, -2:].replace([np.inf, -np.inf, np.nan], 0)
        df.iloc[:, -2:] = df.iloc[:, -2:].apply(np.int64)
        df.iloc[:, 1] = df.iloc[:, 1].replace([np.nan], ['not named'])
        df.iloc[:, 2] = df.iloc[:, 2].replace([np.nan], ['1900-01-01T00:00:00Z'])

    # Generate the SQL query to insert data into the table
    placeholders = ', '.join(['?'] * len(df.columns))
    insert_query = f'INSERT INTO {table_name} VALUES ({placeholders})'

    # Create a cursor to execute the SQL query
    cursor = connection.cursor()

    # Loop through the DataFrame and insert each row into the SQL Server table
    for _, row in df.iterrows():
        cursor.execute(insert_query, *row)

    # Commit the changes to the database
    connection.commit()

    # Close the database connection
    connection.close()

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload():
    # Get the type of data from the request parameters
    data_type = request.args.get('type')

    # Validate data_type and process the corresponding CSV file and table
    if data_type == 'departments':
        process_csv_and_upload('departments.csv', 'departments')
    elif data_type == 'jobs':
        process_csv_and_upload('jobs.csv', 'jobs')
    elif data_type == 'hired_employees':
        process_csv_and_upload('hired_employees.csv', 'employes')
    else:
        return jsonify({'error': 'Invalid data type'})

    return jsonify({'message': 'Upload successful'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
