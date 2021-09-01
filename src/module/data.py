"""
data.py
Defines Data
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'

import shutil

from pyspark.sql.dataframe import DataFrame
from pyspark.sql import SparkSession

from config.constant import DATA_FOLDER
from util.util import get_df_types
from util.util import log_item


class Data:
    def __init__(self, spark: SparkSession) -> None:
        """
        Class constructor

        args:
            - spark: spark_session

        attributes:
            - spark: spark session
        """
        self.spark = spark


    @log_item
    def load_csv(self, filename: str, test: bool) -> DataFrame:
        """
        Read CSV file into dataframe

        args:
            - filename: file to load
            - test: load only sample data
        
        returns:
            - df: loaded data into spark DataFrame
        """
        # read file
        schema = get_df_types(filename)
        filepath = f'{DATA_FOLDER}/{filename}.csv'

        if test:
            df = self.spark.read \
                .schema(schema) \
                .option("header",True) \
                .option("mode", "PERMISSIVE") \
                .option('columnNameOfCorruptRecord', 'bad_record') \
                .csv(filepath) \
                .limit(20)

        else:
            df = self.spark.read \
                .schema(schema) \
                .option("header",True) \
                .option("mode", "PERMISSIVE") \
                .option('columnNameOfCorruptRecord', 'bad_record') \
                .csv(filepath)

        # corrects unordered events
        # TODO: remove
        df = df.sort(df.seq_num.asc())

        return df


    @log_item
    def load_stream(self, stream_name: str, test: bool) -> DataFrame:
        """
        Loads stream

        args:
            - stream_name: target folder name
            - test: load only sample data

        returns:
            - stream: Stream DataFrame
        """
        # load data
        l3df = self.load_csv('l3_data_v3', test)
        # replicate stream behavior
        self.partition(l3df, 'l3_data_v3')
        
        # read stream
        schema = get_df_types(stream_name)
        stream_name = f'/tmp/{stream_name}'
        stream = self.spark.readStream.format("csv") \
            .schema(schema) \
            .option("header",True) \
            .option("ignoreLeadingWhiteSpace",True) \
            .option("mode", "PERMISSIVE") \
            .option('columnNameOfCorruptRecord', 'bad_record') \
            .option("maxFilesPerTrigger",1) \
            .load(stream_name) \
            .selectExpr(
                "seq_num",
                "add_order_id",
                "add_side",
                "add_price",
                "add_qty",
                "update_order_id",
                "update_side",
                "update_price",
                "update_qty",
                "delete_order_id",
                "delete_side",
                "trade_order_id",
                "trade_side",
                "trade_price",
                "trade_qty",
                "time"
            )

        return stream


    def partition(self, df, folderpath: str, partitions: int = 1):
        """
        Partition CSV file to replicate stream behavior

        args:
            - folderpath: path to stream folder
            - partitions: number of created files
                          default to 1 for testing
        """
        df_part = df.repartition(partitions)

        folderpath = f'/tmp/{folderpath}'

        try:
            shutil.rmtree(folderpath)
        except:
            pass

        df_part.write \
            .format("CSV") \
            .option("header",True) \
            .save(folderpath)


    @log_item
    def save(self, df: DataFrame, filename: str):
        """
        Saves dataframe to CSV file. Leverages pandas.to_csv

        args:
            - df: loaded data into DataFrame object
            - filename: target filename
        """
        filepath = f'{DATA_FOLDER}/{filename}.csv'
        df.toPandas().to_csv(filepath, index=False)
