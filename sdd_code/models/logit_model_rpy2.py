import re

import numpy as np
import pandas as pd

import rpy2.robjects as robjects

import sdd_code.utilities.parameters as param
from sdd_code.models.r_integration import r_to_py, py_to_r


def logit_model(
    df,
    model_response,
    model_effects,
    bubble_factor,
    factor_ref=pd.DataFrame(**param.FACTOR_REF),
    weight=param.WEIGHTING_VAR,
    strata=param.STRATA,
    psu=param.PSU,
):
    """
    Use R (via rpy2) to create a logistic regression model of model response
    against effect.

    Parameters
    ----------
        df: pd.DataFrame
            A dataframe containing the data to model
        model_response: str
            The response variable that is being modelled
        model_effects: list[str]
            The effect variables. To test for an interaction, enter
            the variables as "effect1*effect2".
        bubble_factor: int
            Multipying factor for bubble visualisation of model effects
        factor_ref: pd.DataFrame
            A dataframe with rows of variables and the reference level to use for this
            variable, defaults to value in parameters.py
        weight: str
            The weighting variable in the dataset, defaults to value in parameters.py
        strata: str
            The strata variable in the dataset, defaults to value in parameters.py
        psu: str
            The PSU (cluster) variable in the dataset, defaults to value in parameters.py

    Returns
    -------
        Dict[str, pd.DataFrame]
        Dataframes of model information stored in a dictionary
    """

    # Get all effects, they may be interactions so have to split these
    # Get unique, as can list interactions alongside main effects
    effects_list = np.unique(
        # Sum flattens a list of lists, though is inefficient for large uses
        sum(
            # Split interaction effects, i.e. eff1*eff2 or eff1:eff2, into a sublist
            [list(re.split(r"\*|\||\:", eff)) for eff in model_effects],
            # Set start value of sum to an empty list
            []
        )
    )

    # Select just the variables we are interested in
    df = df[[model_response, *effects_list, strata, psu, weight]]

    # Setup main R object and load libraries
    r = robjects.r

    # Get custom R functions
    r.source(str(param.LOCAL_ROOT / "sdd_code" / "sddR" / "R" / "model_functions.R"))

    # Fill in missing data for model
    df = df.fillna(-9)

    # Convert dataframes to R compatible ones
    r_df = py_to_r(df)
    r_factor_ref = py_to_r(factor_ref)

    # Set factor levels, same as class ... (ref=) stmt in SAS model
    data = r.assign_factor_level(r_df, r_factor_ref)

    # Create model
    model = r.survey_logit(
        data=data,
        formula=f"{model_response} ~" + "+".join(model_effects),
        psu=psu,
        strata=strata,
        weight=weight,
    )

    # Calculate the overall significance of each effect
    anova_stats = r.sas_anova(model)

    # Calculate the impact of each effect on the model
    c_stats = r.effect_c_stats(
        model,
        bubble_factor
    )

    # Converts list of output stats and model info into a dataframe
    output = r.format_model_output(model)

    # Adds the anova stats to the above dataframe
    output = r.merge(output, anova_stats, by="Variable", all=True)

    output_py = r_to_py(output).reset_index(drop=True)
    c_stats_py = r_to_py(c_stats).reset_index(drop=True)
    
    # Sort the effect contributions by strength of effect (guess reduction)
    # First allocate a 1 to the overall model row so that this remains at the top
    c_stats_py["guess_reduction"] = np.where(c_stats_py["effect"] == "",
                                             1, c_stats_py["guess_reduction"])
    c_stats_py = c_stats_py.sort_values(by="guess_reduction", ascending=False)
    c_stats_py = c_stats_py.reset_index(drop=True)

    output_py["Year"] = param.YEAR

    # Use a dict for accessing each part of the output in create_models
    return {"Model": output_py, "Effect_Contributions": c_stats_py}
