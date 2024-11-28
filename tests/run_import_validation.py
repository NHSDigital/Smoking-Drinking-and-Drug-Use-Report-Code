"""Main file for running the IPSOS import data tests

Includes command line arguments for running the pytest data validation tests. Creates
a html report of the output. For more information on the tests, see
the README in /datatests
"""
import io
import logging
import time
from contextlib import redirect_stdout
from pathlib import Path

import pytest

import sdd_code.utilities.parameters as param


def run_all_import_tests(
    pupil: bool = param.RUN_PUPIL_INPUT_TESTS,
    teacher: bool = param.RUN_TEACHER_INPUT_TESTS
):
    """Groups all import tests to be ran together

    Parameters
    ----------
        pupil: bool
            Whether to run the pupil data tests
        teacher: bool
            Whether to run the teacher data tests

    Returns
    -------
        None

    Raises
    ------
        RuntimeError: If tests are not passing (i.e. non-zero return code)
    """
    pupil_report = param.REPORT_DIR / "input_pupil_report"
    teacher_report = param.REPORT_DIR / "input_teacher_report"
    if pupil:
        logging.info("Running pupil input tests")
        rcp = run_import_tests(
            param.LOCAL_ROOT / "tests" / "datatests" / "test_ipsos_raw_pupil_input.py",
            report_loc=pupil_report,
            file_loc=param.PUPIL_DATA_PATH,
            meta_loc=param.PUPIL_META_DIR
        )
    else:
        rcp = 0
        logging.info("Skipping pupil input tests")

    if teacher:
        logging.info("Running teacher input tests")
        rct = run_import_tests(
            param.LOCAL_ROOT / "tests" / "datatests" / "test_ipsos_raw_teacher_input.py",
            report_loc=teacher_report,
            file_loc=param.TEACHER_DATA_PATH,
            meta_loc=param.TEACHER_META_DIR
        )
    else:
        rct = 0
        logging.info("Skipping teacher input tests")

    if rcp != 0 & rct != 0:
        raise RuntimeError(
            "All input tests failing, check latest output reports: "
            f"{pupil_report}, {teacher_report}"
        )
    elif rcp != 0:
        raise RuntimeError(
            f"Pupil tests failing, check latest output report: {pupil_report}"
        )
    elif rct != 0:
        raise RuntimeError(
            f"Teacher tests failing, check latest output report: {teacher_report}"
        )
    else:
        logging.info("Tests passing")


def run_import_tests(
    test_loc: Path,
    report_loc: Path,
    file_loc: Path,
    meta_loc: Path,
) -> None:
    """Run the set of import tests

    Parameters
    ----------
        test_loc: Test file/folder to run
        report_loc: Where to store the test report
        file_loc: Where the data to test is located
        meta_loc: Where the metadata to test against is located.

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
        # Which file to run them on:
        f"--sdd_file={file_loc}",
        # What metadata to verify against:
        f"--sdd_metadata={meta_loc}",
        # Where to save the report:
        f"--html={report_loc}",
        "--self-contained-html"
    ]

    # Redirect stdout to unused string to avoid errors in logging, handle invalid
    f = io.StringIO()
    with redirect_stdout(f):
        rc = pytest.main(input_test_arguments)

    return rc



if __name__ == "__main__":
    # Run tests
    run_all_import_tests(pupil=True, teacher=True)
