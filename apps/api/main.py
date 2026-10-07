"""EvoOps API entrypoint."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from evoops.api.auth_routes import router as auth_router
from evoops.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="EvoOps API",
    version="0.1.0",
    description="Self-evolving AI operations platform — Phase 1 auth",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "evoops-api", "env": settings.app_env}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "EvoOps API",
        "docs": "/docs",
        "health": "/health",
        "me": "/api/v1/auth/me",
    }
