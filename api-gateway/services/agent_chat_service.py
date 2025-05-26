from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, File, UploadFile, HTTPException
from api_gateway.services.index_document import index_document
from pydantic import BaseModel
import os
import httpx

DEFAULT_AGENT_URL = "http://127.0.0.1:8002/agent_respond/" # Update to internal Docker network or API Gateway config later

class Chat(BaseModel):
    user_message: str
    session_id: str = "12345"  # Default session ID, can be overridden

async def get_response(chat: Chat):
    # agent_url = os.getenv("AGENT_SERVICE_URL", DEFAULT_AGENT_URL)
    agent_url = DEFAULT_AGENT_URL

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            agent_response = await client.post(
                agent_url,
                json={"user_message": chat.user_message, "session_id": chat.session_id}  # Example session ID
            )

            if agent_response.status_code == 200:
                response = agent_response.json().get("response")
                return {"response": response}

            else:
                # Optionally raise an HTTPException or return an error message
                raise HTTPException(status_code=agent_response.status_code, 
                                    detail="Error encountered from agent")
                # agent_response.raise_for_status()

    except httpx.RequestError as exc:
        print(f"HTTP Exception: {exc}")
        raise HTTPException(status_code=503, detail=f"Error communicating with agent service: {str(exc)}")