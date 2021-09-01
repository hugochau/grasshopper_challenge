"""
adapter.py

Defines Adapter
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'

import logging
from logging import LogRecord


class Adapter(logging.Filter):
    def __init__(self, scope: str) -> None:
        """
        Class constructor

        attributes:
            - scope: optional logging option
        """
        self.scope = scope


    def filter(self, record: LogRecord) -> bool:
        """
        Adds scope attribute to logger output line

        args:
            record: str, logger output

        returns:
            - true
        """
        record.scope = self.scope.upper()

        return True
