import os
import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph import build_graph

st.set_page_config(page_title="RAG Support Assistant", layout="wide")

# Initialize the LangGraph app in session state
if "app" not in st.session_state:
    st.session_state.app = build_graph()
    st.session_state.thread_id = "1" # Constant for demo purposes
    st.session_state.config = {"configurable": {"thread_id": st.session_state.thread_id}}

st.title("Customer Support Assistant")
st.write("Ask questions about the company policy. Type 'human' to test the escalation flow.")

# Initialize chat history in Streamlit (distinct from graph state for display)
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

# Layout: User chat on left, Admin HITL on right
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("User Chat")
    
    # Display chat messages
    for msg in st.session_state.chat_display:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    if prompt := st.chat_input("How can I help you?"):
        st.session_state.chat_display.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Stream the graph execution
        input_data = {"messages": [HumanMessage(content=prompt)]}
        try:
            for event in st.session_state.app.stream(input_data, st.session_state.config):
                for k, v in event.items():
                    if k == "generate" or k == "escalate":
                        messages = v.get("messages", [])
                        if messages:
                            response = messages[-1].content
                            st.session_state.chat_display.append({"role": "assistant", "content": response})
                            st.chat_message("assistant").write(response)
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            st.error(error_msg)
            st.session_state.chat_display.append({"role": "assistant", "content": error_msg})

        # Check if the graph is interrupted (paused for HITL)
        state = st.session_state.app.get_state(st.session_state.config)
        if state.next:
            st.warning("Query escalated. Awaiting human agent response...")

with col2:
    st.subheader("Admin Control (HITL)")
    state = st.session_state.app.get_state(st.session_state.config)
    
    if state.next:
        st.error("Graph Execution Paused: Escalation Required")
        st.write("User Context:")
        # Show recent messages to admin
        recent_msgs = state.values.get("messages", [])[-3:]
        for m in recent_msgs:
            role = "User" if isinstance(m, HumanMessage) else "Bot"
            st.caption(f"{role}: {m.content}")
            
        admin_response = st.text_area("Admin Reply:")
        if st.button("Resume & Send Reply"):
            # Inject human response and resume
            human_msg = AIMessage(content=f"[Human Agent]: {admin_response}")
            # We bypass the 'escalate' node and just finish since we got the human reply
            st.session_state.app.update_state(
                st.session_state.config, 
                {"messages": [human_msg]},
                as_node="escalate" # Pretend the human is the escalate node finishing
            )
            st.success("Reply sent. User can continue.")
            st.session_state.chat_display.append({"role": "assistant", "content": human_msg.content})
            st.rerun()
    else:
        st.info("No active escalations.")
