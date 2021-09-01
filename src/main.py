"""
main.py
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'

import os
import sys

from module import *
from module.logger import *

# init
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable


def main():
    # parse args
    args = Parser.parse()

    # spark session
    spark = Spark.session()
    data = Data(spark)
    postgres = Postgres(spark)

    # load stream l3 data
    stream = data.load_stream('l3_data_v3', args.test)

    # stream listener
    query = stream.writeStream \
        .queryName("stream") \
        .format("memory") \
        .outputMode("append") \
        .start()
    l3df = spark.sql("select * from stream")
    query.awaitTermination(10)
    query.stop()

    # update l1 data
    bbo = Bbo(spark)
    for row in l3df.rdd.collect():
        l1 = bbo.update(row)
        data.save(l1, 'l1_data')
        postgres.write(l1, 'l1_data')


if __name__ == '__main__':
    main()
