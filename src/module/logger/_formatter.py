"""
_formatter.py

Defines _Formatter
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'

import logging
from logging import LogRecord


class _Formatter(logging.Formatter):
    """
    The logging decorator logs the file and function name
    where it's defined, not where it's used.
    _Formatter corrects this behavior
    """

    def format(self, record: LogRecord):
        """
        Takes LogRecord object as input
        replaces funcName and filename
        with override values if existing

        args:
            - log record

        returns:
            - log record
        """
        # func/filename override defined in log_item.py
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override

        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override

        # returns superclass original method
        # but with updated record attributes
        return super(_Formatter, self).format(record)
