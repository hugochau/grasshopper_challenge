"""
bbo.py
Defines bbo
"""

__version__ = '1.0'
__author__ = 'Hugo Chauvary'
__email__ = 'chauvary.hugo@gmail.com'

from module import logger
from pyspark.sql import SparkSession
from pyspark.sql.types import Row

from module.data import Data
from module.logger import *
from util.util import get_df_types
from util.util import log_item


class Bbo:
    def __init__(self, spark: SparkSession) -> None:
        """
        Class constructor
        
        args:
            - spark: spark session

        attributes:
            - spark: spark session
            - bids: collection of bids, sspark df
            - asks: collection of asks, spark df
            - l1: collection of bbos, spark df

        """
        self.spark = spark
        self.bids = spark.createDataFrame([], get_df_types('bbo'))
        self.asks = spark.createDataFrame([], get_df_types('bbo'))
        self.l1 = spark.createDataFrame([], get_df_types('l1_data'))


    @log_item
    def update(self, record: Row):
        """
        Update bbo

        attributes:
            - record: l3 formatted record
        """
        logger = Logger().logger
        logger.info(f'processing seq_num {record.seq_num}')

        bids_count = self.bids.count()
        asks_count = self.asks.count()
        bids_first = self.bids.first()
        asks_first = self.asks.first()

        # case 1: new order/buy side
        if record.add_side == 'BUY':
            # create bid record
            vals = [(
                record.time,
                record.add_price,
                record.add_qty,
                record.add_order_id,
                record.seq_num
            )]
            bid = self.spark.createDataFrame(vals, get_df_types('bbo'))

            # condition to create a bbo entry
            # new highest buy price
            if ((bids_count > 0 and record.add_price > bids_first.price) \
                or bids_count == 0) \
                and asks_count > 0:
                vals = [(
                    record.time,
                    record.add_price,
                    asks_first.price,
                    record.add_qty,
                    asks_first.size,
                    record.seq_num
                )]

                bbo = self.spark.createDataFrame(vals, get_df_types('l1_data'))
                # bbo.show()

                self.l1 = self.l1.union(bbo)

            # self.bids.show()
            
            # limit(2) because we do not need to store all bids
            # improves performance
            # TODO: test
            self.bids = self.bids.limit(2).union(bid)
            self.bids = self.bids.sort(self.bids.price.desc())
            # self.bids.show()

        # case 2: new order/sell side
        if record.add_side == 'SELL':
            # create ask record
            vals = [(
                record.time,
                record.add_price,
                record.add_qty,
                record.add_order_id,
                record.seq_num
            )]

            ask = self.spark.createDataFrame(vals, get_df_types('bbo'))

            # condition to create a bbo entry
            # new lowest sell price
            if ((asks_count > 0 and record.add_price < asks_first.price) \
                or asks_count == 0) \
                and bids_count > 0:
                vals = [(
                    record.time,
                    bids_first.price,
                    record.add_price,
                    bids_first.size,
                    record.add_qty,
                    record.seq_num
                )]

                bbo = self.spark.createDataFrame(vals, get_df_types('l1_data'))

                # bbo.show()
                self.l1 = self.l1.union(bbo)

            self.asks = self.asks.limit(2).union(ask)
            self.asks = self.asks.sort(self.asks.price.asc())
            # self.asks.show()

        # case 3: deleted order/buy side
        if record.delete_side == 'BUY':
            order_id = bids_first.order_id

            self.bids = self.bids.filter(self.bids.order_id != record.delete_order_id)
            bids_first = self.bids.first()

            # condition to create a bbo entry
            # deleted highest buy price
            if order_id == record.delete_order_id:
                vals = [(
                    record.time,
                    bids_first.price,
                    asks_first.price,
                    bids_first.size,
                    asks_first.size,
                    record.seq_num
                )]

                bbo = self.spark.createDataFrame(vals, get_df_types('l1_data'))
                # bbo.show()

                self.l1 = self.l1.union(bbo)

        # case 4: deleted order/sell side
        if record.delete_side == 'SELL':
            order_id = asks_first.order_id

            self.asks = self.asks.filter(self.asks.order_id != record.delete_order_id)
            asks_first = self.asks.first()

            # condition to create a bbo entry
            # deleted lowest sell price
            if order_id == record.delete_order_id:
                vals = [(
                    record.time,
                    bids_first.price,
                    asks_first.price,
                    bids_first.size,
                    asks_first.size,
                    record.seq_num
                )]

                bbo = self.spark.createDataFrame(vals, get_df_types('l1_data'))
                # bbo.show()

                self.l1 = self.l1.union(bbo)

        # case 5: updated order/buy side
        if record.update_side == 'BUY':
            order_id = bids_first.order_id

            # delete bid
            self.bids = self.bids.filter(self.bids.order_id != record.update_order_id)

            # condition to create a bbo entry
            # updated highest buy price
            # TODO: check if remains highest price
            if order_id == record.update_order_id:
                vals = [(
                    record.time,
                    record.add_price,
                    asks_first.price,
                    record.add_qty,
                    asks_first.size,
                    record.seq_num
                )]

                bbo = self.spark.createDataFrame(vals, get_df_types('l1_data'))
                # bbo.show()

                self.l1 = self.l1.union(bbo)

            # create updated bid
            vals = [(
                record.time,
                record.update_price,
                record.update_qty,
                record.update_order_id,
                record.seq_num
            )]

            bid = self.spark.createDataFrame(vals, get_df_types('bbo'))

            # add bid and reorder
            self.bids = self.bids.limit(2).union(bid)
            self.bids = self.bids.sort(self.bids.price.desc())

        # case 6: updated order/sell side
        if record.update_side == 'SELL':
            order_id = asks_first.order_id

            # delete ask
            self.asks = self.asks.filter(self.asks.order_id != record.update_order_id)

            # condition to create a bbo entry
            # updated lowest sell price
            # TODO: check if remains lowest price
            if order_id == record.update_order_id:
                vals = [(
                    record.time,
                    bids_first.price,
                    record.add_price,
                    bids_first.size,
                    record.add_qty,
                    record.seq_num
                )]

                bbo = self.spark.createDataFrame(vals, get_df_types('l1_data'))
                # bbo.show()

                self.l1 = self.l1.union(bbo)

            # create updated ask
            # add to asks and reorder
            vals = [(
                record.time,
                record.update_price,
                record.update_qty,
                record.update_order_id,
                record.seq_num
            )]
            ask = self.spark.createDataFrame(vals, get_df_types('bbo'))
            self.asks = self.asks.limit(2).union(ask)
            self.asks = self.asks.sort(self.asks.price.desc())

        # self.l1.show()
        return self.l1