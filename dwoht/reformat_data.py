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
        if df[col].dtype is np.dtype('float') or df[col].dtype is np.dtype('float64'):
            print(f'column {col} is float, changing to str ...')
            df = df.astype({col: np.int64})
            df = df.astype({col: str})
        elif df[col].dtype is np.dtype('int') or df[col].dtype is np.dtype('int64'):
            print(f'column {col} is int, changing to str ...')
            df = df.astype({col: str})
        elif df[col].dtype is np.dtype('O'):
            print(f'column {col} is already str')
        else:
            raise ValueError(f'Not able to handle {df[col].dtype} type')

    return df


def col_to_float(df: pd.DataFrame, col_list: List[str]) -> pd.DataFrame:
    """
    transform int / str column to float

    :param df: dataframe to be transformed
    :param col_list: list of columns to be transformed
    :return: transformed dataframe
    """

    for col in col_list:
        if df[col].dtype is np.dtype('float') or df[col].dtype is np.dtype('float64'):
            print(f'column {col} is already float')
        elif df[col].dtype is np.dtype('int') or df[col].dtype is np.dtype('int64'):
            print(f'column {col} is int, changing to str ...')
            df = df.astype({col: float})
        elif df[col].dtype is np.dtype('O'):
            print(f'column {col} is str, changing to float ...')
            df = df.astype({col: float})
        else:
            raise ValueError(f'Not able to handle {df[col].dtype} type')

    return df
