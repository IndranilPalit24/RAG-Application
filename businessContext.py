from transformers import pipeline

# Load a pre-trained model for text classification
classifier = pipeline("zero-shot-classification")

# Define potential business categories and their contexts
category_contexts = {
    "finance": "This is the finance context for decision-making, covering budgeting, forecasting, and financial analysis.",
    "operations": "This is the operations context, covering supply chain management, logistics, and resource optimization.",
    "strategy": "This is the strategy context for helping with business growth, competition analysis, and long-term planning.",
    "marketing": "This is the marketing context, covering customer outreach, campaign performance, and brand growth.",
    "sales": "This is the sales context, covering sales pipeline management, deal closure, and revenue generation.",
    "human resources": "This is the HR context, covering employee management, recruitment strategies, and talent retention."
}

def get_business_context(user_question):
    # Check if the user input is empty or None
    if not user_question.strip():
        return "Please ask a valid business-related question."

    # Classify the user's question into one of the business categories
    result = classifier(user_question, list(category_contexts.keys()))
    
    # Get the top predicted category
    top_category = result['labels'][0]
    
    # Fetch the context directly from the dictionary
    return category_contexts.get(top_category, "Enterprise RAG helps businesses retrieve augmented information for decision-making.")
