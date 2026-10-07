# EvoOps API

FastAPI service for EvoOps (Phase 0: health shell + domain skeleton).

## Local setup

```powershell
cd apps\api
uv sync --extra dev
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- Health: http://localhost:8000/health  
- OpenAPI: http://localhost:8000/docs  

Copy repo-root `.env.example` to `P:\EGG PROJECT\.env` and adjust as needed.
