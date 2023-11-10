import pandas as pd
import pyodbc
import csv
import numpy as np
from sqlalchemy import create_engine
import boto3
from io import StringIO

def lambda_handler(event, context):
    # RDS database connection settings
    server = 'localhost'
    database = 'DataTestDB'
    db_port = '1433'
    username = 'master'
    password = 'master123'

    # List of CSV files to process
    csv_files = ['departments.csv', 'jobs.csv', 'hired_employees.csv']
    s3_bucket_name = 'config-bucket-550514509590'
    s3_folder_path = 'DataTests/'
    s3 = boto3.client('s3')

    # Specify the path to your local CSV file
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
    )
    connection = pyodbc.connect(connection_string)

    table_names = ['departments', 'jobs', 'employes']
    
    for record in event['Records']:
        # Retrieve S3 bucket and key information from the event record
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if key.startswith(s3_folder_path) and key.endswith('.csv'):
            # Fetch CSV file from S3
            csv_obj = s3.get_object(Bucket=bucket, Key=key)
            csv_body = csv_obj['Body']
            csv_string = csv_body.read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_string), header=None)

            # Process CSV based on table_name
            for csv_file, table_name in zip(csv_files, table_names):
                if key.endswith(csv_file):
                    if table_name == 'employes':
                        df.iloc[:, -2:] = df.iloc[:, -2:].replace([np.inf, -np.inf, np.nan], 0)
                        df.iloc[:, -2:] = df.iloc[:, -2:].apply(np.int64)
                        df.iloc[:, 1] = df.iloc[:, 1].replace([np.nan], ['not named'])
                        df.iloc[:, 2] = df.iloc[:, 2].replace([np.nan], ['1900-01-01T00:00:00Z'])

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

    return {
        'statusCode': 200,
        'body': 'Data processed successfully.'
    }