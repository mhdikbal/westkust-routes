# Systematic Scoping Review Protocol — Computational Hermeneutics, Colonial Archives, and Temporal Event Modeling

**Status:** PLANNING ONLY. No search has been executed. No database has been queried. No record has been retrieved, screened, or extracted. This protocol governs a future review; it does not itself review anything.

**Project:** Painan–Indrapura Strategic History Lab / Model 3B
**Scope of this turn:** protocol authoring only
**Network search:** NOT AUTHORIZED this turn
**S1-B2 through S1-B5:** NOT AUTHORIZED
**Historical inference / model fitting:** NOT AUTHORIZED

---

## 1. Purpose and Decision

Before content indexing (S1-B2), interpretive claim entry, Hawkes V2 implementation, game-theory application, or counterfactual modeling proceed, the project adopts a two-track sequence:

1. close and freeze the completed S1-B1 bibliographic-identity evidence after researcher review (a separate, already-in-progress workstream — not touched by this protocol);
2. run a systematic/scoping literature review across six linked strata before any of the interpretive or modeling work listed above begins.

This review exists to establish, from the published methodological and critical literature, what disciplined practice looks like for computational hermeneutics, colonial-archive criticism, historical information extraction, temporal point-process modeling under coarse timestamps, and network/game-theoretic/counterfactual historical claims — **before** those methods are applied to this project's own archival material. The review must not be used to overwrite archival evidence, retrofit conclusions already suspected, or manufacture legitimacy for a predetermined modeling choice.

---

## 2. Review Type

A **systematic scoping review with PRISMA 2020-compatible reporting** (PRISMA-ScR alignment), chosen because the seven research questions (§4) span heterogeneous humanities, archival-critical, computational, and statistical literatures rather than a single intervention-effect estimand. A scoping review is the correct instrument here: it maps the extent, range, and nature of evidence and practice, rather than pooling effect sizes.

The protocol explicitly distinguishes four review activities, which must not be collapsed into one another:

1. **evidence mapping** — where, how much, and what kind of relevant literature exists per domain;
2. **conceptual synthesis** — how hermeneutic and epistemic concepts (situated meaning, plurality, ambiguity, archival silence, identifiability) are defined and operationalized across sources;
3. **methodological appraisal** — how rigorously each study specifies its observation model, estimand, denominator, and validation;
4. **quantitative effect synthesis** — explicitly **not presumed applicable** here; pooling is authorized only if a later amendment demonstrates design and estimand compatibility across a specific subset of studies (see §14 of the instruction; not evaluated in this planning turn).

---

## 3. Review Domains (Six Linked Strata)

```text
S1: Computational hermeneutics and hermeneutics of computation
    - situated meaning; plurality of interpretation; ambiguity; hermeneutic circle;
      human-in-the-loop interpretation; AI as cultural technology; contextual evaluation.

S2: Digital humanities and computational history
    - relation of computational method to humanistic argument; interpretation of model
      output; methodological transparency; distant vs. close reading; uncertainty
      representation; the boundary between pattern and historical claim.

S3: Colonial archive criticism
    - archival silence; colonial categories; administrative/observation bias;
      record survival; source selection; absent actors/voices; VOC classification
      as institutional position, not neutral fact.

S4: Historical information extraction and provenance
    - entity/event extraction; uncertainty labels; claim-source linkage; provenance;
      temporal ambiguity; document date vs. event date; source dependence;
      parent-episode structure; human validation.

S5: Hawkes and temporal event modeling
    - annual/coarse timestamps; interval censoring; tied timestamps; sparse event
      series; branching-ratio identifiability; exact-null construction; boundary
      parameters; simulation recovery; uncertainty calibration; observation-process
      distortion.

S6: Network, game theory, and counterfactual history
    - network evidence vs. visual representation; actor/relation uncertainty;
      dynamic alliances; strategic interaction; payoff provenance; equilibrium
      claims; counterfactual identification; prohibition on arbitrary numerical payoffs.
```

