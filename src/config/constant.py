"""
constant.py
Defines constants
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'

import os
import logging
import datetime


# folders
DATA_FOLDER = '../data'

# logger
LOG_FOLDER = os.path.join(DATA_FOLDER, 'log')
LOG_LEVEL = logging.INFO
LOG_FILENAME = 'log_' \
                + datetime.datetime.isoformat(datetime.datetime.today())
LOG_FILEPATH = os.path.join(LOG_FOLDER, LOG_FILENAME)

# postgres
PGHOST = os.getenv('PGHOST')