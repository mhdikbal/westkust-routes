# Atlas Integration Decision Review

**Date:** 2026-08-28
**Scope:** Langkah 7 of the post-freeze roadmap for the multi-case power-relations prototype (commit `77b79b68`) and its Graph Projection Contract v1.0 (`ba32eb0`). Reviews whether/how the prototype should integrate into the public Atlas, given the frozen contract and the two adjudicated known gaps (DEC-05/06, DEC-19).
>
> **Correction (this turn):** this line originally also cited "the validated (19/19) disposable graph projection from Langkah 5-6" as an accomplished fact. That claim has been independently verified and found **unverifiable** — see `DELTA09_GRAPH_PROJECTION_CLAIM_VERIFICATION.md`. A build+validate script pair for it plausibly existed in a session-scoped scratchpad (corroborated by a prior session's own file-modification record) but the scratchpad no longer exists and no result was ever committed anywhere durable. Treat the disposable projection as **not existing** for any practical purpose; do not assume its "19/19" result carries forward.

**This is a decision review, not an implementation.** No route was added. No Atlas file was touched. No authentication code was written.

## 1. Finding That Changed the Calculus

Prior framing (this session's own earlier message) assumed the blocker was "Basic Auth/session authentication belum diterapkan" — read as a configuration gap. Direct inspection of `frontend/config/settings.py` shows it is stronger than that:

```text
django.contrib.auth in INSTALLED_APPS:      absent
django.contrib.sessions in INSTALLED_APPS:  absent
SessionMiddleware in MIDDLEWARE:            absent
Any login view / authenticate() call:       none found in frontend/
All 7 existing /riset/* views:              plain public functions, no decorator
```

There is no authentication *system* in this Django app at all — not a toggle away, a from-scratch build (app install, user/session migrations, middleware ordering, login view, then route gating). This makes "resolve authentication" (Langkah 8) a separate infrastructure project, not a short prerequisite step alongside Atlas integration.

## 2. Options Reconsidered

**A — Keep prototype local/nonproduction.** No Atlas change, no new work. Everything actually confirmed to exist (validated prototype, frozen projection contract, two adjudicated gaps) remains valid as internal research infrastructure regardless of public visibility. The "validated disposable projection" is **not** included in that list — see the correction above; it would need to be rebuilt and re-verified before being relied on again.

**B — Authenticated research-only Atlas page.** Correct destination for the content (keeps RESEARCH_ONLY entities behind a gate, matches the contract's own boundary). Blocked by §1 as a hard prerequisite, not a parallel task — Langkah 8 must complete first.

**C — Reviewed public summary without research-only structures.** Technically buildable without auth, but blocked by a different gate: every decision in `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` (DEC-01 through DEC-19) declares `public_impact: None`. No decision has ever authorized publishing any form of this data. Choosing C now would require opening a new public-vocabulary policy decision, not a smaller technical step than B.

## 3. Decision

**Option A confirmed by user (2026-08-28).** Prototype and graph-projection work remain local/nonproduction. No Atlas route, page, or navigation link is added.

**Option B remains the recorded target** for if/when Langkah 8 (build authentication from scratch) is completed and separately requested — not scheduled, not started, not authorized by this decision.

**Option C is not adopted.** Any future move toward it requires a new, explicit public-vocabulary/publication-policy decision first (its own DEC-xx equivalent), out of scope for this review.

## 4. Non-Actions (explicit)

- No `frontend/map_app/urls.py` or `views.py` change.
- No `django.contrib.auth`/`sessions` installation or configuration.
- No Atlas navigation link.
- No Graphify work.
- No production route, container rebuild, or restart.
- No new public-vocabulary or publication-policy decision opened.

## 5. Status

`ATLAS_INTEGRATION_DECISION_A_CONFIRMED_LOCAL` — not committed, not pushed. Production, Atlas, backend, frontend, and database all unchanged.

Roadmap position: Langkah 8 (resolve authentication) and Langkah 9 (Graphify pilot, only after Langkah 8) remain unstarted, contingent on a future, separately-requested turn.
