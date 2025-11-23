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