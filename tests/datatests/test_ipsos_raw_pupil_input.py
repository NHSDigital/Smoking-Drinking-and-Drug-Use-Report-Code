"""Data tests for SDD pupil raw input from IPSOS

These are pytest tests for a raw .SAV SPSS file, that check values based on
metadata.
To test a different .sav file or use different metadata, change the command line
arguments --sdd_file and --sdd_metadata.

These tests are written based on the 2018 SAV input file, using metadata from that
file. If there are substanstive changes to the format (for example responses are no
longer integer codes) then these tests may have to be rewritten.

For testing a new iteration of SDD, run the file run_import_validation with a new
sdd_file and sdd_metadata location (initally metadata will be copied from 2018).
Then iteratively update the metadata or request new data from IPSOS as issues are
found and either corrected, or the metadata is updated.
"""

import json
from pathlib import Path
import sys
from typing import Dict, List

import numpy as np
import pandas as pd
import pytest

import sdd_code.utilities.parameters as param
from sdd_code.utilities.data_import import import_sav_values


# sdd_file is set via command line arguments, defaults to None
# session scoping to cache dataframes, enable fast testing
@pytest.fixture(scope="session")
def sdd_all(sdd_file: str) -> pd.DataFrame:
    """Get main sdd output table and output to test"""
    return import_sav_values(sdd_file, param.DROP_COLUMNS)


# sdd_metadata is set via command line
@pytest.fixture(scope="session")
def sdd_dtypes(sdd_metadata: str) -> Dict[str, str]:
    """Get expected sdd attributes from metadata JSON"""
    with open(param.PUPIL_META_DIR  / "sdd_metadata.json", "r") as f:
        meta = json.load(f)
    dtype_map = {col: d["dtype"] for col, d in meta.items()}
    return dtype_map


@pytest.fixture(scope="session")
def sdd_allowed_values(sdd_metadata: str) -> Dict[str, List[float]]:
    """Get allowed values, dict map of col name to list"""
    with open(param.PUPIL_META_DIR  / "sdd_metadata.json", "r") as f:
        meta = json.load(f)
    value_map = {col: d["values"] for col, d in meta.items()}

    return value_map


@pytest.fixture(scope="session")
def sdd_meta(sdd_metadata: str) -> Dict[str, List[str]]:
    """Get all different column lists that could want to be tested

    This uses dtypes from metadata to separate columns, logic may change
    as metadata structure is determined
    """
    with open(param.PUPIL_META_DIR  / "sdd_metadata.json", "r") as f:
        meta = json.load(f)
    return meta


def test_null_vals(sdd_all: pd.DataFrame):
    msg = (
        f"{sdd_all.isnull().sum().sum()} null values found in dataframe, "
        f"in columns {list(sdd_all.columns[sdd_all.isnull().any()])}"
    )

    assert not sdd_all.drop('pupilwt', axis=1).isnull().values.any(), msg


def test_input_attributes(sdd_all: pd.DataFrame, sdd_dtypes: Dict[str, str]):
    """Does table have basic attributes as expected?

    Tests: No. rows, dtypes, column names
    """
    results = sdd_all
    exp_cols = sdd_dtypes.keys()
    # Convert string repr. of types to numpy.dtype for comparison
    exp_rows = param.NUM_PUPIL_ROWS  # Know exactly how many rows we should have

    # With specifically columns, want to show a more detailed view of what is in each
    cols_in_exp = set(exp_cols).difference(set(results.columns))
    cols_in_res = set(results.columns).difference(set(exp_cols))

    assert list(exp_cols) == list(results.columns), (
        f"Expected columns not found. \nOnly in expected: {cols_in_exp}"
        f"\nOnly in actual: {cols_in_res}"
    )
    assert exp_rows == results.shape[0], "Not expected number of rows"


# Currently cant pass fixtures as the list for parameterise
# TODO: Investigate pytest-lazy plugins plus similar
@pytest.mark.slow
# Parametrize loops over all columns
@pytest.mark.parametrize("column_index", list(range(0, 2000)))
def test_discrete_values(
    sdd_all: pd.DataFrame,
    sdd_meta: Dict[str, Dict],
    sdd_allowed_values: Dict[str, List[float]],
    column_index: int,
):
    """Do all discrete values fall within expected sets"""
    results = sdd_all

    # Use index list to get column name, can't pass exact list into
    # parametrize so use try/except
    try:
        column = list(sdd_allowed_values.keys())[column_index]
    except IndexError:
        return
    if sdd_meta[column]["type"] != "discrete":
        return

    # Remove NAs, as we have a separate check for them.
    col = results[column].dropna()

    # Discrete values are integer response codes that should all be within
    # the allowed list in metadata
    exp_values = sdd_allowed_values[column]
    values_in_list = col.isin(exp_values)
    assert all(
        values_in_list
    ), f"Unexpected value in {column}: {dict(col[~values_in_list])}"


@pytest.mark.slow
@pytest.mark.parametrize("column_index", list(range(0, 700)))
def test_continuous_values(
    sdd_all: pd.DataFrame,
    sdd_meta: Dict[str, List[str]],
    sdd_allowed_values: Dict[str, List[float]],
    column_index: int,
):
    """Do all continuous col values fall within expected range"""
    results = sdd_all
    try:
        column = list(sdd_allowed_values.keys())[column_index]
    except IndexError:
        return
    if sdd_meta[column]["type"] != "continuous":
        return

    # Remove NAs, as we have a separate check for them.
    col = results[column].dropna()

    # Check if column has a min/max mapping to use as a range
    values = sdd_allowed_values[column]
    min_max = [val for val in values if val >= 0]
    if min_max:
        max_val = max(min_max)
        min_val = min(min_max) if min(min_max) != max_val else 0
    else:
        min_val = 0
        max_val = 500

    # Continuous values are float responses (i.e. units drank) that should be
    # in this range, or are coded as negatives missiing/unknown/other
    values_in_range = col.between(min_val, max_val) | col.isin(
        [-9, -7, -8, -1]
    )

    assert all(
        values_in_range
    ), f"Unexpected values in {column}, {dict(col[~values_in_range])}"


def test_pupilwt(sdd_all: pd.DataFrame):
    """Do all weights lie in expected ranges and sum to appropriate values"""
    if 'pupilwt' in sdd_all.columns:
        assert (
            sdd_all["pupilwt"].dropna().between(0.01, 10).all()
        ), "Pupil weighting variable is not in range"

        assert sdd_all["pupilwt"].dropna().sum() == pytest.approx(
            sdd_all["pupilwt"].dropna().shape[0]
        ), "Pupil weighting does not sum to pupil count"

        assert (sdd_all.loc[sdd_all["volunsch"] != 1]["pupilwt"].isnull().values.any(),
               "Null pupil weight values present in sample data")


def test_unique_keys(sdd_all: pd.DataFrame):
    assert sdd_all["archsn"].is_unique, "ID column is not unique"
