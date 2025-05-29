from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, File, UploadFile, HTTPException
from api_gateway.services.index_document import index_document
from api_gateway.services.agent_chat_service import get_response, Chat

app = FastAPI(title="API Gateway")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins but for production, specify the frontend URL
    # allow_origins=["https://your-frontend-domain.com"],  # Example for production
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

@app.post("/upload_document/")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, TXT and WORD files are allowed.")
    else:
        try:
            response = await index_document(file)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while indexing the document: {str(e)}") 


# Endpoint to handle chat requests
@app.post("/chat_with_agent/")
async def chat_with_agent(chat: Chat):
    """Endpoint to handle chat requests."""
    if not isinstance(chat.user_message, str):
        raise HTTPException(status_code=400, detail="User message must be a string.")
    try:
        response = await get_response(chat)
        return response
    except HTTPException as e:
        raise HTTPException(status_code=response.status_code, 
                            detail=f"An error occurred while processing the chat request: {str(e)}") 