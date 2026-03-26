from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import handle_query

app = FastAPI(title="RAG Chatbot API")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "RAG Chatbot is running "}


@app.post("/chat")
def chat(req: ChatRequest):
    return handle_query(req.message)