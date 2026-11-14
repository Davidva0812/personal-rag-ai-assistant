import os
import time
import shutil

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DATA_PATH = "./data"
DB_PATH = "./chroma_db"

# FONTOS: ugyanannak kell lennie, mint a main.py-ban (EMBEDDING_MODEL)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

# Az ingyenes keret: 100 embedding kérés / perc, és minden szövegrész külön kérés.
# 10 chunk / 8 mp = kb. 75 kérés / perc, ami biztonságosan a limit alatt van.
BATCH_SIZE = 10
PAUSE_SECONDS = 8
RATE_LIMIT_WAIT = 65   # ennyit várunk, ha 429-es (kvóta) hibát kapunk
MAX_RETRIES = 5


def load_documents():
    print("--- Adatok keresése... ---")
    docs = []
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith((".txt", ".md")):
                    loader = TextLoader(file_path, encoding="utf-8")
                    docs.extend(loader.load())
                elif file.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    docs.extend(loader.load())
            except Exception as e:
                print(f"Hiba ({file}): {e}")
    return docs


def is_rate_limit_error(error):
    text = str(error)
    return "429" in text or "RESOURCE_EXHAUSTED" in text


def add_in_batches(vector_db, splits):
    total = len(splits)
    for start in range(0, total, BATCH_SIZE):
        batch = splits[start:start + BATCH_SIZE]
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Az embedding a mentés ELŐTT történik, ezért egy hibás batch
                # nem kerül be félig az adatbázisba, az újrapróbálás biztonságos.
                vector_db.add_documents(batch)
                break
            except Exception as e:
                if attempt == MAX_RETRIES:
                    raise
                if is_rate_limit_error(e):
                    wait = RATE_LIMIT_WAIT
                    print(f"Elértük a percenkénti limitet, várok {wait} mp-et...")
                else:
                    wait = PAUSE_SECONDS * (2 ** attempt)
                    print(f"Hiba ({e}); újrapróbálom {wait} mp múlva...")
                time.sleep(wait)
        print(f"  {min(start + BATCH_SIZE, total)}/{total} egység kész")
        time.sleep(PAUSE_SECONDS)


def create_vector_db():
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Hiányzik a GEMINI_API_KEY (.env fájl vagy környezeti változó).")
        return

    # A régi (félig kész vagy MiniLM-es) adatbázist törölni kell
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    docs = load_documents()
    if not docs:
        print("❌ Nem találtam dokumentumot a ./data mappában.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)

    print(f"Vektorizálás Gemini embeddinggel ({len(splits)} egység, modell: {EMBEDDING_MODEL})...")
    print("Ez a limit miatt 2-3 percig is eltarthat, ne szakítsd meg.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    add_in_batches(vector_db, splits)

    print("\n✅ SIKER! A 'chroma_db' mappa elkészült.")


if __name__ == "__main__":
    create_vector_db()