# (NexQ) A RAG Application - Business Decision Assistant Using Retrieval-Augmented Generation

This project implements an Enterprise Business Decision Assistant using Retrieval-Augmented Generation (RAG) with a large language model (LLM). The assistant helps business users make informed decisions by retrieving context-aware information based on specific domains like finance, marketing, operations, etc. Built using Streamlit and Hugging Face's Transformers, the application supports real-time Q&A interactions with user-friendly responses. The repository is a prototype for an AI-powered tool to aid enterprise-level decision-making.


![NexQ](https://github.com/user-attachments/assets/b7977a17-7a7d-4c1c-aebe-85570eba340a)

## 1. Data Warehouse
The Data Warehouse stores various data sources, including business-specific documents, reports, videos, and other formats. It is where all business data resides before being processed.

## 2. Document Loader and Text Splitter
The Document Loader and Text Splitter are responsible for loading documents from different data sources, such as PDFs, TXT files, or even video transcriptions, and splitting them into smaller, manageable chunks called Text Chunks. This allows for easier processing and better embedding representation.

## 3. Text Chunks
These Text Chunks are smaller sections of the original documents, each representing a portion of business data that can be processed and embedded into vector representations. The chunks are created to make searching more efficient and to allow the system to handle specific parts of documents.

## 4. Embeddings Generation Model
The Embeddings Generation Model uses a pre-trained model, such as Sentence Transformers, to convert the Text Chunks into numeric embeddings. These embeddings represent the meaning of the text in a format that can be processed by computers. The embeddings are then stored in a Vector Database.

## 5. Vector Databases
The Vector Database (in this case, Pinecone) stores the embeddings generated from the Text Chunks. This database is essential for quickly finding similar pieces of text based on user queries. Each text chunk, along with metadata like the document type and context, is stored as an embedding in the vector database.

## 6. User Query
The User interacts with the system via a UI, such as the Streamlit interface. The user inputs a query, which could be a business-related question like "What are the sales figures for Q1?" This query is then processed to understand the user's intent.

## 7. Embeddings Generation Model - Query Embedding
The Embeddings Generation Model also generates an embedding for the user's query. This embedding represents the query in the same vector space as the Text Chunks, allowing for comparison and similarity search.

## 8. Similarity Search
The Similarity Search component searches through the Vector Database for embeddings that are similar to the user's query. The search is based on a similarity score, and it retrieves the Top K Matches that are most relevant to the user's query.

## 9. Top K Matches
Once the top matches are retrieved from the Vector Database, they are passed on to the Large Language Model (LLM) to generate a coherent and context-aware response.

## 10. LLM (Large Language Model)
The LLM (like GPT-4) uses the context retrieved from the Vector Database to provide an answer to the user's question. This LLM is fine-tuned to generate human-like responses based on the relevant data found.

## 11. User Interface (UI)
The User Interface (e.g., Streamlit) is responsible for displaying the question and answer as part of a back-and-forth conversation. It also handles user inputs, and the display of retrieved answers and any error messages if necessary.

## Data Flow Overview:
Data Ingestion: Documents are uploaded from multiple data sources and split into chunks.
Embeddings Generation: The Embeddings Generation Model processes the chunks to generate embeddings.
Storing in Vector Database: The embeddings are stored in the Vector Database.
User Query: A user enters a question through the UI.
Query Embedding: The Embeddings Generation Model converts the user's question into an embedding.
Similarity Search: The system searches the Vector Database for relevant embeddings based on the query embedding.
Top Matches Retrieval: The top-matching data chunks are retrieved.
Answer Generation: The LLM generates an answer using the top-matching context retrieved.
User Response Display: The response is displayed in the UI, and the user can continue the conversation.
