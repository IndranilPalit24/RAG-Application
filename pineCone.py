# pineCone.py
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Initialize the model
sentence_embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Pinecone setup
pinecone_client = Pinecone(api_key="<Your_API__Key>")
business_index = pinecone_client.Index("enterprise-rag-data")

