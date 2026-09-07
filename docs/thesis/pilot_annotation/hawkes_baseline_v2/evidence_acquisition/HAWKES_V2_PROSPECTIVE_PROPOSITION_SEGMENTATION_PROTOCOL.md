# HAWKES V2 — PROSPECTIVE PROPOSITION-SEGMENTATION PROTOCOL

WP-E10. This protocol is prospective only. It does **not** retrospectively
alter the prior finding:

```
D1^prior = NOT_EVALUABLE
```

That finding stands regardless of whether the protocol below is complete,
because no proposition-segmentation rule existed when the prior epistemic
ledger was built, and this operation does not retroactively apply one to it.

## 1. Definition

A **proposition** is the smallest independently typeable claim that can
change truth or epistemic status without necessarily changing adjacent
claims.

## 2. Design requirements and how each is met

| Requirement | Design resolution |
|---|---|
| Sentence boundaries are not automatically proposition boundaries | A single sentence containing a claim plus its evidentiary basis (e.g. "X is true because Y") segments into two propositions: the claim and the evidentiary basis, each independently typeable (e.g. claim = `AGENT_HYPOTHESIS`, basis = `REPOSITORY_FACT`) |
| Formulas and their interpretations may be separate propositions | A formula (e.g. `G_ontology = 1[M1=...=M5=1]`) is one proposition (`COMPUTED_DESCRIPTION` of a definition); a stated numeric or categorical *value* of that formula in a specific instance is a second, separate proposition |
| Compound claims must be separable | A claim of the form "A and B" segments into two propositions only if A and B could independently be found true/false without affecting the other's truth value; if A's truth is a precondition for B's meaningfulness (not just its truth), they remain one compound proposition with a noted internal dependency |
| Quotations and analyst assertions must remain distinct | A quoted source excerpt is typed `SOURCE_REPORTED_CLAIM` (or `PHILOLOGICAL_READING` if translated/interpreted); the analyst's assertion *about* that quotation is a separate proposition typed `AGENT_HYPOTHESIS`, `HISTORIAN_INTERPRETATION`, or `COMPUTED_DESCRIPTION` as appropriate — never merged into one typed unit |
| Row-level CSV claims must define their unit | For any CSV ledger, the unit is declared explicitly per file (e.g. "one row = one mechanism" for the mechanism register; "one row = one hypothesis" for the DEDUP-06 matrix); a row containing multiple columns is NOT automatically one proposition per column — columns that jointly describe one claim (e.g. `mechanism` + `current_status`) may be one proposition, while columns describing genuinely independent claims (e.g. `supporting_evidence` vs `contradicting_evidence`) are separate propositions |
| Deterministic segmentation examples must be included | See Section 3 below |
| Ambiguous cases must enter an adjudication queue | See Section 4 below |
| Inter-reviewer disagreement must remain categorical | Disagreement is recorded as `{reviewer_1_type, reviewer_2_type, agreement: YES/NO}`, never averaged, scored, or converted into a probability of correctness, unless a separately authorized reliability study with its own justified numerical domain is later commissioned |

## 3. Deterministic segmentation examples

**Example 1** (from the master report, Section 9, blue-team paragraph):
> "The gate matrix is unambiguous at 0 PASS / 1 FAIL / 9 NOT_EVALUABLE; the one FAIL (R-O4/DEDUP-06) is a demonstrated contradiction, not a close call"

Segments into:
```
p1: "0 PASS / 1 FAIL / 9 NOT_EVALUABLE" — type COMPUTED_DESCRIPTION (a stated tally)
p2: "R-O4/DEDUP-06 is a demonstrated contradiction" — type REPOSITORY_FACT
p3: "[this] is not a close call" — type AGENT_HYPOTHESIS (an analyst characterization of p2)
```

**Example 2** (from the mechanism register, MEC-02 row):
> "Five independently corroborated regime-shift episodes ... cross-checked against primary sources in closed memory workstreams."

Segments into:
```
p1: "Five ... regime-shift episodes [are documented]" — type SOURCE_SUPPORTED_CLAIM
p2: "[they were] cross-checked against primary sources in closed memory workstreams" — type REPOSITORY_FACT (a provenance statement about p1, not part of p1 itself)
```

## 4. Ambiguity-adjudication queue (design)

An item enters the queue when segmentation itself is contested — e.g. when
it is unclear whether a compound sentence expresses one claim with two
supporting clauses, or two independently falsifiable claims. Queue entries
record: `{document, locator, candidate_segmentations (>=2), reviewer_notes,
researcher_decision}`. No default resolution rule is specified — genuinely
ambiguous cases require researcher adjudication, not an automatic
tie-breaker.

## 5. Prospective readiness gate

```
G_seg^prospective = 1[ rule=1 AND examples=1 AND ambiguity_policy=1 AND researcher_acceptance=1 ]
```

```
rule              = 1 (Section 1-2 above)
examples          = 1 (Section 3 above)
ambiguity_policy  = 1 (Section 4 above)
researcher_acceptance = 0 (not yet obtained — this document is a proposal, pending Checkpoint 1 adjudication)

G_seg^prospective = 0   (blocked solely on researcher_acceptance)
```

## 6. Explicit non-retroactivity statement

Even if `G_seg^prospective` reaches 1 upon researcher acceptance, this does
**not** change the historical finding `D1^prior = NOT_EVALUABLE`. Applying
this protocol retrospectively to the already-produced epistemic-object
ledger would require a new, separately authorized operation that
re-segments and re-types the prior ledger's source documents from scratch
— not a reinterpretation of the existing file-level ledger under the new
rule.
