from PyPDF2 import PdfReader
import tempfile
from vector_store import upsert_embeddings

# ---- Lightweight embedding (no torch) ----
def simple_embedding(text, dim=384):
    # Deterministic, tiny embedding based on text stats
    base = float(len(text) % 1000) / 1000.0
    return [base + (i % 7) * 0.001 for i in range(dim)]

def process_document(file, filename):
    try:
        filename = file.filename

        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        # Read PDF
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            raise ValueError("No text extracted from PDF")

        print(f"Processed file: {filename}")

        # ---- Chunking ----
        chunks = []
        chunk_size = 200
        overlap = 50

        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i + chunk_size])

        print(f"Chunks created: {len(chunks)}")

        # ---- Lightweight embeddings ----
        embeddings = [simple_embedding(chunk) for chunk in chunks]
        print("Embeddings generated (lightweight)")

        # ---- Store ----
        upsert_embeddings(chunks, embeddings, filename)
        print("Upload complete with metadata")

    except Exception as e:
        print("INGESTION ERROR:", e)
        raise e