# SLR — Search-String Remediation Plan (C1–C6)

**Status:** REMEDIATION PLAN ONLY. No search string is executed or frozen by this document. This plan specifies what remediation each of the six families needs; it does not perform that remediation, and it does not change `SLR_SEARCH_STRING_REGISTRY.csv` or `SLR_SEARCH_STRING_AUDIT_MATRIX.csv`.

---

## 1. Current State (unchanged, restated from the pre-freeze audit)

For every family `c ∈ {C1,...,C6}`:

```math
K_c=H_c=X_c=1,\qquad V_c=P_c=F_c=B_c=0.
```

Therefore:

```math
G_c^{\mathrm{string}}=0 \quad\forall c,\qquad G_C^{\mathrm{string}}=\prod_{c=1}^{6}G_c^{\mathrm{string}}=0.
```

Core concept terms (`K_c`), humanities context terms (`H_c`), and zero-execution (`X_c`) are already satisfied for all six families. This plan addresses only the four missing components: `V_c`, `P_c`, `F_c`, `B_c`.

---

## 2. Remediation Items Required for Every Family (C1 through C6)

### 2.1 Lexical and spelling variants
Identify and document alternate spellings, transliterations, and orthographic variants for every core and context term (e.g., British vs. American spelling; "hermeneutics" has no major variant, but "colonialism/colonialisation/colonisation" does; VOC-related terms may appear as "Vereenigde Oostindische Compagnie," "Dutch East India Company," or archaic Dutch spellings).

### 2.2 Hyphenation variants
Document hyphenated vs. unhyphenated vs. spaced forms (e.g., "self-exciting" vs. "self exciting"; "point-process" vs. "point process"; "game-theoretic" vs. "game theoretic").

### 2.3 Approved language variants (per SLR-DEC-02, now adjudicated)
For each family, draft equivalent term sets in Dutch, German, French, and Indonesian where a database's syntax and the review's language scope (English, Dutch, German, French, Indonesian — `ADJUDICATED_APPROVED_WITH_LIMITATIONS`) make this useful. Not every family needs every language — e.g., C5 (Hawkes/point-process terminology) is overwhelmingly English/international-mathematical-notation; C3 (colonial archive criticism) and C6 (VOC-context network/game-theory) most need Dutch-language terms.

### 2.4 Controlled vocabulary
Check each family's core terms against the controlled subject-heading vocabularies of the sources most likely to be approved in Wave B (e.g., Library of Congress Subject Headings, JSTOR's own thesaurus if any, ACM Computing Classification System for C2/C4) so that database-native subject search can supplement free-text search.

### 2.5 Provider-specific syntax translation
Translate the family's boolean template into the exact query syntax of each candidate database once SLR-DEC-05 is adjudicated — e.g., Scopus `TITLE-ABS-KEY(...)`, Web of Science `TS=(...)`, JSTOR's field-restricted search operators, ACM Digital Library's query builder syntax, arXiv's `abs:`/`ti:` field prefixes. This item is explicitly sequenced **after** SLR-DEC-05, since it cannot be written against an unconfirmed source set.

### 2.6 Filter rationale
For each family, state explicitly which filters (date, document type, language) will be applied at the database level versus screened manually, and why — grounded in the now-adjudicated SLR-DEC-02 (language), SLR-DEC-03 (temporal), and SLR-DEC-04 (publication-type) decisions. No filter may be added without being traceable to one of these three adjudicated decisions.

### 2.7 Breadth risk
Document, per family, which terms are broad enough to generate high false-positive volume (e.g., "ambiguity," "network," "interpretation," "silence" are all generic English words with large unrelated literatures) and what secondary filtering (subject-area restriction, co-occurrence with a context term) mitigates this.

### 2.8 Narrowness risk
Document, per family, which terms might be too narrow or too specific to this project's own vocabulary (e.g., "computational hermeneutics" itself is a relatively rare exact phrase; over-reliance on it risks missing adjacent literature that uses different terminology for the same concept, such as "critical digital humanities" or "algorithmic reading").

---

## 3. Per-Family Remediation Focus

