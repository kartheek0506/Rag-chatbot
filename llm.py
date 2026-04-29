import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query, context):
    try:
        prompt = f"""
You are an AI assistant.

Answer the question ONLY using the given context.

If the context does not contain relevant information, say:
"I don't have enough information."

Context:
{context}

Question:
{query}

Answer clearly in 2-3 sentences.
Do NOT return single words or SQL keywords.
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "Error generating response."
