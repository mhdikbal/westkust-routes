# HAWKES BASELINE V2-A — H-05 FINAL RESEARCHER DECISION

Status: **Checkpoint 1 APPROVED IN SUBSTANCE**, subject to two completed
pre-staging corrections: F-SLR closure to `F_SLR=1` (Section "V2-A
completion and V2-B readiness" below) and the governance-amendment status
wording in `HAWKES_BASELINE_V2A_H05_GOVERNANCE_AMENDMENT_PROPOSAL.md`
(prospective, unadopted, non-retrospective). Both corrections are applied
in this frozen version.

## Decision

```
H-05 = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
```

**Not PASS. Not FAIL.** Per the governing instruction's operational gate
(`G_H05^operational = 1[G_H05^semantic=1 ∧ Σ A_o^oper=1]`), evaluated
mechanically this operation:

```
G_H05^semantic  = 0   (8 of 10 semantic components ambiguous/absent/hindsight-only;
                        see HAWKES_BASELINE_V2A_H05_SEMANTIC_CONTRACT.csv)
Σ A_o^oper      = 0   (all 8 candidate operationalizations O1-O8 inadmissible;
                        see HAWKES_BASELINE_V2A_H05_OPERATIONALIZATION_CANDIDATES.csv)
G_H05^operational = 0
```

Both independent tests fail. This is not a borderline call.

## Three reasons, preserved

```
H05_REASON_1 = AUTHORITATIVE_RECOVERY_ACCURACY_CRITERION_NOT_OPERATIONALIZED
H05_REASON_2 = RESIDUAL_VALIDATION_COMPLETED
H05_REASON_3 = D2_PRESPECIFICATION_PROVENANCE_NOT_RECOVERED
```

Reason 2 remains a completed condition (R1/R2 both terminal), not a blocker.
Reason 1 is the primary, and now more thoroughly evidenced, semantic
blocker. Reason 3 continues to limit the evidence domain (D2 excluded).

## What this operation newly established, beyond the prior operation's finding

The prior operation (H-05 operationalization decision, same baseline
lineage) already found the metric ambiguous among "RB/RMSE/coverage." This
operation traced the *actual historical verdict number* (Phase D's "15.6–
19.2%") to its source and found it is **not** any of RB, RMSE, or coverage —
it is the AIC/BIC correct-model-selection rate, a fourth, structurally
different metric that answers "did model selection pick the right model,"
not "how accurate is the parameter estimate." The same authoritative row
(`HAWKES_BASELINE_V2_G7_GATE_MATRIX.csv`) names one metric family in its
`metric` column and justifies its FAIL verdict with a number from an
entirely different, unnamed metric family — a genuine internal
contradiction, not merely an unspecified choice among compatible options.
That metric (AIC-selection accuracy) is, independently, inapplicable to
V2-A's eligible recovery arms (D7, D8, D9-correct, D10) without new
computation this operation is prohibited from performing.

## Candidate operationalizations — why each fails, in one line

| id | one-line reason for inadmissibility |
|---|---|
| O1 replication-level joint recovery | no parameter tolerance bands exist anywhere; explicitly undefinable per the governing instruction's own text |
| O2 interval coverage | no source ties 0.80 to coverage probability; selecting it now would be the explicitly prohibited "choosing coverage because it exceeds 0.80" |
| O3 arm pass-proportion | circular — needs O1 or O2 to define "pass" first |
| O4 cell pass-proportion | same circularity as O3, one level finer |
| O5 optimizer/CI success | trivially 100% everywhere; explicitly prohibited pattern named verbatim in the governing instruction |
| O6 composite score | requires inventing weights; explicitly prohibited pattern |
| O7 original Phase D AIC-selection accuracy | the one metric with genuine historical traceability, but never computed for V2-A's eligible arms, and Phase D itself is permanently excluded as an H-05 evidence source |
| O8 other | exhaustive source search found no ninth candidate with any distinct authoritative anchor |

## Governance amendment

One narrow prospective amendment proposed:
`HAWKES_BASELINE_V2A_H05_GOVERNANCE_AMENDMENT_PROPOSAL.md`. It retires the
single-scalar `≥0.80` test in favor of a non-composited coverage/relative-
bias report, and is explicitly marked
`AMENDMENT_APPLIES_PROSPECTIVELY_ONLY` — it is not applied to the frozen
V2-A results in this operation, and doing so later would itself carry post
hoc risk given this proposal was drafted with full sight of the existing
numbers.

## V2-A completion and V2-B readiness (mechanical consequences)

```
C_H05 = 0
G_V2A_complete = 0   (blocked solely by C_H05=0; every other constituent
                       gate — C_R1, C_R2, C_provenance, G_causal=0,
                       G_ontology=0, historical-fit=0, Phase-D-rerun=0 —
                       already holds)

G_V2B_preauth = 1[H05=PASS AND P_analysis=1 AND F_SLR=1 AND O_obs=1
                   AND E_epi=1 AND I_guard=1 AND B_historical=1 AND B_PhaseD=1]
             = 0 * 1 * 1 * 1 * 1 * 1 * 1 * 1 = 0

PRIMARY V2-B BLOCKER = H05_NOT_EVALUABLE (the sole false term in the
                       conjunction — every other factor already holds,
                       including F_SLR=1: F-08 is DIRECT_PRIMARY_SUPPORT_
                       ESTABLISHED via Brown, Barbieri, Ventura, Kass &
                       Frank (2002), Neural Computation 14(2):325-346,
                       Sec.2.1, pp.329-331, eq.2.8/2.16/2.17 — the same
                       citation already embedded in v2a_validation_engine.py's
                       time_rescaling_residuals() docstring. Ogata (1988)
                       remains BIBLIOGRAPHIC_IDENTITY_CONFIRMED /
                       EXACT_F08_LOCATOR_NOT_INDEPENDENTLY_VERIFIED, but
                       that residual gap no longer fails F-08 or F_SLR)
V2B_execution_count = 0
V2B_authorization_created = 0
```

## Classification of the three H-05 reasons

| reason | role |
|---|---|
| `H05_REASON_1 = AUTHORITATIVE_RECOVERY_ACCURACY_CRITERION_NOT_OPERATIONALIZED` | `PRIMARY_SEMANTIC_BLOCKER` |
| `H05_REASON_2 = RESIDUAL_VALIDATION_COMPLETED` | `COMPLETED_REQUIREMENT_NOT_A_BLOCKER` |
| `H05_REASON_3 = D2_PRESPECIFICATION_PROVENANCE_NOT_RECOVERED` | `EVIDENCE_DOMAIN_LIMITATION` (limits eligible evidence to {D7,D8,D9-correct,D10}; does not itself invalidate that separately-prespecified eligible set) |

## Causal and ontological boundaries — unchanged

```
G_causal = 0
G_ontology = 0
```

Nothing in this operation — the source recovery, the semantic decomposition,
or the operationalization audit — identifies historical causality,
resistance contagion, or validates any mapping between coded events and
latent historical occurrence. The maximum allowed interpretation of
anything produced here remains: **model-conditional performance of a
synthetic validation pipeline.**

## Final status

```
HAWKES_V2A_H05_NOT_EVALUABLE_PROSPECTIVE_GOVERNANCE_ARCHITECTURE_FROZEN_AND_SYNCED_V2B_BLOCKED
```

**Checkpoint 1 and Checkpoint 2 both complete. This seven-file package is
frozen and staged/committed/synced under the governing instruction's
authorization; no further approval checkpoint is created by this
document.**
