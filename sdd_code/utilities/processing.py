import logging
from itertools import chain, combinations

import pandas as pd
import numpy as np

import sdd_code.utilities.parameters as param
from sdd_code.utilities import stats
from sdd_code.utilities import stats_R


def create_domain(df, domains):
    """Creates a single domain column from a list of domains.

    Parameters
    ----------
    df : pandas.DataFrame
    domains: list[str]
        Columns to use as domains

    Returns
    -------
    pd.Series
        The new domain column
    """
    domain = df[domains].astype("string").agg("_".join, axis=1)

    # Need second conversion to stop being object and fix np.unique() in samplics
    return domain.astype(pd.StringDtype())


def safe_check_columns_eq(df, col1, col2):
    """Checks that two numeric columns are equal.
    First coerces to numeric and drops resulting nan rows, to compensate for suppression
    and mixed dtype columns.

    Parameters
    ----------
    df : pandas.DataFrame
    col1: str
    col2: str

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If columns are not equal
    """
    # Keep in 1 df rather than just passing in columns for dropna
    check_df = df.loc[:, [col1, col2]]
    check_df.loc[:, col1] = pd.to_numeric(check_df[col1], errors="coerce")
    check_df.loc[:, col2] = pd.to_numeric(check_df[col2], errors="coerce")
    check_df.dropna(inplace=True)

    assert np.isclose(
        check_df[col1], check_df[col2], rtol=1e-4
    ).all(), f"{col1} and {col2} are not matching"


def add_response_subgroup(df, breakdowns, question, subgroup):
    """
    Combines groups of question responses into a single response code.
    This is added to the dataframe as an additional response.

    Parameters
    ----------
    df : pandas.DataFrame
        Record-level data with pupil breakdowns, question and counts
    breakdowns: list[str]
        Columns to use in the breakdowns (e.g. age, sex, etc)
    question: str
        Single variable name that defines the question to be analysed
        (e.g. dallast5, alevr)
    subgroup: dictionary
        Contains with new response code(s) that will be assigned to the new grouping(s),
        and the response values that will form the group.

    Returns
    -------
    pandas.DataFrame with new response subgroup

    """
    for subgroup_code, subgroup_values in subgroup.items():
        subgroup = df[df[question].isin(subgroup_values)]
        subgroup = subgroup.groupby([*breakdowns]).sum().reset_index()
        subgroup[question] = subgroup_code
        df = df.append(subgroup)

    return df.reset_index(drop=True)


def add_breakdown_groups(df, breakdowns, question):
    """
    Add groupings to the record level data for each of the table breakdowns.

    3-types of groups are added
    1. For each combination of values in the breakdowns (e.g. males aged 11)
    2. For each column individually (e.g. all males, all females)
    3. Overall across all records

    For 2 and 3, the column(s) excluded from the breakdown (e.g. age if
    breaking down by sex) has all values replaced by param.TOT_CODE to
    indicate that it is the group that includes all values in the column(s)

    Parameters
    ----------
    df : pandas.DataFrame
        Record-level data to breakdown
    breakdowns: list[str]
        Columns to use in the breakdowns (e.g. age, sex, etc)
    question: str
        Single variable name that defines the question to be analysed
        (e.g. dallast5, alevr)

    Returns
    -------
    pandas.DataFrame
        Record-level data with breakdown groups added

    """

    # List to store the different breakdown groups
    total_dfs = []

    # Combinations of columns to be replaced with params.TOT_CODE
    # Firstly don't replace any, then replace a single column, then 2 columns, etc
    # E.g. [[], ["sex"], ["age"], ["sex", "age"], ...]
    n_replacements = len(breakdowns) + 1
    replace_combinations = [combinations(breakdowns, n) for n in range(n_replacements)]
    replace_combinations = chain.from_iterable(replace_combinations)

    for columns_to_replace in replace_combinations:
        # Make a copy of df with default values for non-grouped columns
        # inserted (e.g. replace values in 'sex' with 99)
        default_df = df.copy()

        for col in columns_to_replace:
            default_df[col] = param.TOT_CODE

        # Join the breakdown groupings
        total_dfs.append(default_df)

    # Concatenate the totals into a single DataFrame
    return pd.concat(total_dfs, axis=0).reset_index(drop=True)


