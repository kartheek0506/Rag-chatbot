from sentence_transformers import SentenceTransformer
from vector_store import index

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query):
    query = query.lower()

    query_vector = model.encode(query).tolist()

    results = index.query(
        vector=query_vector,
        top_k=1,
        include_metadata=True
    )

    contexts = []
    sources = []
    scores = []

    for match in results["matches"]:
        contexts.append(match["metadata"]["text"])
        sources.append(match["metadata"].get("source", "unknown"))
        scores.append(match["score"])

    # ✅ ADD HERE (after scores is filled)
    print("Scores:", scores)

    return contexts, scores, sources
