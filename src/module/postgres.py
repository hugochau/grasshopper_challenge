"""
postgres.py
Defines Postgres
"""

from pyspark.sql.dataframe import DataFrame
from pyspark.sql import SparkSession

from config.constant import PGHOST
from util.util import get_pg_types
from util.util import log_item


class Postgres:
    def __init__(self, spark: SparkSession) -> None:
        """
        Class constructor
        args:
            - spark: spark session
        """
        self.spark = spark


    @log_item
    def write(self, df: DataFrame, table: str) -> None:
        """
        Writes spark DataFrame to table
        args:
            - df: data to be inserted
            - table: target table in RDBMS
        """
        url = f"jdbc:postgresql://{PGHOST}/grasshopper"
        properties = {
            "user": "grasshopper"
        }

        df.write \
            .option("driver", "org.postgresql.Driver") \
            .option("createTableColumnTypes", get_pg_types(table)) \
            .jdbc(url=url,
                  table=table,
                  mode='overwrite',
                  properties=properties)