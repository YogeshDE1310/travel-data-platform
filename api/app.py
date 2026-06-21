from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_json(file_name):

    with open(f"data/{file_name}", "r") as f:
        return json.load(f)

@app.route('/')
def home():

    return {"message": "Travel API Running"}

@app.route('/users')
def users():

    return jsonify(load_json("users.json"))

@app.route('/flights')
def flights():

    return jsonify(load_json("flights.json"))

@app.route('/hotels')
def hotels():

    return jsonify(load_json("hotels.json"))

@app.route('/bookings')
def bookings():

    return jsonify(load_json("bookings.json"))

if __name__ == '__main__':
    app.run(debug=True)