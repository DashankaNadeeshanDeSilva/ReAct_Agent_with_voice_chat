from fastapi import APIRouter, Request
from pydantic import BaseModel
from agent.graph import build_agent_graph
from langchain_core.messages import HumanMessage

# define router
router = APIRouter()

# define agent
react_agent = build_agent_graph()


class ChatInput(BaseModel):
    """Input data validation."""
    user_message: str  # human message/query
    session_id: str  # session id


@router.post("/reply")
async def chat(input: ChatInput):

    response = react_agent.invoke(
        {"messages": [HumanMessage(content=input.user_message)]},
        config={"configurable": {"thread_id": input.session_id}}
    )
    final_response = response['messages'][-1].content

    return {"response": final_response}