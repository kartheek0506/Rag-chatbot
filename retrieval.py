from vector_store import index

# -------------------------
# 🔹 Lightweight embedding
# -------------------------
def simple_embedding(text, dim=384):
    base = float(len(text) % 1000) / 1000.0
    return [base + (i % 7) * 0.001 for i in range(dim)]


# -------------------------
# 🔹 Retrieval function
# -------------------------
def retrieve(query, top_k=3):
    try:
        # Generate embedding for query
        query_embedding = simple_embedding(query)

        # Query Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        matches = results.get("matches", [])

        if not matches:
            return {
                "context": "",
                "confidence": 0,
                "sources": []
            }

        # Extract context
        context = "\n".join(
            [match["metadata"].get("text", "") for match in matches]
        )

        # Confidence (average score)
        confidence = sum(
            [match.get("score", 0) for match in matches]
        ) / len(matches)

        # Sources
        sources = list(set(
            [match["metadata"].get("source", "unknown") for match in matches]
        ))

        return {
            "context": context,
            "confidence": confidence,
            "sources": sources
        }

    except Exception as e:
        print("RETRIEVAL ERROR:", e)
        return {
            "context": "",
            "confidence": 0,
            "sources": []
        }
