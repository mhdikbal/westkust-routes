# OD-005 Specification-Clarification Review

> **Status: REVIEW ARTIFACT.** Not an amendment, not a final adjudication. No change to `WAVE_2_OPEN_DECISION_LEDGER.csv`, any frozen V2 spec, any NUM-DEC document, or `WAVE_2_OD_005_DRAFT_ADJUDICATION.md` is made or implied by this document. Authoritative baseline: `9da3d9fec04341e5fb71ecb934b8acdc59f7d044`.

## 1. Clarification identity

`clarification_id: CLARIFY-OD-005-01`
`decision_id: OD-005`
Source: `WAVE_2_OD_005_DRAFT_ADJUDICATION.md` §13 ("Required specification clarification").

## 2. Exact clarification question (verbatim from the frozen draft)

> "Whether `OPT-005-B` should be formally retired from the ledger's `candidate_options` field (leaving `OPT-005-A` as the sole live candidate) or replaced with a concretely-named alternative formula for future evaluation."

Cross-checked against `WAVE_2_OPEN_DECISION_LEDGER.csv` row `OD-005`: `candidate_options` = "`AbsBias_c` as proposed; a different exact-null-specific metric; `RelBias` with a regularized denominator (rejected in spec S8.4 discussion)." The draft's framing is consistent with the ledger — `OPT-005-B` ("a different exact-null-specific metric") is exactly the ledger's second listed candidate, named without a formula. No inconsistency found between draft and ledger.

## 3. Relevant mathematical object

`AbsBias_c` — no formula is at stake for `OPT-005-B` itself, since none has ever been proposed. The clarification is about **ledger/candidate-set hygiene**, not about a mathematical definition.

## 4. Authoritative source paths consulted

| Source | Relevant content |
|---|---|
| `WAVE_2_OPEN_DECISION_LEDGER.csv`, row `OD-005` | `candidate_options` field, `notes` field (empty — no governing rule for unnamed placeholders recorded) |
| `WAVE_2_MATHEMATICAL_CONTRACT.md` §S2.3 | Writes `AbsBias_c` and `RelBias_c` formulas; explicitly marks `AbsBias_c` as "a *candidate*, not yet adopted (`OD-005`, `OPEN_REQUIRES_ADJUDICATION`)" — no mention of `OPT-005-B` or any alternative formula |
| `WAVE_2_MATHEMATICAL_CONTRACT.md` §S2.2, §S8.7 (acceptance-criterion registry, row `AC-M2-03`) | `threshold_status=OPEN_REQUIRES_ADJUDICATION`, `threshold_value=NULL`, `options_rejected="none (OD-005)"` — confirms no formula for `OPT-005-B` exists anywhere in the frozen contract |
| `WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv`, row `OD-005,OPT-005-B` | `mathematical_consequence`, `implementation_consequence`, `calibration_consequence` all recorded as `undefined -- no formula has been proposed`; `silent_default_risk = high`; explicit note: "review should determine whether it should be retired ... or replaced with a named formula" — this is the evidence package's own framing, already carried into the draft verbatim |
| `MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md`, `MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md`, `MODEL_3B_NUM_DEC_03_M2_EXACT_NULL_ADJUDICATION.md` | Govern the metric-bearing denominator and profile-likelihood/exact-null contract `AbsBias_c` inherits — none of the three discusses candidate-set housekeeping for undefined options |
| `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`, `MODEL_3B_V2_NUMERICAL_DECISION_DIGEST.md` | Reviewed; contain no policy statement on retiring vs. concretizing a ledger candidate option that lacks a formula |
| `WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv`, rows `REQ-M2-005`, `REQ-M2-008` | Confirm `REQ-M2-005` traces to `WAVE_2_PLANNING_INSTRUCTIONS.md` §S8.3–8.4 and the frozen V2 spec — no candidate-set-hygiene rule found there either |
| `docs/thesis/colab/model3b_spec_validator/` (Wave 1 validation contract: `parser.py`, `schema_validator.py`, `applicability_validator.py`) | Reviewed; these enforce structural/schema validity of frozen artifacts (no blank required fields, no duplicate IDs, correct enum usage) but contain no rule governing whether a *candidate option value* inside a field must itself resolve to a concrete formula. The validators would not flag `OPT-005-B`'s text as a schema violation — it is a syntactically valid string in the `candidate_options` field, just semantically unresolved |

## 5. Explicit statements found

None. No frozen source anywhere states a general or specific policy for handling a named-but-formula-less candidate option in the ledger's `candidate_options` field.

## 6. Implied statements found

