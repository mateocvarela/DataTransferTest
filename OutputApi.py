from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

# RDS database connection settings
server = 'localhost'
database = 'DataTestDB'
username = 'master'
password = 'Complexpasw1993*'

# Function to execute SQL queries
def execute_query(query):
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
    )

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    connection.close()
    return result,columns

# API route for Case 1
@app.route('/api/case1' ,methods=['GET'])
def case1():
    query = """
    SELECT D.[departments],J.[job],
	SUM(CASE WHEN DATEPART(QUARTER, hired_date) = 1 THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN DATEPART(QUARTER, hired_date) = 2 THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN DATEPART(QUARTER, hired_date) = 3 THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN DATEPART(QUARTER, hired_date) = 4 THEN 1 ELSE 0 END) AS Q4
  FROM [DataTestDB].[dbo].[employes] as E

 join [DataTestDB].[dbo].[departments] as D
	ON(E.department_id = D.id)
JOIN  [DataTestDB].[dbo].[jobs] as J
	ON(E.job_id = J.job_id)
	where YEAR (E.hired_date)=2021
	GROUP BY D.departments, J.job
	ORDER BY D.departments,J.job
    """
    result , columns = execute_query(query)
    result_list = [dict(zip(columns, row)) for row in result]
    response = jsonify(result_list)
    return response

# API route for Case 2
@app.route('/api/case2', methods=['GET'])
def case2():
    query = """
    WITH DepartmentSummary AS (
    SELECT
        d.id,
        d.departments,
        COUNT(e.employee_id) AS NumEmployees
    FROM
        employes e
    JOIN
        departments d ON e.department_id = d.id
    WHERE
        YEAR(e.hired_date) = 2021
    GROUP BY
        d.id, d.departments
)
SELECT
    d.id AS DepartmentID,
    d.departments AS DepartmentName,
    COUNT(e.employee_id) AS NumEmployeesHired
FROM
    employes e
JOIN
    departments d ON e.department_id = d.id
WHERE
    YEAR(e.hired_date) = 2021
    AND e.department_id IN (
        SELECT department_id
        FROM DepartmentSummary
        WHERE NumEmployees > (SELECT AVG(NumEmployees) FROM DepartmentSummary)
    )
GROUP BY
    d.id, d.departments
ORDER BY
    NumEmployeesHired DESC
    """
    result , columns = execute_query(query)
    result_list = [dict(zip(columns, row)) for row in result]
    response = jsonify(result_list)
    return response

if __name__ == '__main__':
    # Use Waitress as the production server
    from waitress import serve
    serve(app, host='0.0.0.0', port=5002)