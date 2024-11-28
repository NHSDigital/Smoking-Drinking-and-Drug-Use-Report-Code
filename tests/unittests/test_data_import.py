import pandas as pd

from sdd_code.utilities import parameters as param
from sdd_code.utilities.data_import import import_sav_values


def test_data_import():
    """Tests the data import function against a known test .sav file.

    The .sav file has 6 columns, archsn, pupilwt, region, age, sex, cg7tot
    cg7tot should be dropped, all others are read in as float64
    """
    actual = import_sav_values(
        file_path=param.LOCAL_ROOT / "tests" / "data" / "test_data.sav",
        drop_col=param.DROP_COLUMNS,
    )
    expected = pd.DataFrame(
        {
            "archsn": [13816.0, 13817.0, 13818.0],
            "pupilwt": [0.56, 0.53, 0.79],
            "region": [1.0, 1.0, 2.0],
            "age": [11.0, 15.0, 12.0],
            "sex": [1.0, 1.0, 2.0],
        }
    )

    pd.testing.assert_frame_equal(actual, expected)