- The evidence-to-option matrix's own risk assessment (`silent_default_risk = high`) implies that leaving `OPT-005-B` in its current unnamed form is undesirable, because it "risks a future silent, undocumented choice of an unreviewed metric." This is an *implied* methodological concern, not an explicit contract for which of the two remedies (retire vs. concretize) to apply.
- The general pattern visible across other Model 3B V2 governance documents (e.g. the original Wave 2 planning instruction's own prohibition, referenced in prior milestone work this session, against generic `TBD`/`UNKNOWN`/`PENDING` values without a governing decision reference) is suggestive by analogy that vague placeholders are disfavored project-wide — but this pattern was established for a *different* artifact (the V2 gate specification's `threshold_status` column), not for the open-decision ledger's `candidate_options` field, and does not itself specify which of the two remedies to apply here.

## 7. Conflict count

**0.** No source contradicts another on this question — the absence of an explicit rule is uniform across every source consulted, not a disagreement between sources.

## 8. Ambiguity count

**1.** The single ambiguity is: which of the two named remedies (retire `OPT-005-B`, or replace it with a concretely-named formula) should be applied, and no frozen source resolves that choice.

## 9. New numerical decision required?

**No.** Neither remedy (retiring an option, or naming a new option) requires selecting a threshold, tolerance, replication count, or any other numeric value. If a concrete replacement formula were later proposed, *that* formula might eventually require its own numerical decisions (e.g. a threshold on it) — but that is a separate, downstream, not-yet-triggered question, not part of this clarification.

## 10. Implementation evidence required?

**No.** Whether `OPT-005-B` is retired or renamed does not depend on any implementation behavior.

## 11. Calibration evidence required?

**No.** Neither remedy requires running a simulation, benchmark, or calibration procedure.

## 12. Primary classification

## `C. ADDITIVE_NONNUMERICAL_AMENDMENT_REQUIRED`

**Source chain supporting this classification:**

```text
source path: WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv, row OD-005/OPT-005-B
  → section/row: silent_default_risk field
    → explicit statement: "leaving this option open without a concrete formula
      risks a future silent, undocumented choice of an unreviewed metric"
      → mathematical consequence: none (no formula exists to have one)
        → clarification classification: C — the methodological *intent* (avoid an
          ambiguous, uncited placeholder surviving into implementation) is clear
          and explicitly stated in the evidence package, but no frozen source
          states the contract for HOW to resolve it (retire vs. concretize); a
          non-numerical additive amendment to the ledger's candidate_options
          field is required to close the ambiguity, and closing it does not
          require any numeric value, implementation behavior, or calibration
          result
```

This does not qualify as **B** (`RESOLVABLE_BY_CROSS_DOCUMENT_RECONCILIATION`) because no combination of frozen sources deterministically implies *which* of the two remedies to choose — cross-referencing the sources only confirms the ambiguity exists, it does not resolve it. It does not qualify as **A** because no source states the answer explicitly. It is not **D/E/F** because closure requires neither a numeric value, implementation evidence, nor calibration evidence.

## 13. Secondary dependencies

- Downstream: `AC-M2-03` (acceptance-criterion registry row for the exact-null bias metric) currently reads `threshold_status=OPEN_REQUIRES_ADJUDICATION`, `options_rejected="none (OD-005)"` — an eventual amendment to `OD-005`'s candidate set would need to keep this row's `options_rejected`/`notes` fields synchronized, but that synchronization is itself non-numerical.
- Upstream: none — this clarification does not depend on any other open decision.

## 14. Recommended next action

Prepare a narrowly-scoped, non-numerical additive amendment proposal for `OD-005`'s `candidate_options` field in `WAVE_2_OPEN_DECISION_LEDGER.csv`, choosing explicitly between: (a) retiring `OPT-005-B`, leaving `OPT-005-A` (`AbsBias_c`) as the sole live candidate, or (b) replacing `OPT-005-B`'s text with a concretely-named formula for future evaluation. This recommendation is **not** an amendment — it identifies the next authorizable step, per the user's own stated intent ("jika membutuhkan amendment nonnumerik, kita buat rencana amendment aditif lebih dahulu").

This recommendation is additively resolved by WAVE_2_OD_005_RETIREMENT_REVIEW_DECISION_DRAFT.md (outcome: APPROVED_WITH_LIMITATIONS_TO_RETIRE) and, at execution time, by WAVE_2_OD_005_EXACT_AMENDMENT_EXECUTION_SPECIFICATION.md. Retirement removes no existing requirement or test obligation; the eight OD005-AMD-001 through OD005-AMD-008 future tests remain PLANNED_ONLY until separately authorized execution.

## 15. Prohibited interpretation

Do not treat this review as having already retired `OPT-005-B` or selected `AbsBias_c` as final. Do not treat the evidence package's "high silent-default risk" note as itself constituting an explicit frozen-source resolution — it is a risk observation, not a contract. Do not use this review to modify the ledger, the draft, or any frozen artifact.

```text
OD-005 clarification status: C — ADDITIVE_NONNUMERICAL_AMENDMENT_REQUIRED
OD-005 final decision: WITHHELD (unchanged)
```
