# ATLAS Power-Relation Ontology — Artifact Migration Audit (V1-V4 → Draft V2.1)

> **5 ARTIFACTS MIGRATED AS NEW FILES. ORIGINALS UNMODIFIED (CHECKSUM-VERIFIED).**
> **NO ATLAS/BACKEND/FRONTEND/API/DATABASE CHANGE. NO GRAPHIFY. NO PRODUCTION CHANGE. NO STAGE/COMMIT/PUSH.**

## 1. Scope

Migrates Painan, Natal, Koto Tangah, Tiku, and Sillida to Draft V2.1 shape, per DEC-14: "original V1-V4 artifacts remain immutable, migrated artifacts will be written as new files." All 5 migrated files are new, under `data/power_relations/migrated_v2_1/`; none of the 5 originals under `data/power_relations/` was opened for writing.

## 2. Two Genuine Validator Gaps Fixed This Phase (disclosed, not silently patched)

Testing the generalized validator (commit `703634a`) against real content — rather than only synthetic fixtures — surfaced two gaps in the validator's own rule set, not in any artifact:

1. **`resistance_candidate` shape mismatch.** The validator's own synthetic fixtures (Phase V2.1-GV1) modeled `resistance_target_actor_id` nested inside a `resistance_candidate` object. Tiku's real relations store `resistance_candidate` as a bare descriptive string. The changeset ledger's own CH-06 language — "1 new optional field on the existing resistance_candidate annotation *only*" — means a **sibling field on the relation**, not a restructuring of `resistance_candidate` (restructuring it would itself violate DEC-13's "no existing annotation is renamed or redefined"). Fixed in `check_resistance_candidate`: `resistance_target_actor_id` and `resistance_target_public_status` are now read directly off the relation. The two affected fixtures (`positive_09_resistance_target.json`, `negative_13_resistance_as_factual_edge.json`) were updated to the corrected shape; full 174-test suite reconfirmed passing before any real artifact was touched.
2. **Incomplete relation-type vocabulary.** `ALLOWED_RELATION_TYPES` covered only the 14 `MVP_CORE_RELATION` + 2 `EXTENDED_RESEARCH_RELATION` values (16 total), missing Draft V2 SS2's own third named tier, `REQUIRES_MORE_EVIDENCE_RELATION` (`MAINTAINS_PARALLEL_ALIGNMENT_WITH`, `APPOINTS_OFFICE_HOLDER`). Painan's own frozen, already-validated (23/23) artifact legitimately uses `MAINTAINS_PARALLEL_ALIGNMENT_WITH` — Draft V2 SS2 explicitly retains it "for Painan's own use." Rejecting it was a validator defect, confirmed by evidence, not a case of Painan needing correction. Fixed: `ALLOWED_RELATION_TYPES` now covers all 18 values Draft V2 SS2 names as usable. `CASE_SPECIFIC_ONLY` (`CONTROLS_PORT`, `DISMISSES_OFFICE_HOLDER` — Draft V2 itself flags the latter as needing a subject-type correction) and `ANNOTATION_NOT_RELATION` (`IMPOSES_PUNITIVE_CLASSIFICATION_ON` — explicitly demoted) remain deliberately excluded: no real artifact uses them, and Draft V2 does not present them as ready.

Full 174-test suite reconfirmed passing after both fixes, before any migrated file was written. Updated files: `scripts/research_validators/validate_power_relation_ontology.py`, `scripts/research_validators/power_relation_ontology_rules.json`, `tests/fixtures/power_relation_ontology/positive_09_resistance_target.json`, `tests/fixtures/power_relation_ontology/negative_13_resistance_as_factual_edge.json`.

## 3. What Was Migrated, Per Case (source-grounded, nothing invented)

