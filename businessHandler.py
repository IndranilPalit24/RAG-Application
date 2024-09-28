# businessHandler.py

import pandas as pd
from pineCone import index, model  # Use existing Pinecone index and model

class BusinessDataHandler:
    def __init__(self):
        self.index = index  # Use the existing index
        self.model = model  # Use the existing model

    def load_mock_data(self, file_path):
        """Load mock data from CSV using pandas"""
        self.data = pd.read_csv(file_path)
        print(f"Data Loaded: {self.data.head()}")

    def embed_and_store_data(self):
        """Convert each row of mock data into embeddings and store them in Pinecone."""
        for idx, row in self.data.iterrows():
            row_str = ' '.join(str(row[col]) for col in self.data.columns)
            embedding = self.model.encode(row_str).tolist()
            self.index.upsert([(str(idx), embedding, {"row_data": row_str})])
        print("Mock data embedded and uploaded to Pinecone!")

    def query_data(self, query_text):
        """Query Pinecone with a user question to retrieve relevant business data."""
        query_embedding = self.model.encode(query_text).tolist()
        result = self.index.query(vector=query_embedding, top_k=1)
        if result['matches']:
            top_match = result['matches'][0]['metadata']['row_data']
            return top_match
        return "No relevant data found."
