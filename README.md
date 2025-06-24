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
