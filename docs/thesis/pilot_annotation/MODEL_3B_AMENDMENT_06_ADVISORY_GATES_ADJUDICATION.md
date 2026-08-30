# Amendment Adjudication — Proposal 6: Advisory Gates Omitted From the Pilot

> **Decision record only. No advisory-gate computation performed. No source code modified. No V2 gate specification created. No tournament rerun. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **only** `PROPOSAL-06` — the requirement that mathematically-applicable advisory gates omitted from the pilot be computed during a future versioned recovery execution, without automatically becoming mandatory or changing any candidate's current verdict. `PROPOSAL-01` through `PROPOSAL-05` were adjudicated separately and are **not** touched — all five remain `APPROVED_WITH_LIMITATIONS`, `implementation_authorized=NO`, `rerun_authorized=NO`, `historical_fit_authorized=NO`. `PROPOSAL-07` is **not** adjudicated here.

## 2. Authoritative Evidence

```text
Diagnostic-audit commit:    4b94cd689c995765102b4ca4c63e2636334432bb
Authoritative status:       MODEL_3B_PILOT_DIAGNOSTIC_AUDIT_PUSHED_AND_SERVER_SYNCED
Tournament verdict:         NOT_AVAILABLE
Historical-data fitting:    NOT_AUTHORIZED
Proposals 1-5 status:       all APPROVED_WITH_LIMITATIONS (implementation-free)
```

## 3. Original Proposal

Read verbatim from `docs/thesis/pilot_annotation/MODEL_3B_GATE_AMENDMENT_PROPOSAL.md` (as required, not from a terminal summary):

> **Proposal 6 — advisory gates never computed by this pilot (GATE-038-042/050/053-057/059/061-063): scope gap, not a gate defect**
>
> **Observed issue**: 21 of the 42 pilot-applicable gates (all ADVISORY tier, plus GATE-032/031 discussed separately below) have no observed value at all — the pilot's run scripts never implemented `boundary_solution_rate` aggregation (M0/M3), `held_out_predictive_score`, `source_removal_stability`, `episode_removal_stability`, or `calibration`. **Correction (2026-08-30):** `GATE-036` (`false_negative_excitation_rate`, M0) is excluded from this list — it was reclassified `NOT_INTERPRETABLE`/`NOT_APPLICABLE_TO_MODEL_DOMAIN`...
>
> **Proposed amendment**: none to the gates themselves... Proposed **scope decision**... Recommend **after**.
> **Researcher decision required**: NO immediate decision — noted for future scoping only.

**Confirmed: the proposal concerns 21 (as titled) advisory gates not computed during the pilot** — subject matches the researcher's framing exactly. Ledger row `PROPOSAL-06` (`MODEL_3B_AMENDMENT_DECISION_LEDGER.csv`) confirms the same topic: `"21 advisory gates never computed by this pilot... -- scope/sequencing decision only, not a gate defect"`.

**Verification finding (§8 below): the count of 21 does not survive a rigorous tier-by-tier recount against the frozen gate specification's own `mandatory_advisory_status` column — the true count is 19.** This does not change the proposal's subject or the decision content (both concern the same population of never-computed diagnostic gates and the same treatment principle); it corrects an inherited counting imprecision, exactly as `GATE-036`'s classification was corrected in Proposal 4's freeze. Per §1's own governing rule, this is reported, not silently forced to match 21.

## 4. Researcher Decision

```text
PROPOSAL-06: APPROVED_WITH_LIMITATIONS

Decision: all mathematically applicable advisory gates omitted from the
pilot must be computed during the future versioned recovery execution.

Current omitted advisory gates remain: NOT_COMPUTED
  -- NOT NOT_APPLICABLE_TO_MODEL_DOMAIN (that classification is reserved
     for gates mathematically undefined for a candidate's parameter space,
     per Proposal 4's precedent -- these 19 gates ARE mathematically
     defined for their respective candidates, simply not yet computed by
     the pilot's run scripts)

Must not be interpreted as: PASS / FAIL / VALID_GATE_VALID_FAILURE /
                              MODEL_VALIDATED / MODEL_REJECTED

Implementation:   NOT_AUTHORIZED
Rerun:             NOT_AUTHORIZED
Historical fit:     NOT_AUTHORIZED
```

## 5. Advisory versus Mandatory Gates

```text
MANDATORY_GATE:  directly contributes to candidate go/no-go
ADVISORY_GATE:   provides diagnostic evidence but does not independently
                 determine go/no-go
```

Advisory gates do **not** automatically change a candidate's primary PASS/FAIL verdict unless a future versioned gate specification explicitly promotes a specific gate to mandatory status **before** execution. **However**, if an advisory result reveals numerical failure, an invalid confidence interval, a severe calibration defect, data loss, non-identifiability, or a protocol violation, the future execution must **stop for researcher review** even though the gate is formally advisory — a severe advisory finding must never be silently ignored.

