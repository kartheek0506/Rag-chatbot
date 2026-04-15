from PyPDF2 import PdfReader
import tempfile
from sentence_transformers import SentenceTransformer
from vector_store import upsert_embeddings

# Load embedding model once (global)
model = SentenceTransformer("all-MiniLM-L6-v2")


def process_document(file, filename):
    try:
        # Always use filename from UploadFile
        filename = file.filename.lower()

        # -------------------------
        # 🔥 STEP 1: EXTRACT TEXT
        # -------------------------

        # Handle TXT files
        if filename.endswith(".txt"):
            text = file.file.read().decode("utf-8")

        # Handle PDF files
        elif filename.endswith(".pdf"):
            # Save temporarily
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(file.file.read())
                tmp_path = tmp.name

            reader = PdfReader(tmp_path)

            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

        else:
            raise ValueError("Unsupported file format. Only PDF and TXT allowed.")

        # Validate text
        if not text.strip():
            raise ValueError("No text extracted from document")

        print(f"Processed file: {filename}")

        # -------------------------
        # 🔥 STEP 2: CHUNKING
        # -------------------------
        chunks = []
        chunk_size = 200
        overlap = 50

        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i + chunk_size])

        print(f"Chunks created: {len(chunks)}")

        # -------------------------
        # 🔥 STEP 3: EMBEDDINGS
        # -------------------------
        embeddings = model.encode(chunks).tolist()
        print("Embeddings generated")

        # -------------------------
        # 🔥 STEP 4: STORE
        # -------------------------
        upsert_embeddings(chunks, embeddings, filename)

        print("Upload complete with metadata")

    except Exception as e:
        print("INGESTION ERROR:", e)
        raise e