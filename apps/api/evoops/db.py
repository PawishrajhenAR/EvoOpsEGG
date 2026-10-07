"""Postgres access via DATABASE_URL (pooler recommended)."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

import psycopg
from psycopg.rows import dict_row

from evoops.settings import get_settings


@contextmanager
def get_conn() -> Iterator[psycopg.Connection]:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not configured")
    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        yield conn


def fetch_user_roles(user_id: str) -> list[str]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select r.key
                from public.user_roles ur
                join public.roles r on r.id = ur.role_id
                where ur.user_id = %s
                order by r.key
                """,
                (user_id,),
            )
            rows = cur.fetchall()
    return [r["key"] for r in rows]


def list_profiles_with_roles() -> list[dict[str, Any]]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select
                  p.id,
                  p.email,
                  p.display_name,
                  coalesce(
                    array_agg(r.key order by r.key) filter (where r.key is not null),
                    '{}'
                  ) as roles
                from public.profiles p
                left join public.user_roles ur on ur.user_id = p.id
                left join public.roles r on r.id = ur.role_id
                group by p.id
                order by p.email
                """
            )
            return list(cur.fetchall())


def list_roles() -> list[dict[str, Any]]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select id, key, name, description from public.roles order by key"
            )
            return list(cur.fetchall())


def grant_role_as_admin(admin_id: str, target_user_id: str, role_key: str) -> None:
    """Grant role using DB as postgres; caller must already verify admin."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into public.user_roles (user_id, role_id, granted_by)
                select %s, r.id, %s
                from public.roles r
                where r.key = %s
                on conflict do nothing
                """,
                (target_user_id, admin_id, role_key),
            )
        conn.commit()


def revoke_role_as_admin(target_user_id: str, role_key: str) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                delete from public.user_roles ur
                using public.roles r
                where ur.role_id = r.id
                  and ur.user_id = %s
                  and r.key = %s
                """,
                (target_user_id, role_key),
            )
        conn.commit()
