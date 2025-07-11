from fastapi import FastAPI

from .config import settings
from .routers import api

app = FastAPI(
    title="Meta Supervisor",
    description="Orchestration agent for Fin-Agent services.",
    version="0.1.0",
)

app.include_router(api.router, prefix="/api")


@app.get("/", tags=["Health Check"])
async def health_check():
    """
    Checks if the server is running.
    """
    return {"status": "ok"} 