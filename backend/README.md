# Arbitrium Backend

FastAPI + PostgreSQL backend for Arbitrium.

## Requirements

- Python 3.10 or 3.11
- PostgreSQL 15 or newer
- `DATABASE_URL` and `SECRET_KEY` configured in `.env`

## 1. Create the Virtual Environment

From the `backend/` folder:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py -3.10` is not available, use your installed Python 3.10 or 3.11 executable directly:

```powershell
"C:\Path\To\Python310\python.exe" -m venv .venv
```

## 2. Create `.env`

```powershell
copy .env.example .env
```

Generate a secret key:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Paste it into `SECRET_KEY` in `backend/.env`.

Default local `.env` shape:

```env
DATABASE_URL=postgresql+psycopg2://arbitrium:arbitrium@localhost:5432/arbitrium
SECRET_KEY=<paste-generated-secret-here>
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=./uploads
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000
```

## 3. Start PostgreSQL

The default `DATABASE_URL` expects a database named `arbitrium`, user `arbitrium`, and password `arbitrium`.

Docker option:

```powershell
docker run --name arbitrium-postgres `
  -e POSTGRES_USER=arbitrium `
  -e POSTGRES_PASSWORD=arbitrium `
  -e POSTGRES_DB=arbitrium `
  -p 5432:5432 `
  -d postgres:16
```

If the container already exists:

```powershell
docker start arbitrium-postgres
```

## 4. Apply Migrations and Seed Data

```powershell
alembic upgrade head
python -m app.seed.seed_db
```

The seed command is idempotent. It loads seats, institutions, rule links, fee placeholders, and recommendation ratings.

## 5. Run the API

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## 6. Run Tests

```powershell
pytest
```

The tests cover recommendation logic, clause generation, and cost estimation without requiring a live browser.

## API Surface

| Area | Endpoints |
| --- | --- |
| Auth | `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me` |
| Dashboard | `GET /api/v1/dashboard` |
| Seat Allocation | `POST /api/v1/seat-allocation/upload-contract`, `POST /api/v1/seat-allocation/analyze`, `GET /api/v1/seat-allocation/{id}` |
| Rules | `GET /api/v1/rules`, `GET /api/v1/rules/sources` |
| Clauses | `POST /api/v1/clauses/generate`, `GET /api/v1/clauses`, `GET /api/v1/clauses/{id}` |
| Cost Estimate | `POST /api/v1/cost-estimate/calculate` |
| Reference Data | `GET /api/v1/seats`, `GET /api/v1/institutions` |

Most demo endpoints work without authentication. If a user is authenticated, generated records are associated with that user.
