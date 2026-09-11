# Arbitrium

Arbitrium is an arbitration intelligence prototype for domestic and cross-border seat selection, institutional rule review, clause drafting, cost estimation, and source-backed output generation.

## Project Structure

```text
backend/    FastAPI API, database models, migrations, seed data, and tests
frontend/   Vite/React interface and visual assets used by the app
ai_engine/  Retrieval and extraction prototype for source-grounded arbitration facts
docs/       Product notes, review screenshots, and archived build inputs
```

## Quick Start

Backend:

```powershell
cd backend
py -3.10 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

API docs are available at `http://127.0.0.1:8000/docs` when the backend is running.
