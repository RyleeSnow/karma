from __future__ import annotations

from collections import namedtuple
from pathlib import Path

import numpy as np

from .log import logger


def yaml_to_object(yaml_file, yaml_folder=None, to_object=True) -> namedtuple:
    """
    read yaml config file to a dict

    Args:
        yaml_file: yaml file name
        yaml_folder: yaml file folder
        to_object: whether to transform it to a Python object
    Returns:
        a namedtuple
    """

    if yaml_folder is None:
        yaml_folder = Path(__file__).parent.joinpath('config')
    else:
        yaml_folder = Path(yaml_folder)
    import yaml

    with open(yaml_folder.joinpath(yaml_file), encoding='utf-8') as file:
        data = yaml.safe_load(file)

    if to_object:
        data = namedtuple('ObjectName', data.keys())(*data.values())

    return data


def col_to_str(df, col_list):
    """
    transform int / float column to str

    Args:
        df: dataframe to be transformed
        col_list: list of columns to be transformed
    Returns:
        transformed dataframe
    """

    for col in col_list:
        if df[col].dtype is np.dtype('float') or df[col].dtype is np.dtype('float64'):
            logger.info(f'column {col} is float, changing to str ...')
            df = df.astype({col: np.int64})
            df = df.astype({col: str})
        elif df[col].dtype is np.dtype('int') or df[col].dtype is np.dtype('int64'):
            logger.info(f'column {col} is int, changing to str ...')
            df = df.astype({col: str})
        elif df[col].dtype is np.dtype('O'):
            logger.info(f'column {col} is already str')
        else:
            raise ValueError(f'Not able to handle {df[col].dtype} type')

    return df


def col_to_float(df, col_list):
    """
    transform int / str column to float

    Args:
        df: dataframe to be transformed
        col_list: list of columns to be transformed
    Returns:
        transformed dataframe
    """

    for col in col_list:
        if df[col].dtype is np.dtype('float') or df[col].dtype is np.dtype('float64'):
            logger.info(f'column {col} is already float')
        elif df[col].dtype is np.dtype('int') or df[col].dtype is np.dtype('int64'):
            logger.info(f'column {col} is int, changing to str ...')
            df = df.astype({col: float})
        elif df[col].dtype is np.dtype('O'):
            logger.info(f'column {col} is str, changing to float ...')
            df = df.astype({col: float})
        else:
            raise ValueError(f'Not able to handle {df[col].dtype} type')

    return df
