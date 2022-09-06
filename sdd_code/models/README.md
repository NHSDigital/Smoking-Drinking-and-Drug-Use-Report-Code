[[_TOC_]]


# Overview

This file describes the design and usage of the R models in Python for SDD. The files in [`/sdd_code/models/`](/sdd_code/models/) are python modules that integrate the R code for creating survey logistic models into the main Python pipeline. The modules are:

1. [logit_model_R.py](logit_model_R.py)
2. [logit_model_rpy2.py](logit_model_rpy2.py)
3. [r_integration.py](r_integration.py)
4. [model_tables.py](model_tables.py)

The first two are different implementations of the R integration, the third contains helper functions for communicating between R and Python using rpy2, and
the final one contains simple functions to create each model.

# How Do They Work

For more detailed information on both the R code and setting up your R environment, check the README in [/sdd_code/sddR/](/sdd_code/sddR/README.md). For a simplified version of the R model, which should help with understanding the Python implementation, see [here](sdd_code/sddR/scripts/interactive_logistic_regression.R).


## [logit_model_rpy2.py](logit_model_rpy2.py)

This module uses [rpy2](https://rpy2.github.io/doc.html) to run R functions from Python. It starts an integrated R session that can be communicated with via Python objects. rpy2 surfaces R functions as Python objects in a number of ways, we use a call to `r = rpy2.robjects.r`. This allows the user to call any R function as if it were a python function using the `r` object. For example:
```python
survey_design = r.svydesign(...)
```
This uses the `svydesign` function from the R package `survey`. The module uses code and methods that will be familiar to both R and Python users.

Custom functions have been written in R to prepare the data for modelling, create the model, and format the model for output. These are loaded using `r.source(...)`.

The main function in this module is `logit_model`, for details on how to call it see the docstring. The steps are very similar to the ones in the base R model:
- It uses `py_to_r()` from [r_integration.py](r_integration.py) to convert pandas dataframes to R dataframes.
- Then a custom R function `r.assign_factor_level` converts columns to factors and sets their reference levels, see [here](https://www.stat.berkeley.edu/~s133/factors.html) for info on factors. The default factor/ref levels are set via the parameter `FACTOR_REF` in [parameters.py](sdd_code/utilities/parameters.py).
- Next it creates a survey design object and then generates the model based on that design using the custom function `r.survey_logit`. For more information on how this function works, see the survey [documentation](https://www.rdocumentation.org/packages/survey/versions/4.1-1/topics/svydesign).
- It then uses a custom function `r.effect_c_stats`, which calculates the impact that each model effect had on the final model.
- The model is converted to a pandas dataframe using `r_to_py()` before being returned.

## [logit_model_R.py](logit_model_R.py])

This module is a backup for if the `rpy2` library is ever unavailable. This uses the `subprocess` python library to call an R script via the command line. This R script, [sdd_logistic.R](sdd_code/sddR/R/sdd_logistic.R), has been written to accept command line arguments that define the model parameters. This module is the simplest, arguments passed into `logit_model` are passed through to the `subprocess.run` as strings that define the model parameters. As there is no direct communication between R and Python, any dataframes are transferred by first saving it to a temporary CSV, then passing the path to that CSV to the call to R. This is also how the model data is retrieved.

Note that the way it determines where the RScript file used to run R is located is via a helper functions from rpy2, if rpy2 was unavailable this function can be easily extracted from their source code. For details on arguments see the docstring.


# How Do I Use Them

The models are ran via [create_models.py](/sdd_code/create_models.py), which works similarly to [create_publication.py](/sdd_code/create_publication.py).

The models can also be ran interactively in RStudio using [interactive_logistic_regression.R](sdd_code/sddR/scripts/interactive_logistic_regression.R), which is useful for testing changes to the custom functions and exploring the raw model created by svyglm.


# How Do I Update Them

The models may need to be updated, either to check new effects or to add a new model. This can be done by simply updating the calls to `logit_model` in [model_tables.py](model_tables.py) with any new effects (making sure that [`FACTOR_REF`](sdd_code/utilities/parameters.py) is updated), or adding a new call to `logit_model` in a new table function.

`FACTOR_REF` is a pandas dataframe structured as a dictionary in [parameters.py](sdd_code/utilities/parameters.py) that defines the reference level for every categorical variable used in the model. For variables that are effects in the model, the reference level will be used to determine the coefficients *relative* to that level. For the response variable, this reference level sets the outcome that is *not* of interest, i.e. if it is set to `"0"` then outcome `"1"` will be modelled or vice-versa.

To update the underlying R code, for example to extract a new column or alter the model family, edit the functions in model_functions.R. This is the single point which all methods of running the models rely on.

To extract different columns or information, edit the R function `format_model_output` in `model_functions.R`. If the method used to apply factors needs editing, edit `assign_factor_level`. And if the main model needs to be adjusted, then edit `survey_logit`.