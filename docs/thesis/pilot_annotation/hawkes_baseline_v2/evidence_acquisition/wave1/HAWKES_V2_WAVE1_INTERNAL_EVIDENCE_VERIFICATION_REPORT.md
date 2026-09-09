# HAWKES V2 — WAVE 1 INTERNAL EVIDENCE VERIFICATION REPORT

Scope: ACT-02 (repository-only citation/locator verification), ACT-06
(repository-only date/locator/provenance verification), ACT-10 preparation
(one prospective segmentation decision package). Repository-read-only.
No external source retrieval. No modeling. No Git mutation.

```
Authoritative HEAD (local, matches origin at time of this operation) = 985ebe786af5767161ff5864a01c1173ba3e7f35
Operation date (UTC) = 2026-09-09
```

## 1. Frozen state — confirmed unchanged

All values below were read from
`evidence_acquisition/HAWKES_V2_EVIDENCE_ACQUISITION_MASTER_REPORT.md` and
cross-checked against the underlying CSVs cited in this report. None was
recomputed, reinterpreted, or mutated in this operation.

```
V2-A = MIXED_VALIDATION_RESULT
Hawkes family = EXPLORATORY_CANDIDATE / NOT_RULED_OUT
F3 = SUSPEND_PENDING_ONTOLOGY_AND_OBSERVATION_MODEL_REMEDIATION
Hawkes fitting = SUSPENDED
Hawkes visualization = SUSPENDED
H-05 = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
D1_prior = NOT_EVALUABLE
G_divergent = NOT_EVALUABLE
G_ontology = 0
G_causal = 0
G_reconsider_future = 0
V2-B = BLOCKED
DEDUP-06 = UNRESOLVED
G_DEDUP06 = 0
R-O4 = FAIL
AS86 = FROZEN_UNCHANGED
G_seg_prospective = 0
G_ACT05_design = 0
G_sync = NOT_EVALUABLE
Phase D = CLOSED / MUST NOT BE RERUN
```

Model 3B-CD V1 and Phase D are permanently closed; Hawkes V2 itself is
**suspended pending remediation**, not closed. This report preserves that
distinction throughout.

## 2. ACT-02 — Citation and locator verification

### 2.1 25-claim dependency ledger

Source: `evidence_acquisition/HAWKES_V2_CLAIM_EVIDENCE_DEPENDENCY_LEDGER.csv`
(25 data rows, confirmed by direct count).

Every row's `source_artifact` was confirmed to exist at its cited path, and
its cited locator (row/section) was opened and confirmed to contain the
content the ledger describes. The seven distinct cited artifacts —
`HAWKES_BASELINE_V2_DIALECTICAL_CLAIM_MATRIX.csv`,
`HAWKES_BASELINE_V2_RO1_RO10_GATE_MATRIX.csv`,
`HAWKES_BASELINE_V2_DEDUP06_ABDUCTIVE_MATRIX.csv`,
`HAWKES_BASELINE_V2_EXPOSURE_INFORMATION_REQUIREMENTS.csv`,
`HAWKES_BASELINE_V2_COMPARATOR_PREREQUISITE_MAP.csv`,
`HAWKES_BASELINE_V2_DEEP_UNCERTAINTY_SCENARIO_MATRIX.csv` — were all present
and internally consistent with the ledger's row-by-row descriptions. No
citation in this ledger failed to resolve.

```
N_material citation targets (25-claim ledger) = 25
N_verified_resolve                            = 25
P_citation = 25/25 = 1.00
```

This is citation-resolution coverage only — it does not certify that any
`ADOPT`/`REJECT`/`RETAIN_AS_OPEN` decision recorded in the ledger is
historically or scientifically correct, only that the cited evidence exists
where claimed and says what the ledger says it says.

### 2.2 Nine identified source objects

Source: `evidence_acquisition/HAWKES_V2_SOURCE_FAMILY_OPPORTUNITY_MAP.csv`
(9 data rows, confirmed by direct count).

All nine locally-cited files were confirmed present on disk:
`docs/BL_IOR_G_35_198.txt`, `docs/30.txt`, `docs/36.txt`, `docs/HenryBotham`,
`docs/bsb10468472.txt`, `docs/EIC_alternatif.json`,
`docs/The voyages of Sir James Lancaster.docx`,
`docs/NL-HaNA_2.10.39_797_0054-groot.jpg`, and `docs/UNTRACKED_INVENTORY.md`
(the inventory document itself, cited as the provenance source for several
rows). Access-state labels already recorded in the map (`CONFIRMED` /
`PARTIAL` / `NOT CONFIRMED` / `UNCLASSIFIABLE (INFERENCE_ONLY)`) were spot
checked against file presence and found accurate as stated — this operation
does not upgrade any of those labels except where noted in Section 2.3.

