# OD-015 Draft Procedural Contract — Compute Planning: Storage, Checkpoint, Restart Determinism, Provenance Manifest

> **Status: DRAFTING-ONLY.** This document is a reviewable draft, not a final adjudication. No status change to `OD-015` in `WAVE_2_OPEN_DECISION_LEDGER.csv` is made or implied by this draft. Authorized drafting scope is restricted to `PROCEDURAL_CONTRACT` + `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` **only** — no candidate-set or provisional-recommendation content is included, per the governing instruction's stricter boundary for this decision.

## 1. Decision identity

`OD-015`, source requirements `REQ-M3-015`, `REQ-CROSS-001`, mathematical object `n/a` (systems/reproducibility design question, not a statistical formula question).

## 2. Exact frozen decision question

Verbatim from `WAVE_2_OPEN_DECISION_LEDGER.csv`: **topic** — "Compute planning: storage estimate, checkpoint design, restart determinism, provenance manifest (Package H)."

## 3. Current status

`OPEN_REQUIRES_ADJUDICATION` (ledger, unchanged by this draft). Readiness (evidence-to-option matrix): `EVIDENCE_PARTIAL` — **preserved unchanged by this draft.**

## 4. Candidate options

Stated exactly as in the ledger: **OPT-015-A** — "symbolic/structural estimate scaled from Wave-1-era pilot logs (per-cell time x replication count x method-cost multiplier); manifest schema per `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` S1, storage/checkpoint/restart/provenance design per S2 — no benchmark executed." Rejected option (already rejected in the ledger): running an actual compute-cost benchmark in this planning turn — rejection basis: explicit prohibition in the governing Wave 2 instruction §18 Package H ("jangan menjalankan compute-cost benchmark, gunakan symbolic atau structural dependency estimates saja").

## 5. Internal-source evidence

- `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` §1 already specifies the future manifest schema (`manifest_version`, `repository_baseline`, `specification_hashes`, `code_commit_future`, `container_digest_future`, `model_stage`, `cell_id`, `replication_id`, `master_seed`, `component_seed`, `parameter_truth`, `attempt_status`, `failure_code`, `start_time_future`, `end_time_future`, `software_versions_future`, `output_hash_future`) and the required manifest properties (deterministic restart, no silent replacement, attempted-replication accounting, per-cell completeness check, artifact hashing, staged-run separation, provenance-to-requirement traceability).
- `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` §2 is a deliberately qualitative structural compute-planning estimate — explicitly states "no number in this section is a measured quantity," and defers all 8 resource-envelope ceiling dimensions to `NUM-DEC-08`'s separately-authorized profiling turn.
- `NUM-DEC-08`'s resource-envelope framework (`M3-BLOCK-08` in the M3 blocker registry): all 8 ceilings remain `PENDING_MEASUREMENT` — this draft does not alter that status.

## 6. Literature evidence

- **E-005** (Sandve, Nekrutenko, Taylor, Hovig 2013, "Ten Simple Rules for Reproducible Computational Research," *PLOS Computational Biology*, DOI:10.1371/journal.pcbi.1003285, open-access CC-BY, `FULL_TEXT_ACCESSED`) — **primary substantive evidence for this draft**, per the drafting instruction's explicit requirement. Explicit source claims used: Rule 1 ("for every involved step, you should ensure that every detail that may influence the execution of the step is recorded" — provenance from result back to process); Rule 4 ("only that exact state of the script may be able to produce that exact output" — mandates version control); Rule 5/7 (archive intermediate results and raw data in standardized, retrievable formats); Rule 6 (the random seed should be recorded, allowing exact reproduction by supplying the same seed in future runs). These map directly to 4 of the manifest schema's fields: `master_seed`/`component_seed` (Rule 6), `code_commit_future` (Rule 4), the requirement-to-output provenance traceability (Rule 1), and archiving raw replication rows rather than only summaries (Rule 5/7). **Explicit gap, stated affirmatively by this source's own scope**: E-005's content, as fetched, contains no discussion of checkpoint/restart mechanisms or deterministic resumption of an interrupted long-running computation — a genuine evidentiary gap for this decision's restart-determinism sub-question, not an omission by this reviewer.
- **E-006** (Antunes, Hill et al. 2024, "Reproducibility, Replicability, and Repeatability: A survey... with a focus on high performance computing," *Computer Science Review*, arXiv:2402.07530, `ABSTRACT_ONLY`) — **contextual/unverified citation only**, per the drafting instruction. Citation and peer-reviewed journal placement confirmed; no specific methodological claim about checkpoint/restart, provenance manifests, or parallel seed management is asserted from this source anywhere in this draft, because only the abstract/landing page was accessible.
- **E-007** (Shahmoradi & Bagheri 2020, ParaMonte, preprint, arXiv:2009.14229, `ABSTRACT_ONLY`) — **contextual/unverified citation only**, per the drafting instruction. An earlier web-search-engine summary asserted a specific deterministic-restart precision claim for this library; that specific claim was **not** independently confirmed via full-text access and is explicitly **not used** for any method detail or implementation recommendation anywhere in this draft.

