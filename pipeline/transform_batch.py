""" Script for combining all truck transaction csvs into one CSV file,
    cleaning the data, and removing any redundant files. """

import os
import pandas as pd


def get_all_csv_filenames(directory: str) -> list[str]:
    """
    Returns a list of the names of all relevant CSV files in the specified path.
    """
    return [
        filename
        for filename in os.listdir(directory)
        if filename.endswith(".csv") and filename.startswith("T3_")
    ]


def get_truck_id(filename: str) -> int:
    """Returns the truck id determined by the filename"""
    truck_id = filename.split("_")[1][1]
    return int(truck_id)


def clean_truck_data(truck_df: pd.DataFrame) -> pd.DataFrame:
    """Removes erroneous rows from the truck transaction data,
    and converts the total column into float values."""

    bad_totals = ["ERR", "blank", "VOID", "0.00", "0", "None", "NULL", ""]

    # Drops rows with missing values for total
    truck_df = truck_df.dropna(subset=["total"])
    # Changes "total" values to floats
    truck_df.loc[:, "total"] = pd.to_numeric(truck_df["total"], errors="coerce")
    # Removes bad values from total
    truck_df = truck_df[
        ~truck_df["total"].astype(str).isin(bad_totals)
        & truck_df["total"].notna()
        & (truck_df["total"] > 0)
        & (truck_df["total"] < 100)
    ]

    return truck_df


def combine_transaction_data_files(
    source_filenames: list[str], csv_directory: str, new_combined_filename: str
):
    """
    Loads and combines relevant csv files from the data/historical/ folder.
    Adds the truck id present in the filenames as a column in each csv.
    Produces a single combined file in the data/historical/ folder.
    """

    truck_dataframes = []

    for filename in sorted(source_filenames):

        truck_dataframe = pd.read_csv(f"{csv_directory}/{filename}")

        truck_id = get_truck_id(filename)
        truck_dataframe.insert(0, "truck_id", truck_id)

        truck_dataframes.append(truck_dataframe)

    joined_truck_dataframe = pd.concat(truck_dataframes, ignore_index=True)

    joined_truck_dataframe = clean_truck_data(joined_truck_dataframe)

    joined_truck_dataframe.to_csv(
        f"{csv_directory}/{new_combined_filename}", index=False
    )


def remove_csv_files(csv_filenames: list[str], csv_directory: str) -> None:
    """Deletes all files named in passed-in list."""
    for filename in csv_filenames:
        if os.path.exists(f"{csv_directory}/{filename}"):
            os.remove(f"{csv_directory}/{filename}")
        else:
            print(f"{filename} does not exist")


if __name__ == "__main__":

    filenames = get_all_csv_filenames("data/")

    combine_transaction_data_files(filenames, "data/", "TRUCK_DATA_BATCH_MERGED.csv")
