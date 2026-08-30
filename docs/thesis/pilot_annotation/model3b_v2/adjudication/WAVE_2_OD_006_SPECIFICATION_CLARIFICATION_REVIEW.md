# OD-006 Specification-Clarification Review

> **Status: REVIEW ARTIFACT.** Not an amendment, not a final adjudication. No change to `WAVE_2_OPEN_DECISION_LEDGER.csv`, any frozen V2 spec, any NUM-DEC document, or `WAVE_2_OD_006_DRAFT_ADJUDICATION.md` is made or implied by this document. Authoritative baseline: `9da3d9fec04341e5fb71ecb934b8acdc59f7d044`.

## 1. Clarification identity

`clarification_id: CLARIFY-OD-006-01`
`decision_id: OD-006`
Source: `WAVE_2_OD_006_DRAFT_ADJUDICATION.md` §13 ("Required specification clarification").

## 2. Exact clarification question (verbatim from the frozen draft)

> "Whether `OPT-006-B`, if ultimately adopted, requires the `NUM-DEC-02` target band to be formally re-derived/reinterpreted as a separate, explicitly-authorized specification-amendment turn (analogous to the earlier `NUM-DEC` amendment pattern used elsewhere in this project), rather than assumed to carry over unchanged."

Cross-checked against `WAVE_2_OPEN_DECISION_LEDGER.csv` row `OD-006`: topic = "Primary M2 coverage metric: `Coverage_c` vs `CoverAndValid_c`"; `notes` field records "instruction requires checking against NUM-DEC and frozen spec before adopting a new primary metric (S8.7)" and "cross-check against NUM-DEC-01/02's own metric-denominator language." The draft's clarification is a direct, faithful specialization of this ledger note — no inconsistency found.

## 3. Relevant mathematical object

`Coverage_c` (`OPT-006-A`) and `CoverAndValid_c` (`OPT-006-B`), and the frozen `GATE-021-V2` acceptance band that currently governs coverage evaluation.

## 4. Authoritative source paths consulted

| Source | Relevant content |
|---|---|
| `WAVE_2_OPEN_DECISION_LEDGER.csv`, row `OD-006` | Confirms the ledger's own note already directs a cross-check against `NUM-DEC-01`/`NUM-DEC-02` before adopting a new primary metric |
| `WAVE_2_MATHEMATICAL_CONTRACT.md` §S2.6, and acceptance-criterion row `AC-M2-02` | Writes both `Coverage_c` and `CoverAndValid_c` formulas verbatim; states "Which is primary = `OD-006`, `OPEN_REQUIRES_ADJUDICATION` — no new primary metric may be adopted without an explicit NUM-DEC/spec cross-check"; `AC-M2-02` row: `threshold_status=OPEN_REQUIRES_ADJUDICATION`, `threshold_value=NULL`, denominator explicitly listed as "`R_valid` or `R_attempted`" (both, unresolved) |
| **`MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md`, line 183** | **Explicit statement, quoted directly**: *"`NUM-DEC-02` does not alter this threshold (`GATE-021-V2` `threshold: between 0.925 and 0.975`). It selects only the method used to construct and validate uncertainty for `n`."* This is the single most load-bearing sentence for this clarification — see §12 below. |
| `MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md`, SS11/SS18/SS19 | Writes `Coverage_hat = (1/R_metric) * sum over valid metric-bearing replications of I[n_true in CI_b]` — mathematically identical in form to `OPT-006-A` (`Coverage_c`, valid-denominator) — and freezes the `0.925`–`0.975` target band under that convention |
| `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`, row `GATE-021-V2` | Confirms `ci_coverage_95pct` threshold `0.925`–`0.975` is frozen and currently `"Blocked on NUM-DEC-02 (M2 uncertainty method)"` |
| `MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md` | Establishes `R_valid,c`/`R_attempted,c`/`FailureRate_c` joint-bookkeeping requirement, independent of which coverage metric is adopted |
| **Project-wide governance pattern, observed across all 8 `NUM-DEC` documents and both amendment rounds this session** | Every single `NUM-DEC` decision text explicitly and uniformly states what it does *not* decide, and requires a separately-authorized turn for anything adjacent (e.g. `NUM-DEC-05`: "does not select marginal-likelihood method (`NUM-DEC-06`) or threshold tau (`NUM-DEC-04`)"; `NUM-DEC-06`: "does not select tau"; `NUM-DEC-04`: "a separate researcher decision selects the final value"). `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` states the same principle generally: *"This manifest design ... enable[s] a future, **separately authorized** implementation wave ... They do **not** authorize [it]."* This is not an isolated statement but the single most consistently-applied structural convention across every governance document produced in this project to date — a document-wide norm, not an isolated inference. |
| `WAVE_2_OD_005_006_015_EVIDENCE_LEDGER.csv`, `WAVE_2_OD_005_006_015_MATHEMATICAL_EVIDENCE_REVIEW.md` (E-002, Pawel et al. 2025) | Supplies the methodological *reason* a denominator change might be needed (informative-failure caution) but does not itself speak to project governance procedure — kept separate from the procedural question analyzed here |

