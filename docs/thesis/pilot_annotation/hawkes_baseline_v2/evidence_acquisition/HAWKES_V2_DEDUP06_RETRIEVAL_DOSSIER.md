# HAWKES V2 — DEDUP-06 EVIDENCE-ACQUISITION DOSSIER

WP-E6. **This dossier does not resolve DEDUP-06.** It specifies what would
need to be retrieved and read, by whom, and how the result would be
adjudicated, for a future, separately authorized operation.

```
DEDUP-06                 = UNRESOLVED
D_primary_unresolved     = 1
K_primary_unresolved     = 1
AS86                     = FROZEN_UNCHANGED
```

## 1. Known coded row

```
event_id: EVT-1687-gm-vol04-05-162-a6b1
Source collection: GM (Generale Missiven), Deel 04-05
Coded summary: [as already recorded in MODEL_3B_EVENT_SOURCE_PROVENANCE_WORKING.csv — not reproduced or reread here]
Membership: part of the 86-event primary set (AS86)
```

## 2. Known citation target as written

```
"Corpus III, nr. D"
```
This string does not resolve to any existing `event_id` in the 141-row
corpus. Its literal form suggests a compilation-series citation (volume
"Corpus III", item "nr. D"), consistent with — but not confirmed as — an
RGP-style (Rijks Geschiedkundige Publicatiën) editorial cross-reference
(see `HAWKES_V2_SOURCE_FAMILY_OPPORTUNITY_MAP.csv`, row "RGP editorial
cross-reference apparatus").

## 3. Archival locator components (as currently decomposable)

| Component | Value | Status |
|---|---|---|
| Series/compilation name | "Corpus III" | UNCONFIRMED — could denote an RGP sub-volume, a different diplomatic-instrument compilation (possibly related to the project's own "CD" series numbering), or something else entirely |
| Item designator | "nr. D" | UNCONFIRMED format — "D" could be a letter-indexed sub-item, an appendix letter, or a transcription artifact |
| Originating document | The GM vol. 04-05 entry that cross-references it | KNOWN (same row that produced EVT-1687-gm-vol04-05-162-a6b1) |
| Date window | ~1687 (inferred from the citing entry's context) | INFERRED, not independently confirmed |

## 4. Source image/text currently available

None. No image, transcription, or independent citation of "Corpus III, nr.
D" exists anywhere in this repository beyond the string itself as recorded
in the dedup-adjudication artifact chain.

## 5. Missing object

The primary or secondary source document that "Corpus III, nr. D" actually
denotes — its full text or a reliable summary sufficient to compare its
narrative content against `EVT-1687-gm-vol04-05-162-a6b1`.

## 6. Retrieval route (specification, not execution)

1. Determine whether "Corpus III" matches a known published series
   (candidates to check, in order of plausibility given this project's
   existing source families: an RGP volume; the project's own "CD"
   Corpus Diplomaticum numbering under a different citation convention;
   a GM cross-reference apparatus internal to the Generale Missiven
   editorial series itself).
2. If a series is identified, locate its library/digital holding (per
   `HAWKES_V2_SOURCE_FAMILY_OPPORTUNITY_MAP.csv`'s "lawful future access
   route" column for whichever family matches).
3. Retrieve item "nr. D" (or the nearest addressable unit if "D" denotes a
   sub-item within a longer document).
4. Produce a transcription or reliable summary sufficient for comparison.

**This operation does not execute any of steps 1–4.** No external source
retrieval is authorized here.

## 7. Paleographic or philological checks required

- Confirm whether "Corpus III, nr. D" is a faithful transcription of the
  original citation string, or itself a project transcription/OCR artifact
  that may have altered the original wording (e.g. a misread volume number
  or letter).
- If retrieved, confirm the document's date, actors, and location align
  plausibly with the 1687 GM vol. 04-05 context before any comparison is
  attempted.

## 8. Hypotheses A, B, C (restated from the abductive matrix, not re-adjudicated)

| Hypothesis | Statement | Evidence that would favor it | Evidence that would disfavor it |
|---|---|---|---|
| H-DEDUP06-A | Same historical occurrence as `EVT-1687-gm-vol04-05-162-a6b1` (corroborating cross-reference) | Retrieved text describes the same actors/location/action already coded | Retrieved text describes a materially different occurrence |
| H-DEDUP06-B | A different, currently uncoded occurrence near in time | Retrieved text describes a distinct occurrence not already in the 141-row corpus | Retrieved text is absent, or describes the same occurrence as A |
| H-DEDUP06-C | A citation/editorial artifact only (no discrete event-shaped referent) | Retrieved target is confirmed to be a compilation-section or index entry, not a narrative of an occurrence | Retrieved target is confirmed to narrate a specific occurrence |

Per the governing instruction's Section 17 stop-rule (three live alternatives,
no discriminating observation yet), none of these three is currently
preferred.

## 9. Researcher adjudication form (to be completed only after retrieval)

```
Retrieved object identified:            [ ] YES  [ ] NO
Retrieved object read in full:          [ ] YES  [ ] NO
Comparison against EVT-1687-...-a6b1:   [ ] FAVORS_A  [ ] FAVORS_B  [ ] FAVORS_C  [ ] INCONCLUSIVE
Researcher acceptance of a reading:     [ ] ACCEPTED  [ ] NOT ACCEPTED
Resulting DEDUP-06 status:              [ ] UNRESOLVED (unchanged)  [ ] RESOLVED (requires researcher signature + evidence citation)
```

## 10. Closure gate (required current value)

```
G_DEDUP06 = 1[ source_object_retrieved=1 AND referent_read=1 AND alternatives_compared=1 AND researcher_accepted=1 ]
G_DEDUP06 = 0   (none of the four preconditions is met; none is attempted in this operation)
```

**DEDUP-06 remains UNRESOLVED. This dossier does not resolve it, even
though a plausible interpretation (H-DEDUP06-C, citation artifact) might
appear parsimonious — that appearance is explicitly not treated as
resolution.**
