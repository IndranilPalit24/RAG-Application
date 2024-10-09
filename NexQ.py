from transformers import pipeline
import streamlit as st
from UIHandler import display_ui  # Import UIHandler for UI management
from greetingHandler import check_greeting
from businessContext import query_context_from_pinecone, store_business_context_embeddings
from businessHandler import BusinessDataHandler
import threading
import time
from dataAnalysis import SalesDataHandler

# Load local CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
local_css("PageStyling/style.css")

# Store the embeddings into Pinecone before running the Streamlit app
store_business_context_embeddings()

# Initialize the business handler for mock data
business_handler = BusinessDataHandler()

# Load pre-trained model for question answering (move this outside of any conditions)
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Define a function to load the mock data in a separate thread
def load_data_in_background(business_handler):
    try:
        print("Loading mock data...")
        business_handler.load_mock_data('D:\\RAGHackathon\\sales_data_sample.csv')  # Load mock data from a CSV
        print("Mock data loaded.")
        business_handler.embed_and_store_mock_data()  # Embed and store mock data in Pinecone
        print("Mock data embedded and uploaded to Pinecone!")
        st.session_state['data_loaded'] = True
        print("Data Loaded Succesfully")
        st.rerun()  # Rerun the Streamlit app to reflect the change
    except Exception as e:
        print(f"Error during data loading: {e}")
        st.session_state['data_loaded'] = False


# Initialize session state for loading status
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False

    # Start loading the data and refresh the UI
if not st.session_state['data_loaded']:
    load_data_in_background(business_handler)
    st.write("Data loaded! Refreshing...")
    time.sleep(1)  # Wait for a second to allow data loading
    st.rerun()  # Trigger rerun

# Initialize session state for conversation history if not already initialized
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Start loading the data in the background if not already loaded
if not st.session_state['data_loaded']:
    if 'thread_started' not in st.session_state:
        st.session_state['thread_started'] = True
        threading.Thread(target=load_data_in_background, args=(business_handler,)).start()
    st.write("Loading data, please wait...")

# Once the data is loaded, show the main interface
if st.session_state['data_loaded']:
    # Display the UI and get the user input
    user_question = display_ui(st.session_state['conversation'])

    # Handling user input
    if user_question:
        # Add user question to chat history
        st.session_state['conversation'].append(("user", user_question))

        # Check for greeting
        greeting_response = check_greeting(user_question)
        if greeting_response:
            st.session_state['conversation'].append(("system", greeting_response))
        else:
            # Query Pinecone for context
            context = query_context_from_pinecone(user_question)

            # Query mock data if necessary
            mockup_data_response = business_handler.query_mock_data(user_question)

            # Get the answer from the QA model using the retrieved context
            if mockup_data_response:
                result = qa_model(question=user_question, context=mockup_data_response)
                bot_response = result['answer']
                st.session_state['conversation'].append(("system", bot_response))
            else:
                st.session_state['conversation'].append(("system", "No metadata available in the top match. Refresh to continue."))

         # Clear input after submission and display the updated conversation
        st.session_state['user_input'] = ""

        # Display the updated conversation
        display_ui(st.session_state['conversation'])


        # Clear the text box on refresh
        if st.button("Refresh"):
            st.session_state['conversation'] = []
            st.rerun()