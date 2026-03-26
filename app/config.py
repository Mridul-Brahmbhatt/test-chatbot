import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

HF_EMBED_MODEL = os.getenv(
    "HF_EMBED_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)