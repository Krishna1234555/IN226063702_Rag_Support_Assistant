from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from state import AgentState
from nodes import retrieve_node, generate_node, escalate_node

def route_query(state: AgentState):
    """
    Conditional routing logic to decide if we should retrieve context or escalate.
    """
    messages = state.get("messages", [])
    if not messages:
        return "retrieve"
        
    last_message = messages[-1].content.lower()
    
    # Simple keyword-based intent detection
    escalation_keywords = ["human", "agent", "manager", "operator", "frustrated", "angry"]
    if any(word in last_message for word in escalation_keywords):
        return "escalate"
        
    return "retrieve"

def build_graph():
    """
    Constructs the LangGraph StateMachine.
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("escalate", escalate_node)
    
    # Define edges
    # START -> router
    workflow.add_conditional_edges(
        START,
        route_query,
        {
            "retrieve": "retrieve",
            "escalate": "escalate"
        }
    )
    
    # retrieve -> generate
    workflow.add_edge("retrieve", "generate")
    
    # generate -> END
    workflow.add_edge("generate", END)
    
    # escalate -> END
    workflow.add_edge("escalate", END)
    
    # Compile graph with persistence and an interrupt before escalate for HITL
    memory = MemorySaver()
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["escalate"]
    )
    
    return app

if __name__ == "__main__":
    app = build_graph()
    print("Graph compiled successfully!")
