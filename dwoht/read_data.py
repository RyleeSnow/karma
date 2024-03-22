from __future__ import annotations

import logging
import os
import time
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from tqdm.auto import tqdm


def my_read_parquet(file_path, **kwargs) -> pd.DataFrame:
    """
    customized function to read parquet

    :param file_path: parquet file path
    :return: loaded pd.dataframe
    """

    parquet_file = pq.ParquetFile(file_path, **kwargs)
    dfs = [batch.to_pandas() for batch in tqdm(parquet_file.iter_batches(), disable=False, desc='Loading data')]
    df = pd.concat(dfs, ignore_index=True)

    return df


def read_small_data(file_name: str,
                    data_folder: str | Path,
                    reformat_cols: str = None,
                    rename_cols: dict = None,
                    logger: logging.Logger = None,
                    **kwargs) -> pd.DataFrame:
    """
    customized function to read a singe data file, supporting read_excel / read_csv / read_parquet

    :param file_name: full file path including suffix
    :param data_folder: the main dir where the data is saved
    :param reformat_cols: reformat column names to lower or upper characters, accept `lower` / `upper`, default is None
    :param rename_cols: rename the columns
    :param logger: logger
    :return: loaded pd.dataframe
    """

    data_folder = Path(data_folder)
    file_path = data_folder.joinpath(file_name)

    if logger is None:
        print(f'Reading {file_path}')
    else:
        logger.info(f'Reading {file_path}')

    start_time = time.time()

    file_suffix = file_name.split('.', 1)[1]

    if file_suffix in ['xlsx', 'xls']:
        df = pd.read_excel(file_path, **kwargs)

    elif file_suffix == 'csv':
        if 'nrows' in kwargs:
            df = pd.read_csv(file_path, low_memory=False, **kwargs)
        else:
            rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1

            chunk_list = []
            with tqdm(total=rows, desc='Loading data') as bar:
                for chunk in pd.read_csv(file_path, chunksize=10000, low_memory=False, **kwargs):
                    chunk_list.append(chunk)
                    bar.update(len(chunk))

            df = pd.concat((f for f in chunk_list), axis=0)

    elif file_suffix == 'txt':
        df = df = pd.read_csv(file_path, low_memory=False, **kwargs)

    elif file_suffix == 'gzip':
        df = my_read_parquet(file_path=file_path, **kwargs)

    elif 'csv.' in file_suffix:
        compression_type = file_suffix.split('.', 1)[1]

        if '.' in compression_type:
            raise ValueError(f'invalid file name {file_name}')
        else:
            if compression_type == 'gz':
                compression_type = 'gzip'
            else:
                pass

            df = pd.read_csv(file_path, low_memory=False, compression=compression_type, **kwargs)

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

    if logger is None:
        print(f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, '
              f'read {df.shape[0]} rows and columns are: {df.columns.to_list()}')
    else:
        logger.info(f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, '
                    f'read {df.shape[0]} rows and columns are: {df.columns.to_list()}')

    return df


def read_big_data(file_name: str,
                  data_folder: str | Path,
                  reformat_cols: str = None,
                  rename_cols: dict = None,
                  logger: logging.Logger = None,
                  **kwargs) -> pd.DataFrame:
    """
    customized function to read a singe data file, supporting read_excel / read_csv / read_parquet

    :param file_name: full file path including suffix
    :param data_folder: the main dir where the data is saved
    :param reformat_cols: reformat column names to lower or upper characters, accept `lower` / `upper`, default is None
    :param rename_cols: rename the columns
    :param logger: logger
    :return: loaded pd.dataframe
    """

    data_folder = Path(data_folder)

    file_path = data_folder.joinpath(file_name)

    if logger is None:
        print(f'Reading {file_path}')
    else:
        logger.info(f'Reading {file_path}')
    start_time = time.time()

    file_suffix = file_name.split('.', 1)[1]

    if file_suffix in ['xlsx', 'xls']:
        df = pd.read_excel(file_path, **kwargs)

    elif file_suffix == 'csv':
        if 'nrows' in kwargs:
            df = pd.read_csv(file_path, low_memory=False, **kwargs)
        else:
            if logger is None:
                print('Loading Chunks ...')
            else:
                logger.info('Loading Chunks ...')

            chunk_reader = pd.read_csv(file_path, chunksize=1000000, **kwargs)  # the number of rows per chunk

            df_lst = []
            for df in chunk_reader:
                df_lst.append(df)

            if logger is None:
                print('Concat Chunks ...')
            else:
                logger.info('Concat Chunks ...')

            df = pd.concat(df_lst, sort=False)

    elif file_suffix == 'txt':
        df = df = pd.read_csv(file_path, low_memory=False, **kwargs)

    elif file_suffix == 'gzip':
        df = my_read_parquet(file_path=file_path, **kwargs)

    elif 'csv.' in file_suffix:
        compression_type = file_suffix.split('.', 1)[1]

        if '.' in compression_type:
            raise ValueError(f'invalid file name {file_name}')
        else:
            if compression_type == 'gz':
                compression_type = 'gzip'
            else:
                pass

            df = pd.read_csv(file_path, low_memory=False, compression=compression_type, **kwargs)

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

    if logger is None:
        print(f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, '
              f'read {df.shape[0]} rows and columns are: {df.columns.to_list()}')
    else:
        logger.info(f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, '
                    f'read {df.shape[0]} rows and columns are: {df.columns.to_list()}')

    return df


def save_data(df: pd.DataFrame, data_folder: str | Path, file_name: str, logger: logging.Logger = None, **kwargs) -> None:
    """
    customized function to save a dataframe, supporting to_excel / to_csv / to_parquet

    :param df: pd.dataframe to be saved
    :param data_folder: the main dir where the data is saved
    :param file_name: full file path including suffix
    :param logger: logger
    :return: None
    """

    data_folder = Path(data_folder)

    if data_folder.is_dir():
        pass
    else:
        os.makedirs(data_folder)

    file_path = data_folder.joinpath(file_name)
    file_suffix = file_name.split('.', 1)[1]

    if logger is None:
        print(f'Saving {file_path}')
    else:
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
    if logger is None:
        print(f'Time consumed: {round((time.time() - start_time), 2)} seconds, '
              f'saved {df.shape[0]} rows and columns are: {df.columns.to_list()}')
    else:
        logger.info(f'Time consumed: {round((time.time() - start_time), 2)} seconds, '
                    f'saved {df.shape[0]} rows and columns are: {df.columns.to_list()}')
