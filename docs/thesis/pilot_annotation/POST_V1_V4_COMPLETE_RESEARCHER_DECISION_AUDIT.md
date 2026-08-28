# Post-V1-V4 Ontology Adjudication — Complete Researcher Decision Audit

> **18/18 decisions complete. Implementation, migration, Draft V2.1 construction, generalized-validator implementation, artifact migration, multi-case prototype, and Graphify all remain NOT AUTHORIZED by this audit or by the ledger it records.**

---

## 1. Scope

Consolidates the final state of the post-V1-V4 cross-case ontology failure synthesis's 18-item researcher-adjudication ledger, now fully decided (0 PENDING), against the changeset ledger and revalidation matrix it governs. This is the authoritative closing record of the adjudication milestone — it does not authorize any next step beyond adjudication itself.

## 2. Authoritative Baselines

```text
Local HEAD before this freeze: 6766787fe60c58f10da1c69e64da7cc6723bdfcd
origin/main:                   6766787fe60c58f10da1c69e64da7cc6723bdfcd (identical)
Latest commit with the first five blocking decisions: 6766787
  (research(ontology): freeze five approved researcher decisions
  DEC-01/04/09/10/14)
Committed ledger checksum (at 6766787): 65feefc1f095aab0c800b27bcd60758b18305585b37f318590f36f7135f358fe
Working ledger checksum (18/18 decided, before DEC-11 provenance append):
  b3ae9d0470d7fcd6d757c27287a7c40f4e1b26ac34a80413eb569f0d1b10daec
Working ledger checksum (final, after DEC-11 provenance append -- this is
  what gets committed): recorded in the terminal summary for this turn
```

## 3. Selected Package

```text
BALANCED
```
Recorded in DEC-14's `researcher_notes`: *"PACKAGE SELECTED: BALANCED (recorded here -- no dedicated package field exists in this ledger's schema; Balanced chosen among Minimal/Balanced/Expanded Research per PRD Section 8)."* Consistent and unchanged across every decision recorded in this ledger.

## 4. Final Decision Distribution

```text
APPROVED:                  5  (DEC-12, DEC-13, DEC-15, DEC-17, DEC-18)
APPROVED_WITH_LIMITATIONS: 8  (DEC-01, DEC-02, DEC-03, DEC-04, DEC-08, DEC-09, DEC-10, DEC-16)
DEFERRED:                  3  (DEC-05, DEC-06, DEC-11)
REJECTED:                  1  (DEC-07)
DRAFT_V2_1:                1  (DEC-14)
PENDING:                   0
TOTAL:                     18
```

## 5. Exact Eighteen Decisions

| ID | Topic | Status |
|---|---|---|
| DEC-01 | Actor identity continuity fields (CH-01/CH-02) | APPROVED_WITH_LIMITATIONS |
| DEC-02 | Explicit non-identity field (CH-02) | APPROVED_WITH_LIMITATIONS |
| DEC-03 | Mandate status and scope (part of CH-01) | APPROVED_WITH_LIMITATIONS |
| DEC-04 | Rights/privilege object model (CH-03) | APPROVED_WITH_LIMITATIONS |
| DEC-05 | Institutional-state observation (CH-04) | DEFERRED |
| DEC-06 | Institutional-presence observation | DEFERRED |
| DEC-07 | Ambiguous spatial-feature fields (CH-05) | REJECTED |
| DEC-08 | Resistance-target extension (CH-06) | APPROVED_WITH_LIMITATIONS |
| DEC-09 | Command/operation-participation model (CH-07) | APPROVED_WITH_LIMITATIONS |
| DEC-10 | Constrained-agency annotation fields | APPROVED_WITH_LIMITATIONS |
| DEC-11 | Dispute-settlement object (CH-08) | DEFERRED |
| DEC-12 | Public vocabulary impact | APPROVED |
| DEC-13 | Backward compatibility strategy | APPROVED |
| DEC-14 | Version naming | DRAFT_V2_1 |
| DEC-15 | Cases required for revalidation | APPROVED |
| DEC-16 | New relation types research-only initially | APPROVED_WITH_LIMITATIONS |
| DEC-17 | Graphify deferral | APPROVED |
| DEC-18 | Production gate continuation | APPROVED |

