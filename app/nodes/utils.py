import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def call_llm(prompt: str) -> str:
    try:
        # model_name = os.getenv("GEMINI_MODEL", "models/gemini-pro")
        model_name = st.secrets.get("GEMINI_MODEL", "models/gemini-pro")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini API Error:", e)
        return "SELECT * FROM orders LIMIT 5;"

