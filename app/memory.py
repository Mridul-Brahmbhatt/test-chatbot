# Simple global memory (for demo)

chat_history = []

def get_history():
    return chat_history

def add_to_history(user, bot):
    chat_history.append({"role": "user", "content": user})
    chat_history.append({"role": "assistant", "content": bot})