## 6. Mathematical Applicability Rule

```text
A(g,m) = 1  if q_g(theta) is defined for theta in Theta_m
A(g,m) = 0  otherwise

If A(g,m) = 0: classify NOT_APPLICABLE_TO_MODEL_DOMAIN
             (never NOT_COMPUTED, PROTOCOL_NOT_COMPLETED, or FAIL)
```

This is the same rule adopted in the diagnostic audit's Methodological Lesson (§17) and applied in Proposal 4 — restated here explicitly so Proposal 6's inventory cannot recreate the M0 excitation-gate category error the audit already corrected once (`GATE-002/003/005/006/036`).

## 7. Candidate Parameter Spaces

```text
Theta_M0 (current, unamended):
  gamma (count-model regression parameters); phi (NB dispersion, where used);
  exposure/predictive quantities defined by the count model.
  Does NOT include: alpha, beta, branching ratio n, excitation-existence
  state, excitation detection power.

Theta_M2 (under the Proposal 2/3 approved future direction):
  baseline parameters; n (primary estimand); beta (secondary/diagnostic);
  predictive interval-count quantities.

Theta_M3 (under the Proposal 4/5 approved future design):
  exact null model M0: n=0; excitation model M1: 0<n<1; baseline and
  observation-model parameters; posterior model-existence probability P(M1|Y).
```

No candidate's advisory gate is applied mechanically to another candidate — each gate's applicability is assessed per-candidate against that candidate's own parameter space.

## 8. Twenty-One (Corrected: Nineteen) -Gate Inventory

**Reconciliation, derived mechanically from `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv` cross-referenced against `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`'s own `mandatory_advisory_status` column (not asserted):**

```text
Total PROTOCOL_NOT_COMPLETED gates (post-GATE-036-correction): 24
  MANDATORY-tier among these (NOT advisory, excluded from this inventory):
    GATE-015 M2 invalid_estimate_rate
    GATE-016 M2 false_positive_excitation_rate
    GATE-029 M3 invalid_estimate_rate
    GATE-032 M3 normalized_absolute_bias_baseline_param
    GATE-051 M2 convergence_rate
    (5 gates -- these are mandatory recovery gates undermined by M2's
    150/1,000 protocol shortfall, already governed by Proposal 3, not a
    "never computed by design" scope gap)
  ADVISORY-tier among these: 24 - 5 = 19
```

`GATE-031` (M3, `absolute_relative_bias_excitation_params`) is **not** in this inventory at all — its classification is `ESTIMAND_MISMATCH`, already governed by Proposal 2 (M2's estimand narrowing) / Proposal 4-5 (M3's exact-null and decision-rule redesign), not "never computed." The original proposal's own parenthetical ("plus GATE-032/031 discussed separately below") already signaled these two do not belong to the core inventory — this reconciliation makes that separation exact rather than approximate.

**The 19-gate advisory inventory** (metric-level detail below, since formula/threshold/provenance are identical across candidates for the same metric — full per-gate table follows):

| Metric | M0 | M2 | M3 | Applicability |
|---|---|---|---|---|
| `boundary_solution_rate` | GATE-038 | GATE-052 | GATE-059 | APPLICABLE (all three) |
| `held_out_predictive_score` | GATE-039 | GATE-053 | GATE-060 | APPLICABLE (all three) |
| `source_removal_stability` | GATE-040 | GATE-054 | GATE-061 | APPLICABLE (all three) |
| `episode_removal_stability` | GATE-041 | GATE-055 | GATE-062 | APPLICABLE (all three) |
| `calibration` | GATE-042 | GATE-056 | GATE-063 | APPLICABLE (all three) |
| `false_negative_excitation_rate` | — (GATE-036, `NOT_APPLICABLE_TO_MODEL_DOMAIN`, excluded per Proposal 4/audit) | GATE-050 | GATE-057 | APPLICABLE for M2/M3 only |
| `branching_ratio_absolute_bias` | — (no branching ratio in Theta_M0) | GATE-019 | — (not PROTOCOL_NOT_COMPLETED for M3; GATE-033, already `VALID_GATE_VALID_FAILURE`) | APPLICABLE for M2 only, in this inventory |
| `branching_ratio_relative_bias` | — | GATE-020 | — (GATE-034, already `VALID_GATE_VALID_FAILURE`) | APPLICABLE for M2 only, in this inventory |

