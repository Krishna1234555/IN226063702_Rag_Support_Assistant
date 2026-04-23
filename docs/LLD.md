# Low-Level Design (LLD)
## RAG-Based Customer Support Assistant

### 1. Module-Level Design

- **Document Processing Module:** Handles the ingestion of PDF files. Uses LangChain's `PyPDFLoader` to read pages and extract text.
- **Chunking Module:** Utilizes `RecursiveCharacterTextSplitter`. Configuration: `chunk_size=1000`, `chunk_overlap=200`, `separators=["\n\n", "\n", " ", ""]`.
- **Embedding Module:** Wraps Google Generative AI Embeddings (`models/embedding-001`).
- **Vector Storage Module:** Initializes a ChromaDB persistent client to store collections of document chunks and their vector representations.
- **Retrieval Module:** A function that takes a string query, performs `similarity_search` on ChromaDB, and returns a list of `Document` objects.
- **Query Processing Module:** The LLM prompt engineering layer. It injects the user query and retrieved context into a `ChatPromptTemplate`.
- **Graph Execution Module:** The core `StateGraph` definition using LangGraph, encompassing nodes and edges.
- **HITL Module:** Configuration within LangGraph to pause execution (`interrupt_before`) and a specialized UI component to input human override data.

---

### 2. Data Structures

**Document Representation:**
```json
{
  "page_content": "The actual text extracted from the PDF.",
  "metadata": {
    "source": "manual.pdf",
    "page": 1
  }
}
```

**State Object for LangGraph (`TypedDict`):**
```python
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # The history of messages in the conversation
    messages: Annotated[List[BaseMessage], add_messages]
    # Context retrieved from the Vector DB
    context: str
    # Flag to determine if the query should be routed to a human
    requires_human: bool
```

---

### 3. Workflow Design (LangGraph)

**Nodes:**
1. `retrieve_node(state)`: Extracts the latest user message, queries the Vector DB, formats the retrieved documents, and updates the `context` key in the state.
2. `generate_node(state)`: Constructs a prompt using `state['messages']` and `state['context']`, invokes the LLM, and appends the response to `messages`.
3. `escalate_node(state)`: Sets a standard "A human agent will be with you shortly" message and prepares the state for interruption.

**Edges:**
- `START -> router_edge`: The entry point.
- `router_edge -> retrieve_node`: If the query relates to the knowledge base.
- `router_edge -> escalate_node`: If the query explicitly asks for a human or exhibits high frustration.
- `retrieve_node -> generate_node`: After context is found.
- `escalate_node -> END`: Pauses execution for HITL.
- `generate_node -> END`: Finishes the workflow and returns the response.

---

### 4. Conditional Routing Logic

The system utilizes a lightweight LLM call or regex-based router to determine the next step:

- **Answer generation criteria:** The intent is an informational request related to the product/service.
- **Escalation criteria:** The user types "talk to human", "agent", or the router detects intense negative sentiment.
- **Missing context:** If `retrieve_node` returns empty or low-score results, the logic flags the state to route to `escalate_node` instead of generating an hallucinated answer.

---

### 5. HITL Design

- **When escalation is triggered:** The graph compiles with `interrupt_before=["escalate_node"]`.
- **What happens after escalation:** The system pauses. The user sees a standby message. The State is persisted using a `MemorySaver` checkpointer.
- **Human Integration:** A dashboard views the paused graph state. An admin can read the user's `messages`, input a manual text response, and use the LangGraph `update_state` API to resume the graph, bypassing the LLM generation node entirely.

---

### 6. API / Interface Design

The primary interface is a Streamlit Web UI.

**Input Format:** Natural language string entered via `st.chat_input()`.
**Output Format:** Markdown-formatted text rendered via `st.chat_message()`.

**Interaction Flow:**
1. System: "Hello, how can I help you?"
2. User: "What is your refund policy?"
3. System (Processing via Graph -> Retrieve -> Generate) -> Returns Answer.
4. User: "This is useless, get me a manager."
5. System (Processing via Graph -> Escalate) -> Returns "Escalating to human agent..." (Graph paused).

---

### 7. Error Handling

- **Missing Data:** If no PDF is loaded, the UI will disable the chat input and prompt the user to upload/ingest documents first.
- **No Relevant Chunks Found:** The retriever handles empty results by injecting a standard "No relevant context found" string. The `generate_node` is prompted to state "I don't have enough information" and optionally trigger escalation.
- **LLM Failure:** API timeouts or quota errors are caught using `try/except` blocks around the LLM invocation, returning a polite fallback message.
