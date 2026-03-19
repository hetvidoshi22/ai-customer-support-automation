import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")


def rule_based_fallback(query):
    q = query.lower()

    if "refund" in q:
        return "Refund Request"
    elif "late" in q or "delay" in q:
        return "Delivery Delay"
    elif "track" in q or "where is my order" in q:
        return "Order Tracking"
    elif "payment" in q or "deducted" in q:
        return "Payment Failure"
    elif "subscription" in q:
        return "Subscription Issue"
    elif "broken" in q or "damaged" in q or "quality" in q:
        return "Product Issue"
    elif len(q.strip()) < 5:
        return "Ambiguous"

    return None


def classify_query_with_gemini(query):
    try:
        prompt = f"""
        Classify this query into ONE category:
        [Order Tracking, Delivery Delay, Refund Request, Product Issue, Payment Failure, Subscription Issue, General Query, Ambiguous]

        Query: "{query}"

        Return ONLY category name.
        """

        response = model.generate_content(prompt)
        category = response.text.strip()

        # 🔥 Post-processing correction
        fallback = rule_based_fallback(query)

        if category == "Ambiguous" and fallback:
            return fallback

        return category

    except Exception:
        fallback = rule_based_fallback(query)
        return fallback if fallback else "Ambiguous"