import pytest
import pandas as pd
import numpy as np
from sdd_code.utilities import processing
from sdd_code.utilities import parameters as param
from sdd_code.utilities.parameters import TOT_CODE as T


@pytest.fixture()
def input_df():
    """Standard input dataframe for a number of questions"""
    data = {
        "sex": [1, 1, 1, 2, 2, 2],
        "age": [11, 12, 11, 12, 11, 12],
        "region": [1, 2, 1, 2, 1, 2],
        "alevr": [1, 2, 3, 3, 2, 3],
        "variable": [1, 1, 1, 1, 1, 1],
    }
    return pd.DataFrame(data=data)


@pytest.fixture()
def single_breakdown_df():
    """Dataframe used for testing create_breakdown_single"""
    input_df = pd.DataFrame(
        {
            "sex": [1, 1, 1, 2, 2, 2, 2],
            "q": [1, 2, 3, 1, 2, 3, 1],
            param.WEIGHTING_VAR: [0.5, 0.5, 1, 1, 0.5, 1.5, 1],
            "filter": [1, 1, 1, 1, 1, 1, 0],
            param.STRATA: [1, 1, 1, 2, 2, 2, 2],
            param.PSU: [1, 1, 2, 3, 3, 3, 4],
        }
    )

    # Extend this data with copies of itself to prevent
    # suppression by add_percentage
    multiple_dfs = [input_df for i in range(30)]
    large_df = pd.concat(multiple_dfs)
    return large_df


@pytest.fixture()
def single_breakdown_df_combined():
    """Dataframe used for testing create_breakdown_single_combined"""
    input_df = pd.DataFrame(
        {
            "sex": [1, 1, 2, 1, 2, 2, 2],
            "y7smok": [1, 1, 1, 2, 2, 2, 2],
            "y8smok": [5, 5, 5, 6, 6, 6, 6],
            param.WEIGHTING_VAR: [0.25, 0.5, 0.5, 1, 1.25, 1.5, 1.75],
            param.STRATA: [1, 1, 1, 2, 2, 2, 2],
            param.PSU: [1, 1, 2, 3, 3, 3, 4],
        }
    )

    # Extend this data with copies of itself to prevent
    # suppression by add_percentage
    multiple_dfs = [input_df for i in range(90)]
    large_df_combined = pd.concat(multiple_dfs)

    return large_df_combined


