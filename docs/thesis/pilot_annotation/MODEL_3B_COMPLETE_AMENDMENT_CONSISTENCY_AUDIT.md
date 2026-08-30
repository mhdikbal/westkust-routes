# Model 3B — Complete Amendment Consistency Audit

> **Consistency audit only. Does not implement any amendment, create a gate specification V2 or protocol V2, modify M0/M2/M3 source, rerun any model, run calibration, select a threshold or prior, or fit historical data. Read-only against all seven adjudication documents, the ledger, the original gate specification, raw pilot outputs, and the tournament harness.**

---

## 1. Scope

Audits the internal consistency of all seven Model 3B amendment adjudications (Proposals 1-7, all `APPROVED_WITH_LIMITATIONS`, none implemented) for coherent equations, parameter spaces, estimands, gate applicability, versioning direction, and implementation ordering — not for scientific correctness of the underlying pilot findings (already audited and frozen separately) and not as an implementation authorization of any kind.

## 2. Authoritative Evidence

```text
Diagnostic-audit commit:    4b94cd689c995765102b4ca4c63e2636334432bb
Authoritative ledger:       docs/thesis/pilot_annotation/MODEL_3B_AMENDMENT_DECISION_LEDGER.csv
Seven adjudication docs:    MODEL_3B_AMENDMENT_01_M0_ADJUDICATION.md
                             MODEL_3B_AMENDMENT_02_M2_ESTIMAND_ADJUDICATION.md
                             MODEL_3B_AMENDMENT_03_M2_FULL_SCALE_ADJUDICATION.md
                             MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATION.md
                             MODEL_3B_AMENDMENT_05_M3_DECISION_RULE_ADJUDICATION.md
                             MODEL_3B_AMENDMENT_06_ADVISORY_GATES_ADJUDICATION.md
                             MODEL_3B_AMENDMENT_07_M3_GATE031_RETIREMENT_ADJUDICATION.md
Supporting (read-only):     MODEL_3B_PILOT_RECOVERY_DIAGNOSTIC_AUDIT.md,
                             MODEL_3B_M0_INTERVAL_COVERAGE_AUDIT.md,
                             MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md,
                             MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md,
                             MODEL_3B_GATE_AMENDMENT_PROPOSAL.md,
                             MODEL_3B_PILOT_GATE_CLASSIFICATION.csv,
                             MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv (original, 70 rows),
                             MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md,
                             docs/thesis/colab/model3b_tournament_harness/ (source + raw outputs)
```
All paths resolved from the repository as-is; no path differed from what the governing instruction assumed.

## 3. Seven-Decision Distribution

Validated with a proper CSV parser against `MODEL_3B_AMENDMENT_DECISION_LEDGER.csv`:

```text
Rows: 7. Proposal IDs: PROPOSAL-01..07, unique, matches expected sequence exactly.
Malformed rows: 0. Duplicate rows: 0. Blank required fields: 0.
researcher_decision = APPROVED_WITH_LIMITATIONS for all 7: TRUE
decision_status = ADJUDICATED for all 7: TRUE
implementation_authorized = NO for all 7: TRUE
rerun_authorized = NO for all 7: TRUE
historical_fit_authorized = NO for all 7: TRUE
```
All 7 markdown adjudication files: UTF-8 valid, code fences balanced, headings structurally complete, final-status line present, no truncation (verified directly, not asserted).

## 4. Mathematical Domains

```text
Theta_M0 = {gamma; phi where applicable}. Does NOT contain alpha, beta,
  branching ratio n, excitation-state indicator, or excitation decision
  rule. Confirmed consistent across Proposal 1 (prose form) and Proposal 6
  §7 (explicit Theta_M0 notation) -- no contradiction found.

Theta_M2 (approved future direction, Proposals 2/3) = {baseline; n
  (primary); beta (secondary/diagnostic)}. g(u)=alpha*exp(-beta*u);
  n=alpha/beta=integral_0^inf g(u)du. Stationarity-safe form: alpha=n*beta,
  0<=n<1, beta>0. Confirmed consistent across Proposal 2 §8, Proposal 3
  §14, Proposal 6 §7.

Theta_M3 (approved future design, Proposals 4/5) = {exact-null model M0:
  n=0; excitation model M1: 0<n<1; baseline/observation params; excitation
  magnitude conditional on M1; P(M1|Y)}. Confirmed consistent across
  Proposal 4 §5/§11, Proposal 5 §5/§8, Proposal 6 §7, Proposal 7 §5.
```
No adjudication document contradicts these domains.

