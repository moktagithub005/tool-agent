# app.py

import streamlit as st
from chatbot_core import ask_question
from langchain.schema import HumanMessage

st.set_page_config(page_title="Unisole RAG Chatbot", page_icon="🤖")

st.title("🤖 Unisole Conversational Chatbot")
st.markdown("Ask me anything about Unisole. I’ll use my memory and documents to help you!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render the existing conversation history
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Handle user input
user_input = st.chat_input("Ask your question...")

if user_input:
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response
    response = ask_question(user_input)

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add both messages to history AFTER display
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": response})
