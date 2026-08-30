# Amendment Adjudication — Proposal 7: Retirement of GATE-031 for Future Amended M3

> **Decision record only. No amendment implemented. No V2 gate specification created. No M0/M2/M3 rerun. No historical data fitted. Nothing staged, committed, pushed, or deployed. This is the seventh and final proposal — all seven proposals are ADJUDICATED after this document, but zero are implemented, rerun-authorized, or historical-fit-authorized.**

---

## 1. Scope

This document adjudicates **only** `PROPOSAL-07` — prospective retirement of `GATE-031` for future amended M3 recovery specifications, in favor of the branching-ratio and exact-null/decision-rule gate families approved under Proposals 4 and 5. `PROPOSAL-01` through `PROPOSAL-06` were adjudicated separately and are **not** touched — all six remain `APPROVED_WITH_LIMITATIONS`, `implementation_authorized=NO`, `rerun_authorized=NO`, `historical_fit_authorized=NO`.

## 2. Authoritative Evidence

```text
Diagnostic-audit commit:    4b94cd689c995765102b4ca4c63e2636334432bb
Authoritative status:       MODEL_3B_PILOT_DIAGNOSTIC_AUDIT_PUSHED_AND_SERVER_SYNCED
Tournament verdict:         NOT_AVAILABLE
Historical-data fitting:    NOT_AUTHORIZED
Proposals 1-6 status:       all APPROVED_WITH_LIMITATIONS (implementation-free)
```

## 3. Exact GATE-031 Definition

Read directly from `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` (frozen, unmodified) and `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv` (pilot result), not asserted:

```text
Candidate:              M3
Mandatory/advisory:      MANDATORY
Metric:                  absolute_relative_bias_excitation_params
Parameter/estimand:      bias of a distinct "alpha-like" excitation-
                         amplitude parameter, per the gate's own notes:
                         "n (branching ratio, per Design doc sec5
                         parameterization) and beta" -- i.e. the gate was
                         authored assuming an alpha/beta-shaped
                         parameterization
Threshold:                <= 0.10
Direction:                lower_is_better
Threshold provenance:     RESEARCHER_POLICY (no universal literature cutoff
                          verified; explicit preregistered project decision)
Original failure meaning: candidate excluded from tournament (fails its own
                          preregistered recovery test; ineligible for
                          real-data-fitting consideration)
Pilot observed value:     not separately computed by run_recovery_m3.py --
                          "M3 parameterizes directly in n, beta -- no
                          separate alpha" (source-verified)
Pilot classification:     ESTIMAND_MISMATCH
                          (implementation_valid=TRUE, estimand_valid=FALSE)
Reason Proposal 7 recommends retirement: the gate assumes a separate
                          alpha-like amplitude parameter distinct from n;
                          M3's own parameterization (Design doc sec5
                          Option B/C) never separates them -- this is a
                          gate/model parameterization mismatch identified
                          before the gate was ever meaningfully evaluable
                          for M3, per the pilot's own notes.
```

**Confirmed: Proposal 7 is specifically and exactly about prospective retirement of `GATE-031` for M3's own parameterization** — verified against the verbatim text in `MODEL_3B_GATE_AMENDMENT_PROPOSAL.md` ("Proposal 7 — M3 excitation-parameter gate (GATE-031): retire for M3's own parameterization... Do not retire GATE-031 for M0/M1/M2/M4, which do have a distinct alpha") and the ledger's `PROPOSAL-07` row (`proposal_topic`: "Retire GATE-031... for M3 only... makes the gate inapplicable as worded"). No material difference found; adjudication proceeds.

## 4. Original Mathematical Domain

```text
Theta_M3_old (as executed in the pilot):
  theta0, theta1 (baseline); n (branching ratio, direct); beta (decay)
  No separate alpha-like amplitude parameter exists or ever existed.
```