| Family | Primary remediation focus | Rationale |
|---|---|---|
| C1 (computational hermeneutics) | Narrowness risk (2.8) is the dominant concern — "computational hermeneutics" is a niche exact phrase; must draft adjacent-terminology variants (e.g. "critical digital humanities," "algorithmic reading," "AI and interpretation") to avoid missing the broader literature | S1 is the domain most likely to be under-retrieved by literal phrase-matching alone |
| C2 (digital/computational history) | Breadth risk (2.7) — "digital history," "distant reading" are established but broad terms with large adjacent literatures (e.g. general digital-collections scholarship with no methodological content) | requires precise co-occurrence filtering with methodological terms |
| C3 (colonial archive criticism) | Language variants (2.3) — much foundational archival-criticism scholarship on VOC/Dutch colonial archives is published in Dutch | highest-priority family for Dutch-language term development |
| C4 (historical NLP/provenance) | Controlled vocabulary (2.4) and provider syntax (2.5) — this is the most technical/CS-adjacent family, likely to benefit most from ACM/IEEE classification alignment | |
| C5 (Hawkes/temporal modeling) | Lexical/spelling variants (2.1) and hyphenation (2.2) — mathematical/statistical terminology has many stylistic variants across statistics vs. CS vs. physics literatures publishing on point processes | must ensure recall across disciplinary silos that use different conventions for the same concept |
| C6 (network/game theory/counterfactual) | Both breadth (2.7: "game theory," "network" are enormous generic literatures) and language variants (2.3: VOC/colonial-Indonesia context needs Dutch terms) | most demanding family, needs the most work before freeze |

---

## 4. Success Gate for Remediation (to be evaluated, not asserted, once remediation is done)

```math
G_c^{\mathrm{string}}=\mathbf 1[K_c=H_c=V_c=P_c=F_c=B_c=X_c=1].
```

Remediation for family `c` is complete only when all seven components are independently `1`. Remediation does not itself set `G_c^{string}=1` — a subsequent audit turn must verify each component against the updated registry before the gate value is asserted, consistent with the pre-freeze audit's explicit refusal to set the gate to `1` merely because text exists.

```math
G_C^{\mathrm{string}}=\prod_{c=1}^{6}G_c^{\mathrm{string}}.
```

`G_C^{string}` remains `0` until all six families independently reach `G_c^{string}=1`.

---

## 5. Stop Condition for This Remediation Work

Remediation must stop and require researcher review if:
- a lexical/language variant would require inventing a term not attested in any dictionary, glossary, or existing scholarly usage;
- provider-syntax translation is attempted before SLR-DEC-05 is adjudicated (out of sequence);
- a filter is added that cannot be traced to SLR-DEC-02, 03, or 04;
- any test query is executed against a live database during remediation drafting.

---

## 6. Explicit Non-Execution Status

```text
C1: NOT_EXECUTED
C2: NOT_EXECUTED
C3: NOT_EXECUTED
C4: NOT_EXECUTED
C5: NOT_EXECUTED
C6: NOT_EXECUTED
```

This plan specifies *what* remediation work is needed; it performs none of it. Actual remediation (populating `V_c, P_c, F_c, B_c` in the registry) is the next work item in Wave B, sequenced as: complete 2.1–2.4 and 2.6–2.8 first (source-independent), then 2.5 (provider syntax) only after SLR-DEC-05 is adjudicated.

---

## 7. Remediation Executed This Turn (appended additively)

**Provenance:** appended after §1-6 above (unmodified) following the Wave B1 documentation-remediation turn. This section records what was actually produced, in four new artifacts, none of which executes or freezes a search:

```text
SLR_SEARCH_TERM_VARIANT_REGISTRY.csv        (59 term rows, 6 families, 5 languages: en/nl/de/fr/id)
SLR_PROVIDER_QUERY_TRANSLATION_MATRIX.csv    (78 rows = 6 families x 13 sources, 42 applicable + 36 NOT_APPLICABLE)
SLR_SEARCH_STRING_RISK_REGISTER.csv          (20 risk rows; every family has >=1 broadness AND >=1 narrowness risk)
SLR_SEARCH_STRING_REMEDIATION_AUDIT.md       (gate recomputation)
```

### 7.1 Filter Contract (`F_c`) — documented per family, grounded in adjudicated Wave A decisions

For filter `f` in family `c`: `A_cf^filter = 1[J_cf=1 ∧ R_cf=1 ∧ E_cf=1]` (methodological justification, recall consequence, exclusion-bias risk). Three filter types apply uniformly across all six families, each traceable to an already-adjudicated Wave A decision — no filter here has independent, unprovenanced justification:

