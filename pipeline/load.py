import os
import redshift_connector
import pandas as pd


def get_data(filename: str, path: str) -> list:
    """Opens a .csv and returns the data as a Pandas dataFrame"""
    return pd.read_csv(f"{path}{filename}")


def replace_payment_method(
    transactions_df: pd.DataFrame, mapping: dict
) -> pd.DataFrame:
    """Replaces the payment method name with the corresponding payment method id"""
    transactions_df["type"] = transactions_df["type"].map(mapping)
    return transactions_df


def convert_df_to_tuple(transactions_df: pd.DataFrame) -> list[tuple]:
    """Converts the transactions dataFrame into a list of tuples."""
    return transactions_df.apply(tuple, axis=1).tolist()


def get_connection() -> redshift_connector.Connection:
    """Creates a database session and returns a connection object"""
    return redshift_connector.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def get_payment_method_ids(connection: redshift_connector.Connection) -> dict:
    """Returns a payment method ID mapping."""
    with connection.cursor() as cursor:
        cursor.execute("""SELECT name, id FROM eyuale_schema.payment_method""")
        result = cursor.fetchall()

    return {row[0]: row[1] for row in result}


def upload_transaction_data(
    data: list[tuple], connection: redshift_connector.Connection
) -> None:
    """Uploads transaction data to the database."""
    with connection.cursor() as cursor:

        stmt = """INSERT INTO eyuale_schema.transaction (truck_id, timestamp, payment_method_id, total)
                VALUES (%s, %s, %s, %s)"""
        cursor.executemany(stmt, data)

    connection.commit()