```
N_source_objects = 9
N_locally_cited_files_confirmed_present = 9
P_locator (source objects) = 9/9 = 1.00 (file-existence only; does not
  certify relevance, completeness, or lawful-access-route identification —
  those remain UNRESOLVED/UNKNOWN exactly as already recorded)
```

### 2.3 DEDUP-06 / "Corpus III, nr. D" / EVT-1687-gm-vol04-05-162-a6b1 — finding

This thread was checked in depth because it is the sole `FAIL` in the
program's gate matrix (`R-O4`).

**Cross-file consistency confirmed.** `HAWKES_BASELINE_V2_DEDUP_ADJUDICATION.csv`
(row `DEDUP-06`), `HAWKES_BASELINE_V2_DEDUP06_ABDUCTIVE_MATRIX.csv` (rows
`H-DEDUP06-A/B/C` and `STOP_RULE_RESULT`), and
`evidence_acquisition/HAWKES_V2_DEDUP06_RETRIEVAL_DOSSIER.md` all describe
the same case identically: status `UNRESOLVED` / `RETAIN_AS_OPEN` /
`MECHANISM_UNDERDETERMINED`, with `AS86` unmutated in every account. No
inter-file contradiction on status.

**One factual correction to the retrieval dossier.** Section 4 of
`HAWKES_V2_DEDUP06_RETRIEVAL_DOSSIER.md` states: *"No image, transcription,
or independent citation of 'Corpus III, nr. D' exists anywhere in this
repository beyond the string itself as recorded in the dedup-adjudication
artifact chain."* This is not accurate. The source file already cited as
this event's own provenance —
`docs/thesis/GM/xml/05/p0162.xml` (the same file the dossier's Section 1
says was "directly verified this project") — contains the full editorial
footnote at line 987, attached directly to the Radja Itam / 12 penghulus
Bajang / 22 Dec 1687 passage (lines 982–989):

```
[note mark="1"] Met dezen Radja Hitam werd door Lobs 22 dec. 1687 een
contract afgesloten, zo ook met de 12 penghulus van Bajang, vgl.
Corpus III, nr. D.
```

("vgl." = Dutch "compare/see" — standard RGP editorial practice for citing
another published edition of the *same* document.) This citation is a
verbatim editorial cross-reference attached to the identical passage that
produced `EVT-1687-gm-vol04-05-162-a6b1`, not a free-floating or
unlocated string.

