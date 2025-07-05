from fastapi import FastAPI, UploadFile, File, HTTPException
from load_docs import load_document
from index_docs import index_docs
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("indexing_service")

app = FastAPI(
    title="Indexing Service",
    description="Document indexing service for KIFrag Assistant",
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

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and container orchestration."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "indexing-service"
    }

@app.post("/index_document/")
async def process(file: UploadFile = File(...)):
    logger.info(f"Received file for indexing: {file.filename}")
    content = await file.read()
    
    try:
        # load document (temp file) 
        documents = load_document(content, file.filename)
        
        # check if the document is empty
        if not documents or documents[0].page_content == "":
            logger.warning(f"Empty document received: {file.filename}")
            return {
                "message": "Document is empty",
                "success": False
            }
            
        # index document
        added_docs = index_docs(documents)
        
        if added_docs:
            logger.info(f"Successfully indexed document: {file.filename}")
            return {
                "message": "Document has been indexed successfully",
                "success": True           
            }
        else:
            logger.warning(f"Failed to index document: {file.filename}")
            return {
                "message": "Document has not been indexed",
                "success": False
            }

    except Exception as e:
        logger.error(f"Error indexing document {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred while indexing the document: {str(e)}")

@app.post("/echo/")
async def echo_file(file: UploadFile = File(...)):
    """Simple echo endpoint for testing file uploads."""
    logger.debug(f"Echo endpoint received file: {file.filename}")
    return {"received_filename": file.filename}
