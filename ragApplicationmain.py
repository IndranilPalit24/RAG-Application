from transformers import pipeline
import streamlit as st
from greetingHandler import check_greeting
from businessContext import query_context_from_pinecone, store_business_context_embeddings  # Import both
from businessHandler import BusinessDataHandler  # Import the BusinessDataHandler class

# Store the predefined business context embeddings into Pinecone before running the Streamlit app
store_business_context_embeddings()  # Store general business contexts

# Initialize the business handler for mock data
business_data_handler = BusinessDataHandler()
business_data_handler.load_mock_data('D:\\RAGHackathon\\MOCK_DATA.csv')  # Load mock data from a CSV
business_data_handler.embed_and_store_mock_data()  # Embed and store mock data in Pinecone

# Load pre-trained model (like GPT-4) for question-answering
question_answering_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Streamlit UI
st.title("NexQ - Enterprise RAG-powered Business Decision Assistant")

# Input for user's question
user_query = st.text_input("Ask a business-related question:")

# Check if the user input is a greeting
greeting_response = check_greeting(user_query)
if greeting_response:
    st.write(greeting_response)
else:
    # Query Pinecone for the most relevant context based on the user query
    context_response = query_context_from_pinecone(user_query)
    
    # Query mock data if needed
    mock_data_response = business_data_handler.query_mock_data(user_query)
    
    if user_query:
        # Get the answer from the question-answering model using the retrieved context
        answer = question_answering_model(question=user_query, context=mock_data_response)
        st.write(f"Answer: {answer['answer']}")
