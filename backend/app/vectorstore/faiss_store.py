import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Embedding model
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Step 1: Chunk large text into smaller overlapping sections
def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.create_documents([text])  # returns a list of Document objects

# Step 2: Create a FAISS index and save it to disk
def create_faiss_index(text: str, index_path: str = "data/index"):
    docs = chunk_text(text)  # 1. Split text into chunks
    db = FAISS.from_documents(docs, embeddings)  # 2. Embed and store chunks
    db.save_local(index_path)  # 3. Save index to disk
    return f"Indexed {len(docs)} chunks to {index_path}"
