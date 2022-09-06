"""
This file contains the functions that define each model & it's parameters, as
well as the function that collects each model and specifies where it is to be saved
"""
from sdd_code.utilities import parameters as param
from sdd_code.models.logit_model_rpy2 import logit_model
# R subprocess version currently unused, but can be switched to by simply uncommenting
# the below line
# from sdd_code.models.logit_model_R import logit_model


def get_models():
    """Define the output workbooks and sheets for the model tables.

    Each element of sheets should be a key in the dictionary returned by the related
    model function.
    """
    output = {
        "output_path": param.OUTPUT_DIR / "MasterFiles" / "model_source.xlsx",
        "models": [
            {
                "name": "Drinking",
                "content": create_model_drank_lastwk,
                "sheets": ["Model", "Effect_Contributions"]
            },
            {
                "name": "Smoking",
                "content": create_model_smoker_current,
                "sheets": ["Model", "Effect_Contributions"]
            },
            {
                "name": "Drugs",
                "content": create_model_drugs,
                "sheets": ["Model", "Effect_Contributions"]
            },
        ],
    }
    
    return output


def create_model_drank_lastwk(df):
    """Creates the logistic regression model for the variable dallastwk,
    whether a pupil has drank in the last week.

    Parameters:
    -----------
        df: pd.DataFrame

    Returns:
    --------
        Dict[str, pd.DataFrame]
        Dataframes of model information stored in a dictionary
    """
    df_filt = df.loc[
        df['age1315'].isin([13, 14, 15])
        & df['dallastwk'].isin([0, 1])
        & df['version'].eq(1)
    ]

    model_response = "dallastwk"
    model_effects = [
        #"sex",
        "age1315",
        "dfasbands",
        "dcgstg3",
        #"dlifsat",
        #"dlifwor",
        "dlifhap",
        #"dlifanx",
        #"dlsalc",
        "ddgdrugs",
        "truant",
        #"excla",
        "dalfam",
        "dfamdrin",
        "region",
        #"schlearn",
        #"met4wks",
        "ethnicgp4",
    ]

    dranklastwk = logit_model(
        df_filt,
        model_response=model_response,
        model_effects=model_effects,
        bubble_factor=8
    )

    return dranklastwk


def create_model_smoker_current(df):
    """Creates the logistic regression model for the variable dcgsmk,
    whether a pupil is a current smoker.

    Parameters:
    -----------
        df: pd.DataFrame

    Returns:
    --------
        Dict[str, pd.DataFrame]
        Dataframes of model information stored in a dictionary
    """
    df_filt = df.loc[
        df['age1315'].isin([13, 14, 15])
        & df['dcgsmk'].isin([0, 1])
        & df['version'].eq(1)
    ]

    model_response = "dcgsmk"
    model_effects = [
        "sex",
        "age1315",
        #"dfasbands",
        "dallast3",
        #"dlifsat",
        #"dlifwor",
        #"dlifhap",
        #"dlifanx",
        #"dlssmk",
        "ddgdrugs",
        "cgelecevr",
        #"truant",
        #"excla",
        "dcgfam4",
        "dfamsmok",
        "dcgppfr",
        #"region",
        #"schlearn",
        #"met4wks",
        #"ethnicgp4",
    ]

    currentsmoke = logit_model(
        df_filt,
        model_response=model_response,
        model_effects=model_effects,
        bubble_factor=8
    )

    return currentsmoke


def create_model_drugs(df):
    """Creates the logistic regression model for the variable ddgmonany,
    whether a pupil has taken drugs in the last month

    Parameters:
    -----------
        df: pd.DataFrame

    Returns:
    --------
        Dict[str, pd.DataFrame]
        Dataframes of model information stored in a dictionary
    """
    df_filt = df.loc[
        df['age1315'].isin([13, 14, 15])
        & df['ddgmonany'].isin([0, 1])
        & df['version'].eq(2)
    ]

    model_response = "ddgmonany"
    model_effects = [
        #"sex",
        #"dfasbands",        
        "dcgstg3",
        "dallast3",
        "truant",
        #"excla",
        #"dlifhap",
        #"dlifanx",
        #"dlifwor",
        "ddgfam",
        #"region",
        #"dlsdrg",
        #"schlearn",
        "met4wks",
        "dlifsat",
        "age1315",  
        #"ethnicgp4",
    ]

    drugsmonth = logit_model(
        df_filt,
        model_response=model_response,
        model_effects=model_effects,
        bubble_factor=8
    )

    return drugsmonth
