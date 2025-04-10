from langchain_core.messages import SystemMessage
from agent.tools import TOOLS
from agent.config import LLM
from agent.state import AgentState 

SYSTEM_MESSAGE = "You are a helpful assistant who thinks step-by step before taking actions like using tools available to you.\n Use process: Thought → Action → Observation → Final Answer \n Only provide the final answer/response at the end without providing Thought, Action and Observation"

def agent(state: AgentState):
    """Agent invokes the llm with given query (human message) + system message
    and call tools if needed to get the response"""

    # Initialize LLM
    llm = LLM().init_llm()
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(TOOLS)

    # Parse the state
    messages = state["messages"]
    # Add system message
    system_message = SystemMessage(content=(SYSTEM_MESSAGE))

    # Get new LLm response
    llm_response = llm_with_tools.invoke([system_message] + messages)
    
    response = {
        "messages": [llm_response]
    }

    return response