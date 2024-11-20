"""Code for generating truck performance reports"""

from datetime import datetime, timedelta
import pandas as pd
import redshift_connector
from dotenv import load_dotenv
from connect import get_connection


def get_yesterdays_date() -> str:
    """Returns yesterdays date as a string"""

    yesterday_date = datetime.now() - timedelta(days=1)
    return yesterday_date.strftime("%Y-%m-%d")


def get_transaction_data(
    connection: redshift_connector.Connection, date: str
) -> pd.DataFrame:
    """Retrieves transaction data from a specific day, from the database, and returns it as
    a Pandas DataFrame."""

    try:
        with connection.cursor() as cur:

            cur.execute(
                f"SELECT * FROM eyuale_schema.transaction WHERE DATE(timestamp) = '{date}'"
            )
            data = cur.fetchall()

        return pd.DataFrame(
            data, columns=["id", "truck_id", "timestamp", "type", "total"]
        )

    except redshift_connector.Error as e:
        raise redshift_connector.Error(
            f"Error retrieving data from Redshift: {e}"
        ) from e

    finally:
        connection.close()


def calculate_active_hours(transaction_data: pd.DataFrame) -> pd.Series:
    """Calculates the active hours for each truck, and returns them."""

    time_difference = transaction_data.groupby("truck_id")["timestamp"].apply(
        lambda x: x.max() - x.min()
    )
    active_hours = time_difference.apply(lambda x: x.total_seconds() / 3600)

    return active_hours


def get_average_hourly_revenue_per_truck(transaction_data: pd.DataFrame) -> dict:
    """Returns a dictionary with the average hourly revenue for each truck."""

    active_hours = calculate_active_hours(transaction_data)
    total_trans_value_per_truck = transaction_data.groupby("truck_id")["total"].sum()

    return (total_trans_value_per_truck / active_hours).round(2).to_dict()


def generate_html_report(transaction_data: pd.DataFrame, date: str) -> str:
    """Generates an HTML report string directly from the transaction data."""

    total_transactions = transaction_data["id"].nunique()
    total_transaction_value = transaction_data["total"].sum().round(2)

    avg_trans_value_per_truck = (
        transaction_data.groupby("truck_id")["total"].mean().round(2).to_dict()
    )
    num_trans_per_truck = transaction_data.groupby("truck_id").size().to_dict()

    avg_revenue_per_hour_per_truck = get_average_hourly_revenue_per_truck(
        transaction_data
    )

    truck_names = {
        1: "Burrito Madness",
        2: "Kings of Kebabs",
        3: "Cupcakes by Michelle",
        4: "Hartmann's Jellied Eels",
        5: "Yoghurt Heaven",
        6: "SuperSmoothie",
    }

    html = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Truck Performance Report</h1>
        <h2>Date: {date}</h2>

        <table>
            <tr>
                <th>Truck Name</th>
                <th>Number of Transactions</th>
                <th>Average Transaction Value</th>
                <th>Average Revenue per Hour</th>
            </tr>
    """

    for truck_id, truck_name in truck_names.items():
        html += f"""
            <tr>
                <td>{truck_name}</td>
                <td>{num_trans_per_truck.get(truck_id, 0)}</td>
                <td>£{avg_trans_value_per_truck.get(truck_id, 0.00)}</td>
                <td>£{avg_revenue_per_hour_per_truck.get(truck_id, 0.00)}</td>
            </tr>
        """

    html += f"""
        </table>
        <p><b>Total No. Transactions (all trucks):</b> {total_transactions}</p>
        <p><b>Total Transaction Value (all trucks):</b> £{total_transaction_value}</p>
        </body>
        </html>
        """

    return html


if __name__ == "__main__":

    load_dotenv()

    conn = get_connection()

    date = get_yesterdays_date()

    transactions = get_transaction_data(conn, date)
    transactions["total"] = pd.to_numeric(transactions["total"])

    html_report = generate_html_report(transactions, date)

    filename = f"report_data_{date}.html"

    with open(f"report/{filename}", "w", encoding="utf-8") as html_file:
        html_file.write(html_report)
