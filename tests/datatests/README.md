This file describes the design and usage of the input data tests for SDD. For an example of the process when testing a new file, skip to [Example Usage](#example-usage).

[[_TOC_]]

# What Are They For
These tests, defined in [test_ipsos_raw_input_pupil.py](test_ipsos_raw_input_pupil.py) and [test_ipsos_raw_input_teacher.py](test_ipsos_raw_input_teacher.py), confirm that a raw SPSS file (i.e. ending with the `.sav` extension) conforms to the properties defined in the SDD metadata 

# How Do They Work
The tests are written using pytest, a Python testing framework - see [here](https://github.com/NHSDigital/rap-community-of-practice/blob/main/docs/training_resources/python/unit-testing-field-definitions.md) for the NHSD RAP guide. Pytest tests are traditionally written to test code, but can be used to test any set of assumptions that you can define. These work by reading in the metadata files - see [Updating Metadata](#updating-metadata) for detailed info on each of the files - and using the information stored within to check the input `.sav` file.

The steps within each are very similar, and so for brevity this file will describe the steps in the Pupil test file.

The first step in [test_ipsos_raw_input_pupil.py](test_ipsos_raw_input_pupil.py) is to read in the SPSS `.sav` file specified, it does this using the `import_sav_values` function defined in [data_import.py](/sdd_code/utilities/data_import.py), dropping the columns specified in [parameters.py](/sdd_code/utilities/parameters.py), and attempting to coerce the data types to expected Pandas ones using `convert_sdd_dtypes` from [metadata.py](/sdd_code/utilities/metadata.py). Next the metadata is loaded, as a Python dictionary for each file. The metadata and SPSS file are read-in as session scoped pytest [fixtures](https://docs.pytest.org/en/6.2.x/fixture.html), to enable them to be parsed once and passed to the tests.

The results of these tests will be saved to a HTML report, in the location specified in `parameters.REPORT_DIR`.

Once all the data and metadata is loaded, the tests are ran:

## 1. test_input_attributes
This tests that the basic attributes of the data are as expected, these are:
- Number of rows
- Number of columns
- Names of columns
- Data types

## 2. test_discrete_values
This test is ran for each column, using [`@pytest.mark.parametrize`](https://docs.pytest.org/en/6.2.x/parametrize.html). If the column is referenced as a discrete column in metadata, then it checks that all of the values are in the set of allowed values as defined in metadata.

## 3. test_continuous_values
Similarly to `test_discrete_values`, this is ran for every column if it is defined as continuous in metadata. It then checks for a minimum/maximum value in the metadata, if none exist it will default to 0 and 500 respectively. It then checks that every value is either between the minimum and maximum, or is coded as unknown/missing/other (which are -9, -8, and -1).

## 4. test_pupilwt
This tests that the sum of the weighting column (`pupilwt`) is equal to the number of rows, and that each value is within the range [0.01, 10].

## 5. test_null_vals
This checks whether there are any null values in the dataframe.

## 6. test_unique_keys
This checks that the unique key column (`archsn`) is actually unique.  

# How Do I Use Them

These tests are run as part of the main pipeline. The input tests are ran before anything else to ensure that the data is as expected (if `RUN_PUPIL_INPUT_TESTS = True` and/or `RUN_TEACHER_INPUT_TESTS = True` in [parameters.py](/sdd_code/utilities/parameters.py)). They are ran using the `run_all_import_tests` function defined in [run_import_validation.py](../run_import_validation.py).

For instructions on how to run the main pipeline see the main README file for the project ([README.md](sdd_code/README.md)) 

# How Do I Update Them

When running these tests on a new SDD `.sav` file, the metadata and underlying tests may need to be updated.

## Updating Metadata

The metadata for each of the Pupil data and teacher data for SDD is stored in 2 files. These are:
- `sdd_metadata.json`

These are `.json` files, for our purposes they can be interpreted as a Python [dictionary](https://docs.python.org/3/tutorial/datastructures.html) - which are maps from "keys" to "values".


### sdd_metadata.json:
This file contains the relevant information about each column, e.g.:
```json
"ethnic": {
    "type": "discrete",
    "dtype": "int8",
    "values": [
        -9.0,
        -8.0,
        -1.0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
        11.0,
        12.0,
        13.0,
        14.0,
        15.0,
        16.0,
        17.0,
        18.0
    ]
},
```
This is used within the tests to check a number of things:

1. `"type"` is used to determine which tests to run, either `test_discrete_values` or `test_continuous_values` or neither if it is not a measure column.
2. `"dtype"` defines the pandas/numpy that each column should have, or be able to be converted to using `convert_sdd_dtypes`. When updating the metadata, use types as in the [numpy documentation](https://numpy.org/doc/stable/reference/arrays.dtypes.html), generally only `object`, `bool`, `string`, `float<n>`, `int<n>` or `category` should be needed (where `<n>` is a number from 8 to 64). The types that have been selected are the smallest that can safely store each column's values, to save memory.
3. `"values"` is the set of allowed values, used within each of the measure tests.

### Automatically Generating Metadata

The metadata that exists was not written by hand, it was generated by `create_pupil_metadata_from_sav` and equivalent teacher function in [metadata.py](/sdd_code/utilities/metadata.py). This function uses the metadata stored in a `.SAV` file to extract the files above. It contains a number of hardcoded references and assumptions, and is not intended for use a regular part of the pipeline. However, if for any reason the metadata needs to be created from scratch again this function can be used.

## Updating Tests
To add, remove, or change the tests that are ran, simply edit the main [test_ipsos_raw_input_pupil.py](test_ipsos_raw_input_pupil.py) file. Use the unit testing RAP guide and pytest documentation to add new features.

To alter the command line arguments used, modify [conftest.py](/conftest.py). This file defines hooks, helper functions, and fixtures that are shared across multiple test files. In this case, the `pytest_addoption` function is used to add new command line options for pytest, and `pytest_generate_tests` is used to pass these arguments to each test before it runs. That is how, in `test_ipsos_raw_input_pupil.py`, `sdd_all` can have `sdd_file` as an argument without it being defined in the file.

# Example Usage

As an example, here is the process that would be undergone when a new survey is completed, and the data is recieved from IPSOS:

1. A copy of the previous year's metadata is archived.
2. The [parameter](/sdd_code/utilities/parameters.py) `PUPIL_DATA_PATH` is updated to point to the new SPSS file.
3. The tests are ran, by executing [`run_import_validation.py`](../run_import_validation.py) with default settings.
4. The test report is checked for any issues in validation, for example:
```console
E       AssertionError: Unexpected values in cgbuyn, {3289: -56, 3532: -48, 7262: -48}
```
5. Either new data is requested, with unexpected values removed/replaced, or the metadata is updated to allow the new values.
6. The tests are ran again, until no errors occur.
