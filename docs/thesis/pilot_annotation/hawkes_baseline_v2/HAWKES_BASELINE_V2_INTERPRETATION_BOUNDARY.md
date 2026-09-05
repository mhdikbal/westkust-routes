# Hawkes Baseline V2 — Interpretation Boundary

This document types every claim this audit is entitled to make, per instruction §24.

## Allowed claim types

```text
DESCRIPTIVE_CORPUS_PATTERN
MODEL_CONDITIONAL_RESULT
ROBUSTNESS_RESULT
FALSIFICATION_RESULT
HISTORICAL_INTERPRETATION_REQUIRING_SOURCES
UNRESOLVED_LIMITATION
```

## What this audit found, typed

| Claim | Type |
|---|---|
| n=141 events reconciles across `data/export/all_event_years.csv` and the provenance working CSV | DESCRIPTIVE_CORPUS_PATTERN |
| 6/141 events carry an unresolved duplicate-review flag; 32/141 are `PROVENANCE_AMBIGUOUS` | UNRESOLVED_LIMITATION |
| CD source family carries 71/141 events (HHI=0.30); 57/141 events' existence depends primarily on CD | DESCRIPTIVE_CORPUS_PATTERN |
| The already-published pooled Hawkes fit (mu=0.2573, alpha=0.4207, beta=0.6215, eta=0.6769) reproduces exactly from the unmodified script and current data | MODEL_CONDITIONAL_RESULT |
| The existing LR-test p-value tests a parameter-space boundary null (eta=0) using an interior-null chi-square reference, which is very likely invalid | UNRESOLVED_LIMITATION |
| Event-type strata (smallest n=4) and most episode strata (n<5) are too sparse for a stratified/multivariate Hawkes (M6) | UNRESOLVED_LIMITATION |
| CD/GM/Daghregister document-density series exist and could support an exposure-adjusted model (M4), but GM/Daghregister only cover partial year ranges | DESCRIPTIVE_CORPUS_PATTERN |
| No simulation-recovery, false-Hawkes, or residual-diagnostic result exists this turn | UNRESOLVED_LIMITATION (nothing was run — Branch B) |

## Prohibited statements (per instruction §14, §24 — none of these were made anywhere in this audit)

```text
event nyata
resistance contagion proven
causal propagation
defection diffusion established
resistance contagion / historical causal transmission / defection diffusion /
true endogenous share of historical events (as an interpretation of eta)
```

## Required substitutions when referring to the existing baseline

```text
observed coded event   (not "real event" / "event nyata")
fitted corpus-event clustering   (not "cascade" as a historical claim)
model-conditional excitation   (not "self-excitation is real")
```

## Epistemic relation preserved throughout

```text
N(t) = O{H(t), O(t), S(t), C(t)}   —   N(t) ≠ H(t) is never violated in this audit.
```
The current Hawkes estimand concerns the observed coded-event process `N(t)`, never the latent historical process `H(t)`, directly. No historical mechanism, resistance dynamic, or causal claim is asserted anywhere in this audit's outputs.
