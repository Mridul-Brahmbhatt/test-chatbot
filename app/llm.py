import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


def generate_response(messages):
    model = genai.GenerativeModel("gemini-1.5-flash") 

    # Convert OpenAI-style messages to a single prompt
    prompt = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        prompt += f"{role}: {content}\n"

    response = model.generate_content(prompt)

    return response.text
