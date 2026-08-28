# MODEL 3B-CD V1 — STATUS ADDENDUM: RESEARCH_ONLY / INFERENCE_NOT_AUTHORIZED

> **STATUS ADDENDUM ONLY — NOT A NEW FINDING, NOT A V2 DESIGN, NOT A REPAIR**
> **NO SIMULATION RUN, NO V1 REPAIR, NO REAL-DATA FITTING, NO PHASE REOPENED**
> **DOES NOT REOPEN PHASE A/B/C/D — THOSE STATUSES ARE READ HERE, NOT DECIDED HERE**
> **NO RUNTIME, API, ATLAS, GRAPHIFY, OR PRODUCTION CHANGE AUTHORIZED BY THIS ADDENDUM**
> **RESEARCHER-DIRECTED FRAMING CORRECTION, FROZEN 2026-08-28**

---

## 1. Purpose

This addendum does exactly one thing: it fixes the **status label and the framing
language** for `MODEL_3B_CD_V1`. It introduces no new evidence, recomputes nothing,
and changes no prior document. Every number cited here is quoted from an existing
frozen artifact, named at the point of use.

It exists because the previously used phrasing — "the model **cannot be deployed**" —
states the wrong category of failure. That phrasing describes a *technical*
impediment. The actual failure is one of *epistemic authority*. This addendum
replaces the phrasing and freezes the correct status label.

## 2. Frozen Status (this addendum's operative content)

```text
MODEL_3B_CD_V1:                 RESEARCH_ONLY / INFERENCE_NOT_AUTHORIZED
```

Read in full, this label means:

```text
CODE_EXECUTABILITY:             UNIMPAIRED   (the pipeline runs and is reproducible)
ESTIMATED_EXCITATION:           NOT_INTERPRETABLE_AS_HISTORICAL_INFERENCE
REAL_DATA_FITTING_V1:           NOT_AUTHORIZED
PRODUCTION_USE:                 NOT_AUTHORIZED
PUBLIC_DISPLAY:                 NOT_AUTHORIZED
THESIS_USE:                     METHODOLOGICAL_NEGATIVE_RESULT_ONLY
```

Statuses carried forward unchanged from `MODEL_3B_CD_V1_POSTMORTEM.md` §2 and
`MODEL_3B_POST_PHASE_D_EPISTEMOLOGICAL_NOTE.md` §2 — reaffirmed, not re-decided:

```text
MODEL_3:                        RETAINED_AS_POOLED_EXPLORATORY_BASELINE
MODEL_3B_CD_V1:                 CLOSED_AFTER_FAILED_RECOVERY_VALIDATION
SIMULATION_RECOVERY_V1:         FAILED
MODEL_V2:                       NOT_AUTHORIZED
HISTORICAL_MECHANISM_INFERENCE: PROCESS_TRACING_ONLY
PHASE_D_PRIMARY_RESULT:         RESIDUAL_CLUSTERING_NOT_SUPPORTED IN ALL 9 ARMS
```

`RESEARCH_ONLY / INFERENCE_NOT_AUTHORIZED` is a **relabeling** of this existing
state, not an additional restriction and not a relaxation of one.

## 3. The Framing Correction

**Superseded phrasing:** "Model 3B-CD V1 cannot be deployed."

**Correct phrasing:**

> Model 3B-CD V1 **can be executed; it is not authorized to produce historical
> inference.**

The distinction is not cosmetic. "Cannot be deployed" implies an obstacle that
better engineering, more compute, or a longer run would remove. Nothing in the
V1 record supports that reading. The pipeline was demonstrated to work:
9,300/9,300 checksum-valid sequences, 0 duplicate seeds or replicate IDs,
0 nonfinite or out-of-window events, convergence 0.999–1.0
(`MODEL_3B_CD_FINAL_1000_RECOVERY_AUDIT.md` §7, §8; `MODEL_3B_CD_V1_POSTMORTEM.md`
§11 "V1 established" items 1–2). The machinery is sound. What the machinery
produces is not admissible as a claim about the past.

## 4. Why Simulation-Recovery Failure Is Disqualifying

Simulation-recovery tests the **pipeline**, not the history. Its logic is closed:

```text
Input:        simulated data whose generating mechanism is KNOWN
Expected:     the pipeline recovers the signal it was given
Observed:     recovery inadequate
Consequence:  estimated excitation cannot be trusted as historical inference
```

If a pipeline cannot recover a mechanism it planted itself — under conditions
strictly more favourable than the archive, because the truth is known and the data
are clean — then the parameters it reports on 141 real events carry no referential
guarantee. Numbers still appear. Their meaning does not.

This is why the failure blocks interpretation rather than merely weakening it, and
why it cannot be argued around by appeal to how well the model fits the real series.
Goodness-of-fit on real data is not evidence of recovery; V1's own record shows the
two can come apart.

## 5. Why "Low Significance" Is the Wrong Diagnosis

Treating this as a significance problem misplaces the failure by one layer.

| Framing | Presupposes | Remedy implied | Applicable here |
|---|---|---|---|
| Low significance | estimator works, sample is thin | raise n, widen window, pool | **No** |
| Recovery failure | estimator's referential validity is unestablished | new validation design | **Yes** |

Low significance is a statement about **power**. Recovery failure invalidates an
assumption one layer beneath power — **identifiability**. Increasing n, extending
the window, or swapping the kernel are power interventions; none of them addresses
whether the parameter was ever recoverable in this data regime.

