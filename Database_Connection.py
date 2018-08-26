# Michael Spearing

import psycopg2 as pg
import config
class Database_Conection:
        
    def __init__(self):
        self.conn = pg.connect(database=config.db, user=config.username, password=config.password, host=config.host, port=config.port)
        self.cur = self.conn.cursor()

    def get_Last_Entry(self, coin, base):
        sql = "SELECT * FROM {}_{} ORDER BY timestamp DESC LIMIT 1".format(coin.lower(), base.lower())
        self.cur.execute(sql)
        return(self.to_json(self.cur.fetchone()))

    def get_Last_Entries(self, coin):
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()
    
    def to_json(self, entry):
        entry_dict = {'timestamp' : entry[0], 'ask_price' : entry[1], 'ask_size' : entry[2], 'ask_num_orders' : entry[3], 'bid_price' : entry[4], 'bid_size' : entry[5], 'bid_num_orders' : entry[6]}
        return(entry_dict)

if(__name__ == '__main__'):
    db = Database_Conection()
    tmp = db.get_Last_Entry('btc', 'usd')
    print(tmp)