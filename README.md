# Food Truck Transaction Analytics

## Project Overview

This project is designed to analyse transaction data from food trucks. It consists of three main components:

1. **Pipeline**: Extracts, transforms, and loads (ETL) sales data into a Redshift database.
2. **Dashboard**: A Streamlit-based dashboard for visualising transaction data.
3. **Report Generator**: Generates performance reports for food trucks based on their transaction data.

Each component has its own detailed README file with specific instructions for installation and usage.

## Environment Setup

Ensure you have a `.env` file in the root directory with the following variables:

```plaintext
# AWS Access
ACCESS_KEY=<your_aws_access_key>
SECRET_ACCESS_KEY=<your_aws_secret_access_key>
DATA_PATH=<local_data_path>
S3_BUCKET=<your_s3_bucket_name>

# AWS Redshift Access
DB_HOST=<your_redshift_host>
DB_PORT=<your_redshift_port>
DB_NAME=<your_database_name>
DB_USER=<your_redshift_username>
DB_PASSWORD=<your_redshift_password>
```

## Running the Project

Refer to the detailed README files in the `pipeline`, `dashboard`, and `report` directories for specific instructions on running each component.