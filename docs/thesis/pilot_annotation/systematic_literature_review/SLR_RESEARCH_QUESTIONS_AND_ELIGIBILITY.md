# SLR — Research Questions and Eligibility Criteria

**Status:** PLANNING ONLY. No record has been screened against these criteria yet.

---

## 1. Research Questions, Mapped to Domains

| RQ | Question | Domain(s) |
|---|---|---|
| RQ1 | How is computational hermeneutics defined, operationalized, and evaluated? | S1 |
| RQ2 | How do computational-humanities studies separate tool output from humanistic interpretation? | S1, S2 |
| RQ3 | How are colonial categories, archival silences, and source observation processes represented? | S3 |
| RQ4 | Which provenance and uncertainty practices are used for historical event/entity extraction? | S4 |
| RQ5 | Which temporal-event models are defensible under year-level timestamps, ties, interval censoring, and sparse exact dates? | S5 |
| RQ6 | Which validation, simulation-recovery, identifiability, and negative-result practices are recommended? | S5 |
| RQ7 | How are network, strategic, game-theoretic, and counterfactual claims bounded to avoid arbitrary payoffs or unsupported equilibrium claims? | S6 |

---

## 2. Eligibility Indicator

```math
I(r)=\mathbf 1[P(r)=1\land M(r)=1\land E(r)=1].
```

### 2.1 Population/corpus/problem relevance, `P(r)`

`P(r)=1` if the record concerns at least one of:
- interpretation or meaning-making applied to historical, textual, archival, or cultural material (any period/region);
- colonial or imperial archival record-keeping, classification, or historiography (any colonial context — not restricted to VOC/EIC, since methodological lessons generalize);
- computational or statistical modeling of historical events, entities, texts, or networks;
- game-theoretic or counterfactual analysis of historical political/economic interaction.

`P(r)=0` if the record concerns none of the above (e.g., a purely contemporary NLP benchmark paper with no historical, archival, or interpretive dimension, and no methodological content transferable to any of the six domains).

### 2.2 Method/conceptual-framework relevance, `M(r)`

`M(r)=1` if the record substantively addresses a method or concept from §3 of the protocol (hermeneutic theory of computation; digital-humanities methodology; archival criticism; historical NLP/extraction/provenance; temporal point-process/Hawkes modeling under coarse time; historical network/game-theory/counterfactual methodology).

`M(r)=0` if the record only mentions such a method in passing without substantive methodological or conceptual treatment (e.g., a single sentence citing "distant reading" with no engagement).

### 2.3 Sufficiency of evidence, `E(r)`

`E(r)=1` if the record provides enough methodological or conceptual detail to be extracted against the schema in `SLR_DATA_EXTRACTION_SCHEMA.csv` (i.e., the record is not a title-only index entry, abstract-only stub with no accessible full text, or a duplicate placeholder).

`E(r)=0` if full text cannot be obtained or the accessible content is insufficient for extraction. **Inaccessible full text is never treated as negative evidence about the study's quality or relevance** — it is recorded as `E(r)=0` for the distinct, disclosed reason "full text inaccessible," not conflated with "irrelevant" or "poor quality."

---

## 3. Explicit Non-Exclusions

The review must **not** exclude a record solely because:
- it is humanities scholarship without a quantitative evaluation (qualitative archival criticism and hermeneutic theory are core to domains S1 and S3);
- it predates a particular software tool or computational method (foundational hermeneutic and archival-critical theory is frequently pre-computational and is exactly the theoretical grounding domains S1/S3 require);
- it addresses a different colonial context than VOC/EIC West Sumatra (methodological and critical lessons about archival silence, observation bias, and classification generalize across colonial archives);
- it is a critical or negative-result methodological paper (Hawkes/temporal-model identifiability failures and null results are directly relevant to RQ5/RQ6 and to Model 3B's own closed V1 Hawkes finding).

---

## 4. Domain-Specific Eligibility Notes

### 4.1 S1 — Computational hermeneutics
Eligible: theoretical/philosophical treatments of situated meaning, plurality of interpretation, the hermeneutic circle, human-in-the-loop interpretive systems, and evaluation frameworks for AI as a "cultural technology." Ineligible: purely technical NLP papers with no interpretive or hermeneutic framing.

### 4.2 S2 — Digital/computational humanities and history
Eligible: methodological papers separating computational pattern-finding from historical argument; distant-vs-close-reading methodology; transparency and reproducibility standards in computational history. Ineligible: purely descriptive digital-collection announcements with no methodological content.

### 4.3 S3 — Colonial archive criticism
Eligible: archival theory and historiography addressing silence, classification, administrative bias, record survival/selection, and absent voices in any colonial or imperial archive. Explicitly eligible regardless of statistical content — this is the domain most likely to be purely qualitative/theoretical, and must not be filtered by a quantitative-evidence bar.

### 4.4 S4 — Historical information extraction and provenance
Eligible: entity/event extraction methodology for historical corpora; uncertainty-labeling schemes; claim-source linkage and provenance models; treatment of document-date-vs-event-date ambiguity; human-validation protocols.

### 4.5 S5 — Hawkes and temporal event modeling
Eligible per the relevance gate in §5 below.

### 4.6 S6 — Network, game theory, counterfactual history
Eligible: methodology for representing actor/relation uncertainty in historical networks; strategic-interaction modeling with explicit payoff provenance; counterfactual-identification frameworks bounding what can and cannot be inferred from historical "what if" scenarios; critiques of arbitrary payoff assignment or unsupported equilibrium claims in historical game theory.

---

## 5. Hawkes Relevance Gate (S5, RQ5/RQ6)

```math
H_i^{\mathrm{relevant}}=\mathbf 1\left(\sum_{k=1}^{9}h_{ik}\ge1\right),
```

where the nine features `h_{i1},\dots,h_{i9}` are: (1) coarse or interval-censored timestamps; (2) tied timestamps; (3) sparse event sequences; (4) observation-process distortion; (5) simulation recovery; (6) exact-null construction; (7) branching-ratio identifiability; (8) uncertainty calibration; (9) model comparison under boundary parameters.

This is a **relevance gate only** — `H_i^{relevant}=1` means the study is in-scope for extraction under S5, not that the study's conclusions are endorsed or that a historical Hawkes fit is authorized. No historical Hawkes fit is authorized by this review, consistent with Model 3B's closed V1 status (`FAILED_VALIDATION` / `RESEARCH_ONLY` / `INFERENCE_NOT_AUTHORIZED`).

---

## 6. Exclusion Reason Taxonomy (recorded at full-text stage)

```text
EXCL_NO_POPULATION_MATCH        - P(r)=0
EXCL_NO_METHOD_MATCH            - M(r)=0
EXCL_INSUFFICIENT_EVIDENCE      - E(r)=0, full text inaccessible or insufficient for extraction
EXCL_DUPLICATE                  - exact or adjudicated-fuzzy duplicate of an already-included record
EXCL_WRONG_PUBLICATION_TYPE     - e.g., conference abstract with no accompanying paper, editorial with no substantive content
EXCL_LANGUAGE_NOT_PROCESSABLE   - full text in a language the review team cannot read or reliably machine-assist, disclosed explicitly per record
```

Every exclusion at full-text stage records exactly one of these reasons (mutually interpretable, per protocol §9); no record is excluded with an unexplained or catch-all reason.
