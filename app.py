from fastapi import FastAPI, UploadFile
from ingestion import process_document
from retrieval import retrieve
from llm import generate_answer
from fastapi import BackgroundTasks
from pydantic import BaseModel

app = FastAPI()
class QueryRequest(BaseModel):
    q: str
    session_id: str


@app.post("/upload")
def upload(file: UploadFile, bg: BackgroundTasks):
    bg.add_task(process_document, file, file.filename)
    return {"message": "Processing started"}


@app.get("/query")
def query(q: str, session_id: str = "default"):
    contexts, scores, sources = retrieve(q)

    confidence = max(scores) if scores else 0


    # ✅ Confidence threshold
    if confidence < 0.1:   # was 0.3
        return {
            "query": q,
            "answer": "This question is not covered in uploaded documents.",
            "confidence": confidence,
            "sources": []
        }

    answer = generate_answer(contexts, q)

    return {
        "query": q,
        "answer": answer,
        "confidence": confidence,
        "sources": list(set(sources))
    }