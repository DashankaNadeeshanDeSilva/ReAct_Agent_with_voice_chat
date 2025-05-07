from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_service import LLM

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

llm = LLM()

class Transcription(BaseModel):
    transcription: str

@app.post("/transcribe")
async def receive_transcription(data: Transcription):
    print(f"Received transcription: {data.transcription}")
    output = llm.invoke_llm("provide a short answer for the following query: " + data.transcription) # Invoke LLM with the transcription


    # return {"response": "I received your message!"}
    return {"response": output}
