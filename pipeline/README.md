# Food Truck Transaction Analytics Pipeline

This pipeline is designed to extract, transform, and load (ETL) sales data from food trucks into a Redshift database for analysis. The pipeline processes transaction data, combines it into a single file, and uploads it to the database.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/e-lemma/FoodTruck-Transaction-Analytics.git
    cd FoodTruck-Transaction-Analytics/pipeline
    ```

2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Environment Setup

Ensure you have a `.env` file in the root directory with the following variables:
```
# AWS Access
ACCESS_KEY=<your_aws_access_key>
SECRET_ACCESS_KEY=<your_aws_secret_access_key>
DATA_PATH=<local_data_path>
S3_BUCKET=<your_s3_bucket_name>


# AWS Redshift Access
DB_HOST=your-redshift-host
DB_PORT=your-redshift-port
DB_NAME=your-database-name
DB_USER=your-redshift-username
DB_PASSWORD=your-redshift-password
```
Make sure the .env file is placed in the root directory of the project, and that your AWS and Redshift credentials are correctly configured.

## Database Setup

Run the `schema.sql` script to set up the necessary tables in your Redshift database.

## Running the Pipeline

To run the pipeline, execute the following command:
```bash
python pipeline.py
```

This will trigger the following steps:

- **Extract**: Data is downloaded from the S3 bucket.
- **Transform**: Raw CSV data is cleaned and combined into a single file.
- **Load**: The transformed data is uploaded into the Redshift database.

You can monitor the process in the terminal. If any errors occur, they will be logged in the output.

## Docker

You can also run the pipeline using Docker. Build the Docker image and run the container:
```bash
docker build -t foodtruck-pipeline .
docker run --env-file .env foodtruck-pipeline
```

## Analysis

The `analysis.ipynb` notebook contains analyses of the processed data. Open it with Jupyter Notebook to explore the insights.

## Additional Notes

- The project is designed to handle CSV transaction data, but it can be adapted to handle other formats if needed.
- Ensure that your Redshift credentials and S3 credentials are kept secure and not hard-coded into the script.