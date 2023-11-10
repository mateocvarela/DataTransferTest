import pandas as pd
import pyodbc
import csv
import numpy as np
from sqlalchemy import create_engine
import boto3
from io import StringIO

# RDS database connection settings
server = 'localhost'
database = 'DataTestDB'
db_port='1433'
username = 'master'
password = 'master123'

# List of CSV files to process
csv_files = ['departments.csv','jobs.csv','hired_employees.csv']
s3_bucket_name = 'config-bucket-550514509590'
s3_folder_path = 'DataTests/'
s3 = boto3.client('s3')

# Specify the path to your local CSV file
#df = pd.read_csv('C:/Users/arqinfraestructura/Documents/Code_Challenge/Downloads/departments.csv',header=None, names=['id', 'departments'])
connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)
connection = pyodbc.connect(connection_string)

table_names = ['departments','jobs','employes' ]
# Generate the SQL query to insert data into the table
for csv_file, table_name in zip(csv_files, table_names):
    csv_obj = s3.get_object(Bucket=s3_bucket_name, Key=s3_folder_path + csv_file)
    csv_body = csv_obj['Body']
    csv_string = csv_body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string), header=None)
    #df = pd.read_csv(f'C:/Users/arqinfraestructura/Documents/Code_Challenge/Downloads/{csv_file}', header=None) #line for local testing
    if table_name == 'employes':
        df.iloc[:, -2:] = df.iloc[:, -2:].replace([np.inf, -np.inf, np.nan], 0)
        # Convert the last two columns (index -2 and -1) to integers
        df.iloc[:, -2:] = df.iloc[:, -2:].apply(np.int64) 
                # Handle empty values by replacing them with an empty string for the name column
        df.iloc[:, 1] = df.iloc[:, 1].replace([np.nan], ['not named'])
        
        # Handle empty values by replacing them with a specific date or datetime for the date column
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