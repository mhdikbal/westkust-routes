# ATLAS Multi-Case Power-Relation Prototype — Construction/Validation Audit

> **NONPRODUCTION PROTOTYPE. LOCAL, STATIC, READ-ONLY. NO ATLAS/BACKEND/FRONTEND/API/DATABASE/GRAPHIFY/PRODUCTION CHANGE.**

## 1. Scope

Builds a second research prototype, sibling to `research_prototypes/painan_1663_relational/`, generalizing its single-case rendering discipline across the 5 now-migrated Draft V2.1 cases (Painan, Natal, Koto Tangah, Tiku, Sillida), per `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md` SS5-SS6 — which specified, without building, exactly this step. Authorized by the user's explicit "Lanjut ke multi-case prototype."

## 2. What Was Reused, What Was New

Reused wholesale (in spirit, case-parametrized) from `research_prototypes/painan_1663_relational/prototype.js`: `el()`, `badge()`, `escapeHtml()`, the `disclosureDrawer()` three-level pattern, the render-error-collection discipline (skip an invalid record, surface it, never silently drop it), and the six original view renderers (Overview, Actors, Timeline, Network, Claim/Control, Public-Copy).

New: a case switcher (`CASES_DEF`, `switchCase()`, `setupCaseSwitcher()`) loading all 5 `migrated_v2_1` artifacts up front via `Promise.all`; a Case Index view (case table + counts + the cross-case namespace diagnostic `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md` SS5 calls for); a V2.1 Additions view (`CommercialRight`/`RightModification`/`CommandObservation`/`OperationParticipation`, closed-by-default, RESEARCH-ONLY, never a graph edge); an 18-value `AUTHORIZED_RELATION_TYPES` array mirroring `scripts/research_validators/power_relation_ontology_rules.json`'s own closed vocabulary exactly (Painan's own prototype hardcoded only its own 7 case-specific values); an `objectIdOf()` helper normalizing the confirmed field-name divergence between Painan's relations (`object_actor_id`) and the other 4 cases' (`object_id`).

## 3. Design Decision: Never Merge Actors Across Cases