def transpose_multi(df, breakdowns, question):
    """
    Creates a single column for multi-response question options
    The multi-response options are fed in as individual columns in addition to breakdown and weighting

    Parameters
    ----------
    df : pandas.DataFrame
    breakdowns : list[str]
        these are the pupil breakdowns from the table e.g. sex and age1115.
    question: str
        this is the name to be allocated to the column in the output that
         will contain the multi response options

    Returns
    -------
    df : pandas.DataFrame
        with the individual response variables as a single column named as per the 'question' input

    """
    # Set the index on all columns except those that are to be transposed to a single column
    df.set_index([*breakdowns, param.WEIGHTING_VAR], inplace=True)
    # Transpose the non-index columns into a single new column
    df = df.stack().rename_axis(index={None: question}).rename("Value").reset_index()

    return df


def suppress_column(col_to_suppress, base, lower=30, upper=50, round_to_dp=None):
    """Suppress the values of a column based on upper and lower bounds of a base column

    If base is less than lower, then replace the values with "u"
    If it is between lower and upper, then round the value and surround
    it with square brackets
    If it is 0 and should be rounded, then replace with "[-]"

    Parameters
    ----------
        col_to_suppress: pd.Series
            A numeric column that should be suppressed
        base: pd.Series
            A column with the same structure as col_to_suppress containing the
            values that determine suppression
        lower: int
            Lower bound for rounding - default is 30
        upper: int
            Upper bound for rounding - default is 50
        round_to_dp: int
            Number of decimal places for rounding - default is None

    Returns
    -------
        pd.Series

    """
    suppression = col_to_suppress.copy(deep=True)

    should_suppress = base < lower
    should_round = base.between(lower, upper, inclusive="left")
    should_zero = np.isclose(suppression, np.zeros_like(suppression))

    suppression.loc[should_suppress] = "u"

    # Round to specified dp (default of None = integer) and add warning symbols
    # to column values where suppression base between 30 and 50
    suppression.loc[should_round & ~should_zero] = (
        suppression[should_round & ~should_zero]
        .apply(
            lambda p: f"[{round(p, round_to_dp)}]"
            )
        )

    # Set to [-] for values where col = 0 and denom between 30 and 50
    suppression.loc[should_round & should_zero] = "[-]"

    return suppression


def add_percentage(
    df, numerator="NumerW", denominator="DenomW", denominator_sup="DenomW"
):
    """
    Adds a perentage calculation
    Supresses percents wusing suppress_column

    Parameters
    ----------
    df : pandas.DataFrame
        df expects a numerator and a denominator among the columns
    numerator : str
        Column to use as numerator (default='NumerW')
    denominator : str
        Column to use as denominator for percentage (default='DenomW')
    denominator_sup : str
        Column to use for the supression check (default='DenomU')

    Returns
    -------
    pandas.DataFrame
        Copy df with Percentage column added (including required supression
        and warning symbols)

    """
    # Use the weighted counts and base to calculate the percentage for each group
    numer = df[numerator]
    denom = df[denominator]
    percentage_s = 100 * numer / denom

    percentage_s = suppress_column(percentage_s, df[denominator_sup])

    # Return copy of df with 'Percentage' column
    return df.assign(Percentage=percentage_s)


