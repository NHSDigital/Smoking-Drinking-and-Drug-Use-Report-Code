context("Model functions")

# =============================================================================#
# Creating test data
test_data <- data.frame(
    resp = c(1, 1, 1, 0, 0, 1, 1, 0, 0, 0),
    eff1 = c(1, 1, 0, 0, 1, 1, 0, 0, 1, 0),
    eff2 = c(0, 1, 1, 0, 0, 1, 0, 0, 0, 1),
    psu = c(1, 2, 1, 2, 3, 3, 4, 4, 5, 5),
    strata = c(1, 1, 1, 1, 2, 2, 2, 2, 2, 2),
    weight = c(1, 1, 1, 1, 0.5, 1.5, 1, 1, 1, 1)
)

# Set columns to factors so that modelling works correctly
cols <- names(test_data)[names(test_data) != "weight"]
test_data[cols] <- lapply(test_data[cols], as.factor)

test_design <- survey::svydesign(
    ids = ~psu,
    strata = ~strata,
    weights = ~weight,
    data = test_data
)

expected_model <- survey::svyglm(
    resp ~ eff1 + eff2,
    design=test_design,
    family=quasibinomial()
)

# =============================================================================#
# Testing factor assignment

test_that("assign_factor_level has modified dataframe as expected", {
    # Produce test data
    test_df <- data.frame(
        a = c(1, 1, 2, 2, 3, 4),
        b = c("a", "a", "b", "c", "c", "a")
    )

    factor_ref <- data.frame(
        factors = c("a", "b"),
        refs = c(1, "c")
    )

    # Get actual output to check
    data <- assign_factor_level(test_df, factor_ref)

    # Tests
    expect_s3_class(data, "data.frame")
    expect_s3_class(data$a, "factor")
    expect_s3_class(data$b, "factor")
    expect_equal(levels(data$a), c("1", "2", "3", "4"))
    expect_equal(levels(data$b), c("c", "a", "b"))
})

# =============================================================================#
# Testing survey_logit, these tests check that it produces outputs of an
# expected "shape"/type

test_that("Survey_logit produces an expected output", {
    # Generate actual output
    test_model <- survey_logit(
        test_data,
        formula=resp ~ eff1 + eff2,
        psu=~psu,
        strata=~strata,
        weight=~weight
    )

    # Tests
    expect_s3_class(
        test_model,
        "svyglm"
    )
    expect_equal(
      coef(test_model),
      coef(expected_model)
    )
})

# =============================================================================#
# Testing sas_anova

test_that("SAS_anova works as expected", {
    # Generate actual output
    test_model <- survey_logit(
        test_data,
        formula=resp ~ eff1 + eff2,
        psu=~psu,
        strata=~strata,
        weight=~weight
    )

    # Tests
    expect_equal(
        sas_anova(test_model),
        sas_anova(expected_model)
    )
    expect_s3_class(
        sas_anova(test_model),
        "data.frame"
    )
})
# =============================================================================#
# Testing effect_c_stats

test_that("effect_c_stats works as expected", {
    expect_s3_class(effect_c_stats(expected_model, bubble_factor=8), 'data.frame')
})

# =============================================================================#
# Testing format_model_output

test_that("format_model_output produces expected outputs", {
    # Generate data
    test_model <- survey_logit(
        test_data,
        formula=resp ~ eff1 + eff2,
        psu=~psu,
        strata=~strata,
        weight=~weight
    )
    test_output <- format_model_output(test_model)

    # Tests
    expect_s3_class(test_output, 'data.frame')
    expect_equal(
        names(test_output),
        c(
            "Variable",
            "Measure",
            "N",
            "coefficient",
            "odds_ratio",
            "prob_gt_t",
            "stderror",
            "lower_ci",
            "upper_ci"
        )
    )
    expect_equal(
        test_output,
        format_model_output(expected_model)
    )
})
