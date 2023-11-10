# DataTransferTest

This repository contains scripts for managing data, including uploading CSV files to Amazon S3 and populating a SQL Server database. Additionally, it provides API endpoints for querying specific cases using Flask.

# Data Processing and API Project

This project involves processing CSV files, uploading them to an SQL Server database, and providing access to the data through a Flask API. Here are some considerations to set up the required components:

## SQL Server Database

1. **Database Configuration:**
   - Make sure you have an SQL Server database instance set up.
   - Ensure you have the necessary credentials (username and password) and connection details.

2. **Table Structure:**
   - The project assumes the existence of three tables: `departments`, `jobs`, and `employees`. Make sure these tables are created in your SQL Server database.

3. **AWS CLI Configuration:**
   - Install AWS CLI on your local machine.
   - Configure AWS CLI with the necessary credentials using `aws configure`.

## AWS S3 Bucket

1. **S3 Bucket Setup:**
   - Create an S3 bucket to store the CSV files. In this project, the bucket is assumed to be named `config-bucket-550514509590`.

2. **Folder Structure:**
   - Organize your CSV files within the S3 bucket. This project assumes the CSV files are located in the `DataTests/` folder.

3. **IAM User Permissions:**
   - Create an IAM user with the necessary permissions to perform read and write operations in the S3 bucket.
   - Attach the required policies (e.g., AmazonS3FullAccess) to the IAM user.
4. **Lambda Deployment Package:**
   - Clone this repository to your local machine.
## Running the Project

1. **Local Setup:**
   - Install the required Python packages listed in `requirements.txt` using `pip install -r requirements.txt`.

2. **Database Connection:**
   - Update the connection details in the Python scripts (`db_upload.py` and `output_api.py`) to match your SQL Server setup.

3. **AWS CLI Configuration:**
   - Make sure the AWS CLI on your local machine is configured correctly.

4. **Run the Scripts:**
   - Execute `api.py` to upload CSV data to the S3 bucket whit an api endpoint .
   - Execute `db_upload.py` to upload CSV data to the SQL Server database.
   - Run `outputapi.py` to start the Flask API.

5. **Access the API:**
   - Use tools like Postman or your preferred method to make API requests to the provided endpoints.
6. **Lambda Function Structure**

- **lambda.py:** Python script containing the Lambda function code.
- **requirements.txt:** List of Python packages required for the Lambda function.

### Using the `db_upload` API

To use the `db_upload` API:

1. **Endpoint:**
   - The `db_upload` API is available at `http://localhost:5000/upload`.

2. **Method:**
   - Use the HTTP POST method to upload CSV files to the SQL Server database.

3. **Payload:**
   - Send a POST request with the CSV file as part of the payload.

4. **Handling Null Data:**
   - The API script (`db_upload.py`) handles null data and includes conditions to replace null values with appropriate default values.

5. **Example Request (using curl):**
   ```bash
   curl -X POST -F "file=@/path/to/your/file.csv" http://localhost:5000/upload
## Installing Dependencies

Before deploying the Lambda function, you need to install the required dependencies (libraries) locally and include them in the deployment package.

```bash
# Navigate to the Lambda function directory
cd path/to/lambda_function

# Install dependencies locally
pip install pandas pyodbc -t .

# Create a ZIP archive for Lambda deployment
zip -r lambda_function.zip .

