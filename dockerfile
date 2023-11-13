# Use an official Python runtime as a parent image
FROM python:3.11


# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        gfortran \
    && rm -rf /var/lib/apt/lists/*

 # Install Microsoft ODBC Driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17   
# Update library cache
RUN ldconfig

RUN pip install --upgrade pip

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Copy Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port 5000 for the Flask app
EXPOSE 5000
EXPOSE 5001
EXPOSE 5002

# Set environment variables for AWS credentials
ENV AWS_ACCESS_KEY_ID=<apiacceskey>
ENV AWS_SECRET_ACCESS_KEY=<apisecretkey>
ENV AWS_DEFAULT_REGION=<Region>

# Set environment variables
ENV SERVER=localhost
ENV DATABASE=DataTestDB
ENV UID=master
ENV PWD=Complexpasw1993*

# Copy SQL script to create tables


# CMD to run Supervisor, which will start both api.py and db_upload.py
CMD ["/usr/bin/supervisord"]