```text
LANGUAGE_FILTER (all C1-C6):
  J_cf: per SLR-DEC-02 (ADJUDICATED_APPROVED_WITH_LIMITATIONS) - English/Dutch/German/French/Indonesian,
        no English-only exclusion at screening.
  R_cf: applying this at the DATABASE level (not the screening level) risks under-recall wherever a
        source's own language-filter UI does not cleanly separate these five languages; therefore this
        filter is NOT applied as a hard database-level exclusion - it governs which language-variant terms
        are searched (per SLR_SEARCH_TERM_VARIANT_REGISTRY.csv) and how screening decisions are made,
        not which records a database returns.
  E_cf: excluding a database result by language is explicitly PROHIBITED at title/abstract screening,
        per SLR-DEC-02; full-text inclusion is conditional on documented competence/translation support only.
  Status: DRAFT_NOT_FROZEN, NOT_EXECUTED. A_cf^filter = 1 (all three components documented).

TEMPORAL_FILTER (all C1-C6):
  J_cf: per SLR-DEC-03 (ADJUDICATED_APPROVED_WITH_LIMITATIONS) - METHOD_SPECIFIC_DATE_WINDOWS,
        NO_LOWER_DATE_LIMIT as the default for every family; no upper limit.
  R_cf: since no lower/upper bound is actually applied, there is no recall loss from this filter -
        it is a documented EXPECTATION about evidence clustering (e.g. C5/Hawkes literature clusters
        post-1971), not an applied cutoff.
  E_cf: no exclusion-bias risk, since nothing is excluded by date.
  Status: DRAFT_NOT_FROZEN, NOT_EXECUTED. A_cf^filter = 1.

PUBLICATION_TYPE_FILTER (all C1-C6):
  J_cf: per SLR-DEC-04 (ADJUDICATED_APPROVED_WITH_LIMITATIONS) - all types including theses/grey
        literature included; software/method documentation and editorials included only if they pass
        M(r)=1 and E(r)=1 at full-text stage.
  R_cf: excluding theses/preprints/grey literature by default would risk exactly the failure mode already
        observed in this project's own S1-B1 execution (ET-10's most load-bearing candidate was an
        unpublished 1965 PhD thesis, not a journal article) - so no such exclusion is applied.
  E_cf: publication type is flagged in extraction (EXT-01) for synthesis transparency, but is never
        used as an inclusion/exclusion gate or a quality proxy.
  Status: DRAFT_NOT_FROZEN, NOT_EXECUTED. A_cf^filter = 1.
```

No universal lower publication date is introduced. Language is never used as an English-only exclusion gate. Publication type is never treated as a quality score. All three filter types remain `DRAFT_NOT_FROZEN`/`NOT_EXECUTED`.

### 7.2 Updated Component States

```math
K_c=H_c=X_c=1 \text{ (unchanged)}
```
```math
V_c=1 \text{ (SLR\_SEARCH\_TERM\_VARIANT\_REGISTRY.csv exists, complete for review, per family)}
```
```math
P_c=1 \text{ (SLR\_PROVIDER\_QUERY\_TRANSLATION\_MATRIX.csv exists, explicitly pending verification per source - satisfies the gate's "complete OR explicitly pending verification per source" clause)}
```
```math
F_c=1 \text{ (\S7.1 above, all three filter types documented and provenanced)}
```
```math
B_c=1 \text{ (SLR\_SEARCH\_STRING\_RISK\_REGISTER.csv - every family has} \ge 1 \text{ broadness and} \ge 1 \text{ narrowness risk)}
```

```math
G_c^{\mathrm{remediation}}=\mathbf 1[K_c=H_c=V_c=P_c=F_c=B_c=X_c=1]=1 \quad \forall c\in\{1,\dots,6\}.
```
```math
G_C^{\mathrm{remediation}}=\prod_{c=1}^{6}G_c^{\mathrm{remediation}}=1.
```

**This does not set `SLR-DEC-06` to approved, and it does not authorize search execution.** It means the documentation evidence is now complete enough for SLR-DEC-06 to be adjudicated in a later, separate turn — after the still-pending controlled verification of the 13 candidate sources (SLR-DEC-05), since several `P_c` entries explicitly depend on that verification before any provider syntax can move from `PROVIDER_SYNTAX_REQUIRES_VERIFICATION` to confirmed.
