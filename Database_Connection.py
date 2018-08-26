# Michael Spearing

#TODO: Consider using SQLAlchemy instead of direct SQL
import psycopg2 as pg
import config

class Database_Conection:
        
    def __init__(self):
        self.conn = pg.connect(database=config.db, user=config.username, password=config.password, host=config.host, port=config.port)
        self.cur = self.conn.cursor()

    def get_Latest_Entry(self, coin, base):
        sql = "SELECT * FROM {}_{} ORDER BY timestamp DESC LIMIT 1".format(coin.lower(), base.lower())
        return(self.execute_SQL(sql))

    def get_Latest_Entries(self, coin, base, number):
        sql = f'SELECT * FROM {coin.lower()}_{base.lower()} ORDER BY timestamp DESC LIMIT {number}'
        return(self.execute_SQL(sql))

    def get_Currencies(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        return(self.execute_SQL(sql))

    def execute_SQL(self, sql):
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        column_names = [desc[0] for desc in self.cur.description]
        if(type(rows[0]) == int):
            tmp = []
            tmp.append(rows)
            rows = tmp
        rows_formatted = []
        for row in rows:
            entry_dict = {}
            index = 0
            for column in column_names:
                entry_dict[column] = row[index]
                index += 1
            rows_formatted.append(entry_dict)
        return(rows_formatted)

    def __del__(self):
        print('Removing DB Connecton')
        self.cur.close()
        self.conn.close()

    def playground(self):
        self.cur.execute('SELECT * FROM btc_usd LIMIT 2')
        columns = [desc[0] for desc in self.cur.description]
        return(columns)
    

if(__name__ == '__main__'):
    db = Database_Conection()
    tmp = db.get_Latest_Entries('btc', 'usd', 5)
    print(tmp)