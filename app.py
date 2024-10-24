# app.py

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/add', methods=['GET'])
def add():
    return jsonify(result=2 + 3)

@app.route('/subtract', methods=['GET'])
def subtract():
    return jsonify(result=5 - 2)

if __name__ == '__main__':
    app.run(debug=True)