## 6. Blocking Decisions (originally frozen first, commit 6766787)

```text
DEC-01: APPROVED_WITH_LIMITATIONS -- actor identity continuity
DEC-04: APPROVED_WITH_LIMITATIONS -- rights/privilege object model (Option B selected)
DEC-09: APPROVED_WITH_LIMITATIONS -- command/operation-participation model
DEC-10: APPROVED_WITH_LIMITATIONS -- constrained-agency fields
DEC-14: DRAFT_V2_1 -- version naming
```
All five carry: implementation NOT AUTHORIZED, migration NOT AUTHORIZED, public-display impact NONE, Graphify DEFERRED, production gate BLOCKED.

## 7. Cluster A Decisions

```text
DEC-02: APPROVED_WITH_LIMITATIONS -- explicit non-identity folded into CH-01's
        explicit_non_identity_with field
DEC-03: APPROVED_WITH_LIMITATIONS -- mandate status/scope as semi-structured
        free-text-with-guidance, not a closed enum
```
Both extend DEC-01's already-approved identity-continuity work; same safeguard discipline (no automatic merge, CANNOT_DETERMINE/NOT_TESTABLE remain valid, manual review for consequential decisions, no rewriting frozen artifacts).

## 8. Cluster F Decisions

```text
DEC-12: APPROVED -- confirms no new public-facing category from any of the 8 changes
DEC-13: APPROVED -- confirms all 8 changes are additive/optional
DEC-17: APPROVED -- confirms continued Graphify deferral
DEC-18: APPROVED -- confirms continued production-gate blocking
```
Each ratifies a governance principle already consistently applied across all decided items — approval does not authorize schema implementation, Draft V2.1 construction, generalized-validator implementation, artifact migration, or any Atlas/database/API/Graphify/production change.

## 9. Remaining Decisions (final batch)

```text
DEC-05: DEFERRED -- authorize a future design-exploration turn for Natal's
        institutional-state hesitation; no schema change adopted now
DEC-06: DEFERRED -- same decision as DEC-05, recorded separately (shared
        failure cluster FCL-03, distinct ledger rows)
DEC-07: REJECTED -- no spatial-feature schema change; Sillida V4 demonstrates
        the existing Location model is adequate; authorize a non-ontology
        source re-check of Vogel's "Refort" usage instead
DEC-08: APPROVED_WITH_LIMITATIONS -- resistance_target_actor_id as an
        OPTIONAL field; resistance remains Research-Only throughout
DEC-11: DEFERRED -- see § 10, explicit researcher adjudication
DEC-15: APPROVED -- revalidation scope covers all 5 artifacts, Painan as
        clean 23/23 regression baseline
```

## 10. DEC-11 Researcher Adjudication

```text
Final value: DEFERRED
```

**Provenance, preserved not erased:** Claude Code initially proposed DEFERRED as the conservative default, in the absence of an explicit researcher risk-tolerance instruction, and explicitly flagged this in the ledger's `researcher_notes` field as requiring researcher confirmation rather than machine inference — the ledger's own prior text states this verbatim: *"FLAGGED FOR EXPLICIT RESEARCHER OVERRIDE... requires explicit researcher risk-tolerance judgment, not inference."* The researcher subsequently reviewed this proposal and explicitly accepted DEFERRED, on the following stated grounds, appended to the same field as a superseding decision (original text preserved, not overwritten):

```text
- evidence currently rests on one principal case (Sillida V4)
- the proposed object has the highest schema-to-evidence ratio in the changeset
- implementation now risks case-specific overfitting
- a second sufficiently independent case is required before reconsideration
- deferral does not reject the historical phenomenon (the 1679 VOC
  disproportionate fine-share pattern remains real, just not yet
  schema-represented)
- evidence collection may continue
- no dispute-settlement object is authorized in Draft V2.1 at this stage
```