def test_add_response_subgroup(input_df):
    """Tests add_response_subgroup, which will create a new
    alevr response of 10, created by combining alevr 2 & 3
    by sex, age, region. Due to the breakdowns, only 2 records
    will combine into 1.
    """
    expected = pd.DataFrame(
        {
            "sex": [1, 1, 1, 2, 2, 2, 1, 1, 2, 2],
            "age": [11, 12, 11, 12, 11, 12, 11, 12, 11, 12],
            "region": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            "alevr": [1, 2, 3, 3, 2, 3, 10, 10, 10, 10],
            "variable": [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        }
    )

    actual = processing.add_response_subgroup(
        input_df,
        breakdowns=["sex", "age", "region"],
        question="alevr",
        subgroup={10: [2, 3]},
    )

    pd.testing.assert_frame_equal(actual, expected)


def test_transpose_multi(input_df):
    """Tests transpose_multi, which will transpose every
    column that isn't in breakdowns + pupilwt.
    """
    input_df[param.WEIGHTING_VAR] = 1.0

    actual = processing.transpose_multi(
        input_df, ["sex", "age", "region"], question="Result"
    )

    expected = pd.DataFrame(
        columns=["sex", "age", "region", "pupilwt", "Result", "Value"],
        data=[
            [1, 11, 1, 1.0, "alevr", 1],
            [1, 11, 1, 1.0, "variable", 1],
            [1, 12, 2, 1.0, "alevr", 2],
            [1, 12, 2, 1.0, "variable", 1],
            [1, 11, 1, 1.0, "alevr", 3],
            [1, 11, 1, 1.0, "variable", 1],
            [2, 12, 2, 1.0, "alevr", 3],
            [2, 12, 2, 1.0, "variable", 1],
            [2, 11, 1, 1.0, "alevr", 2],
            [2, 11, 1, 1.0, "variable", 1],
            [2, 12, 2, 1.0, "alevr", 3],
            [2, 12, 2, 1.0, "variable", 1],
        ],
    )

    pd.testing.assert_frame_equal(actual, expected)


def test_suppress_column():
    input_df = pd.DataFrame(
        {
            "to_suppress": [10.59, 1.26, 0, 0, 124.97267, 50.167],
            "base": [10, 35, 40, 10, 30, 90],
        }
    )

    actual = processing.suppress_column(input_df["to_suppress"], input_df["base"])

    expected = pd.Series(["u", "[1]", "[-]", "u", "[125]", 50.167], name="to_suppress")

    pd.testing.assert_series_equal(actual, expected)
    
    
def test_suppress_column_round_dp():
    input_df = pd.DataFrame(
        {
            "to_suppress": [10.59, 1.26, 0, 0, 50.167],
            "base": [10, 35, 40, 10, 90],
        }
    )

    actual = processing.suppress_column(input_df["to_suppress"], input_df["base"], round_to_dp=1)

    expected = pd.Series(["u", "[1.3]", "[-]", "u", 50.167], name="to_suppress")

    pd.testing.assert_series_equal(actual, expected)


def test_add_percentage():
    """
    Tests add_percentage, should calculate a percentage of two columns and
    suppress those with DenomU below 30, round and add [] where DenomU
    between 30 and 50, and convert to [-] where NumerW = 0 and DenomU between 30 and 50
    """
    input_df = pd.DataFrame(
        {
            "NumerW": [15, 30, 40, 40, 60, 0, 0],
            "DenomW": [20, 45, 80, 50, 80, 90, 30],
            "DenomU": [10, 30, 40, 50, 100, 100, 40],
        }
    )

    expected = pd.DataFrame(
        {
            "NumerW": [15, 30, 40, 40, 60, 0, 0],
            "DenomW": [20, 45, 80, 50, 80, 90, 30],
            "DenomU": [10, 30, 40, 50, 100, 100, 40],
            "Percentage": ["u", "[67]", "[50]", 80.0, 75.0, 0.0, "[-]"],
        }
    )

    actual = processing.add_percentage(
        input_df, numerator="NumerW", denominator="DenomW", denominator_sup="DenomU"
    )

    pd.testing.assert_frame_equal(actual, expected)


def test_format_breakdown_output(input_df):
    # Set one breakdown to -9 to create a dropped row in formatting
    input_df.loc[5, "sex"] = -9

    breakdowns = ["sex", "age", "region"]
    question = "alevr"
    column_order = ["Year", "Breakdown_type", *breakdowns, question]
    expected = pd.DataFrame(
        {
            "Year": [param.YEAR, param.YEAR, param.YEAR, param.YEAR, param.YEAR],
            "Breakdown_type": [
                "sex_age_region_alevr",
                "sex_age_region_alevr",
                "sex_age_region_alevr",
                "sex_age_region_alevr",
                "sex_age_region_alevr",
            ],
            "sex": [1, 1, 1, 2, 2],
            "age": [11, 11, 12, 11, 12],
            "region": [1, 1, 2, 1, 2],
            "alevr": [1, 3, 2, 2, 3],
        }
    )

    actual = processing.format_breakdown_output(
        input_df,
        breakdowns=breakdowns,
        question=question,
        column_order=column_order,
        year=param.YEAR,
    )

    pd.testing.assert_frame_equal(actual, expected)


def test_create_breakdown_statistics():
    """Tested outputs against R, code to generate outputs is below:
    library(data.table)
    library(survey)

    test <- data.table(
        sex = c(1, 1, 1, 2, 2, 2, 2),
        question = c(1, 2, 3, 1, 2, 3, 1),
        weight = c(0.5, 0.5, 1, 1, 0.5, 1.5, 1),
        filter = c(1, 1, 1, 1, 1, 1, 0),
        strata = c(1, 1, 1, 2, 2, 2, 2),
        PSU = c(1, 1, 2, 3, 4, 5, 5)
    )

    # Specify survey design, ID is cluster
    surv_design <- svydesign(
        id = ~PSU,
        strata = ~strata,
        weights = ~weight,
        data = test
    )

    # Get mean/SE for each group, plus the total
    sex_mean <- svyby(~question, by = ~sex, FUN = svymean, design = surv_design)
    sex_quantile <- svyby(~question, by = ~sex, FUN = svyquantile, design = surv_design, quantile=c(0.5))
    total_mean <- svymean(~question, surv_design)
    total_median <- svyquantile(~question, design=surv_design, quantile=c(0.5))

    # Get confidence intervals, confint isn't accurate
    ci_sex_mean_1 <- svyciprop(~question, subset(surv_design, sex == 1), method="mean")
    ci_sex_mean_2 <- svyciprop(~question, subset(surv_design, sex == 2), method="mean")
    ci_total <- svyciprop(~question, surv_design, method="mean")
    """
    input_df = pd.DataFrame(
        {
            "sex": [1, 1, 1, 2, 2, 2, 2],
            "q": [1, 2, 3, 1, 2, 3, 1],
            param.WEIGHTING_VAR: [0.5, 0.5, 1, 1, 0.5, 1.5, 1],
            "filter": [1, 1, 1, 1, 1, 1, 0],
            param.STRATA: [1, 1, 1, 2, 2, 2, 2],
            param.PSU: [1, 1, 2, 3, 4, 5, 5],
        }
    )

    breakdowns = ["sex"]
    questions = ["q"]
    filter_condition = None
    actual = processing.create_breakdown_statistics(
        input_df, breakdowns, questions, questions[0], filter_condition
    )
    expected = pd.DataFrame(
        {
            "Year": [param.YEAR, param.YEAR, param.YEAR],
            "Breakdown_type": ["sex_q", "sex_q", "sex_q"],
            "sex": [1, 2, 9999],
            "Question": ["q", "q", "q"],
            "DenomW": [2.0, 4.0, 6.0],
            "DenomU": [3, 4, 7],
            "Mean": [2.25, 1.875, 2.0],
            "Median": [2.0, 1.0, 2.0],
            "std_err": [0.75, 0.3661, 0.3333],
            "lower_ci": [-0.1368, 0.7099, 0.9392],
            "upper_ci": [4.6368, 3.0401, 3.0608],
            "deff": [1.2792, 0.684, 0.8944],
        }
    ).astype(
        {
            "DenomW": float,
            "DenomU": np.int64,
        }
    )
    pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)


