from fastapi import FastAPI
#from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import build_agent_graph
from langchain_core.messages import HumanMessage


app = FastAPI(title="Agent Service")

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# define agent
react_agent = build_agent_graph()

# Define input model for chat
class ChatInput(BaseModel):
    """Input data validation."""
    user_message: str  # human message/query
    session_id: str  # session id


# Define the chat endpoint
@app.post("/agent_respond/")
async def chat(input: ChatInput):
    response = react_agent.invoke(
        {"messages": [HumanMessage(content=input.user_message)]},
        config={"configurable": {"thread_id": input.session_id}}
    )
    final_response = response['messages'][-1].content

    for msgs in response['messages']:
        msgs.pretty_print()

    return {"response": final_response}