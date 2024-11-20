""" Script for downloading historical food truck transaction data """

from datetime import datetime, timedelta, timezone
import botocore
import botocore.exceptions
from boto3 import client


def create_s3_client(access_key_id: str, secret_access_key: str) -> client:
    """
    Creates an S3 client using an AWS Access Key.
    """
    try:
        return client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Error creating S3 client: {e}") from e


def get_bucket_files(s3_client: client, bucket_name: str) -> dict:
    """
    Retrieves information on the files in an s3 bucket.
    """
    try:
        return s3_client.list_objects_v2(Bucket=bucket_name, Prefix="trucks")
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Error retrieving files from the S3 bucket: {e}") from e


def download_truck_data_files(
    bucket_files: dict, s3_client: client, bucket_name: str, path: str
):
    """
    Downloads all the relevant files from the specified bucket, to the
    specified path, retaining only the name.
    """

    for file in bucket_files["Contents"]:
        filename_and_folder = file["Key"]
        filename = file["Key"].split("/")[-1]
        creation_date = file["LastModified"]

        if is_relevant_file(filename_and_folder) and is_new_batch(creation_date):
            s3_client.download_file(
                bucket_name, filename_and_folder, f"{path}{filename}"
            )


def is_relevant_file(filename: str) -> bool:
    """
    Returns True if the filename matches the specified format,
    otherwise returns False.
    """
    return filename.endswith(".csv")


def is_new_batch(file_creation_date: datetime) -> bool:
    """
    Returns True if the file was added to the S3 Bucket in
    last 3 hours, otherwise returns False.
    """
    hour_ago = datetime.now(timezone.utc) - timedelta(hours=3)
    return hour_ago < file_creation_date
