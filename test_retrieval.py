import os
import sys

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

print(f"Dokumentumok az adatbázisban: {vector_db._collection.count()}")

# Használat: python test_retrieval.py "kérdés"  (több kérdés is megadható)
queries = sys.argv[1:] or [
    "Tell me about your experiences",
    "Where did you do your internship?",
]

K = 5

for q in queries:
    print("\n" + "=" * 70)
    print(f"KÉRDÉS: {q}")
    print("=" * 70)
    results = vector_db.similarity_search_with_score(q, k=K)
    for i, (doc, score) in enumerate(results, 1):
        source = doc.metadata.get("source", "?")
        print(f"\n--- #{i} | távolság: {score:.4f} | forrás: {source}")
        print(doc.page_content)