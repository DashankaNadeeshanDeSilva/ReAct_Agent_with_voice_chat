from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, File, UploadFile, HTTPException
from api_gateway.services.index_document import index_document

app = FastAPI(title="API Gateway")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post("/upload_document/")
async def upload_document(file: UploadFile = File(...)):
    print()
    print(file.content_type)
    if file.content_type not in ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, TXT and WORD files are allowed.")
    else:
        try:
            response = await index_document(file)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while indexing the document: {str(e)}") 