class TestCreateBreakdownSingle:
    def test_basic(self, single_breakdown_df):
        """Tests a very simple example of create_breakdown_single"""
        breakdowns = ["sex"]
        question = "q"
        filter_condition = None
        subgroup = None

        actual = processing.create_breakdown_single(
            single_breakdown_df,
            breakdowns,
            question,
            filter_condition,
            subgroup,
            create_SE=False,
        )

        expected = pd.DataFrame(
            {
                "Year": [
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                ],
                "Breakdown_type": [
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                ],
                "sex": [1, 1, 1, 2, 2, 2, T, T, T],
                "q": [1, 2, 3, 1, 2, 3, 1, 2, 3],
                "NumerW": [15.0, 15.0, 30.0, 60.0, 15.0, 45.0, 75.0, 30.0, 75.0],
                "DenomW": [60.0, 60.0, 60.0, 120.0, 120.0, 120.0, 180.0, 180.0, 180.0],
                "DenomU": [90, 90, 90, 120, 120, 120, 210, 210, 210],
                "Percentage": [
                    25.0,
                    25.0,
                    50.0,
                    50.0,
                    12.5,
                    37.5,
                    41.666666666666664,
                    16.666666666666668,
                    41.666666666666664,
                ],
                "std_err": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "lower_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "upper_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "deff": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "sex": np.int64,
                "q": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)

    def test_filter(self, single_breakdown_df):
        """Test using a filter condition on the previous example"""
        breakdowns = ["sex"]
        question = "q"
        subgroup = None
        filter_condition = "filter == 1"

        actual = processing.create_breakdown_single(
            single_breakdown_df,
            breakdowns,
            question,
            filter_condition,
            subgroup,
            create_SE=False,
        )

        expected = pd.DataFrame(
            {
                "Year": [
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                ],
                "Breakdown_type": [
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                ],
                "sex": [1, 1, 1, 2, 2, 2, T, T, T],
                "q": [1, 2, 3, 1, 2, 3, 1, 2, 3],
                "NumerW": [15.0, 15.0, 30.0, 30.0, 15.0, 45.0, 45.0, 30.0, 75.0],
                "DenomW": [60.0, 60.0, 60.0, 90.0, 90.0, 90.0, 150.0, 150.0, 150.0],
                "DenomU": [90, 90, 90, 90, 90, 90, 180, 180, 180],
                "Percentage": [
                    25.0,
                    25.0,
                    50.0,
                    33.333333333333336,
                    16.666666666666668,
                    50.0,
                    30.0,
                    20.0,
                    50.0,
                ],
                "std_err": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "lower_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "upper_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "deff": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "sex": np.int64,
                "q": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)

    def test_subgroup(self, single_breakdown_df):
        """Test creating a subgroup of 2/3"""
        breakdowns = ["sex"]
        question = "q"
        filter_condition = None
        subgroup = {10: [2, 3]}

        actual = processing.create_breakdown_single(
            single_breakdown_df,
            breakdowns,
            question,
            filter_condition,
            subgroup,
            create_SE=False,
        )

        expected = pd.DataFrame(
            {
                "Year": [
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                ],
                "Breakdown_type": [
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                ],
                "sex": [1, 1, 1, 1, 2, 2, 2, 2, T, T, T, T],
                "q": [1, 2, 3, 10, 1, 2, 3, 10, 1, 2, 3, 10],
                "NumerW": [
                    15.0,
                    15.0,
                    30.0,
                    45.0,
                    60.0,
                    15.0,
                    45.0,
                    60.0,
                    75.0,
                    30.0,
                    75.0,
                    105.0,
                ],
                "DenomW": [
                    60.0,
                    60.0,
                    60.0,
                    60.0,
                    120.0,
                    120.0,
                    120.0,
                    120.0,
                    180.0,
                    180.0,
                    180.0,
                    180.0,
                ],
                "DenomU": [90, 90, 90, 90, 120, 120, 120, 120, 210, 210, 210, 210],
                "Percentage": [
                    25.0,
                    25.0,
                    50.0,
                    75.0,
                    50.0,
                    12.5,
                    37.5,
                    50.0,
                    41.666666666666664,
                    16.666666666666668,
                    41.666666666666664,
                    58.333333333333336,
                ],
                "std_err": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "lower_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "upper_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "deff": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "sex": np.int64,
                "q": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)

    def test_no_breakdowns(self, single_breakdown_df):
        """Tests an example of create_breakdown_single with no breakdowns"""
        breakdowns = []
        question = "q"
        filter_condition = None
        subgroup = None

        actual = processing.create_breakdown_single(
            single_breakdown_df,
            breakdowns,
            question,
            filter_condition,
            subgroup,
            create_SE=False,
        )

        expected = pd.DataFrame(
            {
                "Year": [param.YEAR, param.YEAR, param.YEAR],
                "Breakdown_type": ["q", "q", "q"],
                "q": [1, 2, 3],
                "NumerW": [75.0, 30.0, 75.0],
                "DenomW": [180.0, 180.0, 180.0],
                "DenomU": [210, 210, 210],
                "Percentage": [
                    41.666666666666664,
                    16.666666666666668,
                    41.666666666666664,
                ],
                "std_err": [np.nan, np.nan, np.nan],
                "lower_ci": [np.nan, np.nan, np.nan],
                "upper_ci": [np.nan, np.nan, np.nan],
                "deff": [np.nan, np.nan, np.nan],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "q": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(actual, expected)

    def test_create_se(self, single_breakdown_df):
        """Testing create_SE=True"""
        breakdowns = ["sex"]
        question = "q"
        filter_condition = None
        subgroup = None

        actual = processing.create_breakdown_single(
            single_breakdown_df,
            breakdowns,
            question,
            filter_condition,
            subgroup,
            create_SE=True,
        )

        expected = pd.DataFrame(
            {
                "Year": [
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                ],
                "Breakdown_type": [
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                    "sex_q",
                ],
                "sex": [1, 1, 1, 2, 2, 2, T, T, T],
                "q": [1, 2, 3, 1, 2, 3, 1, 2, 3],
                "NumerW": [15.0, 15.0, 30.0, 60.0, 15.0, 45.0, 75.0, 30.0, 75.0],
                "DenomW": [60.0, 60.0, 60.0, 120.0, 120.0, 120.0, 180.0, 180.0, 180.0],
                "DenomU": [90, 90, 90, 120, 120, 120, 210, 210, 210],
                "Percentage": [
                    25.0,
                    25.0,
                    50.0,
                    50.0,
                    12.5,
                    37.5,
                    41.6667,
                    16.6667,
                    41.6667,
                ],
                "std_err": [
                    25.0,
                    25.0,
                    50.0,
                    25.0,
                    6.25,
                    18.75,
                    16.1971,
                    8.7841,
                    20.0308,
                ],
                "lower_ci": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "upper_ci": [
                    100.0,
                    100.0,
                    100.0,
                    100.0,
                    39.39157956093413,
                    100.0,
                    100.0,
                    54.46161835208119,
                    100.0,
                ],
                "deff": [
                    5.4467,
                    5.4467,
                    9.434,
                    5.4544,
                    2.0616,
                    4.2249,
                    4.7496,
                    3.4075,
                    5.8738,
                ],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "sex": np.int64,
                "q": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
                "std_err": np.dtype("O"),
                "lower_ci": np.dtype("O"),
                "upper_ci": np.dtype("O"),
                "deff": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(
            actual.reset_index(drop=True),
            expected.reset_index(drop=True),
            check_exact=False,
            rtol=1e-3,
        )

    def test_subgroup_and_se(self, single_breakdown_df):
        """Test creating a subgroup of 2/3"""
        breakdowns = ["sex"]
        question = "q"
        filter_condition = None
        subgroup = {10: [2, 3]}

        actual = processing.create_breakdown_single(
            single_breakdown_df,
            breakdowns,
            question,
            filter_condition,
            subgroup,
            create_SE=True,
        )

        expected_data = {
            "Year": [
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
                param.YEAR,
            ],
            "Breakdown_type": [
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
                "sex_q",
            ],
            "sex": [1, 1, 1, 1, 2, 2, 2, 2, 9999, 9999, 9999, 9999],
            "q": [1, 2, 3, 10, 1, 2, 3, 10, 1, 2, 3, 10],
            "NumerW": [
                15.0,
                15.0,
                30.0,
                45.0,
                60.0,
                15.0,
                45.0,
                60.0,
                75.0,
                30.0,
                75.0,
                105.0,
            ],
            "DenomW": [
                60.0,
                60.0,
                60.0,
                60.0,
                120.0,
                120.0,
                120.0,
                120.0,
                180.0,
                180.0,
                180.0,
                180.0,
            ],
            "DenomU": [90, 90, 90, 90, 120, 120, 120, 120, 210, 210, 210, 210],
            "Percentage": [
                25.0,
                25.0,
                50.0,
                75.0,
                50.0,
                12.5,
                37.5,
                50.0,
                41.6667,
                16.6667,
                41.6667,
                58.3333,
            ],
            "std_err": [
                25.0,
                25.0,
                50.0,
                25.0,
                25.0,
                6.25,
                18.75,
                25.0,
                16.1971,
                8.7841,
                20.0308,
                16.1971,
            ],
            "lower_ci": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "upper_ci": [
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                39.39157956093413,
                100.0,
                100.0,
                100.0,
                54.46161835208119,
                100.0,
                100.0,
            ],
            "deff": [
                5.4467,
                5.4467,
                9.434,
                5.4467,
                5.4544,
                2.0616,
                4.2249,
                5.4544,
                4.7496,
                3.4075,
                5.8738,
                4.7496,
            ],
        }

        expected = pd.DataFrame(expected_data).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "sex": np.int64,
                "q": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
                "std_err": np.dtype("O"),
                "lower_ci": np.dtype("O"),
                "upper_ci": np.dtype("O"),
                "deff": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)


class TestCreateBreakdownSingleCombined:
    def test_basic_combined(self, single_breakdown_df_combined):
        """Tests a very simple example of create_breakdown_single_combined"""

        breakdowns = ["sex"]
        questions = ["y7smok", "y8smok"]
        filter_condition = None
        subgroup = None

        actual = processing.create_breakdown_single_combine(
            single_breakdown_df_combined,
            breakdowns,
            questions,
            filter_condition,
            subgroup,
            create_SE=False,
        )

        expected = pd.DataFrame(
            {
                "Year": [
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                ],
                "Breakdown_type": [
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                ],
                "Question": [
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                ],
                "sex": [1, 1, 2, 2, T, T, 1, 1, 2, 2, T, T],
                "Response": [1, 2, 1, 2, 1, 2, 5, 6, 5, 6, 5, 6],
                "NumerW": [
                    67.5,
                    90.0,
                    45.0,
                    405.0,
                    112.5,
                    495.0,
                    67.5,
                    90.0,
                    45.0,
                    405.0,
                    112.5,
                    495.0,
                ],
                "DenomW": [
                    157.5,
                    157.5,
                    450.0,
                    450.0,
                    607.5,
                    607.5,
                    157.5,
                    157.5,
                    450.0,
                    450.0,
                    607.5,
                    607.5,
                ],
                "DenomU": [270, 270, 360, 360, 630, 630, 270, 270, 360, 360, 630, 630],
                "Percentage": [
                    42.857142857142854,
                    57.142857142857146,
                    10.0,
                    90.0,
                    18.51851851851852,
                    81.48148148148148,
                    42.857142857142854,
                    57.142857142857146,
                    10.0,
                    90.0,
                    18.51851851851852,
                    81.48148148148148,
                ],
                "std_err": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "lower_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "upper_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "deff": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "Question": str,
                "Response": np.int64,
                "sex": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(
            actual.reset_index(drop=True), expected.reset_index(drop=True)
        )

    def test_combined_filter(self, single_breakdown_df_combined):
        """Tests an example of create_breakdown_single_combined
        with a filter"""

        breakdowns = ["sex"]
        questions = ["y7smok", "y8smok"]
        filter_condition = "{question} != 6"
        subgroup = None

        actual = processing.create_breakdown_single_combine(
            single_breakdown_df_combined,
            breakdowns,
            questions,
            filter_condition,
            subgroup,
            create_SE=False,
        )

        expected = pd.DataFrame(
            {
                "Year": [
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                ],
                "Breakdown_type": [
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                ],
                "Question": [
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                ],
                "sex": [1, 1, 2, 2, T, T, 1, 2, T],
                "Response": [1, 2, 1, 2, 1, 2, 5, 5, 5],
                "NumerW": [67.5, 90.0, 45.0, 405.0, 112.5, 495.0, 67.5, 45.0, 112.5],
                "DenomW": [157.5, 157.5, 450.0, 450.0, 607.5, 607.5, 67.5, 45.0, 112.5],
                "DenomU": [270, 270, 360, 360, 630, 630, 180, 90, 270],
                "Percentage": [
                    42.857142857142854,
                    57.142857142857146,
                    10.0,
                    90.0,
                    18.51851851851852,
                    81.48148148148148,
                    100.0,
                    "[100]",
                    100.0,
                ],
                "std_err": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "lower_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "upper_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "deff": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "Question": str,
                "Response": np.int64,
                "sex": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(
            actual.reset_index(drop=True), expected.reset_index(drop=True)
        )

    def test_combined_subgroup(self, single_breakdown_df_combined):
        """Tests an example of create_breakdown_single_combined
        with a response subgroup added"""

        breakdowns = ["sex"]
        questions = ["y7smok", "y8smok"]
        filter_condition = None
        subgroup = {12: [1, 2]}

        actual = processing.create_breakdown_single_combine(
            single_breakdown_df_combined,
            breakdowns,
            questions,
            filter_condition,
            subgroup,
            create_SE=False,
        )

        expected = pd.DataFrame(
            {
                "Year": [
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                ],
                "Breakdown_type": [
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                ],
                "Question": [
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                ],
                "sex": [1, 1, 1, 2, 2, 2, T, T, T, 1, 1, 2, 2, T, T],
                "Response": [1, 2, 12, 1, 2, 12, 1, 2, 12, 5, 6, 5, 6, 5, 6],
                "NumerW": [
                    67.5,
                    90.0,
                    157.5,
                    45.0,
                    405.0,
                    450.0,
                    112.5,
                    495.0,
                    607.5,
                    67.5,
                    90.0,
                    45.0,
                    405.0,
                    112.5,
                    495.0,
                ],
                "DenomW": [
                    157.5,
                    157.5,
                    157.5,
                    450.0,
                    450.0,
                    450.0,
                    607.5,
                    607.5,
                    607.5,
                    157.5,
                    157.5,
                    450.0,
                    450.0,
                    607.5,
                    607.5,
                ],
                "DenomU": [
                    270,
                    270,
                    270,
                    360,
                    360,
                    360,
                    630,
                    630,
                    630,
                    270,
                    270,
                    360,
                    360,
                    630,
                    630,
                ],
                "Percentage": [
                    42.857142857142854,
                    57.142857142857146,
                    100.0,
                    10.0,
                    90.0,
                    100.0,
                    18.51851851851852,
                    81.48148148148148,
                    100.0,
                    42.857142857142854,
                    57.142857142857146,
                    10.0,
                    90.0,
                    18.51851851851852,
                    81.48148148148148,
                ],
                "std_err": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "lower_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "upper_ci": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
                "deff": [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "Question": str,
                "Response": np.int64,
                "sex": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(
            actual.reset_index(drop=True), expected.reset_index(drop=True)
        )

    def test_create_SE(self, single_breakdown_df_combined):
        """Tests creating a combined breakdown with standard errors"""

        breakdowns = ["sex"]
        questions = ["y7smok", "y8smok"]
        filter_condition = None
        subgroup = None

        actual = processing.create_breakdown_single_combine(
            single_breakdown_df_combined,
            breakdowns,
            questions,
            filter_condition,
            subgroup,
            create_SE=True,
        )

        expected = pd.DataFrame(
            {
                "Year": [
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                    param.YEAR,
                ],
                "Breakdown_type": [
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y7smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                    "sex_y8smok",
                ],
                "Question": [
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y7smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                    "y8smok",
                ],
                "sex": [1, 1, 2, 2, T, T, 1, 1, 2, 2, T, T],
                "Response": [1, 2, 1, 2, 1, 2, 5, 6, 5, 6, 5, 6],
                "NumerW": [
                    67.5,
                    90.0,
                    45.0,
                    405.0,
                    112.5,
                    495.0,
                    67.5,
                    90.0,
                    45.0,
                    405.0,
                    112.5,
                    495.0,
                ],
                "DenomW": [
                    157.5,
                    157.5,
                    450.0,
                    450.0,
                    607.5,
                    607.5,
                    157.5,
                    157.5,
                    450.0,
                    450.0,
                    607.5,
                    607.5,
                ],
                "DenomU": [270, 270, 360, 360, 630, 630, 270, 270, 360, 360, 630, 630],
                "Percentage": [
                    42.857142857142854,
                    57.142857142857146,
                    10.0,
                    90.0,
                    18.51851851851852,
                    81.48148148148148,
                    42.857142857142854,
                    57.142857142857146,
                    10.0,
                    90.0,
                    18.51851851851852,
                    81.48148148148148,
                ],
                "std_err": [
                    34.6338,
                    34.6338,
                    9.2195,
                    9.2195,
                    6.2621,
                    6.2621,
                    34.6338,
                    34.6338,
                    9.2195,
                    9.2195,
                    6.2621,
                    6.2621,
                ],
                "lower_ci": [
                    0.0,
                    0.0,
                    0.0,
                    50.331501873782216,
                    0.0,
                    54.53775728592035,
                    0.0,
                    0.0,
                    0.0,
                    50.331501873782216,
                    0.0,
                    54.53775728592035,
                ],
                "upper_ci": [
                    100.0,
                    100.0,
                    49.668498126217784,
                    100.0,
                    45.46224271407967,
                    100.0,
                    100.0,
                    100.0,
                    49.668498126217784,
                    100.0,
                    45.46224271407967,
                    100.0,
                ],
                "deff": [
                    11.4785,
                    11.4785,
                    5.8228,
                    5.8228,
                    4.0431,
                    4.0431,
                    11.4785,
                    11.4785,
                    5.8228,
                    5.8228,
                    4.0431,
                    4.0431,
                ],
            }
        ).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "Question": str,
                "Response": np.int64,
                "sex": np.int64,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
                "std_err": np.dtype("O"),
                "lower_ci": np.dtype("O"),
                "upper_ci": np.dtype("O"),
                "deff": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(
            actual.reset_index(drop=True),
            expected.reset_index(drop=True),
            check_exact=False,
            rtol=1e-4,
        )


class TestCreateBreakdownMultiple:
    def test_discrete_response(self):

        # Basic input df, resp1/2 are subquestions related
        # to base_q
        input_df = pd.DataFrame(
            {
                "sex": [1, 1, 1, 2, 2, 2],
                "resp": [1, 0, 0, -1, 1, 0],
                "base_q": [1, 1, 1, -1, 1, 1],
                param.WEIGHTING_VAR: [0.5, 0.5, 1, 1, 0.5, 1.5],
                param.STRATA: [1, 1, 1, 2, 2, 2],
                param.PSU: [1, 1, 2, 3, 3, 4],
            }
        )
        # Extend this data with copies of itself to prevent
        # suppression by add_percentage
        multiple_dfs = [input_df for i in range(30)]
        large_df = pd.concat(multiple_dfs)

        breakdowns = ["sex"]
        responses = ["resp"]
        question = "q"
        bases = ["base_q"]
        filter_condition = None
        actual = processing.create_breakdown_multiple_discrete(
            large_df,
            breakdowns,
            responses,
            question,
            bases,
            filter_condition,
            create_SE=True,
        )

        expected_data = {
            "Year": [param.YEAR, param.YEAR, param.YEAR],
            "Breakdown_type": ["sex_q", "sex_q", "sex_q"],
            "sex": [1, 2, 9999],
            "q": ["resp", "resp", "resp"],
            "NumerW": [15.0, 15.0, 30.0],
            "DenomW": [60.0, 60.0, 120.0],
            "DenomU": [90, 60, 150],
            "Percentage": [25.0, 25.0, 25.0],
            "std_err": [25.0000, 37.50000, 22.5347],
            "lower_ci": [0.0, 0.0, 0.0],
            "upper_ci": [100.0, 100.0, 100.0],
            "deff": [5.4467, 6.6521, 6.3525],
        }

        expected = pd.DataFrame(expected_data).astype(
            {
                "Year": np.dtype("O"),
                "Breakdown_type": str,
                "sex": np.int64,
                "q": str,
                "NumerW": float,
                "DenomW": float,
                "DenomU": np.int64,
                "Percentage": np.dtype("O"),
                "std_err": np.dtype("O"),
                "lower_ci": np.dtype("O"),
                "upper_ci": np.dtype("O"),
                "deff": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)

    def test_continuous_response(self):
        # Basic input df, resp1/2 are subquestions and base_1q
        # is a sum of resp1/2 unless missing
        input_df = pd.DataFrame(
            {
                "sex": [1, 1, 1, 2, 2],
                "resp1": [1, 0, 0, -1, 3],
                "resp2": [0, 2, 1, -1, 2],
                "base_q": [1, 2, 1, -1, 5],
                param.WEIGHTING_VAR: [0.5, 0.5, 1, 1.5, 1.5],
                param.STRATA: [1, 1, 2, 2, 2],
                param.PSU: [1, 2, 3, 4, 4],
            }
        )

        # Extend this data with copies of itself to prevent
        # suppression by add_percentage
        multiple_dfs = [input_df for i in range(30)]
        large_df = pd.concat(multiple_dfs)

        breakdowns = ["sex"]
        responses = ["resp1", "resp2"]
        question = "q"
        base = "base_q"
        filter_condition = None
        actual = processing.create_breakdown_multiple_cont(
            large_df,
            breakdowns,
            responses,
            question,
            base,
            filter_condition,
            create_SE=True,
        )

        expected_data = {
            "Year": [param.YEAR, param.YEAR, param.YEAR, param.YEAR, param.YEAR, param.YEAR],
            "Breakdown_type": ["sex_q", "sex_q", "sex_q", "sex_q", "sex_q", "sex_q"],
            "sex": [1, 1, 2, 2, 9999, 9999],
            "q": ["resp1", "resp2", "resp1", "resp2", "resp1", "resp2"],
            "NumerW": [15.0, 60.0, 135.0, 90.0, 150.0, 150.0],
            "DenomW": [60.0, 60.0, 45.0, 45.0, 105.0, 105.0],
            "DenomU": [90, 90, 30, 30, 120, 120],
            "Percentage": [20.0, 80.0, "[60]", "[40]", 50.0, 50.0],
            "std_err": [
                25.29822128134703,
                25.298221281347022,
                "[-]",
                "[-]",
                14.577379737113253,
                14.577379737113253,
            ],
            "lower_ci": [0.0, 0.0, '[60.0]', '[40.0]', 0.0, 0.0],
            "upper_ci": [100.0, 100.0, '[60.0]', '[40.0]', 100.0, 100.0],
            "deff": [6.360388781713381, 6.360388781713381, "[nan]", "[nan]", 7.602631123499285, 7.602631123499285],
        }
        expected = pd.DataFrame(expected_data).astype(
            {
                "std_err": np.dtype("O"),
                "deff": np.dtype("O"),
            }
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)


class TestAddBreakdownGroups(object):
    def test_two_breakdowns(self, input_df):
        breakdowns = ["sex", "age"]
        question = "alevr"

        actual = processing.add_breakdown_groups(
            input_df,
            breakdowns,
            question,
        )

        expected = pd.DataFrame(
            columns=["sex", "age", "region", "alevr", "variable"],
            data=[
                [1, 11, 1, 1, 1],
                [1, 12, 2, 2, 1],
                [1, 11, 1, 3, 1],
                [2, 12, 2, 3, 1],
                [2, 11, 1, 2, 1],
                [2, 12, 2, 3, 1],
                [T, 11, 1, 1, 1],
                [T, 12, 2, 2, 1],
                [T, 11, 1, 3, 1],
                [T, 12, 2, 3, 1],
                [T, 11, 1, 2, 1],
                [T, 12, 2, 3, 1],
                [1, T, 1, 1, 1],
                [1, T, 2, 2, 1],
                [1, T, 1, 3, 1],
                [2, T, 2, 3, 1],
                [2, T, 1, 2, 1],
                [2, T, 2, 3, 1],
                [T, T, 1, 1, 1],
                [T, T, 2, 2, 1],
                [T, T, 1, 3, 1],
                [T, T, 2, 3, 1],
                [T, T, 1, 2, 1],
                [T, T, 2, 3, 1],
            ],
        )

        pd.testing.assert_frame_equal(actual, expected)

    def test_three_breakdowns(self, input_df):
        breakdowns = ["sex", "age", "region"]
        question = "alevr"

        actual = processing.add_breakdown_groups(
            input_df,
            breakdowns,
            question,
        )

        expected = pd.DataFrame(
            columns=["sex", "age", "region", "alevr", "variable"],
            data=[
                [1, 11, 1, 1, 1],
                [1, 12, 2, 2, 1],
                [1, 11, 1, 3, 1],
                [2, 12, 2, 3, 1],
                [2, 11, 1, 2, 1],
                [2, 12, 2, 3, 1],
                [T, 11, 1, 1, 1],
                [T, 12, 2, 2, 1],
                [T, 11, 1, 3, 1],
                [T, 12, 2, 3, 1],
                [T, 11, 1, 2, 1],
                [T, 12, 2, 3, 1],
                [1, T, 1, 1, 1],
                [1, T, 2, 2, 1],
                [1, T, 1, 3, 1],
                [2, T, 2, 3, 1],
                [2, T, 1, 2, 1],
                [2, T, 2, 3, 1],
                [1, 11, T, 1, 1],
                [1, 12, T, 2, 1],
                [1, 11, T, 3, 1],
                [2, 12, T, 3, 1],
                [2, 11, T, 2, 1],
                [2, 12, T, 3, 1],
                [T, T, 1, 1, 1],
                [T, T, 2, 2, 1],
                [T, T, 1, 3, 1],
                [T, T, 2, 3, 1],
                [T, T, 1, 2, 1],
                [T, T, 2, 3, 1],
                [T, 11, T, 1, 1],
                [T, 12, T, 2, 1],
                [T, 11, T, 3, 1],
                [T, 12, T, 3, 1],
                [T, 11, T, 2, 1],
                [T, 12, T, 3, 1],
                [1, T, T, 1, 1],
                [1, T, T, 2, 1],
                [1, T, T, 3, 1],
                [2, T, T, 3, 1],
                [2, T, T, 2, 1],
                [2, T, T, 3, 1],
                [T, T, T, 1, 1],
                [T, T, T, 2, 1],
                [T, T, T, 3, 1],
                [T, T, T, 3, 1],
                [T, T, T, 2, 1],
                [T, T, T, 3, 1],
            ],
        )
        pd.testing.assert_frame_equal(actual, expected)
