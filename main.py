import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# LangChain és AI components - FRISSÍTETT IMPORTOK
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpointEmbeddings # Ezt használjuk az API-hoz
from langchain_community.vectorstores import Chroma

load_dotenv()

# --- Inicialize FastAPI ---
app = FastAPI(title="David Varga Portfolio API")

# --- CORS SETTINGS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://davidva0812.github.io",
        "http://localhost:3000",  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AI ENGINE INITIALIZATION ---

# Ellenőrizzük, hogy létezik-e az adatbázis (amit te már feltöltöttél GitHubra)
db_path = "./chroma_db"
if not os.path.exists(db_path):
    print(f"CRITICAL ERROR: {db_path} NOT FOUND!")
else:
    print("Database folder found, loading...")

# Az API alapú embedding beállítása (ez nem eszi meg a RAM-ot!)
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

# Vektoradatbázis betöltése (Csak olvassa a meglévő mappát)
vector_db = Chroma(
    persist_directory=db_path, 
    embedding_function=embeddings
)

# Groq LLM beállítása
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

class ChatRequest(BaseModel):
    message: str

# --- ENDPOINTS ---

@app.get("/")
async def root():
    return {"message": "David Varga AI Portfolio API is online!"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        user_input = request.message
        
        # 1. Releváns részek keresése az adatbázisban
        docs = vector_db.as_retriever(search_kwargs={'k': 5}).invoke(user_input)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 2. Prompt összeállítása
        prompt = f"""
        SYSTEM INSTRUCTION:
        You are David Varga, a Junior Developer. Answer the question in the FIRST PERSON ("I...").
        Base your answers ONLY on the provided Context. 
        Your goal is to help recruiters.
        
        CRITICAL RULES:
        1. 'Gerilla Mentor Klub', 'Udemy', 'Cisco', 'Google', 'freeCodeCamp' and 'Mimo' are EDUCATION, not work experience.
        2. Professional experience must include a COMPANY NAME.
        3. If the information is missing, say: "I'm sorry, I haven't included that specific detail in my records yet."
        4. Do NOT repeat yourself. Be concise.
        5. Answer in ENGLISH.
        6. If the question is unrelated to your CV, politely decline and say: "I'm sorry, I can only answer questions related to my CV and projects."
        7. When listing items (like courses, projects, or skills), ALWAYS provide a complete list based on the context.
        8. Strictly NEVER provide David's phone number or exact home address.
        9. David's email: david.varga.1208@gmail.com

        CONTEXT:
        {context}
        
        USER QUESTION:
        {user_input}
        
        YOUR RESPONSE AS DAVID:
        """

        # 3. Válasz generálása
        response = llm.invoke(prompt)
        return {"response": response.content}

    except Exception as e:
        print(f"Server Error: {e}")
        # Részletesebb hibaüzenet a logba
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)