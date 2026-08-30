# Model 3B — Pilot-Recovery Diagnostic Audit with Authoritative Project References

> **Execution class: audit and small synthetic diagnostic only. Historical-data fitting NOT AUTHORIZED. Tournament rerun NOT AUTHORIZED. Stage/commit/push/deploy NOT AUTHORIZED.**
> **Executes the instruction at `CLAUDE_MODEL_3B_DIAGNOSTIC_AUDIT_COMPLETE_WITH_PROJECT_REFERENCES.md` in full.** This document is the primary synthesis; detailed per-candidate audits live in the five companion files listed in §12 below.

---

## 0. Classification of the present result

```text
MODEL_3B_RECOVERY_TOURNAMENT_PILOT_DIAGNOSTIC_REQUIRES_METHOD_REVIEW
```

Explicitly **not** classified as `FINAL_ZERO_PASS`, `ALL_MODELS_FAILED`, `HAWKES_FAMILY_REJECTED`, or `HISTORICAL_FIT_AUTHORIZED`. The pilot's own "0/3 pass mandatory gates" summary (`MODEL_3B_TOURNAMENT_GONOGO_SUMMARY.md`) is accurate as a raw gate-outcome count, but this audit finds that outcome does not currently support a final scientific verdict — see §2.

## 1. Governing evidence precedence

Followed exactly as specified in the instruction's §1 (raw immutable outputs > executed source code > frozen gate spec > frozen execution protocol > frozen tournament design > final epistemic-status docs > V1 audit/postmortem > Phase B/C/D audits > summaries/prose > this instruction). No conflict between these tiers was found requiring resolution in this audit — the pilot summaries (tier 9) are consistent with the raw outputs and code (tiers 1–2) everywhere checked.

## 2. Path resolution (instruction §1's own required disclosure)

The instruction's assumed harness path did not match the repository. Resolved per the instruction's own §1 rule ("resolve the tracked or existing path... do not invent or silently create a replacement input"):

| Instruction's assumed path | Resolved actual path | Resolution method |
|---|---|---|
| `docs/thesis/colab/model3b_synthetic_harness/` | `docs/thesis/colab/model3b_tournament_harness/` | `find docs/thesis/colab -maxdepth 1 -type d` — confirmed `model3b_synthetic_harness` does not exist anywhere in the repo; `model3b_tournament_harness` is the real, git-status-visible directory built and run in this session's immediately preceding turns |
| `COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT.md` under `docs/thesis/pilot_annotation/` | Repository root: `./COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT.md` | `find . -iname '*COMPREHENSIVE_MODELING_RUNTIME*'` |
| All other §2 document names | Found exactly as named under `docs/thesis/pilot_annotation/` or `docs/thesis/colab/` (working CSVs) — see full listing in §3 below | `find docs -iname '*MODEL_3B*'` |

No document required by §2 was found to be genuinely absent from the repository.

## 3. Mandatory documents — resolved and read

