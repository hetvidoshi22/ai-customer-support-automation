import sys
import os
import logging
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from backend.data_processor import load_and_analyze_data
from backend.gemini_classifier import classify_query_with_gemini

from flask import Flask, request, jsonify
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data', 'customer_support_dataset.csv')

dashboard_cache = None


@app.route('/')
def home():
    return "🚀 API Running"


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    global dashboard_cache

    try:
        if dashboard_cache is None:
            logger.info("Loading dataset...")
            dashboard_cache = load_and_analyze_data(DATA_FILE_PATH)

        return jsonify({
            "success": True,
            "data": dashboard_cache
        })

    except Exception as e:
        logger.exception("Dashboard error")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/classify', methods=['POST'])
def classify_new_query():
    try:
        data = request.get_json()
        query_text = data.get("query", "").strip()

        if not query_text:
            return jsonify({"success": False, "error": "Query required"}), 400

        category = classify_query_with_gemini(query_text)

        confidence = 0.9 if category != "Ambiguous" else 0.5

        return jsonify({
            "success": True,
            "original_query": query_text,
            "predicted_category": category,
            "confidence": confidence,
            "reasoning": f"Classified as {category}"
        })

    except Exception as e:
        logger.exception("Classification error")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)