# search tools
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import BaseTool, tool
# from langchain_core.tools import tool
from agent.utils import init_vector_store

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

# initialize the vector store
vector_store = init_vector_store()

@tool
def retrieve_context_from_vector_store(query: str) -> str:
    """Retrieve context from vector store based on the query to get specific information.

    Args:
        query: The query to search for in the vector store.
    Returns:
        The context retrieved from the vector store.
    """

    retrived_context = vector_store.similarity_search(query, k=3)
    if not retrived_context:
        return "No relevant context found in the vector store."     

    # parse the retrieved context into a string
    context = "\n".join([doc.page_content for doc in retrived_context])
    return context


agent_tools: list[BaseTool] = [search_tool, multiply_tool, retrieve_context_from_vector_store]