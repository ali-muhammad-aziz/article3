import os
import streamlit as st
from google import genai

# --- Page Setup and Custom Styling ---
st.set_page_config(page_title="Gemini Chat", layout="wide", initial_sidebar_state="collapsed")

# --- Initialize Gemini Client and ChatSession ---
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)  # API-key mode for Gemini Developer API

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(model="gemini-2.0-flash")
chat_session = st.session_state.chat_session

# --- Conversation History State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render Past Messages ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

# --- Handle New User Input and Streaming Response ---
user_input = st.chat_input("Type your message here…")
if user_input:
    # Display and record user message
    st.session_state.messages.append({"role": "user", "text": user_input})
    st.chat_message("user").write(user_input)

    # Stream assistant response
    assistant_text = ""
    placeholder = st.chat_message("assistant")
    response = chat_session.send_message(user_input)
    placeholder.write(response.candidates[0].content.parts[0].text)

    # Record assistant message
    st.session_state.messages.append({"role": "assistant", "text": assistant_text})