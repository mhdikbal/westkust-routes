# HAWKES BASELINE V2-A — ONTOLOGY AND CAUSAL BOUNDARY

## Ontology contract

| Type | Definition |
|---|---|
| `LATENT_HISTORICAL_EVENT` | An event that actually occurred in history, whether or not any surviving document reports it. Never directly observed by any process in this repository. |
| `DOCUMENTED_OR_REPORTED_EVENT` | A `LATENT_HISTORICAL_EVENT` recorded by a contemporary source, subject to that source's survival, access, and reporting biases. Subset of `LATENT_HISTORICAL_EVENT`. |
| `CORPUS_CODED_EVENT` | A `DOCUMENTED_OR_REPORTED_EVENT` located, read, and coded into this project's structured corpus. Subset of `DOCUMENTED_OR_REPORTED_EVENT`. |
| `PARENT_EPISODE` | A `CORPUS_CODED_EVENT` (or cluster) treated as a cluster-process triggering point (D6's Neyman-Scott parents). A modeling role, not an independent class. |
| `SYNTHETIC_GENERATED_EVENT` | An event produced by a V2-A simulator from a fully specified synthetic DGP. No historical referent. The only type any V2-A generator (`gen_D1`...`gen_D9`, `gen_D10_latent`) produces. |
| `OBSERVED_SYNTHETIC_EVENT` | A `SYNTHETIC_GENERATED_EVENT` after a design's observation mechanism (D5 thinning, D10 precision-class assignment). Subset of `SYNTHETIC_GENERATED_EVENT`. |
| `ESTIMATOR_INPUT_EVENT` | The array actually passed to the fitting routines. Equals `OBSERVED_SYNTHETIC_EVENT` (or `SYNTHETIC_GENERATED_EVENT` where no observation mechanism applies) for most designs; for D10, the post-imputation array. |

**Mapping:**

```
N_corpus(t) = O{ H(t), observation, survival, access, coding }
```

The count of `CORPUS_CODED_EVENT`s at time `t` is the image of the true
`LATENT_HISTORICAL_EVENT` process `H(t)` under the composed, lossy,
non-random-in-`t` operator of contemporary observation, documentary
survival, researcher access, and coding.

**Prohibited identity:**

```
N_corpus(t) = H(t)     -- FORBIDDEN
```

No result in R1, R2, or any prior V2-A artifact treats corpus-coded counts
as equal to true latent historical counts. Every computation in R1 and R2
operates exclusively on `SYNTHETIC_GENERATED_EVENT` / `OBSERVED_SYNTHETIC_EVENT`
/ `ESTIMATOR_INPUT_EVENT` data — the bootstrap DGPs in R2 simulate from
fitted parameters on synthetic parent replications, never from or into the
historical corpus.

```
G_ontology = 1[ M_event=1 AND M_report=1 AND M_episode=1 AND M_source=1 AND M_coding=1 ]
G_ontology = 0
```

V2-A (including this residual-validation operation) does not establish any
of the five mappings `M_event/M_report/M_episode/M_source/M_coding` between
synthetic estimator behavior and the real historical record. `G_ontology`
therefore cannot be set to 1 by this or any prior V2-A operation.

## Causal boundary

**V2-A (R1+R2 included) validates estimator and diagnostic behavior under
prespecified synthetic data-generating processes.** It establishes: how
often a fitted Hawkes model is preferred over a stated comparator under
known synthetic truth (D1–D6); how well MLE recovers known parameters and
how well Wald CIs cover the known truth under known synthetic DGPs (D7–D10);
whether marginal and serial-independence residual diagnostics reject under
those same known DGPs, with and without parametric-bootstrap calibration
(R1, R2, this operation).

**V2-A does not identify, and no result from this operation should be read
as evidence of:**
- historical causality between any two real events;
- resistance contagion or diffusion in the historical record;
- event-to-event transmission mechanisms;
- the endogenous share of historical events attributable to
  self-excitation versus exogenous causes;
- the effect of any intervention, historical or counterfactual.

```
G_causal = 1[ E_intervention=1 AND E_counterfactual=1 AND E_confounding=1
              AND E_observation=1 AND E_identification=1 ]
G_causal = 0
```

**Hawkes preference over Poisson, wherever it appears in D1–D6, is
model-selection evidence only within the specific candidate model set
compared, and only under the synthetic DGP each design constructs.** R1's
independence-diagnostic non-rejection and R2's bootstrap non-rejection (all
five arms, this operation) are, likewise, statements about a fitted model's
own residual behavior relative to a synthetic null or a model-relative
bootstrap distribution — not statements about whether a Hawkes process
correctly describes any real historical process, and not statements that
self-excitation "is present" in history.

**Required final language:**
```
model-conditional synthetic validation
corpus-event temporal pattern
estimator recovery under specified DGP
Hawkes preference within a candidate model set
model-relative bootstrap calibration for one prespecified parent realization
```

**Prohibited language:**
```
historical contagion
causal transmission
resistance diffusion proven
true endogenous fraction of history
ontology validated by Hawkes fit
residual independence validated (R1 shows non-rejection only)
D9-misspecified model validated (p_boot=0.680 is model-relative only)
```