This decision is **not** represented as autonomous machine adjudication — the ledger's `researcher_notes` field for DEC-11 carries both the original machine-proposed default and the researcher's own explicit superseding acceptance, in that order, both preserved.

## 11. DEC-16 Research-Only Boundary

```text
Final value: APPROVED_WITH_LIMITATIONS
```

Confirms all newly approved structures from this changeset remain `RESEARCH_ONLY` (Draft V2 section 10), including, where applicable:

```text
- CommercialRight, RightModification (DEC-04)
- CommandObservation, OperationParticipation (DEC-09/DEC-10)
- constrained-agency fields: dependency_status, coercion_status,
  ability_to_refuse, voice_availability, political_intent,
  constrained_agency (DEC-10)
- explicit_non_identity_with, mandate_status, mandate_scope (DEC-01/02/03)
- resistance_target_actor_id (DEC-08)
```

These remain `RESEARCH_ONLY` until **all** of the following occur, none of which this decision or this audit authorizes:
```text
- Draft V2.1 contract review
- generalized-validator implementation and PASS
- migrated-artifact revalidation
- multi-case prototype review
- explicit public-vocabulary authorization (the existing 7-simultaneous-criteria
  promotion discipline, Draft V2 section 3)
```
DEC-16 does not authorize Graphify or public display, and its trigger condition (§1 of the prior digest turn) is confirmed no longer hypothetical — DEC-04 selected Option B and DEC-09/DEC-10 already introduced structured entities, so this boundary is presently load-bearing, not speculative.

## 12. DEC-14 Version Naming

```text
Final value: DRAFT_V2_1
```
This selects the version **name only**. It does not create, construct, or authorize construction of a Draft V2.1 document or schema. Confirmed: no file named or shaped like a Draft V2.1 contract exists anywhere in the repository as of this audit (search performed, none found).

## 13. Changeset Consistency

`docs/thesis/colab/ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CHANGESET_LEDGER.csv` — verified unchanged, read-only this turn:

```text
8 changeset rows: CH-01 through CH-08, all implementation_status = PROPOSED_ONLY
None changed to IMPLEMENTED, MIGRATED, or DEPLOYED
No changeset schema modification
No implementation artifact created
```

**DEC-to-CH mapping:**
```text
CH-01 (identity continuity core)      -> DEC-01 (+DEC-03 mandate sub-decision)
CH-02 (explicit non-identity)         -> DEC-02
CH-03 (rights/privilege object)       -> DEC-04
CH-04 (institutional-state/presence)  -> DEC-05, DEC-06
CH-05 (ambiguous spatial features)    -> DEC-07
CH-06 (resistance-target extension)   -> DEC-08
CH-07 (command/operation model)       -> DEC-09, DEC-10
CH-08 (dispute-settlement object)     -> DEC-11
```

```text
Approved changes (full or with limitations): CH-01, CH-02, CH-03, CH-06, CH-07
  -> DEC-01/02/03/04/08/09/10
Deferred changes: CH-04, CH-08 -> DEC-05/06/11
Rejected changes: CH-05 -> DEC-07
Changes requiring Draft V2.1 design before any implementation: CH-01, CH-02,
  CH-03, CH-06, CH-07 (all approved-with-limitations changes -- approval is
  not implementation authorization)
Changes excluded from Draft V2.1 due to deferral/rejection: CH-04 (DEC-05/06),
  CH-05 (DEC-07), CH-08 (DEC-11) -- none of these three proceeds into any
  future Draft V2.1 construction unless independently reopened
```

## 14. Revalidation-Matrix Consistency

`docs/thesis/colab/ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv` — verified unchanged, read-only this turn:

```text
Exactly 10 planned tests (REV-01 through REV-10)
No status/execution-state field exists in this matrix's own schema (columns:
  revalidation_id, change_id, case_id, prior_failure_id, prior_result,
  expected_v2_1_result, regression_risk, required_fixture,
  required_validator_update, acceptance_criteria, researcher_review_required,
  notes) -- there is structurally no field that could be falsely marked
  "executed," and none was
No generalized-validator result is claimed or referenced anywhere in this
  matrix
```