**Count check:** 5 metrics × 3 candidates = 15, plus `false_negative_excitation_rate` × 2 applicable candidates (M2, M3) = 2, plus `branching_ratio_absolute/relative_bias` × 1 applicable-and-still-`PROTOCOL_NOT_COMPLETED` candidate (M2 only, since M3's equivalents `GATE-033/034` already carry an observed value and a `VALID_GATE_VALID_FAILURE` classification, not `PROTOCOL_NOT_COMPLETED`) = 2. **Total: 15+2+2 = 19.**

**Flagged boundary case, not resolved here:** `GATE-019`/`GATE-020` (M2 branching-ratio bias) already carry **observed values** (0.020–0.054 absolute, per Proposals 2/3) at the 150/cell pilot scale — they are not "no observed value at all" in the same sense as the other 17 gates, which have genuinely never been computed by any pilot script regardless of scale. `GATE-019`/`GATE-020`'s path to final adjudication runs through **Proposal 3**'s full-scale requirement, not through Proposal 6's "implement the missing computation" scope. They are included in this inventory for completeness (they are advisory-tier and currently `PROTOCOL_NOT_COMPLETED`) but their remediation is Proposal 3's, not Proposal 6's.

## 9. Metric Formulas

Recorded per metric (identical across candidates where applicable, confirmed from `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`, not reinvented):

```text
RelBias(theta_hat)  = [mean(theta_hat) - theta_true] / theta_true
                       (NOT used when theta_true = 0)
AbsBias(theta_hat)   = mean(theta_hat) - theta_true
                       (used instead, when theta_true = 0)
RMSE                 = sqrt( (1/R) * sum_{r=1}^R (theta_hat_r - theta_true)^2 )
Coverage_hat          = (1/R) * sum_{r=1}^R I(theta_true in [L_r, U_r])
FPR_hat               = (1/R0) * sum_{r=1}^{R0} I(excitation selected | exact null)
FNR_hat               = (1/R1) * sum_{r=1}^{R1} I(excitation not selected | true positive)
MCSE(p_hat)            = sqrt( p_hat*(1-p_hat) / R_effective )
ConvergenceRate        = converged replications / attempted replications
BoundaryRate            = boundary-solution replications / attempted replications
```

Per-gate thresholds (confirmed from `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`, applies uniformly across M0/M2/M3 unless noted):

```text
boundary_solution_rate:          <= 0.10, lower_is_better, RESEARCHER_POLICY
held_out_predictive_score:       must exceed M0's own held-out score at
                                  matched settings, relative_to_M0,
                                  COMPARATIVE_BENCHMARK
source_removal_stability:        parameter shift <= 0.20 (relative) under
                                  leave-one-source-out refit, RESEARCHER_POLICY
episode_removal_stability:       parameter shift <= 0.20 (relative) under
                                  leave-one-episode-out refit, RESEARCHER_POLICY
calibration:                     PIT/reliability curve within +/-0.05 of
                                  nominal across deciles, target_band,
                                  SIMULATION_DESIGN_REQUIREMENT
false_negative_excitation_rate:  <= 0.10, lower_is_better, RESEARCHER_POLICY
branching_ratio_absolute_bias:   <= 0.05, lower_is_better, RESEARCHER_POLICY
branching_ratio_relative_bias:   <= 0.10, lower_is_better, RESEARCHER_POLICY
```

## 10. Denominator Rules

Metric denominators must be **explicit** — attempted replications vs. converged replications must not be silently interchanged (consistent with Proposal 3 §8's `REPLICATION_DENOMINATOR_REQUIRES_EXPLICIT_PREEXECUTION_DECISION`). A future execution report must record the denominator actually used for each rate/proportion metric, alongside its MCSE.

## 11. Threshold Provenance

Every advisory threshold uses exactly one of: `LITERATURE_DERIVED`, `MATHEMATICAL_REQUIREMENT`, `SIMULATION_DESIGN_REQUIREMENT`, `COMPARATIVE_BENCHMARK`, `RESEARCHER_POLICY`, `NO_THRESHOLD_DIAGNOSTIC_ONLY` — confirmed from the frozen gate spec (§9 above), all already assigned, none `UNEXPLAINED`/`IMPLICIT`/`ARBITRARY`. `held_out_predictive_score` is a `COMPARATIVE_BENCHMARK` (relative to M0), not an absolute cutoff; if any future gate has no defensible cutoff, it is retained as a diagnostic quantity without inventing a threshold, not forced into a PASS/FAIL shape.

## 12. Missing-Metric Handling

If an applicable advisory metric cannot be computed in a future run, classify `APPLICABLE_METRIC_NOT_COMPUTED` and report: missing input; implementation gap; affected candidate; consequence; whether the final candidate verdict remains blocked. A missing value must **not** be replaced with `0`, `false`, `PASS`, unexplained `NaN`, or an empty string.

## 13. Not-Applicable Handling

If a metric is outside a model's domain, classify `NOT_APPLICABLE_TO_MODEL_DOMAIN` and record the mathematical reason (e.g., `M0`'s excitation false-negative rate is not applicable because `M0` has no excitation-positive state or excitation decision rule — `GATE-036`, already so classified). Not-applicable gates are **not** counted as omitted computations — they are excluded from the "must be computed" set entirely, not merely deferred.

## 14. Severe Advisory Findings

Per §5: a severe advisory finding (numerical failure, invalid CI, severe calibration defect, data loss, non-identifiability, protocol violation) halts future execution for researcher review, regardless of the gate's formal advisory/mandatory status. This is not silently waivable by Proposal 6's own "advisory does not determine go/no-go" principle — the two rules operate at different levels (routine advisory results don't drive verdicts; severe advisory anomalies still demand a stop).

## 15. Relationship to Proposals 1–5

Proposal 6 preserves: `PROPOSAL-01` (M0 full-Hessian direction), `PROPOSAL-02` (M2 primary estimand `n=alpha/beta`), `PROPOSAL-03` (M2 full 1,000-replications-per-cell requirement), `PROPOSAL-04` (M3 exact-null representation), `PROPOSAL-05` (M3 calibrated posterior excitation-model probability) — none altered. Once those amendments are implemented, advisory gates must use the **amended** candidate equations and applicability domains (e.g., M2's advisory gates would be assessed against the amended `n`-primary parameterization, not the original raw `alpha/beta`). **Proposal 6 does not authorize implementation of Proposals 1–5.**

## 16. Future Versioning

The applicable advisory-gate inventory enters a new versioned gate specification. `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` (original, frozen 70-row file) is **not** overwritten. Future candidate name (naming direction only, not created this turn): `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`.

## 17. Required Future Tests (recorded, NOT executed this turn)

```text
M3B-ADV-001: All advisory gate IDs in the corrected 19-gate inventory are
             inventoried exactly once (superseding the originally-stated 21).
M3B-ADV-002: Every gate declares its candidate.
M3B-ADV-003: Every gate declares its applicability domain.
M3B-ADV-004: Every applicable gate declares its estimand.
M3B-ADV-005: Every applicable gate declares its metric formula.
M3B-ADV-006: Every denominator is explicit.
M3B-ADV-007: Relative bias is not used when the true value is zero.
M3B-ADV-008: Not-applicable gates do not affect candidate verdicts.
M3B-ADV-009: Applicable but missing metrics block final completeness review.
M3B-ADV-010: Mandatory and advisory gates remain distinct.
M3B-ADV-011: Severe advisory failures trigger researcher review.
M3B-ADV-012: Threshold provenance is present for every threshold.
M3B-ADV-013: Diagnostic-only gates do not receive invented thresholds.
M3B-ADV-014: Raw replication rows reconcile with advisory summaries.
M3B-ADV-015: Failed optimization runs remain in denominators where prescribed.
M3B-ADV-016: MCSE is computed for rate and proportion metrics.
M3B-ADV-017: M0 excitation gates are rejected as not applicable.
M3B-ADV-018: M2 metrics use n as the primary estimand.
M3B-ADV-019: M3 decision metrics use the exact-null model comparison.
M3B-ADV-020: No historical data enter advisory-gate computation.
M3B-ADV-021: Repeated calculation from identical raw output is deterministic.
```

## 18. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```
No advisory-gate computation is performed. No `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv` is created.

## 19. Rerun Nonauthorization

```text
RERUN: NOT_AUTHORIZED
```
No tournament execution of any kind occurs.

## 20. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```
`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` are not read, written, or referenced by any executed code in this adjudication turn.

## 21. Decision Summary

```text
PROPOSAL-06: APPROVED_WITH_LIMITATIONS
Corrected inventory count:    19 (not 21) genuinely-advisory-tier,
                               genuinely-never-computed gates -- GATE-031
                               (ESTIMAND_MISMATCH) and GATE-032 (MANDATORY)
                               excluded per rigorous tier recount; GATE-019/
                               020 included but their remediation path is
                               Proposal 3, not Proposal 6
Applicable count:              19 (all mathematically defined for their
                                candidate's current or amended parameter space)
Not-applicable count:          0 in this inventory (GATE-036 already excluded
                                upstream by Proposal 4/audit)
Current status:                NOT_COMPUTED (missing diagnostic evidence)
Verdict impact:                NONE automatic -- advisory, not mandatory,
                                unless a future versioned spec promotes a gate
Severe-finding override:       still applies (advisory != ignorable)
Implementation:                 NOT_AUTHORIZED
Rerun:                          NOT_AUTHORIZED
Historical fit:                 NOT_AUTHORIZED
```

## Final Status (this document)

```text
MODEL_3B_AMENDMENT_06_ADVISORY_GATES_ADJUDICATED
```
