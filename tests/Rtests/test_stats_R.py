import pytest
import pandas as pd
import numpy as np

from sdd_code.utilities import parameters as param

# If rpy2/R aren't installed then skip these tests
try:
    import rpy2
    from sdd_code.utilities.stats_R import (
        survey_stats,
        survey_perc_proportions,
        survey_perc_ratios,
    )
except ImportError:
    rpy2 = None


@pytest.fixture()
def stats_input():
    df = pd.DataFrame(
        {
            "value": [1, 2, 3, 4, 5, 6, 7, 8],
            "unweight": [1, 1, 1, 1, 1, 1, 1, 1],
            "weight": [2, 1, 1, 1, 0, 1, 1, 1],
            "strata": [1, 1, 1, 1, 2, 2, 2, 2],
            "psu": [1, 1, 2, 2, 3, 3, 4, 4],
            "domain_single": [1, 1, 1, 1, 1, 1, 1, 1],
            "domain": [1, 2, 1, 2, 1, 2, 1, 2],
        }
    )
    return df


@pytest.fixture()
def prop_input():
    df = pd.DataFrame(
        {
            "value": [1, 1, 2, 2, 2],
            "unweight": [1, 1, 1, 1, 1],
            "weight": [0.5, 1, 1, 1, 1.5],
            "strata": [1, 1, 1, 2, 2],
            "psu": [1, 1, 2, 3, 4],
            "domain_single": [1, 1, 1, 1, 1],
            "domain": [1, 2, 3, 1, 2],
        }
    )
    return df


@pytest.fixture()
def ratio_input():
    df = pd.DataFrame(
        {
            "value": [10, 15, 5, 0, 90],
            "base": [100, 100, 200, 200, 200],
            "unweight": [1, 1, 1, 1, 1],
            "weight": [0.5, 1, 1, 1, 1.5],
            "strata": [1, 1, 1, 2, 2],
            "psu": [1, 1, 2, 3, 4],
            "domain_single": [1, 1, 1, 1, 1],
            "domain": [1, 2, 3, 1, 2],
        }
    )
    return df


