# 🧠 RAG Chatbot (AI-Powered Document Q&A System)

An end-to-end Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions with context-aware answers using FastAPI, Pinecone, and Groq LLM.

---

## 🚀 Live Demo

- 🌐 API Docs: http://18.60.154.239:8000/docs  
- 💬 UI: http://18.60.154.239:7860  

> ⚠️ Note: The AWS instance may be stopped to avoid charges. Please contact me if the demo is not accessible.

---

## 🎥 Demo Video

👉 https://www.loom.com/share/ed55d0b4c60f4cdaa4d67b9c6a2f155a

---

## 🏗️ Architecture

![Architecture](assets/architecture.png)

---

## 🔄 Workflow

1. User uploads a PDF document
2. Text is extracted and split into chunks
3. Lightweight embeddings are generated
4. Embeddings are stored in Pinecone vector database
5. User submits a query
6. Relevant chunks are retrieved from Pinecone
7. Groq LLM generates an answer using retrieved context
8. System returns answer with confidence score and source

---

## ⚙️ Tech Stack

- **Backend**: FastAPI  
- **Frontend**: Gradio  
- **Vector Database**: Pinecone  
- **LLM**: Groq (LLaMA 3.1)  
- **Deployment**: AWS EC2  
- **Language**: Python  

---

## 📦 Project Structure
Rag-chatbot/
│── app.py
│── ingestion.py
│── retrieval.py
│── vector_store.py
│── llm.py
│── ui.py
│── data/
│── assets/
│── requirements.txt
│── README.md


---

## 🔑 Key Features

- 📄 Upload and process PDF documents
- 🔍 Context-aware question answering (RAG)
- ⚡ Fast vector search using Pinecone
- 🧠 LLM-powered answer generation using Groq
- 📊 Confidence scoring for responses
- 📄 Source attribution for transparency
- 🌐 Fully deployed on AWS EC2

---

## 🧠 Design Decisions

- Used lightweight embeddings to ensure compatibility with AWS free-tier (t3.micro)
- Implemented keyword-based filtering to improve retrieval accuracy without heavy ML dependencies
- Chose Pinecone for scalable and efficient vector search
- Used Groq LLM for fast inference and low latency
- Modular architecture separating ingestion, retrieval, and generation

---

## ⚠️ Limitations

- Lightweight embeddings reduce semantic accuracy compared to transformer-based embeddings
- Retrieval quality depends on document content and structure
- Requires running EC2 instance for live demo

---

## 🚀 Future Improvements

- Integrate OpenAI or HuggingFace embeddings for better semantic search
- Add authentication and multi-user support
- Implement conversational memory
- Dockerize the application for production deployment
- Deploy with custom domain and HTTPS

---

## 🛠️ Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-link>
cd Rag-chatbot
2. Create Virtual Environment

python -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt


4. Create .env File
PINECONE_API_KEY=your_key
GROQ_API_KEY=your_key
5. Run Backend
uvicorn app:app --host 0.0.0.0 --port 8000

6. Run UI
python ui.py

💼 Project Impact

Built and deployed a full-stack AI system that processes documents and generates context-aware answers using Retrieval-Augmented Generation (RAG) architecture on AWS EC2.