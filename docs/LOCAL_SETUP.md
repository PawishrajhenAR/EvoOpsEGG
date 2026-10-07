# Local setup (Phase 0)

## Why `npm install` failed earlier

`apps/web` was only a placeholder (`.gitkeep`). There was no `package.json` until Phase 0 scaffold. That is fixed — Next.js is now in `apps/web`.

## Prerequisites

- Node.js 20+ (you have 24)
- npm
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Git

## 1. Clone / open repo

```powershell
cd "P:\EGG PROJECT"
```

## 2. Environment file

```powershell
Copy-Item .env.example .env
# Fill Supabase URL, anon/publishable keys, DATABASE_URL (pooler), service_role
```

For Next.js, also ensure `apps/web/.env.local` has the `NEXT_PUBLIC_*` values
(copy from repo-root `.env`). Passwords with `#` / `@` must be quoted and URL-encoded
(see comments in `.env.example`).

### Supabase Auth (local)

In Dashboard → **Authentication → Providers → Email**:

- Enable Email
- For local demos, turn **off** “Confirm email” so signup returns a session immediately

Then:

1. Open http://localhost:3000/signup and create the first user  
2. Visit **Admin → Roles** (or `/admin/roles`) — first user can `claim_bootstrap_admin`  
3. Grant `operator` / `approver` / `admin` as needed

## 3. Start the web app

```powershell
cd "P:\EGG PROJECT\apps\web"
npm install
npm run dev
```

Open: http://localhost:3000

From repo root (optional):

```powershell
cd "P:\EGG PROJECT"
npm install
npm run dev:web
```

## 4. Start the API

```powershell
cd "P:\EGG PROJECT\apps\api"
uv sync --extra dev
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- Health: http://localhost:8000/health  
- Docs: http://localhost:8000/docs  

API tests:

```powershell
cd "P:\EGG PROJECT\apps\api"
uv run pytest -q
```

## 5. Graphify (engineering graph)

```powershell
cd "P:\EGG PROJECT"
graphify apps/api
graphify cluster-only apps/api --no-label
```

Open `apps/api/graphify-out/graph.html` in a browser.

## Two terminals checklist

| Terminal | Directory | Command | URL |
|----------|-----------|---------|-----|
| 1 | `apps/web` | `npm run dev` | http://localhost:3000 |
| 2 | `apps/api` | `uv run uvicorn main:app --reload --port 8000` | http://localhost:8000 |

## Troubleshooting: `_buildManifest.js.tmp` ENOENT

If `npm run dev` floods errors like:

`ENOENT ... .next\static\development\_buildManifest.js.tmp...`

That is a **stale/corrupt `.next` cache** (common on Windows with Turbopack and paths that contain spaces, e.g. `EGG PROJECT`).

1. Stop the dev server (`Ctrl+C`)
2. Clear cache and restart **without** Turbopack:

```powershell
cd "P:\EGG PROJECT\apps\web"
npm run clean
npm run dev
```

Optional Turbopack (faster, less stable here): `npm run dev:turbo`

If it still fails, close other Node processes and delete `.next` manually, then retry.

## Not included yet (later phases)

- Supabase Auth / migrations
- Real agent orchestration
- Dashboard features beyond the Phase 0 landing page

## Push policy

Do not push until you have tested locally and explicitly approve a push.
