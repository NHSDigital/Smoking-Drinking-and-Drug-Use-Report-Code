import pandas as pd

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


def py_to_r(df: pd.DataFrame) -> robjects.DataFrame:
    """Convert Pandas dataframe to R compatible dataframe
    """
    with localconverter(robjects.default_converter + pandas2ri.converter):
        r_df = robjects.conversion.py2rpy(df)

    return r_df


def r_to_py(r_df: robjects.DataFrame) -> pd.DataFrame:
    """Convert R dataframe to pandas dataframe
    """
    with localconverter(robjects.default_converter + pandas2ri.converter):
        df = robjects.conversion.rpy2py(r_df)

    return df
