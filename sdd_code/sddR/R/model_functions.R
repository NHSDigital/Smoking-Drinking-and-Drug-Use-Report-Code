# Uses:
# survey - Survey stats and modelling functions
# ModelMetrics - GLM metrics & stats

# This should not be required, and is bad practice to source files in a package,
# however this is not a package (just local folder) so uses this to make functions
# available when called from Python (it works automatically in RStudio)
if (file.exists(here::here("R", "utils.R"))) {
    source(here::here("R", "utils.R"))
} else {
    source(here::here("sdd_code", "sddR", "R", "utils.R"))
}

#' Create a survey design object and model a logistic regression
#' for a given formula. Also calculates ANOVA and outputs.
#'
#' Used to ensure changes to the sdd survey logistic regression
#' only need to be made once, and to allow strings to be passed
#' in instead of formulas for ease of use with rpy2 and command line.
#'
#' @param data A dataset containing data needed for the model
#' @param formula A formula or string defining the model relationship
#' @param psu The ID/cluster column, as a string or formula
#' @param strata The strata column, as a string or formula
#' @param weight The weight column, as a string or formula
#'
#' @return A list of a model output from svyglm, and the ANOVA of that model
#'
#' @export
survey_logit  <- function(data, formula, psu, strata, weight) {
    # Coerce strings to formulas
    psu <- coerce_formula(psu)
    strata <- coerce_formula(strata)
    weight <- coerce_formula(weight)

    # Specify survey design, ID is cluster
    # Use super assignment to make sure that anova can see
    # the survey design object, otherwise it acts up
    survey_design <<- survey::svydesign(
        id = psu,
        strata = strata,
        weights = weight,
        data = data,
        nest = TRUE
    )

    # Model logistic (quasibinomial(link="logit")) based on design
    model <- survey::svyglm(
        formula = as.formula(formula),
        design = survey_design,
        family = quasibinomial(),
    )

    return(model)
}


#' Custom anova stats to replicate SAS
#'
#' @param survey_model A svyglm model
#'
#' @return A data.frame of each effect and the ProbF
#'
#' @export
sas_anova <- function(survey_model) {

    # Get all variables used as effects in the model
    formula <- survey_model$formula
    Variable <- all.vars(formula)[-1]

    # Pre-allocate stats vector
    ProbF <- vector(mode = "numeric", length=length(effects))

    # For all effects
    for (i in seq_along(Variable)) {
        # Calculate probF
        term <- as.formula(paste0("~", Variable[i]))

        reg_test <- survey::regTermTest(
            survey_model,
            test.terms=term,
            method="Wald",
            df=NULL,
            # lrt.approximation="satterthwaite"
        )

        ProbF[i] <- reg_test$p
    }

    output <- data.frame(Variable, ProbF)

    return(output)
}


#' Calculate the C statistic and a variety of associated stats
#' for a given survey model
#'
#' @param survey_model The complete survey model
#' @param bubble_factor Multiplying factor for bubble visualisation of model effects
#'
#' @return A dataframe of stats, along with the overall
#' model stats.
#'
#' @export
effect_c_stats  <- function(survey_model, bubble_factor) {
    formula <- survey_model$formula
    survey_design <- survey_model$survey.design
    data <- data.frame(survey_model$data)

    # Recalculate the model using binomial family (to allow AUC to work)
    # Turn off warnings of non-integer success (this is expected)
    oldw <- getOption("warn")
    options(warn = -1)
    bin_survey_model <- survey::svyglm(
        formula=formula,
        design=survey_design,
        family=binomial()
    )
    options(warn=oldw)

    # Extract vars from formula, to then remove 1 at a time
    effects <- all.vars(formula)[-1]
    response <- all.vars(formula)[1]

    # Pre-allocate stats vector
    c_stats <- vector(mode = "numeric", length=length(effects))

    # For all effects
    for (i in seq_along(effects)) {
        # Remove the effect
        effects_less_1 <- effects[!(effects == effects[i])]
        # Survey model
        oldw <- getOption("warn")
        options(warn = -1)
        model <- survey::svyglm(
            formula = paste0(paste0(response, "~"), paste(effects_less_1, collapse="+")),
            design = survey_design,
            family=binomial(link="logit")
        )
        options(warn=oldw)

        # Calculate AUC
        c = ModelMetrics::auc(model)
        c_stats[i] <- c
    }

    # This is the AUC for the entire model
    combined_c <- ModelMetrics::auc(bin_survey_model)
    # Get no. pairs of 1 and 0
    pair_no <- nrow(data[data[[response]] == 1,]) * nrow(data[data[[response]] == 0,])
    # Calculate incorrect guesses
    incorrect <- pair_no - (combined_c * pair_no)

    # Create stat DF
    c_stat_df <- data.frame(
        pairs = rep(pair_no, length(effects)),
        bubble_factor = rep(bubble_factor, length(effects)),
        effect = effects,
        c_statistic = c_stats
    )

    # Get all c statistic calculations
    c_stat_df$incorrect_guesses <- lapply(
        c_stat_df$c_statistic,
        function(x) {pair_no * (1 - x)}
    )
    c_stat_df$add_incorrect_guesses <- lapply(
        c_stat_df$incorrect_guesses,
        function(x) {x - incorrect}
    )
    c_stat_df$guess_reduction <- lapply(
        c_stat_df$incorrect_guesses,
        function(x) {(x - incorrect) / x}
    )
    c_stat_df$bubble_diam <- lapply(
        c_stat_df$guess_reduction,
        function(x) {sqrt(x / pi) * 2 * bubble_factor}
    )

    newrow <- list(pair_no, bubble_factor, "", combined_c, incorrect, NA, NA, NA)

    output <- rbind(newrow, c_stat_df)

    # This step needs to happen for rpy2 to be able to convert it to pandas
    return(data.frame(lapply(output, unlist)))
}


