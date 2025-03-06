import logging
import xlwings as xw
import re
from pathlib import Path

import sdd_code.utilities.parameters as param


def break_workbook_links(
    wb_path,
    macro_wb_path=param.LOCAL_ROOT / "sdd_code" / "VBA" / "SDDMacros.xlsm",
    macro_name="SDD.BreakExternalLinks",
):
    """Uses a VBA macro defined in a local file, defaults to SDDMacros.xlsm, to
    break all links in a specific notebook.

    Parameters
    ----------
        wb_path: Path
            Path to the workbook to break all links in
        macro_wb_path: Path
            Path to the macro enabled workbook containing the macro to run
        macro_name: str
            The macro to run, defaulting to SDD.BreakExternalLinks

    Returns
    -------
        None

    For reference, the SDD.BreakExternalLinks macro is below:

    Sub BreakExternalLinks(WorkbookPath As String)
    'PURPOSE: Breaks all external links that would show up in Excel's "Edit Links" Dialog Box
    'SOURCE: www.TheSpreadsheetGuru.com/the-code-vault

    Dim ExternalLinks As Variant
    Dim x As Long
    Dim WorkbookToBreakLinks As Workbook

    Application.ScreenUpdating = False

    Set WorkbookToBreakLinks = Workbooks.Open(WorkbookPath, UpdateLinks:=3)

    'Create an Array of all External Links stored in Workbook
    ExternalLinks = WorkbookToBreakLinks.LinkSources(Type:=xlLinkTypeExcelLinks)
    If IsEmpty(ExternalLinks) Then Exit Sub

    'Loop Through each External Link in ActiveWorkbook and Break it
    For x = 1 To UBound(ExternalLinks)
        WorkbookToBreakLinks.BreakLink Name:=ExternalLinks(x), Type:=xlLinkTypeExcelLinks
    Next x

    End Sub
    """
    mwb = xw.Book(macro_wb_path)
    BreakLinks = mwb.macro(macro_name)
    BreakLinks(Path(wb_path).resolve().as_posix())
    mwb.close()


def delete_in_range(sht, range):
    """Delete a range of data from a worksheet.

    Parameters
    ----------
        sht: xw.Sheet
        range: Iterable[str]
            A list or set of columns/rows
    """
    delete = f"{min(range)}:{max(range)}"
    sht.range(delete).delete()


def delete_worksheets(wb_path, sheets_to_delete=["Auto checks", "Auto Checks"]):
    """Delete a worksheet from an excel file. Will ignore if sheet not present

    Parameters
    ----------
        wb_path: Path
            Path to the workbook to check
        sheets_to_delete: list[str]
            Worksheets to be deleted from the saved publication tables
    """
    wb = xw.Book(wb_path)

    sheet_names = [sht.name for sht in wb.sheets]
    for sheet_name in sheets_to_delete:
        if sheet_name in sheet_names:
            sht = wb.sheets[sheet_name]
            sht.delete()


def remove_temp_cols_and_rows(
    wb_path, cols_to_check=["A", "B", "C"], rows_to_check=["1"]
):
    """Removes specified columns/rows from workbook.
    To do this it searches for temp flags applied in the Excel
    Excel file:
    Temp_Col: Will remove that column
    Temp_Row: Will removed that row
    Temp_Row_Col: Will removed both the row and the column
    The process is set to check columns A to C ,and row 1 for these flags, which is the
    extent of the current look up values. If lookup values are added to further
    columns then these will need adding to col_range and row_range

    Parameters
    ----------
        wb_path: Path
            Path to the workbook to check in
        cols_to_check: list[str]
            A list of columns to check for temp flags
        rows_to_check: list[str]
            A list of rows to check for temp flags
    """
    wb = xw.Book(wb_path)
    for sht in wb.sheets:
        sht.select()

        # Create empty sets for rows/cols to delete, to avoid duplication
        select_cols = set()
        select_rows = set()

        # Compile regex for matching values
        temp_expr = re.compile("temp", re.IGNORECASE)
        col_expr = re.compile("col", re.IGNORECASE)
        row_expr = re.compile("row", re.IGNORECASE)

        for col in cols_to_check:
            for row in rows_to_check:
                check = str(sht.range(col + row).value)

                # If find "temp" in the check...
                if re.search(temp_expr, check):
                    # If it's a row/col/both then add to the sets
                    if re.search(col_expr, check):
                        select_cols.add(col)
                    if re.search(row_expr, check):
                        select_rows.add(row)

        # If we've found rows/cols, then delete
        if select_cols:
            delete_in_range(sht, select_cols)
        if select_rows:
            delete_in_range(sht, select_rows)


def save_tables(table_path, chapter_number):
    """Updates and writes the specified master table to the publication
    folder.

    Parameters
    ----------
    tablepath : str
        filepath for the final file to be saved
    chapter_number: str
        Chapter number for the final filename

    Returns
    -------
    None
    """
    logging.info(
        f"Saving publication table for chapter: {chapter_number}"
    )

    # Open workbook in existing Excel application
    wb = xw.books.open(table_path, update_links=True)

    # save a copy to the final publication folder
    wb_name = "sdd_" + param.YEAR + "_tab" + chapter_number + ".xlsx"
    save_path = param.TAB_DIR / wb_name
    wb.save(save_path)

    # break all the links in the workbook
    break_workbook_links(save_path)

    # remove the temp cols and rows
    remove_temp_cols_and_rows(save_path)

    # delete the checking worksheets
    delete_worksheets(save_path)

    # return to the contents page and save and close the final file
    sht = wb.sheets["Contents"]
    sht.select()
    wb.save(save_path)
    wb.close()


def write_csv(df, df_type):
    """Updates and writes the specified dataframe to a csv

    Parameters
    ----------
    df : pandas.DataFrame
    df_type : str
        dataframe identifier to be used in the csv filename (e.g. pupildata)

    Returns
    -------
    csv file
    """
    logging.info(
        f"Writing {df_type} dataset to csv"
    )

    # Create the filename
    filename = "sdd_" + df_type + "_" + param.YEAR + ".csv"

    # Write to final csv
    df.to_csv(param.ASSET_DIR / filename, index=False)
