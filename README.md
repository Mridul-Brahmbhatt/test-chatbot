# RAG-Based Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot that answers:  
- General queries (via LLM)  
- NEC code guidelines (from `414.pdf`)  
- Company-specific queries (from Wattmonk PDFs)

---

## 📁 Project Structure
rag-chatbot/
│
├── app/ # Backend code
│ ├── main.py
│ ├── rag.py
│ ├── vectorstore.py
│ └── ...
├── frontend/ # Streamlit frontend
│ └── app.py
├── data/ # PDF knowledge sources
│ ├── 414.pdf
│ ├── Wattmonk (1) (1) (1).pdf
│ └── Wattmonk Information (1).pdf
├── chroma_db/ # Precomputed embeddings (for fast load)
├── .env # API keys (not in GitHub)
├── requirements.txt
└── README.md

---

## Installation

1. Clone the repo:
git clone <repo-url>
cd rag-chatbot

2. Create and activate a virtual environment:
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

3. Install dependencies:

4. Add .env file with your API keys:
   
5. OPENAI_API_KEY=sk-xxxxxxxxxxxx

## Running Locally

1. Start backend:
uvicorn app.main:app --reload

2. Start frontend
streamlit run frontend/app.py


graph TD
    User[User] -->|Types question| Frontend[Streamlit UI]
    Frontend -->|Calls API / function| Backend[FastAPI / RAG logic]
    Backend --> Intent[Intent Classification]
    Intent -->|NEC| NEC[NEC Vector Store (Chroma)]
    Intent -->|Company| Wattmonk[Wattmonk Vector Store (Chroma)]
    Intent -->|General| LLM[OpenAI / Hugging Face LLM]
    NEC -->|Retrieved docs| Backend
    Wattmonk -->|Retrieved docs| Backend
    LLM -->|Generates answer| Backend
    Backend -->|Returns answer| Frontend
    Frontend -->|Displays answer + source| User


## Features
Multi-context handling (General, NEC, Wattmonk)
Source attribution
Multi-turn conversation
Fallback responses for unknown queries
Optional: confidence score, query suggestions

this app was tested using ollama 
you can use your own api key
if you want to change the llm, you can edit the llm.py file
