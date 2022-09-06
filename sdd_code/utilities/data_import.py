import logging
import pandas as pd


def import_sav_values(file_path, drop_col):
    """
    This function will import the sav (SPSS) data from the specified location.
    It will convert column headers to lower case and remove fields as specifed.

    Parameters:
        file_path: the full file path and name.
        drop_col: a list of columns to be dropped on import.

    Returns:
        Dataframe with lower case column names and unused columns dropped.

    """
    logging.info("Importing raw SPSS file")

    # Import the raw sav pupil file
    df = pd.read_spss(file_path, convert_categoricals=False)
    logging.debug(f"Imported dataframe of size {df.shape}")

    # Convert all column headers to lower case
    df.columns = df.columns.str.lower()

    # Drop any columns specified in the drop columns input
    df = df.loc[:, ~df.columns.isin(drop_col)]

    logging.debug(f"Returning dataframe of size {df.shape}")
    return df