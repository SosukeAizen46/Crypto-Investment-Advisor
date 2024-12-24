from flask import Flask, jsonify, request, render_template
from textblob import TextBlob
import requests
import logging

app = Flask(__name__)
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/market_data', methods=['GET'])
def market_data():
    crypto_ids = "bitcoin,ethereum"
    vs_currency = "usd"
    try:
        logging.info("Fetching market data from CoinGecko.")
        url = f"{COINGECKO_API_URL}?ids={crypto_ids}&vs_currencies={vs_currency}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.debug(f"Market data retrieved: {data}")
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching market data: {e}")
        return jsonify({"error": "Failed to fetch market data. Please try again later."}), 500
    except Exception as e:
        logging.exception("Unexpected error occurred while fetching market data.")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        content = request.json.get('content', '').strip()
        if not content:
            logging.warning("No content provided for sentiment analysis.")
            return jsonify({"error": "Content is required for sentiment analysis."}), 400
        logging.info("Performing sentiment analysis.")
        sentiment_score = TextBlob(content).sentiment.polarity
        logging.debug(f"Sentiment score calculated: {sentiment_score}")
        return jsonify({"sentiment_score": sentiment_score})
    except Exception as e:
        logging.exception("Error occurred during sentiment analysis.")
        return jsonify({"error": str(e)}), 500

@app.route('/investment_recommendation', methods=['POST'])
def investment_recommendation():
    try:
        data = request.json
        if not data:
            logging.warning("No data provided in the request.")
            return jsonify({"error": "Request body is required."}), 400

        risk_level = data.get("risk_level", "").lower().strip()
        budget = data.get("budget", 0)

        if not risk_level:
            logging.warning("Risk level not provided.")
            return jsonify({"error": "Risk level is required."}), 400
        if budget <= 0:
            logging.warning("Invalid budget value.")
            return jsonify({"error": "Budget must be greater than zero."}), 400

        recommendations = {
            "low": [
                {"crypto": "bitcoin", "allocation": budget * 0.8},
                {"crypto": "ethereum", "allocation": budget * 0.2}
            ],
            "medium": [
                {"crypto": "bitcoin", "allocation": budget * 0.5},
                {"crypto": "ethereum", "allocation": budget * 0.3},
                {"crypto": "solana", "allocation": budget * 0.2}
            ],
            "high": [
                {"crypto": "bitcoin", "allocation": budget * 0.4},
                {"crypto": "solana", "allocation": budget * 0.4},
                {"crypto": "dogecoin", "allocation": budget * 0.2}
            ],
        }

        if risk_level not in recommendations:
            logging.warning(f"Invalid risk level: {risk_level}")
            return jsonify({"error": "Invalid risk level. Choose from 'low', 'medium', or 'high'."}), 400

        logging.info(f"Generating recommendations for risk level '{risk_level}'.")
        result = recommendations[risk_level]
        logging.debug(f"Recommendations: {result}")
        return jsonify({"recommendations": result})

    except KeyError as e:
        logging.error(f"Key error in request data: {e}")
        return jsonify({"error": f"Missing required key: {str(e)}"}), 400
    except Exception as e:
        logging.exception("Error occurred during investment recommendation.")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        logging.info("Starting the Flask app.")
        app.run(debug=True)
    except Exception as e:
        logging.critical(f"Failed to start the Flask app: {e}")

