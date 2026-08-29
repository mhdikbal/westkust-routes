# Model 3B — Phase-0 Date Precision Audit: Summary

> **Manual classification pass. Read-only against `data/research/linimasa_events.csv` (unmodified). No M4 implementation, no tournament execution, no historical fitting.**

---

## Candidate identification methodology and count vs. the ~75 estimate

The original ~75/141 figure was a rough regex first pass from an earlier turn this session, never saved to a durable file. This audit regenerated the candidate set independently: a day-precision regex (`\d{1,2}\s+<Indonesian/Dutch month>\s+\d{4}`) was run against `event_date_raw` for all 141 rows, then manually filtered to exclude rows where the matched date is actually the boundary of a stated multi-day/multi-month range (e.g. `"24 Juli - 8 Agustus 1680"`, `"27 Januari - 31 Maret 1681"`) rather than a standalone single-day date.

**Final candidate count: 96** (vs. the ~75 original estimate — differs meaningfully, as expected for an independently-regenerated rough pass; not forced to match). The gap is attributable to: (a) this pass also captured day-precise dates embedded inside parenthetical report-date/correction annotations (e.g. `"(lapor 12 Okt 1636)"`), which a stricter first pass may have excluded upfront, and (b) some rows this audit classified as ranges were only caught by manual review, not the regex filter, so the true "clean single-day-looking" candidate pool the original pass saw may have been smaller.

## Classification counts (8 categories)

| Classification | Count |
|---|---|
| `EXACT_EVENT_DATE` | 67 |
| `DOCUMENT_DATE` | 10 |
| `DATE_RANGE_BOUNDARY` | 6 |
| `CANNOT_DETERMINE` | 5 |
| `EXACT_REPORT_DATE` | 4 |
| `MULTIPLE_DATES_AMBIGUOUS` | 2 |
| `ARRIVAL_OR_DEPARTURE_DATE` | 1 |
| `INFERRED_DATE` | 1 |
| **Total** | **96** |

## The number that determines M4 eligibility

**67 rows classified `EXACT_EVENT_DATE`** — well above the design doc's informal 30-40 floor for M4 eligibility.

**However, this headline number needs an explicit caveat, not a clean pass:**

```text
EXACT_EVENT_DATE by classifier confidence:
  HIGH:    13
  MEDIUM:  54
```

The 13 `HIGH`-confidence rows are grounded in an explicit dateline or direct narration visible in the excerpt (e.g. `"desen 17e Januarij... 1607"`, `"is op heeden ter vergaderinge... gearresteert"`, `"Den 1. Septembris wurde... das Fort... eingenommen"`, `"sloot Sas 15 April een soortgelijk contract"`). These are as close to source-certain as this kind of corpus gets.

The 54 `MEDIUM`-confidence rows rely on a genre-level inference — "this is a Corpus Diplomaticum-numbered treaty/deed/oath document, and such documents are conventionally dated by their own conclusion date" — rather than an explicit dateline directly visible within the 500-character `text_asli` excerpt this audit worked from (a length limit chosen for this pass, not the full field). This is a defensible starting classification, consistent with how CD-numbered instruments are conventionally read, but it is **not** the same evidentiary strength as the 13 `HIGH` rows, and this project has a documented history (recorded in session memory) of extraction claims that did not survive a full-text check.

**Recommendation, stated plainly:** if M4 is to proceed, a second pass reading the *full* (untruncated) `text_asli` for the 54 `MEDIUM`-confidence rows is warranted before treating 67 as the final, load-bearing count — not because this pass was careless, but because the 500-char excerpt genuinely could hide a mismatch of the kind found at row 76 (below). Even under a maximally conservative reading (`HIGH`-only, n=13), M4 would fall *below* the 30-40 floor and should default to `EXCLUDED_INSUFFICIENT_PRECISE_SUBSET`; under the full 67-count, M4 clears the floor comfortably. **The eligibility determination is therefore genuinely sensitive to this verification step — this audit does not manufacture false certainty either way.**

## Notable patterns worth flagging

