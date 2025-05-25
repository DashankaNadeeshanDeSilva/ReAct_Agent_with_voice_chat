import aiohttp
from fastapi import UploadFile
from fastapi.responses import JSONResponse

INDEXING_SERVICE_URL = "http://127.0.0.1:8000/index_document/"  # Update to internal Docker network or API Gateway config later


# Index documnet service
async def index_document(file: UploadFile):
    try:
        async with aiohttp.ClientSession() as session:

            form_data = aiohttp.FormData()
            form_data.add_field("file", await file.read(), filename=file.filename, content_type= file.content_type)

            async with session.post(INDEXING_SERVICE_URL, data=form_data) as response:
                content = await response.text()
                print(f"Response from indexing service: {content}")
                return content
                #return JSONResponse(content={"message": content}, status_code=response.status)


    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)