## 5. Cross-Proposal Dependencies

Full detail: `MODEL_3B_AMENDMENT_DEPENDENCY_MATRIX.csv`.

```text
PROPOSAL-01: standalone (M0), no dependency.
PROPOSAL-02 <-> PROPOSAL-03: joint, non-sufficient (M2) -- neither alone
  authorizes implementation; both required in one versioned package.
PROPOSAL-04 -> PROPOSAL-05 -> PROPOSAL-07: linear chain (M3) -- exact-null
  support, then decision-rule form built on it, then gate retirement built
  on both. No back-reference creates a cycle.
PROPOSAL-06: downstream of 1/2/4/5 (all candidates' amended equations).

NO_CIRCULAR_DEPENDENCY: verified TRUE by direct graph construction.
NO_MISSING_GOVERNING_DECISION: verified TRUE -- every "depends on" reference
  in every document resolves to an existing, adjudicated proposal.
No implementation step appears before its governing decision (all seven
  documents' own §Implementation Nonauthorization sections confirm this).
No rerun appears before versioned specifications are frozen (all seven
  confirm rerun_authorized=NO).
```
**Nonblocking finding:** `MODEL_3B_AMENDMENT_02_M2_ESTIMAND_ADJUDICATION.md` §13 still reads "(Proposal 4, not yet adjudicated)" — stale phrasing from when Proposal 2 was written, since Proposal 4 is now adjudicated. The substance (M3's exact-null solution does not automatically transfer to M2) is correct and unaffected; only the parenthetical is dated. Not corrected in this audit (read-only against the seven documents); flagged for a future editorial pass.

## 6. M0 Consistency

All 10 required checks verified against `MODEL_3B_AMENDMENT_01_M0_ADJUDICATION.md` directly: full parameter vector (`theta0`, `theta1`, `log_phi`) confirmed required (§ Limitation 3, Scientific Basis); `phi` inclusion explicit; NLL-minimization sign convention confirmed from source (`minimize()` call site); parameter order matches optimizer signature; Jacobian requirement for `log_phi`->`phi` stated (Limitation 10); diagonal-only silent fallback prohibited (Limitation 8); pseudoinverse must be disclosed as degraded (Limitation 9); 93.3% oracle explicitly not final PASS (§ Diagnostic Oracle); original 15,000-replication pilot outcome preserved unmodified (§ Scientific Basis, unchanged from the diagnostic audit).

```text
M0_IMPLEMENTATION_CORRECTION_APPROVED: TRUE
M0_FINAL_PASS_NOT_ESTABLISHED: TRUE (explicit in the document's own §Final
  M0 Status: M0_FINAL_GATE_PENDING_CORRECTED_RERUN)
```

## 7. M2 Consistency

All required checks verified against `MODEL_3B_AMENDMENT_02_M2_ESTIMAND_ADJUDICATION.md` and `MODEL_3B_AMENDMENT_03_M2_FULL_SCALE_ADJUDICATION.md`: `n` as primary estimand confirmed (§6 of doc 02); `alpha`/`beta` explicitly `DIAGNOSTIC_ONLY` (§6, §7); `beta` weak-identification risk disclosed (§9, "may remain weakly identified... must be checked, not assumed"); `n` explicitly not a historical-causal-probability claim (§10, full prohibited-interpretation list); original gates preserved, not deleted (§11); new versioned file required, original not overwritten (§12); 150 vs 1,000 replication distinction preserved verbatim in both documents; attempted/completed/converged/boundary/invalid distinguished (doc 03 §9); no silent replacement of failed replications (§9, "an optimization failure is itself scientific evidence"); MCSE mandatory (§5, formula given); no data-dependent early stopping (§12, explicit prohibition list).

**Replication-denominator resolution:** checked directly against `MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md` — the protocol's own text ("1,000 replicates per cell") does not disambiguate attempted-vs-valid-for-metric-calculation. Doc 03 §8 correctly leaves this `REPLICATION_DENOMINATOR_REQUIRES_EXPLICIT_PREEXECUTION_DECISION`, not silently decided. **Confirmed still pending, as required — this audit does not resolve it either.**

## 8. M3 Consistency

All required checks verified against `MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATION.md`, `MODEL_3B_AMENDMENT_05_M3_DECISION_RULE_ADJUDICATION.md`, `MODEL_3B_AMENDMENT_07_M3_GATE031_RETIREMENT_ADJUDICATION.md`: exact `n=0` representability required (doc 04 §6); `logit(n)` alone confirmed structurally insufficient (doc 04 §5); epsilon-clipping explicitly rejected as an exact-null solution (doc 04 §10, `M3-NULL-D/E/F`); `M3-NULL-A` (explicit two-model comparison) preferred (doc 04 §7); `P(M1|Y)` primary decision quantity (doc 05 §7); `tau` explicitly unselected (doc 05 §6, §9); calibration/evaluation seed-set separation mandatory (doc 05 §10); `FPR<=0.05` stated necessary-not-sufficient (doc 05 §9); FNR/power jointly evaluated (doc 05 §9, §12); `INCONCLUSIVE` mandatory outcome (doc 05 §18); prior odds unselected (doc 05 §14); Bayes factor secondary diagnostic only (doc 05 §15); ROPE supplementary only (doc 05 §16); `GATE-031` retirement prospective-only (doc 07 §8); replacement gates `M3-REPL-031-A..E` cover the original purpose (doc 07 §12); magnitude-conditional-on-`M1` kept separate from existence (doc 05 §17, doc 07 §12-E).

```text
Required consistency statement, confirmed present verbatim (doc 05 §17):
  EXACT_NULL -> MODEL_EXISTENCE_DECISION -> CONDITIONAL_MAGNITUDE_ESTIMATION
Prohibited pattern, confirmed absent from all three documents:
  SMALL_POSITIVE_N -> AUTOMATIC_EXCITATION_DECISION
  (doc 05 §17: "A model-averaged small positive n must not be reported as
  proof of excitation existence")
```

## 9. Advisory-Gate Reconciliation

Recomputed mechanically, directly from `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv` cross-joined against `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`'s `mandatory_advisory_status` column, keyed correctly by **(candidate, metric)** pair (not metric name alone):

```text
Total PROTOCOL_NOT_COMPLETED: 24 (confirmed, matches all prior turns)
Mandatory-tier among these:    7  -- GATE-015, GATE-016, GATE-019, GATE-020,
                                      GATE-029, GATE-032, GATE-051
Advisory-tier among these:     17 -- GATE-038/039/040/041/042 (M0),
                                      GATE-050/052/053/054/055/056 (M2),
                                      GATE-057/059/060/061/062/063 (M3)
```

**MATERIAL INCONSISTENCY FOUND:** `MODEL_3B_AMENDMENT_06_ADVISORY_GATES_ADJUDICATION.md` (§8) reports the corrected count as **19** advisory gates, explicitly including `GATE-019` and `GATE-020` (M2 `branching_ratio_absolute_bias`/`relative_bias`) as advisory-tier. Direct verification against `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` shows these two metrics are **MANDATORY** tier specifically for M2 (`GATE-019`, `GATE-020` rows) — the same metric names are `ADVISORY` only for M0 (`GATE-005`, `GATE-006`, where they are `NOT_APPLICABLE_TO_MODEL_DOMAIN` entirely, per the diagnostic audit). Proposal 6's own per-metric-name reasoning did not check the tier per-candidate, and inherited an error the same shape as the earlier `GATE-036` miscount it had just finished correcting.

**Net effect on Proposal 6's substance:** limited. Proposal 6's own §8 "flagged boundary case" already noted `GATE-019`/`GATE-020` have observed values (0.020-0.054) and that "their remediation path is Proposal 3, not Proposal 6" — this is *already correct in direction*, just mislabeled as "advisory" when it is actually "mandatory, protocol-incomplete, governed by Proposal 3." No authorization, threshold, or verdict changes as a result of this correction — Proposal 6 grants zero computation authorization regardless of the exact count, and `GATE-019`/`GATE-020` were never going to be computed under Proposal 6's own scope either way. **The true applicable-and-never-computed advisory count is 17, not 19, and not 21.**

`GATE-031` confirmed correctly excluded from this inventory throughout (`ESTIMAND_MISMATCH`, not `PROTOCOL_NOT_COMPLETED` — verified directly). `GATE-032` confirmed `MANDATORY` tier, correctly excluded. All applicable advisory gates (the 17) use each candidate's *current* (unamended) estimands as recorded, correctly deferred to the *amended* equations once Proposals 1/2/4/5 are implemented (Proposal 6 §15) — no not-applicable gate is counted as not-computed (§13 of doc 06, verified: zero `NOT_APPLICABLE_TO_MODEL_DOMAIN` rows appear inside the "applicable" 17/19 count).

## 10. Retired-Gate Treatment

`GATE-031` treatment verified consistent across doc 07 and cross-references in docs 04/05: `RETIRED_PROSPECTIVELY_FOR_M3_V2` (not `DELETED`/`NEVER_EXISTED`/`HISTORICAL_RESULT_INVALIDATED`/`AUTOMATICALLY_PASSED` — all four prohibited labels confirmed absent from all seven documents via direct search). Original gate row in the frozen spec unchanged (§ Validation below). Replacement mapping (`M3-REPL-031-A..E`) confirmed to reference only quantities already established by Proposals 4/5 — no new, uncalibrated gate concept invented.

## 11. Future Applicability Matrix

Full detail: `MODEL_3B_FUTURE_GATE_APPLICABILITY_MATRIX.csv` (26 rows covering M0/M2/M3 gate families, each with candidate, model equation, parameter space, estimand, null definition, applicability, mandatory/advisory, metric formula, denominator, threshold status, threshold provenance, source proposal, implementation status). Every inapplicable candidate-gate pair explicitly marked `NOT_APPLICABLE_TO_MODEL_DOMAIN` (M0's excitation family; `GATE-031`'s retired family). This is a consistency-check artifact, **not** the final V2 gate specification — no full 14-column production-ready row set is authorized by it.

## 12. Threshold and Prior Decisions

```text
M3 tau (decision threshold):              REQUIRES_SYNTHETIC_CALIBRATION
M3 prior model odds P(M0)/P(M1):          REQUIRES_RESEARCHER_POLICY
Bayes-factor evidence categories (if used): REQUIRES_LITERATURE_PROVENANCE
ROPE epsilon_n (if used):                  REQUIRES_LITERATURE_PROVENANCE
                                            or REQUIRES_RESEARCHER_POLICY
                                            (either, per Proposal 5 SS16 --
                                            not predetermined which)
M2 exact-null implementation (M2-specific): REQUIRES_PREIMPLEMENTATION_DECISION
M2 uncertainty method for n:                REQUIRES_PREIMPLEMENTATION_DECISION
Replication denominator (attempted vs valid): REQUIRES_PREIMPLEMENTATION_DECISION
Candidate-specific resource ceilings:       REQUIRES_PREIMPLEMENTATION_DECISION
```
No numerical value assigned to any of the above by this audit or any of the seven adjudications.

## 13. Test Inventory

Full detail: `MODEL_3B_AMENDMENT_TEST_INVENTORY.csv` (121 rows). Mechanically recounted directly from all seven documents by regex extraction of every `PREFIX-NNN:` occurrence:

```text
M0-HESS-001..010:  10 found, 0 gaps, matches expected 10
M2-EST-001..012:   12 found, 0 gaps, matches expected 12
M2-SCALE-001..015: 15 found, 0 gaps, matches expected 15
M3-NULL-001..020:  20 found, 0 gaps, matches expected 20
M3-DEC-001..028:   28 found, 0 gaps, matches expected 28
M3B-ADV-001..021:  21 found, 0 gaps, matches expected 21
M3-G31-001..015:   15 found, 0 gaps, matches expected 15
TOTAL: 121 (matches expected 121 exactly)
```
All IDs unique across the full inventory (verified: 121 rows, 121 unique `test_id` values). No test outside `MODEL_3B_AMENDMENT_07_M3_GATE031_RETIREMENT_ADJUDICATION.md` references `GATE-031` as active (verified by direct grep). No test assumes implementation already exists (all seven documents' own "recorded but not executed" framing preserved verbatim in the extracted descriptions). No test uses historical data (all seven documents' historical-fit-nonauthorization sections confirm this as a standing constraint). No test conflicts with another amendment (cross-checked candidate-by-candidate; no test family asserts a value another family's test would contradict).

## 14. Implementation Waves

Full detail: `MODEL_3B_AMENDMENT_IMPLEMENTATION_WAVES.md`. Seven waves: (1) versioned specs, (2) M0 correction, (3) M2 correction, (4) M3 correction, (5) advisory-gate implementation (corrected to 17 gates, not 19 — see §9), (6) smoke validation, (7) separate tournament-execution decision. No wave authorized by this audit.

## 15. Unresolved Decisions

```text
1. M3 decision threshold tau -- not selected, requires calibration.
2. M3 prior model odds -- not selected, requires researcher policy.
3. Bayes-factor evidence levels (if used) -- not selected.
4. ROPE epsilon_n (if used) -- not selected.
5. M2's own exact-null representability -- not reviewed (separate from M3's).
6. M2 uncertainty method for n -- not selected (profile/bootstrap/likelihood).
7. Replication denominator (attempted vs valid) -- explicitly pending.
8. Advisory-gate count correction (19 -> 17) -- needs propagation into any
   future WAVE 1 versioned specification; does not require reopening
   Proposal 6's APPROVED_WITH_LIMITATIONS status, since no authorization
   or verdict depended on the exact number.
9. Stale "Proposal 4 not yet adjudicated" phrase in Proposal 2 §13 --
   textual only, substance correct, nonblocking editorial note.
```

## 16. Implementation Nonauthorization

No amendment is implemented by this audit. No source file (`m0_baseline.py`, `m2_mbpp.py`, `m3_bayesian_discrete.py`, `observation_pipeline.py`, `recovery_metrics.py`) is modified.

## 17. Rerun Nonauthorization

No M0/M2/M3 execution of any kind occurs in this audit turn.

## 18. Historical-Fit Nonauthorization

`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` are not read, written, or referenced by any executed code in this audit turn.

## 19. Production Isolation

No backend, frontend, Atlas, Graphify, database, or production configuration file is touched. Confirmed via `git status` scoped to those paths (empty diff).

## 20. Final Status

```text
CONSISTENT_WITH_NONBLOCKING_CLARIFICATIONS
```

**Justification:** the seven decisions coexist without contradiction; dependency ordering is acyclic and complete (§5); mathematical domains agree across all documents (§4); no test, gate, or wave assumes an unauthorized action; every unresolved numerical choice is explicitly visible, not silently decided (§12, §15); implementation remains separately gated at every level (§16-18). **One material but non-authorization-affecting inconsistency was found** (§9: Proposal 6's advisory-gate count is 19 as written, 17 as mechanically verified, due to `GATE-019`/`GATE-020` being mistakenly tiered as advisory when the frozen spec marks them mandatory for M2) and **one cosmetic staleness** (§5: a superseded parenthetical in Proposal 2). Neither blocks the freeze: no proposal's `APPROVED_WITH_LIMITATIONS` status, authorization column, or dependency relationship depends on the exact advisory count, and the corrected number is recorded here and in the implementation-wave plan for propagation into any future WAVE 1 versioned specification — not into the frozen Proposal 6 document itself, which remains historically accurate to what it approved (the *principle*, not a self-sufficient final inventory).
