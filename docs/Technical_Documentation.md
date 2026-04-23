# Technical Documentation
## RAG-Based Customer Support Assistant

### 1. Introduction

**What is RAG?**
Retrieval-Augmented Generation (RAG) is an AI architecture that enhances the capabilities of a Large Language Model (LLM) by providing it with dynamic, domain-specific data from an external knowledge base. Instead of relying solely on the LLM's pre-trained knowledge, RAG retrieves relevant facts just-in-time to ground the LLM's responses.

**Why is it needed?**
LLMs are prone to "hallucinations" (inventing facts) and lack access to private, company-specific data. RAG solves this by ensuring the LLM only answers based on the provided company manuals, policies, and documents.

**Use Case Overview:**
We are building a Customer Support Assistant. This bot ingests company policy PDFs and assists users. If the bot is unsure or if the user is frustrated, it uses a Human-in-the-Loop (HITL) system to seamlessly pass the conversation to a human agent without losing context.

---

### 2. System Architecture Explanation

The system is built on a multi-stage pipeline:
1. **Offline Ingestion:** PDFs are loaded, split into chunks, embedded, and saved to a ChromaDB vector store.
2. **Online Querying:** When a user asks a question, the LangGraph orchestrator intercepts it.
3. **Graph Execution:**
   - The State (containing chat history) is updated.
   - A router determines if context retrieval is necessary.
   - If yes, ChromaDB is queried. The top results are appended to the State.
   - The LLM synthesizes an answer based strictly on the retrieved context.
   - If the user requires human assistance, the graph pauses, allowing an admin to inject a response.

---

### 3. Design Decisions

- **Chunk Size Choice:** A chunk size of 1000 characters with an overlap of 200 was chosen. This size is large enough to contain complete thoughts or policy clauses, while the overlap ensures no critical context is split across chunk boundaries.
- **Embedding Strategy:** Dense vector embeddings are used because they capture semantic meaning better than keyword search (TF-IDF). This allows the system to match "refund" with "money back".
- **Retrieval Approach:** Top-K similarity search (K=4) using Cosine Similarity. This provides the LLM with sufficient context without overflowing the context window.
- **Prompt Design Logic:** The system prompt explicitly instructs the LLM: *"You are a support agent. Answer the user's question using ONLY the following context. If you do not know the answer, say 'I don't know'."* This strictly limits hallucinations.

---

### 4. Workflow Explanation

**LangGraph Usage:**
LangGraph was chosen over standard LangChain Chains because customer support requires non-linear flows (cycles, conditional routing, and pausing). LangGraph models the system as a state machine.

**Node Responsibilities:**
- `retrieve`: Purely functional. Queries the database.
- `generate`: Communicates with the external LLM API.
- `escalate`: Updates state flags indicating human intervention is required.

**State Transitions:**
State is immutable within a node. Each node returns a dictionary representing updates to the state (e.g., appending a new message to the `messages` list), which LangGraph merges.

---

### 5. Conditional Logic

**Intent Detection:**
Before executing retrieval or generation, a conditional edge evaluates the last user message. It checks for escalation keywords or analyzes sentiment.
**Routing Decisions:**
- `is_support_query` -> Route to Retriever.
- `is_escalation_request` -> Route to Escalate Node.

---

### 6. HITL Implementation

**Role of Human Intervention:**
AI is not infallible. HITL ensures that high-stakes, complex, or sensitive queries are handled by a human.
**Benefits and Limitations:**
- *Benefits:* Higher accuracy, better customer satisfaction, safeguards against AI failures.
- *Limitations:* Adds latency (user must wait for human), requires staff availability.

---

### 7. Challenges & Trade-offs

- **Retrieval Accuracy vs. Speed:** Increasing the number of retrieved chunks (K) improves accuracy but slows down LLM generation and increases API costs. K=4 is an optimal balance.
- **Chunk Size vs. Context Quality:** Too small, and the LLM lacks context. Too large, and the retrieved chunks introduce noise.
- **Cost vs. Performance:** Using smaller, faster models for intent routing saves costs, while reserving larger models (like GPT-4o or Gemini 1.5 Pro) for actual answer generation ensures high quality.

---

### 8. Testing Strategy

**Testing Approach:**
1. *Unit Testing:* Verify the PDF loader extracts text correctly. Verify ChromaDB returns results for a known query.
2. *Integration Testing:* Run the LangGraph end-to-end to ensure state passes correctly between nodes.
3. *HITL Testing:* Manually trigger the interrupt, update the state, and ensure the graph resumes correctly.

**Sample Queries:**
- *Standard:* "How do I reset my password?"
- *Out-of-Scope:* "Who won the World Cup?" (Should decline to answer).
- *Escalation:* "This product is terrible, I want to speak to a manager." (Should trigger HITL).

---

### 9. Future Enhancements

- **Multi-document Support:** Adding metadata filters so users can query specific manuals.
- **Feedback Loop:** Adding a "thumbs up/down" button to save poorly answered queries for fine-tuning.
- **Memory Integration:** Using Long-Term Memory (e.g., PostgreSQL checkpointer) so the bot remembers past sessions with a specific user.
- **Deployment:** Containerizing the application with Docker and deploying to AWS/GCP.