1. **A concrete event-date/document-date mismatch was found, not merely hypothesized.** Row `idx 76` (`event_date_raw = "23 Maret 1693"`) is a treaty document with Sillibo, but its own `text_asli` narrates the actual military action — the attack on the Aceh fort at Gido — as occurring `"Den 15den Maart"` (15 March), a *different day*. The row's `event_date_raw` reflects the treaty's own date, not the day the substantive event (the attack) happened. This is exactly the failure mode Guard A exists to catch, found in the wild rather than only theorized.

2. **Two rows show the dataset's own prior "correction" overriding a primary source's stated date**, without an independently visible resolution: `idx 128` (`"16 Agustus 1781 (koreksi dari 10 Agst)"`) and `idx 129` (`"17 Agustus 1781 (koreksi dari 19 Agst)"`). For `idx 128`, the primary EIC source text itself states **"On 10 August 1781 the fleet sailed..."** — directly conflicting with the dataset's "corrected" 16 August. This audit does not resolve which date is correct (per Guard A's explicit prohibition against resolving without source review) and classifies both as `CANNOT_DETERMINE`. This is worth the researcher's separate attention regardless of Model 3B — it is a live discrepancy in `linimasa_events.csv` itself.

3. **A meaningful share of "day-precise-looking" dates are actually report/document dates, not event dates**, confirming part of the root-cause audit's temporal-handling finding at the row level, not just in aggregate: `EXACT_REPORT_DATE` (4 rows) and `DOCUMENT_DATE` (10 rows) together account for 14/96 (~15%) of all candidates — cases where a naive parser would have extracted a precise timestamp that does **not** represent when the underlying event occurred.