Each stratum is reviewed on its own terms; no stratum's findings are used to force a conclusion in another (e.g., a strong hermeneutic-plurality finding in S1 does not by itself license a Hawkes identifiability claim in S5).

---

## 4. Review Questions

```text
RQ1: How is computational hermeneutics defined, operationalized, and evaluated?
RQ2: How do computational-humanities studies separate tool output from humanistic interpretation?
RQ3: How are colonial categories, archival silences, and source observation processes represented?
RQ4: Which provenance and uncertainty practices are used for historical event/entity extraction?
RQ5: Which temporal-event models are defensible under year-level timestamps, ties, interval
     censoring, and sparse exact dates?
RQ6: Which validation, simulation-recovery, identifiability, and negative-result practices
     are recommended?
RQ7: How are network, strategic, game-theoretic, and counterfactual claims bounded to avoid
     arbitrary payoffs or unsupported equilibrium claims?
```

RQ1–RQ2 map to stratum S1/S2; RQ3 to S3; RQ4 to S4; RQ5–RQ6 to S5; RQ7 to S6. Full eligibility logic per RQ is in `SLR_RESEARCH_QUESTIONS_AND_ELIGIBILITY.md`.

---

## 5. Search Universe

```math
D=\{d_1,\dots,d_J\}.
```

`J` is **not invented in this protocol**. A candidate provider list is proposed in `SLR_SEARCH_SOURCE_REGISTRY.csv` for researcher review; `J` is frozen only after that review, before any search is executed. Candidate classes:

```text
multidisciplinary citation indexes
humanities bibliographies
library catalogues
publisher databases
preprint repositories
institutional repositories
backward and forward citation chaining
```

Search engines (e.g., Google Scholar) may support discovery but are never the sole bibliographic authority for an included record — consistent with the provider-role discipline already established for S1-B1 (`DISCOVERY_ONLY` providers cannot independently confirm inclusion).

---

## 6. Search Blocks

```math
C_1=\text{computational hermeneutics terms}
```
```math
C_2=\text{digital/computational history terms}
```
```math
C_3=\text{colonial archive/source criticism terms}
```
```math
C_4=\text{historical NLP/provenance/uncertainty terms}
```
```math
C_5=\text{Hawkes/coarse time/interval censoring/identifiability terms}
```
```math
C_6=\text{historical network/game theory/counterfactual terms}
```

Each search family combines a methods block (`C_k`) with a historical-humanities context block. Candidate term lists are drafted in `SLR_SEARCH_STRING_REGISTRY.csv`; every exact query string, database, date, filters, and result count must be recorded at execution time — none of that exists yet, since no search has run.

---

## 7. Record Sets and PRISMA Accounting

```math
R_0=\text{all retrieved records},\quad
R_1=\text{deduplicated records},\quad
R_2=\text{title/abstract screened},\quad
R_3=\text{full-text assessed},\quad
R_4=\text{included studies}.
```

Required monotonicity:

```math
|R_0|\ge|R_1|\ge|R_2|\ge|R_3|\ge|R_4|.
```

PRISMA accounting identity:

```math
|R_0|=|R_1|+N_{dup}+N_{auto}+N_{other},
```

where `N_dup` (exact/fuzzy-adjudicated duplicates), `N_auto` (automation-tool exclusions, if any, with tool and rule disclosed), and `N_other` (any other explicit removal category) are each separately defined and reported — never merged into an opaque "other" bucket. All counts are currently `0/undefined` — no retrieval has occurred.

---

## 8. Deduplication

Exact duplicate:

```math
D_{ab}^{\mathrm{exact}}=\mathbf 1(ID_a=ID_b \land ID_a\neq\varnothing),
```

using DOI, ISBN/edition identifier, or exact catalogue identifier — the same hard-identifier discipline already established for S1-B1.

Fuzzy title similarity is candidate evidence only, never an automatic merge:

```math
D_{ab}^{\mathrm{candidate}}=\mathbf 1(s_{\mathrm{title}}(a,b)\ge\tau_s).
```

