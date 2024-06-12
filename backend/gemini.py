import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI"))

def answer_question(question: str, excel_data: dict) -> str:
    try:
        # Prepare the context for the LLM
        question = f"Excel Data: {excel_data}\n\nQuestion: {question}\n\nAnswer:" 
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred while processing the question: {e}"