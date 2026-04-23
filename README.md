# 🚀 RAG-Based Customer Support Assistant  
### Using LangGraph & Human-in-the-Loop (HITL)

## 📌 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** based Customer Support Assistant designed to answer user queries using information stored in a PDF knowledge base.

The system retrieves relevant information from documents using vector embeddings and generates contextual responses using a Large Language Model (LLM). If the system is unable to confidently answer a query, it escalates the request to a **Human-in-the-Loop (HITL)** for manual resolution.

This project demonstrates system design thinking using **LangGraph workflows**, semantic retrieval, and intelligent routing.

---

## 🎯 Project Objectives

- Process a PDF knowledge base
- Split documents into meaningful chunks
- Generate embeddings using transformer models
- Store embeddings in ChromaDB
- Retrieve relevant context using semantic search
- Generate answers using LLM
- Implement graph-based workflow using LangGraph
- Support Human-in-the-Loop (HITL) escalation
- Simulate real-world customer support automation

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)** is an AI architecture that combines:

1. **Retrieval System** → Fetches relevant document context  
2. **Generation System** → Generates answers using retrieved context  

Instead of relying only on model memory, RAG retrieves real data from documents, making responses:

- More accurate
- Context-aware
- Updatable without retraining

---

## 🏗️ System Architecture

```

User Query
↓
User Interface (CLI / Web UI)
↓
LangGraph Workflow
↓
Query Processing Node
↓
Retriever (ChromaDB)
↓
LLM Response Generator
↓
Confidence Check
├── High Confidence → Send Response
└── Low Confidence → HITL Escalation
↓
Human Agent
↓
Final Response

```

### Document Ingestion Pipeline

```

PDF → Loader → Chunking → Embedding → ChromaDB

```

---

## ⚙️ Technologies Used

| Component | Technology |
|----------|-------------|
| Programming Language | Python |
| Framework | LangChain |
| Workflow Engine | LangGraph |
| Vector Database | ChromaDB |
| Embedding Model | SentenceTransformers |
| PDF Loader | PyPDFLoader |
| LLM | Groq / Ollama |
| UI | Streamlit |
| Environment | Python Virtual Environment |

---

## 📂 Project Structure

```

rag_customer_support/
│
├── data/
│   └── ecommerce_policy.pdf
│
├── vectordb/
│
├── ingest.py
├── retriever.py
├── llm.py
├── graph.py
├── hitl.py
├── app.py
│
├── requirements.txt
├── README.md
└── .env

```

---

## 🔄 Workflow Explanation

### Step 1 — Document Ingestion

- Load PDF file
- Split into chunks
- Generate embeddings
- Store embeddings in ChromaDB

File:

```

ingest.py

```

---

### Step 2 — Retrieval

- User query converted into embedding
- Similar chunks retrieved from ChromaDB
- Top-k results selected

File:

```

retriever.py

```

---

### Step 3 — Response Generation

- Retrieved chunks sent to LLM
- Context-aware response generated

File:

```

llm.py

```

---

### Step 4 — Workflow Execution (LangGraph)

LangGraph manages:

- Input handling
- Query processing
- Conditional routing
- HITL escalation

File:

```

graph.py

```

---

### Step 5 — Human-in-the-Loop (HITL)

Escalation triggered when:

- No relevant chunks found
- Low confidence response
- Complex query detected

File:

```

hitl.py

```

---

## 🧪 Sample Queries

Try queries like:

```

What is the return policy?
How long does shipping take?
Can I cancel my order?
When will I get refund?

```

---

## 🚨 Error Handling

System handles:

- Missing PDF files
- Empty queries
- No relevant chunks found
- LLM response failure
- Vector DB loading issues

---

## 📊 Key Features

✅ Retrieval-Augmented Generation (RAG)  
✅ Vector Database (ChromaDB)  
✅ Graph-Based Workflow (LangGraph)  
✅ Conditional Routing  
✅ Human-in-the-Loop Escalation  
✅ Scalable Modular Design  

---

## 📈 Scalability Considerations

- Efficient chunk indexing
- Top-k retrieval optimization
- Vector caching
- Parallel query handling
- Modular system architecture

---

## 🧪 Testing Strategy

System tested using:

- Policy-based queries
- Edge case queries
- Unknown queries
- Complex queries

Example test cases:

```

Query: What is refund time?
Expected: Refund processed within 5–7 days.

Query: I received a damaged item
Expected: Report within 48 hours.

````

---

## ⚖️ Challenges & Trade-offs

| Challenge | Solution |
|----------|----------|
| Chunk Size Selection | Used overlap strategy |
| Retrieval Accuracy | Top-k tuning |
| Latency | Efficient indexing |
| Context Quality | Balanced chunk length |

---

## 🔮 Future Enhancements

- Multi-document support
- Multi-language support
- Feedback learning loop
- Web deployment
- Database integration
- User authentication
- Chat memory support

---

## ▶️ How to Run the Project

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
````

---

### Step 2 — Add PDF

Place PDF inside:

```
data/ecommerce_policy.pdf
```

---

### Step 3 — Run Ingestion

```bash
python ingest.py
```

---

### Step 4 — Test Retrieval

```bash
python retriever.py
```

---

### Step 5 — Run Application

```bash
python app.py
```

OR

```bash
streamlit run app.py
```

---

## 👨‍💻 Author

**Krishna Birajdar**
AI Internship Project
RAG-Based Customer Support Assistant

---

## 📜 License

This project is developed for educational and internship purposes.

````

---

# What You Should Do Now

1. Create file:



2. Paste the content
3. Save it inside your project folder

---

# Next Recommended Step

We should now build:

✅ **llm.py**
(Connect Retriever → LLM → Answer)

After that:

* graph.py (LangGraph workflow)
* hitl.py
* app.py (Final chatbot)
