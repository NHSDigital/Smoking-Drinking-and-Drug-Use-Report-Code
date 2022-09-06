import logging
import time
import timeit

import pandas as pd
import numpy as np
import xlwings as xw

import sdd_code.utilities.parameters as param
from sdd_code.utilities.data_import import import_sav_values
from sdd_code.utilities import publication
from sdd_code.utilities import derivations
from sdd_code.utilities import chapters
from sdd_code.utilities import difference
from sdd_code.utilities import logger_config
from tests.run_import_validation import run_all_import_tests
from tests.run_unittests import run_all_unit_tests


def main():
    # Check that input tests are passing, set flag in params to skip
    run_all_import_tests(
        pupil=param.RUN_PUPIL_INPUT_TESTS,
        teacher=param.RUN_TEACHER_INPUT_TESTS)

    # Check that unit are passing, set flag in params to skip
    # Currently runs the derivation and processing unit tests only
    run_all_unit_tests(
        derivations=param.RUN_DERIVATION_UNIT_TESTS,
        processing=param.RUN_PROCESSING_UNIT_TESTS)

    # Execute the import data function on the pupil file
    # this returns the filed values not labels
    df = import_sav_values(file_path=param.PUPIL_DATA_PATH, drop_col=param.DROP_COLUMNS)

    # TEMP as imd_quin should have been named imdquin in 2018 dataset (renamed in SAS)
    if 'imd_quin' in df.columns:
        df.rename(columns={'imd_quin': 'imdquin'}, inplace=True)

    # Execute import data function on teacher file
    df_teacher = import_sav_values(file_path=param.TEACHER_DATA_PATH, drop_col=[])
    # Add a dummy pupil weight field (=1) so that the school data can be processed
    # using the same functions as the pupil data.
    df_teacher[param.WEIGHTING_VAR] = 1
    # Add the STRATA for each school to the teacher dataset, merging
    # on param.PSU, the archschn. This enables accurate standard errors and
    # CIs to be produced based on the survey design.
    df_teacher = pd.merge(
        df_teacher,
        df[[param.STRATA, param.PSU]],
        on=param.PSU,
        how="left")

    # This removes the 2nd version of the duplicate school records that
    # were in the 2018 dataset
    # TODO Remove after 2018 testing complete as these will not be allowed
    # in future dataset
    df_teacher = df_teacher.drop_duplicates(subset=["archschn"])

    # Add derived variables from the derivations module,
    # based on the list in all_derivations
    all_derivations = derivations.get_derivations()

    for derivation in all_derivations:
        logging.info(f"Creating derivation {derivation.__name__}")
        df = derivation(df)

    # Write the final pupil and teacher data to csv
    # Flag to skip can be set in parameters
    if param.WRITE_ASSET is True:
        publication.write_csv(df, "pupildata")
        publication.write_csv(df_teacher, "teacherdata")

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
                content_df = pd.concat([table(df_teacher) for table in sheet["content"]])
            else:
                content_df = pd.concat([table(df) for table in sheet["content"]])

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

            logging.debug(f"Output dataframe of size {content_df.shape}")

        # Save and close output workbook
        logging.info(f"Finished writing to {output_path} and saving")
        wb.save(output_path)
        wb.close()

        # save the chapter publication outputs (if parameter set to true)
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


# Note: Excel source data file should be closed before running the code below
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
