from PyPDF2 import PdfReader
import tempfile
from sentence_transformers import SentenceTransformer
from vector_store import upsert_embeddings

# Load embedding model once (global)
model = SentenceTransformer("all-MiniLM-L6-v2")


def process_document(file, filename):
    try:
        # 🔥 Always take filename from UploadFile
        filename = file.filename

        # Save uploaded file temporarily
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

        # -------------------------
        # 🔥 STEP 1: CHUNKING
        # -------------------------
        chunks = []
        chunk_size = 200
        overlap = 50

        for i in range(0, len(text), chunk_size - overlap):
          chunks.append(text[i:i + chunk_size])

        print(f"Chunks created: {len(chunks)}")

        # -------------------------
        # 🔥 STEP 2: EMBEDDINGS
        # -------------------------
        embeddings = model.encode(chunks).tolist()
        print("Embeddings generated")

        # -------------------------
        # 🔥 STEP 3: STORE (CRITICAL)
        # -------------------------
        upsert_embeddings(chunks, embeddings, filename)

        print("Upload complete with metadata")

    except Exception as e:
        print("INGESTION ERROR:", e)
        raise e