def format_breakdown_output(df, breakdowns, question, column_order, year=param.YEAR):
    """
    Will format the output ready for writing to Excel

    Parameters
    ----------
    df : pandas.DataFrame
    breakdown : list[str]
        these are the pupil breakdowns from the table e.g. sex and age1115.
    question: str
        Single variable name that defines the question to be analysed
        (e.g. dallast5, alevr)
    column_order: list[str]
        List that defines the order of columns in the final output
    year: str
        The value to put in the year column, defaults to param.YEAR

    Returns
    -------
    df : pandas.DataFrame
        formatted ready for Excel
        year and breakdown type also added to start of dataframe
    """

    # Remove pupils with unknown values in the breakdowns (still included in totals)
    for breakdown in breakdowns:
        df = df.loc[df[breakdown] >= 0]

    # Sort by breakdown
    df = df.sort_values(by=breakdowns)

    # check for none breakdown content or use of default breakdown
    if not breakdowns:
        df["Breakdown_type"] = question
    elif breakdowns == ["grouping"]:
        df["Breakdown_type"] = question
    else:
        # Add the pupil group descriptor
        a = f"{'_'.join(breakdowns)}"
        b = question
        df["Breakdown_type"] = f"{a}_{b}"

    # Add year
    df["Year"] = year

    # Set the final column order
    df = df[column_order].reset_index(drop=True)

    return df


def percentage_by_domain(df, breakdowns, question, **kwargs):
    """Calculate the percentage, standard error, and confidence interval
    for each by group specified in breakdowns. Includes a check for single PSU
    strata, these will be missing in the final dataframe.

    Parameters
    ----------
    df: pd.DataFrame
    breakdowns: list[str]
    question: str

    Returns
    -------
    pd.DataFrame
    """
    logging.debug(
        f"Calculating standard error for {question} with domains"
        f"{breakdowns} and additional arguments {kwargs}"
    )

    # Create a single domain column for samplics estimator to use
    df["domain"] = create_domain(df, breakdowns)

    # Remove missing breakdowns, due to low no. these lead to
    # issues with the variance (e.g. zero division etc) and
    # these will be removed at the end anyway
    for breakdown in breakdowns:
        if pd.api.types.is_numeric_dtype(df[breakdown]):
            df = df[df[breakdown] >= 0]

    # Get standard errors of percentages
    standard_errors_df = stats.create_weighted_percentage_stats(
        df, question, domain="domain", **kwargs
    )

    return standard_errors_df


