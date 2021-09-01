"""
test.py
Defines tests functions
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'

from module import *
from module.bbo import Bbo


# spark
def test_spark_constructor():
    return Spark.session()


# data
def test_data_load():
    spark = Spark.session()
    data = Data(spark, 'l3_data_v3')
    df = data.load()

    df.printSchema()


def test_data_save():
    spark = Spark.session()
    in_data = Data(spark, 'l3_data_v3')
    df = in_data.load()

    out_data = Data(spark, 'l1_data')
    out_data.save(df)

# bbo
def test_bbo_constructor():
    spark = Spark.session()
    bbo = Bbo(spark)

    bbo.df.printSchema()


if __name__ == '__main__':
    # test_spark_constructor
    # test_spark_constructor()

    # test_data_load
    # test_data_load()

    # test_data_save
    test_data_save()

    # test_bbo_constructor
    # test_bbo_constructor()

