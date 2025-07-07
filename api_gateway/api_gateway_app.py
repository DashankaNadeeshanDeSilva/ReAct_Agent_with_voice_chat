from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, File, UploadFile, HTTPException
from services.index_document import index_document
from services.agent_chat_service import get_response, Chat
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api_gateway")

app = FastAPI(
    title="API Gateway",
    description="API Gateway for KIFrag AI Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend requests
# In production, restrict this to specific origins
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
origins = ["*"] if ENVIRONMENT == "development" else ["https://your-production-domain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Endpoint to handle document uploads and indexing

ALLOWED_FILE_TYPES = {
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and container orchestration."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "api-gateway"
    }

@app.post("/upload_document/")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_FILE_TYPES:
        logger.warning(f"Rejected file upload with invalid type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, TXT and WORD files are allowed.")
    else:
        try:
            logger.info(f"Processing document upload: {file.filename}")
            response = await index_document(file)
            return response
        except Exception as e:
            logger.error(f"Error indexing document: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"An error occurred while indexing the document: {str(e)}") 


# Endpoint to handle chat requests
@app.post("/chat_with_agent/")
async def chat_with_agent(chat: Chat):
    """Endpoint to handle chat requests."""
    if not isinstance(chat.user_message, str):
        logger.warning("Rejected chat request with invalid message type")
        raise HTTPException(status_code=400, detail="User message must be a string.")
    try:
        logger.info(f"Processing chat request for session: {chat.session_id[:8]}...")
        response = await get_response(chat)
        return response
    except HTTPException as e:
        logger.error(f"HTTP error in chat request: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error in chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")