# Product Requirements Document (PRD)

**Document Name:** arbitrium prd iteration 1  
**Product Name:** Arbitrium  
**Product Type:** Legal Decision-Support & Arbitration Intelligence Platform  
**Target Architecture Stack:** ReactJS (TypeScript) Frontend, Python (FastAPI) Backend, SQL (PostgreSQL) Database  
**Status:** Iteration 1 — Production Draft  

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