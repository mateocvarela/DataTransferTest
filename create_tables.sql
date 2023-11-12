-- create_tables.sql

USE DataTestDB;
GO

-- Create Employees table
CREATE TABLE employes (
    employee_id (INT,null),
    name VARCHAR(50,null),
    hired_date(datetime2(7),null),
    departmen_id (INT,null),
    job_id (INT,null)
);

-- Create Jobs table
CREATE TABLE jobs (
    job_id (INT,null),
    job (VARCHAR(50),null)
);

-- Create Departments table
CREATE TABLE departments (
    id (INT,null),
    departments (VARCHAR(255),null)
);
