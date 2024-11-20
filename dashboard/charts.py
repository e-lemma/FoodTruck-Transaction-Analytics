""" Functions for generating Altair Charts """

import pandas as pd
import altair as alt


def get_bar_chart_of_total_trans_per_truck(transaction_data: pd.DataFrame) -> alt.Chart:
    """Returns an Altair bar chart of total transactions for each truck."""

    trans_per_truck = transaction_data["truck_id"].value_counts().reset_index()

    return (
        alt.Chart(trans_per_truck)
        .mark_bar(color="rgb(217, 95, 2)")
        .encode(
            alt.X("truck_id:N", title="Truck ID", axis=alt.Axis(labelAngle=0)),
            alt.Y("count", title="Transactions"),
        )
        .properties(title="Number of Transactions for each Food Truck")
    )


def get_pie_chart_of_transactions_by_day_of_week(
    transaction_data: pd.DataFrame,
) -> alt.Chart:
    """Returns an Altair pie chart of the overall number of transactions for all trucks,
    grouped by day of the week."""

    daily_transactions = (
        transaction_data.groupby(transaction_data["timestamp"].dt.date)
        .size()
        .reset_index()
    )
    daily_transactions["timestamp"] = pd.to_datetime(
        daily_transactions["timestamp"]
    ).dt.day_name()
    daily_transactions.columns = ["day_of_week", "transactions"]

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    return (
        alt.Chart(daily_transactions)
        .mark_arc()
        .encode(
            theta=alt.Theta(
                field="transactions", type="quantitative", title="Transactions"
            ),
            color=alt.Color(
                field="day_of_week",
                type="nominal",
                sort=day_order,
                title="Day of Week",
                scale=alt.Scale(scheme="dark2"),
            ),
        )
        .properties(title="Daily Transactions Distribution")
    )


def get_line_chart_of_num_trans_per_truck_per_hour(
    transaction_data: pd.DataFrame,
) -> alt.Chart:
    """Returns an Altair line chart of number of transactions, per truck, per hour."""

    hourly_transactions = (
        transaction_data.groupby(["truck_id", "hour"])
        .size()
        .reset_index(name="transactions")
    )

    return (
        alt.Chart(hourly_transactions)
        .mark_line(point=True)
        .encode(
            alt.X(
                "hour:O", title="Hour of the Day (24-hour)", axis=alt.Axis(labelAngle=0)
            ),
            alt.Y("transactions:Q", title="Transactions"),
            color=alt.Color(
                "truck_id:N", title="Truck ID", scale=alt.Scale(scheme="dark2")
            ),
        )
        .properties(
            title="Number of Transactions by Hour of the Day", width=800, height=400
        )
    )


def get_line_chart_of_rev_per_truck_per_hour(
    transaction_data: pd.DataFrame,
) -> alt.Chart:
    """Returns an Altair line chart of total revenue per truck, per hour."""

    hourly_transactions_val = (
        transaction_data.groupby(["truck_id", "hour"])["total"].sum().reset_index()
    )

    return (
        alt.Chart(hourly_transactions_val)
        .mark_line(point=True)
        .encode(
            alt.X(
                "hour:O", title="Hour of the Day (24-hour)", axis=alt.Axis(labelAngle=0)
            ),
            alt.Y("total:Q", title="Revenue (£)"),
            color=alt.Color(
                "truck_id:N", title="Truck ID", scale=alt.Scale(scheme="dark2")
            ),
        )
        .properties(
            title="Revenue generated by Hour of the Day ", width=800, height=400
        )
    )
