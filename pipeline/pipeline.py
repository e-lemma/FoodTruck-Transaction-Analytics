""" ETL script for T3 trucks sales data """

import os
import logging
from dotenv import load_dotenv
import extract_batch
import transform_batch
import load

NEW_FILENAME = "TRUCK_DATA_HIST_MERGED.csv"


def setup_logger() -> logging.getLogger:
    """returns a configured logger."""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("pipeline")


def main():

    logger = setup_logger()

    try:

        # Loading environment variables from .env file
        load_dotenv()

        aws_access_key_id = os.getenv("ACCESS_KEY")
        aws_secret_access_key = os.getenv("SECRET_ACCESS_KEY")

        data_path = os.getenv("DATA_PATH")
        truck_bucket_name = os.getenv("S3_BUCKET")

        # Creating S3 client
        s3 = extract_batch.create_s3_client(aws_access_key_id, aws_secret_access_key)
        # Downloading relevant csv files from the truck bucket
        truck_bucket_info = extract_batch.get_bucket_files(s3, truck_bucket_name)
        extract_batch.download_truck_data_files(
            truck_bucket_info, s3, truck_bucket_name, data_path
        )

        transaction_data_filenames = transform_batch.get_all_csv_filenames(data_path)

        if transaction_data_filenames:

            logger.info("New data batch found.")

            # Combines the data files into one CSV
            transform_batch.combine_transaction_data_files(
                transaction_data_filenames, data_path, NEW_FILENAME
            )

            transform_batch.remove_csv_files(transaction_data_filenames, data_path)

            conn = load.get_connection()
            logger.info("Connected to Redshift.")

            transactions_df = load.get_data(NEW_FILENAME, data_path)
            # Retrieves the payment method mapping
            mapping = load.get_payment_method_ids(conn)
            # Applies mapping
            transactions_df_formatted = load.replace_payment_method(
                transactions_df, mapping
            )

            transactions_tuples = load.convert_df_to_tuple(transactions_df_formatted)

            load.upload_transaction_data(transactions_tuples, conn)
            logger.info("Uploaded transaction data to Redshift.")

            conn.close()
            logger.info("Connection to Redshift closed.")

        else:
            logger.info("No data batch to upload.")

    except Exception as e:
        logger.error("An error occurred: %s", e, exc_info=True)


if __name__ == "__main__":
    main()
