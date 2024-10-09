from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Initialize the model
sentence_embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Pinecone with API key
pinecone_client = Pinecone(api_key="6162b032-d14f-4fa7-8807-02236f7b3e42")

# Connect to the index
business_index = pinecone_client.Index("enterprise-rag-data")
