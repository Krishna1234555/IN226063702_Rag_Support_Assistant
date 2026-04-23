import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

def ingest_pdf(file_path: str, persist_directory: str = DB_DIR):
    """
    Loads a PDF, splits it into chunks, and stores embeddings in ChromaDB.
    """
    print(f"Loading document: {file_path}")
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    print(f"Loaded {len(docs)} pages. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)
    print(f"Created {len(splits)} chunks.")

    print("Generating embeddings and saving to ChromaDB...")
    
    # We use local HuggingFace embeddings to avoid API key/versioning issues.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f"Successfully ingested and persisted to {persist_directory}")
    return vectorstore

if __name__ == "__main__":
    # Example usage:
    # Set your API key first: set GOOGLE_API_KEY=your_key
    # python ingest.py
    sample_pdf = os.path.join(BASE_DIR, "data", "TechNova_Policies.pdf")
    if not os.path.exists(sample_pdf):
        print(f"Please run 'python generate_sample_pdf.py' first to create {sample_pdf}.")
    else:
        ingest_pdf(sample_pdf)
