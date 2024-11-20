""" Code for the Streamlit Dashboard"""

from dotenv import load_dotenv
import redshift_connector
import redshift_connector.error
import pandas as pd
import streamlit as st
from connect import get_connection
from charts import (
    get_bar_chart_of_total_trans_per_truck,
    get_pie_chart_of_transactions_by_day_of_week,
    get_line_chart_of_num_trans_per_truck_per_hour,
    get_line_chart_of_rev_per_truck_per_hour,
)


@st.cache_data
def get_data(_connection: redshift_connector.Connection) -> pd.DataFrame:
    """Retrieves transaction data from the database, and returns it as
    a Pandas DataFrame."""
    print("loading data...")
    try:
        with _connection.cursor() as cur:

            cur.execute("""SELECT * FROM eyuale_schema.transaction""")
            data = cur.fetchall()

        return pd.DataFrame(
            data, columns=["id", "truck_id", "timestamp", "type", "total"]
        )

    except redshift_connector.Error:
        st.error(
            f"Error fetching transaction data: {
                 redshift_connector.error}",
            icon="🚨",
        )
        return pd.DataFrame()

    finally:
        _connection.close()


def format_data(trans_data: pd.DataFrame) -> pd.DataFrame:
    """Returns the transaction data in the required format."""

    trans_data = trans_data.drop(columns=["id"])
    trans_data["total"] = pd.to_numeric(trans_data["total"])
    trans_data["timestamp"] = pd.to_datetime(trans_data["timestamp"])

    return trans_data


def main():
    """Runs the dashboard."""

    load_dotenv()

    conn = get_connection()
    if not conn:
        st.error("Failed to connect to database", icon="🚨")
        return

    raw_transactions = get_data(conn)
    if raw_transactions.empty:
        st.error("No data found in database!", icon="🚨")
        return

    transactions = format_data(raw_transactions)

    st.title("🚚 Tasty Truck Treats: :grey[Transaction Data Analytics]")

    col1, col2 = st.columns(2)

    with col1:
        st.altair_chart(get_bar_chart_of_total_trans_per_truck(transactions))

    with col2:
        st.altair_chart(get_pie_chart_of_transactions_by_day_of_week(transactions))

    st.subheader("Transactions by truck, hour")

    trucks = transactions.loc[:, "truck_id"].unique()
    selected_trucks = st.multiselect(
        "Select trucks to display", options=trucks, default=None
    )

    choice = st.radio(
        "Select an option to display graph", ["Revenue", "No. Transactions"]
    )

    if selected_trucks:

        filtered_trans = transactions.loc[
            transactions.loc[:, "truck_id"].isin(selected_trucks)
        ].copy()
        filtered_trans["hour"] = filtered_trans.loc[:, "timestamp"].dt.hour

        if choice == "No. Transactions":
            st.altair_chart(
                get_line_chart_of_num_trans_per_truck_per_hour(filtered_trans)
            )
        else:
            st.altair_chart(get_line_chart_of_rev_per_truck_per_hour(filtered_trans))


if __name__ == "__main__":
    main()
