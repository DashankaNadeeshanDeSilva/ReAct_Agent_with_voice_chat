# search tools
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.tools import tool


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

agent_tools: list[BaseTool] = [search_tool, multiply_tool]