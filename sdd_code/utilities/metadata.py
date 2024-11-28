"""Utility functions for obtatining, applying, and saving metadata for SDD"""
import json
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
import pyreadstat

from .parameters import PUPIL_META_DIR, DROP_COLUMNS, AGE_COLUMNS


def dump_attrs(
    file_name: str,
    dump: dict,
    attr_path: Path,
) -> None:
    """Save a dictionary as a json in a specified location

    Args:
        file_name: THe name of the file
        dump: The dictionary to output
        attr_path: The path to save the file to

    Returns:
        None

    Raises:
        ValueError: If the file exists
    """
    file = attr_path / file_name
    if file.exists():
        raise ValueError("File already exists")

    with file.open("w") as f:
        json.dump(dump, f, indent=4)


def create_teacher_metadata_from_sav(
    sav_path: str,
    meta_path: Union[Path, str],
    drop_cols: list = DROP_COLUMNS,
) -> None:
    """Save the useful metadata from the input SDD .SAV file to a specified location.

    Creates the folder specified, and saves the dtypes,
    column types, and variable_values map as json files. If
    the folder already exists it will error, to avoid rewriting metadata.

    This function is what was used to create the initial metadata for use in the SDD
    process, because of the manual nature of that process it hard codes several values.
    This is not intended to be used as part of the regular process.

    Args:
        sav_path: Path to the SPSS file
        meta_path: Path to a folder to save metadata in
        drop_cols: Constant from parameters, columns to remove
        age_cols: Constant from parameters, columns that are ages

    Returns:
        None

    Raises:
        ValueError, if the metadata folder exists
    """
    _, metadata = pyreadstat.read_sav(str(sav_path))

    meta_path = Path(meta_path)  # convert in case str passed in

    # Never want to overwrite existing metadata
    if meta_path.exists():
        raise ValueError(
            "Path to save metadata in already exists, create a new folder to avoid "
            "overwriting existing metadata"
        )

    # Create the directory
    meta_path.mkdir()

    # Get lowercased columns
    column_list = [
        col.lower() for col in metadata.column_names if col.lower() not in drop_cols
    ]

    # Rough term for the columns that are extra info, not responses
    non_measures = [
        "archschn",
    ]
    # All measures are all vars that are responses on the survey
    all_measures = [col for col in column_list if col not in non_measures]

    # Construct 'allowed values' mapping from labels
    # Basic values come from metadata labels
    allowed_values = {
        col.lower(): list(value_map.keys())
        for col, value_map in metadata.variable_value_labels.items()
        if col.lower() not in drop_cols
    }
    # Remove disallowed values
    for col, values in allowed_values.items():
        if 8 in values and 7 not in values:
            values.remove(8)
        if 98 in values:
            values.remove(98)
        allowed_values[col] = values

    # Continuous cols are floats and can take any value
    continuous_cols = []
    for col in all_measures:
        values = allowed_values[col]
        # If all allowed values in map are less than 0, then
        # it only lists -9,-8,-1 for missing codes, so col is
        # continuous
        if all(val <= 0 for val in values):
            continuous_cols.append(col)
        # TODO: May add min/max values for continuous cols in the future, this would
        #       need to be added after this step.

    # Discrete (all cols that are left) are response codes
    discrete_cols = [col for col in all_measures if col not in continuous_cols]

    # Map SPSS variable types to pandas dtypes
    dtype_map = {"F8.2": "float16", "F8.0": "int8", "F2.0": "int8", "F3.0": "int8"}
    # Get dtypes from metadata, remap to pandas/np dtypes, clean columns
    dtypes = {
        col.lower(): dtype_map[dtype]
        for col, dtype in metadata.original_variable_types.items()
        if col.lower() not in drop_cols
    }

    meta = {}
    for col in column_list:
        if col in continuous_cols:
            col_type = "continuous"
        elif col in discrete_cols:
            col_type = "discrete"
        else:
            col_type = "non-measure"
        meta[col] = {
            "type": col_type,
            "dtype": dtypes[col],
            "values": allowed_values.get(col, "Any"),
        }

    # Save metadata from .SAV
    dump_attrs("sdd_metadata.json", meta, meta_path)


