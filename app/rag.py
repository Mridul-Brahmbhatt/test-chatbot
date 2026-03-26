from app.llm import generate_response
from app.vectorstore import nec_retriever, wattmonk_retriever
from app.memory import get_history, add_to_history


# -------------------------
# Intent Classifier
# -------------------------
def classify_query(query: str) -> str:
    query = query.lower()

    if any(word in query for word in ["grounding", "wiring", "nec", "circuit", "electrical"]):
        return "NEC"

    if any(word in query for word in ["wattmonk", "company", "services", "policy"]):
        return "WATTMONK"

    return "GENERAL"


# -------------------------
# Main RAG Function
# -------------------------
def handle_query(query: str):

    intent = classify_query(query)
    history = get_history()

    # -------- GENERAL --------
    if intent == "GENERAL":
        messages = history + [{"role": "user", "content": query}]
        answer = generate_response(messages)

        add_to_history(query, answer)

        return {
            "answer": answer,
            "source": "LLM",
            "intent": intent
        }

    # -------- DOMAIN --------
    if intent == "NEC":
        docs = nec_retriever.invoke(query)
        source = "NEC"
    else:
        docs = wattmonk_retriever.invoke(query)
        source = "WATTMONK"

    if not docs:
        return {
            "answer": "I couldn't find relevant information.",
            "source": source,
            "intent": intent
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    messages = history + [
        {
            "role": "system",
            "content": "Answer ONLY using the provided context. If not found, say you don't know."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}"
        }
    ]

    answer = generate_response(messages)

    add_to_history(query, answer)

    return {
        "answer": answer,
        "source": source,
        "intent": intent
    }