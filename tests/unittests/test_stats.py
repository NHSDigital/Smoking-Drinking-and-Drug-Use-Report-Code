import math

import pytest
import pandas as pd

from sdd_code.utilities import stats

try:
    import samplics
except ImportError:
    samplics = None


@pytest.fixture()
def mean_input():
    df = pd.DataFrame(
        {
            "value": [1, 2, 3, 4, 5],
            "unweight": [1, 1, 1, 1, 1],
            "weight": [2, 1, 1, 1, 0],
            "strata": [1, 1, 1, 2, 2],
            "psu": [1, 1, 2, 3, 4],
        }
    )
    return df


@pytest.fixture()
def perc_input():
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


class TestWeightedMean:
    def test_unweighted(self, mean_input):
        # Test unweighted, should be equal to normal mean
        expected = 3.0
        actual = stats.weighted_mean(mean_input, "value", "unweight")
        assert actual == expected

    def test_simple_weighted(self, mean_input):
        # Test that a simple weighted example is as expected
        expected = 2.2
        actual = stats.weighted_mean(mean_input, "value", "weight")
        assert actual == expected


class TestWeightedMedian:
    def test_unweighted(self, mean_input):
        # Test unweighted, should be equal to normal median
        expected = 3.0
        actual = stats.weighted_median(mean_input, "value", "unweight")
        assert actual == expected

    def test_simple_weighted(self, mean_input):
        # Test that a simple weighted example is as expected
        # In this example, "halfway" is still at 2.5, which in the
        # cumulative sum of weights occurs at 2
        expected = 2.0
        actual = stats.weighted_median(mean_input, "value", "weight")
        assert actual == expected

@pytest.mark.skipif(
    samplics is None, reason="Skipping tests that use samplics if not installed"
)
class TestWeightedVariances:
    """
    Means and standard deviations checked against R, code is:
        library(data.table)
        library(survey)

        value <-  c(1, 2, 3, 4, 5)
        weight <- c(2, 1, 1, 1, 0) # or c(1, 1, 1, 1, 1) for unweighted
        strata <- c(1, 1, 1, 2, 2)
        psu <- c(1, 1, 2, 3, 4)

        data <-  data.table(value, weight, strata, psu)

        design <- svydesign(
            id = ~psu,
            strata = ~strata,
            weights = ~weight,
            data = data,
        )

        mean <- svymean(~value, design)
    The outputs from this are the expected_mean and expected_se.
    """

    def test_unweighted(self, mean_input):
        actual = stats.weighted_variances(
            mean_input, "value", "unweight", "strata", "psu"
        )
        expected_mean = 3.0
        expected_se = 0.6325

        assert math.isclose(actual.point_est, expected_mean, rel_tol=1e-4)
        assert math.isclose(actual.stderror, expected_se, rel_tol=1e-4)

    def test_weighted(self, mean_input):
        actual = stats.weighted_variances(
            mean_input, "value", "weight", "strata", "psu"
        )
        expected_mean = 2.2
        expected_se = 0.7694

        assert math.isclose(actual.point_est, expected_mean, rel_tol=1e-4)
        assert math.isclose(actual.stderror, expected_se, rel_tol=1e-4)


@pytest.mark.skipif(
    samplics is None, reason="Skipping tests that use samplics if not installed"
)
class TestCreateWeightedPercentageStats:
    """Proportion/percentage stats tested against R, note that small samples
    lead to odd CIs, but they match R. Code is below:
        library(survey)

        data <- data.frame(
            value= c(1, 1, 2, 2, 2),
            unweight= c(1, 1, 1, 1, 1),
            weight= c(0.5, 1, 1, 1, 1.5),
            strata= c(1, 1, 1, 2, 2),
            psu= c(1, 1, 2, 3, 4),
            domain_single= c(1, 1, 1, 1, 1),
            domain= c(1, 2, 3, 1, 2)
        )

        data$value <- as.factor(data$value)

        sdd_design <- svydesign(
            id = ~psu,
            strata = ~strata,
            weights = ~weight, # Or unweight for unweighted version
            data = data
        )

        # Get proportions (mult. by 100 to get percentage)
        props <- svyby(~value, by=~domain, design = sdd_design, FUN=svymean)
        # Get basic confidence intervals
        ci <- confint(props)
        # props <- svyby(~value, by=~domain_single, design = sdd_design, FUN=svymean)
    """

    def test_basic(self, perc_input):
        """Testing a simple unweighted example with no domains"""
        actual = stats.create_weighted_percentage_stats(
            df=perc_input,
            question="value",
            weighting="unweight",
            domain="domain_single",
            strata="strata",
            psu="psu"
        )

        expected = pd.DataFrame(
            {
                "_parameter": ["proportion", "proportion"],
                "domain": [1, 1],
                "value": [1, 2],
                "samplics_percentage": [40.0, 60.0],
                "std_err": [32.0, 32.0],
                "lower_ci_samp": [0.2145, 0.4814],
                "upper_ci_samp": [99.5186, 99.7855],
                "_cv": [0.8000, 0.5333],
                "lower_ci": [-22.72, -2.72],
                "upper_ci": [102.72, 122.72],
            }
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)

    def test_weighted(self, perc_input):
        """As above but weighted"""
        actual = stats.create_weighted_percentage_stats(
            df=perc_input,
            question="value",
            weighting="weight",
            domain="domain_single",
            strata="strata",
            psu="psu"
        )

        expected = pd.DataFrame(
            {
                "_parameter": ["proportion", "proportion"],
                "domain": [1, 1],
                "value": [1, 2],
                "samplics_percentage": [30.0, 70.0],
                "std_err": [27.1662, 27.1662],
                "lower_ci_samp": [0.1637, 0.8848],
                "upper_ci_samp": [99.12, 99.84],
                "_cv": [0.9055, 0.3881],
                "lower_ci": [-23.25, 16.75],
                "upper_ci": [83.2, 123.25],
            }
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)

    def test_domain(self, perc_input):
        """A full example with weights and domains"""
        actual = stats.create_weighted_percentage_stats(
            df=perc_input,
            question="value",
            weighting="weight",
            domain="domain",
            strata="strata",
            psu="psu"
        )

        expected = pd.DataFrame(
            columns=[
                "_parameter",
                "domain",
                "value",
                "samplics_percentage",
                "std_err",
                "lower_ci_samp",
                "upper_ci_samp",
                "_cv",
                "lower_ci",
                "upper_ci",
            ],
            data=[
                ["proportion", 1, 1, 33.3, 31.43, 0.1137, 99.55, 0.9428, -28.26, 94.93],
                ["proportion", 1, 2, 66.67, 31.43, 0.4534, 99.89, 0.4714, 5.070, 128.3],
                ["proportion", 2, 1, 40.0, 33.94, 0.1516, 99.66, 0.8485, -26.52, 106.5],
                ["proportion", 2, 2, 60.0, 33.94, 0.3404, 99.85, 0.5657, -6.525, 126.5],
                ["proportion", 3, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ["proportion", 3, 2, 100.0, 0.0, 100.0, 100.0, 0.0, 100.0, 100.0],
            ],
        )

        pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-3)


class TestCreateWeightedStats:
    def test_basic(self, mean_input):
        # Not testing outputs, just testing integration of functions
        expected = pd.Series(
            {
                "Mean": 2.2,
                "Median": 2.0,
            }
        )
        actual = stats.create_weighted_stats(
            mean_input, "value", "weight"
        )
        pd.testing.assert_series_equal(actual, expected, check_exact=False, rtol=1e-4)
