# -- coding: utf-8 --

import logging
import os
import sys
import time
from logging import handlers


def set_logger(save_file: bool = False, log_file: str = None, log_dir: str = None) -> logging.Logger:
    """
    get a logger
    :param save_file: whether to save log to file
    :param log_file: log file name
    :param log_dir: log file directory
    :return: a logger
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    __formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s')

    __console = logging.StreamHandler(stream=sys.stdout)
    __console.setLevel(logging.INFO)
    __console.setFormatter(__formatter)
    logger.addHandler(__console)

    if save_file:
        if log_dir is None:
            raise ValueError('log_dir must be specified if save_file is True')
        else:
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)

        if log_file is None:
            log_file = time.strftime("%H_%M_%S")

        __file = handlers.TimedRotatingFileHandler(os.path.join(log_dir, '{}.log'.format(log_file)), when='D', encoding='UTF-8')
        __file.setLevel(logging.INFO)
        __file.setFormatter(__formatter)
        logger.addHandler(__file)

    return logger
