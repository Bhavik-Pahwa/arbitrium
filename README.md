# Arbitrium

Arbitrium is a working arbitration-intelligence demo for domestic and cross-border seat selection, institutional rule review, clause drafting, cost estimation, and source-backed output generation.

## Project Structure

```text
backend/    FastAPI API, PostgreSQL models, Alembic migrations, seed data, and tests
frontend/   Vite + React interface
ai_engine/  Retrieval and extraction prototype for source-grounded arbitration facts
docs/       Product notes, references, and archived planning material
```

## Requirements

Install these before setup:

- Python 3.10 or 3.11
- Node.js 20 or newer
- PostgreSQL 15 or newer, or Docker Desktop if you want to run PostgreSQL in a container
- Git

The commands below are written for PowerShell on Windows.

## 1. Clone the Repository

```powershell
git clone <your-repo-url>
cd arbitrium
```

## 2. Start PostgreSQL

Use either an existing local PostgreSQL instance or the Docker command below.

```powershell
docker run --name arbitrium-postgres `
  -e POSTGRES_USER=arbitrium `
  -e POSTGRES_PASSWORD=arbitrium `
  -e POSTGRES_DB=arbitrium `
  -p 5432:5432 `
  -d postgres:16
```

If the container already exists, start it instead:

```powershell
docker start arbitrium-postgres
```

The default backend database URL expects:

```text
postgresql+psycopg2://arbitrium:arbitrium@localhost:5432/arbitrium
```

## 3. Configure the Backend

```powershell
cd backend
py -3.10 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Open `backend/.env` and set `SECRET_KEY` to a long random value. Generate one with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Your `backend/.env` should look like this shape:

```env
DATABASE_URL=postgresql+psycopg2://arbitrium:arbitrium@localhost:5432/arbitrium
SECRET_KEY=<paste-generated-secret-here>
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=./uploads
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000
```

Do not commit the real `.env` file.

## 4. Create and Seed the Database

Run these from the `backend/` folder with the virtual environment active:

```powershell
alembic upgrade head
python -m app.seed.seed_db
```

`alembic upgrade head` creates the database schema.

`python -m app.seed.seed_db` loads seats, institutions, rules, fee placeholders, and recommendation ratings.

## 5. Run the Backend

From `backend/`:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Keep this terminal open.

Verify:

- Health check: `http://127.0.0.1:8000/health`
- API docs: `http://127.0.0.1:8000/docs`

## 6. Run the Frontend

Open a second PowerShell terminal:

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173/
```

The frontend calls `http://localhost:8000` by default. To override it:

```powershell
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
npm run dev -- --host 127.0.0.1 --port 5173
```

## 7. Run Tests

Backend:

```powershell
cd backend
.\.venv\Scripts\activate
pytest
```

Frontend production build:

```powershell
cd frontend
npm run build
```

## Common Problems

### `py -3.10` is not found

Install Python 3.10 or 3.11, then either use the Python launcher:

```powershell
py -3.10 -m venv .venv
```

or use the full path to your Python executable:

```powershell
"C:\Path\To\Python310\python.exe" -m venv .venv
```

### Backend cannot connect to PostgreSQL

Check that PostgreSQL is running and that `DATABASE_URL` in `backend/.env` matches your database credentials.

For Docker:

```powershell
docker ps
docker start arbitrium-postgres
```

### Frontend says it is using local/reference data

Make sure the backend is running on port `8000`, then refresh the frontend.

### CORS error in the browser

Make sure `backend/.env` includes the frontend origin in `CORS_ORIGINS`, especially:

```env
http://127.0.0.1:5173
```