def create_breakdown_single(
    df,
    breakdowns,
    question,
    filter_condition,
    subgroup,
    create_SE=param.CREATE_SE
):
    """
    Will create the output based on any breakdowns (based on one or more breakdowns)
    with a single response question.

    Parameters
    ----------
    df : pandas.DataFrame
    breakdowns : list[str]
        these are the pupil breakdowns from the table e.g. sex and age1115
        if None, default value of 9999 will be used under heading 'grouping'
    question: str
        Single variable name that defines the question to be analysed
        (e.g. dallast5, alevr)
    filter_condition : str
        this is a non-standard, optional dataframe filter as a string
         needed for some tables. It may consist of one or more filters of the
         dataframe variables.
    subgroup: dictionary
        Optional input where a grouped response is reported, requiring a new response subgroup.
        Contains the new response code(s) that will be assigned to the new grouping(s),
         and the response values that will form the group.
    create_SE: bool
        Whether to create standard errors and CIs for the percentage
    Returns
    -------
    df : pandas.DataFrame
        with aggregated counts for the breakdowns to include:
        Weighted Count, Weighted Base, Unweighted Base and Prevalence (percent)
        year and breakdown type also added to start of dataframe
    """
    logging.debug(
        f"Creating table for question: {question}, with breakdowns: {breakdowns},"
        f" subgroup: {subgroup} and filter: {filter_condition}"
    )

    # Apply the optional table filter that is needed for some tables
    if filter_condition is None:
        filtered = df
    else:
        filtered = df.query(filter_condition)

    # Filter to pupils with a valid response to the question (not negative)
    filtered = filtered[filtered[question] >= 0].copy(deep=True)

    # Add breakdown groups if needed
    if not breakdowns:
        filtered["grouping"] = param.TOT_CODE
        breakdowns = ["grouping"]

    # Get required columns
    # Use set() in case param.STRATA is in breakdowns, ensure uniqueness
    select_cols = list(set((
        *breakdowns,
        question,
        param.WEIGHTING_VAR,
        param.STRATA,
        param.PSU,
    )))

    select = filtered[select_cols].copy(deep=True)

    if breakdowns != ["grouping"]:
        # Create the breakdown groups
        select = add_breakdown_groups(select, breakdowns, question)

    # Group the data to create the weighted and unweighted counts.
    numer_df = (select.groupby([*breakdowns, question])
                .agg(NumerW=(param.WEIGHTING_VAR, "sum"),
                     NumerU=(param.WEIGHTING_VAR, "count")).reset_index())

    # Create the weighted and unweighted bases for each pupil group
    denom_df = (numer_df.groupby(by=breakdowns)
                .agg(DenomW=("NumerW", "sum"),
                     DenomU=("NumerU", "sum")).reset_index())

    # Add any required response subgroups
    if subgroup is not None:
        numer_df = add_response_subgroup(
            numer_df,
            breakdowns,
            question,
            subgroup
        )

    # Join the bases to the weighted counts
    output = numer_df.merge(denom_df, how="left", on=breakdowns)

    # Add the percentages including supression/warnings
    output = add_percentage(output)

    if create_SE:
        # Standard errors will be off if using the standard
        # breakdown method, as if the STRATA is a breakdown the appending
        # of new data changes the survey design, so get rid of totals
        # and let python stats functions do the totalling
        breakdowns = [] if breakdowns == ["grouping"] else breakdowns
        select_se = select.copy()
        select_se = select_se[(select_se[breakdowns] != param.TOT_CODE).all(axis=1)]

        # Get standard errors of percentages
        standard_errors = stats_R.survey_perc_proportions(
            select_se,
            question,
            by=breakdowns
        )

        # If calculating subgroups, recode all subgroups to new values
        if subgroup:
            # Will calculate new SE for each subgroup in order
            # as subgroups may be nested
            se_subgroup_list = []
            for new_value, value_list in subgroup.items():
                select_subgroups = select_se.copy()
                select_subgroups.loc[
                    select_subgroups[question].isin(value_list), question
                ] = new_value

                # Get standard errors of percentages
                standard_errors_subgroups = stats_R.survey_perc_proportions(
                    select_subgroups, question, by=breakdowns
                )

                # Add only the new values (for the current subgroup)
                se_subgroup_list.append(
                    standard_errors_subgroups[
                        standard_errors_subgroups[question] == new_value
                    ]
                )

            # Attach all individual se df together
            standard_errors = standard_errors.append(
                pd.concat(se_subgroup_list)
            )

        # Join the variance calculations to both
        output = output.merge(standard_errors, how="left", on=[*breakdowns, question])

        # Internal check that methods are equivalent
        safe_check_columns_eq(output, "Percentage", "R_Percentage")

        # Suppress column based on similar rules as percentages
        for col in ["std_err", "lower_ci", "upper_ci", "deff"]:
            output[col] = suppress_column(output[col], output["DenomW"], round_to_dp=1)
    else:
        for col in ["std_err", "lower_ci", "upper_ci", "deff"]:
            output[col] = np.nan

    # Applies final output formatting removing default breakdowns
    # column if added earlier
    if breakdowns != ["grouping"]:
        column_order = ["Year", "Breakdown_type", *breakdowns, question, "NumerW",
                        "DenomW", "DenomU", "Percentage", "std_err", "lower_ci",
                        "upper_ci", "deff"]
    else:
        column_order = ["Year", "Breakdown_type", question, "NumerW",
                        "DenomW", "DenomU", "Percentage", "std_err", "lower_ci",
                        "upper_ci", "deff"]

    output = format_breakdown_output(output, breakdowns, question, column_order)

    return output


