from transformers import pipeline
import streamlit as st
from greetingHandler import check_greeting
from businessContext import get_business_context  # Import the business context logic

# Load pre-trained model (like GPT-4)
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Streamlit UI
st.title("Enterprise RAG-powered Business Decision Assistant")

# Input for user's question
user_question = st.text_input("Ask a business-related question:")

# Check for greeting
response = check_greeting(user_question)
if response:
    st.write(response)
else:
    # Use the refined context from business_context.py
    context = get_business_context(user_question)
    
    if user_question:
        # Get the answer from the model
        result = qa_model(question=user_question, context=context)
        st.write(f"Answer: {result['answer']}")
