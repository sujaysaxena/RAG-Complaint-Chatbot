import requests
from app.llm import rag_response

user_sessions = {}

def process_chat(session_id, user_input):
    session = user_sessions.get(session_id, {"step": "init"})

    # Complaint Registration FSM
    if session["step"] == "init":
        if "register" in user_input.lower() or "file complaint" in user_input.lower():
            session["step"] = "awaiting_name"
            user_sessions[session_id] = session
            return "Please provide your name."
        elif "status" in user_input.lower() or "complaint" in user_input.lower():
            session["step"] = "awaiting_complaint_id"
            user_sessions[session_id] = session
            return "Please provide your Complaint ID to fetch the status."
        else:
            return rag_response(user_input)

    elif session["step"] == "awaiting_name":
        session["name"] = user_input
        session["step"] = "awaiting_phone"
        user_sessions[session_id] = session
        return "Thank you. Please provide your phone number."

    elif session["step"] == "awaiting_phone":
        session["phone_number"] = user_input
        session["step"] = "awaiting_email"
        user_sessions[session_id] = session
        return "Got it. Please provide your email address."

    elif session["step"] == "awaiting_email":
        session["email"] = user_input
        session["step"] = "awaiting_details"
        user_sessions[session_id] = session
        return "Thanks. Can you describe your complaint?"

    elif session["step"] == "awaiting_details":
        session["complaint_details"] = user_input
        payload = {
            "name": session["name"],
            "phone_number": session["phone_number"],
            "email": session["email"],
            "complaint_details": session["complaint_details"]
        }
        response = requests.post("http://127.0.0.1:8000/complaints", json=payload)
        if response.status_code == 200:
            complaint_id = response.json().get("complaint_id")
            session["step"] = "init"
            user_sessions[session_id] = session  # Reset session
            return f"Your complaint has been registered with ID: {complaint_id}."
        else:
            return "Error in registering complaint. Please try again."

    elif session["step"] == "awaiting_complaint_id":
        complaint_id = user_input
        response = requests.get(f"http://127.0.0.1:8000/complaints/{complaint_id}")
        if response.status_code == 200:
            data = response.json()

            # Use RAG to fetch additional complaint status info
            complaint_query = f"What is the status of the complaint regarding: {data['complaint_details']}?"
            rag_reply = rag_response(complaint_query)

            return (
                f"Complaint ID: {data['complaint_id']}\n\n"
                f"Name: {data['name']}\n\n"
                f"Phone: {data['phone_number']}\n\n"
                f"Email: {data['email']}\n\n"
                f"Details: {data['complaint_details']}\n\n"
                f"Created At: {data['created_at']}\n\n"
                f"Status Info (from RAG Database): {rag_reply}"
            )
        else:
            return "Complaint ID not found."

    return "I didn't understand that. Can you rephrase?"
