# Arbitrium — Engineering Checklist (Iteration 1, Backend-First Pass)

Per the PRD's Development Workflow mandate: tasks are enlisted atomically below and
checked off as they are built and validated. This file is the persistent state log
for this iteration.

Scope decisions made before starting (confirmed with product owner):
- Underlying institutional/rules/caseload data: **seeded reference dataset**, not
  live scraping. Every seeded fact carries a `source_url` and `as_of` date and is
  flagged for periodic manual refresh — see `backend/app/seed/reference_data.py`.
- This pass: **backend only** (DB schema, API, seed data, services). Frontend
  (ReactJS/TypeScript, 5 pages + nav shell) is a follow-up pass.

## 1. Project scaffold
- [x] Backend directory structure (`app/core`, `app/db`, `app/models`, `app/schemas`,
      `app/services`, `app/api/v1/endpoints`, `app/seed`, `alembic`, `tests`)
- [x] `requirements.txt`
- [x] `.env.example`
- [x] `README.md` with setup/run instructions

## 2. Core & DB plumbing
- [x] `app/core/config.py` — settings (DB URL, JWT secret, token expiry)
- [x] `app/core/security.py` — password hashing, JWT encode/decode
- [x] `app/db/session.py` — SQLAlchemy engine/session
- [x] `app/db/base.py` — declarative Base + model registry import

## 3. Database schema (SQLAlchemy models, one per PRD entity)
- [x] `users`
- [x] `seats` (jurisdictions/legal seats)
- [x] `institutions` (LCIA, HKIAC, ICDR/AAA, SIAC, MCIA, ad hoc)
- [x] `institution_rules` (Page 3 — Live Rule Tracking data)
- [x] `annual_report_stats` (Section 4 — cross-border data index)
- [x] `fee_schedules` (Page 5 — cost estimate engine)
- [x] `seat_institution_ratings` (speed/cost/neutrality/enforceability scores
      feeding the Seat Allocation recommendation engine)
- [x] `seat_allocation_requests` / `seat_allocation_results` (Page 2)
- [x] `clauses` (Page 4)
- [x] `cost_estimates` (Page 5)
- [x] `contract_uploads` (Page 2 — Upload Contract intake)
- [x] Alembic initial migration mirroring the above

## 4. Seed reference data
- [x] Seats: India (domestic), Singapore, London/UK, Hong Kong, New York/US,
      Mumbai — with NY Convention membership + supervisory court/statute notes
- [x] Institutions: LCIA, HKIAC, ICDR (AAA), SIAC, MCIA, Ad Hoc — with
      `website_url` and home seat
- [x] Institution rules rows citing the 5 PRD-listed primary sources (LCIA 2020
      Rules, HKIAC 2024 Rules, HKIAC/UNCITRAL Procedures, ICDR Rules/Forms/Fees,
      SIAC Rules 2025)
- [x] Annual report stat rows citing the 4 PRD-listed sources (AAA/ICDR, HKIAC,
      LCIA, SIAC annual report pages) — figures marked `verified=False`
      placeholders pending manual entry from the actual reports
- [x] Fee schedule seed rows (tiered ad valorem placeholders per institution,
      `verified=False`) — structure is real, numbers need a human to confirm
      against the official fee calculators before this goes to production
- [x] Qualitative seat/institution ratings (speed/cost/neutrality/enforceability,
      1–5) used by the recommendation engine
- [x] `seed_db.py` — creates tables (dev convenience) and loads the above,
      idempotent (upsert by natural key)

## 5. Services (business logic, DB-agnostic where practical)
- [x] `recommendation_engine.py` — weighted scorer over seat/institution
      ratings using the four user-supplied slider weights; produces ranked
      results with rationale, pros/cons, and citations
- [x] `cost_estimator.py` — tiered fee calculator over `fee_schedules`
- [x] `clause_generator.py` — template-based clause assembly + pathology
      checks (missing seat/institution mismatch, arbitrator-count vs.
      appointment-mechanism conflicts, language/governing-law gaps)
- [x] `contract_parser.py` — heuristic PDF/DOCX text extraction (parties,
      governing law, claim quantum, scope) to prefill the intake form;
      explicitly best-effort, not a legal-NLP system

## 6. API endpoints
- [x] `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- [x] `GET /api/v1/dashboard` (guest vs. authenticated response shape)
- [x] `GET /api/v1/seats`, `GET /api/v1/institutions`
- [x] `GET /api/v1/rules`, `GET /api/v1/rules/sources` (Page 3 + Section 4 index)
- [x] `POST /api/v1/seat-allocation/upload-contract` (multipart, extraction)
- [x] `POST /api/v1/seat-allocation/analyze` (Page 2 core workflow)
- [x] `GET /api/v1/seat-allocation/{id}`
- [x] `POST /api/v1/clauses/generate`, `GET /api/v1/clauses/{id}`,
      `GET /api/v1/clauses` (history)
- [x] `POST /api/v1/cost-estimate/calculate`
- [x] `app/main.py` — FastAPI app, CORS, router wiring, startup

## 7. Tests
- [x] `tests/test_recommendation_engine.py`
- [x] `tests/test_cost_estimator.py`
- [x] `tests/test_clause_generator.py`

## 8. Validation
- [x] `python -m py_compile` across all backend modules (syntax sanity)
- [x] `pip install -r requirements.txt` into a fresh venv — clean install
      (had to pin `bcrypt==4.0.1`; passlib 1.7.4 is incompatible with
      bcrypt 5.x's removed `__about__` attribute — fixed in requirements.txt)
- [x] `pytest` — 12/12 passing (pure-logic tests: recommendation engine,
      cost estimator, clause generator/pathology checks)
- [x] Full API smoke test against a throwaway SQLite DB (stand-in for
      Postgres, no server available in this sandbox): seed script,
      register/login/me, guest vs. authenticated dashboard, seats/
      institutions/rules listing, seat-allocation analyze end-to-end
      (weights → scored/ranked results with citations), clause generation +
      pathology checks, cost estimate calculation, and dashboard history
      population — all passed. Not a substitute for running against real
      Postgres (JSON/DateTime dialect behavior can differ), but confirms the
      request/response wiring and business logic are correct.

## Known gaps / next iteration
- [ ] Frontend (React/TS): header, right nav sidebar, 5 pages
- [ ] Real auth flows wired to frontend (currently backend JWT only)
- [ ] File storage for uploaded contracts beyond local disk (`uploads/`)
- [ ] Replace placeholder fee-schedule and annual-report figures with the
      real numbers from the cited primary sources (`verified=False` rows)
- [ ] Live rule-tracking refresh job (cron/task) to periodically re-check the
      5 primary rule sources for changes — out of scope for this pass, schema
      already supports storing `last_checked_at` per rule
- [ ] Run `alembic upgrade head` + `uvicorn` against a real PostgreSQL
      instance to confirm the migration and JSON/DateTime column behavior
      match the SQLite smoke test (no Postgres server available in this
      sandbox)
