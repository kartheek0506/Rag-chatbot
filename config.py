import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Pinecone Index
INDEX_NAME = "rag-index"

# Embedding Model
EMBED_MODEL = "all-MiniLM-L6-v2"

# Retrieval Config
TOP_K = 5
SIMILARITY_THRESHOLD = 0.5