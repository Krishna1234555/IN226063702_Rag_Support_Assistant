from typing import TypedDict, Annotated, List, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Represents the state of our customer support agent graph.
    """
    # The list of messages in the conversation
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # The context retrieved from the knowledge base
    context: str
    
    # Flag to indicate if human escalation is required
    requires_human: bool
