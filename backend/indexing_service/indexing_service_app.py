from fastapi import FastAPI, UploadFile, File

app = FastAPI()
''''
@app.post("/index_document/")
async def process(file: UploadFile = File(...)):
    content = await file.read()

    # Simulate processing: just show first 100 bytes
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "preview": content[:100].decode(errors="ignore")  # decode only part of content
    }
'''

@app.post("/index_document/")
async def process(file: UploadFile = File(...)):
    content = await file.read()

    try:
        # load document (temp file) 
        #document = load_document(content, file.filename)
        # documnet chunking
        #document = document_chunking(document)
        # generate embeddings
        # insert documnets
        # return success message syaing the documnet has been indexed

        # index document
        

        if not document[0].page_content == "":
            return {
            #"num_docs": len(document),
            #"preview": document[0].page_content[:200],  # show preview
        }
            
        else:
            return {
                "message": "Document is empty"
            }
            #raise ValueError("Document is empty")

    except Exception as e:
        return {"error": str(e)}