def create_breakdown_single_combine(
    df,
    breakdowns,
    questions,
    filter_condition,
    subgroup,
    create_SE=param.CREATE_SE
):
    """
    Creates and combines outputs for multiple questions using
    create_breakdown_single function

    Parameters
    ----------
    df : pandas.DataFrame
    breakdowns : list[str]
        optional breakdowns from the table e.g. ["sex", "age1115"]
    questions: list[str]
        list of questions to be used for outputs e.g. ["y7smok", "y8smok"]
    filter_condition: str
        optional filter on questions as a list with a string and a
        loop statement, e.g. "dcgstg3 == 1

        if filtering on each question then use {question} instead
        e.g. "{question} != 6"
        this allows filter to be applied within loop in function
        filter is applied to all questions
    subgroup: dictionary
        optional input where a grouped response is reported, requiring a new
        response subgroup
        contains the new response code(s) that will be assigned to the new
        grouping(s), and the response values that will form the group
        subgroup is generated for all questions e.g. {"UsedTotal": [1, 2, 3]}

    Returns
    -------
    df : pandas.DataFrame
        with aggregated counts for each question, response (with any subgroups)
        and any breakdowns to include:
        Weighted Count, Weighted Base, Unweighted Base and Prevalence (percent)
        Year, Question, Response and Breakdown columns (if provided) also added
        to start of dataframe
    """

    logging.debug(
        f"Creating combined table for questions: {questions}, "
        f"with breakdowns: {breakdowns} and filter: "
        f"{'None' if filter_condition is None else filter_condition}"
    )

    total_dfs = []

    if filter_condition is None:
        filter_condition = [None] * len(questions)

    else:
        filter_condition = [filter_condition.format(question=question)
                            for question in questions]

    for filter_condition, question in zip(filter_condition, questions):

        # create initial output from create_breakdown_single
        dfq = create_breakdown_single(df, breakdowns, question,
                                      filter_condition, subgroup, create_SE)

        # rename the question column to be a generic response column and insert the question as a new column
        dfq.rename(columns={question: "Response"}, inplace=True)
        dfq.insert(2, "Question", question)

        # append to total_dfs
        total_dfs.append(dfq)

    # combine outputs for all questions
    output = pd.concat(total_dfs)

    return output