#' For a given data.frame and a data.frame of factors to reference
#' levels, assign all factors and ref levels in the main data.frame
#'
#' @param df data.frame with columns to make factors
#' @param factors A data.frame of factors to ref levels
#'
#' @return A data.frame with factors assigned
#'
#' @export
assign_factor_level <- function(df, factors) {
    # For all factors specified
    for (row in seq_len(nrow(factors))) {
        # Extract column name and reference level
        col_name <- factors$factors[row]
        ref_level <- factors$refs[row]

        # Check if column exists
        if (col_name %in% colnames(df)) {
            # Re-assign column as factor
            df[, col_name] <- relevel(
                as.factor(df[[col_name]]),
                ref = ref_level
            )
        }
    }

    return(df)
}


#' Convert a Logit model into a dataframe in SDD ready formatted output.
#' Creates a data.frame with columns for:
#' * questions,
#' * question levels(i.e. sex = 1),
#' * coefficients,
#' * standard error,
#' * Pr(>|t|) (the p-value),
#' * confidence intervals,
#' * odds ratios
#'
#' @param model A fitted GLM
#'
#' @return A data.frame with columns:
#'
#' @export
format_model_output <- function(model) {
    # Generic summary to get stderror and prob > t
    summ <- summary(model, statistic="Chisq")$coefficients

    # Get confidence intervals
    ci <- confint(model, level=0.95, method="Wald")

    # Create output table of model stats, Measure are all levels of categorical
    # variables investigated
    output <- data.frame(
        Measure = names(model$coefficients),
        coefficient = model$coefficients,
        # Calculate odds ratios from coefficients, e^beta
        odds_ratio = exp(model$coefficients),
        stderror = summ[, "Std. Error"],
        prob_gt_t = summ[, "Pr(>|t|)"],
        # Want CI of odds ratios, so expontiate
        lower_ci = exp(ci[, "2.5 %"]),
        upper_ci = exp(ci[, "97.5 %"])
    )

    # Get main column names alongside Measure
    # TODO: Switch to lapply or tranpose etc, shouldn't append to list in loop
    Variable <- c()
    Measure <- c()
    for (var in names(model$xlevels)) {
        for (level in model$xlevels[[var]]) {
            Variable <- append(Variable, var)
            Measure <- append(Measure, paste0(var, level))
        }
    }
    # Variable_Measure is table of columns and measures within columns
    Variable_Measure <- data.frame(Variable, Measure)

    # Get counts for each variable used, first initialise DF
    counts <- data.frame(Measure=character(), N = numeric())
    data <- as.data.frame((model$data))
    for (var in unique(Variable)) {
        # Get counts of each factor level occurence
        var_count <- data.frame(table(data[, var]))
        names(var_count) <- c("Measure", "N")
        # Initially measure column will just have each value, need to paste0 the
        # variable name
        var_count$Measure <- lapply(
          var_count$Measure,
          function(x) {paste0(var, x)}
        )
        counts <- rbind(counts, var_count)
    }
    counts$N <- as.numeric(counts$N)

    # Add generic column Variable to output
    output <- merge(Variable_Measure, output, all = TRUE, by = "Measure")
    # Add variable counts to output
    output <- merge(output, counts, all=TRUE, by= "Measure")

    column_order <- c(
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

    return(output[, column_order])
}