**Series identity is now inferable from repository evidence, not
unconfirmed.** `HAWKES_V2_SOURCE_FAMILY_OPPORTUNITY_MAP.csv` (row "RGP
editorial cross-reference apparatus") records "whether 'Corpus III' denotes
a specific RGP-series sub-volume identifiable by researcher" as UNKNOWN.
`data/research/linimasa_events.csv` (row 82, an unrelated corpus row, CD4)
independently cites: *"SUMBER: Corpus Diplomaticum Neerlando-Indicum, Jilid
IV, traktat DLIII"* — i.e. this project already treats "Corpus [volume
number]" as shorthand for a specific volume of the named, identifiable
published series *Corpus Diplomaticum Neerlando-Indicum*. This is a strong,
in-repository basis (`AGENT_HYPOTHESIS`, not a confirmed fact) for reading
"Corpus III" in the DEDUP-06 citation as Volume III of the same series,
rather than an unidentified compilation.

**Locator disambiguation.** `docs/thesis/GM/xml/05/p0162.xml` contains
three distinct "Corpus III, nr. [X]" citations on the same page: `nr. D.`
(line 987, attached to the Bajang/Radja Itam passage — this is the DEDUP-06
target), `nr. Dl` (line 1003, attached to a *different* passage about a
Tarusan contract with the Sapuluh Buah Bandar coalition, also dated 22 Dec
1687), and `nr. DXIX` (line 127, attached to an unrelated 1689 passage).
The DEDUP-06 dossier's citation string "Corpus III, nr. D" is confirmed to
refer specifically to the bare `nr. D.` footnote (line 987), not to the
adjacent but textually distinct `nr. Dl` citation — these are two separate
document numbers in the same volume, not the same target read two ways.

**What this does and does not change.**
```
Does NOT change:            DEDUP-06 = UNRESOLVED; G_DEDUP06 = 0; R-O4 = FAIL; AS86 unmutated.
Does NOT constitute:        retrieval, reading, or comparison of the "Corpus III, nr. D"
                             document itself (its full treaty text remains external and
                             unretrieved).
DOES correct:                the retrieval dossier's Section 4 claim of "nothing found
                             in-repo beyond the string" — the citation's full context IS
                             in-repo.
DOES sharpen:                the external-information requirement for a future ACT-01: the
                             retrieval target is now specifically "Corpus Diplomaticum
                             Neerlando-Indicum, Vol. III, item D" rather than an unidentified
                             RGP volume.
DOES weakly favor:           H-DEDUP06-A (corroborating cross-reference to the same
                             occurrence) as the most consistent reading of "vgl." — this is
                             recorded as AGENT_HYPOTHESIS, not entered as a discriminating
                             observation; the stop-rule result (three live hypotheses, no
                             discriminating observation) is explicitly NOT overturned by this
                             finding, per the abductive matrix's own discriminating-observation
                             requirement (full retrieval + reading + comparison, none of which
                             occurred here).
```

## 3. ACT-06 — Date, locator, and provenance verification

### 3.1 Corpus-wide date-precision distribution (unchanged, re-confirmed)

Source: `HAWKES_BASELINE_V2_DATE_UNCERTAINTY_LEDGER.csv`.

```
EXACT_DAY            72   51.1%
MONTH_ONLY            10    7.1%
YEAR_ONLY             16   11.3%
INTERVAL              21   14.9%
DOCUMENT_DATE_PROXY    0    0.0%
INFERRED_DATE          0    0.0%
UNRESOLVED             22   15.6%
                      ---
                      141  100.0%  (sums correctly; re-verified by addition)
```

### 3.2 DEDUP-06 event date (material item)

```
event_id       = EVT-1687-gm-vol04-05-162-a6b1
value          = 22 December 1687
role           = EVENT_DATE  (per HAWKES_BASELINE_V2_DATE_SEMANTICS.csv
                 `date_meaning` column — this value already existed in the
                 committed schema before the WP-E5 taxonomy was designed;
                 it happens to align with the taxonomy's `EVENT_DATE` token,
                 which this operation treats as a pre-existing schema value,
                 not a new role assignment performed here)
precision      = EXACT_DAY
document_date  = "1688 (surat), merujuk 22 Des 1687" (i.e. the letter/report
                 itself is dated 1688 and refers back to the 22 Dec 1687
                 event — this row's schema already distinguishes document
                 date from event date, ahead of the formal WP-E5 taxonomy)
source         = docs/thesis/GM/xml/05/p0162.xml, note mark 1
G_date,i       = 1[role != UNRESOLVED_DATE_ROLE (TRUE) AND provenance
                 documented (TRUE, source distinct from row's own citation)
                 AND bounds coherent (vacuously TRUE, no bounds
                 constructed)] = 1
```
Per `HAWKES_V2_DATE_SEMANTICS_PROTOCOL.md` Section 3: `G_date,i = 1` answers
only "is this date semantically legible," and authorizes no fitting,
forecasting, or comparator use.

### 3.3 R-O5 (explicit interval bounds) — unchanged

`HAWKES_BASELINE_V2_RO1_RO10_GATE_MATRIX.csv` row `R-O5`: `NOT_EVALUABLE`,
0/141 bounds constructed, "bounds deliberately not machine-computed to
avoid silent point-substitution." Re-confirmed unchanged; no bounds were
constructed in this operation.

### 3.4 Minor naming inconsistency noted (not a contradiction of status)

`HAWKES_BASELINE_V2_DATE_SEMANTICS.csv` (`precision_class` column) and
`HAWKES_BASELINE_V2_EVENT_PROVENANCE_AUDIT.csv` (`event_date_precision`
column) use different literal tokens for the same rows' unresolved-date
category — `UNRESOLVED` in the former, `UNRESOLVED_BLANK` in the latter
(checked directly on `EVT-1600-CD1-47-72aa` and three adjacent rows). Same
underlying condition, different label across two sibling files. Recorded as
a documentation inconsistency for future schema cleanup; does not change
any denominator, gate, or frozen status above.

```
P_date (material items assessed: DEDUP-06 event + R-O5 gate + corpus-wide
  distribution cross-check) = 3/3 explicit date-role or date-status
  determinations confirmed consistent with existing records = 1.00
  (full 141-row per-event role re-tagging was not performed — out of
  Wave-1 scope; this remains the unchanged status quo already recorded
  in the master report, not a new gap introduced or found here)
```

## 4. ACT-10 — Prospective proposition-segmentation decision package

`evidence_acquisition/HAWKES_V2_PROSPECTIVE_PROPOSITION_SEGMENTATION_PROTOCOL.md`
was re-read in full and confirmed to already contain:

```
R (rule)              = 1  (Sections 1-2: definition + design-requirement table)
E (examples)          = 1  (Section 3: two worked deterministic examples)
U (ambiguity policy)  = 1  (Section 4: adjudication-queue design)
A (researcher accept) = 1  (ACCEPT_PROSPECTIVELY, recorded 2026-09-09 in
                            HAWKES_V2_WAVE1_RESEARCHER_DECISION_AND_REPRODUCIBILITY_MANIFEST.csv)

G_seg_prospective = 1[R=1 AND E=1 AND U=1 AND A=1] = 1
```

No gap was found in R, E, or U requiring revision on technical grounds.

**Researcher adjudication (post-Wave-1 update):** the researcher selected
`ACCEPT_PROSPECTIVELY` from the three offered options
(`ACCEPT_PROSPECTIVELY | REVISE_PROSPECTIVELY | DEFER`). Effective boundary:
this acceptance applies prospectively, from this adjudication forward, to
future proposition-typing work governed by this protocol only. It does
**not** re-segment or re-type the already-produced epistemic-object
ledger, and does **not** validate ontology or historical truth.
`D1_prior` remains `NOT_EVALUABLE` (protocol Section 6), unchanged by this
decision. `G_seg_prospective=1` is not an input to `G_W1` (Section 6 below)
and does not itself change `G_ontology`, `G_causal`, `G_reconsider_future`,
or `G_DEDUP06`, all of which remain 0.

## 5. Estimands summary

```
P_citation                = 25/25 = 1.00   (Section 2.1)
P_locator (source objects) = 9/9  = 1.00   (Section 2.2; existence only)
P_date                     = 3/3  = 1.00   (Section 3.4)
P_provenance               = 34/34 = 1.00  (every material claim/source in
                              scope links to an existing repository object;
                              the one open external requirement — the
                              "Corpus III, nr. D" full document — is
                              explicitly recorded as an information
                              requirement, not left silently unresolved)
G_ACT10_ready              = 1[rule=1 AND examples=1 AND ambiguity_policy=1
                              AND decision question explicit=1] = 1
                              (readiness of the DECISION PACKAGE itself;
                              does NOT imply G_seg_prospective=1, which
                              remains 0 pending researcher acceptance)
```

## 6. Wave 1 exit gate

```
V_02 = 1   (ACT-02 verification complete for its declared denominator: 25 + 9 = 34 items)
V_06 = 1   (ACT-06 verification complete for its declared denominator: 3 material date items
            + corpus-wide distribution cross-check)
G_ACT10_ready = 1
N_unauthorized_mutations = 0   (no existing file modified; only three new files created
            under evidence_acquisition/wave1/, plus the wave1/ directory itself)
N_false_convergence = 0   (no claim-level ADOPT/REJECT decision was reopened or newly
            forced in this operation; the DEDUP-06 finding in Section 2.3 explicitly
            does not convert R-O4 from FAIL, does not set G_DEDUP06=1, and is recorded
            as AGENT_HYPOTHESIS/weak-favor, not as a discriminating observation)

G_W1 = 1[V_02=1 AND V_06=1 AND G_ACT10_ready=1 AND N_unauthorized_mutations=0
         AND N_false_convergence=0] = 1
```

**Explicit non-implications** (unchanged by `G_W1=1`):
```
G_W1=1  ⇏  G_seg_prospective=1   (still 0, pending researcher acceptance)
G_W1=1  ⇏  G_ontology=1          (still 0)
G_W1=1  ⇏  G_causal=1            (still 0)
G_W1=1  ⇏  G_reconsider_future=1 (still 0)
G_W1=1  ⇏  G_DEDUP06=1           (still 0; DEDUP-06 remains UNRESOLVED)
```

## 7. Confirmation of guardrails

No external source was retrieved (the "Corpus III, nr. D" full document
remains unretrieved — Section 2.3's finding used only files already present
in this repository). ACT-01, ACT-05, and ACT-07 were not executed. AS86 and
the 141-row corpus were not mutated. DEDUP-06 was not resolved; R-O4 was
not promoted. No fitting, forecasting, simulation, bootstrap, calibration,
visualization, or comparator/negative-control execution occurred. No
ontology or causality promotion occurred. V2-B and Phase D were not
executed. No worktree cleanup or full untracked-file census was performed.
`.gitignore` was not modified. No staging, commit, push, sync, or deploy
occurred. Exactly three new files were created (this report plus the two
CSVs listed in Section 0), all under
`docs/thesis/pilot_annotation/hawkes_baseline_v2/evidence_acquisition/wave1/`.
No existing file was edited.

**Pausing for researcher adjudication of the Section 4 decision package.**
