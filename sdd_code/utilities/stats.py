"""Statistical functions"""
import pandas as pd

# Samplics code is not longer used, so samplics is not required as a dependency
# so if importing it fails, then just create a dummy class. If this class is
# used it will raise an error
try:
    from samplics import TaylorEstimator
except ImportError:

    class TaylorEstimator:
        def __init__(*args, **kwargs):
            raise NotImplementedError(
                "Trying to use samplics code when samplics is not installed"
            )


# Local imports
import sdd_code.utilities.parameters as param


def create_weighted_stats(df, question, weighting=param.WEIGHTING_VAR, **kwargs):
    """
    Returns a set of weighted statistic for the question. Is used within df.apply()
    to add all standard weighted stats at once.

    Creates columns: Mean, Median, std_err, lower_ci, upper_ci

    Parameters
    ----------
    df : pandas.DataFrame
    question : str
        Single variable name that defines the question to be analysed
        (e.g. dallast5, alevr)
    weight : str
        Column to use as weighting
    Addition kwargs are passed to weighted_variance

    Returns
    -------
    pd.Series
    """

    return_data = {}
    return_data["Mean"] = weighted_mean(df, question, weighting)
    return_data["Median"] = weighted_median(df, question, weighting)

    return pd.Series(return_data)


def create_weighted_percentage_stats(
    df: pd.DataFrame,
    question: str,
    weighting: str = param.WEIGHTING_VAR,
    domain: str = "domain",
    stat: str = "proportion",
    **kwargs
):
    """
    Returns the weighted percentages and standard errors for a question.
    It does this based by calculating the proportions of each possible value
    of the question, and returns 1 row for each value.

    Creates a dataframe with columns:
        "question", domain, samplics_percentage, std_err, lower_ci, upper_ci

    Parameters
    ----------
    df : pandas.DataFrame
    question : str
        Single variable name that defines the question to be analysed
        (e.g. dallast5, alevr)
    weight : str
        Column to use as weighting
    domain : str
        Domain columns, see: ........
    Addition kwargs are passed to weighted_variance

    Returns
    -------
    pd.DataFrame
    """

    variances = weighted_variances(
        df, question, weighting, stat=stat, domain=df[domain], **kwargs
    )

    variances = variances.to_dataframe().rename(
        columns={
            "_level": question,
            "_domain": "domain",
            "_stderror": "std_err",
            "_estimate": "samplics_percentage",
            "_lci": "lower_ci_samp",
            "_uci": "upper_ci_samp",
        }
    )

    # Samplics CIs uses a slightly more complex CI method, with no
    # option to change. Use basic wald CI, 1.96 from 95% level of normal distribution
    # This is equivalent to confint() in R. Note that this can produce irrational
    # proportions (i.e. below 0, above 1) but is consistent
    variances["lower_ci"] = (
        variances["samplics_percentage"] - 1.96 * variances["std_err"]
    )
    variances["upper_ci"] = (
        variances["samplics_percentage"] + 1.96 * variances["std_err"]
    )

    # Convert to percentages
    numeric_cols = [
        "std_err",
        "samplics_percentage",
        "lower_ci",
        "upper_ci",
        "lower_ci_samp",
        "upper_ci_samp",
    ]
    variances[numeric_cols] = variances[numeric_cols] * 100
    return variances


def weighted_mean(df: pd.DataFrame, value: str, weighting: str) -> float:
    """
    Returns a weighted mean of value column

    Parameters:
    ----------
    df : pd.DataFrame
        Dataframe containing columns to be used in calculation
    value : str
        The name of the column containing values
    weighting : str
        The name of the column containing weights

    Returns:
    ----------
    np.float64
    """
    d = df[value]
    w = df[weighting]

    return (d * w).sum() / w.sum()


def weighted_median(
    df: pd.DataFrame,
    value: str,
    weighting: str,
) -> float:
    """
    Returns a weighted median of the value column

    Parameters:
    ----------
    df : pd.DataFrame
        Dataframe containing columns to be used in calculation
    value : str
        The name of the column containing values
    weighting : str
        The name of the column containing weights

    Returns:
    ----------
    np.float64
    """
    sorted_df = df.sort_values(value)
    cumsum = sorted_df[weighting].cumsum()
    cutoff = sorted_df[weighting].sum() / 2.0
    median = sorted_df.loc[cumsum >= cutoff, value].iloc[0]
    return median


def weighted_variances(
    df: pd.DataFrame,
    value: str,
    weighting: str = param.WEIGHTING_VAR,
    strata: str = param.STRATA,
    psu: str = param.PSU,
    stat: str = "mean",
    **kwargs
) -> TaylorEstimator:
    """Use samplics TaylorEstimator to calculate population statistics and
    variances.

    Paramters:
    ----------
    df : pd.DataFrame
        Dataframe containing columns to be used in calculation
    value : str
        The name of the column containing values
    weighting : str
        The name of the column containing weights
    strata: str
        The name of the column containing strata
    psu: str
        The name of the column containing PSUs
    stat: str
        The statistic to calculate
    Additional kwargs are passed to TaylorEstimator.estimate()

    Returns:
    TaylorEstimator
        An estimation object, see https://samplics.readthedocs.io/en/latest/samplics.estimation.html#module-samplics.estimation.expansion
    """

    # Create estimator for a populations parameter
    variance_estimator = TaylorEstimator(stat, alpha=0.05)

    # Base will be passed though funcs as string, but needs to be series
    try:
        x = df[kwargs.pop("base")]
    except KeyError:
        x = None

    # Estimate parameters
    variance_estimator.estimate(
        y=df[value],
        samp_weight=df[weighting],
        stratum=df[strata],
        psu=df[psu],
        x=x,
        **kwargs
    )

    return variance_estimator
