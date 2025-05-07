### --- React agent with memory --- ###
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.tools import tool
import os
import re
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import AnyMessage, BaseMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver

### Tools ###
@tool
def search_tool(query: str) -> str:
    """Search the web for a query.
    
    Args:
        query: The query to search for.
    Returns:
        The result of the search.
    """
    search = DuckDuckGoSearchRun()
    return search.invoke(query)

@tool
def multiply_tool(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    Returns:
        The product of a and b.
    """
    return int(a) * int(b)

tools = [search_tool, multiply_tool]


### LLM ###

# Set Together.ai key as OPENAI_API_KEY, since Together uses OpenAI-compatible API
os.environ["OPENAI_API_KEY"] = "ab721cf1054a5db66582e22cc43aa90b069b7ee5c39d1f6cd4de48baef4ac06d"

llm = init_chat_model(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", 
    # Lllama gives natural answers compared to DeepSeek R1 70B
    model_provider="together", 
    temperature=0.1
)

llm_with_tools = llm.bind_tools(tools) # bind tools to the llm

### Agent state ###

class AgentState(TypedDict):
    """Agent state for the graph.""" 
    """(define the initial state and structure of incoming data.)"""
    messages: Annotated[Sequence[BaseMessage], add_messages]

### Agent (reasoner) ###

def agent(state: AgentState):
    """Agent invokes the llm with given query (human message) + system message
    and call tools if needed to get the response"""

    # parse the state
    messages = state["messages"]

    # System message   
    system_message = SystemMessage(content=(
        "You are a helpful assistant who thinks step-by step before taking actions like using tools available to you."
        "Use: Thought → Action → Observation → Final Answer"
    ))

    # Get new LLm response
    llm_response = llm_with_tools.invoke([system_message] + messages)

    response = {"messages": [llm_response]}

    return response

### Tools condition ###
def should_continue(state: AgentState) -> str:
    """Determine if we should use tools or end the conversation."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check if the last message has tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"


### Building the agent graph ###
# Define Graph
workflow_graph = StateGraph(AgentState)

# Add nodes
workflow_graph.add_node("agent", agent)
workflow_graph.add_node("tools", ToolNode(tools))

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

# Complie the graph with session memory
memory = MemorySaver()
react_agent = workflow_graph.compile(checkpointer=memory)

# Draw agent graph
from IPython.display import Image, display
display(Image(react_agent.get_graph(xray=True).draw_mermaid_png()))

### Run agent ###
# Define session thread
config = {"configurable": {"thread_id": "1"}}

# Run agent with session
config = {"configurable": {"thread_id": "1"}} # maintain the session thread

# message 1
input_message1 = HumanMessage(content="Hi My name is Jack !. Can you tell me the height of the Big Bell tower in London multiplied by 2 ?")
response1 = react_agent.invoke({"messages": [input_message1]}, config=config)
response1['messages'][-1].pretty_print() # print output
# message 2
input_message2 = HumanMessage(content="What is my name ? and What is address of the Tower ?")
response2 = react_agent.invoke({"messages": [input_message2]}, config)
response2['messages'][-1].pretty_print() # print output

# Visualize the agent responses
'''
for i in range(len(response1['messages'])):
    print(f"Response {i+1}:")
    response1['messages'][i].pretty_print() # Llama 3.3
    print("\n")'''