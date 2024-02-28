import datetime
import multiprocessing
import time
from collections import namedtuple
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from pathos.multiprocessing import ProcessPool


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
        yaml_folder = Path(__file__).parent.joinpath("config")
    else:
        yaml_folder = Path(yaml_folder)
    import yaml

    with open(yaml_folder.joinpath(yaml_file), encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if to_object:
        data = namedtuple("ObjectName", data.keys())(*data.values())

    return data


def dataframe_mp(dataframe, func, mp_cores: int = None):
    """
    do multiprocessing on a dataframe

    :param dataframe: input dataframe
    :param func: function to apply to the dataframe
    :param mp_cores: number of cpus to use
    :return: output dataframe
    """

    if mp_cores is None:
        mp_cores = multiprocessing.cpu_count() - 1

    pool = ProcessPool(mp_cores)

    split_input_dataset = np.array_split(dataframe, mp_cores)

    output_dataset = pool.map(func, split_input_dataset)
    del [split_input_dataset]

    output_dataset = pd.concat(output_dataset, ignore_index=True)

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


def lambda_groupby(lambda_func, groupby_df, groupby_cols, result_col, reformat=False):
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


def calculate_r2_value(input_df, true_col, predict_col, mean_col):
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


def get_time_dif(start_time):
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))