`\tau_s` is **not selected in this protocol** without calibration and documented provenance. Fuzzy candidates always require manual adjudication; a fuzzy match is never silently removed.

---

## 9. Eligibility

```math
I(r)=\mathbf 1[P(r)=1\land M(r)=1\land E(r)=1],
```

where `P(r)` = relevant population/corpus/problem, `M(r)` = relevant method or conceptual framework, `E(r)` = sufficient methodological or conceptual evidence. Full operational definitions per domain are in `SLR_RESEARCH_QUESTIONS_AND_ELIGIBILITY.md`.

Exclusion reasons are mutually interpretable and recorded at full-text stage (schema in `SLR_SCREENING_AND_EXCLUSION_SCHEMA.csv`). Methodological, conceptual, empirical, and critical scholarship are all included; humanities work is never excluded merely for lacking a statistical evaluation.

---

## 10. Screening Reliability

If dual screening is feasible:

```math
P_o=\frac{N_{\mathrm{agree}}}{N_{\mathrm{screened}}},\qquad
\kappa=\frac{P_o-P_e}{1-P_e}.
```

No numeric kappa threshold is imposed without protocol justification (none is imposed in this planning turn). Disagreements go to adjudication, not majority inference. If only one primary screener is available (the realistic case for this project), a preregistered audit sample is used and that limitation is explicitly reported — not concealed.

---

## 11. Extraction Schema

Full column-by-column schema in `SLR_DATA_EXTRACTION_SCHEMA.csv`. Minimum fields (per instruction §11): bibliographic identity and publication type; disciplinary domain; corpus/source type; temporal and spatial domain; research question; hermeneutic framework; computational method; observation model; unit of analysis; estimand or interpretive target; denominator; validation design; uncertainty representation; provenance model; human-in-the-loop role; treatment of ambiguity and plurality; treatment of colonial categories and archival silences; identifiability claims; negative-result handling; reproducibility assets; limitations; relevance to S1, Atlas, Model 3B, Hawkes, networks, game theory, or counterfactual work.

---

## 12. Appraisal Dimensions

```math
A_i=(a_{i1},\dots,a_{iK})
```

Binary/categorical, never collapsed into a weighted score without a separately justified construct-validity argument (none is made here). Full dimension list in `SLR_APPRAISAL_AND_EPISTEMIC_BOUNDARY.md` §1.

---

## 13. Coverage Estimands

```math
\widehat P_h=\frac{N_{\mathrm{included},h}}{|R_4|},\qquad
\widehat P_m=\frac{\sum_{i\in R_4}\mathbf 1(m_i=1)}{|R_4|},
```
```math
\widehat P_{\mathrm{obs}}=\frac{N_{\mathrm{explicit\ observation\ model}}}{|R_4|},\qquad
\widehat P_{\mathrm{recovery}}=\frac{N_{\mathrm{recovery}}}{N_{\mathrm{empirical\ computational\ studies}}}.
```

Every proportion is reported with its denominator, explicitly. None of these has a value yet — `|R_4|` is undefined until screening completes.

---

## 14. Synthesis Products (all deferred to post-search turns)

```text
1. evidence map by domain and method
2. structured narrative synthesis
3. conceptual synthesis of hermeneutic principles
4. methodological matrix linking observation regime, estimand, validation, and inference boundary
5. contradiction ledger
6. research-gap ledger
7. literature-to-design decision ledger
8. implications for S1
9. implications for Atlas
10. implications for Model 3B / Hawkes V2
```

No quantitative pooling occurs unless study designs and estimands are demonstrably compatible — this demonstration itself is a future, separate methodological decision, not assumed here.

---

## 15. Computational-Hermeneutic Boundary

Three distinctions are preserved throughout the review and any downstream use of its findings:

```text
tool-mediated interpretation
!= interpretation of tool output
!= historical claim supported by sources
```

