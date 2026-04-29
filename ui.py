import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/query"


def chat_fn(message, history):
    session_id = "default"

    try:
        response = requests.get(
            API_URL,
            params={"q": message, "session_id": session_id}
        ).json()

        answer = response.get("answer", "Error")
        sources = response.get("sources", [])
        confidence = response.get("confidence", 0)

        # Enhance answer display
        answer += f"\n\n📊 Confidence: {confidence:.2f}"
        if sources:
            answer += f"\n📄 Source: {', '.join(sources)}"

    except Exception as e:
        answer = f"Error: {str(e)}"

    history = history or []

    # ✅ limit memory
    history = history[-6:]

    # ✅ new gradio format
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})

    return "", history


with gr.Blocks() as demo:
    gr.Markdown("# 🧠 RAG Chatbot")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask something...")
    clear = gr.Button("Clear")

    msg.submit(chat_fn, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot, queue=False)

demo.launch(server_name="0.0.0.0", server_port=7860)