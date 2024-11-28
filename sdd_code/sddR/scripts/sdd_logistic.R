#!/usr/bin/env Rscript
# =============================================================================#
# Load libraries
library(data.table) # Data structure akin to dataframe
library(getopt) # Enables command line arguments

# =============================================================================#
# Enable calling this from the command line with options

# Each line of the matrix allows an argument of the style --arg to be added to a
# command line call of this R script.
# The first column defines the long flag, e.g. --output_file. The second defines
# an optional short flag, -o. The third specifies whether the argument is
# required (1), optional (2), or should have no arguments (0).
# The final specifies argument type (char, int, etc)
spec <- matrix(c(
    "model_data_file", "m", 1, "character",
    "output_model_file", "o", 1, "character",
    "output_c_file", "c", 1, "character",
    "bubble_factor", "b", 1, "character",
    "factor_ref", "r", 1, "character",
    "formula", "f", 1, "character",
    "strata", "s", 1, "character",
    "psu", "p", 1, "character",
    "weight", "w", 1, "character"
), byrow = TRUE, ncol = 4)

opt <- getopt(spec)

# =============================================================================#
# Source custom functions
# "here" looks for standard package folders to find the root, in this case
# it will locate the .git folder or .Rproj so account for both
if (file.exists(here::here("R", "model_functions.R"))) {
    source(here::here("R", "model_functions.R"))
} else {
    source(here::here("sdd_code", "sddR", "R", "model_functions.R"))
}

# =============================================================================#
# Set default options
# All cmd arguments are required, this is for running the file within RStudio

# Set default root filepath
DEFAULT_ROOT <- r"(\\output_filepath\)"

if (is.null(opt$model_data_file)) {
    opt$model_data_file <- paste0(DEFAULT_ROOT, "sdd_2018_all_derivations.csv")
}
if (is.null(opt$output_model_file)) {
    opt$output_model_file <- paste0(DEFAULT_ROOT, "dranklastwk_model.csv")
}
if (is.null(opt$output_c_file)) {
    opt$output_c_file <- paste0(DEFAULT_ROOT, "dranklastwk_c_stats.csv")
}
if (is.null(opt$bubble_factor)) {
    opt$bubble_factor <- 8
}
if (is.null(opt$factor_ref)) {
    opt$factor_ref <- paste0(DEFAULT_ROOT, "factor_ref.csv")
}
if (is.null(opt$formula)) {
    opt$formula <- "dallastwk ~ age1215 + ethnicgp4 + dcgstg3 + ddgdrugs + truant + dalfam + dalwhodr"
}
if (is.null(opt$strata)) {
    opt$strata <- "region"
}
if (is.null(opt$psu)) {
    opt$psu <- "archschn"
}
if (is.null(opt$weight)) {
    opt$weight <- "pupilwt"
}

# =============================================================================#
# Main program

# Get data from command line arg
data <- fread(file = opt$model_data_file)

factor_ref <- fread(opt$factor_ref, colClasses = c("character", "character"))

# Replace missing with -9, glm can't handle NaNs and they are an allowed level
data[is.na(data)] <- -9

# Use factor_ref to get vars needed as categorical with correct ref level
data <- assign_factor_level(data, factor_ref)

model <- survey_logit(
    data = data,
    formula = opt$formula,
    psu = opt$psu,
    strata = opt$strata,
    weight = opt$weight
)

# Calculate ANOVA
anova_stats <- sas_anova(model)

# Get C statistics
c_stats <- effect_c_stats(
    model,
    bubble_factor=as.numeric(opt$bubble_factor)
)

# Format output and write to file
output <- format_model_output(model)
output <- merge(output, anova_stats, by="Variable", all=TRUE)

fwrite(output, opt$output_model_file)
fwrite(c_stats, opt$output_c_file)
