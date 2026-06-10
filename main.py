from fastapi import FastAPI, Request

from src.models.pr_model import PullRequestEvent
from src.core.dependencies import get_github_service, get_llm_service
from src.routers.webhook import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}