The V1 gate table (`MODEL_3B_CD_V1_POSTMORTEM.md` §4) shows this directly: the
failures are not marginal-significance failures, and they are not sampling noise at
n=1,000/cell.

- False-positive excitation, S1×3 (α_true = 0): **7.3%–9.6%** against a ≤0.05 gate —
  the model reports excitation where none was planted.
- 95% CI coverage for α/β: **60%–84%** against a nominal 92.5%–97.5% — the
  uncertainty quantification is itself miscalibrated, and specifically for α/β;
  coverage for θ0/θ1 is 0.94–0.99, so this is not a general instrumentation fault
  (§5 of the postmortem).
- Correct-model-selection when the truth *is* M3B-CD: **AIC 15.6%–19.2%,
  BIC 2.2%–3.7%** against a ≥0.80 gate — AIC and BIC overwhelmingly prefer the
  simpler M1 even when density and self-excitation are jointly present (§6).

The third row is the decisive one. A procedure that fails to select the true model
roughly four times out of five cannot be used to argue that the true model obtains
in the archive. More data does not repair a selection rule that is wrong in the
direction of the hypothesis being tested.

The postmortem's §12 question 1 — whether this reflects the α–β parameterization
specifically or a deeper identifiability limit of this data regime — **remains open,
and this addendum does not close it.**

## 6. Second, Independent Blocker (not a restatement)

Real-data fitting is blocked twice over, for two separate reasons that must not be
collapsed into one:

1. **Simulation-recovery failure** (§4–§5 above).
2. **Source circularity risk** — the 141 events may be circularly dependent on the
   same Corpus Diplomaticum series used as the density covariate
   (`MODEL_3B_CD_V1_POSTMORTEM.md` §10; `MODEL_3B_CD_MASTER_BLUEPRINT.md`
   §4/§5.4/§17; comparison-matrix status `circularity_risk: possible`).

Blocker 2 would stand even if V1 had passed every recovery gate. Lifting one does
not lift the other.

## 7. What Survives This Status

The label is scoped to `MODEL_3B_CD_V1`. It does **not** retroactively void:

- **Model 3 pooled Hawkes baseline**, which retains
  `RETAINED_AS_POOLED_EXPLORATORY_BASELINE`. Its branching ratio is notably stable
  across two estimators that answer *different* questions: production conditional
  MLE `α/β = 0.676867` versus full MBPP (Rizoiu et al. 2022, closed-form Eq. 9/10,
  IC-LL Eq. 18) `0.676272` — a **0.088%** relative difference, while α and β
  *individually* differ by ~46% (`data/export/model3_mbpp_full_output.json`).
  **Read this narrowly**: `model3_mbpp_full.py`'s own mandatory interpretation
  states that MBPP with s(t)=μ answers a population-mean question, not a
  single-realisation question, so parameter agreement or disagreement "cannot be
  read as who is right and who is wrong", and the Gamma-kernel delayed-peak claim
  can be neither confirmed nor refuted this way without a multi-impulse MBPP
  variant. The ratio's invariance is a **robustness observation about one summary
  quantity**, not an identifiability result, and it does not transfer to 3B-CD.
- **Phase B / C / D results**, complete and unaffected.
- **The engineering pipeline**, established as reproducible (§3).
- **The negative result itself**, which is a legitimate and reportable thesis
  contribution: a preregistered validation that a well-implemented model failed.

Two adjacent negative results are recorded here for scope discipline, both already
frozen elsewhere and **neither caused by this addendum**: the Siklus-vs-Stabil
branching-ratio distinctness test is **not significant** (Δ = 0.391, p = 0.0995,
2,000 null splits — `data/export/model3_cluster_distinctness_output.json`); and
Model 6's capacity confound stands at Spearman ρ = 0.763, p = 0.0039, n = 12 forts
(`docs/thesis/colab/model6_game_theory.py` §header).

## 8. Prohibited Actions (reaffirmed, not newly imposed)

Per `MODEL_3B_CD_V1_POSTMORTEM.md` §14 and the governing plan §18/§40/§49:

- Do not repair or rerun V1; do not fix the S4-G1 `OverflowError` as a route to
  re-legitimising V1.
- Do not alter V1's numerical gates, cell manifest, or parameters.
- Do not fit V1 — or any undeclared "V1.1" — to the 141 real historical events.
- Do not begin implementing any V2 candidate feature without a separate Phase E
  go decision.
- Do not cite V1 excitation estimates as historical findings in any thesis chapter,
  Atlas page, public endpoint, or Graphify node.
- Do not treat this addendum as a V2 specification. It is a status label.

## 9. Researcher Decisions Still Open

Unchanged from `MODEL_3B_CD_V1_POSTMORTEM.md` §15 — this addendum answers none of
them:

1. Whether to proceed to Phase B as the recommended next step.
2. Whether §6/§7 risks favour Phase D's density-only-null test over a Hawkes V2.
3. Whether the S4-G1 defect warrants a standalone bug report.
4. How the false-positive finding should be weighted in the thesis narrative.

---

**STOP** — status addendum frozen. No simulation was run, no V1 file was modified,
no gate was changed, no dataset was altered, no 141-event fitting was performed,
no phase was reopened, and no runtime, Atlas, Graphify, or production surface was
touched.
