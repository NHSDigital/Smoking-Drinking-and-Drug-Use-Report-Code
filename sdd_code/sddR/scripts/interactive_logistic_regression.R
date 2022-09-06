# This is the simplified/interactive version of sdd_logistic.R
# Designed to be used as part of the interactive process of creating models.

# =============================================================================#
# Load  libraries
library(data.table) # Data structure akin to dataframe

# Set default root filepath for data
ROOT <- r"(\\output_filepath\)"

# =============================================================================#
# Source custom functions
# "here" looks for standard package folders to find the root, in this case
# it will locate the .Rproj folder or .git depending on where this is called
# from, so check both
if (file.exists(here::here("R", "model_functions.R"))) {
    source(here::here("R", "model_functions.R"))
} else {
    source(here::here("sdd_code", "sddR", "R", "model_functions.R"))
}

# =============================================================================#
# Data ingestion and preparation

# Get data from files
data <- fread(paste0(ROOT, "sdd_2018_all_derivations.csv"))

factor_ref <- fread(paste0(ROOT, "factor_ref.csv"))

# Treat all missing values equally
data[data == -8 | data == -1] <- -9
# Just in case, replace NA with -9
data[is.na(data)] <- -9

# Filter to just model data
data <- data[
    age1215 %in% c(12, 13, 14, 15)
    & dallastwk %in% c(0, 1)
    & version == 1
]

# Use factor_ref to get vars needed as categorical with correct ref level
data <- assign_factor_level(data, factor_ref)

# =============================================================================#
# Dranklastwk regression model
# Model logistic (quasibinomial(link="logit")) based on design
dranklastwk <- survey_logit(
    data=data,
    formula = dallastwk ~ age1215 + ethnicgp4 + dcgstg3 + ddgdrugs + truant + dalfam + dfamdrin,
    psu= ~archschn,
    strata = ~region,
    weight = ~pupilwt
)

# Calculate ANOVA
anova_stats <- sas_anova(dranklastwk)

# Get C statistics
c_stats <- effect_c_stats(
    dranklastwk,
    bubble_factor=8
)

# =============================================================================#
# Format output and write to file
dranklastwk_model <- format_model_output(dranklastwk)
dranklastwk_model <- merge(dranklastwk_model, anova_stats, by="Variable", all=TRUE)

fwrite(dranklastwk_model, paste0(ROOT, "dranklastwk_model.csv"))
fwrite(c_stats, paste0(ROOT, "dranklastwk_c_statistics.csv"))
