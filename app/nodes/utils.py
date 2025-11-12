import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def call_llm(prompt: str) -> str:
    try:
        model_name = os.getenv("GEMINI_MODEL", "models/gemini-pro")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini API Error:", e)
        return "SELECT * FROM orders LIMIT 5;"
