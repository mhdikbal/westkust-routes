# Hawkes Baseline V2 — Final Modeling Authorization Recommendation

## Recommendation

```text
DEFER_PENDING_F08_PROVENANCE_AND_AUTHORIZE_SEPARATE_V2_VALIDATION_GATE_AMENDMENT_REVIEW
```

This is **not** a modeling authorization. `G_V2_preauth = 0`, so no authorization artifact is created (`A_V2 = 0`) and `G_V2_model = 0`. No modeling — technical or historical — is authorized by this operation.

## Why this recommendation, and not a simpler one

`DEFER_PENDING_G7_GATES` alone would understate the situation: `G_G7_raw = 0` is not simply "several gates still fail," it includes one gate (H-05) that is blocked by a genuine **authorization circularity** (`H05_PREAUTHORIZATION_CIRCULARITY_CONFIRMED`) rather than a technical negative result, and one gate (H-08) whose **scope** has now been adjudicated (`H_08_technical=1`, `H_08_historical=0`) without that adjudication being usable to shrink the gate product, because no authoritative governance document defines a technical-only gate subset. Both facts need to be visible to whoever makes the next decision, which the generic deferral label would hide.

## What this recommendation asks for

One narrow future governance decision, not a modeling authorization, splitting the workstream into two prospective stages:

```text
STAGE V2-A: validation-only authorization (prospective, NOT adopted)
- execute the already-distinct recovery design
- execute false-Hawkes controls
- no historical data fitting required except where strictly necessary for calibration design
- no historical inference
- no Phase D rerun
- H-05 is an OUTPUT of this stage, not a precondition for authorizing it

STAGE V2-B: exploratory historical-corpus fitting authorization (prospective, NOT adopted)
- possible only after H-05 passes from V2-A
- formula-source gate (F_SLR) must pass
- primary analysis set (AS1 ∩ AS3, n=86) must remain ready
- historical inference remains prohibited throughout
```

Prospective gates, defined for future researcher adjudication only (neither is evaluated as granting authorization now):

```text
G_V2A_preauth = 1[D_distinct=1 ∧ P_analysis=1 ∧ F_SLR=1 ∧ O_obs=1 ∧ E_epi=1 ∧ I_guard=1 ∧ B_historical=1 ∧ R_PhaseD=0]
             = 0  (currently blocked independently by F_SLR=0)

G_V2B_preauth = 1[H-05=1 ∧ P_analysis=1 ∧ F_SLR=1 ∧ O_obs=1 ∧ E_epi=1 ∧ I_guard=1 ∧ B_historical=1]
             = not evaluable until V2-A executes and H-05 becomes an observed output
```

## Current final gate state

```text
G_G7_raw       = 0
D_distinct     = 1
P_analysis     = 1
F_SLR          = 0
O_obs          = 1
E_epi          = 1
I_guard        = 1
B_historical   = 1  (H_08_historical=0 satisfied as the required permanent constraint)
G_V2A_preauth  = 0
G_V2_preauth   = 0
A_V2           = 0
G_V2_model     = 0
```

## What would need to happen before either stage could be authorized

1. A separate, explicit researcher/governance decision adopting (or rejecting) the V2-A/V2-B staged structure itself — this operation only proposes it.
2. Resolution of the F-08 (time-rescaling theorem) provenance gap — lawful full-text access to Ogata (1988) JASA 83(401), confirming the exact locator, and separately verifying the Papangelou attribution lead.
3. If V2-A is adopted and authorized: execution of the already-specified distinct recovery design and false-Hawkes controls, in a dedicated future operation — producing, for the first time, an actual observed H-05 result rather than `NOT_OBSERVED`.
4. Only if V2-A's H-05 output then passes ≥0.80, and F_SLR and the other gates still hold: a further, separate authorization decision for V2-B (technical exploratory historical-corpus fitting only — historical inference remains permanently prohibited regardless of any future decision, per `H_08_historical=0`).

## Explicit non-conclusions

This operation does **not**:
- authorize any fitting, simulation, or recovery execution;
- adopt the V2-A/V2-B structure as governance (it is a recommendation for review, not an amendment already in force);
- resolve F-08;
- compute or imply a corrected p-value;
- change `H_08_historical=0` (permanent);
- rerun Phase D or modify any production Hawkes artifact.

## Final status

```text
HAWKES_V2_FINAL_BLOCKER_CLOSURE_COMPLETE_MODELING_REMAINS_BLOCKED
```
