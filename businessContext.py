# businessContext.py

from transformers import pipeline
from pineCone import model, index 

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

def store_embeddings_in_pinecone():
    # Store business context embeddings into Pinecone
    for category, context in category_contexts.items():
        # Convert context into embeddings
        embedding = model.encode(context).tolist()
        
        # Upsert to Pinecone (ID is the category name)
        try:
            index.upsert([(category, embedding, {"category": category, "context": context})])
        except Exception as e:
            print(f"Error upserting {category}: {str(e)}")

def query_pinecone_for_context(user_question):
    """Query Pinecone for general business contexts based on user input"""
    query_embedding = model.encode(user_question).tolist()
    result = index.query(vector=query_embedding, top_k=5, include_metadata=True)
    print(f"Query result: {result}")

    if result['matches']:
        print(f"Metadata: {result['matches'][0]['metadata']}")
        return "Metadata displayed in console."
    else:
        return "No relevant context found."
