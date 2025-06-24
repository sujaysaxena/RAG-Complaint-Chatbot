# 📝 RAG-Based Complaint Registration Chatbot

A complete end-to-end chatbot system combining:

✅ Conversational Complaint Registration  
✅ Complaint Status Retrieval via FastAPI APIs & MongoDB  
✅ Knowledge-Base-powered (RAG) Responses using FAISS + OpenAI Embeddings

---

## 🚀 Project Overview

This chatbot handles customer grievances in two ways:
1. **Complaint Registration:**  
   Asks the user for Name, Mobile, Email, Complaint Details and stores the info in MongoDB via FastAPI.
   
2. **Complaint Status Retrieval:**  
   When the user asks about complaint status, it:
   - Retrieves complaint details from the database.
   - Fetches relevant status information from a **PDF Knowledge Base (customer_guidelines.pdf)** using RAG pipeline powered by FAISS + OpenAI Embeddings.

---

## 📁 Project Structure

RAG-Complaint-Chatbot/
│
├── app/
│ ├── main.py # FastAPI routes (Complaint APIs & Chatbot API)
│ ├── database.py # MongoDB connection
│ ├── llm.py # FAISS-based RAG pipeline using OpenAI
│ ├── chatbot.py # Chatbot FSM logic handling complaints + RAG responses
│ └── schemas.py # Pydantic models
│
├── frontend/
│ └── streamlit_app.py # Streamlit UI for user interaction
│
├── knowledge_base/
│ └── customer_guidelines.pdf # Knowledge base PDF for RAG
│
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

### Setup

###1️⃣ Clone Repository
```bash
git clone <your-repo-url>
cd RAG-Complaint-Chatbot

### 2️⃣ Create Environment
conda create -n ragapp python=3.11 -y
conda activate ragapp

### 3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Environment Variables (.env)
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=your_mongo_uri

5️⃣ Run FastAPI Backend
uvicorn app.main:app --reload

6️⃣ Run Streamlit Frontend
streamlit run frontend/streamlit_app.py

---
