import logging

import sdd_code.utilities.parameters as param


def filter_schools(df):
    """
    Removes the volunteer schools from the dataset as these are excluded from all
    publication outputs by default.

    The function also returns the number of rows removed.

    Parameters
    ----------
    df : pandas.DataFrame
        containing a column named "volunsch" indicating volunteer schools.

    Returns
    -------
    df : pandas.DataFrame
        filtered based on the volunteer schools column.

    """
    # Return the number of records that will be excluded
    exc_count = len(df.loc[df["volunsch"] == 1])
    message = f"{exc_count} records excluded for volunteer schools."
    logging.info(message)

    # Filter out the volunteer school data
    df = df.loc[df["volunsch"] != 1]

    return df


def filter_dummy_drug(df):
    """
    Filters the input DataFrame (df) based on whether a pupil said they had been
    offered or tried the dummy drug (Semeron), as indicated by the dummy drug flag
    created in exclusion_flags.py.

    If the flag value is 1, then the whole record for that pupil is filtered out.

    The function also prints the number of rows filtered out.

    Parameters
    ----------
    df : pandas.DataFrame
        containing the dummy drug field "dflagdummydrug".

    Returns
    -------
    df : pandas.DataFrame
        filtered based on the dummy drug field.

    """
    # Return the number of records that will be excluded
    exc_count = len(df.loc[df["dflagdummydrug"] == 1])
    message = f"{exc_count} records excluded where pupils say have tried or been offered dummy drug."
    logging.info(message)

    # Exclude records where the dummy drug flag is 1
    df = df.loc[(df["dflagdummydrug"]) != 1]

    return df


def filter_outliers(df):
    """
    Filters the input DataFrame (df) based on the presence of outlier data in selected
    columns, as indicated by the outlier flags created in exclusion_flags.py.

    If any of the flag values is 1, then the whole record for that pupil is filtered out.

    The function also prints the number of rows filtered out.

    Parameters
    ----------
    df : pandas.DataFrame
        containing the outlier flag fields.

    Returns
    -------
    df : pandas.DataFrame
        filtered based on the outlier flag fields.

    """
    # Set the list of column names that identify the records with outlier values
    outlier_cols = ["dflagcigoutlier", "dflagalcoutlier"]

    # Return the number of records that will be excluded
    exc_count = len(df.loc[(df[outlier_cols] == 1).any(axis=1)])
    message = f"{exc_count} records excluded due to record containing outlier values."
    logging.info(message)

    # Exclude records where any outlier flag is 1
    df = df.loc[(df[outlier_cols] != 1).all(axis=1)]

    return df


def apply_exclusions(df):
    """
    Applies all the publication output exclusions:
        - Default removal of volunteer schools.
        - Filtering as determined by the exclusion parameters in parameters.py.

    Returns a final record count.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing all SDD records.

    Returns
    -------
    df : pandas.DataFrame
        The SDD dataframe filtered based on the exclusion parameters.

    """

    # Return an unfiltered record count to the console/log
    message = f"{df.shape[0]} rows present in the final unfiltered SDD pupil dataframe."
    logging.info(message)

    # Apply the schools exclusions filter
    df = filter_schools(df)

    # If dummy drug parameter is set to False, apply the dummy drug data exclusion filter
    if not param.INCLUDE_DUMMY_DRUG:
        df = filter_dummy_drug(df)

    # If outliers parameter is set to False, apply the outliers data exclusion filter
    if not param.INCLUDE_OUTLIERS:
        df = filter_outliers(df)

    # Return a final record count to the console/log
    message = f"{df.shape[0]} rows present in the final filtered SDD pupil dataframe"
    logging.info(message)

    return df
