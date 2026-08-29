# Graphify Authorization & Disposable Graph Projection — Result

> **Scoped authorization record + build result. NOT Atlas/production integration. NOT the code-knowledge-graph tool `graphify-out/`.**

---

## Authorization (2026-08-29)

User instruction: "otorisasi implementasi Graphify." Given the blast radius, scope was clarified before acting (`AskUserQuestion`) — user selected:

> **"Otorisasi + bangun proyeksi graf disposable lokal"** — authorize AND build the disposable local graph projection (roadmap Langkah 5), staying local/nonproduction. Explicitly *not* selected: integration toward Atlas (Option B) or any production route/page work.

```text
GRAPHIFY_PRODUCTION_AUTHORIZATION:        NOT GRANTED (still requires its own future decision)
DISPOSABLE_LOCAL_PROJECTION_BUILD:        AUTHORIZED AND EXECUTED (this document)
ATLAS_ROUTE_PAGE_DECISION (Option B):     NOT GRANTED, NOT ADDRESSED
```

This closes the "explicit Graphify authorization" line item from `GRAPHIFY_READINESS_REASSESSMENT.md` only to the extent authorized: a disposable, local, reproducible graph projection now exists. It does **not** close "Authenticated research-only Atlas infrastructure" or authorize any production/Graphify-tool integration — those remain open, separate decisions.

---

## What was built

Two new, durably committed (not scratchpad-only, correcting the DELTA-09 process gap) scripts:

- `scripts/graph_projection/build_projection.py` — projects the 5 current migrated V2.1 artifacts (Painan, Natal, Koto Tangah, Tiku `_v2_1_1_` post-DEC-19-remodel, Sillida) into a node/edge graph per the frozen `ATLAS_GRAPH_PROJECTION_READINESS_REVIEW.md` contract.
- `scripts/graph_projection/validate_projection.py` — 8 independent safety checks against the build output.

Both import their source-of-truth vocabulary directly from `scripts/research_validators/validate_power_relation_ontology.py` (`ALLOWED_RELATION_TYPES`) rather than duplicating the 18-value list — one source of truth, not a second copy that could drift.

Output: `scripts/graph_projection/disposable_projection_output.json` (regenerable; the JSON output itself is *not* committed, per the contract's own "disposable" framing — the script that produces it, and this result summary, are what's durable).

## Result

```text
Source artifacts:  5 (Painan, Natal, Koto Tangah, Tiku [_v2_1_1_ post-remodel], Sillida)
Total relations:   57 (across all 5)
Nodes:             65  (Actor + Location, case-scoped)
Edges:             54  (closed-vocabulary relation_type, both endpoints resolved)
Unary claims:       2  (Tiku's two DEC-19-remodeled CLAIMS_COMMODITY_MONOPOLY relations —
                        object_id=null + commodity attribute; correctly NOT forced into edge
                        shape, since Commodity has no node under DEC-19 option (b))
Excluded:           1  (Natal's ANNOTATION_VOC_HESITATION_ANNOTATION / CH-04 — outside the
                        closed 18-value vocabulary, per DEC-05/06, correctly unprojected)

Reconciliation: 54 edges + 2 unary claims + 1 excluded = 57 = total relations.
Every relation accounted for exactly once; none silently dropped.

validate_projection.py: 8/8 check categories PASS
  1. No forbidden auto-derived edge type present (RESISTS, PATRON_OF, CLIENT_OF,
     COMMANDS, PARTICIPATES_IN, HOLDS_COMMERCIAL_RIGHT, MODIFIES_RIGHT)
  2. No relation_type outside the closed 18-value vocabulary leaked through
  3. No dangling edge endpoints
  4. No dangling unary-claim subject
  5. No unary claim carries an object_node_id (DEC-19 shape preserved structurally)
  6. Actor-identity rule: every node case-scoped; reused raw_id across cases
     produces distinct node_ids, never a merge
  7. Every edge/unary claim carries full required metadata (contract SS3)
  8. Zero CommercialRight/RightModification/CommandObservation/OperationParticipation
     id leaked into the node/edge/claim id space (RESEARCH_ONLY boundary held)
```

## Scoping decisions made during the build (not pre-specified in the contract, decided here)

1. **Source not projected as a standalone node type.** The contract lists Source as *eligible*, not required. This build keeps source references as edge/claim metadata (`source_document_ids`, `source_passage_locator`) rather than materializing a third node type, to keep the disposable build minimal. Revisiting this is a future, separately-scoped choice, not implied by anything decided today.
2. **DEC-19-shaped relations (object_id=null + commodity attribute) are projected as subject-scoped "unary claims," not edges.** A graph edge structurally needs two nodes; Commodity is explicitly not a node under DEC-19 option (b). Forcing these into edge shape (e.g., against a synthetic Commodity node) was rejected as exactly the kind of side-effect promotion `ATLAS_GRAPH_PROJECTION_READINESS_REVIEW.md` §2.1 was written to prevent. This is the correct-by-construction representation, not an assumption made in advance of building.
3. **Office and Event remain unprojected**, unchanged from the contract's own `DEFERRED_NO_DATA` / `DEFERRED_REQUIRES_JOIN` classification (§1.1) — no artifact populates a first-class Office entity, and Event would require an out-of-scope join against `linimasa_events.csv`.

