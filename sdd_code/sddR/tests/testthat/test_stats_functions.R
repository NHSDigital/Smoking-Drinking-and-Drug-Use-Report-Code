context("Stats functions")

# NOTE: These mainly test integration, testing against actual values is done
# in main python functions that call these
# =============================================================================#
# Setup test data
test_data <- data.frame(
    resp = c(1, 1, 1, 0, 0, 1, 1, 0, 0, 0),
    eff1 = c(1, 1, 0, 0, 1, 1, 0, 0, 1, 0),
    eff2 = c(0, 1, 1, 0, 0, 1, 0, 0, 0, 1),
    psu = c(1, 2, 1, 2, 3, 3, 4, 4, 5, 5),
    strata = c(1, 1, 1, 1, 2, 2, 2, 2, 2, 2),
    weight = c(1, 1, 1, 1, 0.5, 1.5, 1, 1, 1, 1),
    by = c(1, 2, 1, 2, 1, 1, 2, 1, 2, 1)
)

test_design <- survey::svydesign(
    ids = ~ psu,
    strata = ~ strata,
    weights = ~ weight,
    data = test_data
)

# =============================================================================#
# Testing
test_that("survey_stats works as expected", {
    test_stats <- survey_stats(
        data = test_data,
        variable = ~ resp,
        psu = ~ psu,
        by = ~ by,
        strata = ~ strata,
        weights = ~ weight
    )
    expect_s3_class(test_stats, "data.frame")
    expect_equal(nrow(test_stats), 2)
    expect_equal(ncol(test_stats), 10)
})


test_that("survey_ratio works as expected", {
    test_stats <- survey_ratio(
        data = test_data,
        variable = ~ resp,
        base = ~ eff1,
        psu = ~ psu,
        by = ~ by,
        strata = ~ strata,
        weights = ~ weight
    )
    expect_s3_class(test_stats, "data.frame")
    expect_equal(nrow(test_stats), 2)
    expect_equal(ncol(test_stats), 6)
})


test_that("survey_proportion works as expected", {
    test_stats <- survey_proportion(
        data = test_data,
        variable = ~ resp,
        psu = ~ psu,
        by = ~ by,
        strata = ~ strata,
        weights = ~ weight
    )
    expect_s3_class(test_stats, "data.frame")
    expect_equal(nrow(test_stats), 4)
    expect_equal(ncol(test_stats), 9)
})
