import pytest
import pandas as pd
import numpy as np
import sdd_code.utilities.parameters as param

# If rpy2/R aren't installed then skip these tests
try:
    import rpy2
    from sdd_code.models.logit_model_R import logit_model
except ImportError:
    rpy2 = None


@pytest.mark.slow
@pytest.mark.skipif(
    rpy2 is None, reason="Skipping R integration tests if rpy2 is not installed"
)
def test_logit_model():
    """These tests check the integration of R and Python, so just check that the outputs
    of the logit functions are equivalent to the below R code, where output is the output
    model and c_stats are the effect contributions:

    library(here)

    if (file.exists(here("R", "model_functions.R"))) {
        source(here("R", "model_functions.R"))
    } else {
        source(here("sdd_code", "sddR", "R", "model_functions.R"))
    }

    test_data <- data.frame(
        resp = c(1, 1, 1, 0, 0, 1, 1, 0, 0, 0),
        eff1 = c(1, 1, 0, 0, 1, 1, 0, 0, 1, 0),
        eff2 = c(0, 1, 1, 0, 0, 1, 0, 0, 0, 1),
        psu = c(1, 2, 1, 2, 3, 3, 4, 4, 5, 5),
        strata = c(1, 1, 1, 1, 2, 2, 2, 2, 2, 2),
        weight = c(1, 1, 1, 1, 0.5, 1.5, 1, 1, 1, 1)
    )

    factor_ref <- data.frame(
        factors = c("resp", "eff1", "eff2"),
        refs = c("0", "0", "0")
    )

    test_data <- assign_factor_level(test_data, factor_ref)

    test <- survey_logit(
        test_data,
        formula = resp ~ eff1 + eff2,
        psu=~psu,
        strata=~strata,
        weight=~weight
    )

    c_stats <- effect_c_stats(test$model, bubble_factor=8)

    output <- format_model_output(test$model)
    output <- merge(output, test$anova_stats, by="Variable", all=TRUE)
    """
    input_df = pd.DataFrame(
        {
            "resp": [1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
            "eff1": [1, 1, 0, 0, 1, 1, 0, 0, 1, 0],
            "eff2": [0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
            "psu": [1, 2, 1, 2, 3, 3, 4, 4, 5, 5],
            "strata": [1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
            "weight": [1, 1, 1, 1, 0.5, 1.5, 1, 1, 1, 1],
        }
    )

    factor_ref = pd.DataFrame(
        {"factors": ["resp", "eff1", "eff2"], "refs": ["0", "0", "0"]}
    )

    expected_model = pd.DataFrame(
        {
            "Variable": ["eff1", "eff1", "eff2", "eff2", None],
            "Measure": ["eff10", "eff11", "eff20", "eff21", "(Intercept)"],
            "N": [5.0, 5.0, 6.0, 4.0, np.nan],
            "coefficient": [
                np.nan,
                1.3080,
                np.nan,
                1.8536,
                -1.2102,
            ],
            "odds_ratio": [
                np.nan,
                3.6986,
                np.nan,
                6.3828,
                0.2981,
            ],
            "prob_gt_t": [
                np.nan,
                0.3079,
                np.nan,
                0.3305,
                0.5439,
            ],
            "stderror": [
                np.nan,
                0.6871,
                np.nan,
                1.0591,
                1.3898,
            ],
            "lower_ci": [np.nan, 0.0, np.nan, 0.0, 0.0],
            "upper_ci": [np.nan, np.inf, np.nan, np.inf, np.inf],
            "ProbF": [
                0.3080,
                0.3080,
                0.3305,
                0.3305,
                np.nan,
            ],
            "Year": [param.YEAR, param.YEAR, param.YEAR, param.YEAR, param.YEAR],
        }
    )

    expected_effects = pd.DataFrame(
        {
            "pairs": [25, 25, 25],
            "bubble_factor": [8, 8, 8],
            "effect": [np.nan, "eff1", "eff2"],
            "c_statistic": [0.74, 0.7, 0.6],
            "incorrect_guesses": [6.5, 7.50, 10.0],
            "add_incorrect_guesses": [np.nan, 1.0, 3.5],
            "guess_reduction": [np.nan, 0.1333, 0.35],
            "bubble_diam": [np.nan, 3.2962, 5.3405],
        }
    )

    actual = logit_model(
        input_df,
        model_response="resp",
        model_effects=["eff1", "eff2"],
        factor_ref=factor_ref,
        weight="weight",
        strata="strata",
        psu="psu",
        bubble_factor=8
    )

    actual_model = actual["Model"].astype({"N": np.float64, "ProbF": np.float64})

    actual_effect = actual["Effect_Contributions"].astype(
        {"pairs": np.int64, "bubble_factor": np.int64}
    )

    pd.testing.assert_frame_equal(
        actual_model, expected_model, check_exact=False, rtol=1e-3
    )
    pd.testing.assert_frame_equal(
        actual_effect, expected_effects, check_exact=False, rtol=1e-3
    )
