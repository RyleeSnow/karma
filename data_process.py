from __future__ import annotations

import os
import time
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from tqdm.auto import tqdm

from .log import logger


def my_read_parquet(file_path, read_cols: list = None, **kwargs) -> pd.DataFrame:
    """
    customized function to read parquet

    Args:
        file_path: parquet file path
        read_cols: columns to read
    Returns:
        loaded pd.dataframe
    """

    parquet_file = pq.ParquetFile(file_path, **kwargs)
    dfs = [batch.to_pandas() for batch in tqdm(parquet_file.iter_batches(), disable=False, desc='Loading data')]
    df = pd.concat(dfs, ignore_index=True)

    if read_cols is None:
        pass
    else:
        df = df[read_cols]

    return df


def my_read_csv(file_path, set_cs: int = 500000, read_cols: list = None, special_sep: str = ',', **kwargs):
    """
    customized function to read csv

    Args:
        file_path: parquet file path
        set_cs: chunk size for read_csv
        read_cols: columns to read
        special_sep: special sep for .csv file
        loaded pd.dataframe
    Returns:
        loaded pd.dataframe
    """

    if 'nrows' in kwargs:
        df = pd.read_csv(file_path, usecols=read_cols, sep=special_sep, low_memory=False, **kwargs)

    else:
        try:
            rows = sum(1 for _ in open(file_path, 'r')) - 1
        except (Exception,):
            rows = 10000000

        chunk_list = []
        with tqdm(total=rows, desc='Loading data') as bar:
            if read_cols is None:
                for chunk in pd.read_csv(file_path, chunksize=set_cs, sep=special_sep, low_memory=False, **kwargs):
                    chunk_list.append(chunk)
                    bar.update(len(chunk))
            else:
                for chunk in pd.read_csv(file_path, chunksize=set_cs, usecols=read_cols, sep=special_sep, low_memory=False, **kwargs):
                    chunk_list.append(chunk)
                    bar.update(len(chunk))

        df = pd.concat((f for f in chunk_list), axis=0)
    return df


def my_read_data(
    file_name: str = None,
    data_folder: str | Path = None,
    sub_folder: str = None,
    csv_chunksize: int = 500000,
    reformat_cols: str = None,
    read_cols: list = None,
    rename_cols: dict = None,
    special_sep: str = ',',
    **kwargs,
) -> pd.DataFrame:
    """
    customized function to read a singe data file, supporting read_excel / read_csv / read_parquet

    Args:
        file_name: full file path including suffix
        data_folder: the main dir where the data is saved
        sub_folder: the sub folder name where the data is saved
        csv_chunksize: chunk size for read_csv, default is None
        reformat_cols: reformat column names to lower or upper characters, accept `lower` / `upper`, default is None
        read_cols: columns to read
        rename_cols: rename the columns
        special_sep: special sep for .csv file
    Returns:
        loaded pd.dataframe
    """

    if special_sep is None:
        special_sep = ','

    if data_folder is None:
        data_folder = Path(__file__).parents[1].joinpath('data')
    else:
        data_folder = Path(data_folder)

    if sub_folder is None:
        pass
    else:
        data_folder = data_folder.joinpath(sub_folder)

    file_path = data_folder.joinpath(file_name)

    logger.info(f'Reading {file_path}')
    start_time = time.time()

    file_suffix = file_name.split('.', 1)[1]

    if file_suffix in ['xlsx', 'xls']:
        df = pd.read_excel(file_path, usecols=read_cols, **kwargs)

    elif file_suffix == 'csv':
        df = my_read_csv(file_path=file_path, set_cs=csv_chunksize, read_cols=read_cols, special_sep=special_sep, **kwargs)

    elif file_suffix == 'txt':
        df = my_read_csv(file_path=file_path, **kwargs)

    elif file_suffix == 'gzip':
        df = my_read_parquet(file_path=file_path, read_cols=read_cols, **kwargs)

    elif 'csv.' in file_suffix:
        compression_type = file_suffix.split('.', 1)[1]

        if '.' in compression_type:
            raise ValueError(f'invalid file name {file_name}')
        else:
            if compression_type == 'gz':
                compression_type = 'gzip'
            else:
                pass

            df = my_read_csv(file_path=file_path, compression=compression_type, read_cols=read_cols, special_sep=special_sep, **kwargs)

    else:
        raise ValueError(f'invalid file name {file_name}')

    if rename_cols is None:
        pass
    else:
        df.rename(columns=rename_cols, inplace=True)

    if reformat_cols == 'upper':
        df.rename(columns=str.upper, inplace=True)
    elif reformat_cols == 'lower':
        df.rename(columns=str.lower, inplace=True)
    else:
        pass

    logger.info(
        f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, ' f'read {df.shape[0]} rows and columns are: {df.columns.to_list()}'
    )

    return df


def my_save_data(df: pd.DataFrame = None, data_folder: str | Path = None, sub_folder: str = None, file_name: str = None, **kwargs) -> None:
    """
    customized function to save a dataframe, supporting to_excel / to_csv / to_parquet

    Args:
        df: pd.dataframe to be saved
        data_folder: the main dir where the data is saved
        sub_folder: the sub folder name where the data is saved
        file_name: full file path including suffix
    Returns:
        loaded pd.dataframe
    """

    if data_folder is None:
        data_folder = Path(__file__).parents[1].joinpath('data')
    else:
        data_folder = Path(data_folder)

    if sub_folder is None:
        pass
    else:
        data_folder = data_folder.joinpath(sub_folder)

    if data_folder.is_dir():
        pass
    else:
        os.makedirs(data_folder)

    file_path = data_folder.joinpath(file_name)
    file_suffix = file_name.split('.', 1)[1]

    logger.info(f'Saving {file_path}')
    start_time = time.time()

    if 'index' in list(kwargs.keys()):
        pass
    else:
        kwargs['index'] = False

    if file_suffix in ['xlsx', 'xls']:
        df.to_excel(file_path, **kwargs)

    elif file_suffix == 'csv':
        df.to_csv(file_path, **kwargs)

    elif file_suffix == 'gzip':
        df.to_parquet(file_path, compression='gzip', **kwargs)

    elif 'csv.' in file_suffix:
        compression_type = file_suffix.split('.', 1)[1]

        if '.' in compression_type:
            raise ValueError(f'invalid file name {file_name}')
        else:
            df.to_csv(path_or_buf=file_path, compression=compression_type, **kwargs)

    else:
        raise ValueError(f'invalid file name {file_name}')

    logger.info(
        f'Time consumed: {round((time.time() - start_time), 2)} seconds, ' f'saved {df.shape[0]} rows and columns are: {df.columns.to_list()}'
    )