## 7. Access and provenance limits

E-005 is the sole `FULL_TEXT_ACCESSED`, peer-reviewed, open-access source used substantively for this decision — used only within its actually-verified scope (seed recording, version control, provenance traceability, intermediate-result archiving), never for checkpoint/restart-determinism content it does not cover. E-006 and E-007 are both `ABSTRACT_ONLY` and are used exclusively as contextual/unverified citations — neither is cited for method detail, formula, threshold, default, or implementation recommendation, per §7 of the drafting instruction and consistent with both prior narrow-review audits of this evidence package (0 claim-access mismatches found in each).

## 8. Mathematical implications

None — `OD-015`'s `mathematical_object` is `n/a` in the frozen ledger; this is a systems/reproducibility design question. The seed-hierarchy relation `s_{c,r,m} = f(s_master, c, r, m)` is preserved here only as a *conceptual* relationship (per §5.6 of the drafting instruction) — this draft does not select the function `f`, any seed value, a hash algorithm, a checkpoint interval, or a retry limit.

## 9. Option-by-option assessment

**OPT-015-A** (the only concrete candidate): `adjudication_readiness = EVIDENCE_PARTIAL` (evidence-to-option matrix — unchanged by this draft). Decidable-without-execution status is **partial**: the seed/provenance/versioning/archiving design principles (Rules 1/4/5/6/7 of E-005) are decidable from literature without execution or benchmark; the specific checkpoint/restart-determinism *mechanism* is, on the evidence gathered, more naturally an implementation-time engineering decision than a literature-adjudicable one — E-005 does not cover it, and no verified alternative source (E-006/E-007 remain unverified for this specific point) closes that gap. Statistical/provenance risk: low for the covered components; genuinely unresolved, and disclosed as such rather than papered over, for the checkpoint/restart-determinism component specifically.

## 10. Adversarial assessment

No source found argues *against* a symbolic/structural estimate as such for `OD-015` — the evidentiary gap is an absence of positive literature support for the checkpoint/restart-determinism design specifics, which is a limitation, not a contradiction. Silent-default risk (flagged explicitly, not smoothed over): a future implementation wave could wrongly assume "provenance and reproducibility are covered" based on this evidence package, when the specific checkpoint/restart-determinism mechanism remains unaddressed by verified literature. Condition under which the covered-components finding could fail to generalize: E-005 is a general single-machine/single-pipeline reproducibility framework, not explicitly designed for a distributed/parallel Monte Carlo execution context — the manifest schema in `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` §1 anticipates multiple workers/methods `m` with a seed hierarchy `s_{c,r,m}`, which is a simulation-design dependency not resolved by E-005 alone.

## 11. Draft recommendation

`DRAFT_PROCEDURAL_CONTRACT_FOR_REVIEW`: the manifest schema and structural (non-numeric) compute-planning design in `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` §§1–2, cross-checked against E-005's verified reproducibility-rule content, is submitted as a reviewable procedural contract. This draft makes **no candidate-set determination and no provisional recommendation** for `OD-015` — only the governing instruction's `PROCEDURAL_CONTRACT` scope is exercised.

## 12. Limitations

- E-005 does not cover checkpoint/restart determinism at all — this is a positive, disclosed gap, not an inferred one.
- E-006 and E-007 could not be independently verified for the one specific technical claim (deterministic parallel Monte Carlo restart) that would have been most directly relevant, had it been confirmable.
- Whether a general-purpose reproducibility framework (E-005) is sufficient for `OD-015`'s restart-determinism sub-question, or whether a dedicated HPC checkpoint-restart source needs to be found and verified in a future search pass, is an open residual question, not resolved here.

## 13. Required specification clarification

None beyond what is already recorded in the frozen evidence package — no conflict was found between `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` and the ledger/evidence-matrix content for `OD-015`.

## 14. Required implementation evidence

See §15 below — the full 15-requirement implementation-evidence contract, per the governing instruction §8.

## 15. Required calibration evidence

