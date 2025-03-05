import logging
import time
import timeit

import pandas as pd
import xlwings as xw

from sdd_code.utilities.field_definitions import derivations, exclusion_flags
from sdd_code.utilities import logger_config
from sdd_code.utilities import parameters as param
from sdd_code.utilities.data_import import import_sav_values
from sdd_code.models import model_tables


def main():
    df = import_sav_values(file_path=param.PUPIL_DATA_PATH, drop_col=param.DROP_COLUMNS)

    # Add derived variables from the derivations module, based on the list
    # in all_derivations
    all_derivations = derivations.get_derivations()

    for derivation in all_derivations:
        logging.info(f"Creating derivation {derivation.__name__}")
        df = derivation(df)
    all_flags = exclusion_flags.get_flags()
    for flag in all_flags:
        logging.info(f"Creating exclusion flag {flag.__name__}")
        df = flag(df)

    # Treat all missing values the same for models
    df = df.replace([-7, -8, -1], -9)

    # Where to save models, and model functions
    output = model_tables.get_models()

    output_path = output["output_path"]
    logging.info(f"Writing tables to {output_path}")
    wb = xw.Book(output_path)

    # Populate the sheets
    for model in output["models"]:
        # Write the output datasets to the relevant tabs
        logging.info(f"Writing output for {model['name']}")

        # Calculate the actual model
        model_data = model["content"](df)

        # Each model creates several sheets of information
        for sheet in model["sheets"]:
            sheet_name = f"{model['name']}_{sheet}"

            logging.info(f"Writing output to {sheet_name}")

            sht = wb.sheets[sheet_name]
            sht.select()
            sht.clear_contents()
            content_df = model_data[sheet]
            sht.range("A1").options(pd.DataFrame, index=False).value = content_df

            logging.debug(f"Output dataframe of size {content_df.shape}")

    # Save and close workbook.
    logging.info(f"Finished writing to {output_path}, saving and exiting")
    wb.save(output_path)
    wb.app.quit()


if __name__ == "__main__":
    # Setup logging
    formatted_time = time.strftime("%Y%m%d-%H%M%S")
    logger = logger_config.setup_logger(
        # Setup file & path for log, as_posix returns the path as a string
        file_name=(
            param.OUTPUT_DIR / "Logs" / f"sdd_create_mod_{formatted_time}.log"
        ).as_posix())

    start_time = timeit.default_timer()
    main()
    total_time = timeit.default_timer() - start_time
    logging.info(
        f"Running time of create_models: {int(total_time / 60)} minutes and {round(total_time%60)} seconds.")
    logger_config.clean_up_handlers(logger)
