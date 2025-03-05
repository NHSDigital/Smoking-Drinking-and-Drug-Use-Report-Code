from sdd_code.utilities import parameters as param


def get_flags():
    """
    A list of the exclusion flag functions to be run, each of which takes a
    DataFrame as its argument and returns a copy of the DataFrame with an
    exclusion flag field appended.
    Add or remove any from the list as required.

    Parameters:
        None.

    Returns: list (str)
        A list of functions that need to be run.

    """
    # Create the list of general derivations
    general_flags = [dummy_drug_flag]

    # Create the list of derivations relating to alcohol use
    alcohol_outlier_flags = [high_alc_quant_flag, high_alc_daily_flag,
                             all_alc_types_flag, alc_outlier_flag]

    # Create the list of derivations relating to drugs
    smoking_outlier_flags = [cig_outlier_flag]

    all_flags = (
        general_flags
        + alcohol_outlier_flags
        + smoking_outlier_flags
    )

    return all_flags


def dummy_drug_flag(df):
    """
    Creates new field with flags to indicate whether pupils say they have ever
    been offered or tried dummy drug (semeron).

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with dummy drug flag added.

    """
    # Define input columns for offered or tried semeron
    input_columns = ["dgofsem",
                     "dgtdsem"]

    # Set new dummy drug flag to 0
    df["dflagdummydrug"] = 0

    # Create flag for records where input columns = 1 (i.e pupil has heard of
    # or tried semeron)
    df.loc[df[input_columns].eq(1).any(axis=1), "dflagdummydrug"] = 1

    return df


def cig_outlier_flag(df):
    """
    Creates derived field that flags where individual daily cigarette
    quantities equal or exceed value set in parameters.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with cigarette outlier flag added.

    """

    input_columns = ["cg7mon",
                     "cg7tue",
                     "cg7wed",
                     "cg7thu",
                     "cg7fri",
                     "cg7sat",
                     "cg7sun"]

    df["dflagcigoutlier"] = 0

    # Define high alcohol quantity limit
    high_limit = param.HIGH_CIG_QUANTITY

    # Create flag for records where any input column is >= high limit value
    df.loc[(df[input_columns] >= high_limit).any(axis=1), "dflagcigoutlier"] = 1

    return df


def high_alc_quant_flag(df):
    """
    Creates derived field that flags where individual weekly alcohol
    quantities equal or exceed value set in parameters.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame

    """
    # Define alcohol quantity columns as input columns
    input_columns = ["al7brlrptn",
                     "al7brlrhp",
                     "al7brlrlg",
                     "al7brlrsmn",
                     "al7brlrbt",
                     "al7cdptn",
                     "al7cdhpn",
                     "al7cdlgn",
                     "al7cdsmn",
                     "al7cdbtn",
                     "al7wnshgs",
                     "al7spgs",
                     "al7ppcn",
                     "al7ppbt",
                     "al7otpt",
                     "al7othp",
                     "al7otlg",
                     "al7otsm",
                     "al7otbt",
                     "al7otgs"
                     ]

    # Set new high alcohol quantity flag to 0
    df["dflaghighalcquant"] = 0

    # Define high alcohol quantity limit
    high_limit = param.HIGH_ALC_QUANTITY

    # Create flag for records where any input column is >= high limit value
    df.loc[(df[input_columns] >= high_limit).any(axis=1), "dflaghighalcquant"] = 1

    return df


def all_alc_types_flag(df):
    """
    Creates derived field that flags where positive values were given for all of the
    quantities of named alcohol types (not Other).

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame

    """

    # Define alcohol quantity columns as input columns
    input_columns = ["al7brlrptn",
                     "al7brlrhp",
                     "al7brlrlg",
                     "al7brlrsmn",
                     "al7brlrbt",
                     "al7cdptn",
                     "al7cdhpn",
                     "al7cdlgn",
                     "al7cdsmn",
                     "al7cdbtn",
                     "al7wnshgs",
                     "al7spgs",
                     "al7ppcn",
                     "al7ppbt"
                     ]

    # Set all alcohol types flag to 0
    df["dflagallalctypes"] = 0

    # Create flag for records where any input columns is > 0
    df.loc[(df[input_columns] > 0).all(axis=1), "dflagallalctypes"] = 1

    return df


def high_alc_daily_flag(df):
    """
    Creates derived field that flags where mean daily alcohol
    units exceeds value set in parameters.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
         Dataframe with high mean daily alcohol units outlier flag added

    """

    # Set new high daily alcohol units flag to 0
    df["dflaghighdailyalc"] = 0

    # Define high alcohol quantity limit
    high_limit = param.HIGH_ALC_DAILY

    # Create flag for records where mean daily units is greater than high limit value
    df.loc[(df["dal7utmean"] > high_limit), "dflaghighdailyalc"] = 1

    return df


def alc_outlier_flag(df):
    """
    Creates a composite alcohol outlier flag to indicate if any individual alcohol
    outlier flag is 1

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
         Dataframe with composite alcohol outlier flag added

    """

    # Define individual alcohol outlier flags as input columns
    input_columns = ["dflaghighalcquant",
                     "dflaghighdailyalc",
                     "dflagallalctypes"
                     ]

    # Set new composite alcohol flag to 0
    df["dflagalcoutlier"] = 0

    # Create flag for records where any input columns = 1
    df.loc[df[input_columns].eq(1).any(axis=1), "dflagalcoutlier"] = 1

    return df
