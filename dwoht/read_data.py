# -- coding: utf-8 --

import logging
import os
import time
from pathlib import Path
from typing import Dict, Union

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


def read_small_data(data_folder: Union[str, Path],
                    file_name: str,
                    reformat_cols: str = None,
                    rename_cols: Dict = None,
                    logger: Union[logging.Logger, str, None] = 'print',
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

    file_path = Path(data_folder).joinpath(file_name)

    if logger == 'print':
        print(f'Reading {file_path}')
    elif logger:
        logger.info(f'Reading {file_path}')
    else:
        pass

    start_time = time.time()

    file_suffix = str(file_path).split('.', 1)[1]
    read_functions = {'xlsx': pd.read_excel, 'txt': pd.read_csv, 'gzip': pd.read_parquet, 'parquet': pd.read_parquet}

    if 'csv.' in file_suffix:
        compression_type = file_suffix.split('.', 1)[1]

        if compression_type not in ['gz', 'gzip', 'bz2', 'xz', 'zip']:
            raise ValueError(f'Invalid file name {file_name}')

        if compression_type == 'gz':
            compression_type = 'gzip'

        df = pd.read_csv(file_path, low_memory=False, compression=compression_type, **kwargs)

    elif file_suffix == 'csv':
        if 'nrows' not in kwargs:
            rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
            with tqdm(total=rows, desc='Loading data') as bar:
                df = pd.concat((chunk for chunk in pd.read_csv(file_path, chunksize=10000, low_memory=False, **kwargs)), axis=0)
                bar.update(df.shape[0])
        else:
            df = pd.read_csv(file_path, low_memory=False, **kwargs)

    elif file_suffix in read_functions:
        df = read_functions[file_suffix](file_path, **kwargs)

    else:
        raise ValueError(f'Invalid file suffix {file_suffix}')

    if rename_cols:
        df.rename(columns=rename_cols, inplace=True)

    if reformat_cols:
        df.rename(columns=str.upper if reformat_cols == 'upper' else str.lower, inplace=True)

    if logger == 'print':
        print(f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, '
              f'Read {df.shape[0]} rows and columns: {df.columns.to_list()}')
    elif logger:
        logger.info(f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, '
                    f'Read {df.shape[0]} rows and columns: {df.columns.to_list()}')
    else:
        pass

    return df


def read_big_data(data_folder: Union[str, Path],
                  file_name: str,
                  reformat_cols: str = None,
                  rename_cols: Dict = None,
                  logger: Union[logging.Logger, str, None] = 'print',
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

    file_path = Path(data_folder).joinpath(file_name)

    if logger == 'print':
        print(f'Reading {file_path}')
    elif logger:
        logger.info(f'Reading {file_path}')
    else:
        pass

    start_time = time.time()

    file_suffix = str(file_path).split('.', 1)[1]

    read_functions = {'xlsx': pd.read_excel, 'txt': pd.read_csv, 'gzip': pd.read_parquet, 'parquet': pd.read_parquet}

    if 'csv.' in file_suffix:
        compression_type = file_suffix.split('.', 1)[1]

        if compression_type not in ['gz', 'gzip', 'bz2', 'xz', 'zip']:
            raise ValueError(f'Invalid file name {file_name}')

        if compression_type == 'gz':
            compression_type = 'gzip'

        df = pd.read_csv(file_path, low_memory=False, compression=compression_type, **kwargs)

    elif file_suffix == 'csv':
        if 'nrows' not in kwargs:
            if logger == 'print':
                print('Loading Chunks ...')
            elif logger:
                logger.info('Loading Chunks ...')
            else:
                pass

            chunk_reader = pd.read_csv(file_path, chunksize=1000000, **kwargs)  # the number of rows per chunk

            df_lst = []
            for df in chunk_reader:
                df_lst.append(df)

            if logger == 'print':
                print('Concat Chunks ...')
            elif logger:
                logger.info('Concat Chunks ...')
            else:
                pass

            df = pd.concat(df_lst, sort=False)
        else:
            df = pd.read_csv(file_path, low_memory=False, **kwargs)

    elif file_suffix in read_functions:
        df = read_functions[file_suffix](file_path, **kwargs)

    else:
        raise ValueError(f'Invalid file suffix {file_suffix}')

    if rename_cols:
        df.rename(columns=rename_cols, inplace=True)

    if reformat_cols:
        df.rename(columns=str.upper if reformat_cols == 'upper' else str.lower, inplace=True)

    if logger == 'print':
        print(f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, '
              f'Read {df.shape[0]} rows and columns: {df.columns.to_list()}')
    elif logger:
        logger.info(f'Data Reading Time: {round((time.time() - start_time), 2)} seconds, '
                    f'Read {df.shape[0]} rows and columns: {df.columns.to_list()}')
    else:
        pass

    return df


def save_data(data_folder: Union[str, Path], file_name: str, df: pd.DataFrame, logger: Union[logging.Logger, str, None] = 'print', **kwargs) -> None:
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

    if logger == 'print':
        print(f'Saving {file_path}')
    elif logger:
        logger.info(f'Saving {file_path}')
    else:
        pass

    start_time = time.time()

    if 'index' in list(kwargs.keys()):
        pass
    else:
        kwargs['index'] = False

    if file_suffix in ['xlsx']:
        df.to_excel(file_path, **kwargs)

    elif file_suffix == 'csv':
        df.to_csv(file_path, **kwargs)

    elif file_suffix == 'gzip':
        df.to_parquet(file_path, compression='gzip', **kwargs)

    elif 'csv.' in file_suffix:
        compression_type = file_suffix.split('.', 1)[1]

        if compression_type not in ['gz', 'gzip', 'bz2', 'xz', 'zip']:
            raise ValueError(f'Invalid file name {file_name}')

        if compression_type == 'gz':
            compression_type = 'gzip'

        df.to_csv(path_or_buf=file_path, compression=compression_type, **kwargs)

    else:
        raise ValueError(f'invalid file name {file_name}')

    if logger == 'print':
        print(f'Time consumed: {round((time.time() - start_time), 2)} seconds, '
              f'saved {df.shape[0]} rows and columns are: {df.columns.to_list()}')
    elif logger:
        logger.info(f'Time consumed: {round((time.time() - start_time), 2)} seconds, '
                    f'saved {df.shape[0]} rows and columns are: {df.columns.to_list()}')
    else:
        pass