def create_breakdown_multiple_discrete(
    df,
    breakdowns,
    responses,
    question,
    bases,
    filter_condition,
    create_SE=param.CREATE_SE
):
    """
    Will create the output based on any breakdowns (based on one or more
    breakdowns) with a multi response question with a discrete response:
    i.e.(i.e. 1 -> "Yes")

    Parameters
    ----------
    df : pandas.DataFrame
    breakdowns : list[str]
        these are the pupil breakdowns from the table e.g. sex and age1115.
    responses : list[str]
        these are the list of variables that contain responses options to this question.
    question: str
        the name of the new user defined variable that will contain the individual
        response questions defined in the 'responses' parameter - see above.
    bases : list[str]
        this is the list of variables that needs to be used for the pupil base.
        if greater than 1 base then length of bases should = length of responses.
        if the bases directly align with the responses then bases = responses.
    filter_condition : str
        this is an optional filter as a string to be applied to the table
    create_SE: bool
        Whether to create standard errors and CIs for the percentage

    Returns
    -------
    df : pandas.DataFrame
        with aggregated counts for the breakdowns to include:
        Weighted Count, Weighted Base, Unweighted Base and Prevalence (percent)
        year and breakdown type also added to start of dataframe
    """
    logging.debug(
        f"Creating table for question: {question}, with breakdowns: {breakdowns}"
        f", responses: {responses}, bases: {bases}, and filter {filter_condition}"
    )

    if len(bases) == 1:
        bases = bases * len(responses)
    elif len(bases) != len(responses):
        raise ValueError("Either need 1 base or an equal number of bases and responses")

    total_dfs = []
    for response, base in zip(responses, bases):

        if filter_condition is None:
            filtered = df
        else:
            filtered = df.query(filter_condition)

        # Filter to pupils with a valid response to the question used as the base (not negative).
        filtered = filtered[filtered[base] >= 0].copy(deep=True)

        # Rename the base variable
        # This is to allow for tables where each response variable is also it's own base
        # i.e. so df doesn't have the same variable name twice (response and base)
        base_adj = "base_" + base
        filtered[base_adj] = filtered[base]

        # Use set() in case param.STRATA is in breakdowns, ensure uniqueness
        select_cols = list(set([
            *breakdowns,
            response,
            base_adj,
            param.WEIGHTING_VAR,
            param.STRATA,
            param.PSU,
        ]))

        select = filtered[select_cols].copy(deep=True)

        # Transpose the individual response columns into a single question column
        select = transpose_multi(
            df=select,
            breakdowns=[col for col in select_cols if col not in [response, param.WEIGHTING_VAR]],
            question=question,
        )

        # Add a weighted count of yes (1) responses
        select["weighted_num"] = np.where(
            select["Value"] == 1, select[param.WEIGHTING_VAR], 0
        )

        # Create the breakdown groups
        select = add_breakdown_groups(select, breakdowns, question)

        # Base aggregations done for all Qs
        aggregations = {
            "NumerW": ("weighted_num", "sum"),
            "DenomW": (param.WEIGHTING_VAR, "sum"),
            "DenomU": (param.WEIGHTING_VAR, "count")
        }

        # Group the data to create the weighted counts.
        output = select.groupby([*breakdowns, question]).agg(**aggregations).reset_index()

        # Add_percentage
        output = add_percentage(df=output)

        if create_SE:
            # Standard errors will be off if using the standard
            # breakdown method, as if the STRATA is a breakdown the appending
            # of new data changes the survey design, so get rid of totals
            # and let python stats functions do the totalling
            select_se = select.copy()
            select_se = select_se[(select_se[breakdowns] != param.TOT_CODE).all(axis=1)]

            # Get standard errors of percentages
            standard_errors_df = stats_R.survey_perc_proportions(
                select_se,
                question="Value",
                by=breakdowns
            )
            # Retrieve only the levels we are interested in
            standard_errors_df = standard_errors_df.loc[
                standard_errors_df["Value"] == 1
            ]

            # Join the variance calculations to previous grouping
            # Insert question here in case breakdowns is empty
            standard_errors_df.insert(0, question, response)
            output = output.merge(
                standard_errors_df,
                how="left",
                on=[*breakdowns, question]
            )

            # Internal check that methods are equivalent
            safe_check_columns_eq(output, "Percentage", "R_Percentage")

            # Suppress column based on similar rules as percentages
            for col in ["std_err", "lower_ci", "upper_ci", "deff"]:
                output.loc[:, col] = suppress_column(output[col], output["DenomW"], round_to_dp=1)
        else:
            for col in ["std_err", "lower_ci", "upper_ci", "deff"]:
                output[col] = np.nan

        # Applies final output formatting
        column_order = [
            "Year",
            "Breakdown_type",
            *breakdowns,
            question,
            "NumerW",
            "DenomW",
            "DenomU",
            "Percentage",
            "std_err",
            "lower_ci",
            "upper_ci",
            "deff"
        ]
        output = format_breakdown_output(output, breakdowns, question, column_order)

        total_dfs.append(output)

    return pd.concat(total_dfs, axis=0).reset_index(drop=True)


