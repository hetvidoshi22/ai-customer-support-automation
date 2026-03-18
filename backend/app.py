# backend/app.py
import sys
import os
import logging

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Now import modules from backend/ (since they're in same dir as app.py)
from backend.data_processor import load_and_analyze_data
from backend.gemini_classifier import classify_query_with_gemini

# Rest of your imports
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.config import GEMINI_API_KEY

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) # Enable CORS for communication with the HTML frontend

# --- Global Variable to Hold Initial Data ---
initial_analysis_data = None
initial_summary = None
DATA_FILE_PATH = '../data/customer_support_dataset.csv'

@app.route('/')
def home():
    return "<h1>Customer Intelligence API Running!</h1><p>Go to /api/dashboard or /api/classify</p>"

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    global initial_analysis_data, initial_summary
    try:
        if initial_analysis_data is None or initial_summary is None:
            logger.info("Initial data not loaded, loading now...")
            initial_analysis_data, initial_summary, _ = load_and_analyze_data(DATA_FILE_PATH)
        
        return jsonify({
            "success": True,
            "distribution": initial_analysis_data,
            "summary": initial_summary
        }), 200
    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        return jsonify({"success": False, "error": str(fnf_error)}), 404
    except Exception as e:
        logger.error(f"Error loading dashboard data: {e}")
        return jsonify({"success": False, "error": "An internal error occurred while loading dashboard data."}), 500


@app.route('/api/classify', methods=['POST'])
def classify_new_query():
    try:
        data = request.get_json()
        query_text = data.get('query', '').strip()

        if not query_text:
            return jsonify({"success": False, "error": "Query text is required."}), 400

        logger.info(f"Classifying new query: {query_text}")
        
        # Use the Gemini classifier
        predicted_category, confidence, reasoning = classify_query_with_gemini(query_text)

        return jsonify({
            "success": True,
            "original_query": query_text,
            "predicted_category": predicted_category,
            "confidence": confidence,
            "reasoning": reasoning
        }), 200

    except Exception as e:
        logger.error(f"Error during classification: {e}")
        return jsonify({"success": False, "error": "An error occurred during classification."}), 500


if __name__ == '__main__':
    # Optional: Pre-load data on startup for faster first dashboard load
    try:
        initial_analysis_data, initial_summary, _ = load_and_analyze_data(DATA_FILE_PATH)
        logger.info("Initial data loaded successfully on startup.")
    except Exception as e:
        logger.error(f"Failed to preload data on startup: {e}")
        # App can still start, data will be loaded on first request if needed
        
    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000) # Listen on localhost:5000