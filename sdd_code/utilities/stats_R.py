from itertools import chain, combinations
from typing import List

import pandas as pd
import rpy2.robjects as robjects

import sdd_code.utilities.parameters as param
from sdd_code.models.r_integration import r_to_py, py_to_r


def get_breakdown_combinations(breakdowns: List[str]) -> chain:
    """Get a chain of all breakdown combinations for a list of breakdowns

    Parameters
    ----------
        breakdowns: list[str]
            A list of breakdowns

    Returns
    -------
        chain
    """
    n_replacements = len(breakdowns) + 1
    breakdown_combinations = [combinations(breakdowns, n) for n in range(n_replacements)]
    breakdown_combinations = chain.from_iterable(breakdown_combinations)

    return breakdown_combinations


def ci_cutoff(df, lower_ci="lower_ci", upper_ci="upper_ci"):
    """Fix confidence intervals that go above 100 or below 0.

    Due to the underlying method, a wald confidence interval equal to mu +/- 1.96 * se,
    some confidence intervals can be outside of what should be statistically possible.
    This function corrects those.

    Parameters
    ----------
        df: pd.DataFrame
        lower_ci: str
        upper_ci: str

    Returns
    -------
        pd.DataFrame
    """

    df.loc[df[lower_ci] < 0, lower_ci] = 0
    df.loc[df[upper_ci] > 100, upper_ci] = 100

    return df


def survey_stats(
    df, question, by, psu=param.PSU, strata=param.STRATA, weights=param.WEIGHTING_VAR
):
    """
    Calculate a set of weighted statistics for the variable.

    Calculates columns: Mean, Median, std_err, lower_ci, upper_ci

    Parameters
    ----------
    df : pandas.DataFrame
    question : str
        Single variable name that defines the question to be analysed
        (e.g. dallast5, alevr)
    by: list[str]
        The subpopulations to group statistics by
    psu: str
        The name of the column containing PSUs
    strata: str
        The name of the column containing strata
    weight : str
        The name of the column containing weights

    Returns
    -------
    pd.DataFrame
    """
    r = robjects.r

    # Get custom R functions
    r.source(str(param.LOCAL_ROOT / "sdd_code" / "sddR" / "R" / "stats_functions.R"))

    # Allow for no breakdowns
    df["const"] = 1

    # Convert inputs into R formats
    df_r = py_to_r(df)

    output_list = []
    by_combinations = get_breakdown_combinations(by)
    for by_subset in by_combinations:
        # Allow for no breakdowns
        if not by_subset:
            by_subset = ["const"]

        not_in_subset = [col for col in by if col not in by_subset]

        # Calculate means
        output_r = r.survey_stats(
            df_r,
            question,
            by=list(by_subset),
            psu=psu,
            strata=strata,
            weights=weights,
        )

        # Convert R dataframe to python
        output = r_to_py(output_r)

        # Set all constant columns to total code
        output[not_in_subset] = param.TOT_CODE

        output_list.append(output)

    output = pd.concat(output_list)

    # Format the output
    output = output.rename(
        {
            f"{question}.x": "R_Mean",
            f"{question}.y": "R_Median",
            "se": "std_err",
            "2.5 %": "lower_ci",
            "97.5 %": "upper_ci",
            "DEff": "deff"
        },
        axis=1,
    ).drop(["Row.names", f"se.{question}", "const"], axis=1, errors="ignore")

    return output


