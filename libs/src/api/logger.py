#!/usr/bin/env python3
from logging import DEBUG, getLogger as _getLogger, FileHandler, ERROR, basicConfig, Formatter
from os import getenv

from common.file import mkdir_if_not_exist

LOG_PATH = getenv('LIN_LOGSDIR', '/var/log/linapi')

mkdir_if_not_exist(LOG_PATH)
mkdir_if_not_exist(f'{LOG_PATH}/reports')

FORMATTER = Formatter('[%(asctime)s] %(levelname)s\t- %(name)s: %(message)s.')


def getHandler(filename: str, level: int) -> FileHandler:
    hdl = FileHandler(f'{LOG_PATH}/{filename}.log', encoding='utf-8')
    hdl.setLevel(level)
    hdl.setFormatter(FORMATTER)
    return hdl


ERROR_HANDLER = getHandler('errors', ERROR)
DEBUG_HANDLER = getHandler('debug', DEBUG)


basicConfig(format='[%(asctime)s] %(levelname)s\t- %(name)s: %(message)s',
            level=DEBUG)


def getLogger(name: str):
    logger = _getLogger(name)
    logger.setLevel(DEBUG)
    logger.propagate = False

    logger.addHandler(DEBUG_HANDLER)
    logger.addHandler(ERROR_HANDLER)

    return logger