**Dependency check against deferred/rejected changes:**
```text
REV-08 (CH-04, V1_NATAL) and REV-09 (CH-04, V2_KOTO_TANGAH): already
  correctly pre-labeled "CH-04 (deferred)" in the matrix's own change_id
  field -- consistent with DEC-05/06 = DEFERRED, no update needed
REV-10 (CH-05, V2_KOTO_TANGAH): already correctly pre-labeled "CH-05 (no
  change proposed)" -- consistent with DEC-07 = REJECTED, no update needed
REV-07 (CH-08, V4_SILLIDA): NOT pre-labeled as deferred in the matrix,
  unlike REV-08/09/10 -- FLAGGED. This test now depends on CH-08, which
  DEC-11 has deferred. The revalidation matrix was not modified by this
  audit (per Phase 5/6 instructions, read-only), so this flag is recorded
  here for whoever next touches the matrix, not resolved by editing it.
```

## 15. Deferred and Rejected Scope

```text
Deferred (3): DEC-05, DEC-06 (institutional-state/presence observation,
  pending a future design-exploration turn), DEC-11 (dispute-settlement
  object, pending a second confirming case)
Rejected (1): DEC-07 (ambiguous spatial-feature fields -- Location model
  adequacy already demonstrated by Sillida V4)
```
None of these four decisions authorizes any schema change, and none is represented as a closed/settled research question — DEC-05/06/11 remain explicitly reopenable on new evidence; DEC-07 accepts a disclosed, case-specific limitation rather than papering over it.

## 16. Implementation Nonauthorization

```text
NOT_AUTHORIZED
```
Every one of the 18 decisions carries this language verbatim or by direct equivalent. No decision in this ledger authorizes writing implementation code for any proposed schema change.

## 17. Migration Nonauthorization

```text
NOT_AUTHORIZED
```
No decision authorizes migrating any of the 5 frozen V1-V4 artifacts to a new schema version. Original artifacts remain immutable per DEC-14's own recorded terms ("original V1-V4 artifacts remain immutable, migrated artifacts will be written as new files") — a future-state description, not a present authorization.

## 18. Public-Display Boundary

```text
NO NEW AUTHORIZATION
```
Every approved/approved-with-limitations decision explicitly states public-display impact NONE. DEC-16 additionally makes this an active, load-bearing boundary for the specific new entities this changeset introduces (§ 11).

## 19. Graphify Boundary

```text
DEFERRED
```
Reaffirmed by DEC-17 specifically, and consistent across all 18 decisions. Confirmed this turn: no Graphify runtime consumer exists anywhere in `backend/` or `frontend/` (unchanged from the comprehensive audit's Phase 5 finding).

## 20. Production-Gate Status

```text
BLOCKED
```
Reaffirmed by DEC-18 specifically. The 8-item Production Gate (Draft V2 section 14) is unaffected by this adjudication milestone, which authorizes only a fully-adjudicated but still `PROPOSED_ONLY` changeset.

## 21. Remaining Preconditions for Draft V2.1

Per DEC-14's own terms and this audit's cross-checks, before any Draft V2.1 document could be constructed:
```text
[ ] separate, explicit researcher authorization to begin construction
    (this freeze does not grant it)
[ ] generalized-validator implementation (currently PLANNED_ONLY, no
    executable exists)
[ ] resolution of the 5 approved-with-limitations changes' exact schema
    syntax (each decision approved a direction, not a copy-paste-ready
    schema fragment)
[ ] artifact migration plan for the 5 V1-V4 artifacts as new, separate files
[ ] multi-case prototype review (does not currently exist)
[ ] revalidation-matrix execution once implementation exists (currently
    10 planned, 0 executed)
```
None of these is authorized or begun by this audit.

## 22. Final Status

```text
ONTOLOGY_DECISIONS: 18/18 COMPLETE
PENDING: 0
DECISION_MILESTONE: COMPLETE
IMPLEMENTATION: BLOCKED
DRAFT_V2_1_CONSTRUCTION: REQUIRES_SEPARATE_AUTHORIZATION
GRAPHIFY: DEFERRED
```