4. **`DATE_RANGE_BOUNDARY` (6 rows)** confirms that even after the initial regex+manual filtering pass, some range-shaped dates still slipped through as apparent single-day candidates until read closely — reinforcing that automated first-pass identification alone (the kind V1's recovery study implicitly relied on) is not a safe substitute for this manual review.

## Hard-prohibition compliance

- No date in `event_date_raw` or any other source field was altered.
- No uncertainty was replaced with an invented precise date (`CANNOT_DETERMINE`/`MULTIPLE_DATES_AMBIGUOUS`/`INFERRED_DATE` used for exactly the cases where resolution was not source-grounded — 8 rows total).
- No multi-date row was resolved by picking the first date automatically (`idx 13`, `idx 49` both classified `MULTIPLE_DATES_AMBIGUOUS`, not arbitrarily resolved).
- Document dates were not treated as event dates (10 rows explicitly separated out as `DOCUMENT_DATE`).
- `idx 128`/`idx 129`'s internal correction discrepancies were not silently resolved.

## Outputs

- `docs/thesis/pilot_annotation/MODEL_3B_PHASE0_DATE_PRECISION_LEDGER.csv` — 96 rows, full classification detail.
- This summary.

## What this audit does not do

- Does not implement M4 or any model code.
- Does not run any recovery test or historical fit.
- Does not finalize M4's eligibility status — that determination (`CONDITIONALLY_ELIGIBLE` → `ELIGIBLE` or `EXCLUDED_INSUFFICIENT_PRECISE_SUBSET`) is the design document's own next step, informed by this ledger, not decided by this audit.
- Does not resolve the `idx 128`/`idx 129` date discrepancy.

## QA Addendum (second pass, full-text verification)

Per the first pass's own recommendation, a second verification pass was performed against the FULL `text_asli` field (not the 500-char excerpt the first pass used) with 100% coverage on: all rows containing more than one date-like expression (regex + numeric-date-format scan across all 96 rows, plus manual review), all 6 `LOW`-confidence rows, all 5 `CANNOT_DETERMINE` rows, all 54 `EXACT_EVENT_DATE`/`MEDIUM` rows, and all 13 `EXACT_EVENT_DATE`/`HIGH` rows (exceeding the minimum-10-random requirement — all 13 were checked).

**Multi-date scan (100% of 96 rows):** a day+month-name regex and a numeric DD-MM-YYYY scan across full `text_asli` found exactly one mismatch — the already-known `row_76` case (event_date_raw "23 Maret 1693" vs. text's own "Den 15den Maart"). No new mismatches found elsewhere.

**54 MEDIUM `EXACT_EVENT_DATE` rows:** full text (including the tails of the 30 rows exceeding the original 400/500-char excerpt) was scanned for dateline markers (`gedaen`, `gegeven`, `actum`, `getekent`, etc.). None were found beyond what the first pass already saw. All 54 remain `MEDIUM` — confirmed, not just re-asserted, that the classification rests on genre-inference alone (CD-numbered treaty, standard conclusion-dating convention) with no directly-visible dateline anywhere in the full text.

**Reclassifications made (7 rows changed):**

| Row | Before | After | Reason |
|---|---|---|---|
| `row_54` | CANNOT_DETERMINE / LOW | EXACT_EVENT_DATE / MEDIUM | Same CD-treaty genre pattern as the 54 MEDIUM rows; original classification was inconsistent with identically-evidenced peer rows (row_5, row_14, row_15, etc.) |
| `row_92` | CANNOT_DETERMINE / LOW | EXACT_EVENT_DATE / MEDIUM | Same reasoning — CD-numbered treaty (traktat DCXCI), same genre pattern |
| `row_128` | CANNOT_DETERMINE / HIGH(ambiguity) | EXACT_EVENT_DATE / HIGH | Two independent primary sources (Harries, English side; van Kempen, Dutch side, the captured VOC resident) both converge on 16 Agustus 1781, superseding a single secondary academic source's 10 August |
| `row_129` | CANNOT_DETERMINE / HIGH(ambiguity) | MULTIPLE_DATES_AMBIGUOUS / HIGH(ambiguity) | Better fit: three distinct source-attributed day candidates (17/18/19 Aug) exist, not merely insufficient information; the row's own notes explicitly call this unresolved — left unresolved here too |
| `row_75` | EXACT_EVENT_DATE / HIGH | INFERRED_DATE / MEDIUM | Date is calculated ("sehari setelah Air Bangis" / "a day after Air Bangis"), matching the INFERRED_DATE definition, not directly stated in the row's own text. QA also found an unresolved 6-day arithmetic discrepancy against the most plausible "Air Bangis" anchor (row_74, 22 Jan) — flagged, not resolved |
| `row_82` | EXACT_EVENT_DATE / HIGH | EXACT_EVENT_DATE / MEDIUM | Date is stated relationally ("a day later" than row_81), and row_81 itself is only MEDIUM confidence — chained uncertainty caps this row at MEDIUM too. Distinguished from row_83 (same date), which independently states "op denzelfden 3den Mei" directly and correctly remains HIGH |
| `row_27` | EXACT_EVENT_DATE / HIGH (unchanged) | EXACT_EVENT_DATE / HIGH (unchanged) | Rationale only: verified this turn that row_27's inherited date (from sibling row_26, "TRAKTAT SAMA") is grounded in row_26's own genuine explicit dateline ("onderteijckent wederzijts... desen 16e Augustus 1660"), not an unverified cross-reference |

**10-row random spot-check of the original 13 HIGH rows (seed=42):** `row_107, row_18, row_1, row_36, row_82, row_83, row_75, row_80, row_110, row_116` were the random sample — coverage was then extended to all 13 (also checking `row_26, row_27, row_79` not drawn by the random sample), since two problems (`row_75`, `row_82`) surfaced during review and full coverage was judged more valuable than stopping at the minimum. Outcome: 11/13 confirmed solid as originally classified; 2/13 (`row_75`, `row_82`) required correction (above).

**Post-QA category counts (96 rows total):**

| Category | Count |
|---|---|
| EXACT_EVENT_DATE | 69 (was 67) |
| DOCUMENT_DATE | 10 |
| DATE_RANGE_BOUNDARY | 6 |
| EXACT_REPORT_DATE | 4 |
| MULTIPLE_DATES_AMBIGUOUS | 3 (was 2) |
| INFERRED_DATE | 2 (was 1) |
| CANNOT_DETERMINE | 1 (was 5) |
| ARRIVAL_OR_DEPARTURE_DATE | 1 |

**Post-QA EXACT_EVENT_DATE confidence split:** HIGH 12 (was 13), MEDIUM 57 (was 54). Total 69.

**`researcher_review_required` column added** to the ledger CSV. Rule (stated explicitly for auditability): `FALSE` only when `classification == EXACT_EVENT_DATE AND classifier_confidence == HIGH` (post-QA); `TRUE` for every other row. Result: 12 rows `FALSE`, 84 rows `TRUE`.

**M4 eligibility reading, still not decided by this document:**
- **Permissive reading (all EXACT_EVENT_DATE, n=69):** clears the ~30-40 threshold comfortably.
- **Conservative reading (HIGH-confidence only, n=12):** falls below the ~30-40 threshold — materially unchanged from the pre-QA figure of 13, since the QA pass net removed one HIGH row (row_75, reclassified out; row_82 downgraded to MEDIUM) while adding one (row_128, promoted in).
- This split is unchanged in substance by the QA pass: the underlying question — whether genre-inferred (MEDIUM) treaty dates are acceptable evidence for M4, or only directly-narrated (HIGH) dates — remains a researcher policy decision, not a data-quality question this audit can resolve further.

**Hard-prohibition compliance (QA pass):** no date in `event_date_raw`/`text_asli` was altered; no ambiguity was force-resolved (`row_129`'s three-way conflict and `row_16`'s single remaining `CANNOT_DETERMINE` were left unresolved); no date was chosen because it appeared first; document dates were not treated as event dates; the `row_75`/`row_74` arithmetic discrepancy was flagged, not silently fixed. Source CSVs (`data/research/linimasa_events.csv`, `data/export/linimasa_events.csv`) were read-only throughout — confirmed untouched via `git status`.

## Researcher Adjudication (2026-08-29) — Final

The 7 QA-approved reclassifications above are **approved as-is**. The researcher applied the **HIGH-only threshold** to the M4 eligibility question (deliberately not combining HIGH and MEDIUM to reach the sample-size floor):

```text
EXACT_EVENT_DATE total:    69
  HIGH confidence:          12
  MEDIUM confidence:        57
M4 eligible subset:        12 (HIGH-confidence exact event dates only)
M4 final eligibility:      EXCLUDED_INSUFFICIENT_PRECISE_SUBSET
Reason: the verified HIGH-confidence subset (12) is below the prespecified
  approximate minimum of 30-40 observations and is insufficient for
  defensible continuous-time Hawkes recovery and estimation.
MEDIUM rows (57):          SENSITIVITY_ONLY_NOT_PRIMARY_M4 -- reconsiderable
  only under a future uncertainty-aware temporal model or an explicit
  sensitivity design, never folded into M4's primary recovery test.
row_129:                   remains MULTIPLE_DATES_AMBIGUOUS -- no candidate
  date selected, no further source review conducted in this phase.
```

Tournament impact recorded: M0 `ELIGIBLE`, M1 `BENCHMARK_ONLY`, M2 `ELIGIBLE`, M3 `ELIGIBLE`, M4 `EXCLUDED FOR CURRENT DATASET`. This is treated as the correct conservative outcome — M4 not running is preferable to a continuous-time result built on a mostly-MEDIUM precision base.

The ledger (`MODEL_3B_PHASE0_DATE_PRECISION_LEDGER.csv`) now carries an `m4_eligibility_class` column: `M4_PRIMARY_ELIGIBLE` (12 rows), `SENSITIVITY_ONLY_NOT_PRIMARY_M4` (57 rows), `NOT_APPLICABLE_NON_EXACT` (27 rows) — sums to 96.

**Pre-freeze verification (all confirmed):** 96/96 rows accounted for; category totals sum to 96; `EXACT_EVENT_DATE` = 69; HIGH = 12; MEDIUM = 57; all 7 QA reclassifications recorded; `row_129` remains `MULTIPLE_DATES_AMBIGUOUS`; no date auto-selected; no source date altered; `data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` confirmed untouched; no model/tournament execution performed.

## Final Status (this document)

```text
MODEL_3B_PHASE0_DATE_PRECISION_AUDIT_COMPLETE_M4_EXCLUDED
```
