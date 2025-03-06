import logging
import time
import timeit

import pandas as pd
import numpy as np
import xlwings as xw

import sdd_code.utilities.parameters as param
from sdd_code.utilities.data_import import import_sav_values
from sdd_code.utilities import publication
from sdd_code.utilities.field_definitions import derivations, exclusion_flags
from sdd_code.utilities.processing import processing_exclusions, processing
from sdd_code.utilities import chapters
from sdd_code.utilities import difference
from sdd_code.utilities import logger_config
from tests.run_import_validation import run_all_import_tests
from tests.run_unittests import run_all_unit_tests


def main():
    """
    Main function used to run the pipeline.

    Runs each element of the pipeline as determined by the run parameters in
    parameters.py

    """
    # --- Run required import and unit tests ---

    # Check that input tests are passing, set flag in params to skip
    run_all_import_tests(
        pupil=param.RUN_PUPIL_INPUT_TESTS,
        teacher=param.RUN_TEACHER_INPUT_TESTS)

    # Check that unit tests are passing, set flag in params to skip
    # Currently runs the derivation and processing unit tests only
    run_all_unit_tests(
        derivations=param.RUN_DERIVATION_UNIT_TESTS,
        processing=param.RUN_PROCESSING_UNIT_TESTS)

    # --- Import the data ---

    # Execute the import data function on the pupil file
    df = import_sav_values(file_path=param.PUPIL_DATA_PATH, drop_col=param.DROP_COLUMNS)

    # Execute import data function on teacher file
    df_teacher = import_sav_values(file_path=param.TEACHER_DATA_PATH, drop_col=[])
    # Add a dummy pupil weight field (=1) so that the school data can be processed
    # using the same functions as the pupil data.
    df_teacher[param.WEIGHTING_VAR] = 1

    # Temp function added for 2023 to drop extra prefixes added to some column names in
    # teacher dataset
    df_teacher = processing.teacher_drop_lesson_prefix(df_teacher)

    # Removing volunteer schools from teacher data
    df_teacher_filt = processing_exclusions.filter_schools(df_teacher)

    # --- Add the derivations and exclusion flag columns ---

    # Add derived variables from the derivations module,
    # based on the list in all_derivations
    all_derivations = derivations.get_derivations()

    for derivation in all_derivations:
        logging.info(f"Creating derivation {derivation.__name__}")
        df = derivation(df)

    # Add flags used later to filter out exclusions, as set in parameters.py
    all_flags = exclusion_flags.get_flags()
    for flag in all_flags:
        logging.info(f"Creating exclusion flag {flag.__name__}")
        df = flag(df)

    # --- Create a filtered version of the data (used for publication outputs) ---

    # Apply school, dummy drug and outlier filters
    df_filt = processing_exclusions.apply_exclusions(df)

    # --- Write unfiltered data to external file ---

    # Write the final pupil and teacher data to csv
    # Flag to skip can be set in parameters
    if param.WRITE_ASSET is True:
        publication.write_csv(df_filt, "pupildata")
        publication.write_csv(df_teacher_filt, "teacherdata")

    # --- Create and write the publication outputs using the filtered data ---

    # Prepare the sheet content for each chapter, based on the list in all_chapters
    all_chapters = chapters.get_chapters()

    # Open Excel application
    xw.App()

    for chapter in all_chapters:
        # Skip this chapter if CHAPTER_ALL is False or this chapter param is False.
        if not (param.CHAPTER_ALL | chapter["run_chapter"]):
            continue
        output_path = chapter["output_path"]
        table_path = chapter["table_path"]
        chapter_number = chapter["chapter_number"]
        logging.info(f"Writing tables to {output_path}")

        # Open workbook in existing Excel application
        wb = xw.books.open(output_path)

        # Populate the sheets
        for sheet in chapter["sheets"]:
            # Write the output datasets to the relevant tabs
            logging.info(f"Writing output to {sheet['name']}")

            sht = wb.sheets[sheet["name"]]
            sht.select()
            sht.clear_contents()
            # Check if the Sheet has a key called teacher_table, if it
            # does and the value is True then use teacher data. If it does
            # but the value is False then use pupil, if it has no key
            # then also use pupil
            if sheet.get("teacher_table", False):
                content_df = pd.concat([table(df_teacher_filt) for table in
                                        sheet["content"]])
            else:
                content_df = pd.concat([table(df_filt) for table in sheet["content"]])

            # Find the same table in the previous year (if it exists) and attempt to
            # compare the percentage column
            # If they don't exist or can't be matched then the diff cols will be NAN
            if param.CHECK_PREV_YEAR:
                source_prev = difference.get_source_data(output_path)

                content_df = difference.get_prev_year_diff(
                    content_df,
                    table_name=sheet["name"],
                    prev_source_data=source_prev,
                    col_to_check="Percentage",
                    diff_tol=param.BREACH_LEVEL)
            else:
                content_df["PrevYearDiff"] = np.nan
                content_df["DiffFlag"] = np.nan

            sht.range("A1").options(pd.DataFrame, index=False).value = content_df

        # Save and close output workbook
        logging.info(f"Finished writing to {output_path} and saving")
        wb.save(output_path)
        wb.close()

        # Save the chapter publication outputs (if parameter set to true)
        if param.RUN_PUBLICATION_OUTPUTS is True:
            publication.save_tables(table_path, chapter_number)

    # Create final CI tables if the all chapter parameter, the publication
    # output parameter and the create SE parameter are all set to True
    if (param.RUN_PUBLICATION_OUTPUTS and param.CREATE_SE and param.CHAPTER_ALL):

        # Get output details for update of CI tables
        ci_chapters = chapters.get_ci_chapters()

        for chapter in ci_chapters:
            table_path = chapter["table_path"]
            chapter_number = chapter["chapter_number"]

            # Save tables
            publication.save_tables(table_path, chapter_number)

    # Close Excel application if still open
    if xw.apps.active is not None:
        xw.apps.active.api.Quit()

    # If all the CHAPTER parameters are set to False then add a warning to the log
    chapters_skipped = sum(not chapter["run_chapter"] for chapter in all_chapters)
    if not param.CHAPTER_ALL and chapters_skipped == len(all_chapters):
        logging.info("No outputs written as all CHAPTER parameters are set to False")


if __name__ == "__main__":
    # Setup logging
    formatted_time = time.strftime("%Y%m%d-%H%M%S")
    logger = logger_config.setup_logger(
        # Setup file & path for log, as_posix returns the path as a string
        file_name=(
            param.OUTPUT_DIR / "Logs" / f"sdd_create_pub_{formatted_time}.log"
        ).as_posix())

    start_time = timeit.default_timer()
    main()
    total_time = timeit.default_timer() - start_time
    logging.info(
        f"Running time of create_publication: {int(total_time / 60)} minutes and {round(total_time%60)} seconds.")
    logger_config.clean_up_handlers(logger)
