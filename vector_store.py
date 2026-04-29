from dotenv import load_dotenv
import os
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Connect to index
index = pc.Index("rag-index")


 


def upsert_embeddings(chunks, embeddings, filename):
    try:
        print("VECTOR STORE FILENAME:", filename)  # ✅ debug

        vectors = []

        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            vectors.append({
                "id": f"{filename}_{i}",
                "values": emb,
                "metadata": {
                    "text": chunk,
                    "source": filename  # ✅ CRITICAL LINE
                }
            })

        # Upload to Pinecone
        index.upsert(vectors)

        print(f"Inserted {len(vectors)} vectors into Pinecone")

    except Exception as e:
        print("VECTOR STORE ERROR:", e)
        raise e