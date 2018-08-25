from flask import Flask

app = Flask(__name__)

@app.route('/home/')
def home_page():
    return('Hello World!')

if(__name__ == '__main__'):
    app.run(debub=True)
