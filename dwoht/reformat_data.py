# -- coding: utf-8 --

from typing import List

import numpy as np
import pandas as pd


def col_to_str(df: pd.DataFrame, col_list: List[str]) -> pd.DataFrame:
    """
    transform int / float column to str

    :param df: dataframe to be transformed
    :param col_list: list of columns to be transformed
    :return: transformed dataframe
    """

    for col in col_list:
        col_dtype = df[col].dtype

        if pd.api.types.is_float_dtype(col_dtype):
            try:
                df = df.astype({col: np.int64})
                df = df.astype({col: str})
            except ValueError:
                raise ValueError(f"Cannot convert column '{col}' to str due to invalid data.")
        elif pd.api.types.is_integer_dtype(col_dtype):
            df = df.astype({col: str})
        elif pd.api.types.is_object_dtype(col_dtype):
            continue
        else:
            raise ValueError(f"Not able to handle dtype '{col_dtype}' for column '{col}'")

    return df


def col_to_float(df: pd.DataFrame, col_list: List[str]) -> pd.DataFrame:
    """
    transform int / str column to float

    :param df: dataframe to be transformed
    :param col_list: list of columns to be transformed
    :return: transformed dataframe
    """

    for col in col_list:
        col_dtype = df[col].dtype

        if pd.api.types.is_float_dtype(col_dtype):
            continue  # Already float, no conversion needed
        elif pd.api.types.is_integer_dtype(col_dtype):
            df[col] = df[col].astype(float)
        elif pd.api.types.is_object_dtype(col_dtype):
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                raise ValueError(f"Cannot convert column '{col}' to float due to invalid data.")
        else:
            raise ValueError(f"Not able to handle dtype '{col_dtype}' for column '{col}'")

    return df
