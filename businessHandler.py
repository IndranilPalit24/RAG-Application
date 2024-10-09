import pandas as pd
from pineCone import index, model  # Use existing Pinecone index and model

class BusinessDataHandler:
    def __init__(self):
        self.index = index  # Use the existing index
        self.model = model  # Use the existing model

    def load_mock_data(self, csv_file_path):
        """Load mock data from a CSV file using pandas"""
        self.mock_data = pd.read_csv(csv_file_path)
        print(f"Data Loaded: {self.mock_data.head()}")

    def embed_and_store_mock_data(self):
        """Convert each row of mock data into embeddings and store them in Pinecone"""
        for row_index, row in self.mock_data.iterrows():
            row_text = ' '.join(str(row[column]) for column in self.mock_data.columns)
            row_embedding_vector = self.model.encode(row_text).tolist()
            self.index.upsert([(str(row_index), row_embedding_vector, {"row_data": row_text})])
        print("Mock data embedded and uploaded to Pinecone!")

    def query_mock_data(self, query_text):
        """Query Pinecone with a user question to retrieve relevant mock business data"""
        query_embedding_vector = self.model.encode(query_text).tolist()
        search_result = self.index.query(vector=query_embedding_vector, top_k=1)
        
        if search_result['matches']:
            top_match_metadata = search_result['matches'][0]['metadata']['row_data']
            return top_match_metadata
        return "No relevant data found."
