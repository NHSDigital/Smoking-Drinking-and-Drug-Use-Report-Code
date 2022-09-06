[[_TOC_]]

# Overview
This file documents the setup, implementation, and design of the R code in SDD.

# Setup
This section assumes that both R and RStudio are installed, and your Python libraries have been updated using the [requirements.txt](/requirements.txt). To setup the R packages needed, simply open RStudio, go to `File > Open Project...`, and open the [sddR.RProj](sddR.RProj) file in this directory. This will initialise the project, and should install any packages required that have not been installed. If it does not, then open and run [setup.R](setup.R). Once that has ran and installed all packages without issue, then you can run the models either from [create_models.py](sdd_code/create_models.py), or interactively in RStudio. The statistical R functions are integrated into the main pipeline. Neither RStudio or R need to be open to run the Python process.


# Implementation Details
## [model_functions.R](/R/model_functions.R)
This file contains utility functions for manipulating the input/output of the models and the main modelling function. The main functions are listed below. For more information, including inputs/outputs, see each function's docstring.

### 1. survey_logit

This function combines `svydesign()` and `svyglm()` from the survey package to provide a single point to create the SDD logistic regression models. It can accept model and survey design details as either formulas or strings, for ease of use with rpy2 and subprocess.

It additionally calculates the ANOVA for the model, and outputs a 2 element list of the model and the anova_stats.

### 2. assign_factor_level

When modelling a logistic regression, categorical model effects are modeled against a "reference level". This is one category of the effect that all others are compared against. This function ensures that all categorical effects are [factors](https://www.stat.berkeley.edu/~s133/factors.html) in the data.frame, and sets the reference levels using the factors data.frame passed in.

### 3. format_model_output

The model object created by svyglm needs to be manipulated before being returned, for example to calculate the odds ratios and to re-format it into a desired structure. This function extracts the required information from the survey model object.

### 4. effect_c_stats

This calculates the impact that each model effect had on the overall model, by iteratively recalculating the model without each effect and calculating the AUC for each.

### 5. sas_anova

This function replicates the ANOVA done in SAS, as the standard R `anova` function did not exactly replicate prior values. It does this by repeatedly calling `regTermTest`.

## [stats_functions.R](/R/stats_functions.R)

This file contains the functions used to produce survey statistics for tables, using the R survey package. The main functions are listed below. For more documentation including inputs/outputs, see each functions docstring. These functions are called in [stats_R.py](..\utilities\stats_R.py), and used during processing to both produce SEs and CIs and as checks that custom calculations of weighted means/medians have worked.

### 1. survey_stats

This function calculates the Mean, Median, and standard errors/confidence limits for a variable in a dataset. It does this by any breakdowns/subpopulations specified, and accounting for the survey design.

### 2. survey_ratio

This function calculates a weighted ratio of one variable against another, as well as standard errors and confidence intervals.

### 3. survey_proportion

This function calculates a weighted proportion of a variable, i.e. how often each value of the variable occurs, as well as standard errors and confidence intervals.

## [utils.R](/R/utils.R)

This file contains any utility functions used.

### 1. coerce_formula

This function takes in a string, formula, or list of strings, and attempts to coerce them to a formula object.

## [sdd_logistic.R](/scripts/sdd_logistic.R)
This file is the R script ran by [logit_model_R](sdd_code/models/logit_model_R.py). It uses `getopt` to accept command line arguments, setting defaults if it has been ran from RStudio. The steps here are the same steps used by each model creation method, so are not described here for brevity.

## [interactive_logistic_regression.R](/scripts/interactive_logistic_regression.R)
This file exists as a simplified example of the modelling process, that can be used to design new models and test changes to the model functions by running interactively in RStudio. The steps are as follows:
- It first replaces all missing data with -9
- Then sets the factor levels using assign_factor_level
- Creates the model using survey_logit
- Extracts relevant information using format_model_output.
- Finally merges the formatted model and anova_stats to create the final output

# Dependency Management
This project tracks the dependencies in the DESCRIPTION file, which notes the packages required as well as any minimum version requirements if they exist. To add a new required package, add it to both this DESCRIPTION file, and the list of packages in setup.R.

A conda environment can be used to install and manage R dependencies, but the set of packages and their versions required is not currently available on the default conda channel. If conda-forge is available, then conda can be used to install all dependencies by uncommenting the R dependencies in [environment.yml](/environment.yml) and running `conda env create -f environment.yml`. This removes the need to use setup.R, but that method is still preferred.

# Testing
Although the R code for SDD is not a package, a very similar structure has been used for ease of development and to enable bundling into a package in the future. To test the code in R, run [/tests/testthat.R](/tests/testthat.R). These tests are also ran via pytest when testing the code in Python.

# R Structure
The R code in this directory is structured similarly to a package, for several reasons. Firstly this enables us to use some package tools to make development easier, i.e. testthat, devtools, etc. This also enables it to be brought out and made into a package in the future if that's required. The structure is as follows:

```
sddR
│   .Rbuildignore                               - Will be used if creating a package
│   .Rprofile                                   - Used to run code when opening the project, in this case setup.R
│   DESCRIPTION                                 - Describes the package and what packages it depends on
│   NAMESPACE                                   - Used to make package functions available, currently only helps in RStudio as this is not a package
│   README.md
│   sddR.Rproj                                  - Open this in RStudio to open the whole package
│   setup.R                                     - Installs required packages
│
├───man                                         - This folder is created by devtools::document(), and enables hovering tooltips and ?function for help
│       assign_factor_level.Rd
│       ...
│
├───R                                           - The source functions for the package
│       model_functions.R
│       stats_functions.R
│       utils.R
│
├───scripts                                     - Any script files that can be directly ran
│       interactive_logistic_regression.R       - Used for testing changes to the models
│       sdd_logistic.R                          - Can be called by Python via subprocess
│
└───tests                                       - The R tests for the package
    │   testthat.R
    │
    └───testthat
            test_model_functions.R
            test_stats_functions.R
            test_utils.R
```