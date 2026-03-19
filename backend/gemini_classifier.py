import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-pro")


def classify_query_with_gemini(query):
    try:
        prompt = f"""
        Classify this customer query into ONE category:
        [Order Tracking, Delivery Delay, Refund Request, Product Issue, Payment Failure, Subscription Issue, General Query, Ambiguous]

        Query: "{query}"

        Return only the category name.
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception:
        return "Ambiguous"