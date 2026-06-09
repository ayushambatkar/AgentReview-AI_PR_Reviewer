from fastapi import FastAPI, Request

from src.models.pr_model import PullRequestEvent
from src.core.dependencies import get_github_service, get_llm_service
from src.routers.webhook import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)

llm_service = get_llm_service()

result = llm_service.review_pr(
    title="Add new feature X",
    description="This PR adds a new feature X that allows users to do Y.",
    diff="diff --git a/file1.py b/file1.py\nindex 83db--- a/file1.py\n+++ b/file1.py\n@@ -1,5 +1,10 @@\n+def new_function():\n+    pass\n\n def existing_function():\n     print('Hello World')\n",
)

print("Review Result:")
print(result)
