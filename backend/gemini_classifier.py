import google.generativeai as genai
from backend.config import GEMINI_API_KEY
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.1, 
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 512,
    "response_mime_type": "application/json", 
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    
    system_instruction="""
    You are an expert customer service query classifier. Analyze the provided customer query and classify it into one of the following predefined categories. Only respond with a valid JSON object containing 'category' and 'confidence'.

    Categories:
    - Order Tracking
    - Delivery Delay
    - Refund Request
    - Product Issue
    - Payment Failure
    - Subscription Issue
    - General Query
    - Ambiguous (if the query is unclear or doesn't fit other categories well)

    Response Format (JSON only):
    {
      "category": "Predicted Category Name",
      "confidence": 0.00
    }
    """
)

def classify_query_with_gemini(query_text):
    """
    Sends a query to the Gemini model and parses the response.
    """
    try:
        logger.info(f"Sending query to Gemini: {query_text[:50]}...") # Log first 50 chars
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(query_text)
        
        # Gemini should return a JSON string based on our system instruction
        response_text = response.text.strip()
        logger.debug(f"Gemini raw response: {response_text}")

        # Attempt to parse the JSON response
        import json
        parsed_response = json.loads(response_text)
        
        # Validate the structure
        if 'category' in parsed_response and 'confidence' in parsed_response:
            # Optional: Add reasoning if Gemini provides it
            reasoning = parsed_response.get('reasoning', 'Classified by Gemini AI.')
            return parsed_response['category'], parsed_response['confidence'], reasoning
        else:
            logger.warning("Gemini response did not match expected JSON format.")
            return "Ambiguous", 0.0, "Gemini response format was unexpected."

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode Gemini JSON response: {e}")
        logger.error(f"Raw response causing error: {response_text}")
        return "Ambiguous", 0.0, "Gemini response was not valid JSON."
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return "Ambiguous", 0.0, f"Gemini API error: {str(e)}"