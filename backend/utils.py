from pathlib import Path
from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet
from collections.abc import Iterable
from typing import Any, Union
import pandas as pd
from tabulate import tabulate


def read_pandas(excel_file_path:str) -> str:
    # Read the Excel file
    xls = pd.ExcelFile(excel_file_path)
    result = ""
    # Iterate over each sheet and convert to markdown
    markdown_tables = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        markdown_table = tabulate(df, headers='keys', tablefmt='pipe', showindex=False)
        markdown_tables[sheet_name] = markdown_table

    # Print the markdown tables
    for sheet_name, markdown_table in markdown_tables.items():
        result += f"### {sheet_name}\n"
        result += markdown_table
        result += "\n"
    return result
