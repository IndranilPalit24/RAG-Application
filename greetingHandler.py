from fuzzywuzzy import fuzz

def check_greeting(user_input):
    """Check if the user input is a greeting"""
    greetings = ["hello", "hi", "hey"]

    # Check if user input is similar to known greetings
    for greeting in greetings:
        if fuzz.ratio(user_input.lower(), greeting) > 80:  # If similarity is more than 80%
            return "Hello! How can I assist you with business decisions today?"
    
    return None
