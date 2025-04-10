from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include the router
app.include_router(router, prefix="/api", tags=["ReAct Agent"])