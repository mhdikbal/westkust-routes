# SLR — Appraisal Dimensions and Epistemic Boundary

**Status:** PLANNING ONLY. No study has been appraised yet.

---

## 1. Appraisal Dimensions

```math
A_i=(a_{i1},\dots,a_{iK}).
```

Each dimension is binary or categorical and reported individually — **never collapsed into a single weighted quality score** unless a future protocol amendment separately justifies that score's construct validity (no such justification is made or assumed here).

| Dimension | Definition | Values |
|---|---|---|
| source_criticism | Does the study critically examine its own sources' provenance, bias, and limitations? | YES / PARTIAL / NO |
| observation_model_clarity | Is the separation between a latent process and its observed trace made explicit (cf. `Y_t ~ p(Y_t \mid H_t, O_t, S_t)`)? | EXPLICIT / IMPLICIT / ABSENT |
| provenance_completeness | Are claims traceable to specific sources with position/location information? | COMPLETE / PARTIAL / ABSENT |
| estimand_clarity | Is what the study estimates or interprets stated unambiguously? | CLEAR / AMBIGUOUS / UNSTATED |
| denominator_clarity | Are all reported proportions/rates given with an explicit denominator? | ALWAYS / SOMETIMES / NEVER / NOT_APPLICABLE |
| validation_adequacy | Is the method validated (simulation recovery, holdout, expert agreement) proportionate to its claims? | ADEQUATE / PARTIAL / ABSENT / NOT_APPLICABLE |
| identifiability_treatment | Are identifiability limits of the model or method discussed? | EXPLICIT / ASSUMED / NOT_ADDRESSED / NOT_APPLICABLE |
| ambiguity_handling | Is interpretive ambiguity/plurality represented or averaged away? | REPRESENTED / AVERAGED_AWAY / NOT_APPLICABLE |
| reproducibility | Are code/data/replication materials available? | FULL / PARTIAL / NONE |
| epistemic_boundary_discipline | Does the study distinguish tool output, interpretation of tool output, and source-supported historical claim? | MAINTAINED / BLURRED / NOT_APPLICABLE |

These dimensions populate `SLR_DATA_EXTRACTION_SCHEMA.csv` fields EXT-08, EXT-11–EXT-20 at the per-study level; this document defines the dimension semantics once, for consistent application across all extractors.

---

## 2. Computational-Hermeneutic Boundary (governs synthesis, not just appraisal)

Three distinctions must be preserved throughout the review, and by extension in any project work the review informs:

```text
tool-mediated interpretation
!= interpretation of tool output
!= historical claim supported by sources
```

- **Tool-mediated interpretation**: a human interpreter using a computational tool (search, extraction, network layout, simulation) as an aid.
- **Interpretation of tool output**: the human act of assigning meaning to what a tool produced — this is where hermeneutic judgment actually happens, and it is irreducibly human, plural, and situated.
- **Historical claim supported by sources**: a claim that can be traced to and defended by primary or properly admissible secondary sources, independent of any tool's output.

A tool's output (a similarity score, a network edge, a fitted intensity function, an extracted entity) is never itself a historical claim. Collapsing these three levels — treating a model's output as if it were already an interpreted, source-supported historical fact — is the single most important failure mode this review is designed to detect and prevent, in the reviewed literature and in this project's own future work alike.

---

## 3. Colonial Observation Model (governs domain S3 appraisal and downstream use)

```math
Y_t\sim p(Y_t\mid H_t,O_t,S_t),
```

with `H_t` the latent historical process, `O_t` the institutional observation/recording process, and `S_t` the survival/selection/accessibility process. The review must never assume `Y_t = H_t`.

Appraisal consequence: a study appraised as `observation_model_clarity = ABSENT` for domain-S3-relevant material is flagged in the contradiction/gap ledgers as a methodological weakness — silently treating archival records as unmediated fact is precisely the failure this project's own governance (already established across S1-B0/S1-B1) exists to avoid.

VOC labels, classifications, and silences are always treated as source-positioned institutional observations (`O_t`, filtered through `S_t`), never as neutral historical fact (`H_t`) — in the reviewed literature's own claims, and in this project's later use of that literature.

---

## 4. Hawkes Relevance Gate (governs domain S5 appraisal, reiterated from protocol §17)

```math
H_i^{\mathrm{relevant}}=\mathbf 1\left(\sum_{k=1}^{9}h_{ik}\ge1\right).
```

Relevance is necessary but not sufficient for inclusion in any future Model 3B V2 design decision — a relevant study still passes through full appraisal (§1 above) before its findings inform anything. No historical Hawkes fit is authorized by this review or by any appraisal within it.

---

## 5. Epistemic Red Lines (apply across all six domains)

The review, and anything built on it, must never:

1. treat a computational pattern as a historical claim without independent source support;
2. treat archival presence/absence as evidence of historical presence/absence without modeling `O_t` and `S_t`;
3. average away documented interpretive plurality into a single "consensus" reading;
4. assign a numerical historical payoff, weight, or threshold without documented provenance;
5. claim game-theoretic equilibrium or strategic rationality for a historical actor without source support for that actor's actual reasoning;
6. treat a Hawkes-family model's temporal excitation as historical causation;
7. pool incompatible study designs/estimands to manufacture an aggregate finding;
8. use this review's findings to overwrite or reinterpret already-frozen archival evidence (S1-B0/S1-B1 outputs) retroactively.

These red lines are the same discipline already enforced across this project's S1-B0/S1-B1 mathematical contracts, extended here to govern how literature-review findings may (and may not) be used.
