# SLR-DEC-06 — Collection Scope and Boundary (Manifest-Preparation-Only Authorization)

**Status:** SCOPE-AND-BOUNDARY SPECIFICATION ONLY. Governs what a future, separately authorized manifest-preparation turn may and may not do. No manifest row exists yet; no evidence is accessed by this document.

---

## 1. What This Authorization Covers

If adopted, this authorization permits exactly one future action:

```text
PREPARE a finite evidence-candidate manifest (SLR_DEC_06_EVIDENCE_CANDIDATE_MANIFEST.csv,
or equivalently named artifact) listing candidate evidence locations to be considered
for future Track A / Track B collection.
```

It does not permit any action beyond listing candidates and their planned discovery/access path.

---

## 2. What This Authorization Does Not Cover

```text
- accessing any evidence source (web fetch, database query, catalogue lookup)
- retrieving any methodological publication, standard, or guideline text
- reading or testing any provider's actual query syntax behavior
- promoting any provider-syntax row's verification_status
- executing any C1-C6 review-corpus search string
- retrieving, screening, or extracting any review-corpus record
- adjudicating SLR-DEC-06
- beginning SLR-DEC-07 or SLR-DEC-08 work
- modifying the decision ledger
- opening S1-B2 or running Model 3B / Hawkes
- staging, committing, pushing, or deploying anything
```

A future manifest-preparation turn that performs any of the above has exceeded this authorization and must stop.

---

## 3. Track Boundary (binding on the future manifest)

```text
TRACK A rows: candidate_source_or_issuing_body must be a methodological guidance issuer
              (standards body, professional association, peer-reviewed venue, or
              institutional methods clearinghouse) — never a review-corpus study.

TRACK B rows: candidate_source_or_issuing_body must be the provider's own official
              documentation domain — never a third-party tutorial, forum post, or
              unofficial syntax guide.
```

No manifest row may straddle both tracks. No Track B row may be used to populate a Track A `DEC06_component` other than `syntax`.

---

## 4. Manifest Row Contract (binding on the future turn)

Every row the future manifest turn writes must include all 17 fields specified in `SLR_DEC_06_EVIDENCE_COLLECTION_AUTHORIZATION_REVIEW.md` Sec.7, and every row's `execution_status` must be `PLANNED_ONLY` at creation. The manifest turn itself does not access any listed candidate — it only records the plan to consider it later.

```math
K_{\mathrm{manifest}} = 17.
```

*Correction note:* pre-freeze independent review mechanically recounted the unchanged ordered manifest schema and found 17 fields. Earlier references to 16 fields were an off-by-one documentation error. No field was added, removed, renamed, reordered, or redefined, and the future candidate count \(J\) remains undetermined.

```math
J = |E^*| \quad \text{must equal the actual row count once the manifest exists.}
```

No estimate of \(J\) is made here; none is authorized to be asserted before the manifest rows exist.

---

## 5. Escalation Discipline (binding on the future manifest)

Where a manifest row anticipates a multi-step access path (e.g., an index page before a specific document), the `predecessor_candidate_id` / `escalation_condition` fields must record that dependency explicitly — mirroring the discipline already enforced in `S1_B1_TARGET_PROVIDER_QUERY_MANIFEST.csv` for the S1-B1 workstream. No manifest row may silently presuppose a prior step's success.

---

## 6. Contradiction Boundary (inherited)

If a future collection run discovers two admissible items prescribing materially incompatible rules for the same `K_6` component:

```text
DEC06_METHOD_GUIDANCE_CONTRADICTION_REQUIRES_RESEARCHER_REVIEW
```

is required, and the conflict may not be resolved by vote count, recency alone, or source prestige alone — unchanged from the gap plan.

---

## 7. Relationship to SLR-DEC-06 Adjudication

Nothing produced under this authorization — not the manifest, not any future Track A/B collection result — automatically adjudicates SLR-DEC-06. `G_6^decision_ready` is recomputed only in a later, explicitly separate adjudication-readiness turn, after collection results (if any) exist and have been audited.

---

## 8. Final Status

```text
SLR_DEC_06_MANIFEST_PREPARATION_AUTHORIZATION_RECOMMENDATION_READY_FOR_RESEARCHER_REVIEW
```
