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


# ---------------- AUTO RESPONSE ----------------
def generate_auto_response(category):
    responses = {
        "Delivery Delay": "🚚 Your order is on the way. We apologize for the delay.",
        "Refund Request": "💰 Your refund is being processed.",
        "Order Tracking": "📦 You can track your order via your tracking link.",
        "Product Issue": "⚠️ Please share product images for resolution.",
        "Payment Failure": "💳 Try another payment method.",
        "Subscription Issue": "🔄 Manage subscription in settings.",
        "General Query": "ℹ️ Our team will assist you.",
        "Ambiguous": "❓ Please provide more details."
    }
    return responses.get(category, "Support team will assist you.")


# ---------------- ESCALATION ----------------
def escalation_logic(category, confidence):
    if category == "Ambiguous" or confidence < 0.6:
        return "⚠️ Escalated to Human Agent"
    return "✅ Handled by AI"


# ---------------- CLASSIFY API ----------------
@app.route('/api/classify', methods=['POST'])
def classify():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"success": False, "error": "Query required"})

    category = classify_query_with_gemini(query)
    confidence = 0.9 if category != "Ambiguous" else 0.5

    return jsonify({
        "success": True,
        "original_query": query,
        "predicted_category": category,
        "confidence": confidence,
        "reasoning": f"Classified as {category}",
        "auto_response": generate_auto_response(category),
        "escalation": escalation_logic(category, confidence)
    })


# ---------------- DASHBOARD API ----------------
@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    global dashboard_cache

    try:
        if dashboard_cache is None:
            dashboard_cache = load_and_analyze_data(DATA_FILE_PATH)

        return jsonify({
            "success": True,
            "data": dashboard_cache
        })

    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        })


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)