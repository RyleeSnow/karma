# -- coding: utf-8 --

import concurrent.futures
import datetime
import os
import sys
import time
from collections import Union, namedtuple
from datetime import timedelta
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
import yaml


def yellow_print(text: str) -> None:
    """Print text in bold yellow"""
    print(f"\n\033[1;33m{text}\033[0m\n")


def yaml_to_object(yaml_file: str, yaml_folder: str = None, to_object: bool = True):
    """
    read yaml config file to a dict

    :param yaml_file: yaml file name
    :param yaml_folder: yaml file folder
    :param to_object: whether to transform it to a Python object
    :return: a namedtuple
    """

    if Path(yaml_file).is_file():
        input_path = Path(yaml_file)
    else:
        if yaml_folder:
            yaml_folder = Path(yaml_folder)
            input_path = yaml_folder.joinpath(yaml_file)
        else:
            raise ValueError('Invalid yaml folder')

    with open(input_path, encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if to_object:
        data = namedtuple("ObjectName", data.keys())(*data.values())

    return data


def check_path(path: Union[str, Path]) -> None:
    """Check the path and create it if not exist"""
    # Ensure path is a Path object
    path = Path(path)

    # Check if directory exists, if not, create it
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"An error occurred while creating the directory: {e}")


def dataframe_mp(dataframe: pd.DataFrame, func: Callable, mp_cpus: int = None) -> pd.DataFrame:
    """
    do multiprocessing on a dataframe

    :param dataframe: input dataframe
    :param func: function to apply to the dataframe
    :param mp_cpus: number of cpus to use
    :return: output dataframe
    """

    mp_cpus = mp_cpus if mp_cpus > 0 else os.cpu_count()

    split_input_dataset = np.array_split(dataframe, mp_cpus)

    with concurrent.futures.ProcessPoolExecutor(max_workers=mp_cpus) as executor:
        results = list(executor.map(func, split_input_dataset))

    output_dataset = pd.concat(results, ignore_index=True)

    return output_dataset


def get_sunday(date, input_format="%Y%m%d", output_format="%Y%m%d"):
    """
    get the sunday of the week of the input date

    :param date: input date
    :param input_format: input date format, default is yyyymmdd
    :param output_format: output date format (sunday), default is yyyymmdd
    :return: sunday of the week of the input date
    """

    duty_date = datetime.datetime.strptime(str(date), input_format)
    sunday = duty_date

    one_day = datetime.timedelta(days=1)

    while sunday.weekday() != 6:
        sunday += one_day

    return datetime.datetime.strftime(sunday, output_format)


def lambda_groupby(lambda_func, groupby_df: pd.DataFrame, groupby_cols: list, result_col: str, reformat: bool = False):
    """
    apply lambda function to a groupby dataframe

    :param lambda_func: lambda function, e.g. lambda x: (x['daily_price'] * x['daily_unit']).sum() / x['daily_unit'].sum()
    :param groupby_df: input groupby dataframe
    :param groupby_cols: columns to groupby
    :param result_col: result column name
    :return: output dataframe
    """

    df_temp = groupby_df.groupby(groupby_cols).apply(lambda_func)
    df_temp = df_temp.to_dict()

    temp_lst = []

    for key, value in df_temp.items():
        a = key[0]
        b = key[1]
        c = value
        temp_lst.append([a, b, c])

    new_col_lst = groupby_cols + [result_col]
    df_temp = pd.DataFrame(data=np.array(temp_lst), columns=new_col_lst)

    if reformat == "float":
        df_temp[result_col] = df_temp[result_col].astype(float)
    elif reformat == "int":
        df_temp[result_col] = df_temp[result_col].astype(int)
    else:
        pass

    return df_temp


def calculate_r2_value(input_df: pd.DataFrame, true_col: str, predict_col: str, mean_col: str) -> float:
    """
    calculate R2 value

    :param input_df: input dataframe
    :param true_col: the column name of true value
    :param predict_col: the column name of predicted value
    :param mean_col: the column name of mean value
    :return: R2 value
    """

    check = input_df.copy()

    check["a"] = check[true_col] - check[predict_col]
    check["a"] = check["a"].map(lambda x: x * x)
    check["b"] = check[true_col] - check[mean_col]
    check["b"] = check["b"].map(lambda x: x * x)

    R2_VALUE = 1 - check["a"].sum() / check["b"].sum()

    return R2_VALUE


def get_time_dif(start_time: time.time):
    """Get the time difference between now and the start time"""

    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


def list_intersection(a: list, b: list) -> list:
    """Return the intersection of two lists"""

    return list(set(a).intersection(set(b)))


def list_diff(a: list, b: list) -> list:
    """Return the difference of two lists"""

    return list(set(a).difference(set(b)))


def list_sym_diff(a: list, b: list) -> list:
    """Return the symmetric difference of two lists, in a or in b but not in both"""
    return list(set(a) ^ set(b))


def list_union(a: list, b: list) -> list:
    """Return the union of two lists"""
    return list(set(a).union(set(b)))


def set_intersection(a: set, b: set) -> set:
    """Return the intersection of two sets"""
    return a & b


def set_diff(a: set, b: set) -> set:
    """Return the difference of two sets, in a not in b"""
    return a - b


def set_sym_diff(a: set, b: set) -> set:
    """Return the symmetric difference of two sets, in a or in b but not in both"""
    return a ^ b


def set_union(a: set, b: set) -> set:
    """Return the union of two sets"""
    return a | b


def add_sys_path(wrkdir: list):
    """Add the working directory to sys.path"""
    for w in wrkdir:
        if w not in sys.path:
            sys.path.append(w)


def count_words_in_list(lst, output_format: 'str' = 'dataframe'):
    """
    count the frequency of words in a list

    :param lst: input list
    :param output_format: output format, either dict or dataframe
    :return: a dict or a dataframe
    """

    counts = {}

    for i in lst:
        if len(i) > 1:
            counts[i] = counts.get(i, 0) + 1

    if output_format == 'dict':
        return counts
    elif output_format == 'dataframe':
        df_counts = pd.DataFrame.from_dict(counts, orient='index', columns=['count'])
        df_counts = counts.reset_index().rename(columns={'index': 'word'})
        return df_counts
    else:
        raise ValueError('output_format must be either dict or dataframe')