The case switcher fully replaces the active actor/relation set in every view. No shared cross-case graph is ever built. When an `actor_id` string recurs across independently-authored case files (confirmed: `ACTOR_VOC` recurs in Natal/Sillida/Tiku's own files, each an independently-authored object, never the same in-memory record), the Case Index view's namespace diagnostic panel reports this as a fact, explicitly labeled "not an error" — consistent with DEC-01's own "no automatic actor merge" safeguard, applied here to the presentation layer, not just the ontology.

## 4. Bug Found and Fixed During Real-Data Execution Testing (disclosed, not silently patched)

No headless browser was available in this environment (Playwright's own `browser_navigate` failed: `chrome executable not found`). Genuine execution-level verification was still performed, not skipped: `jsdom` installed in an isolated scratchpad (never added to the repo's own `package.json`/`node_modules` — this project has neither), loading the real `index.html` + `prototype.js` in a DOM, firing real click events through the case switcher and all 8 views, and asserting `window.onerror`/`console.error` stayed empty.

This surfaced a real bug on the first run: `endpointById` (constructed only from `data.actors`) did not include `data.locations`, so relations targeting a Location (e.g. `USES_MILITARY_FORCE_AGAINST` a fort, `CLAIMS_COMMODITY_MONOPOLY` over a salt refinery) were incorrectly flagged `unresolved endpoint` — 3 relations in Koto Tangah, 1 in Sillida. The Python generalized validator's own equivalent check already unions `_actor_ids(artifact) | _location_ids(artifact)`; the JS prototype had not mirrored that. Fixed by merging `data.locations` into the same lookup map used for endpoint resolution (the Actors view still iterates `data.actors` directly, so locations do not render as actor cards). Re-verified after the fix: JS-side valid/invalid relation counts per case now match the Python generalized validator's own findings exactly (see SS5).

## 5. Execution-Level Verification Results (jsdom, all 5 cases x 8 views)

```text
window.onerror / console.error: NONE, across all 5 cases and all 8 views
load-status: "5/5 cases loaded read-only."
Case Index counts (post-fix):
  Painan       6 actors, 9/9 valid relations,  0 V2.1 entities, 0 flagged
  Natal       13 actors, 11/12 valid relations, 0 V2.1 entities, 1 flagged (VOC_INSTITUTIONAL_HESITATION_ANNOTATION)
  Koto Tangah  8 actors, 12/12 valid relations, 0 V2.1 entities, 0 flagged
  Tiku        13 actors, 8/10 valid relations, 2 V2.1 entities, 2 flagged (COMMODITY_PEPPER/SALT as object_id)
  Sillida     14 actors, 14/14 valid relations, 3 V2.1 entities, 0 flagged
V2.1 Additions view (Sillida): renders CR_SILLIDA_1698_SALIMOET_TOLL under a closed, RESEARCH-ONLY
  disclosure drawer, confirmed by DOM text extraction
Natal/Tiku Overview: "Render-time validation errors" panel present, confirmed by DOM text extraction
```

These per-case flagged counts match the migration-phase audit's own generalized-validator findings exactly (`ATLAS_POWER_RELATION_V2_1_ARTIFACT_MIGRATION_AUDIT.md` SS5) — Natal's 1 and Tiku's 2 are the same pre-existing, already-disclosed gaps, not new ones introduced by this prototype.

## 6. Checklist Validator Results

```text
scripts/research_validators/validate_multi_case_power_relations_prototype.py
CHECKS PASSED: 29/29
VALIDATION RESULT: PASS
```

29 checks, generalizing the Painan prototype's own 30-item checklist (`ATLAS_PAINAN_1663_LOCAL_RELATIONAL_RESEARCH_PROTOTYPE_PLAN.md` SS13) across 5 cases, plus the 2 `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md` SS5 checks (closed relation-type vocabulary parity with the rule registry; namespace diagnostic implemented). Check 1 re-verifies all 5 `migrated_v2_1` files' checksums against the migration audit's own recorded values (chain-of-custody continuity). Check 2 re-runs the Python generalized validator against all 5 files and confirms the PASS/FAIL pattern matches exactly what the migration phase already found — no drift.

## 7. Existing Validator Chain (unaffected)

```text
Painan artifact:    23/23 PASS
Painan prototype:   30/30 PASS
Natal:              28/28 PASS
Koto Tangah:        34/34 PASS
Tiku:               35/35 PASS
Sillida:            32/32 PASS
Generalized validator pytest suite: 174/174 PASS
```

None of these 6 scripts, the generalized validator, its rule registry, or any of the 5 `migrated_v2_1` files was modified. All 5 `migrated_v2_1` checksums are unchanged from the migration-phase audit's own recorded values (verified in SS6 check 1 above and independently via `sha256sum` this turn).

## 8. Files Created

```text
research_prototypes/multi_case_power_relations/index.html
research_prototypes/multi_case_power_relations/prototype.js
research_prototypes/multi_case_power_relations/prototype.css
research_prototypes/multi_case_power_relations/README.md
scripts/research_validators/validate_multi_case_power_relations_prototype.py
```

## 9. Checksums

```text
research_prototypes/multi_case_power_relations/index.html
  250546c41024e6c40d29c62c886ea93b92a152d05af8c8fb04e226a43362a3eb
research_prototypes/multi_case_power_relations/prototype.js
  f4e8cc2d62ff8df6c96208c5795beb9e41b5ea56c61e0757e1ca1a069a23dfa0
research_prototypes/multi_case_power_relations/prototype.css
  e656fb49c3279b59d615aebe6a0f2a9036a913c5ce2f30d5ed0381e0ee79eab4
research_prototypes/multi_case_power_relations/README.md
  14252e28302203973e42ec2c25a7a89480d089b1ad5e11286564d828a7f175f3
scripts/research_validators/validate_multi_case_power_relations_prototype.py
  3a491a87a0007e67556f667420bf45e1ef0436916f4569275083661c47834045
```

## 10. Migration/Graphify/Production Nonauthorization

Unaffected. No artifact migrated or modified by this phase (all 5 `migrated_v2_1` files pre-date this turn and are unchanged). No Graphify execution or reference (functional). No Atlas/backend/frontend/API/database file touched. No production change.

## 11. Final Status

```text
MULTI_CASE_PROTOTYPE_CONSTRUCTED_AND_VALIDATED_LOCALLY
```
