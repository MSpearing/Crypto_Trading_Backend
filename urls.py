from flask import Flask
from flask import jsonify
import Database_Connection
app = Flask(__name__)

db = Database_Connection.Database_Conection()

@app.route('/home/<string:coin>_<string:base>/')
def home_page(coin, base):
    return(jsonify(db.get_Last_Entry(coin, base)))

if(__name__ == '__main__'):
    app.run(debug=True)
