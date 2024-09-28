# ragApplication.py

from transformers import pipeline
import streamlit as st
from greetingHandler import check_greeting
from businessContext import query_pinecone_for_context, store_embeddings_in_pinecone  # Import both
from businessHandler import BusinessDataHandler  # Import the new class

# Store the embeddings into Pinecone before running the Streamlit app
store_embeddings_in_pinecone()  # Store general business contexts

# Initialize the business handler for mock data
business_handler = BusinessDataHandler()
business_handler.load_mock_data('D:\\RAGHackathon\\MOCK_DATA.csv')  # Load mock data from a CSV
business_handler.embed_and_store_data()  # Embed and store mock data in Pinecone

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
    # Query Pinecone for the most relevant context based on the question
    context = query_pinecone_for_context(user_question)
    
    # Query mock data if needed
    mockup_data_response = business_handler.query_data(user_question)
    
    if user_question:
        # Get the answer from the model using the retrieved context
        result = qa_model(question=user_question, context=mockup_data_response)
        st.write(f"Answer: {result['answer']}")