None identified for the procedural-contract scope of this decision — no simulation, benchmark, or calibration run is authorized or performed in this draft (per the ledger's own `rejection_basis`: benchmark execution was explicitly rejected as an option for this planning turn).

## 16. Prohibited shortcuts

This draft does not: select a candidate option beyond the single concrete `OPT-015-A`; assign a numeric resource-ceiling value (all 8 `NUM-DEC-08` dimensions remain `PENDING_MEASUREMENT`); select a checkpoint interval, retry limit, hash algorithm, or seed function `f`; assert that E-006/E-007 confirm any checkpoint/restart claim; or use final-status language for `OD-015`.

## 17. Proposed resolution type

`PROCEDURAL_CONTRACT` + `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` (matches the classification already frozen in `WAVE_2_OPEN_DECISION_ADJUDICATION_MAP.md` and `WAVE_2_OD_005_006_015_ADJUDICATION_READINESS_REPORT.md` — not altered here).

## 18. Final decision withheld

```text
OD-015 final decision: WITHHELD
```

No final adjudication is made. `OD-015` remains `OPEN_REQUIRES_ADJUDICATION`, readiness `EVIDENCE_PARTIAL`, in the ledger.

---

## Appendix: Required Implementation-Evidence Contract (governing instruction §8)

Exactly 15 requirement topics, each with the required field set. All `current_status = PLANNED_ONLY` — none is marked implemented or passed.

| requirement_id | requirement_text | failure_prevented | verification_method_future | negative_test_future | closure_evidence_future | current_status |
|---|---|---|---|---|---|---|
| OD015-IMPL-001 | Every checkpoint carries an immutable identity (`cell_id`, `replication_id`, checkpoint sequence number) traceable to a `WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv` requirement_id. | Checkpoints being mistaken for a different cell/replication on resume. | Future implementation review of checkpoint-identity generation logic against the manifest schema (§1). | Attempt to resume from a checkpoint whose identity does not match the manifest row; verify rejection. | A future implementation-wave test report confirming identity-mismatch rejection. | PLANNED_ONLY |
| OD015-IMPL-002 | Checkpoint completeness is verifiable — a checkpoint is either fully written or does not exist as a resumable artifact. | Resuming from a partially-written, corrupt checkpoint. | Future implementation review of checkpoint-write completion signaling (e.g. a completion marker or manifest row update only after full write). | Simulate an interrupted checkpoint write; verify the partial artifact is not treated as resumable. | A future implementation-wave test report confirming partial-write rejection. | PLANNED_ONLY |
| OD015-IMPL-003 | Checkpoint writes use an atomic-write pattern or an equivalent integrity guarantee (e.g. write-to-temp-then-rename, or a checksum verified before use). | Silent use of a corrupted or truncated checkpoint file. | Future implementation review of the write mechanism against a documented atomic-write or checksum pattern. | Simulate a crash mid-write; verify no non-atomic partial file is ever read as valid. | A future implementation-wave test report confirming atomicity or checksum enforcement. | PLANNED_ONLY |
| OD015-IMPL-004 | Restart from any valid checkpoint produces bit-identical (or explicitly documented tolerance-bounded) downstream results to an uninterrupted run, given the same seed and configuration. | Silent divergence between interrupted-and-resumed runs and uninterrupted runs, undermining reproducibility claims. | Future implementation review comparing resumed-run output hashes against uninterrupted-run output hashes for the same seed. | Run a cell to completion twice — once uninterrupted, once with a forced interruption and resume — and compare `output_hash_future`. | A future implementation-wave test report showing hash equality (or documented, disclosed tolerance). | PLANNED_ONLY |
| OD015-IMPL-005 | The full seed state (`master_seed`, `component_seed`, and any internal RNG stream state) required to resume a replication exactly is captured in the checkpoint. | Resume using a fresh/incorrect seed state, silently changing the replication's scientific identity. | Future implementation review of what RNG state is serialized into each checkpoint. | Resume a checkpoint and verify the first post-resume random draw matches what an uninterrupted run would have produced at that point. | A future implementation-wave test report confirming seed-state fidelity. | PLANNED_ONLY |
| OD015-IMPL-006 | `cell_id` and `replication_id` are preserved exactly across interruption and resume — never reassigned. | A resumed replication silently acquiring a new identity, breaking provenance traceability to its requirement. | Future implementation review of identity-preservation logic across the resume code path. | Interrupt and resume a replication; verify `cell_id`/`replication_id` in the manifest are unchanged. | A future implementation-wave test report confirming identity preservation. | PLANNED_ONLY |
| OD015-IMPL-007 | A failed or interrupted replication is never silently replaced with a new seed to inflate the valid-fit count (per `NUM-DEC-01`'s failed-run-as-evidence principle, already frozen). | Silent discarding of scientific evidence of optimizer/generation failure. | Future implementation review confirming no code path regenerates a failed replication_id with a new seed. | Force a replication failure; verify the manifest row remains with its original seed and a terminal failure status, never regenerated. | A future implementation-wave test report confirming no silent replacement occurred. | PLANNED_ONLY |
| OD015-IMPL-008 | The manifest maintains the `R_attempted,c = 1000` invariant (`NUM-DEC-01`) across interruption/resume — no attempted-replication row is lost or double-counted. | Attempted-replication accounting drift after a restart, invalidating `FailureRate_c`/`Coverage_c`/etc. denominators. | Future implementation review of per-cell row-counting logic before/after a forced restart. | Interrupt and resume a cell mid-execution; verify the total attempted-row count for that cell is still exactly 1000 with no duplicates. | A future implementation-wave test report confirming invariant preservation. | PLANNED_ONLY |
| OD015-IMPL-009 | Every terminal replication status uses a `failure_code` from the 24-entry failure taxonomy (`WAVE_2_MATHEMATICAL_CONTRACT.md`/governing instruction §14) — never a generic or missing code. | Ambiguous or lost failure classification after interruption/resume, breaking downstream failure-rate accounting. | Future implementation review confirming every terminal row has a taxonomy-valid `failure_code` or `VALID`. | Force several distinct failure types across an interruption boundary; verify each retains its specific taxonomy code after resume. | A future implementation-wave test report confirming failure-code preservation. | PLANNED_ONLY |
| OD015-IMPL-010 | Every output artifact is tied to an immutable `output_hash_future` recorded in the manifest. | Undetected silent modification or corruption of a stored output artifact. | Future implementation review of hash-computation-and-storage logic. | Modify a stored output artifact post-hoc; verify hash verification detects the modification. | A future implementation-wave test report confirming hash-mismatch detection. | PLANNED_ONLY |
| OD015-IMPL-011 | The manifest table remains internally continuous (no gaps, no orphaned rows) across an interruption/resume cycle, and staged runs (SMOKE/PILOT/LOCKED_PARTIAL_BATCH/FULL_PREREGISTERED_RUN) are never merged in the same manifest table. | Manifest corruption or stage-conflation making provenance unauditable. | Future implementation review of manifest continuity checks and stage-separation enforcement. | Attempt to write a FULL_PREREGISTERED_RUN row into a PILOT-stage manifest table; verify rejection. | A future implementation-wave test report confirming continuity and stage separation. | PLANNED_ONLY |
| OD015-IMPL-012 | `software_versions_future` captures the exact dependency/environment versions used for each replication. | Undetectable environment drift between replications or between an original run and its resume. | Future implementation review of version-capture logic (e.g. dependency lockfile hash, interpreter version). | Resume a replication under a deliberately different dependency version; verify the manifest records the discrepancy. | A future implementation-wave test report confirming version-capture accuracy. | PLANNED_ONLY |
| OD015-IMPL-013 | `container_digest_future` (or equivalent runtime-provenance identifier) is captured for every replication. | Undetectable runtime-environment drift (e.g. base image changes) affecting reproducibility. | Future implementation review of container/runtime digest capture at execution time. | Run the same replication under two different container digests; verify both are distinctly recorded, not silently unified. | A future implementation-wave test report confirming runtime-provenance capture. | PLANNED_ONLY |
| OD015-IMPL-014 | A partially-written or interrupted-mid-write output is quarantined (never treated as a valid completed output) until integrity is verified. | Downstream metrics silently consuming a truncated or corrupt output. | Future implementation review of the output-finalization/quarantine gate. | Force an interruption mid-output-write; verify the partial output is excluded from any metric computation until (and unless) verified complete. | A future implementation-wave test report confirming quarantine enforcement. | PLANNED_ONLY |
| OD015-IMPL-015 | Resume behavior is idempotent — resuming an already-complete replication a second time is a safe no-op, not a duplicate execution, and this idempotency is validated by an execution independent of the one that produced the original checkpoint. | Double-execution of a completed replication (wasting resources, or worse, producing two divergent outputs under the same `replication_id`). | Future implementation review of the idempotency-check gate on resume, plus an independent-process validation run. | Issue a resume command against an already-`EXECUTION_COMPLETE` replication; verify no new execution occurs and the existing output/hash is untouched; repeat the validation from a separate process/session. | A future implementation-wave test report confirming idempotent resume and independent-validation pass. | PLANNED_ONLY |
