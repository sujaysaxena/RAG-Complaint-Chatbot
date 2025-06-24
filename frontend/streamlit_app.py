import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="RAG Complaint Chatbot", page_icon="💬")

st.title("🤖 RAG Complaint Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input:
    st.session_state.chat_history.append({"role": "user", "message": user_input})

    with st.spinner("Thinking..."):
        response = requests.post(API_URL, json={"message": user_input, "session_id": "user123"})
        if response.status_code == 200:
            bot_reply = response.json().get("response")
        else:
            bot_reply = "Error: Unable to get response."
        st.session_state.chat_history.append({"role": "bot", "message": bot_reply})

for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['message']}")
    else:
        st.markdown(f"**Bot:** {chat['message']}")
