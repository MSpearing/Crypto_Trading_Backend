# Michael Spearing

import requests
import pandas as pd
import time
import datetime
import psycopg2 as pg
import logging
import config


class Currency:
    def __init__(self, name, base):
        # Currncy Name
        self.name = name
        self.base = base
        self.conn = None
        self.cur = None

        # Set up Logging
        self.log_file = 'logs/{}_{}.log'.format(self.name.lower(), self.base.lower())
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

    def make_Connection(self):
        # Make Connection to RDS instance
        self.conn = pg.connect(database=config.db, user=config.username, password=config.password, host=config.host)
        self.cur = self.conn.cursor()
        return(self.conn, self.cur)
    
    def end_connection(self):
        # TODO: Make safe if invalid connection 
        self.conn.close()
        self.cur.close()

    def store_data(self):
        trading_url = config.trading_url
        #while(True):
        # Run for 2 min in stead of indefinitely
        for i in range(12):
            response = requests.get(trading_url +'/products/BTC-USD/book?level=1')
            now = int(time.time())
            pd_response = pd.read_json(response.text)
            pd_response = pd_response.drop('sequence', axis=1)

            bid_price = float(pd_response['asks'][0][0])
            ask_price = float(pd_response['bids'][0][0])
            bid_size = float(pd_response['asks'][0][1])
            ask_size = float(pd_response['bids'][0][1])
            bid_num_orders = int(pd_response['asks'][0][2])
            ask_num_orders = int(pd_response['bids'][0][2])
            pd_write = pd.DataFrame(columns=['ask_price','ask_size', 'ask_num_orders',
                                            'bid_price', 'bid_size', 'bid_num_orders'])
            pd_write.loc[now] = [bid_price,bid_size,bid_num_orders,ask_price,ask_size,ask_num_orders]

            price = round((ask_price+bid_price)/2,2)
            logging.info("[{}] BID: {} ASK: {} AVG: {}".format(now, bid_price, ask_price, price))
            sql = ("INSERT INTO btc_usd VALUES ({}, {}, {}, {}, {}, {}, {})").format(now, ask_price, ask_size, ask_num_orders, bid_price, bid_size, bid_num_orders)
            self.cur.execute(sql)
            self.conn.commit()
            time.sleep(config.delay)

if(__name__ == '__main__'):
    btc_usd = Currency('btc', 'usd')
    btc_usd.make_Connection()
    btc_usd.store_data()
    btc_usd.end_connection()