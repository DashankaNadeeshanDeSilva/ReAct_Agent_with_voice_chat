from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
DEFULT_AGENT_URL = "http://127.0.0.1:5000/agent/reply"

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)


class Chat(BaseModel):
    user_message: str

@app.post("/chat")
async def chat(chat: Chat):

    agent_url = os.getenv("AGENT_SERVICE_URL", DEFULT_AGENT_URL)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            agent_response = await client.post(
                agent_url,
                json={"user_message": chat.user_message, "session_id": "12345"}  # Example session ID
            )

            if agent_response.status_code == 200:
                response = agent_response.json().get("response")
                return {"response": response}

            else:
                # Optionally raise an HTTPException or return an error message
                raise HTTPException(status_code=agent_response.status_code, 
                                    detail="Error encountered from agent")

    except httpx.RequestError as exc:
        print(f"HTTP Exception: {exc}")
        raise HTTPException(status_code=503, detail=f"Error communicating with agent service: {str(exc)}")
    

# Upload documnets for indexing
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    # Step 1: Read file content into memory
    content = await file.read()

    # Step 2: Forward to another microservice
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:9000/process/",  # URL of the secondary microservice
            files={"file": (file.filename, content, file.content_type)}
        )

        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error processing file")