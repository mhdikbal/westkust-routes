# HAWKES V2 — EVENT-UNIT ADJUDICATION PROTOCOL (DESIGN INSTRUMENT ONLY)

WP-E4. This document designs a protocol for distinguishing event-unit
categories. **No AS86 row is scored. No corpus mutation occurs.** The
protocol and worked examples below use hypothetical or already-published
illustrative material only.

## 1. Six entity classes

```
LATENT_HISTORICAL_EVENT      -- an occurrence in the past, never directly observed
DOCUMENTED_OR_REPORTED_EVENT -- a period source's account of an occurrence
CORPUS_CODED_EVENT           -- a row in this project's extracted dataset
PARENT_EPISODE                -- a higher-level grouping of related coded events
SOURCE_CITATION_TARGET        -- an editorial/compilation cross-reference, not itself an event
UNRESOLVED_REFERENT           -- a citation target that cannot currently be classified into any of the above
```

## 2. Adjudication instrument

For candidate item *i*:

```
E_i^unit = 1[ I_i=1 AND B_i=1 AND G_i=1 AND P_i=1 ]
```

| Component | Question the adjudicator must answer | Evidence required to answer YES |
|---|---|---|
| I_i (identity) | Is there an explicit rule for what makes this item the *same* occurrence across sources? | A stated identity criterion (e.g. "same actors + same location + same calendar month, cross-checked against at least one independent source") — not merely "it has a unique row ID" |
| B_i (boundary) | Are the temporal and substantive start/end boundaries explicit? | A stated rule for where one occurrence ends and the next begins (e.g. distinguishing a single negotiation from a multi-session negotiation spanning weeks) |
| G_i (granularity) | Is the intended level of granularity explicit (atomic act vs. composite episode)? | A stated choice between atomic-act and episode-level coding, applied consistently |
| P_i (provenance) | Is there a locator distinct from the event's own citation that grounds the above three? | An independent audit trail (e.g. a second source, an editorial note, a researcher adjudication record) — not just the coded row itself asserting its own identity |

`E_i^unit = 1` only when **all four** hold with cited evidence. Absence of a criterion is scored 0 for that component, not imputed.

## 3. Worked examples (illustrative only, not corpus rows)

### Example A — clean atomic event (hypothetical)
A single dated letter reports a single specific act (e.g. "on 12 October a treaty was signed"), with the letter itself as the sole source.
```
I = 1 (identity: the letter's own narrative act)
B = 1 (boundary: a single dated act)
G = 1 (granularity: atomic, by construction)
P = 0 (provenance: only the letter itself — no independent corroboration or audit locator)
E^unit = 0   -- fails on provenance alone, illustrating that plausibility is not sufficient
```

### Example B — multi-session episode (hypothetical)
A negotiation is reported across three letters spanning six weeks, each describing a different session of the same underlying negotiation.
```
I = 0 (no explicit rule yet for whether these three reports denote one occurrence or three)
E^unit = 0   -- fails immediately once any component is 0; this is the PARENT_EPISODE case
  requiring R-O3-style adjudication (WP-E4 does not resolve which reading is correct)
```

### Example C — the DEDUP-06 pattern (real, but not scored here)
A coded event has a citation-apparatus cross-reference to a locator that does not resolve to any existing `event_id`.
```
This is, by construction, classified SOURCE_CITATION_TARGET or UNRESOLVED_REFERENT
before any I/B/G/P scoring is attempted — the adjudication instrument in Section 2
applies only after an item is provisionally admitted as a candidate DOCUMENTED_OR_REPORTED_EVENT
or CORPUS_CODED_EVENT. DEDUP-06 itself remains at the prior stage (referent-class
undetermined among same-event / second-event / citation-artifact), handled by
WP-E6, not by this instrument.
```

## 4. Relationship to R-O1

The prior operation's R-O1 finding (`NOT_COMPUTABLE` for the original evidence-grounded construct; `119/141` for the weaker `EVENT_METADATA_MINIMUM_AVAILABILITY` proxy) is **preserved unchanged**. This protocol is the *design* of the instrument that a future, separately authorized operation would need to apply row-by-row to close that gap — it is not itself an application of that instrument to the 141-row corpus.

## 5. Non-authorization statement

This protocol authorizes nothing beyond its own existence as a design artifact. Applying it to AS86 or the 141-row corpus, or using its output as a model input, requires a separate, explicit future authorization.
