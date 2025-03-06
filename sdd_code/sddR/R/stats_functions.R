# Uses:
# survey - Survey stats and modelling functions
# data.table - data manipulation and reshaping functions
# here - Navigating project structure


# This should not be required, and is bad practice to source files in a package,
# however this is not a package (just local folder) so uses this to make functions
# available when called from Python (it works automatically in RStudio)
if (file.exists(here::here("R", "utils.R"))) {
    source(here::here("R", "utils.R"))
} else {
    source(here::here("sdd_code", "sddR", "R", "utils.R"))
}

#' Calculate a set of weighted statistics for the variable.
#'
#' Calculates columns: Mean, Median, std_err, lower_ci, upper_ci
#'
#' @param data A dataset
#' @param variable A formula or string defining the variable of interest
#' @param by A vector defining the subpopulations to calculate stats by, as
#' a string or a formula.
#' @param psu The ID/cluster column, as a string or formula
#' @param strata The strata column, as a string or formula
#' @param weights The weight column, as a string or formula
#'
#' @return data.frame
#'
#' @export
survey_stats <- function(data, variable, by, psu, strata, weights) {
    # Set package options to match SAS
    options(survey.lonely.psu="certainty")

    # Coerce strings to formulas
    psu <- coerce_formula(psu)
    strata <- coerce_formula(strata)
    variable <- coerce_formula(variable)
    weights <- coerce_formula(weights)
    by <- coerce_formula(by)

    # Specify survey design, ID is cluster
    survey_design <- survey::svydesign(
        id = psu,
        strata = strata,
        weights = weights,
        data = data,
        nest = TRUE
    )

    # Calculate means/medians for each subpopulations, using
    # svyby and survey funcs
    means <- survey::svyby(
        variable,
        by=by,
        design=survey_design,
        FUN=survey::svymean,
        deff = "replace"
    )

    # Technically calculated DEft, so sqrt to get DEff
    means$DEff <- sqrt(means$DEff)

    # Median is the 50% quantile
    # Ignore warnings from this, as low num breakdowns produce nans
    # this is expected
    medians <- suppressWarnings(survey::svyby(
        variable,
        by=by,
        design=survey_design,
        FUN=survey::svyquantile,
        quantile = c(0.5)
    ))

    ci <- confint(
        means,
        level = 0.95,
        df = survey::degf(survey_design)
    )

    output <- merge(
        means,
        ci,
        by="row.names",
        all=TRUE
    )

    output <- merge(
        output,
        medians,
        by=all.vars(by),
        all=TRUE
    )

    return(output)
}

#' Calculate a weighted ratio of one variable against another, as well as
#' standard errors and confidence intervals
#'
#'
#' @param data A dataset
#' @param variable A formula or string defining the numerator of the ratio
#' @param base A formula or string defining the denominator of the ratio
#' @param by A vector defining the subpopulations to calculate stats by, as
#' a string or a formula.
#' @param psu The ID/cluster column, as a string or formula
#' @param strata The strata column, as a string or formula
#' @param weights The weights column, as a string or formula
#'
#' @return data.frame
#'
#' @export
survey_ratio <- function(data, variable, base, by, psu, strata, weights) {
    # Set package options to match SAS
    options(survey.lonely.psu="certainty")

    psu <- coerce_formula(psu)
    strata <- coerce_formula(strata)
    variable <- coerce_formula(variable)
    weights <- coerce_formula(weights)
    base <- coerce_formula(base)
    by <- coerce_formula(by)

    # Specify survey design, ID is cluster
    survey_design <- survey::svydesign(
        id = psu,
        strata = strata,
        weights = weights,
        data = data,
        nest = TRUE
    )

    # Calculate ratios using svyratio
    ratios <- survey::svyby(
        variable,
        denominator = base,
        design = survey_design,
        by = by,
        FUN=survey::svyratio,
        deff = "replace"
    )

    # Get confidence intervals
    ci <- as.data.frame(confint(
        ratios,
        level = 0.95,
        df = survey::degf(survey_design)
    ))

    ratios$lower_ci <- ci[, "2.5 %"]
    ratios$upper_ci <- ci[, "97.5 %"]

    # Technically calculated DEft, so sqrt to get DEff
    ratios$DEff <- sqrt(ratios$DEff)

    return(ratios)
}


