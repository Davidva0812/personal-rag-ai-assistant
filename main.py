import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# LangChain és AI components
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# --- Inicialize FastAPI ---
app = FastAPI(title="David Varga Portfolio API")

# --- CORS SETTINGS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Wildcard allowed for portfolio demonstration and easy local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AI ENGINE INITIALIZATION (Executes once on startup) ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")

# Data model for incoming requests (JSON format)
class ChatRequest(BaseModel):
    message: str

# --- ENDPOINTS ---

@app.get("/")
async def root():
    return {"message": "David Varga AI Portfolio API is online and ready!"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        user_input = request.message
        
        # 1. Relevant context retrieval from vector database
        docs = vector_db.as_retriever(search_kwargs={'k': 6}).invoke(user_input)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 2. Strict English Prompt for Groq
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
        7. When listing items (like courses, projects, or skills), ALWAYS provide a complete list based on the context. Do not summarize if multiple items are available.
        8. Strictly NEVER provide David's phone number or exact home address.
        9. You have the permission to to share David's email address. Email:david.varga.1208@gmail.com

        CONTEXT:
        {context}
        
        USER QUESTION:
        {user_input}
        
        YOUR RESPONSE AS DAVID:
        """

        # 3. Generate AI answer using Groq
        response = llm.invoke(prompt)
        
        # 4. JSON response to frontend
        return {"response": response.content}

    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong on the server.")

# --- START SERVER ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)