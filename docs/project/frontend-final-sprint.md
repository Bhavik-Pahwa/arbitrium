# Arbitrium Frontend Final Sprint Checklist

## Completed
- [x] Read `project-reference.md`, `implementation-checklist.md`, `ai-engine-checklist.md`, backend API schemas, and endpoint behavior.
- [x] Extracted and read the supplied `Dashboards.zip` guidance.
- [x] Used the 10k websites landing-page guidance with the provided `Background Animation.mp4`.
- [x] Created a fresh React + TypeScript + Tailwind frontend in `frontend/`.
- [x] Processed `Background Animation.mp4` into scrub-ready `hero-scrub.mp4`, `hero-poster.jpg`, and `hero-ending.jpg`.
- [x] Built a scroll-scrub landing page with visible copy kept off the video title and hands.
- [x] Built a top navbar and workflow navigation linking all lawyer-facing pages.
- [x] Built Dashboard, Seat Allocation, Rule Tracking, Clause Generation, Cost Estimate, Final Outputs, and Data Integrity pages.
- [x] Wired Seat Allocation, Clause Generation, and Cost Estimate forms to backend-compatible payloads.
- [x] Added quiet demo mode by default, with live API calls gated behind `VITE_API_ENABLED=true`.
- [x] Preserved legal-data guardrails in the UI: source links, pathology notes, unverified fee warnings, and known AI engine gaps.
- [x] Ran TypeScript build, lint, copy gate, screenshots, route checks, form interaction checks, and scroll-video timing check.

## Still Not Production Claims
- [ ] Annual report figures remain unverified until primary-source values are loaded.
- [ ] Fee schedules remain prototype-only until official institution calculators are checked.
- [ ] Backend PostgreSQL migration still needs a real Postgres run.
- [ ] SIAC annual report ingestion still needs a browser-based fetch strategy.
