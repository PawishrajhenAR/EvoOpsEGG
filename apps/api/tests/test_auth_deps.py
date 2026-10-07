"""Unit tests for role gate helpers (no live Supabase required)."""

from __future__ import annotations

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from evoops.auth.deps import AuthUser, require_admin, require_roles


def test_auth_user_has_role():
    user = AuthUser(id="1", email="a@b.c", roles=["operator"])
    assert user.has_role("operator")
    assert not user.has_role("admin")
    assert not user.is_admin


def test_require_admin_dependency():
    app = FastAPI()

    async def fake_admin() -> AuthUser:
        return AuthUser(id="1", email="admin@evoops.local", roles=["admin"])

    @app.get("/admin-only")
    async def admin_only(user: AuthUser = Depends(require_admin)):
        return {"id": user.id}

    app.dependency_overrides[require_admin] = fake_admin
    client = TestClient(app)
    assert client.get("/admin-only").status_code == 200


def test_require_roles_forbidden():
    app = FastAPI()

    async def fake_operator() -> AuthUser:
        return AuthUser(id="2", email="op@evoops.local", roles=["operator"])

    dep = require_roles("approver", "admin")

    @app.get("/approver-only")
    async def route(user: AuthUser = Depends(dep)):
        return {"ok": True}

    # Override the inner require_auth used by require_roles by overriding dep itself
    async def deny() -> AuthUser:
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail="Requires one of roles: approver, admin")

    app.dependency_overrides[dep] = deny
    client = TestClient(app)
    assert client.get("/approver-only").status_code == 403


def test_health_still_ok():
    from main import app

    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
