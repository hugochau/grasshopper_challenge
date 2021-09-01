"""
schema.py
Defines schemas
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'


from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    DecimalType,
    LongType,
    TimestampType
)

# spark df dtypes
L3_DF_DTYPES = StructType([
    StructField("seq_num", LongType(), True),
    StructField("add_order_id", LongType(), True),
    StructField("add_side", StringType(), True),
    StructField("add_price", DoubleType(), True),
    StructField("add_qty", DoubleType(), True),
    StructField("update_order_id", LongType(), True),
    StructField("update_side", StringType(), True),
    StructField("update_price", DoubleType(), True),
    StructField("update_qty", DoubleType(), True),
    StructField("delete_order_id", LongType(), True),
    StructField("delete_side", StringType(), True),
    StructField("trade_order_id", DoubleType(), True),
    StructField("trade_side", StringType(), True),
    StructField("trade_price", DoubleType(), True),
    StructField("trade_qty", DoubleType(), True),
    StructField("time", StringType(), True),
    StructField("bad_record", StringType(), True)
])

L1_DF_DTYPES = StructType([
    StructField("time", StringType(), True),
    StructField("bid_price", DoubleType(), True),
    StructField("ask_price", DoubleType(), True),
    StructField("bid_size", DoubleType(), True),
    StructField("ask_size", DoubleType(), True),
    StructField("seq_num", LongType(), True)
])


BBO_DF_DTYPES = StructType([
    StructField("time", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("size", DoubleType(), True),
    StructField("order_id", LongType(), True),
    StructField("seq_num", LongType(), True)
])

# pg dtypes
L1_PG_DTYPES = """
time varchar(255),
bid_price DECIMAL(6, 2),
ask_price DECIMAL(6, 2),
bid_size integer,
ask_size integer,
seq_num bigint
"""