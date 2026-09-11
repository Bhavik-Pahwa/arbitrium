# Arbitrium — Master Project Reference

**Compiled:** 2026-09-10
**Scope:** Everything built across this conversation — PRD, scope decisions, backend (FastAPI/PostgreSQL), AI Engine (OpenRouter agentic RAG extractor), every schema field, every endpoint, every algorithm, every source cited, every bug found and fixed, every open gap.
**Owner:** ashishvermabpit@gmail.com
**Working directory:** `d:\deepika doc\Study materials\arbitrium\`

This file is a single point-in-time snapshot of everything discussed and built. It is not auto-maintained — if the code changes after this date, trust the code over this document and update this file to match.

---

## Table of Contents

1. [Problem & Product](#1-problem--product)
2. [Original PRD (verbatim)](#2-original-prd-verbatim)
3. [Scope Decisions & Rationale](#3-scope-decisions--rationale)
4. [Repository Layout](#4-repository-layout)
5. [Backend — Architecture](#5-backend--architecture)
6. [Backend — Database Schema (full field-level detail)](#6-backend--database-schema-full-field-level-detail)
7. [Backend — API Surface (full request/response detail)](#7-backend--api-surface-full-requestresponse-detail)
8. [Backend — Services (algorithms, low level)](#8-backend--services-algorithms-low-level)
9. [Backend — Seed Reference Data (every source, every value)](#9-backend--seed-reference-data-every-source-every-value)
10. [Backend — Auth](#10-backend--auth)
11. [Backend — Validation Run & Bugs Found](#11-backend--validation-run--bugs-found)
12. [AI Engine — Purpose & Non-Negotiable Constraints](#12-ai-engine--purpose--non-negotiable-constraints)
13. [AI Engine — Design Decisions & Rationale](#13-ai-engine--design-decisions--rationale)
14. [AI Engine — Module-by-Module Detail](#14-ai-engine--module-by-module-detail)
15. [AI Engine — Agentic Loop Mechanics](#15-ai-engine--agentic-loop-mechanics)
16. [AI Engine — Tool Schemas (exact JSON)](#16-ai-engine--tool-schemas-exact-json)
17. [AI Engine — Hallucination Guard (exact algorithm)](#17-ai-engine--hallucination-guard-exact-algorithm)
18. [AI Engine — System Prompt (verbatim)](#18-ai-engine--system-prompt-verbatim)
19. [AI Engine — Validation Run, Bugs Found, and Live Test Results](#19-ai-engine--validation-run-bugs-found-and-live-test-results)
20. [Credentials & Secrets — What Exists, Where It Lives](#20-credentials--secrets--what-exists-where-it-lives)
21. [All External Sources Cited (complete list)](#21-all-external-sources-cited-complete-list)
22. [Legal & Data-Integrity Scaffolding](#22-legal--data-integrity-scaffolding)
23. [Environment Details (dependency versions, Python version, OS)](#23-environment-details-dependency-versions-python-version-os)
24. [Deliverables Summary](#24-deliverables-summary)
25. [Known Gaps / Next Iteration (both modules)](#25-known-gaps--next-iteration-both-modules)

---

## 1. Problem & Product

**Product name:** Arbitrium
**Product type:** Legal decision-support & arbitration intelligence platform
**Target stack (per PRD):** ReactJS (TypeScript) frontend, Python (FastAPI) backend, PostgreSQL database

**Problem statement (from the PRD):** When drafting commercial agreements, arbitration clauses are frequently copied from legacy templates without rigorous analysis of seating suitability, institutional administrative capabilities, or cross-border asset enforcement paths. Arbitrium is meant to act as a neutral, multi-institution intelligence platform: it processes institutional rule updates, historical caseload statistics, and jurisdiction-specific statutory rules to deliver defensible seat recommendations, cost/duration estimates, and pathology-free custom arbitration clauses.

**What "defensible" means in this build, concretely:** every recommendation, every clause, every cost estimate the system produces must trace back to a stored source (a URL, a rules document, a curated rating with a written rationale) — never an opaque model judgment with no paper trail. This single requirement shaped nearly every architectural decision documented below.

---

## 2. Original PRD (verbatim)

The PRD was supplied as `iteration1.md` in the working directory. Full text, reproduced exactly as received (note: the source file had a mojibake character in "Iteration 1 â Production Draft" — reproduced as-is, not corrected):

~~~markdown
# Product Requirements Document (PRD)

**Document Name:** arbitrium prd iteration 1
**Product Name:** Arbitrium
**Product Type:** Legal Decision-Support & Arbitration Intelligence Platform
**Target Architecture Stack:** ReactJS (TypeScript) Frontend, Python (FastAPI) Backend, SQL (PostgreSQL) Database
**Status:** Iteration 1 â Production Draft

---

## Development Workflow & Implementation Mandate

To ensure complete and systematic execution, the engineering team must follow these rules:

1. **Task Enlistment:** Deconstruct every page component, API endpoint, database schema, and source integration routine into discrete, atomic engineering tasks before writing production code.
2. **Logs & Checklist Maintenance:** Maintain a persistent state log and task checklist throughout all development sprints.
3. **Continuous Iteration Cycle:** Continuously iterate, build, and test until every item on the task checklist is completed and validated against primary legal datasources.

---

## 1. Executive Summary & Problem Statement

When drafting commercial agreements, arbitration clauses are frequently copied from legacy templates without rigorous analysis of seating suitability, institutional administrative capabilities, or cross-border asset enforcement paths.

**Arbitrium** bridges this gap by acting as a neutral, multi-institution intelligence platform. It processes real-time institutional rule updates, historical annual caseload statistics, and jurisdiction-specific statutory rules to deliver defensible seat recommendations, cost/duration estimates, and pathology-free custom arbitration clauses.

---

## 2. Information Architecture & Global UI Layout

The platform features a fixed top header bar and a persistent right-hand navigation sidebar across all application views.

### Top Header Bar
* **Top Left:** Application Logo (`Arbitrium`)
* **Top Right:** Authentication Action (`Log In` / `User Profile`)

### Right-Side Navigation Sidebar
The right sidebar contains five navigation options:
1. **Dashboard** (Default Landing Page)
2. **Seat Allocation**
3. **Live Rule Tracking & Components**
4. **Clause Generation**
5. **Cost and Duration Estimate**

---

## 3. Page Specifications & User Workflows

### Page 1: Dashboard

* **Guest State (Unauthenticated):**
  * Displays a welcome banner outlining the core capabilities of Arbitrium.
  * Prominently presents a direct Call-to-Action (CTA) button redirecting users to the **Clause Generation** module.
* **Authenticated State:**
  * Displays a personalized welcome message and user activity history.
  * Lists historical **Clause Generated** records and previously completed **Seat Allocated** analysis summaries with timestamps and saved parameters.

---

### Page 2: Seat Allocation

#### Path Guidance & Layout Setup
* **Path Explanations (Right Side):** Non-clickable static guidance cards defining:
  * **Domestic Arbitration:** Proceedings seated locally under national supervisory courts and statutes (e.g., Indian Arbitration and Conciliation Act 1996).
  * **Cross-Border Arbitration:** Multi-jurisdictional proceedings requiring foreign asset enforcement analysis (e.g., New York Convention enforcement) and forum neutrality.

#### Intake Actions (Bottom Right Corner)
* **Upload Contract:** Allows users to upload agreement files (`.pdf`, `.docx`). An automated extraction module parses core transactional details (parties, scope, claim quantum, governing law) and populates the intake form fields.
* **Enter Manually:** Opens a structured Google Form-style intake form allowing direct manual entry.
* **Manual Preferences (Always Required):** Even when fields are auto-filled via contract upload, users must explicitly configure priority slider weightings for:
  * **Speed** (Time to Award)
  * **Cost** (Administrative & Tribunal Fees)
  * **Neutrality** (Forum Independence)
  * **Enforceability** (Asset Enforcement Security)

#### Output & Results View
* **Recommendation Rationale:** Clear explanations detailing why specific seats and institutions were recommended.
* **Sourced Citations:** Clickable hyperlinks referencing the primary data sources (e.g., annual reports, statutory rules) supporting the recommendation.
* **Pros & Cons:** Bulleted advantages and disadvantages for the primary recommended seat and top alternative choices.
* **Clause Output Integration:** Displays a generated clause preview with a direct CTA button that redirects the user to the **Clause Generation** module with pre-populated parameters.

---

### Page 3: Live Rule Tracking & Components

Monitors active institutional rule updates, procedural amendments, and statutory modifications across major global arbitral bodies.

#### Primary Rule Data Sources
* **LCIA:** [LCIA Arbitration Rules 2020](https://www.lcia.org/Dispute_Resolution_Services/lcia-arbitration-rules-2020.aspx)
* **HKIAC:** [HKIAC 2024 Administered Arbitration Rules](https://hkiac.org/arbitration/rules-and-practice-notes/2024-administered-arbitration-rules/)
* **HKIAC / UNCITRAL:** [HKIAC Procedures for Administration under UNCITRAL Rules](https://hkiac.org/arbitration/rules-and-practice-notes/2015-procedures-administration-under-uncitral-rules/)
* **ICDR:** [ICDR Rules, Forms & Fees](https://www.icdr.org/rules_forms_fees)
* **SIAC:** [SIAC Rules 2025](https://siac.org.sg/siac-rules-2025)

---

### Page 4: Clause Generation

Allows users to configure custom arbitration agreements or refine pre-filled clauses redirected from the Seat Allocation workflow.

#### Configurable User Inputs
1. **Selected Seat** (e.g., Singapore, London, Mumbai)
2. **Number of Arbitrators** (Sole Arbitrator / Three-Member Tribunal / Emergency Provisions)
3. **Arbitral Institution** (e.g., SIAC, HKIAC, LCIA, ICDR, MCIA, Ad Hoc)
4. **Party Details & Corporate Identities**
5. **Appointment Mechanism** (Default institutional rules, co-arbitrator nomination, or presiding officer appointment)
6. **Language of Proceedings**
7. **Governing Law of Contract & Arbitration Agreement**

#### Output
* Renders a custom, pathology-checked arbitration clause ready for direct copying or export.

---

### Page 5: Cost and Duration Estimate

Calculates administrative fee ranges, tribunal cost estimations, and projected dispute timelines based on claim quanta and institutional fee schedules.

---

## 4. Cross-Border Data Index (Annual Reports)

The cross-border seat allocation engine relies on primary statistics and caseload metrics extracted from institutional annual reports:

* **AAA / ICDR:** [American Arbitration Association Annual Reports Repository](https://www.adr.org/annual-reports/)
* **HKIAC:** [Hong Kong International Arbitration Centre Case Statistics & Annual Reports](https://hkiac.org/about-us/annual-report/)
* **LCIA:** [London Court of International Arbitration Reports & Casework Data](https://www.lcia.org/lcia/reports.aspx)
* **SIAC:** [Singapore International Arbitration Centre Annual Reports](https://siac.org.sg/annual-reports)
~~~

**Second user message (later in the conversation, verbatim, transcribed from voice input with filler words intact as spoken):**

> "If I am creating a website which analyzes the uh uh which analyzes the annual reports of the arbitration sites and checks upon which seat is expert in handling which type of arbitration such as construction or um technology or whatever and which of which country do they get more of arbitrations. So using those we can analyze and we can create a seat suggester to any person who is giving us those informations like uh where do they want it enforced and whatever. So what things that I need to pick up from the annual reports of like SIAC and HKIAC and AAA-ICDR and MCIA.
>
> Technical Implementation of the AI Workflow:
> - Python is the backbone of the complete architecture
>
> Create a completely separate module, the AI Engine. That module will handle all the tasks that have just been defined.
>
> Use the openrouter API key provided, use OpenAI library for API calls to the models, design the system to modularly send, process and respond with data. create an Agentic Loop for recursive API calls in case tool calls are required. You will be needed to use RAG on PDFs and Web-Pages so be open to that.
> Strictly use "openrouter/free" as the model name in the AI Engine. no other models are allowed.
>
> You are allowed to choose your own paths in case of any ambiguity.
> Stick to modular and clean code as much as possible.
>
> Firstly, list out the architecture requirements according to the context provided and do not stop till the checklist is completed.
>
> You are not allowed to hamper with any data. No numeric data values can be added without proof. This is Legal Matter. Either send pure truth or send out whatever truth you have available."

This second message is the origin of the entire `ai_engine/` module. Every constraint in it is treated as load-bearing (see §12).

---

## 3. Scope Decisions & Rationale

Two decisions were surfaced to the user via clickable questions before backend work began (the PRD alone under-specifies feasibility-critical choices):

### Decision 1 — Underlying institutional/rules/caseload data source
**Options presented:** (a) seeded reference dataset with source citations, (b) stub/mock data only, (c) user supplies the real data.
**Chosen:** **(a) Seeded reference dataset.**
**Why this was asked at all:** Live scraping of LCIA/HKIAC/ICDR/SIAC in one pass was judged unsafe — fragile scrapers, no legal-accuracy guarantee, and a legal decision-support tool that silently fabricates or misreads caseload statistics is actively harmful, not just low-quality.
**Consequence:** `backend/app/seed/reference_data.py` was built with two tiers of data: structural facts (seat names, supervisory courts, institution home seats — asserted as true) and quantitative facts (fee tiers, annual caseload numbers — explicitly `verified=False` placeholders with a `source_url` and a docstring warning not to trust them until a human confirms them against the cited primary source).

### Decision 2 — Build scope for the first pass
**Options presented:** (a) full scaffold (all 5 pages, frontend + backend), (b) backend only, (c) one vertical slice (Seat Allocation only, end to end).
**Chosen:** **(b) Backend only.**
**Consequence:** No React/TypeScript frontend exists yet. Every one of the PRD's 5 pages has a corresponding, fully working REST API, but no UI.

### Decision 3 — AI Engine coupling to backend
Not asked as a formal question (the user's second message left it "your own path in case of any ambiguity"). Resolved unilaterally as: **the AI Engine is fully decoupled from `backend/`.** It has its own SQLite fact store and its own JSON corpus cache. It does not write into the backend's PostgreSQL schema directly. `ai_engine/storage/export.py` produces a JSON bundle shaped for a human (or a follow-up task) to load into the backend explicitly. Rationale documented in `ai_engine/CHECKLIST.md` §"Design decisions," point 2: this is what "a completely separate module" was taken to mean literally, and it avoids a fully-automated agent writing directly into a legal-data production database with no human checkpoint.

### Decision 4 — RAG retrieval mechanism
Not asked as a question either (same "choose your own path" clause). Resolved as: **local BM25 (`rank-bm25` library), not a second hosted embedding model.** Rationale: introducing a second API-based embedding model would quietly violate the spirit of "strictly use openrouter/free... no other models are allowed" even though that instruction was literally about the *generation* model. BM25 needs no API key and runs entirely locally.

### Decision 5 — Tool set exposed to the extraction agent
Kept deliberately small: `search_corpus`, `fetch_source`, `list_ingested_sources`. No general web-browsing tool, no arbitrary code execution tool. Rationale: auditability — every action the model can take is enumerable and inspectable in `ai_engine/core/tools.py`.

---

## 4. Repository Layout

```
arbitrium/
├── CHECKLIST.md                     # backend engineering checklist (PRD-mandated)
├── iteration1.md                    # original PRD, as supplied
├── PROJECT_REFERENCE.md             # this file
│
├── backend/                         # FastAPI + PostgreSQL — PRD pages 1-5 as REST APIs
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/0001_initial.py
│   ├── uploads/                     # local disk storage for uploaded contracts
│   ├── app/
│   │   ├── main.py                  # FastAPI app, CORS, router wiring
│   │   ├── core/
│   │   │   ├── config.py            # pydantic-settings Settings
│   │   │   └── security.py          # bcrypt hashing, JWT encode/decode
│   │   ├── db/
│   │   │   ├── base_class.py        # SQLAlchemy DeclarativeBase
│   │   │   ├── base.py              # imports all models for metadata registration
│   │   │   └── session.py           # engine, SessionLocal, get_db dependency
│   │   ├── models/                  # 12 SQLAlchemy ORM models — see §6
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── recommendation_engine.py
│   │   │   ├── cost_estimator.py
│   │   │   ├── clause_generator.py
│   │   │   └── contract_parser.py
│   │   ├── api/
│   │   │   ├── deps.py              # get_current_user / get_current_user_optional
│   │   │   └── v1/
│   │   │       ├── router.py        # aggregates all endpoint routers
│   │   │       └── endpoints/       # auth, dashboard, seats, rules, seat_allocation, clauses, cost_estimate
│   │   └── seed/
│   │       ├── reference_data.py    # curated seed dataset — see §9
│   │       └── seed_db.py           # idempotent loader script
│   └── tests/                       # 12 pytest tests, all offline (no DB needed)
│
└── ai_engine/                       # standalone Python module — RAG extraction agent
    ├── README.md
    ├── CHECKLIST.md                 # AI Engine architecture checklist
    ├── requirements.txt
    ├── .env                         # LOCAL ONLY, gitignored — holds the real OpenRouter key
    ├── .env.example
    ├── .gitignore
    ├── main.py                      # CLI: ingest / sources / extract / export
    ├── core/
    │   ├── config.py                # Settings, model-lock enforcement
    │   ├── client.py                # OpenRouterClient wrapper (OpenAI SDK)
    │   ├── tools.py                 # tool JSON schemas + ToolRegistry
    │   └── agent_loop.py            # the agentic tool-calling loop
    ├── ingestion/
    │   ├── fetch.py                 # PDF/HTML fetch + text extraction
    │   ├── chunker.py                # overlapping chunking with char-span provenance
    │   └── corpus_store.py          # JSON persistence + BM25Plus retrieval
    ├── extraction/
    │   ├── schemas.py               # ExtractedFact / ExtractionResult Pydantic models
    │   ├── system_prompt.py         # the extraction agent's system prompt
    │   ├── extractor.py             # drives the agent loop, parses output
    │   └── hallucination_guard.py   # verbatim-excerpt + numeric-plausibility check
    ├── storage/
    │   ├── fact_store.py            # SQLite CRUD for accepted facts
    │   └── export.py                # JSON bundle export
    ├── data/
    │   ├── corpus/                  # gitignored — ingested document chunks (JSON per source)
    │   └── facts/                   # gitignored — facts.db (SQLite) + export.json
    └── tests/                       # 28 pytest tests, all offline/mocked
