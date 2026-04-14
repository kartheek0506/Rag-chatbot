from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(contexts, query):
    try:
        # 🔥 Combine retrieved chunks
        context = "\n\n".join(contexts).strip()

        # 🔥 Strong prompt (fixed hallucination issue)
        prompt = f"""
You are a strict assistant.

ONLY answer using the provided context.
If the answer exists in the context, answer directly.
DO NOT say "not found" if relevant information is present.
Be concise.

Context:
{context}

Question:
{query}

Answer:
"""

        # 🔥 Call Groq LLM
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ keep this if it works in your account
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "Error generating answer"