def survey_perc_ratios(
    df,
    question,
    base,
    by,
    psu=param.PSU,
    strata=param.STRATA,
    weights=param.WEIGHTING_VAR,
):
    """
    Calculate a weighted ratio of one variable against another, as well as
    standard errors and confidence intervals

    Parameters
    ----------
    df : pandas.DataFrame
    question : str
        Single variable name that defines the question to be analysed, should be
        equal to "Value"
    by: list[str]
        The subpopulations to group statistics by
    psu: str
        The name of the column containing PSUs
    strata: str
        The name of the column containing strata
    weight : str
        The name of the column containing weights

    Returns
    -------
    pd.DataFrame
    """
    r = robjects.r

    # Get custom R functions
    r.source(str(param.LOCAL_ROOT / "sdd_code" / "sddR" / "R" / "stats_functions.R"))

    # Allow for no breakdowns
    df["const"] = 1

    # Convert inputs into R formats
    df_r = py_to_r(df)

    output_list = []
    by_combinations = get_breakdown_combinations(by)
    for by_subset in by_combinations:
        # Allow for no breakdowns
        if not by_subset:
            by_subset = ["const"]

        not_in_subset = [col for col in by if col not in by_subset]

        # Get standard errors of percentages
        # Calculate ratio of Value against base
        output_r = r.survey_ratio(
            df_r,
            question,
            base,
            by=list(by_subset),
            psu=psu,
            strata=strata,
            weights=weights,
        )

        # Convert R dataframe to python
        output = r_to_py(output_r)

        # Set all constant columns to total code
        output[not_in_subset] = param.TOT_CODE

        output_list.append(output)

    output = pd.concat(output_list)

    # Format the output
    output = output.rename(
        {
            f"se.{question}/{base}": "std_err",
            f"{question}/{base}": "R_Percentage",
            "DEff": "deff"
        },
        axis=1,
    ).drop("const", axis=1, errors="ignore")

    # Convert proportions to percentages
    perc_cols = [
        "std_err",
        "R_Percentage",
        "lower_ci",
        "upper_ci",
    ]
    output[perc_cols] = output[perc_cols] * 100

    output = ci_cutoff(output)

    return output


def survey_perc_proportions(
    df, question, by, psu=param.PSU, strata=param.STRATA, weights=param.WEIGHTING_VAR
):
    """
    Calculate a weighted percentage of a variable, i.e. how often each value
    of the variable occurs as a percentage of the total

    Parameters
    ----------
    df : pandas.DataFrame
    question : str
        Single variable name that defines the question to be analysed
        (e.g. dallast5, alevr)
    by: list[str]
        The subpopulations to group statistics by
    psu: str
        The name of the column containing PSUs
    strata: str
        The name of the column containing strata
    weights : str
        The name of the column containing weights

    Returns
    -------
    pd.DataFrame
    """
    r = robjects.r

    # Get custom R functions
    r.source(str(param.LOCAL_ROOT / "sdd_code" / "sddR" / "R" / "stats_functions.R"))

    # Allow for no breakdowns
    df["const"] = 1

    # Convert inputs into R formats
    df_r = py_to_r(df)

    output_list = []
    by_combinations = get_breakdown_combinations(by)
    for by_subset in by_combinations:
        # Allow for no breakdowns
        if not by_subset:
            by_subset = ["const"]

        not_in_subset = [col for col in by if col not in by_subset]

        output_r = r.survey_proportion(
            df_r,
            question,
            by=list(by_subset),
            psu=psu,
            strata=strata,
            weights=weights,
        )

        # Convert R dataframe to python
        output = r_to_py(output_r)

        # Set all constant columns to total code
        output[not_in_subset] = param.TOT_CODE

        output_list.append(output)

    output = pd.concat(output_list)

    # Format the output
    output = (
        output.rename(
            {
                "2.5 %": "lower_ci",
                "97.5 %": "upper_ci",
                "se": "std_err",
                "proportion": "R_Percentage",
                "DEff": "deff"
            },
            axis=1,
        )
        .drop(["join", "var_as_chr", "const"], axis=1, errors="ignore")
        .astype({question: float})
    )

    # Convert proportions to percentages
    perc_cols = [
        "std_err",
        "R_Percentage",
        "lower_ci",
        "upper_ci",
    ]
    output[perc_cols] = output[perc_cols] * 100

    output = ci_cutoff(output)

    return output
