import pandas as pd
from pineCone import business_index, sentence_embedding_model  # Use existing Pinecone business_index and sentence_embedding_model
import concurrent.futures

class BusinessDataHandler:
    def __init__(self):
        self.business_index = business_index  # Use the existing business_index
        self.sentence_embedding_model = sentence_embedding_model  # Use the existing sentence_embedding_model

    def load_mock_data(self, csv_file_path):
        """Load mock data from a CSV file using pandas"""
        try:
            self.data = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
            print(f"Data Loaded: {self.data.head()}")
        except Exception as e:
            print(f"Error during data loading: {e}")

    def process_row(self, row):
        """Helper function to process each row and convert it into embeddings."""
        row_text = ' '.join(str(row[col]) for col in self.data.columns)  # Changed to self.data
        embedding_vector = self.sentence_embedding_model.encode(row_text).tolist()
        return (str(row.name), embedding_vector, {"row_data": row_text})

    def embed_and_store_mock_data(self, batch_size=100):
        """Convert each row of mock data into embeddings and store them in Pinecone in batches."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_row, row) for _, row in self.data.iterrows()]  # Changed to self.data
            results = []
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    results.append(future.result())
                    # Upsert data in batches
                    if len(results) >= batch_size:
                        self.business_index.upsert(results)  # Changed to self.index
                        results = []
                except Exception as e:
                    print(f"Error during processing row {i}: {e}")
            
            # Upsert any remaining results
            if results:
                try:
                    self.business_index.upsert(results)  # Changed to self.index
                except Exception as e:
                    print(f"Error during final upsert: {e}")
        
        print("Mock data embedded and uploaded to Pinecone in batches with error handling!")

    def query_mock_data(self, query_text):
        """Query Pinecone with a user question to retrieve relevant business data."""
        query_embedding = self.sentence_embedding_model.encode(query_text).tolist()
        search_result = self.business_index.query(vector=query_embedding, top_k=1)

        # Check if 'matches' is present and has at least one item
        if 'matches' in search_result and len(search_result['matches']) > 0:
            top_match = search_result['matches'][0]
        
        # Check if 'metadata' is present in the top match
            if 'metadata' in top_match and 'row_data' in top_match['metadata']:
                top_match_metadata = top_match['metadata']['row_data']
                return top_match_metadata
            else:
                return "No metadata available in the top match."
        return "No relevant data found."

