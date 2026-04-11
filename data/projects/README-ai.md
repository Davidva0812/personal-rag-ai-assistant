# 🧠 Semantic Knowledge Base - AI-Powered Document Search

This project is a **Semantic Search Engine** that allows users to query a set of documents based on their actual meaning rather than just keywords. It utilizes state-of-the-art Natural Language Processing (NLP) to understand context and intent.



## 🚀 Key Features

* **Semantic Understanding**: Uses a Transformer-based model (`all-MiniLM-L6-v2`) to find answers based on meaning.
* **Vector Database**: Implements **ChromaDB** for persistent storage of document embeddings, ensuring fast and scalable retrieval.
* **Dynamic Ingestion**: Automatically processes all `.txt` files from a specified directory.
* **Interactive UI**: Built with **Gradio**, providing an intuitive web interface for managing and searching the knowledge base.
* **Local & Private**: Everything runs locally on your machine—no data is sent to external APIs like OpenAI.

## 🛠️ Tech Stack

* **Python**: The core logic.
* **Sentence-Transformers**: For generating high-quality text embeddings.
* **ChromaDB**: Vector Database for semantic storage.
* **Gradio**: Web-based GUI for ease of use.
* **PyTorch**: Backend for model computations.



## 📋 How It Works

1.  **Ingestion**: The system reads `.txt` files and converts them into 384-dimensional vectors (**embeddings**).
2.  **Storage**: These vectors are stored in a local ChromaDB instance.
3.  **Querying**: When a user asks a question, the question is also converted into a vector.
4.  **Matching**: The system calculates the **L2 distance** between the question vector and all document vectors to find the most relevant content.


## 💻 Usage:
1. Place your .txt files into a folder (e.g., ./notes).
2. Open the web interface (usually at http://127.0.0.1:7860).
3. Click "Ingest Documents" to initialize the database.
4. Start searching!

## 🧪 Example Test Case
Document: "Python is widely used in data science and AI development."

Query: "What is the best language for machine learning?"

Result: The system finds the Python document because it understands that "machine learning" and "AI development" are semantically related concepts.

## 📜 License & Legal
This project is open-source and available under the MIT License.

MIT License Highlights:
✅ Commercial use is allowed.
✅ Modification and distribution are permitted.
✅ Private use is allowed.
⚠️ The software is provided "as is", without warranty of any kind.

Copyright (c) 2026 David

Developed as a portfolio project to demonstrate Semantic Search and Vector Database integration.

