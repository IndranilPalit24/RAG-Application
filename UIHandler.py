import streamlit as st
from boxDescription import business_contexts  # Import the business contexts

# Function to render the UI for the conversation
def display_ui(chat_history):
    st.title("NexQ - Enterprise RAG-powered Business Decision Assistant")
    st.subheader("How can I assist you today?")

    # Display existing conversation history
    for index, chat in enumerate(chat_history):
        if chat[0] == "user":
            st.markdown(f"<div style='text-align: right; background-color: #D0F0C0; padding: 10px; margin: 5px; border-radius: 10px;'>{chat[1]}</div>", unsafe_allow_html=True)
        elif chat[0] == "system":
            st.markdown(f"<div style='text-align: left; background-color: #F8F8FF; padding: 10px; margin: 5px; border-radius: 10px;'>{chat[1]}</div>", unsafe_allow_html=True)

    # Ensure unique key for each user input widget using index or timestamp
    user_input = st.text_input("Type your question here:", key=f"user_input_{len(chat_history)}", placeholder="Type your question here...")

    if st.button("Send", key=f"send_button_{len(chat_history)}"):
        return user_input
    return None
