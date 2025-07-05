from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import build_agent_graph
from langchain_core.messages import HumanMessage
import logging
from datetime import datetime
import os


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("agent_service")


app = FastAPI(
    title="Agent Service",
    description="AI Agent Service for KIFrag Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow CORS for all origins in development, but restrict in production
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
origins = ["*"] if ENVIRONMENT == "development" else ["https://your-production-domain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# define agent
try:
    logger.info("Initializing AI agent...")
    react_agent = build_agent_graph()
    logger.info("AI agent successfully initialized")
except Exception as e:
    logger.error(f"Failed to initialize AI agent: {str(e)}", exc_info=True)
    raise


# Define input model for chat
class ChatInput(BaseModel):
    """Input data validation."""
    user_message: str  # human message/query
    session_id: str  # session id


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and container orchestration."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "agent-service"
    }


# Define the chat endpoint
@app.post("/agent_respond/")
async def chat(input: ChatInput):
    try:
        logger.info(f"Processing request for session {input.session_id[:8]}...")
        
        response = react_agent.invoke(
            {"messages": [HumanMessage(content=input.user_message)]},
            config={"configurable": {"thread_id": input.session_id}}
        )
        final_response = response['messages'][-1].content

        """
        # print the response for debugging purposes
        for message in response['messages']:
            message.pretty_print()
        """

        logger.info(f"Successfully generated response for session {input.session_id[:8]}")
        return {"response": final_response}
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your request: {str(e)}")