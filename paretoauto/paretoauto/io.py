# csv/excel loading and linking indices back to original rows

import numpy as np
import pandas as pd


def load_csv(filepath, objective_columns=None):
    # load csv file & return points array with source info for data linking
    df = pd.read_csv(filepath)

    if objective_columns is None:
        # get all numeric columns
        numeric_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        objective_columns = numeric_cols

    points = df[objective_columns].to_numpy()

    source_info = {
        "filepath": filepath,
        "columns": objective_columns,
        "dataframe": df,
    }

    return points, source_info


def load_excel(filepath, sheet_name=0, objective_columns=None):
    # load excel file & return points array with source info for data linking
    df = pd.read_excel(filepath, sheet_name=sheet_name)

    if objective_columns is None:
        numeric_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        objective_columns = numeric_cols

    points = df[objective_columns].to_numpy()

    source_info = {
        "filepath": filepath,
        "sheet": sheet_name,
        "columns": objective_columns,
        "dataframe": df,
    }

    return points, source_info


def get_source_rows(indices, source_info):
    # get original dataframe rows for given point indices
    df = source_info["dataframe"]
    return df.iloc[indices].copy()


def save_with_fronts(source_info, ranks, fronts, output_filepath):
    # save data with pareto_front column added so you can filter in excel
    df = source_info["dataframe"].copy()
    df["Pareto_Front"] = ranks

    # check extension to decide csv or excel
    if output_filepath.endswith('.xlsx') or output_filepath.endswith('.xls'):
        df.to_excel(output_filepath, index=False)
    else:
        df.to_csv(output_filepath, index=False)

    return df


def print_row_references(indices, source_info, front_number=0):
    # prints which excel rows the pareto points are from
    # excel rows are 1-indexed and have header so add 2
    excel_rows = [idx + 2 for idx in indices]

    print(f"\nFront {front_number} corresponds to these rows in Excel/CSV:")
    print(f"  Row numbers: {', '.join(map(str, excel_rows))}")
    print(f"  (Row 1 is the header)")

    # show first column values for reference
    df = source_info["dataframe"]
    if len(df.columns) > 0 and hasattr(df.index, 'name'):
        first_col = df.columns[0]
    else:
        first_col = df.columns[0] if len(df.columns) > 0 else None

    if first_col:
        values = df.iloc[indices][first_col].tolist()
        print(f"  Items: {', '.join(map(str, values))}")