Model output (from this project's own future NLP/extraction/Hawkes/network tools, or from any reviewed study's tool) is never self-interpreting. Ambiguity, situatedness, and plurality of interpretation are represented as such, not averaged away into a single summary statistic.

---

## 16. Colonial Observation Model

For latent historical process `H_t` and observed archival record `Y_t`:

```math
Y_t\sim p(Y_t\mid H_t,O_t,S_t),
```

where `O_t` is the institutional observation/recording process and `S_t` is the survival, selection, and accessibility process governing which sources reach us at all. The review must never assume:

```math
Y_t=H_t.
```

VOC labels, classifications, and archival silences are treated throughout the review (and in any of this project's own future work informed by it) as source-positioned observations, not neutral historical facts. This formal separation directly extends the Painan-Indrapura project's own existing epistemic discipline (established across the S1-B0/S1-B1 workstreams) into the literature-review stage.

---

## 17. Hawkes Relevance Gate

A reviewed study is directly relevant to Model 3B only if it addresses at least one of nine listed features (coarse/interval-censored timestamps; tied timestamps; sparse event sequences; observation-process distortion; simulation recovery; exact-null construction; branching-ratio identifiability; uncertainty calibration; model comparison under boundary parameters):

```math
H_i^{\mathrm{relevant}}=\mathbf 1\left(\sum_{k=1}^{9}h_{ik}\ge1\right).
```

This is a **relevance gate only** — it does not endorse the Hawkes method, and it does not authorize a historical Hawkes fit. Model 3B's V1 Hawkes workstream remains closed (`FAILED_VALIDATION`/`RESEARCH_ONLY`/`INFERENCE_NOT_AUTHORIZED`); this review may inform a future V2 identifiability redesign decision, but does not itself constitute that decision.

---

## 18. Review Completion Gate

```text
G_P: protocol frozen
G_S: search sources and strings frozen
G_R: retrieval accounting complete
G_D: deduplication complete
G_E: eligibility decisions complete
G_X: extraction complete
G_A: appraisal complete
G_Y: synthesis complete
G_C: contradictions and gaps recorded
G_0: no unauthorized historical inference or model execution occurred
```

```math
G_{SLR}^{\mathrm{complete}}=\mathbf 1[G_P=G_S=G_R=G_D=G_E=G_X=G_A=G_Y=G_C=G_0=1].
```

Current state (this planning turn): `G_P=0` (protocol drafted, not yet researcher-frozen), all other gates `0`/undefined — no search has occurred. Live tracking in `SLR_SPRINT_BOARD.md`.

---

## 19. Stop Conditions

Stop and report `SYSTEMATIC_LITERATURE_REVIEW_REQUIRES_RESEARCHER_REVIEW` if: search strings or databases change after screening begins without a documented amendment; inclusion criteria are altered after seeing desirable results; duplicate records are silently removed; inaccessible full text is treated as negative evidence; colonial terminology is normalized into historical fact; humanities evidence is excluded solely for lacking quantitative metrics; incompatible studies are pooled; a numerical threshold lacks provenance; review findings are used to overwrite archival transcription or source evidence; or S1-B2, claim entry, Hawkes fitting, game-theory payoff assignment, or counterfactual execution begins without separate authorization.

---

## 20. Immediate Project Sequence

```text
1. Review and freeze the four completed S1-B1 execution outputs — separate workstream, in progress.
2. Create and review these eight SLR planning artifacts (this turn).
3. Freeze the SLR protocol before any literature search.
4. Execute pilot searches and calibrate eligibility rules.
5. Run the full review with PRISMA-compatible accounting.
6. Produce a literature-to-design decision ledger.
7. Only then authorize S1-B2 content indexing, interpretive claim entry, or Model 3B V2
   implementation, each as a separate decision.
```

---

## 21. Final Status of This Turn

```text
COMPUTATIONAL_HERMENEUTICS_SYSTEMATIC_SCOPING_REVIEW_PROTOCOL_READY_FOR_RESEARCHER_REVIEW
```

No search executed. No stage/commit/push performed.