`q_031` (bias of a distinct amplitude parameter, per the gate's own authored intent) was **never defined** on `Theta_M3_old` — this is not a consequence of Proposals 4/5's amendments; it predates them, confirmed by the pilot's own `estimand_valid=FALSE` finding before any amendment was adjudicated.

## 5. Amended M3 Mathematical Domain

```text
Theta_M3_new (per Proposals 4 and 5):
  exact-null model M0: n = 0
  excitation model M1: 0 < n < 1
  baseline and observation-model parameters
  excitation magnitude parameters conditional on M1
  model-existence quantity P(M1|Y)
```

`Theta_M3_new` **also** contains no separate alpha-like amplitude parameter — the amendment reparameterizes around `n` and the model-existence indicator, it does not introduce an `alpha`. `q_031` remains undefined on `Theta_M3_new` for the same structural reason it was undefined on `Theta_M3_old`.

## 6. Applicability Review

```text
Classification: C. PARAMETERIZATION_SPECIFIC_GATE_OBSOLETE

(secondary, reinforcing factor: D. DUPLICATED_BY_EXACT_NULL_DECISION_GATES
 -- the underlying scientific question GATE-031 was meant to answer, "how
 much excitation mass is recoverable," is already covered without an
 alpha-shaped parameterization by GATE-033/034 (branching-ratio gates,
 already reported by M3 directly) and, prospectively, by Proposal 5's
 requirement (Decision Rule Adjudication SS17) that magnitude estimation
 be reported separately as E[n|Y,M1] and a credible interval for n
 conditional on M1)
```

**Reasoning:** `q_031` is not "removed by amendment" (classification A) — it was never present in either the old or new parameter space, so there is nothing for the amendment to have removed. It is not merely "retained as secondary diagnostic" (B) — there is no quantity to retain, since `alpha` itself does not exist for M3 in any parameterization. It is precisely a **gate authored for a parameterization M3 never used** (C), and its scientific purpose is **already served by other, already-approved gate families** (D) — `GATE-033/034` directly, and the magnitude-conditional-on-`M1` reporting Proposal 5 already requires. Classification is **C** (primary) with **D** as the supporting rationale for why retirement, rather than replacement invention, is the correct response.

Per the governing rule: **classification C qualifies for approval** (only E or F would block it). Proceeding to adjudication.

## 7. Researcher Decision

```text
PROPOSAL-07: APPROVED_WITH_LIMITATIONS

Candidate:              M3
Decision:                RETIRE GATE-031 FOR FUTURE AMENDED M3 RUNS ONLY
Original gate:            PRESERVED AS HISTORICAL PILOT EVIDENCE
Replacement:              M3 exact-null model-comparison and calibrated
                          decision-rule gates (SS12 below)
Implementation:           NOT_AUTHORIZED
Rerun:                    NOT_AUTHORIZED
Historical fit:           NOT_AUTHORIZED
```

## 8. Prospective Retirement

```text
Selected action: RETIRE_GATE_031_FOR_FUTURE_AMENDED_M3_ONLY

Scope:
  - applies to: a future, prospective, versioned amended M3 recovery
    specification only
  - does NOT apply to: M0 (never had this gate applicable in the first
    place -- different reason, different candidate)
  - does NOT apply to: M2 (M2's own gates are separately governed by
    Proposals 2/3)
  - does NOT apply to: the frozen original pilot record
  - does NOT constitute: historical evidence deletion
```

`RETIRED_PROSPECTIVELY` — **not** `DELETED`, **not** `NEVER_EXISTED`, **not** `HISTORICAL_RESULT_INVALIDATED`, **not** `AUTOMATICALLY_PASSED`. The gate's existence and its `ESTIMAND_MISMATCH` classification in the pilot record are permanent historical facts, unaffected by this retirement decision applying only to future work.

## 9. Historical Preservation

**Not modified by this document:** the original 70-row gate specification; `GATE-031`'s original row within it; original M3 raw results; the original 200/200 false-positive result (governed by Proposals 4/5, unrelated to `GATE-031` specifically but part of the same preserved pilot record); the diagnostic-audit classifications; Proposal 1 through Proposal 6; current M3 source (`m3_bayesian_discrete.py`) — all confirmed byte-unchanged (§ Validation below). The original gate remains authoritative for documenting **what the pilot actually tested** — a mismatched gate applied to a model that never had the assumed parameter, correctly caught and classified `ESTIMAND_MISMATCH` before this adjudication, not retroactively excused.

## 10. Relationship to Proposal 4

Proposal 4 approved `EXACT_NULL_N_EQUALS_ZERO_MUST_BE_IN_MODEL_SUPPORT`. `GATE-031`'s retirement is consistent with, but not identical to, this requirement — Proposal 4 concerns whether `n=0` is representable; `GATE-031`'s obsolescence concerns whether a *separate amplitude parameter* (never `n` itself) is representable. Both point to the same underlying fact: M3's parameterization does not, and under the amendment still does not, contain an `alpha`-shaped quantity.

## 11. Relationship to Proposal 5

Proposal 5 approved `CALIBRATED_POSTERIOR_EXCITATION_MODEL_PROBABILITY` (`P(M1|Y)`) as the primary decision quantity, with magnitude estimation (`E[n|Y,M1]`, credible interval for `n` given `M1`) reported **separately** from existence (Decision Rule Adjudication §17). This magnitude-conditional-on-`M1` requirement is one of the natural replacement locations for the scientific question `GATE-031` was originally meant to answer (§6, §12).

Future M3 gate families must therefore evaluate separately:
```text
1. exact-null support (Proposal 4)
2. model-existence calibration (Proposal 5)
3. false-positive rate under exact null (Proposal 5)
4. false-negative rate / power under positive excitation (Proposal 5)
5. posterior model-probability calibration (Proposal 5)
6. excitation magnitude conditional on M1 (Proposal 5 SS17; replaces
   GATE-031's original intent)
7. baseline and observation-process confounding (Proposal 5 SS19)
8. convergence and numerical stability
```

`GATE-031` may **not** remain a mandatory primary gate merely because it existed under the old M3 parameterization — its scientific content is redistributed across this list, not silently dropped.

## 12. Replacement Gate Mapping

`GATE-031` is **not** retired without an explicit replacement mapping (required by the governing instruction; redundant new gates are not created merely to inflate test count):

```text
GATE-031 (original: bias of a nonexistent alpha-like amplitude parameter)
  maps to:

M3-REPL-031-A: Exact-null representability
  -- covers whether the model can even express "no excitation," a
     precondition GATE-031 implicitly assumed by testing amplitude bias
     at all (Proposal 4).

M3-REPL-031-B: Posterior excitation-model probability calibration
  -- covers whether the existence decision itself is well-calibrated,
     which GATE-031's amplitude-bias framing never addressed at all
     (Proposal 5 SS7-9).

M3-REPL-031-C: False-positive rate under exact null
  -- directly replaces the diagnostic value GATE-031 could never provide
     for M3 (since it was never computable), using the calibrated
     P(M1|Y) rule instead of a raw amplitude bias (Proposal 5 SS11).

M3-REPL-031-D: False-negative rate / detection power under positive
                excitation
  -- the complementary diagnostic to C, again not previously available
     under GATE-031's framing (Proposal 5 SS12).

M3-REPL-031-E: Magnitude recovery for n conditional on M1
  -- the direct successor to GATE-031's original "how much excitation"
     question, already partially served today by GATE-033/034 and
     formalized further by Proposal 5's E[n|Y,M1] reporting requirement
     (Proposal 5 SS17).
```

Only these five families are used — they match `GATE-031`'s exact original purpose (amplitude/magnitude recovery diagnostics for M3's excitation) as redistributed across the exact-null/decision-rule design, not an invented expansion.

