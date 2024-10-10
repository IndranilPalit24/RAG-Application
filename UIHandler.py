import streamlit as st

def display_ui(chat_history, unique_key):
    """Handles the display of the chat interface, including the input box and chat history."""
    st.write("How can I assist you today?")  # Remove the redundant title here

    # Display chat history
    for role, message in chat_history:
        if role == "user":
            st.write(f"**You:** {message}")
        else:
            st.write(f"**NexQ:** {message}")

    # Input field with unique key
    user_input = st.text_input("Type your question here:", key=unique_key, placeholder="Type your question here...")

    # Send button to submit input
    #send_button_clicked = st.button("Send", key=f"send_button_{unique_key}")

    # Return both user input and the status of the send button click
    #return user_input if send_button_clicked else None

def display_title():
    """Displays the title of the application."""
    st.write("## NexQ - Enterprise RAG-powered Business Decision Assistant")  # Keep the title in a separate function

def display_action_buttons(session_state):
    """Display action-based buttons below the chat input."""
    
    action_col1, action_col2, action_col3, action_col4, action_col5, action_col6, action_col7 = st.columns(7)
    with action_col1:
        if st.button("Sales", key="check_sales"):
            session_state['conversation'].append(("system", "Fetching sales data..."))
    with action_col2:
        if st.button("Finance", key="show_finance"):
            session_state['conversation'].append(("system", "Fetching finance overview..."))

    with action_col3:
        if st.button("Ops", key="run_ops"):
            session_state['conversation'].append(("system", "Running Operations Update..."))

    with action_col4:
        if st.button("Market", key="run_marketing"):
            session_state['conversation'].append(("system", "Fetching Marketing data..."))

    with action_col5:
        if st.button("Strategy", key="run_strategy"):
            session_state['conversation'].append(("system", "Running Strategy..."))

    with action_col6:
        if st.button("Analytics", key="run_analysis"):
            session_state['conversation'].append(("system", "Fetching Recent Analytics..."))

    with action_col7:
        if st.button("HR", key="human_resource"):
            session_state['conversation'].append(("system", "Human Resources Data ..."))

    #display_ui(session_state['conversation'], unique_key="conversation_display")

