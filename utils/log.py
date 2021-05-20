import datetime as dt
import os
import logging

now: dt.datetime = dt.datetime.now()
DEFAULT_LEVEL = logging.DEBUG
LOGGER_NAME = 'Set logger name...'

now_str = now.strftime('%Y%m%d_%H%M')

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

if not len(logger.handlers):
    directory = 'output_log\\'
    try:
        os.stat(directory)
    except NotADirectoryError:
        os.mkdir(directory)
    except FileNotFoundError:
        os.mkdir(directory)
    FILE_NAME = '{directory!s}_{module!s}_{user!s}_{now_str!s}.txt'.format(
        directory=directory, module='log', user=os.getlogin(), now_str=now_str
    )
    fh = logging.FileHandler(FILE_NAME)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(levelname)s: [%(asctime)s - %(name)s - %(process)s - [%(filename)s:%(lineno)s - %(module)s - %(function)s() ]] - %(message)s'
    )
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

'''
logger.critical('This is a critical message.')
logger.error('This is an error message.')
logger.warning('This is a warning message.')
logger.info('This is an informative message.')
logger.debug('This is a low-level debug message.')
'''
