# React agent with reasoning log
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
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    model_provider="together", 
    temperature=0.1
)

llm_with_tools = llm.bind_tools(tools) # bind tools to the llm

### Agent state ###

class AgentState(TypedDict):
    """Agent state for the graph.""" 
    """(define the initial state and structure of incoming data.)"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    history: Annotated[list[str], lambda x, y: x+y] # history trace

### Agent (reasoner) ###

def extract_reasoning_chunks(text: str) -> list[str]:
    """Extract reasoning chunks (looks like) Thought, Action, Observation and Final Answer."""
    lines = text.splitlines()
    reasoning_chunks = [line.strip() for line in lines if re.match(r"^(Thought|Action|Observation|Final Answer):", line.strip())]
    return reasoning_chunks


def agent(state: AgentState):
    """Agent invokes the llm with given query (human message) + system message
    and call tools if needed to get the response"""

    # parse the state
    messages = state["messages"]

    # System message   
    system_message = SystemMessage(content=(
        "You are a helpuful AI agent that thinks step-by-step before taking actions like using tools available to you."
        "Use the following format:\n"
        "Thought: Describe what you’re thinking.\n"
        "Action: Specify the tool and its arguments.\n"
        "Observation: The result from that tool.\n\n"
        "When you’re confident, give a final answer."
    ))

    # Get new LLm response
    llm_response = llm_with_tools.invoke([system_message] + messages)
    
    # Extract reasoning chunks from the response for history
    reasoning = extract_reasoning_chunks(llm_response.content)
    
    response = {
        "messages": [llm_response],
        "history": reasoning
    }

    return response


### Building the agent graph ###
# Define Graph
workflow_graph = StateGraph(AgentState)

# Add nodes
workflow_graph.add_node("agent", agent)
workflow_graph.add_node("tools", ToolNode(tools))

# Add edges
workflow_graph.add_edge(START, "agent")
workflow_graph.add_conditional_edges("agent", tools_condition)
workflow_graph.add_edge("tools", "agent")

# Complie the graph
react_agent = workflow_graph.compile()

### Run agent ###
response = react_agent.invoke({"messages": [HumanMessage(content="multiply the height of the Eiffel Tower by 5")]})
print(response['messages'][-1].pretty_print())

# Print full ReAct reasoning
print("\n--- Reasoning Trace ---")
for step in response["history"]:
    print(step)