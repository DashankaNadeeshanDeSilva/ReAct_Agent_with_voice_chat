from fastapi import FastAPI, UploadFile, File
from indexing_service.load_docs import load_document
from indexing_service.index_docs import index_docs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post("/index_document/")
async def process(file: UploadFile = File(...)):
    content = await file.read()
    print(f"Received file: {file.filename}")

    try:
        # load document (temp file) 
        documents = load_document(content, file.filename)
        
        # check if the document is empty
        if not documents[0].page_content == "":
            # index document
            added_docs = index_docs(documents)  # return success message syaing the documnet has been indexed
            if added_docs:
                return {
                    "message": "Document has been indexed successful"            
                }
            else:
                return {
                    "message": "Document has not been indexed"
                }
            
        else:
            return {
                "message": "Document is empty"
            }

    except Exception as e:
        return {"error": str(e)}

@app.post("/echo/")
async def echo_file(file: UploadFile = File(...)):
    return {"received_filename": file.filename}
