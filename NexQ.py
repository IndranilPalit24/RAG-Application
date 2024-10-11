from transformers import pipeline
import streamlit as st
from UIHandler import display_ui, display_title, display_action_buttons  # Import necessary functions
from greetingHandler import check_greeting
from businessHandler import BusinessDataHandler
from dataAnalyze import SalesDataHandler
from businessContext import store_business_context_embeddings 
from queryHandler import QueryHandler

# Load local CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
local_css("PageStyling/style.css")

# Store the embeddings into Pinecone before running the Streamlit app
store_business_context_embeddings()

# Initialize the business and sales handlers
business_handler = BusinessDataHandler()
sales_handler = SalesDataHandler('sales_data_sample.csv')

# Initialize QueryHandler to manage business-related data queries
query_handler = QueryHandler('Data/sales_data_sample.csv') # Path to your mock data
                                                              
# Load pre-trained model for question answering
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Function to load the mock data
def load_mock_data():
    try:
        print("Loading mock data...")
        business_handler.load_mock_data('D:\\RAGHackathon\\sales_data_sample.csv')  # Load mock data from a CSV
        print("Mock data loaded.")
        business_handler.embed_and_store_mock_data()  # Embed and store mock data in Pinecone
        print("Mock data embedded and uploaded to Pinecone!")
        st.session_state['data_loaded'] = True  # Mark data as loaded
    except Exception as e:
        print(f"Error during data loading: {e}")
        st.session_state['data_loaded'] = False

# Initialize session state for loading status, conversation, and widget counter if not already set
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False
    load_mock_data()  # Load the data directly without threading

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Initialize the widget counter in session state
if 'widget_counter' not in st.session_state:
    st.session_state['widget_counter'] = 0

# Display the title and introductory message
display_title()

# Check if data is loaded
if not st.session_state['data_loaded']:
    # Display loading message
    st.write("Loading data, please wait...")

else:
    # Once data is loaded, display the conversation and input box
    st.session_state['widget_counter'] += 1  # Increment widget counter before calling display_ui
    user_question = display_ui(st.session_state['conversation'], unique_key=f"user_input_{st.session_state['widget_counter']}")

    if user_question:
        # Check for greeting first
        greeting_response = check_greeting(user_question)
        if greeting_response:
            # Append the greeting response to the conversation
            st.session_state['conversation'].append(("system", greeting_response))
        else:
            # Handle specific queries for sales and finance using QueryHandler
            if "sales growth" in user_question.lower():
                # Example: extracting data from Q1 to Q2
                sales_growth = query_handler.get_sales_growth('Q1', 'Q2')
                st.session_state['conversation'].append(("system", sales_growth))

            elif "sales for q1" in user_question.lower():
                # Example: getting sales data for Q1
                sales_for_q1 = query_handler.get_sales_for_quarter('Q1')
                st.session_state['conversation'].append(("system", sales_for_q1))

            elif "finance" in user_question.lower():
                # Example: fetching finance data
                finance_data = query_handler.get_finance_overview()
                st.session_state['conversation'].append(("system", finance_data))
            else:
                # Handle other non-sales, non-finance queries
                st.session_state['conversation'].append(("user", user_question))

        # Clear input after submission and display the updated conversation
        st.session_state['user_input'] = ""

        # Increment widget counter and display the conversation again
        st.session_state['widget_counter'] += 1  
        display_ui(st.session_state['conversation'], unique_key=f"conversation_display_{st.session_state['widget_counter']}")

# Call the function to display buttons
display_action_buttons(st.session_state)
