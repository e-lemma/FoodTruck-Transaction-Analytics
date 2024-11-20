""" Functions for connecting to the database """

import os
import redshift_connector


def get_connection() -> redshift_connector.Connection:
    """Creates a database session and returns a connection object"""

    print("connecting to database...")
    return redshift_connector.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
