context("Utility functions")

# =============================================================================#
# Testing coerce_formula for different use-cases

test_that("coerce_formula correctly deals with all input types", {
    expect_equal(coerce_formula("~ var"), ~var)

    expect_equal(coerce_formula("var"), ~var)

    expect_equal(coerce_formula(~ var), ~var)

    expect_equal(coerce_formula("~ var1 + var2"), ~var1 + var2)

    expect_equal(coerce_formula("var1 + var2"), ~var1 + var2)

    expect_equal(coerce_formula(c("var1", "var2")), ~var1 + var2)

    expect_equal(coerce_formula(42), ~ 42)
})
