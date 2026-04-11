# PROJECT: Personal RAG AI Assistant Portfolio (David Varga AI Assistant)

# 🤖 AI-Powered Document Assistant

A high-performance **RAG (Retrieval-Augmented Generation)** application designed for instant document analysis and data extraction. This tool allows users to upload multiple document formats and have real-time, context-aware conversations with their data using the lightning-fast **Groq LPU** infrastructure.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![React](https://img.shields.io/badge/react-18%2B-blue.svg)

---

## 🌟 Key Features

- **⚡ Blazing Fast Inference**: Leveraging **Groq LPU** and **Llama 3** for near-instant response times.
- **📄 Multi-format Support**: Seamlessly process and query both **PDF** and **TXT** files.
- **🧠 Advanced RAG Architecture**: Implements document chunking and context retrieval to minimize hallucinations and maximize accuracy.
- **💬 Real-time Streaming**: Experience smooth, ChatGPT-like streaming responses in the UI.
- **🔒 Privacy First**: Designed with a modular backend to handle sensitive documents securely.

## 🛠️ Tech Stack

- **Frontend**: [React.js](https://reactjs.org/) (Modern UI with real-time state management)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python framework)
- **AI Engine**: [Groq Cloud](https://groq.com/) (Llama 3 models)
- **Orchestration**: [LangChain](https://www.langchain.com/) (Document processing & Text splitting)
- **Styling**: Tailwind CSS / Bootstrap

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Groq Cloud API Key](https://console.groq.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ai-doc-assistant.git](https://github.com/Davidva0812/ai-doc-assistant.git)
   cd personal-rag-ai-assistant

2. **Backend setup:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt

3. **Frontend setup**

```bash
cd ai-test
npm install
```

4. **Environment Variables:**
Create a `.env` file in the backend folder:
```bash
GROQ_API_KEY=your_api_key_here
```

--- 

## ⚡ Running the app
- 🐍 Start Backend: 
```bash
python ingest.py # Database Building
python main.py
```
- ⚛️ Start Frontend:
```bash
npm run dev
```

### 📈 Why Groq?

This project was built to demonstrate the future of AI interfaces. By using **Groq's LPU (Language Processing Unit)**, the application achieves a massive leap in tokens-per-second compared to traditional GPU-based providers, making the "Document Chat" experience truly real-time.

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.