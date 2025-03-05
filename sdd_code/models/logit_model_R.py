import re

import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
# Currently rpy2 used to get R HOME, relevant portion could be extracted to
# remove extra dependencies
from rpy2.situation import get_r_home

import sdd_code.utilities.parameters as param


def logit_model(
    df,
    model_response,
    model_effects,
    bubble_factor,
    factor_ref=pd.DataFrame(**param.FACTOR_REF),
    weight=param.WEIGHTING_VAR,
    strata=param.STRATA,
    psu=param.PSU,
    r_model=param.LOCAL_ROOT / "sdd_code" / "sddR" / "scripts" / "sdd_logistic.R",
    temp_data_loc=param.OUTPUT_DIR / "MasterFiles" / "intermediate_csvs",
    clean_up=True
):
    """This calls the R logistic regression model via the command line, with arguments
    specified via variables that are inserted into the call to Rscript.

    Parameters
    ----------
        df: pd.DataFrame
            A dataframe containing the data to model
        factor_ref: pd.DataFrame
            A dataframe with rows of variables and the reference level to use for this
            variable, defaults to value in parameters.py
        model_response: str
            The response variable that is being modelled
        model_effects: list[str]
            The effect variables
        bubble_factor: int
            Multiplying factor for bubble visualisation of model effects
        strata:
            The strata variable in the dataset, defaults to value in parameters.py
        weight:
            The weighting variable in the dataset, defaults to value in parameters.py
        psu:
            The PSU (cluster) variable in the dataset, defaults to value in parameters.py
        r_model: str|Path
            The path to the R file containing the model code to run, default to sdd_logistic.R
            in local R folder.
        temp_data_loc: str|Path
            The folder to output the temporary CSVs in, default to intermediate_csvs
        clean_up: bool
            Whether to delete temporary files, default to True

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
            # Split interaction effects, i.e. eff1*eff2 or eff1:eff2
            [list(re.split(r"\*|\||\:", eff)) for eff in model_effects],
            # Set start value of sum to an empty list
            []
        )
    )

    # Select just the variables we are interested in
    df = df[[model_response, *effects_list, strata, psu, weight]]

    # Set root for model data
    root = Path(temp_data_loc)

    # Set files for input/output
    model_data_file = root / "sdd_model_data.csv"
    factor_ref_file = root / "factors_to_refs.csv"
    output_model_file = root / "sdd_model.csv"
    output_c_file = root / "sdd_model_effects.csv"

    # Save input dataframes
    df.to_csv(model_data_file, index=False)
    factor_ref.to_csv(factor_ref_file, index=False)

    # Set model details
    formula = f"{model_response} ~" + "+".join(model_effects)

    # Set path to Rscript, how the R code is ran
    r_script = Path(get_r_home()) / "bin" / "Rscript"

    result = subprocess.run(
        [
            str(r_script),
            "--vanilla",
            str(r_model),
            "--model_data_file",
            str(model_data_file),
            "--output_model_file",
            str(output_model_file),
            "--output_c_file",
            str(output_c_file),
            "--factor_ref",
            str(factor_ref_file),
            "--formula",
            formula,
            "--strata",
            strata,
            "--psu",
            psu,
            "--weight",
            weight,
            "--bubble_factor",
            str(bubble_factor)
        ],
        # Capture console output from R
        capture_output=True,
        # Raises an error if the process fails
        # check=True
    )

    if result.returncode:
        raise RuntimeError(
            result.stdout.decode("utf-8"),
            result.stderr.decode("utf-8")
        )
    # Get output data from where R saved it

    model = pd.read_csv(output_model_file)
    c_stats = pd.read_csv(output_c_file)

    if clean_up:
        # Delete temp files
        model_data_file.unlink()
        factor_ref_file.unlink()
        output_model_file.unlink()
        output_c_file.unlink()

    model["Year"] = param.YEAR

    # Use a dict for accessing each part of the output in create_models
    return {"Model": model, "Effect_Contributions": c_stats}