def create_breakdown_multiple_cont(
    df,
    breakdowns,
    responses,
    question,
    base,
    filter_condition,
    create_SE=param.CREATE_SE
):
    """
    Will create the output based on any breakdowns (based on one or more
    breakdowns) for multi response questions with a continuous response
    (i.e. no. of units), where the function calculates the percentage of each
    weighted response as a total of all weighted responses summed.
    It assumes 'base' is the required total.

    Parameters
    ----------
    df : pandas.DataFrame
    breakdowns : list[str]
        these are the pupil breakdowns from the table e.g. sex and age1115.
    responses : list[str]
        these are the list of variables that contain responses options to this question.
    question: str
        the name of the new user defined variable that will contain the individual
        response questions defined in the 'responses' parameter - see above.
    base : str
        this is the variable that needs to be used for the pupil base.
        (needed as the base question is not always the same as the analysis
         question).
    filter_condition : str
        this is an optional filter as a string to be applied to the table
    create_SE: bool
        Whether to create standard errors and CIs for the percentage
    Returns
    -------
    df : pandas.DataFrame
        with aggregated counts for the breakdowns to include:
        Weighted Count, Weighted Base, Unweighted Base and Prevalence (percent)
        year and breakdown type also added to start of dataframe
    """
    logging.debug(
        f"Creating table for question: {question}, with breakdowns: {breakdowns}"
        f" ,responses: {responses}, base: {base}, and filter {filter_condition}"
    )

    # Apply the optional table filter that is needed for some tables
    if filter_condition is None:
        filtered = df
    else:
        filtered = df.query(filter_condition)

    # Filter to pupils with a valid response to the question used as the base (not negative).
    filtered = filtered[filtered[base] >= 0].copy(deep=True)

    # Use set() in case param.STRATA is in breakdowns, ensure uniqueness
    select_cols = list(set([
        *breakdowns,
        *responses,
        base,
        param.WEIGHTING_VAR,
        param.STRATA,
        param.PSU,
    ]))

    # Select the fields needed for the table
    select = filtered[select_cols].copy(deep=True)

    # Transpose the individual response columns into a single column
    select = transpose_multi(
        df=select,
        breakdowns=[col for col in select_cols if col not in [*responses, param.WEIGHTING_VAR]],
        question=question,
    )

    # Create new columns to be used for the weighted numerator / denominator
    # that are each of the responses values weighted, and the base question weighted
    select["weighted_num"] = select["Value"] * select[param.WEIGHTING_VAR]
    select["weighted_denom"] = select[base] * select[param.WEIGHTING_VAR]

    # Create the breakdown groups
    select = add_breakdown_groups(select, breakdowns, question)

    # Create aggregations including the sum of the total response options that
    # is used for the perentage denominator
    aggregations = {
        "NumerW": ("weighted_num", "sum"),
        "DenomW": (param.WEIGHTING_VAR, "sum"),
        "DenomU": (param.WEIGHTING_VAR, "count"),
        "DenomTotalW": ("weighted_denom", "sum"),
    }

    # Group the data to create the weighted counts.
    grouped = select.groupby([*breakdowns, question]).agg(**aggregations).reset_index()

    # Add the percentages including supression/warnings
    # Use Total weighted sum as denom rather than the usual default
    output = add_percentage(
        df=grouped,
        numerator="NumerW",
        denominator="DenomTotalW",
        denominator_sup="DenomW"
    )

    if create_SE:
        # Standard errors will be off if using the standard
        # breakdown method, as if the STRATA is a breakdown the appending
        # of new data changes the survey design, so get rid of totals
        # and let python stats functions do the totalling
        select_se = select.copy()
        select_se = select_se[(select_se[breakdowns] != param.TOT_CODE).all(axis=1)]

        standard_errors_df = stats_R.survey_perc_ratios(
            df=select_se,
            question="Value",
            base=base,
            by=[*breakdowns, question]
        )

        # Join the variance calculations to both
        output = output.merge(standard_errors_df, how="left", on=[*breakdowns, question])

        # Internal check that methods are equivalent
        safe_check_columns_eq(output, "Percentage", "R_Percentage")

        # Suppress column based on similar rules as percentages
        for col in ["std_err", "lower_ci", "upper_ci", "deff"]:
            output.loc[:, col] = suppress_column(output[col], output["DenomW"], round_to_dp=1)
    else:
        for col in ["std_err", "lower_ci", "upper_ci", "deff"]:
            output[col] = np.nan

    # Applies final output formatting
    column_order = [
        "Year",
        "Breakdown_type",
        *breakdowns,
        question,
        "NumerW",
        "DenomW",
        "DenomU",
        "Percentage",
        "std_err",
        "lower_ci",
        "upper_ci",
        "deff"
    ]
    output = format_breakdown_output(output, breakdowns, question, column_order)

    return output


