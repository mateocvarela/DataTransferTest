import pandas as pd
import pyodbc
import csv
from sqlalchemy import create_engine

# RDS database connection settings
server = 'localhost'
database = 'DataTestDB'
db_port='1433'
username = 'master'
password = 'master123'

# Specify the path to your local CSV file
df = pd.read_csv('C:/Users/arqinfraestructura/Documents/Code_Challenge/Downloads/departments.csv',header=None, names=['id', 'departments'])
connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)
connection = pyodbc.connect(connection_string)
print(df)
# Generate the SQL query to insert data into the table
insert_query = f'INSERT INTO departmentstest (id, departments) VALUES (?, ?)'

# Create a cursor to execute the SQL query
cursor = connection.cursor()

# Loop through the DataFrame and insert each row into the SQL Server table
for index, row in df.iterrows():
    cursor.execute(insert_query, row['id'], row['departments'])

# Commit the changes to the database
connection.commit()

# Close the database connection
connection.close()