```

---

## 5. Backend — Architecture

**Stack:** FastAPI 0.115.0, SQLAlchemy 2.0.35 (2.0-style `Mapped`/`mapped_column` declarative models), PostgreSQL via `psycopg2-binary`, Alembic 1.13.2 for migrations, Pydantic 2.9.2 / pydantic-settings 2.5.2 for validation, `python-jose` for JWT, `passlib` + `bcrypt` for password hashing.

**Layering:**
```
HTTP request
  → app/api/v1/endpoints/*.py   (FastAPI route handlers — thin, no business logic)
  → app/schemas/*.py            (Pydantic validation of request body)
  → app/services/*.py           (business logic — pure-ish, mostly DB-read + compute)
  → app/models/*.py             (SQLAlchemy ORM — DB read/write)
  → PostgreSQL
```

Auth is JWT bearer-token based, but **every content-producing endpoint works for guests too** (no `Authorization` header). When a request does carry a valid token, results are attributed to that user and become visible on their dashboard; when it doesn't, results are computed and returned but not tied to any account. This directly implements the PRD's "Guest State" vs. "Authenticated State" split from Page 1 — one code path, not two.

CORS is enabled via `CORSMiddleware`, origins configurable through `CORS_ORIGINS` env var (comma-separated), defaulting to `http://localhost:5173,http://localhost:3000` (Vite / CRA dev server defaults, anticipating the not-yet-built React frontend).

---

## 6. Backend — Database Schema (full field-level detail)

All tables defined via SQLAlchemy 2.0 `Mapped`/`mapped_column`. Alembic migration `0001_initial.py` mirrors this exactly (hand-written, not autogenerated, since no live Postgres instance was available in the build sandbox to autogenerate against).

### `users`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| email | String(255) | unique, indexed |
| hashed_password | String(255) | bcrypt hash |
| full_name | String(255) | nullable |
| created_at | DateTime(tz) | server_default now() |

### `seats`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| name | String(120) | unique — e.g. "Singapore", "London, UK" |
| country | String(120) | |
| ny_convention_member | Boolean | default True |
| supervisory_court | String(255) | nullable |
| governing_statute | String(255) | nullable |
| notes | Text | nullable |

### `institutions`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| short_code | String(20) | unique — e.g. "SIAC", "LCIA", "ADHOC" |
| name | String(255) | |
| website_url | String(500) | nullable |
| home_seat_id | Integer FK → seats.id | nullable |

### `institution_rules` (feeds PRD Page 3 — Live Rule Tracking)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| institution_id | Integer FK → institutions.id | |
| rules_name | String(255) | e.g. "SIAC Rules 2025" |
| version_year | Integer | nullable |
| effective_date | Date | nullable |
| summary | Text | nullable |
| source_url | String(500) | not null — the citation |
| last_checked_at | DateTime(tz) | server_default now() |

### `annual_report_stats` (feeds PRD §4 — Cross-Border Data Index)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| institution_id | Integer FK → institutions.id | |
| report_year | Integer | |
| new_cases_filed | Integer | nullable — **left null in seed data, see §9** |
| avg_claim_value_usd | Float | nullable — **left null in seed data** |
| avg_duration_months | Float | nullable — **left null in seed data** |
| source_url | String(500) | not null |
| verified | Boolean | default False |
| notes | Text | nullable |

### `fee_schedules` (feeds PRD Page 5 — Cost and Duration Estimate)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| institution_id | Integer FK → institutions.id | |
| schedule_name | String(255) | |
| currency | String(10) | default "USD" |
| admin_fee_tiers | JSON | list of `{claim_min, claim_max, base, rate_pct}` |
| tribunal_fee_tiers | JSON | same shape |
| typical_duration_months_min | Integer | nullable |
| typical_duration_months_max | Integer | nullable |
| source_url | String(500) | not null |
| verified | Boolean | default False |

### `seat_institution_ratings` (feeds the recommendation engine)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| seat_id | Integer FK → seats.id | |
| institution_id | Integer FK → institutions.id | |
| speed_score | Integer | 1-5, curated |
| cost_score | Integer | 1-5, curated |
| neutrality_score | Integer | 1-5, curated |
| enforceability_score | Integer | 1-5, curated |
| rationale | Text | nullable — human-readable justification for the scores |

### `contract_uploads` (PRD Page 2 — "Upload Contract" intake)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| user_id | Integer FK → users.id | nullable (guest uploads allowed) |
| filename | String(500) | original filename |
| storage_path | String(1000) | local disk path under `uploads/` |
| status | String(30) | default "processed"; "extraction_failed" on parse error |
| extracted_parties | JSON | nullable, list of `{name, role}` |
| extracted_scope | String(2000) | nullable |
| extracted_claim_quantum | Float | nullable |
| extracted_claim_currency | String(10) | nullable |
| extracted_governing_law | String(255) | nullable |
| created_at | DateTime(tz) | server_default now() |

### `seat_allocation_requests` (PRD Page 2 core workflow, input side)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| user_id | Integer FK → users.id | nullable |
| contract_upload_id | Integer FK → contract_uploads.id | nullable |
| arbitration_type | String(20) | "domestic" \| "cross_border" |
| parties | JSON | nullable |
| scope | Text | nullable |
| claim_quantum | Float | nullable |
| claim_currency | String(10) | nullable |
| governing_law | String(255) | nullable |
| priority_speed | Float | default 0.25 |
| priority_cost | Float | default 0.25 |
| priority_neutrality | Float | default 0.25 |
| priority_enforceability | Float | default 0.25 |
| created_at | DateTime(tz) | server_default now() |

### `seat_allocation_results` (PRD Page 2 core workflow, output side)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| request_id | Integer FK → seat_allocation_requests.id | |
| rank | Integer | 1 = top recommendation |
| seat_id | Integer FK → seats.id | |
| institution_id | Integer FK → institutions.id | |
| score | Float | weighted score, 0-1 |
| rationale | Text | not null |
| pros | JSON | list of strings |
| cons | JSON | list of strings |
| citations | JSON | list of `{label, url, type}` |

### `clauses` (PRD Page 4)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| user_id | Integer FK → users.id | nullable |
| source_seat_allocation_result_id | Integer FK → seat_allocation_results.id | nullable — links back to Page 2 if the clause was generated via the "Clause Output Integration" CTA |
| seat_id | Integer FK → seats.id | |
| institution_id | Integer FK → institutions.id | |
| num_arbitrators | String(30) | "sole" \| "three" \| "emergency" |
| appointment_mechanism | String(50) | "institutional_default" \| "co_arbitrator_nomination" \| "presiding_officer" |
| language | String(60) | |
| governing_law_contract | String(255) | |
| governing_law_arbitration | String(255) | |
| party_details | JSON | nullable |
| generated_text | Text | not null |
| pathology_check_notes | JSON | not null — list of strings, always at least one entry |
| created_at | DateTime(tz) | server_default now() |

### `cost_estimates` (PRD Page 5)
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| user_id | Integer FK → users.id | nullable |
| institution_id | Integer FK → institutions.id | |
| claim_amount | Float | |
| currency | String(10) | default "USD" |
| estimated_admin_fee | Float | |
| estimated_tribunal_fee_min | Float | |
| estimated_tribunal_fee_max | Float | |
| estimated_duration_months_min | Integer | |
| estimated_duration_months_max | Integer | |
| breakdown | JSON | full calculation trace, see §8 |
| created_at | DateTime(tz) | server_default now() |

---

## 7. Backend — API Surface (full request/response detail)

Base path: `/api/v1`. Interactive docs at `/docs` (FastAPI auto-generated). Health check at `/health` (no prefix).

### Auth (`app/api/v1/endpoints/auth.py`)
| Method | Path | Auth | Body / Params | Response |
|---|---|---|---|---|
| POST | `/auth/register` | none | `{email, password, full_name?}` | `UserRead` (201) |
| POST | `/auth/login` | none | form-encoded `username`, `password` (OAuth2PasswordRequestForm — `username` field carries the email) | `{access_token, token_type: "bearer"}` |
| GET | `/auth/me` | bearer required | — | `UserRead` |

JWT: `python-jose`, algorithm `HS256`, subject claim = user's email, expiry from `ACCESS_TOKEN_EXPIRE_MINUTES` (default 1440 = 24h).

### Dashboard (`dashboard.py`)
| Method | Path | Auth | Response |
|---|---|---|---|
| GET | `/dashboard` | optional | Guest: `{authenticated: false, headline, capabilities[], cta}`. Authenticated: `{authenticated: true, welcome_message, seat_allocations[], clauses_generated[]}` (each list capped at 20, newest first) |

### Seats / Institutions (`seats.py`)
| Method | Path | Response |
|---|---|---|
| GET | `/seats` | `SeatRead[]`, ordered by name |
| GET | `/institutions` | `InstitutionRead[]`, ordered by name |

### Rules (`rules.py`) — PRD Page 3
| Method | Path | Params | Response |
|---|---|---|---|
| GET | `/rules` | `institution_id?` (query) | `InstitutionRuleRead[]` |
| GET | `/rules/sources` | — | `SourceIndexEntry[]` — combines `institution_rules` + `annual_report_stats` into one citation index (`{label, source_url, category}`) |

### Seat Allocation (`seat_allocation.py`) — PRD Page 2
| Method | Path | Auth | Body | Response |
|---|---|---|---|---|
| POST | `/seat-allocation/upload-contract` | optional | multipart `file` (.pdf or .docx only) | `ContractUploadRead` |
| POST | `/seat-allocation/analyze` | optional | `SeatAllocationAnalyzeRequest` (below) | `SeatAllocationResponse` |
| GET | `/seat-allocation/{request_id}` | none | — | `SeatAllocationResponse` |

**`SeatAllocationAnalyzeRequest` body shape:**
```json
{
  "arbitration_type": "domestic" | "cross_border",
  "contract_upload_id": null,
  "parties": [{"name": "...", "role": "...", "jurisdiction": "..."}],
  "scope": "string or null",
  "claim_quantum": 0,
  "claim_currency": "USD",
  "governing_law": "string or null",
  "priority_speed": 0.25,
  "priority_cost": 0.25,
  "priority_neutrality": 0.25,
  "priority_enforceability": 0.25
}
```
The four `priority_*` fields are validated by a Pydantic `field_validator` to sum to 1.0 (±0.01 tolerance) — this is the "Manual Preferences (Always Required)" rule from the PRD enforced at the schema layer, not just in the UI.

**`SeatAllocationResponse` shape:**
```json
{
  "request_id": 1,
  "arbitration_type": "cross_border",
  "created_at": "...",
  "results": [
    {
      "rank": 1,
      "seat_id": 2,
      "institution_id": 4,
      "score": 0.9,
      "rationale": "Singapore seated arbitration under SIAC scores 0.90/1.00 given your stated priorities...",
      "pros": ["Speed (time to award): 4/5", "Cost (administrative & tribunal fees): 4/5"],
      "cons": [],
      "citations": [{"label": "SIAC Rules 2025", "url": "https://siac.org.sg/siac-rules-2025", "type": "rules"}, ...]
    }
  ]
}
```
Returns HTTP 422 if no eligible seat/institution pair exists for the given inputs (e.g. `arbitration_type=domestic` with a `governing_law` matching no seeded seat's country and no fallback available).

### Clauses (`clauses.py`) — PRD Page 4
| Method | Path | Auth | Body | Response |
|---|---|---|---|---|
| POST | `/clauses/generate` | optional | `ClauseGenerateRequest` (below) | `ClauseRead` |
| GET | `/clauses/{clause_id}` | none | — | `ClauseRead` |
| GET | `/clauses` | optional | — | `ClauseRead[]` (empty list for guests; own clauses, newest first, for authenticated users) |

**`ClauseGenerateRequest` body shape:**
```json
{
  "source_seat_allocation_result_id": null,
  "seat_id": 2,
  "institution_id": 4,
  "num_arbitrators": "sole" | "three" | "emergency",
  "appointment_mechanism": "institutional_default" | "co_arbitrator_nomination" | "presiding_officer",
  "language": "English",
  "governing_law_contract": "Singapore",
  "governing_law_arbitration": "Singapore",
  "party_details": [{"name": "...", "role": "...", "jurisdiction": "..."}]
}
```

### Cost Estimate (`cost_estimate.py`) — PRD Page 5
| Method | Path | Auth | Body | Response |
|---|---|---|---|---|
| POST | `/cost-estimate/calculate` | optional | `{institution_id, claim_amount, currency}` | `CostEstimateRead` |

Returns HTTP 404 if no `FeeSchedule` row exists for the given `institution_id`.

---

## 8. Backend — Services (algorithms, low level)

### 8.1 Recommendation Engine (`app/services/recommendation_engine.py`)

**Purpose:** the algorithm behind PRD Page 2's "Recommendation Rationale," "Pros & Cons," and "Sourced Citations."

**Design philosophy, stated explicitly in the module docstring:** *"Deliberately transparent and deterministic rather than a black-box model: every score is a weighted sum of curated 1-5 ratings (SeatInstitutionRating), and every citation traces back to a stored source_url from the seed reference data."*

**Algorithm, step by step:**
1. `_eligible_ratings(db, arbitration_type, governing_law)` filters the full `seat_institution_ratings` table:
   - `arbitration_type == "cross_border"` → keep only seats where `ny_convention_member == True`.
   - `arbitration_type == "domestic"` and `governing_law` given → keep ratings where `rating.seat.country.lower()` appears as a substring of `governing_law.lower()`. If that yields zero matches, or `governing_law` is not given, **fall back to the full unfiltered rating set** rather than returning empty.
2. For each surviving rating, `_weighted_score` computes:
   ```
   score = (speed_score * priority_speed
          + cost_score * priority_cost
          + neutrality_score * priority_neutrality
          + enforceability_score * priority_enforceability) / 5.0
   ```
   (division by 5 normalizes the 1-5 rating scale to a 0-1 score range, since weights already sum to 1.0).
3. `_pros_cons` ranks the four dimension scores for that rating descending, takes the top 2 as `pros` (formatted `"{label}: {score}/5"`), and takes any of the bottom 2 that are `<= 3` as `cons` (so a uniformly strong rating produces an empty `cons` list — this is intentional, seen live in the validated test run where SIAC's top result had `cons: []`).
4. `_citations` pulls every `InstitutionRule` and `AnnualReportStat` row for that institution and formats them as `{label, url, type}`.
5. `rationale` string template: `"{seat.name} seated arbitration under {institution.name} scores {score:.2f}/1.00 given your stated priorities (weighted most heavily on {top_factor}). {rating.rationale}"` — `top_factor` is whichever of the four priority weights the user set highest.
6. Candidates are sorted by score descending; top 3 (`top_n` param, default 3) are returned.

### 8.2 Cost Estimator (`app/services/cost_estimator.py`)

**Purpose:** PRD Page 5.

**Algorithm:** tiered ad-valorem calculation. Each `FeeSchedule` row stores `admin_fee_tiers` and `tribunal_fee_tiers` as JSON lists of `{claim_min, claim_max (nullable = open-ended), base, rate_pct}`.

`_apply_tiers(tiers, claim_amount)`:
```python
for tier in tiers:
    if claim_amount >= tier.claim_min and (tier.claim_max is None or claim_amount < tier.claim_max):
        portion = claim_amount - tier.claim_min
        return round(tier.base + portion * (tier.rate_pct / 100.0), 2)
# fallback: claim below lowest tier's floor → use first tier's base fee
return tiers[0].base
```

Tribunal fee range: point estimate computed the same way, then **±20% band** applied (`tribunal_min = point * 0.8`, `tribunal_max = point * 1.2`) — documented rationale in-code: *"Tribunal fees vary more with tribunal composition/complexity than admin fees do."*

Response `breakdown` field includes: `schedule_name`, `currency`, `claim_amount`, `admin_fee`, `tribunal_fee_point_estimate`, `tribunal_fee_range`, `source_url`, `verified` — i.e. the full calculation trace is always returned, not just the final numbers, so a lawyer reviewing the estimate can see exactly which tier and rate produced it.

**Verified live example (SIAC, claim = 500,000 USD):**
```json
{
  "estimated_admin_fee": 7000.0,
  "estimated_tribunal_fee_min": 18400.0,
  "estimated_tribunal_fee_max": 27600.0,
  "estimated_duration_months_min": 12,
  "estimated_duration_months_max": 18,
  "breakdown": {
    "admin_fee": 7000.0,
    "tribunal_fee_point_estimate": 23000.0,
    "tribunal_fee_range": [18400.0, 27600.0],
    "source_url": "https://siac.org.sg/siac-rules-2025",
    "verified": false
  }
}
```
Note `"verified": false` is carried all the way through to the API response — a consumer of this endpoint cannot miss that these are illustrative, not the institution's real published figures.

### 8.3 Clause Generator (`app/services/clause_generator.py`)

**Purpose:** PRD Page 4, including the "pathology-checked" requirement.

**Design note (explicit in-code):** uses a generic clause skeleton common to essentially all institutional model clauses, rather than reproducing any single institution's copyrighted model clause verbatim.

**Template structure (4 paragraphs):**
1. Dispute-reference paragraph: `"Any dispute, controversy, or claim arising out of or relating to this contract... shall be referred to and finally resolved by arbitration administered by {administering_body} under {rules_reference}..."`
   - `_administering_body`: for `short_code == "ADHOC"` → `"an ad hoc tribunal constituted under those rules, with no administering institution"`; otherwise → `"{institution.name} (\"{short_code}\")"`.
   - `_rules_reference`: for `ADHOC` → `"the UNCITRAL Arbitration Rules"`; otherwise → `"the Arbitration Rules of {institution.name} (the \"Rules\")"`.
2. Seat paragraph: `"The seat (legal place) of arbitration shall be {seat.name}, {seat.country}."`
3. Tribunal composition paragraph, using lookup tables:
   - `ARBITRATOR_COUNT_TEXT`: `sole` → `"a sole arbitrator"`; `three` → `"three (3) arbitrators"`; `emergency` → `"a sole arbitrator, provided that either party may apply for the emergency arbitrator provisions of the applicable rules pending constitution of the tribunal"`.
   - `APPOINTMENT_TEXT`: `institutional_default` → `"in accordance with the default appointment procedure of the applicable rules"`; `co_arbitrator_nomination` → `"with each party nominating one co-arbitrator and the two co-arbitrators nominating the presiding arbitrator"`; `presiding_officer` → `"with the presiding arbitrator appointed by the appointing authority under the applicable rules"`.
4. Language + governing-law paragraph.

**Pathology checks (`check_pathologies`), exact rules:**
| Condition | Note emitted |
|---|---|
| `num_arbitrators == "sole"` and `appointment_mechanism == "co_arbitrator_nomination"` | "Co-arbitrator nomination is inconsistent with a sole-arbitrator tribunal (there are no co-arbitrators to nominate); the institutional default appointment procedure will apply instead." |
| `num_arbitrators == "three"` and `appointment_mechanism == "presiding_officer"` | "Presiding-officer appointment alone does not specify how the two co-arbitrators are nominated for a three-member tribunal; consider co-arbitrator nomination plus a presiding-officer mechanism instead." |
| `institution.short_code == "ADHOC"` and `appointment_mechanism == "institutional_default"` | "Ad hoc arbitration has no administering institution to apply an 'institutional default'..." |
| `institution.home_seat_id != seat.id` (institution being used outside its home jurisdiction) | "{short_code}'s home jurisdiction differs from the selected seat ({seat.name}); confirm {short_code} can administer cases seated outside its home jurisdiction..." |
| `len(party_details) < 2` | "Fewer than two parties supplied — a clause needs at least two identified parties to be complete." |
| none of the above triggered | "No pathologies detected against the structural checks applied." (always at least one entry in the list) |

**Verified live example** (Singapore seat, SIAC, three arbitrators, co-arbitrator nomination, clean config): pathology_check_notes = `["No pathologies detected against the structural checks applied."]`. Sole arbitrator + co-arbitrator nomination correctly triggered the first pathology note in the live smoke test.

### 8.4 Contract Parser (`app/services/contract_parser.py`)

**Purpose:** the PRD's "automated extraction module" for the "Upload Contract" intake path.

**Explicit scope disclaimer in-code:** *"Not a legal-NLP system: uses regex/keyword heuristics... Extraction results are always presented to the user as editable defaults, never as final data."*

**Text extraction:** `.pdf` via `pdfplumber` (page-by-page `extract_text()`, joined with newlines); `.docx` via `python-docx` (`paragraph.text` joined with newlines). Any other extension raises `ValueError`.

**Extraction heuristics (regex, exact patterns):**
- **Parties:** `r"between\s+(.+?)\s+\(.*?\)\s+and\s+(.+?)\s+\(.*?\)"` (case-insensitive) — matches the common "between X (the "Claimant") and Y (the "Respondent")" contract phrasing. Produces `[{"name": ..., "role": "Party A"}, {"name": ..., "role": "Party B"}]`.
- **Governing law:** `r"govern(?:ed|ing)\s+(?:by|in accordance with)\s+the\s+laws?\s+of\s+([A-Z][A-Za-z\s]+?)(?:[.,;\n]|$)"`.
- **Claim quantum:** `r"(USD|US\$|\$|INR|Rs\.?|GBP|£|EUR|€|SGD|HKD)\s?([\d,]+(?:\.\d+)?)\s?(million|mn|crore|lakh)?"` — first match only, with a multiplier map (`million`/`mn` → ×1,000,000; `crore` → ×10,000,000; `lakh` → ×100,000) and a currency-symbol-to-ISO-code map.
- **Scope:** the first paragraph (split on `\n`) longer than 80 characters, truncated to 1000 chars.

**Verified live test** (synthetic .docx): correctly extracted `parties=[{"name":"Acme Corp","role":"Party A"},{"name":"Globex Ltd","role":"Party B"}]`, `governing_law="Singapore"`, `claim_quantum=2500000.0`, `claim_currency="USD"` from a sentence reading "The total contract value is USD 2,500,000."

---

## 9. Backend — Seed Reference Data (every source, every value)

File: `backend/app/seed/reference_data.py`. Full module docstring (verbatim, this is the data-integrity contract for the whole seed set):

> "IMPORTANT — read before trusting this data in production: `SEATS`, `INSTITUTIONS`: structural/factual... low risk of being wrong. `INSTITUTION_RULES`: the five primary rule sources named explicitly in the PRD... URLs and titles are taken verbatim from the PRD. `ANNUAL_REPORT_STATS`: the four primary annual-report sources named in the PRD. Numeric fields... are deliberately left as `None` and `verified=False`... fabricating plausible-looking statistics for a legal decision-support tool would be actively harmful. `FEE_SCHEDULES`: tier structure... is representative... but the specific base/rate figures are illustrative placeholders, not the institutions' real published fee tables. `SEAT_INSTITUTION_RATINGS`: qualitative 1-5 judgments... not derived from a single hard metric."

### 9.1 Seats (6 rows)
| name | country | NY Convention | supervisory_court | governing_statute |
|---|---|---|---|---|
| London, UK | United Kingdom | true | High Court of Justice (Commercial Court) | Arbitration Act 1996 (England & Wales) |
| Singapore | Singapore | true | Singapore International Commercial Court / High Court | International Arbitration Act 1994 |
| Hong Kong SAR | Hong Kong SAR, China | true | Hong Kong Court of First Instance | Arbitration Ordinance (Cap. 609) |
| New York, USA | United States | true | U.S. District Court (S.D.N.Y.) / New York State courts | Federal Arbitration Act; New York CPLR Article 75 |
| Mumbai, India | India | true | Bombay High Court | Arbitration and Conciliation Act 1996 (India) |
| New Delhi, India | India | true | Delhi High Court | Arbitration and Conciliation Act 1996 (India) |

### 9.2 Institutions (6 rows)
| short_code | name | website_url | home_seat |
|---|---|---|---|
| LCIA | London Court of International Arbitration | https://www.lcia.org/ | London, UK |
| HKIAC | Hong Kong International Arbitration Centre | https://hkiac.org/ | Hong Kong SAR |
| ICDR | International Centre for Dispute Resolution (AAA) | https://www.icdr.org/ | New York, USA |
| SIAC | Singapore International Arbitration Centre | https://siac.org.sg/ | Singapore |
| MCIA | Mumbai Centre for International Arbitration | https://mcia.org.in/ | Mumbai, India |
| ADHOC | Ad Hoc (UNCITRAL Rules, no administering institution) | null | null |

### 9.3 Institution Rules (5 rows — exactly the PRD Page 3 sources)
| institution | rules_name | version_year | source_url |
|---|---|---|---|
| LCIA | LCIA Arbitration Rules 2020 | 2020 | https://www.lcia.org/Dispute_Resolution_Services/lcia-arbitration-rules-2020.aspx |
| HKIAC | HKIAC 2024 Administered Arbitration Rules | 2024 | https://hkiac.org/arbitration/rules-and-practice-notes/2024-administered-arbitration-rules/ |
| HKIAC | HKIAC Procedures for Administration under UNCITRAL Rules (2015) | 2015 | https://hkiac.org/arbitration/rules-and-practice-notes/2015-procedures-administration-under-uncitral-rules/ |
| ICDR | ICDR Rules, Forms & Fees | null | https://www.icdr.org/rules_forms_fees |
| SIAC | SIAC Rules 2025 | 2025 | https://siac.org.sg/siac-rules-2025 |

### 9.4 Annual Report Stats (4 rows — exactly the PRD §4 sources; **all numeric fields null, `verified=false`**)
| institution | report_year | source_url |
|---|---|---|
| ICDR | 2024 | https://www.adr.org/annual-reports/ |
| HKIAC | 2024 | https://hkiac.org/about-us/annual-report/ |
| LCIA | 2024 | https://www.lcia.org/lcia/reports.aspx |
| SIAC | 2024 | https://siac.org.sg/annual-reports |

`report_year: 2024` here is a *placeholder tag for "most recent," not a verified claim about what year the actual report covers* — flagged explicitly so this isn't mistaken for a sourced fact.

### 9.5 Fee Schedules (6 rows, one per institution — **all `verified=false`**)
Tier template (illustrative, NOT real published figures):
```
admin (base template):    [0-100k: base 1000, 2.0%] [100k-1M: base 3000, 1.0%] [1M-10M: base 12000, 0.5%] [10M+: base 57000, 0.1%]
tribunal (base template):  [0-100k: base 5000, 6.0%] [100k-1M: base 11000, 3.0%] [1M-10M: base 38000, 1.5%] [10M+: base 173000, 0.3%]
```
Per-institution multipliers applied to base/rate (`_tiers(base_multiplier, rate_multiplier, admin)`):
| institution | base_multiplier | rate_multiplier | typical_duration (months) |
|---|---|---|---|
| LCIA | 1.1 | 1.1 | 12-24 |
| HKIAC | 1.0 | 1.0 | 12-20 |
| ICDR | 1.15 | 1.15 | 12-24 |
| SIAC | 1.0 | 1.0 | 12-18 |
| MCIA | 0.5 | 0.6 | 12-24 |
| ADHOC | 0.05 (admin) | 0.4 (tribunal) | 15-30 |

### 9.6 Seat/Institution Ratings (7 rows — the recommendation engine's actual input data)
| seat | institution | speed | cost | neutrality | enforceability | rationale (verbatim) |
|---|---|---|---|---|---|---|
| London, UK | LCIA | 4 | 3 | 5 | 5 | "Mature supervisory courts and deep NY Convention enforcement case law; premium cost profile relative to Asian hubs." |
| Singapore | SIAC | 4 | 4 | 5 | 5 | "Consistently ranked among the most-used neutral cross-border seats with efficient case management and strong enforcement record." |
| Hong Kong SAR | HKIAC | 4 | 4 | 4 | 4 | "Strong Asia-Pacific hub with UNCITRAL-track and administered options; enforcement generally reliable via NY Convention through China's accession." |
| New York, USA | ICDR | 3 | 3 | 4 | 5 | "Preferred where US-connected assets or parties are involved; proceedings can run longer due to broader discovery norms." |
| Mumbai, India | MCIA | 3 | 5 | 3 | 3 | "Lower administrative cost; still building international caseload track record relative to the four established hubs above; India-seated award enforcement can face domestic court delays in contested cases." |
| New Delhi, India | ADHOC | 2 | 5 | 3 | 3 | "Lowest direct cost (no institutional admin fee) but slower without institutional case-management deadlines; suitable mainly for domestic disputes under the Arbitration and Conciliation Act 1996." |
| Mumbai, India | ADHOC | 2 | 5 | 3 | 3 | "Same ad hoc trade-offs as New Delhi; relevant for domestic Mumbai-seated disputes." |

These 7 rows are the entire basis of every seat recommendation the system currently produces. This is a deliberately small, curated, human-written dataset — not derived from any statistical model.

---

## 10. Backend — Auth

- Passwords hashed with `passlib.CryptContext(schemes=["bcrypt"])`.
- JWT: `python-jose`, `HS256`, claims = `{"sub": email, "exp": ...}`.
- `POST /auth/login` uses `OAuth2PasswordRequestForm` (form-encoded `username`/`password`, `username` carries the email) — chosen specifically so FastAPI's `/docs` Swagger "Authorize" button works out of the box against `tokenUrl="/api/v1/auth/login"`.
- `app/api/deps.py` exposes two dependencies: `get_current_user_optional` (returns `User | None`, never raises — used by every content endpoint to support guests) and `get_current_user` (raises 401 if no valid token — used only by `/auth/me`).

---

## 11. Backend — Validation Run & Bugs Found

**Environment:** Python 3.11.4, fresh venv, `pip install -r requirements.txt`.

**Bug found #1 — passlib/bcrypt incompatibility.** Original `requirements.txt` pinned `passlib[bcrypt]==1.7.4` with no bcrypt version pin. Resolved bcrypt was 5.0.0, which removed the `__about__` attribute that passlib 1.7.4 reads to detect the backend version, causing every password hash/verify call to raise `AttributeError` (surfaced as a 500 on `/auth/register`). **Fix:** pinned `bcrypt==4.0.1` explicitly alongside `passlib==1.7.4`.

**Test suite:** `pytest` — 12/12 passing, all pure-logic (no DB required): `test_recommendation_engine.py`, `test_cost_estimator.py`, `test_clause_generator.py`.

**Full API smoke test** (FastAPI `TestClient` against a throwaway SQLite DB, standing in for Postgres — no Postgres server was available in the build sandbox): seed script → guest dashboard → seats/institutions/rules listing → register/login/me → authenticated dashboard → seat-allocation analyze (cross-border, Singapore governing law) → top result was SIAC/Singapore at score 0.9 with citations → clause generation (three arbitrators, co-arbitrator nomination, clean pathology result) → cost estimate calculation (SIAC, 500,000 USD claim) → dashboard history populated with 1 seat allocation + 1 clause. **All steps passed.**

**Contract parser test:** synthetic `.docx` with "between Acme Corp (the Claimant) and Globex Ltd (the Respondent)... governed by the laws of Singapore... USD 2,500,000" → all four fields extracted correctly.

**Not yet done:** running against a real PostgreSQL instance (no server available in this sandboxed build environment). JSON/DateTime column dialect behavior could theoretically differ between SQLite and Postgres, though SQLAlchemy's abstraction makes this low-risk. Flagged in `CHECKLIST.md` §8 and "Known gaps."

---

## 12. AI Engine — Purpose & Non-Negotiable Constraints

**Purpose:** turn institutional annual reports (PDF or HTML) into structured, source-cited facts (case counts by sector, party nationality, seat, duration, tribunal composition) to eventually replace the backend's `verified=False` placeholder data with real, provably-sourced numbers.

**Constraints, taken directly from the user's second message and treated as absolute:**
1. Python only.
2. A **separate module** (`ai_engine/`), not merged into `backend/`.
3. LLM calls go through the **OpenAI Python SDK** pointed at OpenRouter's OpenAI-compatible endpoint.
4. Model name **hardcoded to `openrouter/free`** — no fallback, no silent substitution, ever.
5. An **agentic loop**: the model can emit tool calls, tools execute, results feed back, loop continues until a final (non-tool-call) response or a max-iteration cap.
6. **RAG over PDFs and web pages.**
7. **Zero numeric fabrication.** "You are not allowed to hamper with any data. No numeric data values can be added without proof. This is Legal Matter. Either send pure truth or send out whatever truth you have available." — implemented as a hard validation gate (§17), not just a prompt instruction.
8. "You are allowed to choose your own paths in case of any ambiguity" — used to resolve the 5 design decisions in §3 (decisions 3-5) and §13.
9. "Firstly, list out the architecture requirements... and do not stop till the checklist is completed" — implemented as `ai_engine/CHECKLIST.md`, built and checked off item by item before declaring the module done, mirroring the PRD's own "Task Enlistment / Logs & Checklist Maintenance / Continuous Iteration Cycle" mandate from §1 above.

---

## 13. AI Engine — Design Decisions & Rationale

(Decisions 3-5 already listed in §3; reproduced here with full rationale for completeness, plus one more.)

1. **Retrieval = local BM25, not a second hosted model.** `rank-bm25` library, runs entirely in-process, no API key. Chosen specifically to avoid quietly violating "no other models allowed" even though that constraint's letter was about the generation model only.
2. **Storage = fully separate from backend Postgres.** SQLite (`data/facts/facts.db`) + JSON corpus cache (`data/corpus/*.json`), both local to `ai_engine/`. `storage/export.py` produces a reviewable JSON bundle rather than writing into backend tables automatically — a human checkpoint stays in the loop before legal-facing data changes.
3. **Ingestion scope for this pass** = general PDF+HTML pipeline wired to the 5 PRD-cited sources, not a bulk historical crawl. A full multi-year archive crawl is explicitly deferred (see §25).
4. **Tool set kept small and auditable**: exactly 3 tools (`search_corpus`, `fetch_source`, `list_ingested_sources`). No general web-browsing tool, no code execution tool.
5. **Package import structure**: no wrapping `ai_engine` package — `core/`, `ingestion/`, `extraction/`, `storage/` are top-level packages relative to the `ai_engine/` working directory (mirrors the backend's `app/`-relative-to-`backend/` pattern exactly, so `pytest` and script execution both resolve imports the same way without `PYTHONPATH` gymnastics). This was a mid-build correction — see §19.

---

## 14. AI Engine — Module-by-Module Detail

### `core/config.py`
- `REQUIRED_MODEL = "openrouter/free"` — the single source of truth.
- `Settings.__init__` reads `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL` (default `https://openrouter.ai/api/v1`), `OPENROUTER_MODEL` from env (loaded via `python-dotenv` from `ai_engine/.env`, path resolved relative to `__file__` so it works regardless of the process's cwd).
- **Raises `ConfigError` immediately** if `OPENROUTER_MODEL != REQUIRED_MODEL`, or if `OPENROUTER_API_KEY` is empty.
- `get_settings()` is a lazy singleton (not constructed at import time) — specifically so importing the module never fails during test collection before `.env` is guaranteed loaded.

### `core/client.py`
- `OpenRouterClient(model: str | None = None)`: resolves `requested = model or settings.model`; if `requested != REQUIRED_MODEL`, raises `ModelPolicyError` — **enforced again here, independently of config.py**, so even a caller that constructs the client with an explicit override string cannot bypass the lock.
- Wraps `openai.OpenAI(api_key=..., base_url=...)`.
- `.chat(messages, tools=None, **kwargs)` calls `chat.completions.create(model=REQUIRED_MODEL, ...)`, `temperature` defaulted to `0` (deterministic extraction behavior, overridable via kwargs).

### `ingestion/fetch.py`
- `fetch(url) -> FetchedDocument{url, content_type, text, fetched_at}`.
- PDF detection: `Content-Type` header contains "pdf" OR url ends in `.pdf`. PDF text via `pdfplumber`, page by page.
- HTML: `BeautifulSoup`, strips `<script>/<style>/<nav>/<footer>/<header>`, then `get_text(separator="\n")`, blank lines stripped.
- `USER_AGENT = "ArbitriumAIEngine/1.0 (research tool; contact: project maintainer)"`, 30-second timeout, `response.raise_for_status()` — failures propagate, never silently swallowed.

### `ingestion/chunker.py`
- `chunk_text(text, source_url, institution, chunk_size=1500, overlap=200) -> list[Chunk]`.
- `Chunk{source_url, institution, chunk_index, char_start, char_end, text}` — every chunk carries the **exact character span** of the original document, which is what makes the hallucination guard's excerpt-verification possible.
- Sliding window: `start = end - overlap` each iteration; empty/whitespace-only slices are skipped (index not incremented for skipped slices).
- Raises `ValueError` if `chunk_size <= overlap`.

### `ingestion/corpus_store.py`
- `CorpusStore(corpus_dir)`: one JSON file per ingested source, named by `sha256(url)[:24]` (`_slug`).
- `ingest_document(FetchedDocument, institution) -> int` (chunk count) — chunks and writes to disk.
- `search(query, top_k=5, institution=None) -> list[dict]` — loads **all** chunks from disk on every call (simple, fine for this scale), tokenizes with `_tokenize` (regex `[a-z0-9]+`, lowercased, **stopword-filtered** — see bug fix in §19), builds a **`BM25Plus`** index fresh each call, returns top-k results with `score > 0`, each result carrying `source_url, institution, chunk_index, char_start, char_end, text, score`.
- `get_source_text(source_url) -> str | None` — reassembles a source's full text by concatenating its chunks in index order (note: due to chunk overlap, this is NOT byte-identical to the original for multi-chunk documents, but every substring of the original is still findable in it — which is the only property the hallucination guard actually needs).
- `list_sources() -> list[dict]` — `{source_url, institution, content_type, fetched_at, chunk_count}` per ingested source.

### `extraction/schemas.py`
`ExtractedFact` (Pydantic):
```python
institution: str
report_year: int | None
metric: str                      # e.g. "new_cases_filed", "case_count_by_sector"
dimension: "sector"|"country"|"seat"|"tribunal_composition"|None
dimension_value: str | None      # e.g. "construction", "Singapore"
numeric_value: float | None
unit: str | None
status: "disclosed" | "not_disclosed"
source_url: str
source_excerpt: str | None
hallucination_check_passed: bool | None
```
`requires_excerpt()` → `True` iff `status == "disclosed" and numeric_value is not None`. This is the exact boundary of what the hallucination guard enforces: **numeric claims must be proven; qualitative disclosed facts (no number) are not currently excerpt-gated.**

### `extraction/extractor.py`
`extract(institution, task_description, corpus_store, client=None, max_iterations=8) -> dict`:
1. Builds messages: `[{"role":"system","content":SYSTEM_PROMPT}, {"role":"user","content":f"Institution: {institution}\nTask: {task_description}"}]`.
2. Runs `run_agent_loop`.
3. Strips markdown code fences from the final response (`FENCE_RE = r"^```(?:json)?\s*|\s*```$"`) and `json.loads`s it; raises `ExtractionError` with the raw output (truncated to 500 chars) on parse failure.
4. Constructs `ExtractedFact` per entry in `parsed["facts"]`, collecting Pydantic validation failures separately as `parse_errors` (never silently dropped).
5. Runs `filter_verified_facts` (the hallucination guard) — splits into `accepted_facts` / `rejected_facts`.
6. Returns `{institution, accepted_facts, rejected_facts, parse_errors, iterations_used, tool_calls_made, raw_model_output}`.

### `storage/fact_store.py`
SQLite table `extracted_facts` — one row per accepted `ExtractedFact`, plus `created_at` timestamp. `save()`, `save_many()`, `all()`, `by_institution()`, `close()`.

### `storage/export.py`
`export_bundle(fact_store, output_path)` — groups all stored facts by institution, writes `{exported_at, institutions: {SIAC: [...], ...}}` as pretty JSON.

### `main.py` (CLI)
```
python main.py ingest <institution> <url>
python main.py sources
python main.py extract <institution> "<task description>"
python main.py export --output data/facts/export.json
```
Run with cwd = `ai_engine/`.

---

## 15. AI Engine — Agentic Loop Mechanics

File: `core/agent_loop.py`. `run_agent_loop(client, tool_registry, messages, tools=TOOL_SCHEMAS, max_iterations=8) -> AgentRun`.

**Exact control flow:**
```
for iteration in 1..max_iterations:
    response = client.chat(conversation, tools=tools)
    message = response.choices[0].message
    if message.tool_calls is empty:
        append {"role": "assistant", "content": message.content} to conversation
        return AgentRun(messages=conversation, final_content=message.content,
                         iterations_used=iteration, tool_calls_made=[...])
    append assistant message WITH tool_calls (id, type, function{name, arguments}) to conversation
    for each tool_call in message.tool_calls:
        result = tool_registry.dispatch(tool_call.function.name, tool_call.function.arguments)
        record {name, arguments} in tool_calls_made
        append {"role": "tool", "tool_call_id": tool_call.id, "content": result} to conversation
raise AgentLoopError(f"Agent loop did not terminate within {max_iterations} iterations")
```

`AgentRun` dataclass: `messages` (full conversation, for debugging/audit), `final_content` (str), `iterations_used` (int), `tool_calls_made` (list of `{name, arguments}` dicts).

This is a genuinely recursive tool-use loop, not a single-shot function-call pattern — verified live in §19 with a real multi-turn run against ICDR's page (search → response, in that case terminating after tool use without needing `fetch_source`).

---

## 16. AI Engine — Tool Schemas (exact JSON)

From `core/tools.py`, `TOOL_SCHEMAS` (OpenAI function-calling format, passed verbatim to `client.chat(tools=...)`):

```json
[
  {
    "type": "function",
    "function": {
      "name": "search_corpus",
      "description": "Search previously-ingested document chunks (annual reports, rules pages) for text relevant to a query. Returns ranked chunks with source_url and exact char_start/char_end spans — quote directly from these, do not paraphrase numbers.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {"type": "string", "description": "Search query"},
          "institution": {"type": "string", "description": "Optional institution short code filter, e.g. SIAC"},
          "top_k": {"type": "integer", "description": "Max results (default 5)"}
        },
        "required": ["query"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_source",
      "description": "Fetch and ingest a new PDF or HTML source URL into the corpus so it can then be searched with search_corpus. Only call this for URLs you were explicitly given or that came from a prior tool result — never invent a URL.",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {"type": "string", "description": "Source URL to fetch"},
          "institution": {"type": "string", "description": "Institution short code this source belongs to, e.g. SIAC"}
        },
        "required": ["url", "institution"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "list_ingested_sources",
      "description": "List all sources currently ingested into the corpus.",
      "parameters": {"type": "object", "properties": {}}
    }
  }
]
```

`ToolRegistry.dispatch(name, arguments_json)`: parses arguments JSON (returns a JSON error string on parse failure, doesn't raise), looks up the handler, catches **any** exception from the handler and returns it as `{"error": "{ExceptionType}: {message}"}` — tool failures are always surfaced back to the model as data, never raised up through the loop and crashing the run.

---

## 17. AI Engine — Hallucination Guard (exact algorithm)

File: `extraction/hallucination_guard.py`. This is the concrete enforcement mechanism for the PRD's "no numeric data without proof" instruction — a second, independent check that does not trust the model's own citation.

`check_fact(fact: ExtractedFact, corpus_store: CorpusStore) -> (bool, str)`:
1. If `not fact.requires_excerpt()` (i.e. status is `not_disclosed`, or it's a non-numeric disclosed fact) → **pass automatically**, reason `"no excerpt required"`.
2. If `requires_excerpt()` is true but `source_excerpt` is empty → **fail**, `"numeric fact missing source_excerpt"`.
3. Look up the full reassembled text for `fact.source_url` via `corpus_store.get_source_text()`. If the URL was never ingested → **fail**, `"source_url not found in corpus"`.
4. **Verbatim substring check**: `_normalize(fact.source_excerpt) in _normalize(source_text)`, where `_normalize(text) = " ".join(text.split())` (collapses all whitespace). If the excerpt is not found → **fail**, `"source_excerpt is not a verbatim substring of the ingested source text"`.
5. **Numeric plausibility check**: `_excerpt_mentions_number(fact.source_excerpt, fact.numeric_value)` — strips commas/whitespace from the excerpt, checks whether any of several numeric string representations of `numeric_value` (raw `str()`, integer form, comma-grouped integer, 2-decimal comma-grouped) appears in it. If not → **fail**, `"numeric_value not found within the claimed source_excerpt"`. This catches the case where the excerpt is real text but doesn't actually contain the number being claimed (i.e., the model quoted something true but attached a different number to it).
6. Otherwise → **pass**, `"verified"`.

`filter_verified_facts(facts, corpus_store) -> (accepted, rejected)`: runs `check_fact` on every fact, sets `fact.hallucination_check_passed` on each, splits into accepted/rejected lists. **Rejected facts are never silently dropped** — `main.py`'s `cmd_extract` prints them to stderr with their rejection reason.

---

## 18. AI Engine — System Prompt (verbatim)

From `extraction/system_prompt.py`, `SYSTEM_PROMPT` (exact text sent as the `system` message on every extraction run):

> "You are the Arbitrium AI Engine's extraction agent. You read arbitral institutions' annual reports and rules pages and extract structured facts about case volumes, industry sectors, party nationalities, seats, tribunal composition, and case duration. This output feeds a legal decision-support tool, so accuracy discipline is absolute.
>
> Rules (non-negotiable):
> 1. Use the search_corpus and fetch_source tools to find and read source material. Never answer from prior/general knowledge about these institutions — every fact must come from text you actually retrieved in this conversation.
> 2. Every fact with a numeric_value MUST include a source_excerpt that is a VERBATIM substring of a chunk you retrieved (not paraphrased, not summarized, not rounded differently than the source states it). Copy the exact wording/number as it appears.
> 3. If the report does not disclose a figure you were asked to look for, emit a fact with status="not_disclosed", numeric_value=null, and no invented source_excerpt. Do not estimate, interpolate, average across other institutions, or infer a plausible-sounding number. Absence of data is itself a valid, useful answer.
> 4. Never mix up which institution or which report year a figure came from. If a chunk's year is ambiguous, say so via status="not_disclosed" rather than guessing.
> 5. When you are done gathering evidence, respond with your FINAL answer as a single JSON object (no prose, no markdown fences)..."

(Full JSON output schema instruction follows in the actual file — reproduced exactly in `extraction/system_prompt.py`, omitted here for brevity since it duplicates the `ExtractedFact` schema already documented in §14.)

---

## 19. AI Engine — Validation Run, Bugs Found, and Live Test Results

**Environment:** Python 3.11.4, fresh venv, `pip install -r requirements.txt`.

### Bug #1 — import structure mismatch (caught before tests even ran)
Every module was initially written with absolute imports like `from ai_engine.core.config import ...`, which only resolve if the **parent** of `ai_engine/` is on `sys.path` — inconsistent with the backend's own working pattern (cwd = `backend/`, imports = `app.X`). **Fix:** removed `ai_engine/__init__.py` (so `ai_engine/` itself is not a package) and rewrote every import to drop the `ai_engine.` prefix (`from core.config import ...`, `from ingestion.corpus_store import ...`, etc.), matching the backend's pattern exactly: run `pytest` / `python main.py` with cwd = `ai_engine/`, and `core/`, `ingestion/`, `extraction/`, `storage/`, `tests/` resolve as top-level packages.

### Bug #2 — BM25's classic IDF formula silently zeroes small-corpus scores
First full test run: `test_search_returns_relevant_chunk` failed — a 2-document corpus, query "construction cases," expected the document containing "construction" to rank first; got zero results. Root cause, isolated by direct experimentation: `BM25Okapi`'s IDF formula is `log(N - n + 0.5) - log(n + 0.5)` (no smoothing `+1` term). With `N=2` documents and a query term appearing in exactly `n=1` of them, `idf = log(1.5) - log(1.5) = 0` **exactly** — and this isn't a corner case, it's the *normal* early-stage state of this system (one or two ingested reports). **Fix:** switched to `BM25Plus` (positive-delta variant, confirmed via direct experiment to return `[4.33, 2.19]` instead of `[0, 0]` for the same corpus/query), and added a small stopword list (`STOPWORDS = {"a","an","and","are","as","at","be","by","for","from","has","in","into","is","it","of","on","or","that","the","this","to","was","were","will","with"}`) to `_tokenize` so common connective words don't dilute ranking now that BM25Plus guarantees every shared token contributes a positive score.

### Bug #3 — openai SDK / httpx version incompatibility
`test_client_accepts_required_model` failed with `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`. Root cause: `openai==1.51.0`'s internal HTTP client construction passes a `proxies` kwarg that `httpx>=0.28` removed; pip had resolved `httpx==0.28.1` by default, which is what broke it. **Fix:** pinned `httpx==0.27.2` (same fix already independently applied in `backend/requirements.txt` for the identical reason, since backend also depends on `httpx` transitively).

**After all three fixes: 28/28 pytest tests passing**, covering: agent loop control flow (immediate final message, tool-call-then-final, max-iteration exhaustion raising `AgentLoopError`, unknown-tool-name graceful handling), chunker boundary/overlap correctness, corpus store ingest/search/filter-by-institution/source-text-reassembly, hallucination guard accept/reject cases (real excerpt, invented excerpt, real-excerpt-wrong-number, not_disclosed-needs-no-excerpt, unknown-source-url, batch filter split), and client model-lock enforcement (rejects wrong model at both the `Settings` and `OpenRouterClient` layers).

### Live validation (real network + real OpenRouter API calls)

**Sanity call:** single live request to OpenRouter with `model="openrouter/free"`, prompt "Reply with exactly one word: OK". **Result: SUCCESS.** `finish_reason: "stop"`, content `"OK"`. Confirms the API key is valid and `openrouter/free` is a real, callable model id — this had genuinely been unverified until this point, since the model string was mandated but not independently confirmed to exist.

**Real end-to-end extraction run:**
- First attempt: `python main.py ingest SIAC https://siac.org.sg/annual-reports` → **HTTP 403 Forbidden**. Reported to the user as-is; no workaround attempted, no silent substitution of a different source.
- Second attempt (also a PRD-cited source): `python main.py ingest ICDR https://www.icdr.org/rules_forms_fees` → succeeded, 5 chunks ingested.
- `python main.py extract ICDR "What does this page state about ICDR/AAA case filing statistics, industry sectors handled, or fee amounts? For anything not explicitly stated in the retrieved text, mark status as not_disclosed rather than guessing."` → **live model run, real tool calls, real result:**
  ```
  Accepted facts: 5
    - case_filing_statistics [None=None] = None (not_disclosed)
    - industry_sector_scope [sector=wide variety of industries] = None (disclosed)
    - industry_specific_rules [sector=construction industry] = None (disclosed)
    - fee_schedule_options [None=standard fee or flexible fee schedule] = None (disclosed)
    - fee_amounts [None=None] = None (not_disclosed)
  ```
  All 5 facts passed the hallucination guard. Example verbatim excerpt captured: *"Construction Industry Arbitration Rules and Mediation Procedures – Amended and Effective March 1, 2024"* — independently checkable as a real, specific ICDR document title, not a plausible-sounding invention. Correctly reported `not_disclosed` for the two things the page genuinely doesn't state (case counts, fee amounts) rather than guessing.
- `python main.py export --output data/facts/export.json` produced the full JSON bundle, inspected and confirmed to contain exactly these 5 facts with their source excerpts.

**This is the single most important verification in the whole build**: the no-fabrication chain (system prompt instruction → model behavior → independent hallucination guard → export) was tested against a real live model, not just mocked unit tests, and it held.

---

## 20. Credentials & Secrets — What Exists, Where It Lives

| Secret | Location | Committed to any tracked file? | Notes |
|---|---|---|---|
| OpenRouter API key | `ai_engine/.env` (local file, plaintext) | **No** — `ai_engine/.gitignore` excludes `.env` | Fingerprint: `sk-or-v1-85a9...6f34` (first 12 / last 4 chars only, shown for identification, not reproduction). The full value is not reproduced in this document deliberately — see the note at the top of this response in the conversation. |
| JWT signing secret (backend) | `backend/.env` (**not yet created** — only `.env.example` exists with placeholder `change-me-to-a-random-64-char-string`) | No | Must be set to a real random value before backend goes to any real deployment; the placeholder is intentionally non-functional as a safety net. |
| Backend DB credentials | `backend/.env.example`: `postgresql+psycopg2://arbitrium:arbitrium@localhost:5432/arbitrium` | No | Placeholder dev credentials only, never a real deployment target. |

No repository is git-initialized in `d:\deepika doc\Study materials\arbitrium\` as of this writing (confirmed: "Is a git repository: false" in the environment context) — so "not committed" above currently means "not tracked by any VCS at all," and the `.gitignore` files are there pre-emptively for whenever `git init` happens.

**If this document is ever shared, published, or uploaded anywhere outside this local machine:** it does not leak the live key (only a fingerprint is present), but it does document the exact env var names and file paths where the real key lives — treat this document itself with the same care as source code, not as something safe to post publicly, since it's effectively a map to where the secret is.

---

## 21. All External Sources Cited (complete list)

Every URL that appears anywhere in either module's seed/reference data, with what it's used for:

| URL | Used for | Verified numeric content? |
|---|---|---|
| https://www.lcia.org/Dispute_Resolution_Services/lcia-arbitration-rules-2020.aspx | LCIA Arbitration Rules 2020 (institution_rules) | N/A (rules text, not stats) |
| https://hkiac.org/arbitration/rules-and-practice-notes/2024-administered-arbitration-rules/ | HKIAC 2024 Administered Arbitration Rules (institution_rules) | N/A |
| https://hkiac.org/arbitration/rules-and-practice-notes/2015-procedures-administration-under-uncitral-rules/ | HKIAC UNCITRAL administration procedures (institution_rules) | N/A |
| https://www.icdr.org/rules_forms_fees | ICDR Rules, Forms & Fees (institution_rules); **also actually fetched and extracted from live in §19** | Live-extracted facts verified, no fabricated stats |
| https://siac.org.sg/siac-rules-2025 | SIAC Rules 2025 (institution_rules) | N/A |
| https://www.adr.org/annual-reports/ | AAA/ICDR annual reports index (annual_report_stats) | No — numeric fields null, verified=false |
| https://hkiac.org/about-us/annual-report/ | HKIAC annual report index (annual_report_stats) | No — numeric fields null, verified=false |
| https://www.lcia.org/lcia/reports.aspx | LCIA reports index (annual_report_stats) | No — numeric fields null, verified=false |
| https://siac.org.sg/annual-reports | SIAC annual reports index (annual_report_stats); **attempted live fetch in §19, returned HTTP 403** | No |
| https://www.lcia.org/ | LCIA institution website_url | N/A |
| https://hkiac.org/ | HKIAC institution website_url | N/A |
| https://mcia.org.in/ | MCIA institution website_url; also used as FeeSchedule source_url placeholder | N/A |
| https://uncitral.un.org/en/texts/arbitration/contractualtexts/arbitration | Ad Hoc/UNCITRAL FeeSchedule source_url placeholder | N/A |

**Sources named in conversation but never fetched or used as a system source:** none — every URL discussed was either the PRD's own citation list or was derived directly from it (institution homepage URLs).

---

## 22. Legal & Data-Integrity Scaffolding

This section consolidates every place in the build where a legal-accuracy or data-integrity commitment was made structurally (in code/schema), not just in prose.

1. **`verified: Boolean` column** on both `annual_report_stats` and `fee_schedules` (backend) — defaults to `False`, must be explicitly flipped by a human after confirming a figure against its cited source. Carried through to every API response that touches these tables (e.g. cost-estimate `breakdown.verified`).
2. **`source_url: String, not null`** on `institution_rules`, `annual_report_stats`, `fee_schedules` — every quantitative or rules claim in the schema is required to carry a citation at the database level, not just conventionally.
3. **`status: "disclosed" | "not_disclosed"`** on `ExtractedFact` (AI Engine) — "we don't know" is a first-class, always-available answer, not an omission.
4. **Hallucination guard** (§17) — an independent, code-level verification step that does not trust the LLM's own claimed citation; it re-checks the citation against the actually-retrieved source text before a fact is accepted.
5. **Recommendation engine's transparency-over-black-box design** (§8.1) — every seat/institution score decomposes into 4 named, human-readable, sourced-rationale dimensions; there is no opaque ML ranking step a lawyer couldn't audit.
6. **Clause generator's pathology checks** (§8.3) — directly implements the PRD's "pathology-checked" requirement as enumerable, testable rules rather than an LLM judgment call.
7. **Contract parser's explicit non-authority disclaimer** (§8.4, in-code docstring) — extraction results are contractually (in the code comment) never final data, always editable defaults.
8. **Jurisdictional facts asserted as true** (seat governing statutes, NY Convention membership) are standard, stable, textbook-level facts (e.g., India's Arbitration and Conciliation Act 1996, the UK's Arbitration Act 1996, Hong Kong's Arbitration Ordinance Cap. 609) — these are treated differently from caseload/fee statistics precisely because they're low-volatility legal facts rather than a specific institution's self-reported yearly numbers, which is the category the "no fabrication" rule was really targeting.

**What this build explicitly does NOT claim:** it does not claim to be a substitute for qualified legal counsel; it does not claim any of the illustrative fee/caseload figures are real; it does not claim SIAC/HKIAC/ICDR/LCIA endorse or were involved in this tool. None of these disclaimers currently exist as user-facing copy anywhere (no frontend exists yet) — flagged here as a requirement for whoever builds the frontend.

---

## 23. Environment Details (dependency versions, Python version, OS)

- **OS:** Windows 11 Home Single Language, build 10.0.26200.
- **Python:** 3.11.4 (both venvs).
- **Shell used for builds:** Git Bash (POSIX sh) via the Bash tool; PowerShell also available in this environment but not used for the build commands.
- **Backend venv:** `backend/.venv/` — see `backend/requirements.txt` (§ "Backend — Architecture" intro) for exact pins, all confirmed installing cleanly after the bcrypt fix.
- **AI Engine venv:** `ai_engine/.venv/` — see `ai_engine/requirements.txt`, all confirmed installing cleanly after the httpx fix.
- **No git repository** exists yet anywhere under `d:\deepika doc\Study materials\`. `.gitignore` files exist in both `backend/` and `ai_engine/` pre-emptively.
- **No PostgreSQL server** was available in the build sandbox — all backend validation used SQLite as a stand-in (see §11 "Not yet done").
- **Live network access** was available and used for the AI Engine's real OpenRouter calls and real HTTP fetches (§19).

---

## 24. Deliverables Summary

| Deliverable | Status | Where |
|---|---|---|
| PRD's 5 pages as working REST APIs | ✅ Done | `backend/app/api/v1/endpoints/` |
| PostgreSQL schema (12 tables) + Alembic migration | ✅ Done, not yet run against real Postgres | `backend/app/models/`, `backend/alembic/versions/0001_initial.py` |
| Seeded reference dataset with source citations | ✅ Done | `backend/app/seed/reference_data.py` |
| Recommendation engine | ✅ Done, tested, live-verified | `backend/app/services/recommendation_engine.py` |
| Cost estimator | ✅ Done, tested, live-verified | `backend/app/services/cost_estimator.py` |
| Clause generator + pathology checks | ✅ Done, tested, live-verified | `backend/app/services/clause_generator.py` |
| Contract parser (PDF/DOCX heuristic extraction) | ✅ Done, tested | `backend/app/services/contract_parser.py` |
| JWT auth, guest/authenticated dual mode | ✅ Done, tested | `backend/app/core/security.py`, `backend/app/api/deps.py` |
| React/TypeScript frontend | ❌ Not started (explicit scope decision) | — |
| Standalone AI Engine module | ✅ Done | `ai_engine/` |
| OpenRouter client locked to `openrouter/free` | ✅ Done, live-verified working | `ai_engine/core/client.py`, `core/config.py` |
| Agentic tool-calling loop | ✅ Done, tested, live-verified | `ai_engine/core/agent_loop.py` |
| RAG ingestion (PDF/HTML fetch, chunk, BM25 retrieval) | ✅ Done, tested, live-verified (except SIAC's own site, 403) | `ai_engine/ingestion/` |
| Extraction agent with structured output | ✅ Done, tested, live-verified | `ai_engine/extraction/extractor.py` |
| Hallucination guard (no-fabrication enforcement) | ✅ Done, tested, live-verified against real model output | `ai_engine/extraction/hallucination_guard.py` |
| CLI (ingest/extract/export) | ✅ Done, live-used | `ai_engine/main.py` |
| Both modules' architecture checklists (PRD-mandated) | ✅ Done, fully checked off | `backend/CHECKLIST.md` equivalent → actually `arbitrium/CHECKLIST.md`; `ai_engine/CHECKLIST.md` |
| This master reference document | ✅ Done | `arbitrium/PROJECT_REFERENCE.md` |

---

## 25. Known Gaps / Next Iteration (both modules)

### Backend
- React/TypeScript frontend: header, right nav sidebar, all 5 pages — entirely unbuilt.
- Real auth flows wired to a frontend (backend JWT exists in isolation).
- File storage for uploaded contracts beyond local disk (`backend/uploads/`) — no cloud storage integration.
- Replace every `verified=False` fee-schedule and annual-report row with real figures confirmed against the cited primary source.
- Live rule-tracking refresh job (cron/scheduled task) to re-check the 5 primary rule sources for changes — schema already has `last_checked_at` per rule to support this.
- Run `alembic upgrade head` + the full test suite against a real PostgreSQL instance (only SQLite has been exercised).

### AI Engine
- `siac.org.sg` returns HTTP 403 to the requests-based fetcher (likely WAF/bot protection) — needs either a headless-browser fetch strategy or an alternate access path before SIAC can be covered by this pipeline. This is a real, currently-unsolved gap, not a hypothetical one — it was hit live.
- `ingestion/fetch.py`'s HTML extraction strips all markup including `<a href>` targets, so the agent cannot discover and follow a linked PDF report from an HTML index page on its own — annual report PDF URLs currently must be supplied directly.
- Bulk multi-year ingestion across all five institutions' full report archives — only a single-page, single-institution live run has been done.
- Sector/country dimension tables in the backend's Postgres schema to actually receive `ai_engine/storage/export.py`'s output — the backend's current `annual_report_stats` table only has aggregate fields (new_cases_filed, avg_claim_value_usd, avg_duration_months), no per-sector or per-country breakdown columns yet.
- Scheduled re-ingestion job for new annual report publications.
- Rate limiting / robots.txt compliance policy for `fetch_source` if ingestion scope grows beyond the five cited sources.
- No automated pipeline yet connects `ai_engine`'s exported JSON facts into the backend's database — this is an intentional human-checkpoint gap (§13, decision 2), not an oversight, but it does mean the two modules are not yet actually wired together end-to-end.

---

*End of document. This snapshot reflects the state of the `arbitrium/` project as of 2026-09-10. Treat the running code as authoritative if the two ever disagree.*
