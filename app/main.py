from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import complaints_collection
from app.chatbot import process_chat

app = FastAPI()

class Complaint(BaseModel):
    name: str
    phone_number: str
    email: str
    complaint_details: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/complaints")
def register_complaint(complaint: Complaint):
    from datetime import datetime
    import uuid

    complaint_id = f"CMP{str(uuid.uuid4().int)[:6]}"
    complaint_dict = complaint.dict()
    complaint_dict.update({"complaint_id": complaint_id, "created_at": datetime.utcnow()})

    print("Registering Complaint:", complaint_dict)  # Debug Print (Add this!)

    complaints_collection.insert_one(complaint_dict)
    return {"complaint_id": complaint_id, "message": "Complaint created successfully."}

@app.get("/complaints/{complaint_id}")
def get_complaint_status(complaint_id: str):
    complaint = complaints_collection.find_one({"complaint_id": complaint_id})
    if complaint:
        return {
            "complaint_id": complaint["complaint_id"],
            "name": complaint["name"],
            "phone_number": complaint["phone_number"],
            "email": complaint["email"],
            "complaint_details": complaint["complaint_details"],
            "created_at": complaint["created_at"]
        }
    raise HTTPException(status_code=404, detail="Complaint not found.")

@app.post("/chat")
def chat(chat_req: ChatRequest):
    reply = process_chat(chat_req.session_id, chat_req.message)
    return {"response": reply}
