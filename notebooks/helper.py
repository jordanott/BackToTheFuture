from typing import Tuple

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

LOGO_IMAGE = None

matplotlib.rcParams["axes.spines.right"] = False
matplotlib.rcParams["axes.spines.top"] = False
matplotlib.rcParams["axes.labelsize"] = 20
matplotlib.rcParams["xtick.labelsize"] = 15
matplotlib.rcParams["ytick.labelsize"] = 15
matplotlib.rcParams["savefig.bbox"] = "tight"
matplotlib.rcParams["legend.fontsize"] = 15
matplotlib.rcParams["legend.title_fontsize"] = 15
matplotlib.rcParams["axes.titlesize"] = 25
matplotlib.rcParams["figure.figsize"] = (10, 6)
matplotlib.rcParams["lines.linewidth"] = 1.75


def add_logo(ax, location: Tuple[float, float] = (0.85, -0.15)):
    global LOGO_IMAGE
    if LOGO_IMAGE is None:
        LOGO_IMAGE = plt.imread("../assets/figure_logo.png")

    imagebox = OffsetImage(LOGO_IMAGE, zoom = 0.35)
    ab = AnnotationBbox(imagebox, location, frameon=False, xycoords='axes fraction')
    ax.add_artist(ab)

def create_legend(legend=None, title: str = None, loc: str = None):
    if legend is None:
        legend = plt.legend(loc=loc)
    
    if title is not None:
        legend.set_title(title)
        
    legend.get_frame().set_alpha(None)
    legend.get_frame().set_facecolor((0, 0, 0, 0))

    return legend


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


def savefig(file_path: str, file_format: str = ".png"):
    plt.savefig(file_path + file_format, dpi=1200, facecolor='white', transparent=False)
