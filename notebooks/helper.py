import pandas as pd


def percent_change_relative_to(df: pd.DataFrame, date: str, column_name: str) -> pd.DataFrame:
    """
    Compute the percent change relative to a specific date

    :param df: DataFrame
    :param date: Date to compute percents relative to
    :param column_name: Name of the column to compute on
    :return: New DataFrame with a "Percent Change" column
    """
    index = df[df.Date == date].index[0]
    df_relative_to_date = df.iloc[index:].copy()

    start = df_relative_to_date[column_name].values[0]
    df_relative_to_date["Percent Change"] = 100 * (df_relative_to_date[column_name] - start) / start

    return df_relative_to_date
