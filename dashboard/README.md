# Food Truck Transaction Analytics Dashboard

## Project Overview

This is a Streamlit-based dashboard for analysing transaction data from food trucks. It includes various visualisations to help understand the transaction patterns, including bar charts, pie charts, and line charts.

## Installation

To install the necessary dependencies, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/e-lemma/FoodTruck-Transaction-Analytics.git
    cd FoodTruck-Transaction-Analytics/dashboard
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Environment Information

Ensure you have a `.env` file in the root directory with the following environment variables set:

```plaintext
DB_HOST=<your_redshift_host>
DB_NAME=<your_database_name>
DB_PORT=<your_database_port>
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
```

## Running the Project

To run the dashboard, use the following command:

```sh
streamlit run dashboard.py
```

This will start the Streamlit server and open the dashboard in your default web browser.

## Docker

Alternatively, you can run the project using Docker:

1. Build the Docker image:
    ```sh
    docker build -t foodtruck-dashboard .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 8501:8501 --env-file .env foodtruck-dashboard
    ```

This will start the Streamlit server inside a Docker container and make the dashboard accessible at `http://localhost:8501`.
