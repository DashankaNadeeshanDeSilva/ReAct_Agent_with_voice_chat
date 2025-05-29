from langchain_core.messages import SystemMessage
from agent.tools import agent_tools
from agent.config import LLM
from agent.state import AgentState 

SYSTEM_MESSAGE = """You are a helpful conversation assistant who thinks step-by step before taking actions like using tools available to you.
\n Tools available to you are:
- search_tool: Search the web for a query.  
- multiply_tool: Multiply two numbers.
- retrieve_context_from_vector_store: Similarity search and retrieve context from vector store based on the query to get specific information.
\n Use process: Thought → Action → Observation → Final Answer.
\n Use past coversation context from memory when answering the questions.
\n Only provide the final answer/response at the end without providing Thought, Action and Observation
\n Try to maintain a conversation with the user and be helpful."""

def agent(state: AgentState):
    """Agent invokes the llm with given query (human message) + system message
    and call tools if needed to get the response"""

    # Initialize LLM
    llm = LLM().init_llm()
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(agent_tools)

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