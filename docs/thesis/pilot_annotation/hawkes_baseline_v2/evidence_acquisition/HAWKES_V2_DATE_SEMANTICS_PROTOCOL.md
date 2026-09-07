# HAWKES V2 — DATE-SEMANTICS REMEDIATION PROTOCOL (DESIGN ONLY)

WP-E5. This document designs a date-role taxonomy and a per-date record
structure. **No `L_i/U_i` bounds are constructed for any actual corpus row
in this operation. No modeling use is authorized even where the protocol
below would classify a date as usable.**

## 1. Date-role taxonomy

```
EVENT_DATE            -- the date the occurrence itself is asserted to have happened
REPORT_DATE            -- the date a source document was written describing the occurrence
DISPATCH_DATE           -- the date a letter/report was sent
RECEIPT_DATE            -- the date a letter/report was received by its addressee
RESOLUTION_DATE         -- the date an administrative body acted on a report (e.g. Directors' resolution date)
COMPILATION_DATE        -- the date an editorial compilation (e.g. a GM volume) was assembled, distinct from any event within it
PUBLICATION_DATE        -- the date a secondary edition (e.g. Hakluyt Society volume) was published
BOUNDED_INTERVAL         -- the date is known only to fall within an explicit [lower, upper] range
SUBSTITUTED_PROXY_DATE   -- a date assigned by the project as a stand-in (e.g. deterministic jitter within a tied year) for estimator input
UNRESOLVED_DATE_ROLE     -- the role has not been determined
```

**Key design point:** `EVENT_DATE`, `REPORT_DATE`, `DISPATCH_DATE`, and
`RECEIPT_DATE` are frequently conflated in existing coding practice
(illustrated by the documented GOTCHA of tied years requiring jitter — the
project's own memory records this as a date-*handling* problem, but this
protocol treats it as potentially also a date-*role* problem: a `REPORT_DATE`
may have been coded as if it were an `EVENT_DATE`).

## 2. Per-date record structure

For coded date *d_i*:

```
D_i = ( value, role, precision, lower_bound, upper_bound, source, confidence_basis )
```

| Field | Design requirement |
|---|---|
| `value` | The literal coded value (unchanged from current schema) |
| `role` | One of the 10 taxonomy tokens above — **must be assigned explicitly, never defaulted** |
| `precision` | Reuses the existing 7-category `event_date_precision` schema (unchanged) |
| `lower_bound` / `upper_bound` | Only populated when `role != UNRESOLVED_DATE_ROLE` and a researcher-reviewed parsing rule (not yet authorized) has been applied |
| `source` | The document/citation that the date value was extracted from |
| `confidence_basis` | A **categorical** label describing why the date is trusted at its stated precision (e.g. `EXPLICIT_IN_SOURCE`, `INFERRED_FROM_ADJACENT_DATED_ENTRY`, `EDITORIAL_ESTIMATE`) — **never a numeric confidence score or probability** |

## 3. Usability gate (design definition only)

```
G_date,i = 1[ role_i != UNRESOLVED_DATE_ROLE  AND  provenance_i = 1  AND  bounds_i are coherent ]
```

`provenance_i = 1` requires a `source` field distinct from the coded row's
own self-citation (same provenance-sufficiency logic as WP-E4's `P_i`).
"Bounds coherent" means `lower_bound <= value <= upper_bound` when bounds
exist, and is vacuously true when no bounds are yet constructed.

**Explicit non-authorization:** even for a hypothetical date where
`G_date,i = 1`, no Hawkes fitting, forecasting, or comparator construction
is authorized by that fact alone. This gate answers "is this date
semantically legible," not "may output be modeled with it."

## 4. Relationship to the documented GOTCHA and MBPP robustness check

The existing project record (`project_markov_hawkes_models` memory) shows:
(a) 48+ of the corpus's event-years share an identical coded year, requiring
deterministic jitter for continuous-time MLE, and (b) an MBPP (interval-
censored) comparator reproduced the pooled branching ratio within 0.1% of
the jittered production fit. This protocol does not reopen or repeat that
finding. It records that the MBPP check covers **branching ratio only** —
kernel shape and individual peak-timing under alternative date-role
assignments (e.g. if some `EVENT_DATE`-coded values are actually
`REPORT_DATE`) remain untested, and testing them would require applying
Section 1's taxonomy to actual source documents — a future, separately
authorized operation, not this one.

## 5. Non-authorization statement

This protocol is a design artifact only. It constructs no bounds, resolves
no actual corpus date, and authorizes no modeling use.
