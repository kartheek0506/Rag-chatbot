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
def retrieve(query, top_k=5):
    try:
        query_embedding = simple_embedding(query)

        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        print("PINECONE RESULTS:", results)

        matches = results.get("matches", [])

        if not matches:
            return {
                "context": "",
                "confidence": 0.0,
                "sources": []
            }

        # 🔥 Filter strong matches
        filtered = [m for m in matches if float(m.get("score", 0)) > 0.80]

        if not filtered:
            filtered = matches[:1]  # fallback

        # 🔥 Confidence = best match (not avg)
        scores = [float(m.get("score", 0)) for m in filtered]
        confidence = max(scores)

        # 🔥 Clean context (avoid noisy chunks)
        context = " ".join([
            m["metadata"].get("text", "")[:300].replace("\n", " ")
            for m in filtered
        ])

        # 🔥 Sources
        sources = list(set([
            m["metadata"].get("source", "unknown")
            for m in filtered
        ]))

        return {
            "context": context,
            "confidence": float(confidence),
            "sources": sources
        }

    except Exception as e:
        print("RETRIEVAL ERROR:", e)
        return {
            "context": "",
            "confidence": 0.0,
            "sources": []
        }
