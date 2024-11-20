# Food Truck Transaction Analytics Report Generator

## Project Overview

This report generator is designed to generate performance reports for food trucks based on their transaction data. The reports provide insights into the number of transactions, average transaction value, and average revenue per hour for each truck.

## Installation

To install the necessary dependencies, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/e-lemma/FoodTruck-Transaction-Analytics.git
    cd FoodTruck-Transaction-Analytics/report
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Environment Information

Ensure you have the following environment variables set in a `.env` file:

```env
DB_HOST=your_redshift_host
DB_NAME=your_database_name
DB_PORT=your_database_port
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

## Running the Project

### Local Execution

To generate the report locally, run the `report_generator.py` script:

```sh
python report_generator.py
```

### AWS Lambda Execution

To deploy and run the project on AWS Lambda, follow these steps:

1. Build the Docker image:
    ```sh
    docker build -t food-truck-report-generator .
    ```

2. Push the Docker image to AWS ECR (Elastic Container Registry).

3. Create an AWS Lambda function and configure it to use the Docker image from ECR.

4. Set up the necessary environment variables in the Lambda function configuration.

5. Trigger the Lambda function to generate the report.

## Output

The generated HTML report will be saved in the `report` directory with the filename format `report_data_<date>.html`.