## 13. Versioning Requirement

A future gate specification must be created as a **new** file — the frozen original `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` must **not** be overwritten. Suggested name (naming direction only, not created this turn): `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`. The future file must include at least: `gate_id`, `candidate`, `model_equation`, `parameter_space`, `estimand`, `null_definition`, `applicability`, `mandatory_or_advisory`, `metric_formula`, `denominator`, `threshold`, `threshold_provenance`, `failure_meaning`, `source_amendment`, `version_status`. The future amended specification must state `GATE-031: RETIRED_FROM_M3_V2` and reference Proposal 4, Proposal 5, Proposal 7, and the five replacement gate IDs (§12). **This adjudication does not authorize creation of that file.**

## 14. Retirement Safeguards

```text
1.  Retirement applies only prospectively.
2.  Retirement does not change the pilot's recorded result.
3.  Retirement does not produce automatic PASS.
4.  Retirement does not reduce the need for exact-null calibration.
5.  Retirement does not waive M3 false-positive and false-negative testing.
6.  Retirement does not authorize a threshold.
7.  Retirement does not select prior model odds.
8.  Retirement does not select a Bayes-factor cutoff.
9.  Retirement does not select a ROPE.
10. Retirement does not authorize historical fitting.
11. Retirement does not affect M0 or M2.
12. Replacement gates must be frozen before amended M3 execution.
```

