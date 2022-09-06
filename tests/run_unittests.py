"""Main file for running the unit tests

Includes command line arguments for running the pytest unit tests. Creates
a html report of the output.
"""
import io
import logging
import time
from contextlib import redirect_stdout
from pathlib import Path

import pytest

import sdd_code.utilities.parameters as param


def run_all_unit_tests(
    derivations: bool = param.RUN_DERIVATION_UNIT_TESTS,
    processing: bool = param.RUN_PROCESSING_UNIT_TESTS
):
    """Groups all unit tests to be ran together

    Parameters
    ----------
        derivations: bool
            Whether to run the derivaton unit tests
        processing: bool
            Whether to run the processing unit tests

    Returns
    -------
        None

    Raises
    ------
        RuntimeError: If tests are not passing (i.e. non-zero return code)
    """
    if derivations:
        logging.info("Running derivation unit tests")
        run_unit_tests(
            param.LOCAL_ROOT / "tests" / "unittests" / "test_derivations.py",
            report_loc=param.REPORT_DIR / "derivation_report",
        )
    else:
        logging.info("Skipping derivation unit tests")

    if processing:
        logging.info("Running processing unit tests")
        run_unit_tests(
            param.LOCAL_ROOT / "tests" / "unittests" / "test_processing.py",
            report_loc=param.REPORT_DIR / "processing_report",
        )
    else:
        logging.info("Skipping processing unit tests")


def run_unit_tests(
    test_loc: Path,
    report_loc: Path,
) -> None:
    """Run the set of unit tests

    Parameters
    ----------
        test_loc: test file/folder to run
        report_loc: where to store the test report

    Returns
    -------
        None

    Raises
    ------
        RuntimeError: If tests are not passing (i.e. non-zero return code)
    """
    run_time = time.strftime("%Y%m%d-%H%M%S")
    report_loc = f"{report_loc}_{run_time}.html"

    input_test_arguments = [
        # Which tests to run:
        str(test_loc),
        # Where to save the report:
        f"--html={report_loc}",
        "--self-contained-html",
    ]

    f = io.StringIO()
    with redirect_stdout(f):
        rc = pytest.main(input_test_arguments)

    if rc:
        raise RuntimeError(
            f"Unit tests failing, check latest output report: {report_loc}"
        )
    else:
        logging.info("Tests passing")


if __name__ == "__main__":
    # Run tests
    run_all_unit_tests(derivations=True, processing=False)
