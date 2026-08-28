# GET /api/forts/power-status — Endpoint Migration Plan

> **Planning document. No option implemented. No endpoint created or modified.**

---

## 1. Options Compared

### Option A — Swap the existing endpoint to the minimal contract immediately, create protected endpoint alongside

```text
Steps: change /api/forts/power-status response to the minimal public
  contract; simultaneously stand up /api/research/forts/power-status-detail
  behind auth.
Regression risk: HIGH -- atlas.js is not migrated first, so the moment the
  public endpoint's contract shrinks, the live map immediately loses cluster
  chips, dwell rings, sparklines, source citation, and provenance badges
  with no fallback (per FORT_POWER_STATUS_PUBLIC_SUMMARY_CONTRACT.md § 6).
Rollback: requires reverting the backend change under time pressure once
  the regression is visible.
```

### Option B — Add a new public-summary endpoint, migrate atlas.js, retire the full public endpoint later (RECOMMENDED, matches researcher's stated default)

```text
Steps:
  1. Keep /api/forts/power-status exactly as it is today (temporary).
  2. Add /api/forts/power-status-summary (or similar) returning the minimal
     public contract, alongside the existing endpoint -- purely additive,
     zero risk to the current map.
  3. Add /api/research/forts/power-status-detail behind authentication,
     serving the full protected contract.
  4. Migrate atlas.js to call the two new endpoints instead of the old one
     -- the public summary endpoint for the base map layer, and (once
     authentication exists and an authenticated researcher view is defined,
     which is out of scope for this endpoint-only plan) the protected
     endpoint for any future authenticated detail view.
  5. Verify the migrated atlas.js against the new endpoints in a disposable/
     local rehearsal (same discipline as the CARTO remediation and route-
     retirement work already completed this session).
  6. Only once atlas.js is confirmed fully migrated and verified, retire
     (or restrict) the original /api/forts/power-status endpoint.
Regression risk: LOW -- the live map is never pointed at a changed contract
  until the replacement is already proven to work.
Rollback: trivial at every step -- steps 1-3 are purely additive (nothing
  existing changes), step 4's frontend change can be reverted independently
  of the backend, step 6 is the only step that removes anything and happens
  last, after verification.
```

### Option C — Protect the entire current endpoint immediately, modify the public map to use a new summary endpoint immediately

```text
Steps: add authentication to /api/forts/power-status directly; simultaneously
  ship a new public summary endpoint and an atlas.js change, all at once.
Regression risk: HIGH -- combines a backend contract change, a new
  authentication requirement, and a frontend migration into a single
  deployment with no intermediate verification point. Any one piece failing
  (auth misconfiguration, frontend still pointing at the old now-protected
  URL, a missed field) breaks the public map immediately with no soft
  landing.
Rollback: all-or-nothing -- reverting one piece without the others likely
  leaves the system in a broken intermediate state (e.g. frontend still
  calling the now-protected URL after only the backend part is rolled back).
```

## 2. Recommendation

```text
RECOMMENDED: OPTION B
```

Reasons (as stated by the researcher, recorded verbatim as the basis for this recommendation):
- lowest immediate regression risk
- allows frontend migration before restricting the existing full endpoint
- supports explicit deprecation
- enables rollback
- avoids breaking the current public map abruptly

This recommendation is **not implemented by this turn** — it is a plan for a future, separately authorized execution turn, following the same "propose → disposable rehearsal → candidate diff → separate execution authorization" discipline already established for the CARTO and route-retirement remediations this session.

## 3. Dependencies Before Option B Can Execute

```text
[ ] Basic Auth / research-authentication mechanism must exist in production
    before step 3 (protected endpoint) can be meaningfully authenticated --
    currently NOT_IMPLEMENTED anywhere (per COMPREHENSIVE_MODELING_RUNTIME_
    DEPLOYMENT_STATE_AUDIT.md). This endpoint's protection should join
    whatever mechanism eventually protects /api/research/linimasa and
    /api/research/pemodelan-dashboard, not invent a separate one.
[ ] Public-copy review process for as_of_event.title / dominion_status
    "reviewed" status must be defined (who reviews, what standard) before
    step 2's summary endpoint can honestly claim its title field is
    "reviewed public copy" rather than merely "the same raw value, just in
    a smaller response"
[ ] Audit-logging and cache-policy decisions for the protected endpoint
    (FORT_POWER_STATUS_PROTECTED_RESEARCH_CONTRACT.md § 7) need resolution
    before step 3 ships
[ ] Explicit separate execution authorization for each step, per this
    session's established discipline -- this plan does not pre-authorize
    any of steps 1-6
```

## 4. Status

```text
MIGRATION_OPTION_B_RECOMMENDED_NOT_AUTHORIZED_FOR_EXECUTION
```
