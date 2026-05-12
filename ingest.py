import os
import shutil
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents():
    print("--- Starting deep search in 'data' folder and subdirectories ---")
    docs = []
    data_path = "./data"

    if not os.path.exists(data_path):
        print(f"ERROR: The directory '{data_path}' does not exist!")
        return []

    # os.walk iterates through the data folder AND the projects subfolder
    for root, dirs, files in os.walk(data_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            try:
                # 1. TEXT and MARKDOWN (experiences, skills, and the 14 project files)
                if file.endswith((".txt", ".md")):
                    print(f"Loading Text/Markdown: {file_path}")
                    loader = TextLoader(file_path, encoding='utf-8')
                    docs.extend(loader.load())
                
                # 2. PDF (Your CV)
                elif file.endswith(".pdf"):
                    print(f"Loading PDF: {file_path}")
                    loader = PyPDFLoader(file_path)
                    docs.extend(loader.load())
                    
            except Exception as e:
                print(f"Error processing {file}: {e}")

    print(f"\n--- DONE! Total documents loaded: {len(docs)} ---")
    return docs

def create_vector_db():
    # Clear old database for a fresh start
    db_path = "./chroma_db"
    if os.path.exists(db_path):
        print("Removing old vector database...")
        shutil.rmtree(db_path)

    # 1. Load all files
    docs = load_documents()
    if not docs:
        print("No documents found. Aborting.")
        return
    
    # 2. Chunking (1000 chars to keep project details and work history together)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)
    
    # 3. Vectorization (Embeddings)
    print(f"Vectorizing {len(splits)} chunks...")
    embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"), 
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    embeddings.additional_headers = {"X-Wait-For-Model": "true"}

    # 4. Save to ChromaDB
    vector_db = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=db_path
    )
    print(f"Success! The AI now has access to the CV and all 14 projects in '{db_path}'.")

if __name__ == "__main__":
    create_vector_db()