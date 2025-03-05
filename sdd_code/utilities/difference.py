import logging
from itertools import combinations
from pathlib import Path
from typing import Union, Dict
import sdd_code.utilities.parameters as param

import pandas as pd
import numpy as np


def get_source_data(output_path: str):
    """Retrieve all underlying tables from a folder of source data
    in sheets in excel files.

    Parameters
    ----------
        folder: str or Path
            The location to read the data from
        pattern: str
            The regex pattern to use to find the files required

    Returns
    -------
        A dictionary of sheet/table names to dictionaries of data.
        The data dictionaries contain a "data" key to the pd.DataFrame, and a
        "file" key to the file that this dataframe came from.
    """

    # retrieve the previous year source filename from the main output path
    filename = Path(output_path).name
    source_file = param.PREVYEAR_DIR / filename

    source_data = {}

    xl = pd.ExcelFile(source_file)
    for sheet_name in xl.sheet_names:
        info = {
            # Get the data for each sheet
            "data": xl.parse(sheet_name),
        }
        source_data[sheet_name] = info

    return source_data


def get_breakdown_cols(df: pd.DataFrame, breakdown_col: str):
    """Get the individual breakdown columns from a column of
    breakdown_types.

    Breakdown_type will be a string like: "gender_age1115_region_dallast5"
    We wish to extract the individual cols separated by underscores. However,
    sometimes there may be column names with underscores within them, e.g:
    "gender_age1115_region_unit_drinkdays" where unit_drinkdays is the column of interest.
    To get these, we find all 1 and 2 length combination of columns, and check if they
    are in the dataframe.

    Parameters
    ----------
        df: pd.DataFrame
        breakdown_col: str
            The constant column in the dataframe which defines which columns were
            used as breakdowns

    Returns
    -------
        list[str]
    """
    breakdowns = df[breakdown_col].unique()
    if len(breakdowns) > 1:
        # If we have multiple different breakdowns, then this
        # output is from create_breakdown_combine. So set first
        # breakdown cols to "Question", "Response", and add
        # any others that have been used
        col_all = ["Question", "Response"]
        for c in breakdowns:
            cols = c.split("_")
            # First is value in Question, remove
            breakdown_cols = cols[1:]
            col_all += breakdown_cols
        col_split = list(set(col_all))
    else:
        col_split = breakdowns[0].split("_")
    possible_cols = col_split + list(combinations(col_split, 2))
    cols = []
    df_cols = set(df.columns)
    for col_list in possible_cols:
        if not isinstance(col_list, str):
            col = "_".join(col_list)
        else:
            col = col_list

        if col in df_cols:
            cols.append(col)
    return cols


def get_prev_year_diff(
    df: pd.DataFrame,
    table_name: str,
    prev_source_data: Dict[str, dict],
    col_to_check: str = "Percentage",
    base_col: str = "DenomW",
    base_tol: float = 50.0,
    diff_tol: float = param.BREACH_LEVEL,
    breakdown_col: str = "Breakdown_type",
):
    """Calculate the difference between two SDD tables from different years

    Parameters
    ----------
        df: pd.DataFrame
            The current dataframe to check
        table_name: str
            The name of this table in the output publication
        prev_source_data: Dict[str, dict]
            A dictionary of table names to data dictionaries, as retrieved
            from get_source_data()
        col_to_check: str
            Which column in the two dataframes to compare
        base_col: str
            Base column to determine which values are checked, if less than
            base_tol then not checked
        base_tol: str
            The minimum value for base_col, above which col_to_check will be checked
        diff_tol:
            The tolerance for differences, above which a flag is set to 1
        breakdown_col:
            The name of the column in df which determines the grouping of
            the data

    Returns
    -------
        pd.DataFrame
    """
    logging.info("Checking the difference compared to the previous year for {table_name}")
    # Find the matching table in previous source data dict
    # This gives a dict of data, and the file it came from
    df2_source = prev_source_data.get(table_name, None)

    # Reset the index, to allow for adding in check_df
    df = df.reset_index(drop=True)

    # Check for differences between dfs shape/cols etc, default to NAN if found
    if (
        df2_source is None
        or col_to_check not in df.columns
        or col_to_check not in df2_source["data"].columns
        or base_col not in df.columns
        or base_col not in df2_source["data"].columns
    ):
        logging.debug(f"Could not perform difference check for {table_name}")
        df["PrevYearDiff"] = np.nan
        df["DiffFlag"] = np.nan
        return df

    #extract previous source data from source dictionary
    df2 = df2_source["data"]

    # Get cols to merge by
    merge_cols = get_breakdown_cols(df, breakdown_col)

    # Add cols to check to the same dataframe to allow for not
    # checking rows that are suppressed, ensure same ordering
    check_df = pd.merge(
        df[[*merge_cols, col_to_check, base_col]].rename(
            columns={col_to_check: "check1", base_col: "base1"}
        ),
        df2[[*merge_cols, col_to_check, base_col]].rename(
            columns={col_to_check: "check2", base_col: "base2"}
        ),
        how="left",
        on=merge_cols,
    )

    for base, check in zip(["base1", "base2"], ["check1", "check2"]):
        # Suppress all values below a base that we are interested in
        check_df.loc[check_df[base] < base_tol, check] = "u"

        # Extract square bracketed values
        check_df.loc[:, check] = (
            check_df[check].astype(str).replace(r"\[|\]", "", regex=True)
        )

        # Convert to numeric type for comparison, changing "u" to NaN
        check_df.loc[:, check] = pd.to_numeric(check_df[check], errors="coerce")

    # Calculate the difference between years, and create flag for if
    # it's within tolerance
    df["PrevYearDiff"] = check_df["check1"] - check_df["check2"]
    df["DiffFlag"] = (df["PrevYearDiff"].abs() > diff_tol).astype(int)

    return df
