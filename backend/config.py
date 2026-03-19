import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

if not GEMINI_API_KEY:
    raise RuntimeError(
        "❌ GEMINI_API_KEY is missing! Please create a .env file in the project root with:\n"
        "GEMINI_API_KEY=your_actual_key_here\n"
        "GOOGLE_API_KEY=your_actual_key_here # Also add this line"
    )