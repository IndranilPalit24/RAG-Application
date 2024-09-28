from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Initialize the model
#model = SentenceTransformer('all-mpnet-base-v2')

model = SentenceTransformer('all-MiniLM-L6-v2')

pc = Pinecone(api_key="6162b032-d14f-4fa7-8807-02236f7b3e42")
# Connect to the index you created
index = pc.Index("enterprise-rag-data")



