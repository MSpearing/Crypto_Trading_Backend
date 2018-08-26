from flask import Flask
from flask import jsonify
import Database_Connection
app = Flask(__name__)

db = Database_Connection.Database_Conection()

@app.route('/home/<string:coin>_<string:base>/')
def get_Latest_Entry(coin, base):
    return(jsonify(db.get_Latest_Entry(coin, base)))

@app.route('/home/<string:coin>_<string:base>_<int:amt>/')
def get_Latest_Entries(coin, base, amt):
    return(jsonify(db.get_Latest_Entries(coin, base, amt)))

@app.route('/home/currencies/')
def get_Currencies():
    return(jsonify(db.get_Currencies()))

if(__name__ == '__main__'):
    app.run(debug=True)