@pytest.mark.skipif(
    rpy2 is None, reason="Skipping R integration tests if rpy2 is not installed"
)
class TestSurveyStats:
    def test_unweighted(self, stats_input):
        expected = pd.DataFrame(
            {
                "R_Mean": [4.5],
                "std_err": [0.7071],
                "DEff.value": [0.6667],
                "deff": [0.8165],
                "lower_ci": [1.4576],
                "upper_ci": [7.5424],
                "R_Median": [4.0],
            }
        ).astype(np.float64)

        actual = (
            survey_stats(
                stats_input,
                "value",
                by=[],
                weights="unweight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)

    def test_weighted(self, stats_input):
        expected = pd.DataFrame(
            {
                "R_Mean": [4.0],
                "std_err": [1.0753],
                "DEff.value": [1.0673],
                "deff": [1.0331],
                "lower_ci": [-0.6266],
                "upper_ci": [8.6266],
                "R_Median": [3.0],
            }
        ).astype(np.float64)

        actual = (
            survey_stats(
                stats_input,
                "value",
                by=[],
                weights="weight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)

    def test_domain(self, stats_input):
        expected = pd.DataFrame(
            {
                "R_Mean": [4.0, 3.0, 5.0],
                "std_err": [1.0753, 1.4142, 0.7071],
                "DEff.value": [1.0673, 0.6667, 0.3],
                "deff": [1.0331, 0.8165, 0.5477],
                "lower_ci": [-0.6266, -3.0849, 1.9576],
                "upper_ci": [8.6266, 9.0849, 8.0424],
                "R_Median": [3.0, 1.0, 4.0],
                "domain": [param.TOT_CODE, 1.0, 2.0],
            }
        ).astype(np.float64)

        actual = (
            survey_stats(
                stats_input,
                "value",
                by=["domain"],
                weights="weight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)


@pytest.mark.skipif(
    rpy2 is None, reason="Skipping R integration tests if rpy2 is not installed"
)
class TestSurveyPercProportions:
    def test_unweighted(self, prop_input):
        expected = pd.DataFrame(
            {
                "value": [1.0, 2.0],
                "R_Percentage": [40.0, 60.0],
                "std_err": [32.0, 32.0],
                "lower_ci": [0.0, 0.0],
                "upper_ci": [100.0, 100.0],
                "deff": [1.3064, 1.3064],
            }
        ).astype(np.float64)

        actual = (
            survey_perc_proportions(
                prop_input,
                "value",
                by=[],
                weights="unweight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)

    def test_weighted(self, prop_input):
        expected = pd.DataFrame(
            {
                "value": [1.0, 2.0],
                "R_Percentage": [30.0, 70.0],
                "std_err": [27.1662, 27.1662],
                "lower_ci": [0.0, 0.0],
                "upper_ci": [100.0, 100.0],
                "deff": [1.1856, 1.1856],
            }
        )

        actual = (
            survey_perc_proportions(
                prop_input,
                "value",
                by=[],
                weights="weight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)

    def test_domain(self, prop_input):
        expected = pd.DataFrame(
            {
                "value": [1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0],
                "R_Percentage": [30.0, 70.0, 33.3333, 66.6667, 40.0, 60.0, 0.0, 100.0],
                "std_err": [
                    27.1662,
                    27.1662,
                    31.427,
                    31.427,
                    33.9411,
                    33.9411,
                    0.0,
                    0.0,
                ],
                "lower_ci": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 100.0],
                "upper_ci": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 0.0, 100.0],
                "deff": [
                    1.1856,
                    1.1856,
                    0.6667,
                    0.6667,
                    0.6928,
                    0.6928,
                    np.nan,
                    np.nan,
                ],
                "domain": [
                    param.TOT_CODE,
                    param.TOT_CODE,
                    1.0,
                    1.0,
                    2.0,
                    2.0,
                    3.0,
                    3.0,
                ],
            }
        )

        actual = (
            survey_perc_proportions(
                prop_input,
                "value",
                by=["domain"],
                weights="weight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)

    def test_constant_value(self):
        """Test for bug where constant question value would error,
        should give SE = 0, as checked against SAS"""

        input_df = pd.DataFrame(
            {
                "psu": [1, 1, 3, 4, 4],
                "strata": [1, 1, 1, 2, 2],
                "weight": [1, 1, 1, 1, 1],
                "var": [1, 1, 1, 1, 1],
            }
        )

        expected = pd.DataFrame(
            {
                "var": [1.0],
                "R_Percentage": [100.0],
                "std_err": [0.0],
                "lower_ci": [100.0],
                "upper_ci": [100.0],
                "deff": [np.nan],
            }
        )

        actual = survey_perc_proportions(
            input_df, "var", [], "psu", "strata", "weight"
        ).reset_index(drop=True)

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)


@pytest.mark.skipif(
    rpy2 is None, reason="Skipping R integration tests if rpy2 is not installed"
)
class TestSurveyPercRatio:
    def test_unweighted(self, ratio_input):
        expected = pd.DataFrame(
            {
                "R_Percentage": [15.0],
                "std_err": [11.5244],
                "deff": [1.1491],
                "lower_ci": [0.0],
                "upper_ci": [64.5856],
            }
        ).astype(np.float64)

        actual = (
            survey_perc_ratios(
                ratio_input,
                "value",
                base="base",
                by=[],
                weights="unweight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)

    def test_weighted(self, ratio_input):
        expected = pd.DataFrame(
            {
                "R_Percentage": [18.8235],
                "std_err": [13.9663],
                "deff": [1.30223],
                "lower_ci": [0.0],
                "upper_ci": [78.9157],
            }
        ).astype(np.float64)

        actual = (
            survey_perc_ratios(
                ratio_input,
                "value",
                base="base",
                by=[],
                weights="weight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-4)

    def test_domain(self, ratio_input):
        expected = pd.DataFrame(
            {
                "R_Percentage": [18.8235, 2.0, 37.5, 2.5],
                "std_err": [13.9663, 2.2627, 7.955, 0.0],
                "deff": [1.3023, 0.6667, 0.6928, np.nan],
                "lower_ci": [0.0, 0.0, 3.2726, 2.5],
                "upper_ci": [78.9157, 11.7358, 71.7274, 2.5],
                "domain": [param.TOT_CODE, 1.0, 2.0, 3.0],
            }
        ).astype(np.float64)

        actual = (
            survey_perc_ratios(
                ratio_input,
                "value",
                base="base",
                by=["domain"],
                weights="weight",
                strata="strata",
                psu="psu",
            )
            .reset_index(drop=True)
            .astype(np.float64)
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)