## New finding surfaced by this build (not previously known)

**Painan's migrated artifact uses `object_actor_id`, not `object_id`, on all 9 of its relations** (0/9 have an `object_id` key at all). The generalized validator's `R-REF-05` check (`check_relation_endpoints` in `validate_power_relation_ontology.py`) reads only `subject_actor_id`/`object_id` — it has therefore **never actually checked Painan's endpoint integrity**; `rel.get("object_id")` silently returns `None` for every Painan relation, and the check's own guard (`if val is not None and val not in known`) treats an absent field identically to a legitimately-null one, so no error was ever raised. Painan's "0 errors" status across every audit this session is accurate for every rule *except* this one, which was silently never exercised on Painan at all.

Verified independently this turn: all 9 `object_actor_id` values do resolve to real actors in Painan's own `actors[]` array (no actual orphan endpoints — this is a validator blind spot, not evidence of a data problem). `build_projection.py` reads both `object_id` and `object_actor_id` (checking which key is actually present, `object_id` taking precedence) specifically so the projection itself is not built on this blind spot.

**Not fixed this turn**: the generalized validator itself (`check_relation_endpoints`) was not modified — that is a separate, small, well-scoped fix (add `object_actor_id` as a recognized alias, mirroring the existing `_normalize_legacy_version_marker` pattern for Painan's other legacy field name) that needs its own explicit authorization, consistent with this session's standing discipline of never modifying the validator without being asked. Flagged here as a genuine, previously-undisclosed gap for the researcher's attention — not a Graphify-blocking issue (this build already accounts for it correctly), but a generalized-validator correctness gap.

## What remains unauthorized / not performed

- No graph store, database, or persistent index was created — output is a single disposable JSON file, not committed.
- Not wired into the multi-case prototype (`research_prototypes/multi_case_power_relations/prototype.js` is unmodified).
- Not wired into any Atlas route, page, or API endpoint.
- No Graphify (`graphify-out/`) integration of any kind — unrelated tool, confirmed unrelated per the contract's own §0.
- The `object_actor_id` validator gap is documented, not fixed.
- Production/`westkust-prod` untouched.

## Cross-references

```text
Contract:                   ATLAS_GRAPH_PROJECTION_READINESS_REVIEW.md
Contract freeze:            ATLAS_GRAPH_PROJECTION_CONTRACT_FREEZE_AUDIT.md
DEC-19 decision+impl:       DEC19_TIKU_COMMODITY_ADJUDICATION_DECISION.md
Prior readiness reassessment: GRAPHIFY_READINESS_REASSESSMENT.md
DELTA-09 process lesson applied here: DELTA09_GRAPH_PROJECTION_CLAIM_VERIFICATION.md
  ("a disposable artifact's citable result must be captured durably" —
  this time the scripts themselves are committed under scripts/graph_projection/,
  not left only in an ephemeral scratchpad)
```

---

## Correction Record (2026-08-29, targeted generalized-validator fix)

User explicitly authorized a **targeted correction** of the gap this document originally disclosed, scoped to: generalized-validator fix, rule-registry update, synthetic fixtures, automated tests, and local read-only revalidation. The original finding above is preserved verbatim, not erased:

- **R-REF-05 initially ignored `object_actor_id`** — confirmed: the prior `check_relation_endpoints` read only `subject_actor_id`/`object_id`; Painan's relations carry `object_actor_id` exclusively (0/9 have an `object_id` key).
- **This allowed endpoint integrity to escape actual validation** — `rel.get("object_id")` returned `None` for all 9 Painan relations, and the guard `if val is not None and val not in known` treated an absent field identically to a legitimately-null one, so `R-REF-05` never fired on Painan in either direction (true positive or false positive).
- **Manual inspection found Painan data valid** — all 9 `object_actor_id` values independently confirmed to resolve to real actors in Painan's own `actors[]` array before any code change was made.
- **The validator was corrected**: `check_relation_endpoints` in `scripts/research_validators/validate_power_relation_ontology.py` now recognizes exactly two contract-grounded object-endpoint fields (`object_id`, generic; `object_actor_id`, Painan's own pre-standardization field — grounded in Draft V2's own text naming Painan's case-specific validator as what the generalized validator should replicate), validates `object_actor_id` strictly against actor IDs only (not the actor+location union), requires an endpoint field to be present at all (`MISSING_RELATION_ENDPOINT` if entirely absent, or present-but-null without a `commodity` attribute to justify a DEC-19-shaped unary claim), and rejects any other endpoint-shaped field name outright (`UNAPPROVED_ENDPOINT_FIELD`). `object_location_id`/`subject_location_id`/bare `subject_id` were checked for and found nowhere in Draft V2, Draft V2.1, or any of the 6 migrated artifacts — not added, since that would be inventing an alias rather than recognizing a contract-approved one.
- **All nine Painan `object_actor_id` references were then machine-validated**: re-running the corrected validator against Painan's migrated artifact now genuinely checks all 9 (previously silently skipped) — result: `ERROR=0, PASS` (unchanged from before in outcome, but now for the right reason — actually checked, not silently passed).
- **Projection was regenerated and revalidated**: `build_projection.py` re-run from a clean state, `validate_projection.py` re-run — identical counts (65 nodes / 54 edges / 2 unary claims / 1 excluded), 8/8 checks PASS, confirming the disposable projection was never affected by this validator gap (it already read both `object_id` and `object_actor_id` itself, built independently before this correction).

### Test suite impact

```text
Previous generalized-validator suite:  174/174 PASS
Newly added fixtures:                  5 positive + 7 negative = 12 new fixtures
                                        (72 new parametrized test instances --
                                        each fixture is exercised by 6 test
                                        functions: pass/fail assertion,
                                        immutability, determinism, JSON-output
                                        validity, human-output stability,
                                        exit-code check)
New authoritative total:               246 tests
Result:                                246/246 PASS
```

All 174 prior tests remain PASS, unmodified. Every new negative fixture fails with its intended primary error code (verified individually before wiring into the harness, then reconfirmed via the full suite run).

New fixtures: `positive_11_object_id_actor_endpoint.json`, `positive_12_object_actor_id_endpoint.json`, `positive_13_unary_commodity_claim.json`, `positive_14_object_actor_id_strict_match.json`, `positive_15_object_id_location_endpoint.json`, `negative_19_missing_object_endpoint.json`, `negative_20_object_actor_id_unresolved.json`, `negative_21_object_location_id_unapproved_field.json`, `negative_22_unknown_endpoint_alias.json`, `negative_23_object_actor_id_cross_entity_collision.json`, `negative_24_null_endpoint_without_commodity.json`, `negative_25_binary_relation_incorrectly_treated_as_unary.json` — all synthetic, no production data or archival quotations.

### Revalidation of all five migrated artifacts (corrected validator, read-only)

```text
Painan:       ERROR=0, PASS  -- all 9 object_actor_id endpoints now explicitly
                                validated and resolved (previously silently
                                unchecked, not merely "clean by luck")
Natal:        ERROR=1, FAIL  -- unchanged: the 1 expected CH-04 legacy gap
                                (VOC_INSTITUTIONAL_HESITATION_ANNOTATION,
                                UNAPPROVED_RELATION_TYPE) remains, exactly as
                                documented -- not normalized away
Koto Tangah:  ERROR=0, PASS  -- no false unresolved-location endpoint introduced
Tiku (_v2_1_1_, post-DEC-19): ERROR=0, PASS -- 2 unary Commodity claims
                                represented per the current adjudicated remodel,
                                correctly not treated as orphan endpoints
Sillida:      ERROR=0, PASS  -- no false unresolved-location endpoint introduced
```

Six legacy case-specific validators and the multi-case prototype validator re-run, unaffected (none of them import or depend on the generalized validator):

```text
Painan artifact validator:        23/23 PASS
Painan prototype validator:       30/30 PASS
Natal validator:                  28/28 PASS
Koto Tangah validator:            34/34 PASS
Tiku validator:                   35/35 PASS
Sillida validator:                32/32 PASS
Multi-case prototype validator:   29/29 PASS
```

### Disposable projection rebuild (post-correction)

```text
65 nodes, 54 edges, 2 unary claims, 1 excluded relation
54 + 2 + 1 = 57 = total source relations across the 5 cases (unchanged)
validate_projection.py: 8/8 checks PASS
No silent relation loss. No automatic actor merge. No research-only object
converted to a factual edge. No orphan endpoint. No production consumer.
Generated graph JSON remains disposable and uncommitted (regenerated fresh,
not staged).
```

### What this correction does not claim

Per explicit instruction, this correction is not, and does not imply:

```text
NOT: GRAPHIFY_DEPLOYED
NOT: ATLAS_INTEGRATED
NOT: PRODUCTION_READY
```

## Final Status (this document)

```text
DISPOSABLE_LOCAL_GRAPH_PROJECTION_BUILT_AND_VALIDATED
GRAPHIFY_PRODUCTION_INTEGRATION: STILL NOT AUTHORIZED
ATLAS_WIRING: STILL NOT AUTHORIZED
GENERALIZED_VALIDATOR_REFERENCE_GAP_CORRECTED
DISPOSABLE_GRAPH_PROJECTION_VALIDATED
```
