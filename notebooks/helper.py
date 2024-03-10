import matplotlib
import pandas as pd

matplotlib.rcParams["figure.figsize"] = (12, 6)
matplotlib.rcParams["axes.spines.right"] = False
matplotlib.rcParams["axes.spines.top"] = False
matplotlib.rcParams["axes.labelsize"] = 20
matplotlib.rcParams["xtick.labelsize"] = 15
matplotlib.rcParams["ytick.labelsize"] = 15


def format_year_month_table(df: pd.DataFrame, value_name: str = "Value"):
    """
    Format a DataFrame that has columns like ["Year", "Jan", "Feb", ..., "Dec"]

    :param df: DataFrame to reformat
    :param value_name: Name to give the value column for melting
    :return: DataFrame with Date column and corresponding values
    """
    df = pd.melt(df, id_vars=["Year"], var_name="Month", value_name=value_name)

    # Convert abbreviated month to int; combine into single data column
    df["Month"] = pd.to_datetime(df["Month"], format="%b").dt.month
    df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))
    df = df.sort_values(by="Date").reset_index(drop=True)

    return df


def percent_change_relative_to(df: pd.DataFrame, date: str, column_name: str) -> pd.DataFrame:
    """
    Compute the percent change relative to a specific date

    :param df: DataFrame
    :param date: Date to compute percents relative to
    :param column_name: Name of the column to compute on
    :return: New DataFrame with a "Percent Change" column
    """
    if "Date" in df.columns:
        index = df[df.Date == date].index[0]
    else:
        index = df[df.Year == date].index[0]

    df_relative_to_date = df.iloc[index:].copy()

    start = df_relative_to_date[column_name].values[0]
    df_relative_to_date["Percent Change"] = 100 * (df_relative_to_date[column_name] - start) / start

    return df_relative_to_date