def create_breakdown_statistics(df, breakdowns, questions, base, filter_condition):
    """
    Creates an output that includes statistics needed for the tables
    (based on one or more breakdowns)
    includes weighted mean, median and standard errors
    TODO: add standard error columns
    Parameters
    ----------
    df : pandas.DataFrame
    breakdowns : list[str]
        these are the pupil breakdowns from the table e.g. sex and age1115.
    questions: list[str]
        One or more variable names that defines the question in the survey for
        which the statistics will be created (e.g. nal7ut)
    base : str
        this is the variable that needs to be used for the pupil base.
        (needed as the base question is not always the same as the analysis
         question).
    filter_condition : str
        this is an optional filter as a string to be applied to the table

    Returns
    -------
    df : pandas.DataFrame
        with statistics added for the breakdowns to include:
        Weighted Mean, Weighted Median, Standard Error of the Weighted Mean
        year and breakdown type also added to start of dataframe
        Bases are also added for each breakdown
    """
    logging.debug(
        f"Creating table for question: {questions}, with breakdowns: {breakdowns}"
        f", base: {base}, and filter {filter_condition}"
    )
    # Statistics will be created for each question

    # Apply the optional table filter that is needed for some tables
    if filter_condition is None:
        filtered = df
    else:
        filtered = df.query(filter_condition)

    # Filter to pupils with a valid response to the base question
    filtered = filtered.loc[filtered[base] >= 0]

    # List to store outputs for each inputted question in questions
    total_dfs = []

    for question in questions:
        # Select the fields needed for the table
        select = filtered[
            [
                *breakdowns,
                question,
                param.WEIGHTING_VAR,
                param.STRATA,
                param.PSU,
            ]
        ].copy(deep=True)

        # Create the breakdown groups
        groups = add_breakdown_groups(select, breakdowns, question)

        # Remove any non-responses (still included in breakdown totals)
        for breakdown in breakdowns:
            groups = groups.loc[groups[breakdown] >= 0]

        # Group the data by the breakdowns, applying the weighted stats fct
        output = (
            groups
            .groupby(breakdowns)
            .apply(stats.create_weighted_stats, question)
        ).reset_index()

        # Pass to R to calculate survey statistics SE and CIs
        # Standard errors will be off if using the standard
        # breakdown method, as if the STRATA is a breakdown the appending
        # of new data changes the survey design, so get rid of totals
        # and let python stats functions do the totalling
        select_se = select.copy()
        select_se = select_se[(select_se[breakdowns] != param.TOT_CODE).all(axis=1)]
        standard_errors_df = stats_R.survey_stats(
            select_se,
            question,
            by=breakdowns
        )

        # Create the weighted and unweighted bases for each breakdown
        # (created from earlier step before stats grouping)
        denom_df = (groups.groupby(by=breakdowns)
                    .agg(DenomW=(param.WEIGHTING_VAR, "sum"),
                         DenomU=(param.WEIGHTING_VAR, "count")).reset_index())

        # Join the bases to the stats output
        output = output.merge(denom_df, how="left", on=breakdowns)
        output = output.merge(standard_errors_df, how="left", on=breakdowns)

        # Internal check that R and custom methods are equivalent
        safe_check_columns_eq(output, "R_Mean", "Mean")
        safe_check_columns_eq(output, "R_Median", "Median")

        # Insert a column that identifies the question from which the statistics are calculated
        output.insert(0, "Question", question)

        # Applies final output formatting
        column_order = [
            "Year",
            "Breakdown_type",
            *breakdowns,
            "Question",
            "DenomW",
            "DenomU",
            "Mean",
            "Median",
            "std_err",
            "lower_ci",
            "upper_ci",
            "deff"
        ]
        output = format_breakdown_output(output, breakdowns, question, column_order)

        total_dfs.append(output)
    # Concatenate the outputs for each question into a single DataFrame
    return pd.concat(total_dfs, axis=0).reset_index(drop=True)
