import pandas as pd
import numpy as np
import pytest

from sdd_code.utilities import parameters as param
from sdd_code.utilities import difference


class DFEq():
    """Allow comparison of dataframes directly within pytest"""
    def __init__(self, df):
        self.df = df

    def __eq__(self, df2):
        return all(self.df == df2)


@pytest.fixture()
def source_data():
    
    param.PREVYEAR_DIR = param.LOCAL_ROOT / "tests" / "data"
    
    return difference.get_source_data(
        param.LOCAL_ROOT / "tests" / "data" / "test_source_1.xlsx"
    )


def test_get_source_data(source_data):
    expected_source = {
        "table_1": {
            "data": DFEq(pd.DataFrame({
                "breakdown_col": ["break_1_break2", "break_1_break2", "break_1_break2"],
                "break_1": [1, 2, 3],
                "break2": [3, 4, 5],
                "base": [10, 40, 60],
                "check": [20, 20, 20],
            })),
        },
        "table_2": {
            "data": DFEq(pd.DataFrame({
                "breakdown_col": ["break_1_break2", "break_1_break2", "break_1_break2"],
                "break_1": [1, 2, 3],
                "break2": [3, 4, 5],
                "base": [10, 40, 60],
                "check": [40, 40, '"u"'],
            })),
        },
        "table_3": {
            "data": DFEq(pd.DataFrame({
                "breakdown_col": ["break1_break2", "break1_break2", "break1_break2"],
                "break1": [1, 2, 3],
                "break2": [3, 4, 5],
                "base": [60, 40, 10],
                "check": [20, 20, "[20]"],
            })),
        }
    }

    actual_source = {}
    for name, inner_d in source_data.items():
        new_inner = {
            "data": DFEq(inner_d["data"])
        }
        actual_source[name] = new_inner

    assert actual_source == expected_source


class TestPrevYearDiff:

    def test_basic(self, source_data):
        new_table_1 = pd.DataFrame({
            "breakdown_col": ["break_1_break2", "break_1_break2", "break_1_break2"],
            "break_1": [1, 2, 3],
            "break2": [3, 4, 5],
            "base": [10, 40, 60],
            "check": [10, 23, 50],
        })

        expected_diff = pd.DataFrame({
            "breakdown_col": ["break_1_break2", "break_1_break2", "break_1_break2"],
            "break_1": [1, 2, 3],
            "break2": [3, 4, 5],
            "base": [10, 40, 60],
            "check": [10, 23, 50],
            "PrevYearDiff": [np.nan, 3, 30],
            "DiffFlag": [0, 0, 1]
        }).astype({"DiffFlag": np.int32})

        actual_diff = difference.get_prev_year_diff(
            new_table_1,
            "table_1",
            source_data,
            "check",
            "base",
            30,
            5,
            "breakdown_col"
        )

        pd.testing.assert_frame_equal(actual_diff, expected_diff)

    def test_suppressed(self, source_data):
        new_table_2 = pd.DataFrame({
            "breakdown_col": ["break_1_break2", "break_1_break2", "break_1_break2"],
            "break_1": [1, 2, 3],
            "break2": [3, 4, 5],
            "base": [10, 40, 60],
            "check": [10, 50, "u"],
        })

        expected_diff = pd.DataFrame({
            "breakdown_col": ["break_1_break2", "break_1_break2", "break_1_break2"],
            "break_1": [1, 2, 3],
            "break2": [3, 4, 5],
            "base": [10, 40, 60],
            "check": [10, 50, "u"],
            "PrevYearDiff": [np.nan, 10, np.nan],
            "DiffFlag": [0, 1, 0]
        }).astype({"DiffFlag": np.int32})

        actual_diff = difference.get_prev_year_diff(
            new_table_2,
            "table_2",
            source_data,
            "check",
            "base",
            30,
            5,
            "breakdown_col"
        )

        pd.testing.assert_frame_equal(actual_diff, expected_diff)

    def test_rounded(self, source_data):
        new_table_3 = pd.DataFrame({
            "breakdown_col": ["break1_break2", "break1_break2", "break1_break2"],
            "break1": [1, 2, 3],
            "break2": [3, 4, 5],
            "base": [60, 40, 31],
            "check": [10, 25, "[35]"],
        })

        expected_diff = pd.DataFrame({
            "breakdown_col": ["break1_break2", "break1_break2", "break1_break2"],
            "break1": [1, 2, 3],
            "break2": [3, 4, 5],
            "base": [60, 40, 31],
            "check": [10, 25, "[35]"],
            "PrevYearDiff": [-10, 5, 15],
            "DiffFlag": [1, 0, 1]
        }).astype({"DiffFlag": np.int32})

        actual_diff = difference.get_prev_year_diff(
            new_table_3,
            "table_3",
            source_data,
            "check",
            "base",
            30,
            5,
            "breakdown_col"
        )

        pd.testing.assert_frame_equal(actual_diff, expected_diff)


def test_get_breakdown_cols():
    input_df = pd.DataFrame({
        "breakdown_col": ["col2_col_3_col1", "col2_col_3_col1"],
        "col1": [1, 2],
        "col2": [3, 4],
        "col_3": [5, 6],
        "other_col": [7, 8]
    })

    expected = ["col2", "col1", "col_3"]

    actual = difference.get_breakdown_cols(input_df, "breakdown_col")

    assert actual == expected