import pandas as pd
import pytest

from sdd_code.utilities.field_definitions import exclusion_flags


def test_dummy_drug_flag():
    """
    Tests the dummy drug flag has been implemented correctly

    """
    input_df = pd.DataFrame({"dgofsem": [1, 0, 1, 0, 1, 1, 0],
                             "dgtdsem": [0, 0, 1, 0, 0, 1, 0]})
    return_df = exclusion_flags.dummy_drug_flag(input_df)

    expected = [1, 0, 1, 0, 1, 1, 0]
    actual = list(return_df["dflagdummydrug"].astype(int))

    assert actual == expected, f"When checking for flagdummydrug, expected to find {expected} but found {actual}"


def test_cig_outlier_flag():
    """
    Tests the flag for high individual daily cigarette quantities (49 cigarettes
    or higher) has been implemented correctly

    """
    input_df = pd.DataFrame({"cg7mon": [0, 50, 23, 2, 7, 9, 12, 10, 55],
                             "cg7tue": [10, 13, 70, 4, 8, 11, 4, 13, 60],
                             "cg7wed": [5, 2, 11, 53, 6, 2, 3, 9, 59],
                             "cg7thu": [6, 9, 20, 7, 49, 7, 15, 19, 62],
                             "cg7fri": [20, 17, 9, 3, 3, 51, 13, 5, 56],
                             "cg7sat": [35, 18, 4, 6, 7, 11, 66, 3, 73],
                             "cg7sun": [15, 6, 2, 14, 8, 5, 9, 80, 81]})
    return_df = exclusion_flags.cig_outlier_flag(input_df)

    expected = [0, 1, 1, 1, 1, 1, 1, 1, 1]
    actual = list(return_df["dflagcigoutlier"].astype(int))

    assert actual == expected, f"When checking for flagcigoutlier, expected to find {expected} but found {actual}"


def test_high_alc_quant_flag():
    """
    Tests the high alcohol quantity flag has been implemented correctly

    """

    input_df = pd.DataFrame({"al7brlrptn": [15, 0, 0, 80, 0, 1, 0],
                             "al7brlrhp": [5, 50, 1, 0, 10, 1, 5],
                             "al7brlrlg": [8, 10, 1, 0, 0, 1, 0],
                             "al7brlrsmn": [20, 0, 1, 0, 0, 1, 0],
                             "al7brlrbt": [0, 10, 1, 0, 0, 1, 0],
                             "al7cdptn": [3, 12, 1, 0, 6, 1, 0],
                             "al7cdhpn": [0, 8, 1, 0, 0, 1, 0],
                             "al7cdlgn": [1, 0, 1, 0, 8, 1, 6],
                             "al7cdsmn": [0, 0, 1, 0, 0, 1, 0],
                             "al7cdbtn": [10, 0, 1, 0, 10, 1, 0],
                             "al7wnshgs": [0, 0, 1, 0, 0, 1, 0],
                             "al7spgs": [0, 6, 1, 0, 0, 0, 0],
                             "al7ppcn": [2, 0, 1, 15, 0, 1, 0],
                             "al7ppbt": [0, 100, 1, 10, 0, 1, 0],
                             "al7otpt": [1, 0, 1, 0, 1, 1, 0],
                             "al7othp": [0, 7, 1, 0, 5, 1, 0],
                             "al7otlg": [0, 0, 1, 0, 0, 1, 0],
                             "al7otsm": [1, 0, 1, 0, 0, 1, 0],
                             "al7otbt": [0, 0, 1, 0, 0, 1, 5],
                             "al7otgs": [0, 0, 1, 0, 1, 1, 0]
                             })
    return_df = exclusion_flags.high_alc_quant_flag(input_df)

    expected = [0, 1, 0, 1, 0, 0, 0]
    actual = list(return_df["dflaghighalcquant"].astype(int))

    assert actual == expected, f"When checking for flaghighalcquant, expected to find {expected} but found {actual}"


def test_all_alc_types_flag():
    """
    Tests the all alcohol types flag has been implemented correctly

    """

    input_df = pd.DataFrame({"al7brlrptn": [15, 11, 0, 8, 0, 1, 0],
                             "al7brlrhp": [5, 5, 1, 6, 10, 1, 0],
                             "al7brlrlg": [8, 10, 1, 9, 0, 1, 0],
                             "al7brlrsmn": [20, 18, 1, 5, 0, 1, 0],
                             "al7brlrbt": [0, 10, 1, 10, 0, 1, 0],
                             "al7cdptn": [3, 12, 1, 4, 6, 1, 0],
                             "al7cdhpn": [0, 8, 1, 3, 0, 1, 0],
                             "al7cdlgn": [1, 5, 1, 6, 8, 1, 0],
                             "al7cdsmn": [0, 12, 1, 9, 0, 1, 0],
                             "al7cdbtn": [10, 9, 1, 5, 10, 1, 0],
                             "al7wnshgs": [0, 5, 1, 3, 0, 1, 0],
                             "al7spgs": [0, 6, 1, 8, 0, 0, 0],
                             "al7ppcn": [2, 4, 1, 10, 0, 1, 0],
                             "al7ppbt": [0, 7, 1, 7, 0, 1, 0]
                             })
    return_df = exclusion_flags.all_alc_types_flag(input_df)

    expected = [0, 1, 0, 1, 0, 0, 0]
    actual = list(return_df["dflagallalctypes"].astype(int))

    assert actual == expected, f"When checking for flagallalctypes, expected to find {expected} but found {actual}"


def test_high_alc_daily_flag():
    """
    Tests flag for high daily alcohol units has been implemented correctly

    """

    input_df = pd.DataFrame({"dal7utmean": [10, 50, 12, 80, 0, 140, 49]})
    return_df = exclusion_flags.high_alc_daily_flag(input_df)

    expected = [0, 0, 0, 1, 0, 1, 0]
    actual = list(return_df["dflaghighdailyalc"].astype(int))

    assert actual == expected, f"When checking for flaghighdailyalc, expected to find {expected} but found {actual}"


def test_alc_outlier_flag():
    """
    Tests composite alcohol outlier flag has been implemented correctly

    """
    input_df = pd.DataFrame({"dflaghighalcquant": [0, 0, 1, 0, 0, 0, 1, 1, 1],
                             "dflaghighdailyalc": [0, 1, 0, 1, 0, 0, 0, 0, 1],
                             "dflagallalctypes": [0, 1, 1, 0, 0, 1, 0, 1, 0]
                             })
    return_df = exclusion_flags.alc_outlier_flag(input_df)

    expected = [0, 1, 1, 1, 0, 1, 1, 1, 1]
    actual = list(return_df["dflagalcoutlier"].astype(int))

    assert actual == expected, f"When checking for flagalcoutlier, expected to find {expected} but found {actual}"