```text
Painan  -- version declaration only. DEC-15's clean 23/23 regression baseline; no CH-0x content applies.

Natal   -- version declaration only. FAIL-01 maps to CH-04 (DEC-05 DEFERRED). The migrated copy keeps
           Natal's own pre-existing ad hoc VOC_INSTITUTIONAL_HESITATION_ANNOTATION relation_type
           unmodeled -- this is the EXPECTED, disclosed signature of the still-deferred gap, not
           patched around by inventing an unauthorized relation type or removing real content.

Koto Tangah (CH-01, DEC-01/DEC-03) --
  identity_continuity_status added to ACTOR_KOTOTANGAH_COASTAL_COLLECTIVE_1660_1755, formalizing
  its own already-existing informal continuity_status prose (present since original V1-V4
  validation) under the Draft V2.1 field name. mandate_status was already present under its exact
  V2.1 name; no change needed.

Tiku (CH-01/CH-02, DEC-01/DEC-02) --
  identity_continuity_status + symmetric explicit_non_identity_with added to
  ACTOR_TIKU_REGENTS_1684 <-> ACTOR_PONGELOUS_12_DESA_TICCO_1662, formalizing prose already present
  on ACTOR_TIKU_REGENTS_1684 ("explicitly NOT asserted to be the same collective as
  ACTOR_PONGELOUS_12_DESA_TICCO_1662"). Symmetric back-reference added on the 1662 actor so the
  validator's own R-REF-04 symmetry check passes -- and because the non-identity IS in fact mutual.

Tiku (CH-03, DEC-04) --
  CommercialRight (CR_TIKU_1641_TOLL_EXEMPTION) + RightModification (action=EXEMPTS) added for the
  1641 Aceh toll-exemption reconfirmation for VOC shipping, grounded in
  REL_1641_CLAIMS_JURISDICTION's own source_statement_summary and instrument_id
  (INSTRUMENT_1641_TOLL_EXEMPTION). The existing CLAIMS_JURISDICTION_OVER relation is unchanged --
  it represents Aceh's jurisdictional claim; the new pair represents the exemption act itself,
  which had no prior representable form.

Tiku (CH-06, DEC-08) --
  resistance_target_actor_id=ACTOR_ACEH_COURT added to REL_1662_SWITCHES_PONGELOUS and
  REL_1662_SWITCHES_SOURERADJA, formalizing prose already present on each relation's own
  resistance_candidate value ("resistance-to-Aceh specifically, NOT resistance-to-VOC").

Sillida (CH-03, DEC-04) --
  CommercialRight (CR_SILLIDA_1698_SALIMOET_TOLL) + RightModification (action=RELEASES) added for
  the 1698 salimoet toll relinquishment, grounded in REL_1698_COLLECTS_TOLL_SALIMOET's own
  source_statement_summary and instrument_id (INSTRUMENT_1698_SALIMOET_RELINQUISHMENT).
  "Relinquished" maps to RELEASES, the closest of the 6 DEC-04-verbatim action values. The existing
  COLLECTS_TOLL_FROM relation is unchanged -- it represents the long-standing right itself.

Sillida (CH-07, DEC-09/DEC-10) --
  CommandObservation (CO_SILLIDA_ARMED_ENSLAVED_COMPANY_1687) added, migrating the artifact's own
  pre-existing OBS_CONSTRAINED_AGENCY_ARMED_ENSLAVED_COMPANY observation into the formal structured
  fields: coercion_status=COERCED (directly supported by the source's explicit "Sclaven" [enslaved]
  status); ability_to_refuse=CANNOT_DETERMINE and political_intent=CANNOT_DETERMINE (the original
  observation's own uncertainty_note states the company's agency beyond coerced deployment is
  undocumented -- never inferred beyond what the source says); voice_availability=ABSENT (no
  first-person source for this group); constrained_agency=CONFIRMED (the original observation's own
  words: "the artifact's central constrained-agency finding"). No relation was added between
  ACTOR_VOC and ACTOR_ARMED_ENSLAVED_COMPANY_SILLIDA_MINE -- the original observation explicitly
  states none was created, so the safety-critical R-REF-03 check passes by construction.
```

## 4. Backward Compatibility

Every migrated file is the original's full content plus additive-only new top-level keys (`ontology_version`, `migration_notes`, and where applicable `commercial_rights`/`right_modifications`/`command_observations`) and additive-only new fields on existing actors/relations. Nothing existing is renamed, removed, or restructured. `resistance_candidate` values are untouched strings; `continuity_status`/`mandate_status` informal fields are untouched, sitting alongside their new formal counterparts.

## 5. Generalized Validator Results (real content, first execution)

