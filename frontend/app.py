import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------
# Title
# ---------------------------
st.title("🤖 Multi-Context RAG Chatbot")
st.caption("Ask about NEC, Wattmonk, or general questions")

# ---------------------------
# Session State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This chatbot supports:
    - ⚡ NEC Code Queries  
    - 🏢 Wattmonk Info  
    - 💬 General Questions  
    """)

# ---------------------------
# Display Chat History
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# Chat Input
# ---------------------------
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):

            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_input},
                    timeout=500
                )

                data = response.json()

                answer = data.get("answer", "No response")
                source = data.get("source", "Unknown")
                intent = data.get("intent", "Unknown")

                # Format response
                bot_reply = f"""
{answer}

---
📌 **Source:** {source}  
🧠 **Intent:** {intent}
"""

            except Exception as e:
                bot_reply = f"❌ Error: {str(e)}"

            st.markdown(bot_reply)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })