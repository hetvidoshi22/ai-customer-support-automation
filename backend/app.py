import sys
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

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


# ---------------- AUTO RESPONSE + ACTION ----------------
def generate_automation_action(category):
    actions = {
        "Order Tracking": {
            "response": "📦 Track your order here: example.com/track",
            "action": "Auto-tracking link sent"
        },
        "Delivery Delay": {
            "response": "🚚 Sorry for delay. Your order is in transit.",
            "action": "Delay apology + status update sent"
        },
        "Refund Request": {
            "response": "💰 Refund initiated. It will reflect in 3-5 days.",
            "action": "Refund workflow triggered"
        },
        "Payment Failure": {
            "response": "💳 Payment failed. Try another method.",
            "action": "Payment retry suggestion sent"
        },
        "Product Issue": {
            "response": "⚠️ Please upload product image for resolution.",
            "action": "Support ticket created"
        },
        "Subscription Issue": {
            "response": "🔄 Manage subscription in your account settings.",
            "action": "Subscription self-service link sent"
        },
        "General Query": {
            "response": "ℹ️ Our team will assist you shortly.",
            "action": "Forwarded to support FAQ bot"
        },
        "Ambiguous": {
            "response": "❓ Please provide more details.",
            "action": "Clarification requested"
        }
    }
    return actions.get(category, {
        "response": "Support team will assist you.",
        "action": "Escalated"
    })


# ---------------- ESCALATION ----------------
def escalation_logic(category, confidence):
    if category == "Ambiguous" or confidence < 0.6:
        return "⚠️ Escalated to Human Agent"
    return "✅ Fully Automated"


# ---------------- CLASSIFY API ----------------
@app.route('/api/classify', methods=['POST'])
def classify():
    data = request.get_json()

    query = data.get("query", "").strip()
    source = data.get("source", "Web")  # NEW

    if not query:
        return jsonify({"success": False, "error": "Query required"})

    category = classify_query_with_gemini(query)

    confidence = 0.9 if category != "Ambiguous" else 0.5

    automation = generate_automation_action(category)

    return jsonify({
        "success": True,
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "original_query": query,
        "predicted_category": category,
        "confidence": confidence,
        "reasoning": f"Classified as {category}",
        "auto_response": automation["response"],
        "automation_action": automation["action"],
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


if __name__ == '__main__':
    app.run(debug=True)