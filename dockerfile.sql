#Dockerfile.sql

# Build stage for SQL Server container
FROM mcr.microsoft.com/mssql/server AS sql-server-builder

# Set the working directory
WORKDIR /docker-entrypoint-initdb.d/


# Copy the SQL script
COPY create_tables.sql .

# Copy the entrypoint script



# Entrypoint script to wait for SQL Server to be ready before running scripts
