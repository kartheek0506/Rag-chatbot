from collections import defaultdict

# simple in-memory session storage
chat_memory = defaultdict(list)

def add_to_memory(session_id, user, bot):
    chat_memory[session_id].append({
        "user": user,
        "bot": bot
    })

def get_memory(session_id, k=3):
    history = chat_memory[session_id][-k:]
    memory_text = ""
    for h in history:
        memory_text += f"User: {h['user']}\nBot: {h['bot']}\n"
    return memory_text