#' Calculate a weighted proportion of a variable, i.e. how often each value
#' of the variable occurs.
#'
#'
#' @param data A dataset
#' @param variable A formula or string defining variable of interest
#' @param by A vector defining the subpopulations to calculate stats by, as
#' a string or a formula.
#' @param psu The ID/cluster column, as a string or formula
#' @param strata The strata column, as a string or formula
#' @param weights The weights column, as a string or formula
#'
#' @return data.frame
#'
#' @export
survey_proportion <- function(data, variable, by, psu, strata, weights) {
    # Set package options to match SAS
    options(survey.lonely.psu="certainty")

    # Coerce strings to formulas
    psu <- coerce_formula(psu)
    strata <- coerce_formula(strata)
    variable <- coerce_formula(variable)
    weights <- coerce_formula(weights)
    by <- coerce_formula(by)

    # Change variable of interest to factor to calculate proportions
    data[[all.vars(variable)]] <- as.factor(data[[all.vars(variable)]])
    # Add a dummy factor level for if all values of variable are the same, this
    # lets us calculate the 0 SE
    levels(data[[all.vars(variable)]]) <- c(levels(data[[all.vars(variable)]]), "-1")

    # Specify survey design, ID is cluster
    survey_design <- survey::svydesign(
        id = psu,
        strata = strata,
        weights = weights,
        data = data,
        nest = TRUE
    )

    # Calculate proportions using svymean on a factor
    props <- survey::svyby(
        variable,
        by=by,
        design=survey_design,
        FUN=survey::svymean,
        deff="replace"
    )

    # Extract vars used in formulas
    by <- all.vars(by)
    variable <- all.vars(variable)


    # Will rename SE and props columns separately, avoid identical cols
    props_renamed <- props
    se_renamed <- props
    deff_renamed <- props

    # Rename the variable.value columns in props to just value for transposing
    # Do once each for proportion and standard error
    # Get the values for each variable
    new_names <- as.character(unique(data[[variable]]))
    # Create names as formatted in the data, to check
    old_prop_names <- paste0(variable, new_names)
    old_se_names <- paste0("se.", variable, new_names)
    old_deff_names <- paste0("DEff.", variable, new_names)
    for (i in seq_along(old_prop_names)) {
        # Rename just the proportion columns to the variable values
        names(props_renamed)[
            names(props_renamed) == old_prop_names[i]
        ] = new_names[i]

        # Rename just the standard error columns to variable values
        names(se_renamed)[
            names(se_renamed) == old_se_names[i]
        ] = new_names[i]

        # Rename just the deff columns to variable values
        names(deff_renamed)[
            names(deff_renamed) == old_deff_names[i]
        ] = new_names[i]
    }

    # Calculate confidence intervals
    # TODO: Change method to use vartype = c("se", "ci") in svyby?
    ci <- as.data.frame(confint(
        se_renamed,
        level = 0.95,
        df = survey::degf(survey_design) # Set DF to match SAS, avoid default of Inf
    ))

    # Add breakdowns and variable value joined by ".", used for merging
    ci$join <- sapply(rownames(ci), function(x) {
        variable_val <- strsplit(x, split=variable)[[1]][[2]]
        breakdowns <- strsplit(x, split=":")[[1]][[1]]

        return(paste(breakdowns, variable_val, sep="."))
    })

    # Transpose props wide to long, once for proportions and once for standard
    # errors of proportions. These will then be merged together
    props_melted <- data.table::melt(
        data=data.table::as.data.table(props_renamed),
        id.vars=by,
        measure.vars = new_names,
        variable.name = variable,
        value.name = "proportion"
    )

    se_melted <- data.table::melt(
        data=data.table::as.data.table(se_renamed),
        id.vars=by,
        measure.vars = new_names,
        variable.name = variable,
        value.name = "se"
    )

    deff_melted <- data.table::melt(
        data=data.table::as.data.table(deff_renamed),
        id.vars=by,
        measure.vars = new_names,
        variable.name = variable,
        value.name = "DEff"
    )

    # Technically calculated DEft, so sqrt to get DEff
    deff_melted$DEff <- sqrt(deff_melted$DEff)

    # Add breakdowns and variable value joined by ., used for merging
    # First convert from factor to character
    se_melted$var_as_chr <- lapply(se_melted[, ..variable], as.character)
    # Create list of columns that define the join, from breakdowns plus the q value
    cols <- append(by, "var_as_chr")
    # do.call takes a function and a list of arguments. We want the first few args
    # to be the columns we are pasting together, these should not have names. Then
    # we need a named argument to set the separator.
    joining_args <- unname(as.list(se_melted[, ..cols]))
    joining_args["sep"] <-"."
    se_melted$join <- do.call(paste, joining_args)

    # Add confidence intervals to SE table
    se_ci <- merge(as.data.frame(se_melted), ci, by="join")

    # Merge se_ci to props
    output <- merge(props_melted, se_ci, by=append(by, variable), all=TRUE)
    # Merge all output
    output <- merge(output, deff_melted, by=append(by, variable), all=TRUE)

    return(output)
}