def create_pupil_metadata_from_sav(
    sav_path: str,
    meta_path: Union[Path, str],
    drop_cols: list = DROP_COLUMNS,
    age_cols: list = AGE_COLUMNS,
) -> None:
    """Save the useful metadata from the input SDD .SAV file to a specified location.

    Creates the folder specified, and saves the dtypes,
    column types, and variable_values map as json files. If
    the folder already exists it will error, to avoid rewriting metadata.

    This function is what was used to create the initial metadata for use in the SDD
    process, because of the manual nature of that process it hard codes several values.
    This is not intended to be used as part of the regular process.

    Args:
        sav_path: Path to the SPSS file
        meta_path: Path to a folder to save metadata in
        drop_cols: Constant from parameters, columns to remove
        age_cols: Constant from parameters, columns that are ages

    Returns:
        None

    Raises:
        ValueError, if the metadata folder exists
    """
    _, metadata = pyreadstat.read_sav(str(sav_path))

    meta_path = Path(meta_path)  # convert in case str passed in

    # Never want to overwrite existing metadata
    if meta_path.exists():
        raise ValueError(
            "Path to save metadata in already exists, create a new folder to avoid "
            "overwriting existing metadata"
        )

    # Create the directory
    meta_path.mkdir()

    # Get lowercased columns
    column_list = [
        col.lower() for col in metadata.column_names if col.lower() not in drop_cols
    ]

    # Rough term for the columns that are extra info, not responses
    non_measures = [
        "archsn",
        "archschn",
        "xmas",
        "version",
        "pupilwt",
        "region",
        "imd_quin",
    ]
    # All measures are all vars that are responses on the survey
    all_measures = [col for col in column_list if col not in non_measures]

    # Construct 'allowed values' mapping from labels
    # Basic values come from metadata labels
    allowed_values = {
        col.lower(): list(value_map.keys())
        for col, value_map in metadata.variable_value_labels.items()
        if col.lower() not in drop_cols
    }
    # Remove disallowed values
    for col, values in allowed_values.items():
        if 8 in values and 7 not in values:
            values.remove(8)
        if 98 in values:
            values.remove(98)
        allowed_values[col] = values

    # For age columns allow ages between 0 and 17
    # TODO: Should be more restrictive for all except base age?
    for col in age_cols:
        allowed_values[col] = allowed_values[col] + list(range(0, 18))

    # NEWFAS is uncoded? Add this manually:
    allowed_values["newfas"] = [0.0] + allowed_values["sddfas"]

    # imd_quin is uncoded:
    allowed_values["imd_quin"] = [-9.0, -8.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]

    # Add ranges for 'how X did you feel' style questions:
    range_qs = ["lifeanx", "lifehap", "lifesat", "lifewor"]
    for col in range_qs:
        allowed_values[col] = sorted(allowed_values[col] + list(range(1, 10)))

    # Continuous cols are floats and can take any value
    continuous_cols = []
    for col in all_measures:
        values = allowed_values[col]
        # If all allowed values in map are less than 0, then
        # it only lists -9,-8,-1 for missing codes, so col is
        # continuous
        if all(val <= 0 for val in values):
            continuous_cols.append(col)
        # TODO: May add min/max values for continuous cols in the future, this would
        #       need to be added after this step.

    # Discrete (all cols that are left) are response codes
    discrete_cols = [col for col in all_measures if col not in continuous_cols]
    # Manually add discrete non_measures for testing
    discrete_cols.extend(["xmas", "version", "region", "imd_quin"])

    # Map SPSS variable types to pandas dtypes
    dtype_map = {"F8.2": "float16", "F8.0": "int8", "F2.0": "int8", "F3.0": "int8"}
    # Get dtypes from metadata, remap to pandas/np dtypes, clean columns
    dtypes = {
        col.lower(): dtype_map[dtype]
        for col, dtype in metadata.original_variable_types.items()
        if col.lower() not in drop_cols
    }
    # Manually set archsn
    dtypes["archsn"] = "float32"

    meta = {}
    for col in column_list:
        if col in continuous_cols:
            col_type = "continuous"
        elif col in discrete_cols:
            col_type = "discrete"
        else:
            col_type = "non-measure"
        meta[col] = {
            "type": col_type,
            "dtype": dtypes[col],
            "values": allowed_values.get(col, "Any"),
        }

    # Save metadata from .SAV
    dump_attrs("sdd_metadata.json", meta, meta_path)
