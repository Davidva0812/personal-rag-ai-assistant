import os
import shutil
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings # Frissített import
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents():
    print("--- Adatok keresése... ---")
    docs = []
    data_path = "./data"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith((".txt", ".md")):
                    loader = TextLoader(file_path, encoding='utf-8')
                    docs.extend(loader.load())
                elif file.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    docs.extend(loader.load())
            except Exception as e:
                print(f"Hiba ({file}): {e}")
    return docs

def create_vector_db():
    db_path = "./chroma_db"
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    docs = load_documents()
    if not docs: return
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    print(f"Vektorizálás helyi CPU-val ({len(splits)} egység)...")
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_db = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=db_path
    )
    print("\n✅ SIKER! A 'chroma_db' mappa elkészült.")

if __name__ == "__main__":
    create_vector_db()