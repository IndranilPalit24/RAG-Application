from transformers import pipeline
from pineCone import sentence_embedding_model,business_index

# Load a pre-trained sentence_embedding_model for text classification
classifier = pipeline("zero-shot-classification")

# Define potential business categories and their contexts
business_contexts = {
    "finance": "This is the finance context for decision-making, covering budgeting, forecasting, and financial analysis.",
    "operations": "This is the operations context, covering supply chain management, logistics, and resource optimization.",
    "strategy": "This is the strategy context for helping with business growth, competition analysis, and long-term planning.",
    "marketing": "This is the marketing context, covering customer outreach, campaign performance, and brand growth.",
    "sales": "This is the sales context, covering sales pipeline management, deal closure, and revenue generation.",
    "human_resources": "This is the HR context, covering employee management, recruitment strategies, and talent retention."
}

def store_business_context_embeddings():
    """Store predefined business context embeddings into Pinecone"""
    for category, context in business_contexts.items():
        # Convert context into embeddings
        embedding_vector = sentence_embedding_model.encode(context).tolist()
        
        # Upsert to Pinecone (ID is the category name)
        try:
            business_index.upsert([(category, embedding_vector, {"category": category, "context": context})])
        except Exception as error:
            print(f"Error upserting {category}: {str(error)}")

def query_context_from_pinecone(user_input):
    """Query Pinecone for general business contexts based on user input"""
    query_embedding_vector = sentence_embedding_model.encode(user_input).tolist()
    search_results = business_index.query(vector=query_embedding_vector, top_k=5, include_metadata=True)
    print(f"Query result: {search_results}")

    if search_results['matches']:
        print(f"Metadata: {search_results['matches'][0]['metadata']}")
        return "Metadata displayed in console."
    else:
        return "No relevant context found."
