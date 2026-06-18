# Agent Review - AI Pull Request reviewer bot

A lightweight GitHub pull request reviewer that judges your code and maybe you too

## Overview

- Receives GitHub webhook events for pull requests.
- Fetches changed files from the PR and builds a unified diff.
- Sends the PR title, description, and diff to a review LLM pipeline (LangGraph + Groq/LangChain).
- Returns or stores the model's review output.

## Key files

- `main.py` — example runner.
- `src/routers/webhook.py` — FastAPI webhook endpoint.
- `src/services/github_service.py` — GitHub App auth, fetch PR files, and `build_pr_diff` helper.
- `src/services/llm_service.py` — LLM client wiring and review entrypoint.
- `src/review/` — prompt templates, graph, and nodes for composing the review.

## Requirements

Install dependencies into a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell on Windows
pip install -r requirements.txt
```

## Environment variables / .env

The app reads configuration via `src/core/config.py` (Pydantic `Settings`). Create a `.env` file or set these environment variables:

- `GITHUB_APP_ID` — GitHub App ID (numeric)
- `GITHUB_PRIVATE_KEY_PATH` — Path to the GitHub App private key PEM file
- `GROQ_API_KEY` — API key for Groq (used by `langchain_groq`)
- `LANGCHAIN_API_KEY` — Optional: LangChain / LangSmith API key
- `DEV_SECRET` — Development secret used by the app

Note: The names in `Settings` are `github_app_id`, `github_private_key_path`, `groq_api_key`, `langchain_api_key`, and `dev_secret` (Pydantic reads from environment variables or `.env`).

## Running locally

Start the FastAPI app (development):

```bash
uvicorn main:app --reload
```

Expose a webhook receiver (e.g., via ngrok) and configure the GitHub App to send pull request events to `/webhook`.

## How it works

1. The webhook handler validates the incoming payload and uses the GitHub Service to list PR files.
2. `build_pr_diff` concatenates available `patch` text into a unified diff string.
3. The LLM service invokes a review node that sends a system/human prompt and returns the review.

## Notes & next steps

- The current review flow is a single graph node; consider splitting into separate passes for security, performance, and style.
- Some files may not include `patch` in the GitHub API response (binary or large files); the diff builder adds a placeholder for those files.

## License

MIT


- small change