```text
painan_..._v2_1_migrated.json:      PASS  (0 CRITICAL, 0 ERROR, 27 REVIEW)
natal_..._v2_1_migrated.json:       FAIL  (1 ERROR: UNAPPROVED_RELATION_TYPE -- expected, CH-04 gap)
koto_tangah_..._v2_1_migrated.json: PASS  (0 CRITICAL, 0 ERROR, 45 REVIEW)
tiku_..._v2_1_migrated.json:        FAIL  (2 ERROR: ORPHAN_RELATION_ENDPOINT -- pre-existing
                                            Commodity-as-endpoint gap, already disclosed in the
                                            Phase V2.1-GV1 audit, unrelated to this phase's own
                                            CH-01/CH-02/CH-03/CH-06 additions, which contribute
                                            0 CRITICAL/ERROR findings on their own)
sillida_..._v2_1_migrated.json:     PASS  (0 CRITICAL, 0 ERROR, 56 REVIEW)
```

Natal's and Tiku's failures are both **pre-existing, already-disclosed gaps carried over unchanged from the originals** — neither is caused by, nor patched around by, this migration. Fixing either would require researcher-authorized scope beyond this phase (a CH-04 design for Natal; a Commodity-as-endpoint modeling decision for Tiku, flagged as a known limitation in the Phase V2.1-GV1 audit's own SS16).

## 6. Six Existing Case-Specific Validators (against the untouched originals)

```text
Painan artifact:    23/23 PASS
Painan prototype:   30/30 PASS
Natal:              28/28 PASS
Koto Tangah:        34/34 PASS
Tiku:               35/35 PASS
Sillida:            32/32 PASS
```

Unaffected -- none of the 6 files was read, imported, or edited.

## 7. Original-File Integrity

```text
git ls-files data/power_relations/*.json -> all 5 tracked
git status --porcelain data/power_relations/ -> only ?? data/power_relations/migrated_v2_1/ (new
  directory); zero modifications to any of the 5 tracked originals
```

## 8. Full pytest Suite

```text
tests/test_power_relation_ontology_validator.py: 174 passed, 0 failed (rerun after both validator
  fixes, before any real artifact was migrated)
```

## 9. Revalidation-Matrix Mapping (updated)

`docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_V2_1_REVALIDATION_IMPLEMENTATION_MAP.csv` updated: REV-01 through REV-06 reclassified `PARTIALLY_IMPLEMENTED` -> `IMPLEMENTED`, each now pointing at the specific migrated file and the specific finding count for that change's own content. REV-07/08/09 remain `DEFERRED`; REV-10 remains `NOT_APPLICABLE` -- unchanged, since nothing in this migration touches CH-04, CH-05, or CH-08.

## 10. Checksums

```text
scripts/research_validators/validate_power_relation_ontology.py
  2d3c9f6cb652174fedd844ed709eef37afbb7a9fa27d8e664f6bc03a88091f63
scripts/research_validators/power_relation_ontology_rules.json
  15588db8e8b989cfc95ef65572b8d7a53b513f0ae6701a09f8fe69bae2f534e3
data/power_relations/migrated_v2_1/koto_tangah_destruction_cycle_relational_validation_artifact_v2_1_migrated.json
  a57b20bd80d49ae44f5df1b5569800a106648815ba3ad208c00e048f4d1e7a7d
data/power_relations/migrated_v2_1/natal_1760_relational_validation_artifact_v2_1_migrated.json
  5b32aaabd38425103869dbb1d5c04e8924a4974df2f677bebdbb720e4734e873
data/power_relations/migrated_v2_1/painan_1663_relational_research_artifact_v2_1_migrated.json
  af6ba01972f038f9b9bca9515f59db78f9e1e7b84dd2ba566f32b9c2af562bdc
data/power_relations/migrated_v2_1/sillida_resource_governance_relational_validation_artifact_v2_1_migrated.json
  c43f986530625f8996d60076cf68973018e4dca476904a5195e63ddeae4c65f8
data/power_relations/migrated_v2_1/tiku_1625_1740_relational_validation_artifact_v2_1_migrated.json
  04da257f4153933a5fd0990ccf9cb49a8980410239ceefbfaf84c52bf554854b
```

## 11. Migration Nonauthorization Scope Note

This audit documents a migration explicitly authorized by the user's own turn ("Lanjut ke migrasi 5 artefak V1-V4 ke skema V2.1"). It does NOT authorize: any further schema change beyond what DEC-01 through DEC-16 already approved; multi-case prototype construction; Graphify; any Atlas/backend/frontend/API/database change; production integration; commit, push, or server sync (a separate authorization, matching this session's established rhythm).

## 12. Final Status

```text
ARTIFACT_MIGRATION_V2_1_COMPLETE_LOCALLY
```
