"""Auth / identity routes."""

from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from evoops.auth.deps import AuthUser, require_admin, require_auth
from evoops import db

router = APIRouter(prefix="/auth", tags=["auth"])


class MeResponse(BaseModel):
    id: str
    email: str
    roles: list[str]


class RoleOut(BaseModel):
    id: UUID
    key: str
    name: str
    description: str


class ProfileOut(BaseModel):
    id: UUID
    email: str
    display_name: str
    roles: list[str]


class GrantRoleBody(BaseModel):
    user_id: UUID
    role_key: str = Field(pattern="^(operator|approver|admin)$")


@router.get("/me", response_model=MeResponse)
async def me(user: Annotated[AuthUser, Depends(require_auth)]) -> MeResponse:
    return MeResponse(id=user.id, email=user.email, roles=user.roles)


@router.get("/roles", response_model=list[RoleOut])
async def get_roles(
    _user: Annotated[AuthUser, Depends(require_auth)],
) -> list[dict[str, Any]]:
    return db.list_roles()


@router.get("/users", response_model=list[ProfileOut])
async def list_users(
    _admin: Annotated[AuthUser, Depends(require_admin)],
) -> list[dict[str, Any]]:
    return db.list_profiles_with_roles()


@router.post("/roles/grant", status_code=status.HTTP_204_NO_CONTENT)
async def grant_role(
    body: GrantRoleBody,
    admin: Annotated[AuthUser, Depends(require_admin)],
) -> None:
    try:
        db.grant_role_as_admin(admin.id, str(body.user_id), body.role_key)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/roles/revoke", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_role(
    body: GrantRoleBody,
    _admin: Annotated[AuthUser, Depends(require_admin)],
) -> None:
    try:
        db.revoke_role_as_admin(str(body.user_id), body.role_key)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
