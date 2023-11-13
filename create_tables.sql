-- create_tables.sql
CREATE DATABASE  DataTestDB;
GO
USE DataTestDB;
GO

CREATE LOGIN master WITH PASSWORD = 'Complexpasw1993*';
CREATE USER master_user FOR LOGIN master;
ALTER SERVER ROLE sysadmin ADD MEMBER master_user;

-- Create Employees table
CREATE TABLE employes (
    employee_id INT,
    name VARCHAR(50),
    hired_date datetime2(7),
    departmen_id INT,
    job_id INT
);

-- Create Jobs table
CREATE TABLE jobs (
    job_id INT,
    job VARCHAR(50)
);

-- Create Departments table
CREATE TABLE departments (
    id INT,
    departments VARCHAR(255)
);