## 5. Explicit statements found

1. `NUM-DEC-02` line 183: its own decision explicitly does **not** alter `GATE-021-V2`'s threshold — it only selects the uncertainty *method*, under an implicit assumption (visible in SS11/SS18) that the metric backing the band is the valid-denominator `Coverage_hat` form.
2. `WAVE_2_MATHEMATICAL_CONTRACT.md` §S2.6: "no new primary metric may be adopted without an explicit `NUM-DEC`/spec cross-check" — an explicit procedural gate on adopting either coverage option as primary.
3. Every `NUM-DEC` document in the ledger explicitly disclaims authority over anything beyond its own narrow selected scope, and directs successor questions to "a separate researcher decision" / "a future adjudication turn" / "not authorized here."

## 6. Implied statements found

- That `NUM-DEC-02`'s `0.925`–`0.975` band was frozen *specifically* under the valid-denominator (`Coverage_c`/`OPT-006-A`-form) convention is not stated as a single explicit sentence anywhere — it follows from combining (a) the formula match between `Coverage_hat` (SS11) and `Coverage_c` (§S2.6), and (b) the fact that `CoverAndValid_c` did not exist as a named alternative at the time `NUM-DEC-02` was adjudicated (it enters the record only via `OD-006`, raised afterward). This is an *implied*, not explicit, historical fact — but it is not in dispute; no source contradicts it.

## 7. Conflict count

**0.**

## 8. Ambiguity count

**0** for the procedural question itself (does adopting `OPT-006-B` require a separate amendment turn — see §12). **1** remains, but it is explicitly *outside* this clarification's scope and already correctly flagged as such by the draft itself (§14 of `WAVE_2_OD_006_DRAFT_ADJUDICATION.md`): whether M2's actual future failure modes are informative — that is a distinct, `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` question, not part of `CLARIFY-OD-006-01`.

## 9. New numerical decision required?

**No.** The clarification is purely procedural (does closure require a separate turn, yes/no) — it does not itself select `OPT-006-A` or `OPT-006-B`, nor any threshold value.

## 10. Implementation evidence required?