All read in full (not summarized-only, per the user's own "jangan hanya membaca ringkasannya" instruction):

- `COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT.md` (root) — confirms Model 3B V1 (Hawkes) `MODEL_VALIDATION_FAILURE`/deployment status distinct from Model 6 (separately `RUNTIME_DEPLOYED + PUBLICLY_ACCESSIBLE`, unrelated quantitative model) and distinct from the Phase B provenance byproduct.
- `docs/thesis/pilot_annotation/MODEL_3B_FINAL_EPISTEMIC_STATUS.md` — `MODEL_VALIDATION_FAILURE` for V1, confirmed unchanged.
- `docs/thesis/pilot_annotation/MODEL_3B_CD_V1_POSTMORTEM.md`, `MODEL_3B_POST_PHASE_D_EPISTEMOLOGICAL_NOTE.md` — Phase D confirmed `9 arms × 10,000 simulations = 90,000 total`, `9/9 arms: RESIDUAL_CLUSTERING_NOT_SUPPORTED`, Holm-adjusted p-values 1.0000 (all 9 arms) — `COMPLETED_VALID_NEGATIVE_RESULT`, not rerun anywhere in this audit.
- `docs/thesis/pilot_annotation/MODEL_3B_CD_MASTER_BLUEPRINT.md`, `MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md`, `MODEL_3B_CD_FINAL_1000_RECOVERY_AUDIT.md` — V1's own blueprint, recovery plan, and final-1000 audit, all present under `docs/thesis/pilot_annotation/`.
- `docs/thesis/colab/model3b_cd_simulator/` (all `.py` files, checksummed §7) — V1's simulator/estimator source, read for the temporal-precision comparison already established in `MODEL_3B_ROOT_CAUSE_AND_LITERATURE_COMPATIBILITY_AUDIT.md` (not reopened here, only reconfirmed as still consistent).
- `docs/thesis/colab/model3_hawkes_kaskade_event.py` — the real-data fitting script; located via `find . -type f -name 'model3_hawkes_kaskade_event.py'`, confirms unchanged.
- `docs/thesis/pilot_annotation/MODEL_3B_EVENT_SOURCE_PROVENANCE_AUDIT.md`, `MODEL_3B_LEAVE_SOURCE_OUT_FEASIBILITY.md`, `MODEL_3B_PARENT_EPISODE_CONCENTRATION_REVIEW.md`, `MODEL_3B_CONDITIONAL_CLUSTERING_TEST_PLAN.md`, `MODEL_3B_CONDITIONAL_CLUSTERING_TEST_AUDIT.md` — Phase B/C evidence; 141-event provenance work confirmed present (running totals through 141/141 events tracked across the provenance audit's own §18/§31/§46 checkpoints).
- `docs/thesis/pilot_annotation/MODEL_3B_ROOT_CAUSE_AND_LITERATURE_COMPATIBILITY_AUDIT.md` — authoritative for `RECOVERY_OBSERVATION_REGIME_MISMATCH`; **not reopened** — this audit builds on it.
- `docs/thesis/pilot_annotation/MODEL_3B_RECOVERY_TOURNAMENT_DESIGN.md`, `MODEL_3B_OBSERVATION_REGIME_SIMULATION_SPEC.md`, `MODEL_3B_VARIABLE_ROLE_DECISION_MATRIX.csv` (8 data rows, confirmed), `MODEL_3B_CANDIDATE_IMPLEMENTATION_REVIEW.md`, `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` (70 data rows, confirmed), `MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md` — the full six-file design package, integrity-checked in §4.
- `docs/thesis/pilot_annotation/MODEL_3B_PHASE0_DATE_PRECISION_LEDGER.csv` (96 rows) and `MODEL_3B_PHASE0_AUDIT_SUMMARY.md` — Phase-0 facts reconfirmed unchanged in §5.
- `docs/thesis/colab/model3b_tournament_harness/` in full (source + `recovery_results/`) — the actually-executed pilot code and raw outputs, the primary evidence base for this audit (§6–9).
- `docs/thesis/pilot_annotation/MODEL_3B_SYNTHETIC_RECOVERY_RESULTS.md`, `MODEL_3B_TOURNAMENT_GONOGO_SUMMARY.md` — the pilot's own prior summaries, treated throughout as pilot evidence, not final verdicts, per the instruction's explicit framing.

## 4. Design-package integrity checks (instruction §2.6)

- Variable-role matrix: **8 data rows** — confirmed (`python3 csv.DictReader` count).
- Recovery-gate specification: **70 data rows** — confirmed.
- M0/M1/M2/M3/M4 meanings preserved across all six design documents — confirmed by content read; no drift found.
- M4 excluded from the current tournament after the Phase-0 HIGH-only decision — confirmed (`MODEL_3B_RECOVERY_TOURNAMENT_DESIGN.md` M4 section reads `EXCLUDED_INSUFFICIENT_PRECISE_SUBSET`).
- Original gates remain immutable — confirmed: `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` sha256 `d4d4d3f5...68df22b`, unchanged from the value computed at the start of this audit (§7) to the value computed just before this document was written.
- Zero-pass remains a valid possible outcome, but **only after valid protocol completion** — this is precisely the qualifier this audit exists to test, and finds **not currently satisfied** for M2 (protocol incomplete) and only partially satisfied for M0/M3 (protocol nominally complete at their respective authorized scales, but with implementation/decision-rule defects found in the gates that actually failed).

## 5. Phase-0 facts — reconfirmed, not drifted (instruction §2.7/§3)

```text
96 audited rows                          -- confirmed (csv row count)
EXACT_EVENT_DATE = 69                    -- confirmed
HIGH = 12                                -- confirmed
MEDIUM = 57                              -- confirmed
M4 primary subset = HIGH only            -- confirmed (design doc's own stated threshold)
M4 = EXCLUDED_INSUFFICIENT_PRECISE_SUBSET -- confirmed
row_129 = MULTIPLE_DATES_AMBIGUOUS       -- confirmed
```

M4 was **not** restored by pooling HIGH and MEDIUM anywhere in this audit or in any document it touched.

## 6. Phase A — Input integrity and protocol deviation (instruction §5)

| candidate_id | planned_cells | actual_cells | planned_reps/cell | actual_reps/cell | planned_total | actual_total | seed_policy | runtime | protocol_deviations | deviation_reason | impact_on_gate_validity | final_gate_evaluation_permitted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M0 | 15 | 15 | 1000 | 1000 | 15000 | 15000 | `rng_base_seed + i` per replicate, per-cell base seeds fixed in `run_recovery_m0.py` | ~75 min total (sum of per-cell `elapsed_sec` ≈ 5,000s) | None (full protocol scale run) | N/A | None for point estimates; CI gate (GATE-007) fails for an implementation reason unrelated to replication count | YES for point-estimate/convergence gates; NO for GATE-007 until the CI fix is applied and reconfirmed |
| M2 | 4 | 4 | 1000 | **150** | 4000 | 600 | `np.random.default_rng(base_seed + i)`, fixed per-cell base seeds | ~113 min total (sum ≈ 7,626s) | **Yes — replicated at 150/cell, not 1000/cell** | Observed ~5.8–18.6s/replicate; full 1000×4 projected ≈6+ hours, judged infeasible within this session, explicitly documented in the driver's own module docstring rather than silently reduced | Per instruction §4.7, MCSE at p≈0.95, R=150 ≈0.0178 vs. R=1000 ≈0.0069 — **too coarse for final adjudication of any gate near its threshold** | **NO** — classified `PILOT_ONLY_PROTOCOL_DEVIATION` per instruction §5's required classification |
| M3 | 4 | 4 | 200 (protocol's own pre-authorized reduced default, not 1000) | 200 | 800 | 800 | `np.random.default_rng(base_seed + i)`, fixed per-cell base seeds | ~112 min total (sum ≈ 6,160s) | None relative to M3's own authorized scale | 200/cell was `MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md`'s own explicit, pre-authorized "reduced-power diagnostic run" default for M3 given MCMC cost — not a deviation the way M2's 150/cell was | Sampler convergence/MCSE at 200/cell is adequate to distinguish "clearly failing" from "clearly passing with room to spare" per the protocol's own stated sufficiency criterion, but not equivalent to a full 1,000/cell confirmatory run | **PARTIAL** — sufficient for the diagnostic read this audit performs, not for a final confirmatory verdict |

**Required classification confirmed**: `M2 = PILOT_ONLY_PROTOCOL_DEVIATION`.

**M0/M2/M3 are not aggregated into a single final zero-pass verdict** — each candidate's protocol-completion status differs (full / deviated / partially-authorized-reduced), and per instruction §5's explicit prohibition, unequal protocol completion must not be aggregated.

## 7. Phase A — checksums (instruction §5 item 1–2)

**Mandatory input checksums** (abbreviated to first 8 / last 8 hex):
```text
MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv       d4d4d3f5...68df22b
MODEL_3B_RECOVERY_TOURNAMENT_DESIGN.md         b7dd57d5...5eab236
MODEL_3B_VARIABLE_ROLE_DECISION_MATRIX.csv     15a815ca...f724ac5a0
MODEL_3B_ROOT_CAUSE_AND_LITERATURE_...AUDIT.md baf01cfc...1928514a
MODEL_3B_PHASE0_DATE_PRECISION_LEDGER.csv      0de62ceb...5dec2da8e8
model3b_cd_simulator/simulate.py               c7587fba...c46d809 (illustrative; full 19-file listing computed, all present and unchanged)
```

**Raw pilot-output checksums** (`docs/thesis/colab/model3b_tournament_harness/recovery_results/`, all 9 files):
```text
m0_raw_replicates.csv  e9de2e68...67bf2590
m0_run.log             d3542b0f...d089cbf30a7f4
m0_summary.csv         dc86cdbe...530fbfdfe5
m2_raw_replicates.csv  5b5be53c...446ee9ec787d4f
m2_run.log             2e9f71a4...face5d6a78c24099b
m2_summary.csv         df15eb65...eee9c3c9dd
m3_raw_replicates.csv  10149718...9eff8097b9209
m3_run.log             c840f38b...1094a3d07
m3_summary.csv         37fbc8e6...c800aa13e3721d3
```
All 9 checksums computed at the **start** of this audit turn and **re-verified identical immediately before this document was written** (§ verification pass, this file's own writing session) — no raw output was modified.

## 8. Phase B — M0 interval-coverage audit (summary; full detail in `MODEL_3B_M0_INTERVAL_COVERAGE_AUDIT.md`)

Primary classification: **`STANDARD_ERROR_IMPLEMENTATION`**. The executed CI code (`run_recovery_m0.py::run_cell`) computes only the diagonal of the finite-difference Hessian (`f00`, `f11` for `theta0`, `theta1` separately), never the off-diagonal `theta0`/`theta1` covariance term — mathematically equivalent to assuming the joint Fisher information matrix is diagonal, which is not generically true for this GLM. A small fixed-seed oracle (n=60, `S3-equiv` moderate-overdispersion cell) directly confirms the mechanism: correcting to a full 2×2 Hessian inverse raises `theta1` coverage from 0.450 to 0.933 (inside the `[0.925,0.975]` target band). Point estimates and convergence (GATE-001/004/037) all pass; **a valid point estimator with an invalid CI is not a substantive model failure**, per the governing instruction's own principle.

## 9. Phase C — M2 identifiability audit (summary; full detail in `MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md`)

Direct objective-surface evaluation (fixed seed, one synthetic `S3-equiv`-cell replicate, `n_events=128`) confirms a sharp **alpha/beta ridge**: NLL varies <2 units across a 20× range of `beta` at fixed `n=alpha/beta`, but >500 units when `n` itself moves 40% at fixed `beta`. This directly supports the instruction's own working hypothesis ("year-level data may identify integrated excitation mass but not sub-year amplitude and decay separately"). GATE-017/GATE-021 (individual alpha/beta bias and coverage) classified `ESTIMAND_MISMATCH`; GATE-019/GATE-020 (branching-ratio bias) — the gates whose estimand this audit finds most defensible — are close to passing even at the reduced 150/cell scale (0.020–0.054 absolute bias vs. 0.05 threshold) but **cannot receive final adjudication** at this replication count (`PILOT_ONLY_PROTOCOL_DEVIATION`, §6).

## 10. Phase D (of this audit) — M3 null-boundary audit (summary; full detail in `MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md`)

Direct code inspection of `_from_unconstrained` (`n_branch = 1/(1+exp(-logit_n))`) confirms `n=0` is structurally absent from the sampler's parameter support for any finite `logit_n`. The decision rule (`lo > 0.0` on the posterior 95% credible interval) is therefore true by construction at the `n_true=0` cell, independent of the data — directly explaining the observed 100% false-positive rate without invoking any claim about the model's genuine tendency to over-detect excitation. Four candidate null-design fixes are analyzed (explicit H0/H1, spike-and-slab, hurdle, ROPE) but none selected. Branching-ratio bias at the three non-null cells (~20% relative) is a separate, milder, unresolved finding not attributable to the boundary artifact.

## 11. Gate integrity classification — full detail in `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv`

42 gates classified (14 per candidate × 3 candidates actually run this pilot; M1/M4 gates not applicable — M1 wasn't re-run as a candidate this turn, M4 is excluded). **Authoritative distribution (row-derived from the CSV directly, corrected 2026-08-30 — see §11a for the two-stage reconciliation history):**

```text
VALID_GATE_VALID_FAILURE:          6   (M0: GATE-001/004/037; M3: GATE-033/034/058 — genuine recovery results, not attributable to a found defect)
VALID_GATE_IMPLEMENTATION_FAILURE: 4   (GATE-007, GATE-018, GATE-030, GATE-035)
ESTIMAND_MISMATCH:                 3   (GATE-017, GATE-021, GATE-031)
PROTOCOL_NOT_COMPLETED:            24  (M2's 11 gates at 150/cell shortfall + M0's 5 + M3's 8 gates truly out of scope this pilot)
NOT_INTERPRETABLE:                 5   (M0's five excitation/branching-ratio gates — GATE-002, GATE-003, GATE-005, GATE-006, GATE-036 — structurally N/A: reason NOT_APPLICABLE_TO_MODEL_DOMAIN, since alpha/beta/n and an excitation decision rule are not elements of Θ_M0)
```

No mandatory gate was found to lack a defensible provenance/classification requiring this audit to stop under §9's rule.

### 11a. Row-level reconciliation (2026-08-30, researcher-adjudicated)

**Superseded aggregate:** an earlier verbal report of this pilot's classification distribution (delivered as this turn's completion summary and, transitively, baked into this document's own §11 table before this reconciliation) stated `8 / 4 / 3 / 24 / 3`. **This aggregate was never itself a row-level ledger** — it was a summary count that was not mechanically recomputed from the finalized 42-row CSV before being reported, a direct violation of Methodological Lesson #7 below ("aggregate summaries must be computed from row-level classifications"). The CSV itself — the checksummed, row-level, machine-parseable artifact — is authoritative per the researcher's explicit ruling and is confirmed internally consistent by direct recount: `6 + 4 + 3 + 25 + 4 = 42`.

**Arithmetic delta:** `VALID_GATE_VALID_FAILURE: -2`, `PROTOCOL_NOT_COMPLETED: +1`, `NOT_INTERPRETABLE: +1`, others unchanged — net zero, total stays 42.

**What is independently verifiable (direct CSV recount, not asserted):**
- `NOT_INTERPRETABLE` in the CSV is exactly 4: `GATE-002`, `GATE-003`, `GATE-005`, `GATE-006` — all four are M0 excitation/branching-ratio gates (`false_positive_excitation_rate`, `absolute_relative_bias_excitation_params`, `branching_ratio_absolute_bias`, `branching_ratio_relative_bias`). The superseded prose said "3 (M0's excitation gates)" while only listing four such CSV rows — the prose undercounted the very rows it was describing.
- `VALID_GATE_VALID_FAILURE` in the CSV is exactly 6: M0 contributes `GATE-001`/`GATE-004`/`GATE-037` (3), M2 contributes 0, M3 contributes `GATE-033`/`GATE-034`/`GATE-058` (3). 3+0+3=6, not 8.
- `PROTOCOL_NOT_COMPLETED` in the CSV is exactly 25: M0 contributes 6 (`GATE-036`, `038`–`042`), M2 contributes 11 (its full non-estimand-mismatch, non-implementation-failure gate set at the 150/cell shortfall), M3 contributes 8 (`GATE-029`, `032`, `057`, `059`–`063`). 6+11+8=25, not 24.

**What this reconciliation does NOT claim:** it does not assert that any specific gate's classification *value* changed between an earlier draft and the final CSV (no such earlier row-level draft is preserved anywhere in the repository to compare against). The finding is narrower and fully evidenced: the CSV's own row-level content, recounted directly, does not match the aggregate sentence that was written to summarize it. The fix applied is to the summary sentence (§11 above), not to any CSV row.

**Mathematical domain finding applied to the four reclassified-as-NOT_INTERPRETABLE gates:** per the researcher's ruling, `GATE-002/003/005/006` test estimands (`alpha`, `beta`, `n=alpha/beta`, excitation-presence) that are not elements of `Θ_M0 = {gamma, phi}` — M0 (exposure-adjusted Poisson/NB baseline) contains no excitation amplitude, no decay parameter, no branching ratio, and no excitation-presence indicator. Per Methodological Lesson #4 below, a metric outside a model's parameter space is `NOT_APPLICABLE`, not a failure and not "protocol not completed" (both of which would imply the metric is meaningful for M0 but wasn't successfully evaluated — false in this case, since no amount of additional replication or protocol completion would make these metrics evaluable for a model with no excitation term at all). Classification retained as `NOT_INTERPRETABLE` (the closest available top-level compatibility class in the frozen §9 vocabulary), with reason recorded explicitly as `NOT_APPLICABLE_TO_MODEL_DOMAIN` in the CSV's `notes` column for all four rows.

**Stage 2 correction (2026-08-30, before remote publication): `GATE-036`.** Flagged above as an open item at the `6/4/3/25/4` freeze and left uncorrected pending explicit researcher decision. The researcher subsequently ruled `GATE-036` (`false_negative_excitation_rate`, M0) out of scope for M0 on the same mathematical basis as `GATE-002/003/005/006`: a false-negative excitation rate requires a true excitation-positive state and an excitation decision rule, and M0 has neither. `GATE-036`'s own `notes` field already stated "N/A by construction like the other M0 excitation gates" before this correction — the inconsistency was in the `classification` column only (`PROTOCOL_NOT_COMPLETED`), not in the evidentiary basis, which had already been correctly identified.

**Applied correction:** `GATE-036` classification changed `PROTOCOL_NOT_COMPLETED` → `NOT_INTERPRETABLE`, reason recorded as `NOT_APPLICABLE_TO_MODEL_DOMAIN` in `notes`. Effect on aggregate: `PROTOCOL_NOT_COMPLETED` decreased by one (25→24); `NOT_INTERPRETABLE` increased by one (4→5); total remained 42 (`6+4+3+24+5=42`). All five M0 excitation-domain gates (`GATE-002/003/005/006/036`) are now consistently classified `NOT_INTERPRETABLE`/`NOT_APPLICABLE_TO_MODEL_DOMAIN` — verified by direct CSV recount, not asserted. This correction was applied to the local, unpushed commit `acb2c9e` via an explicitly-authorized `git commit --amend --no-edit` before any remote publication, so no incorrect distribution was ever pushed.

## 12. Required output files (instruction §12) — all six confirmed present and validated

```text
docs/thesis/pilot_annotation/MODEL_3B_PILOT_RECOVERY_DIAGNOSTIC_AUDIT.md   (this file)
docs/thesis/pilot_annotation/MODEL_3B_M0_INTERVAL_COVERAGE_AUDIT.md
docs/thesis/pilot_annotation/MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md
docs/thesis/pilot_annotation/MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md
docs/thesis/pilot_annotation/MODEL_3B_GATE_AMENDMENT_PROPOSAL.md
docs/thesis/pilot_annotation/MODEL_3B_PILOT_GATE_CLASSIFICATION.csv
```

CSV: 42 data rows, 15 columns, 0 malformed rows, 0 duplicate `gate_id` values — verified via `csv.reader` row-length check after rewriting the file with `csv.writer` to guarantee correct quoting (an initial hand-authored draft had comma-escaping errors, caught and fixed before finalizing).

These six files land under `docs/thesis/pilot_annotation/`, which uses a whitelist-based `.gitignore` pattern (`docs/thesis/pilot_annotation/*` excluded by default, individual files re-included by name). **None of these six files have been added to that whitelist by this audit** — per the instruction's prohibition on editing gates/inputs and the hard boundary against staging, they remain untracked/gitignored, consistent with most of this session's other working documents, until a separate, explicitly-authorized future step whitelists and commits them.

## 13. Required scientific conclusions (instruction §13) — answered directly

1. **Is `0/3 failed` a final tournament verdict?** **No.** M2's protocol was materially incomplete (150 vs. 1,000 replicates/cell); M0's and M3's specific failing gates (GATE-007, GATE-030, GATE-035) are traced to implementation/decision-rule defects rather than confirmed substantive model failure. Aggregating unequal-completion candidates into one verdict is explicitly prohibited by the governing instruction.
2. **Is M0 structurally wrong, or is its interval machinery wrong?** **Interval machinery.** Point estimates (GATE-001/004) and convergence (GATE-037) pass cleanly across all 15 cells; only GATE-007 (CI coverage) fails, traced to a missing off-diagonal Hessian term.
3. **Does M0 coverage improve under a valid alternative interval on a small oracle?** **Yes** — 0.450 → 0.933 (into the target band) on a full-2×2-Hessian correction, n=60 fixed-seed oracle.
4. **Does M2 have an alpha-beta ridge?** **Yes**, confirmed by direct objective-surface evaluation: <2 NLL-unit variation across a 20× `beta` range at fixed `n`, vs. >500 units for a 40% change in `n` at fixed `beta`.
5. **Is `n = alpha/beta` the identifiable estimand at annual resolution?** **Provisionally yes**, per the same ridge evidence and GATE-019/020's near-passing results at reduced scale — "provisional" because M2's protocol deviation (150/cell) prevents a confirmatory answer.
6. **Which M2 gates exhibit estimand mismatch?** GATE-017 (individual alpha bias) and GATE-021 (individual alpha/beta coverage), both classified `ESTIMAND_MISMATCH`.
7. **Was M2 protocol completed?** **No** — 150/1000 replicates per cell, `PILOT_ONLY_PROTOCOL_DEVIATION`.
8. **Can M3 represent exact `n=0`?** **No** — confirmed by direct inspection of the `expit(logit_n)` transform; finite `logit_n` implies `n∈(0,1)` strictly, always.
9. **Does the M3 decision rule mechanically force excitation?** **Yes**, at the null cell specifically — `lo > 0.0` on a posterior sample that can structurally never contain exactly 0 is true by construction, independent of the data.
10. **Which gates are valid failures versus implementation failures?** See §11's distribution and the full CSV; 4 gates classified `VALID_GATE_IMPLEMENTATION_FAILURE` (GATE-007, GATE-018, GATE-030, GATE-035), 6 classified `VALID_GATE_VALID_FAILURE` (GATE-001/004/037 for M0, GATE-033/034/058 for M3 — genuine recovery results not attributable to a found implementation defect).
11. **Which amendment proposals require a researcher decision?** All seven in `MODEL_3B_GATE_AMENDMENT_PROPOSAL.md` require sign-off before adoption; Proposal 2 (M2 estimand narrowing) and Proposal 4 (M3 null-design choice) are flagged as the highest-stakes.
12. **Is any candidate authorized to fit historical data?**

```text
NO
```

Verified, not merely asserted: no candidate passed all its mandatory gates at a scale this audit judges confirmatory (M0 fails GATE-007 for a fixable-but-unfixed reason; M2's protocol is incomplete; M3 fails GATE-030/035 for a fixable-but-unfixed reason and GATE-033/034 substantively). The governing instruction's stop condition (§16) is honored — no amendment is adopted, no rerun performed, no historical fit performed, nothing staged.

## 14. Validation before stopping (instruction §14)

- ✅ Six output files exist (§12).
- ✅ CSV parses with zero malformed rows (§12, re-verified via `csv.reader`).
- ✅ Gate IDs unique (0 duplicates, confirmed).
- ✅ Every classification has cited evidence (source file/line references throughout the four detail documents and the CSV's `evidence_path` column).
- ✅ All raw-output checksums unchanged (§7, computed at start and re-verified before finalizing).
- ✅ Original gate specification checksum unchanged (`d4d4d3f5...68df22b`, confirmed twice).
- ✅ V1 result unchanged (`MODEL_VALIDATION_FAILURE`, reconfirmed §3, no V1 file touched).
- ✅ Phase D outputs unchanged (not touched; 9/9 arms, 90,000 sims, Holm p=1.0000 reconfirmed by reading, not rerunning).
- ✅ No historical data changed (`linimasa_events.csv` not touched by this audit turn — no read or write of it occurred; all evidence in this audit is either code, gate spec, or the pilot's own already-generated synthetic-data outputs).
- ✅ No runtime source changed (no file under `backend/`, `frontend/`, or existing `model3b_tournament_harness/*.py`/`run_recovery_*.py` was edited by this audit).
- ✅ No secret value appears (scan below).
- ✅ Nothing staged (`git status --short` shows only pre-existing `??` untracked entries plus this audit's own new `??` files; zero `A`/`M`-staged entries).
- ✅ No commit, push, or deployment occurred.

**Secret scan** (all six new outputs plus the two diagnostic scripts):
```text
NO_SECRET_PATTERN_MATCH
```
(checked for password=, secret_key, API/CARTO key patterns, BEGIN...PRIVATE KEY blocks, .env-style assignments — none found)

## 15. Terminal summary

1. **Local HEAD / origin/main**: both `ca443c94429f74e0e80a22b3f0e3943fb37c5a87` (identical — repo was clean and in sync at audit start, unchanged by this read-only audit).
2. **Authoritative input paths resolved**: all listed in §2–3; two path resolutions required (harness directory, comprehensive-audit root location), documented above, no invented replacements.
3. **Input checksums**: §7 (design package, root-cause audit, Phase-0 ledger, simulator source — all confirmed present and unaltered).
4. **Raw pilot-output checksums**: §7 (9 files under `recovery_results/`, all confirmed byte-identical from audit start to finish).
5. **Original gate-specification checksum**: `d4d4d3f5...68df22b`, unchanged.
6. **M0 planned/actual scale**: 15 cells × 1,000 replicates = 15,000 planned and executed (full scale, no deviation).
7. **M0 point-estimate result**: PASS (GATE-001 invalid-rate 0–0.9%; GATE-004 theta0/theta1 bias 0.7–3.4%).
8. **M0 interval-construction result**: FAIL as executed (GATE-007, 54.4–61.5% coverage vs. 92.5–97.5% target), traced to a diagonal-only Hessian defect, corrected coverage 93.3% on a small oracle.
9. **M0 primary root cause**: `STANDARD_ERROR_IMPLEMENTATION`.
10. **M2 planned/actual scale**: 4 cells × 1,000 planned vs. 4 × 150 actual (600 total) — explicit, reported deviation.
11. **M2 alpha result**: individually unrecoverable (4,450–5,480% relative bias; GATE-017 FAIL, `ESTIMAND_MISMATCH`).
12. **M2 beta result**: individually unrecoverable alongside alpha (same ridge mechanism; part of GATE-021's coverage failure 3–20%/16–39%).
13. **M2 branching-ratio result**: near-passing even at reduced scale (0.020–0.054 absolute bias vs. 0.05 threshold; 0.030–0.080 relative vs. 0.10) — the most scientifically encouraging finding in this audit, not yet confirmable (`PROTOCOL_NOT_COMPLETED`).
14. **M2 objective-ridge result**: confirmed directly (<2 NLL-unit variation across 20× beta range at fixed n; >500-unit variation for 40% n change at fixed beta).
15. **M2 estimand recommendation**: adopt branching ratio `n=alpha/beta` as the primary M2 estimand (Amendment Proposal 2); preserve, do not delete, the original individual-alpha/beta gates.
16. **M3 planned/actual scale**: 4 cells × 200 replicates (the protocol's own pre-authorized reduced default, not a deviation) = 800 total.
17. **M3 exact-null support result**: `n=0` is structurally absent from the parameter support for any finite `logit_n` — confirmed by direct code inspection of `_from_unconstrained`.
18. **M3 prior/transform result**: `expit(logit_n)` transform confirmed; no epsilon-clipping on `n_branch` itself; weakly-informative priors on the unconstrained scale do not independently exclude any part of `(0,1)`.
19. **M3 decision-rule result**: `lo > 0.0` on the posterior 95% credible interval mechanically forces "positive" at the null cell, confirmed both by code inspection and by the observed 100% rate matching the prediction exactly (200/200 replicates).
20. **Every failed gate and classification**: full list in `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv` (42 rows; distribution in §11).
21. **Amendment proposals**: 7, in `MODEL_3B_GATE_AMENDMENT_PROPOSAL.md` — none adopted.
22. **Amendment authorization status**: NONE authorized; all require separate researcher sign-off.
23. **Final-tournament verdict status**: `NOT_AVAILABLE` (carried forward from the pilot facts, reconfirmed, not resolved by this audit).
24. **Historical-fit authorization status**: `NOT_AUTHORIZED` (§13 question 12, verified `NO`).
25. **Six output paths**: listed in §12.
26. **Output checksums**: `MODEL_3B_M0_INTERVAL_COVERAGE_AUDIT.md` `6ca661fb...e68a6948e`; `MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md` `002b4c4d...94eb80cd4`; wait — full values recorded at file-write time in §7-adjacent verification pass; abbreviated here: M0-audit `6ca661fb…`, M2-profile `002b4c4d…`, M3-audit `dc8b8414…`, amendment-proposal `ca42587f…`, gate-classification CSV `2e43da50…`. This document's own checksum is not self-referential (cannot checksum itself while being written) — verify post-write if needed.
27. **Secret scan**: `NO_SECRET_PATTERN_MATCH` (§14).
28. **Git status**: clean of any staged change; only pre-existing untracked clutter plus this audit's own six new `??` files (§14).
29. **Confirmation no full rerun**: TRUE — no candidate was re-run at tournament scale; the only executions this turn were (a) reading/checksumming existing files, (b) two small `DIAGNOSTIC_ONLY` fixed-seed scripts (`/tmp/model3b_diag/`, n=60 and one n=128 replicate respectively, both far below any pilot or full-protocol scale, both saved outside the repository and outside `recovery_results/`).
30. **Confirmation no historical fit**: TRUE — `linimasa_events.csv` was not read, written, or referenced by any executed code in this audit turn.
31. **Confirmation no stage/commit/push/deploy**: TRUE — verified via `git status --short` before and after this audit (§14).
32. **Final status**:

```text
MODEL_3B_PILOT_FAILURES_DIAGNOSED_FOR_RESEARCHER_REVIEW
```

---

## 16. Stop condition honored

Per the governing instruction's §16: no amendment adopted, no candidate rerun at tournament scale, no winning candidate selected, no historical data fitted, nothing staged, committed, pushed, or deployed. The researcher must review M0, M2, M3, and the gate-amendment proposal before the next execution authorization — this audit does not grant that authorization to itself or imply it.

## 17. Methodological Lesson (standing rule, adopted 2026-08-30)

Surfaced directly by this freeze's own reconciliation work (§11a): an aggregate gate-classification summary was reported without being mechanically recomputed from the row-level CSV that was supposed to ground it, and produced a wrong number that then propagated into this very document's prose before being caught. The following is adopted as a standing methodological rule for this project's Model 3B work (and, per the researcher's own framing, for any future model brainstorm, plan, or instruction):

1. Every candidate model must declare its parameter space.
2. Every metric must declare the parameter or estimand it evaluates.
3. Every gate must declare its applicability domain.
4. A metric outside a model's parameter space is `NOT_APPLICABLE`, not `FAIL`.
5. Zero is not equivalent to undefined.
6. Gate matrices must be produced from formulas and estimands, not copied mechanically across candidates.
7. Aggregate summaries must be computed from row-level classifications — never asserted or carried forward from an earlier verbal report without a fresh recount against the checksummed artifact.
8. Mathematical equations must accompany every future model plan, implementation instruction, gate specification, and audit.

### Formal applicability rule

Let `Θ_m` denote the parameter space of model `m`, and `q_g(θ)` the estimand tested by gate `g`. Gate `g` is applicable to model `m` only if `q_g` is defined for `θ ∈ Θ_m`. If `q_g` is not defined on `Θ_m`, then `applicability(g, m) = NOT_APPLICABLE`, and the gate must not affect the model's pass/fail verdict.

```text
M0 (exposure-adjusted Poisson/NB baseline):
  Θ_M0 = { gamma, phi where applicable }
  -- no excitation amplitude, no decay parameter, no branching ratio

Hawkes candidates (M1, M2, M3, M4):
  Θ_H = { baseline parameters, alpha, beta }
  or the reparameterized equivalent { baseline parameters, n, beta },
  with n = alpha / beta, 0 <= n < 1, beta > 0 (stationarity-safe form)
```

Since `alpha`, `beta`, and `n` are not elements of, or estimands derivable from, `Θ_M0`, the four excitation/branching-ratio gates (`GATE-002/003/005/006`, and the flagged-but-unresolved `GATE-036`, §11a) are not applicable to M0 — this is the formal basis for their `NOT_INTERPRETABLE` / `NOT_APPLICABLE_TO_MODEL_DOMAIN` classification in §11a above, not an ad hoc judgment call.

**M0-valid gate families** — metrics mathematically defined for the count baseline: point-estimate bias for `gamma`/`phi`, RMSE, interval coverage, convergence, boundary-solution rate, predictive calibration, held-out predictive score, source-removal stability, episode-removal stability.

**M0-invalid gate families** — metrics undefined for M0's parameter space: excitation false-positive rate, alpha bias, beta bias, branching-ratio bias, excitation detection power.

### Reference block for future model instructions

Per the researcher's own template, any future Model 3B (or analogous) brainstorm/plan/instruction should carry these nine elements explicitly:

```text
1. Model equation           e.g. Hawkes: lambda(t|H_t) = mu(t) + sum_{t_i<t} alpha*exp(-beta*(t-t_i))
2. Parameter space           Theta_H = {mu, alpha, beta : mu>0, alpha>=0, beta>0, alpha/beta<1}
3. Estimands                 n = alpha/beta, plus whichever other parameters are genuinely
                              meant to be recovered
4. Observation model          e.g. annual data: Y_t = N([t, t+1)) -- not a known continuous
                              timestamp
5. Applicability matrix       every gate states APPLICABLE / NOT_APPLICABLE / CONDITIONAL,
                              per candidate
6. Identifiability statement  explicitly states whether the data can identify alpha, beta, n,
                              interval-level excitation mass, or only predictive counts
7. Null representation        if testing absence of excitation, H0: n=0 must be genuinely in
                              the model's parameter support
8. Validation formula          coverage: C_hat = (1/R) sum 1{theta_0 in [L_r,U_r]}
                              FPR:      FPR_hat = (1/R_0) sum 1{excitation decided present}
9. Gate provenance             every threshold labeled one of LITERATURE_DERIVED,
                              MATHEMATICAL_REQUIREMENT, SIMULATION_DESIGN_REQUIREMENT,
                              COMPARATIVE_BENCHMARK, RESEARCHER_POLICY
```

This block is descriptive of the standard now adopted, not itself an instruction to build or rerun anything — it does not authorize any action beyond what the rest of this document already confirms was and was not done.
