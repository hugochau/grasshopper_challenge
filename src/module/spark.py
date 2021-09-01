"""
spark.py
Defines Spark
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'

from pyspark.sql import SparkSession

from util.util import log_item


class Spark:
    @staticmethod
    @log_item
    def session() -> SparkSession:
        """
        Creates spark session
        returns:
            - session: spark session object
        """
        session = SparkSession.builder \
            .master("local[1]") \
            .appName("grasshopper_challenge") \
            .config("spark.jars", "postgresql-42.2.23.jar") \
            .getOrCreate()

        return session