## 15. Required Future Tests (recorded, NOT executed this turn)

```text
M3-G31-001: Original GATE-031 remains present and unchanged in the
            frozen specification.
M3-G31-002: The amended specification marks GATE-031 retired for M3 V2 only.
M3-G31-003: Retirement has an explicit mathematical rationale.
M3-G31-004: Retirement references Proposals 4, 5, and 7.
M3-G31-005: Replacement gate IDs are present.
M3-G31-006: Replacement gates collectively cover the original
            scientific purpose.
M3-G31-007: No replacement gate uses the invalid lower-bound > 0 rule.
M3-G31-008: Exact-null false-positive calibration remains mandatory.
M3-G31-009: Positive-excitation detection remains evaluated.
M3-G31-010: Conditional magnitude recovery remains separate from
            excitation existence.
M3-G31-011: Retirement does not affect M0 applicability.
M3-G31-012: Retirement does not alter M2 estimands.
M3-G31-013: The original pilot result remains reproducible.
M3-G31-014: No historical data enter replacement-gate calibration.
M3-G31-015: No amended M3 run begins before replacement gates are frozen.
```

## 16. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```
No `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv` is created. No replacement gate is implemented.

## 17. Rerun Nonauthorization

```text
RERUN: NOT_AUTHORIZED
```
No M0/M2/M3 execution of any kind occurs.

## 18. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```
`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` are not read, written, or referenced by any executed code in this adjudication turn.

## 19. Final Amendment-Milestone Status

```text
7 / 7 proposals ADJUDICATED
0 IMPLEMENTED
0 RERUN AUTHORIZED
0 HISTORICAL FIT AUTHORIZED
```

All seven proposals are now design decisions, not implementations. Per the researcher's own stated next step: the next action is **not** code correction — it is a single consistency audit across all seven decisions, followed by a local freeze of the ledger and all seven adjudication documents into one milestone. Neither the consistency audit nor the freeze is performed by this document.

## 20. Decision Summary

```text
PROPOSAL-07: APPROVED_WITH_LIMITATIONS
Applicability classification:   C (PARAMETERIZATION_SPECIFIC_GATE_OBSOLETE),
                                 reinforced by D (DUPLICATED_BY_EXACT_NULL_
                                 DECISION_GATES)
Scope:                          future amended M3 only; not M0, not M2,
                                 not the frozen pilot
Historical status:               PRESERVED_IN_ORIGINAL_GATE_SPECIFICATION
Original pilot result:           PRESERVED
Replacement:                     REPLACED_BY_VERSIONED_EXACT_NULL_AND_
                                 CALIBRATED_DECISION_RULE_GATES
                                 (M3-REPL-031-A through E, SS12)
Implementation:                   NOT_AUTHORIZED
Rerun:                            NOT_AUTHORIZED
Historical fit:                   NOT_AUTHORIZED
```

## Final Status (this document)

```text
MODEL_3B_AMENDMENT_07_GATE031_RETIREMENT_ADJUDICATED
```