**No**, for this specific clarification. (The separate, already-disclosed `OD-006` implementation-dependent component — whether M2's failure modes are informative — is a different question; see §8.)

## 11. Calibration evidence required?

**No.**

## 12. Primary classification

## `B. RESOLVABLE_BY_CROSS_DOCUMENT_RECONCILIATION`

**Source chain supporting this classification:**

```text
source path: MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md, line 183
  → section/row: threshold-preservation statement
    → explicit statement: "NUM-DEC-02 does not alter this threshold ... It
      selects only the method used to construct and validate uncertainty for n"
      → mathematical consequence: the 0.925-0.975 band's validity is tied to
        the specific metric form NUM-DEC-02's own text assumed (Coverage_hat,
        SS11, structurally identical to Coverage_c/OPT-006-A) -- NUM-DEC-02
        never considered or authorized CoverAndValid_c

combined deterministically with:

source path: every NUM-DEC document (01 through 08) + WAVE_2_EXECUTION_
  MANIFEST_AND_STOP_RULES.md
  → section/row: each document's own "does not select / not authorized here /
    separate researcher decision" disclaimers (uniform pattern, zero exceptions
    found across 8 documents)
    → explicit statement: any decision adjacent to but outside a NUM-DEC's
      stated scope requires its own separately-authorized turn -- never
      assumed to carry over
      → mathematical consequence: applying this same uniformly-observed rule
        to OD-006 -- adopting OPT-006-B changes the metric's denominator
        convention, which is a change adjacent to but outside what NUM-DEC-02
        actually decided
        → clarification classification: B -- the answer ("yes, a separate
          amendment turn would be required") is not stated in one sentence
          anywhere, but follows deterministically from combining NUM-DEC-02's
          explicit self-limitation with the project's own uniformly-applied
          governance convention -- no NEW decision is added by reaching this
          conclusion; it is the same rule already governing every other
          NUM-DEC boundary, applied to this one
```

This does not qualify as **A** because no single frozen sentence states "adopting `OPT-006-B` requires a separate amendment turn" verbatim — the conclusion requires combining two sources. It is not **C** because the contract (separate authorization for anything outside a `NUM-DEC`'s stated scope) is *already* explicitly stated as a governing project-wide pattern, not merely implied intent requiring a new nonnumerical rule to be written. It is not **D/E/F** because this specific procedural sub-question requires no numeric value, implementation evidence, or calibration evidence to answer — it is answered entirely by reconciling existing frozen text.

**Important scope boundary**: this classification answers only the *procedural* question in `CLARIFY-OD-006-01` (does adoption of `OPT-006-B` require a separate amendment turn — **yes**, by cross-document reconciliation). It does **not** answer, and this review does not attempt to answer, whether `OPT-006-A` or `OPT-006-B` should ultimately be adopted — that remains `OD-006`'s separately-tracked, `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` component (§8 above), which depends on evidence about M2's actual failure-mode informativeness that does not yet exist.

## 13. Secondary dependencies

- Depends on `NUM-DEC-02`'s frozen text remaining unchanged (it is — verified in §16 of the reconciliation document).
- Downstream: if `OD-006` is ever adjudicated toward `OPT-006-B`, the recommended separate amendment turn would need to reconcile or re-derive `GATE-021-V2`'s `0.925`–`0.975` band — that re-derivation is a distinct, not-yet-authorized, likely `NUMERICAL_ADJUDICATION_REQUIRED` (classification D) future task, since re-deriving a coverage target band under a different denominator is itself a numeric-threshold question.

## 14. Recommended next action

Record, for a future adjudication turn on `OD-006`, that **if** `OPT-006-B` is ultimately selected, its adoption is procedurally gated on a separate, explicitly-authorized specification-amendment turn to reconcile `GATE-021-V2`'s frozen `0.925`–`0.975` band — this is not itself an amendment, but a documented procedural precondition ready to be cited when `OD-006`'s substantive candidate-selection question is eventually adjudicated. No amendment is created in this review.

## 15. Prohibited interpretation

Do not treat this review as having selected `OPT-006-A` or `OPT-006-B` as primary. Do not treat the classification `B` as authorizing the re-derivation of `GATE-021-V2`'s band — that re-derivation, if it becomes necessary, requires its own separate future authorization and likely a numerical decision. Do not use this review to modify `NUM-DEC-02`, the ledger, the draft, or any frozen artifact.

```text
OD-006 clarification status: B — RESOLVABLE_BY_CROSS_DOCUMENT_RECONCILIATION
  (procedural sub-question only; the substantive OPT-006-A vs OPT-006-B
  selection remains IMPLEMENTATION_DEPENDENT_FINAL_DECISION, unchanged)
OD-006 final decision: WITHHELD (unchanged)
```
