from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from agent.state import AgentState
from agent.agent import agent
from agent.tools import TOOLS


# Condition function
def should_continue(state: AgentState) -> str:
    """Determine if we should use tools or end the conversation."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check if the last message has tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

def build_agent_graph():
    """Build the agent graph."""
    # Define Graph
    workflow_graph = StateGraph(AgentState)

    # Add nodes
    workflow_graph.add_node("agent", agent)
    workflow_graph.add_node("tools", ToolNode(TOOLS))

    # Add edges
    workflow_graph.add_edge(START, "agent")
    workflow_graph.add_conditional_edges("agent",
                                        should_continue,
                                        {
                                            "tools": "tools",
                                            "end": END
                                        }
                                    )
    workflow_graph.add_edge("tools", "agent")

    # complie the graph
    memory = MemorySaver() # Session memory
    react_agent = workflow_graph.compile(checkpointer=memory)

    return react_agent

