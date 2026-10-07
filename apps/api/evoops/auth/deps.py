"""Supabase JWT auth dependencies for FastAPI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Callable

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from evoops.db import fetch_user_roles
from evoops.settings import Settings, get_settings

_bearer = HTTPBearer(auto_error=False)


@dataclass
class AuthUser:
    id: str
    email: str
    roles: list[str]

    def has_role(self, role: str) -> bool:
        return role in self.roles

    @property
    def is_admin(self) -> bool:
        return self.has_role("admin")


async def _supabase_user_from_token(settings: Settings, token: str) -> dict:
    if not settings.supabase_url or not settings.supabase_anon_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase is not configured on the API",
        )

    async with httpx.AsyncClient(timeout=20.0) as client:
        res = await client.get(
            f"{settings.supabase_url}/auth/v1/user",
            headers={
                "apikey": settings.supabase_anon_key,
                "Authorization": f"Bearer {token}",
            },
        )

    if res.status_code == 401:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    if res.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return res.json()


async def require_auth(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(_bearer)
    ],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthUser:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    user = await _supabase_user_from_token(settings, credentials.credentials)
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    roles = fetch_user_roles(user_id)
    return AuthUser(
        id=user_id,
        email=user.get("email") or "",
        roles=roles,
    )


def require_roles(*needed: str) -> Callable:
    async def _dep(user: Annotated[AuthUser, Depends(require_auth)]) -> AuthUser:
        if not any(user.has_role(r) for r in needed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {', '.join(needed)}",
            )
        return user

    return _dep


async def require_admin(
    user: Annotated[AuthUser, Depends(require_auth)],
) -> AuthUser:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return user
