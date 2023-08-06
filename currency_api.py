from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import requests
import random
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exchange_data.db'
db = SQLAlchemy(app)

class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    base_currency = db.Column(db.String(10), nullable=False)

COINBASE_API_URL = "https://api.coinbase.com/v2/exchange-rates"

@app.route('/rates', methods=['GET'])
def get_exchange_rates():
    base_currency = request.args.get('base')

    if base_currency not in ["fiat", "crypto"]:
        return jsonify({"error": "Invalid base currency. Use 'fiat' or 'crypto'."}), 400

    try:
        response = requests.get(COINBASE_API_URL).json()
        rates = response['data']['rates']
        if base_currency == "fiat":
            data = {currency: rates[currency] for currency in ["BTC", "DOGE", "ETH"]}
        else:
            data = {currency: {fiat: str(1 / float(rates[fiat])) for fiat in ["USD", "SGD", "EUR"]} for currency in ["BTC", "DOGE", "ETH"]}

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch exchange rates."}), 500

@app.route('/historical-rates', methods=['GET'])
def get_historical_rates():
    base_currency = request.args.get('base_currency')
    target_currency = request.args.get('target_currency')
    start = int(request.args.get('start'))
    end = int(request.args.get('end', int(time.time() * 1000)))

    # For demo purposes, generate sample historical data within the specified range
    results = []
    current_timestamp = start
    while current_timestamp <= end:
        rate = random.uniform(0.0001, 0.001)
        results.append({"timestamp": current_timestamp, "value": str(rate)})
        current_timestamp += 60000  # Increment by 1 minute (60000 milliseconds)

    return jsonify({"results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)
