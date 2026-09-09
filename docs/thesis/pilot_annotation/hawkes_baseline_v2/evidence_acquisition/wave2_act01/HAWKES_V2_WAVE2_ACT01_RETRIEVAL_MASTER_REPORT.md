# HAWKES V2 — WAVE 2 ACT-01 RETRIEVAL AND LOCAL DOCUMENTARY ADJUDICATION — MASTER REPORT

Scope: ACT-01 (retrieve/identify/assess the object cited as "Corpus III, nr. D"),
restricted after correction to repository-local inspection only. Manual
approval mode throughout. No Git operation performed at this checkpoint.

```
Authoritative HEAD (unchanged throughout this operation) = f8af5ca8faeae19cdc040f6ea811d0b2bd532cb9
Operation date (UTC) = 2026-09-09
```

## 0. Redundant-search correction

Before local inspection was performed, four WebSearch calls and two WebFetch
calls were made against archive.org, JSTOR, the Corts Foundation, and ANRI to
identify and retrieve *Corpus Diplomaticum Neerlando-Indicum*, Volume III.
The researcher correctly identified that the target already exists locally
at `docs/cd/CD3.pdf` and instructed a stop to all external search.

```
REASONING_SHORTCUT_DETECTED = EXTERNAL_SEARCH_BEFORE_LOCAL_CORPUS_INSPECTION
```

No external content was downloaded or incorporated into this repository.
All findings below derive exclusively from files already present in this
repository before this operation began.

## 1. Local source identity

`docs/cd/CD3.pdf` — confirmed from the PDF's own title page (page 1 of the
PDF) to be *Corpus Diplomaticum Neerlando-Indicum*, ed. Prof. Mr. J. E.
Heeres / Dr. F. W. Stapel, **DERDE DEEL (1676–1691)** — i.e. Volume III,
matching the citation "Corpus III" exactly.

```
Local path   = docs/cd/CD3.pdf
File type    = PDF (OCR text layer, ABBYY FineReader 11)
Byte size    = 15,767,770
SHA-256      = 716c216cc6963a66f894888bbd4c95630a0e736ab86f0f74d6807d0851311f7c
Page count   = 625
```

`docs/cd/` contains 6 files total (`CD1.pdf`–`CD6.pdf`); all 6 title pages
were checked, and only `CD3.pdf` matches "Corpus III."

```
P_local = 6/6 = 1.00
```

## 2. Document D and Document Dl — exact locators and diplomatic excerpts

### Document D ("Corpus III, nr. D")

```
Digital locator = docs/cd/CD3.pdf, PDF pages 453-454
Printed page    = 442-443
Heading         = "D. SUMATRA'S WESTKUST. 22 December 1687."
Title           = "Acte van authorisatie, verleent aan de twaalff ponglous
                   of regenten van Bayang wegens 't gemene bestier van
                   saacken aldaar, door de heer commissaris Jacob Lobs, in
                   dato 22 December 1687."
Archival note (p.453, footnote) = "Uit het Contractboek. Ook in de
                   verzameling der Kamer-Zeeland, no. 8148, en in de
                   Overgecomen brieven 1691, twee-en-twintighste boeck,
                   folio 547 en volg[ende]."
```

Diplomatic excerpt (opening lines, diplomatic form preserved verbatim):

> "Jacob Lobs, expres commissaris van Sumatra's Westcust, uyt de naam en
> vanwegen den Hoog Ed. heere Joannes Camphuys, Gouverneur-Generaal ende d'Ed
> heeren Raden van 't Nederlands India, doen te weten: Dewyle den jongsten
> of laatsten panglima ofte gouverneur van Bayang, genaamt Radja Phaloan,
> sig sedert weynige jaren verleden sodanig in en omtrent de handelinge der
> Engelsche natie hier te custe met de radjas doua Sahela heeft komen in te
> wickelen... soo heeft sulx de twaalff presente ponglous ofte regenten van
> Bayang, met namen Radja Memoeda, Siry Maharadja Radja Bazaar, Radja Amaas,
> Intje Seleman, Radja Indermamoelia, Cede Bayangh, Radja Alam, Radja
> Bandiara, Khatib Maharadja Lilla, Samporna Maradja, Radja Malientangh en
> Nachoda Caya, bewogen ende genoodsaakt voor ons te compareren..."

**Party list of Document D (12 named regents):** Radja Memoeda, Siry
Maharadja Radja Bazaar, Radja Amaas, Intje Seleman, Radja Indermamoelia,
Cede Bayangh, Radja Alam, Radja Bandiara, Khatib Maharadja Lilla, Samporna
Maradja, Radja Malientangh, Nachoda Caya. **"Radja Itam" does not appear in
this party list.** The document concerns the fled prior governor "Radja
Phaloan," not Radja Itam.

Reading status: `READING_SECURE` (full OCR text, internally coherent,
consistent with the archival cross-references cited in its own footnote).

### Document Dl ("Corpus III, nr. Dl")

```
Digital locator = docs/cd/CD3.pdf, PDF pages 455-457
Printed page    = 444-446
Heading         = "Dl. SUMATRA'S WESTKUST. 22 December 1687."
Editorial lead  = "Op denzelfden dag en ter zelfder plaatse sloot Lobs een
                   overeenkomst met den koning van Taroessan of Troessan,
                   door wiens gebied de weg van Bajang naar de kust liep,
                   waarbij deze vorst de Compagnie aannam als zijn schuts-
                   en scheidsheer."
```

Diplomatic excerpt (opening lines):

> "Jacob Lobs, expres commissaris der Sumatra's Westcust weegens den Hoog
> Edelen Heere Joannes Camphuys... Alsoo Sijn Hoogheyt, radia Itam, koning
> ende souveraine hooftgebieder over de landen en volckeren, onder 't
> district van 't rijk ofte provintie van Troussan behorende, ons
> verscheyde maelen... vertoont en aangeclaegt heeft... was hij, coning, soo
> verclaarde en verclaart mits desen, te raede geworden, sig aan ons... te
> addresseren... svne schutsheer, regter en schijtsheer te willen
> verstrecken..."

**Party of Document Dl:** Radja Itam, king ("coning ende souveraine
hooftgebieder") of Troussan/Tarusan, placing his territory under VOC
protection. Signed same date (22 Dec 1687), same place (Troessan), same
commissioner (Lobs), immediately following Document D in the volume.

Reading status: `READING_SECURE`.

```
P_locator = 6/6 = 1.00
  (resolved components: work, volume, item, printed page, digital page,
  local path — all six confirmed for Document D)
```

## 3. GM passage (docs/thesis/GM/xml/05/p0162.xml) — full context re-read

The GM main narrative (printed p.178–179) describes the Bajang governance
crisis (the prior governor Radja Phaloan fled; the community petitioned for
local self-rule by the 12 ponglous, and separately wished to appeal to "den
Radja Itam tot Troessang" for mediation of disputes) as continuous prose. It
does **not** itself state that one contract covered both parties.

That claim originates in the RGP editor's (Stapel's) own footnote (note mark
1, attached at "den Radja Itam"):

> "Met dezen Radja Hitam werd door Lobs 22 dec. 1687 een contract afgesloten,
> zo ook met de 12 penghulus van Bajang, vgl. Corpus III, nr. D."

This is a **source-reported claim by the editor**, not a repository fact
about the primary documents' content. Reading it against Documents D and Dl
directly (Section 2 above) shows it describes two separate instruments as
if they were one contract.

```
SHA-256 (docs/thesis/GM/xml/05/p0162.xml) = 0e0796c5ad09ae8be582ee248637f8bdc1cdadf3fb2808cb83d0565ce1720ad8
```

## 4. Coded row and coding-provenance artifact

`event_id = EVT-1687-gm-vol04-05-162-a6b1`

```
Fields (from HAWKES_BASELINE_V2_EVENT_PROVENANCE_AUDIT.csv):
  event_date            = 22 December 1687
  event_date_precision  = exact_day
  event_type            = perjanjian
  parent_episode_id     = NONE
  primary_source_collection = GM
  source_count_unique   = 1
  provenance_status     = CD_INDEPENDENT
  deduplication_review_required = true
  researcher_review_required    = true
```

**Coding-provenance artifact identified locally:**
`docs/thesis/colab/MODEL_3B_EVENT_SOURCE_PROVENANCE_WORKING.csv`, row `B7`
(`event_id=EVT-1687-gm-vol04-05-162-a6b1`).

```
SHA-256 = 8a93667b88543f9eb8905b0168d62dd6450395b99de96c31ab962be1f9d59528
Bytes   = 122375
```

Actor field: `"Radja Itam (Hitam) & 12 penghulu Bayang -> komisaris Lobs"`
— this follows Stapel's footnote wording, not an independent project
inference.

Row B7's own `notes` field (project coding decision, quoted verbatim, this
is a repository fact about what the coder recorded — not a new finding):

> "GM vol.05 (RGP Deel 5) -- sumber langsung; catatan editorial RGP internal
> merujuk 'Corpus III, nr. D' (CD), BELUM ditelusuri/dibaca terpisah batch
> ini... NAMUN catatan editorial RGP sendiri merujuk 'Corpus III, nr. D'
> sbg traktat CD yg PARALEL/mungkin identik -- BELUM dibaca/dicocokkan ke
> traktat CD3 manapun batch ini (di luar cakupan verifikasi turn ini).
> deduplication_review_required=true: KEMUNGKINAN row ini adalah CATATAN
> GANDA (via GM) dari traktat CD3 yg SUDAH ada di dataset dari batch
> sebelumnya -- BELUM dicek silang, TIDAK di-merge."

This confirms the project **explicitly flagged** the citation as unverified
at coding time and did not silently assume its content — the coder's own
note already anticipated exactly the question this Wave 2 operation now
addresses.

`data/research/linimasa_events.csv` row 82 (SHA-256
`ebca46d15ab1706ed040ae58206048bde5fc53576606d2dedff363fde9b5278b`) — an
unrelated row (CD4/Jilid IV) — independently named the series "Corpus
Diplomaticum Neerlando-Indicum," which is now directly confirmed correct by
CD3's own title page.

```
P_coding_provenance = 5/6 = 0.833
  (actor, summary/title, date, source, event_type each traced to an
  explicit source or coding decision; parent_episode_id=NONE has no
  explicit justifying note in any locally identified artifact)
```

## 5. Documentary-object crosswalk

```
O_D = { GM, D, Dl, CodedRow, ParentEpisodeCandidate }
```

| Object | Explicit crosswalk | Evidence |
|---|---|---|
| GM | YES | docs/thesis/GM/xml/05/p0162.xml, note mark 1, line 987 |
| D | YES | docs/cd/CD3.pdf PDF pp.453-454 |
| Dl | YES | docs/cd/CD3.pdf PDF pp.455-457 |
| CodedRow | YES | MODEL_3B_EVENT_SOURCE_PROVENANCE_WORKING.csv row B7 |
| ParentEpisodeCandidate | NO | `parent_episode_id=NONE`; no explicit source-grounded episode-assignment rule exists anywhere locally for this event pair |

```
P_mapping = 4/5 = 0.80
```

No two members of O_D are treated as identical without the explicit mapping
shown above. GM ≠ D ≠ Dl ≠ CodedRow ≠ ParentEpisodeCandidate.

## 6. Expanded hypothesis matrix (H-A through H-G)

| H | Statement | Status |
|---|---|---|
| H-A | Document D is corroborating documentary evidence for the Bayang component already represented by the coded row | `SUPPORTED_FOR_DOCUMENTARY_MAPPING` |
| H-B | Document D evidences a distinct historical occurrence not adequately represented by the coded row | `DISFAVORED_BY_LOCAL_EVIDENCE` |
| H-C | The "nr. D" reference functions only as a non-discriminating editorial cross-reference | `DISFAVORED_BY_LOCAL_EVIDENCE` |
| H-D | The local mapping remains unresolved or misresolved | `NOT_SUPPORTED_FOR_DOCUMENTARY_MAPPING` |
| H-E | The coded row conflates two distinct same-day legal instruments, D and Dl, into one coded event | `SUPPORTED_FOR_DOCUMENTARY_MAPPING` |
| H-F | D and Dl are distinct instruments but legitimately grouped as one parent episode under an explicit, source-grounded episode rule | `NOT_EVALUABLE / RETAIN_AS_OPEN` |
| H-G | The coded summary is a project-level simplification whose provenance and intended granularity remain unresolved | `PARTIALLY_SUPPORTED_FOR_DOCUMENTARY_MAPPING / RETAIN_AS_OPEN` |

**H-A basis:** Document D's subject matter (Bayang regents' self-governance
authorization) directly corresponds to the "12 penghulu Bayang" component
already named in the coded row's actor/title fields.

**H-B basis:** Document D's content (Bayang regents authorization) is
already represented in the coded row's summary; it does not describe an
occurrence absent from the coding.

**H-C basis:** "Nr. D" resolves to a complete, discrete, readable treaty
document narrating a specific act — not a bare index/citation artifact.

**H-D basis:** The local mapping was fully resolved (Section 2); it was not
left unresolved or misresolved.

**H-E basis — explicitly qualified per researcher instruction:** H-E is
supported only at the level of documentary representation. The coded row
combines actors associated in the local Corpus evidence with two distinct
legal instruments (D's twelve Bayang regents; Dl's Radja Itam of Troussan).
**This does not itself prove that the coded event must be split into two
historical events or two corpus rows.** Whether one coded row appropriately
represents both instruments, or should be split, is a separate researcher
governance question not settled by this documentary finding.

**H-F basis:** No explicit, source-grounded episode-assignment rule exists
locally to test this hypothesis against. `parent_episode_id=NONE` for the
coded row. No such rule is authored by this operation (per instruction).
`RETAIN_AS_OPEN` pending a future, separately authorized rule-design
operation (this mirrors R-O3's existing terminal status in the Wave 1
gate matrix). Researcher decision: `H-F_RESEARCHER_DECISION = DEFER_EPISODE_RULE`
— no episode rule is authored in this or any operation absent separate
future authorization.

**H-G basis:** The coding-provenance note (Section 4) already marked the
"Corpus III, nr. D" citation as unverified at coding time — this finding
preserves and does not overwrite that note. The *provenance* half of H-G
(where did the conflated actor claim come from) is now traced to Stapel's
editorial footnote, not an unexplained project error. The *granularity*
half (whether the project's chosen level of event decomposition is
appropriate) remains an open researcher decision. `RETAIN_AS_OPEN`.
Researcher decision: `H-G_RESEARCHER_DECISION =
KEEP_CODED_ROW_FROZEN_WITH_DOCUMENTED_CAVEAT_PENDING_GRANULARITY_RULE` — the
coded row is not split, merged, deleted, normalized, or rewritten; this
caveat is retained pending a future, separately accepted granularity rule.

## 7. Pairwise discrimination ledger

Live hypothesis set after documentary-object verification:
`H^live = {H-A, H-E, H-F, H-G}`, `|H^live| = 4`, `C(4,2) = 6` pairs.

| Pair | D_ij | Basis |
|---|---|---|
| (H-A, H-E) | 1 | Local evidence (CD3 content + coded actor field) independently confirms each claim; they are compatible, non-rival claims about different aspects of the same document complex |
| (H-A, H-G) | 1 | A concerns content correspondence (resolved); G's provenance half is now resolved (Section 4) while its granularity half is explicitly identified as the remaining open component — the evidence lets these be told apart |
| (H-E, H-G) | 1 | E is the specific, evidenced diagnosis (party-list mismatch); G's provenance is now resolved and traced to the same underlying fact E documents, while G's granularity question is separately identified as still open |
| (H-A, H-F) | 0 | F cannot be evaluated against anything — no episode rule exists to test it |
| (H-E, H-F) | 0 | Same reason |
| (H-F, H-G) | 0 | Same reason |

```
P_disc = 3/6 = 0.50
```

Per the discrimination gate: mere disconfirmation of H-C is insufficient
while H-E, H-F, or H-G remain live. H-F and H-G both remain live (RETAIN_AS_OPEN).
Therefore:

```
C = 0
```

## 8. R, Q, C, A and G_DEDUP06

```
R = 1   (correct referenced object retrieved — Document D located and read at docs/cd/CD3.pdf)
Q = 1   (referent readable and locatable — full OCR text, exact locators recorded)
C = 0   (H-F and H-G remain live; discrimination is partial, P_disc=0.50)
A = 1   (researcher accepts RETAIN_AS_OPEN_PENDING_PROSPECTIVE_GRANULARITY_RULE
         for the case as a whole -- this is acceptance of keeping the case open
         under the stated caveat, NOT acceptance of DEDUP-06 closure)

G_DEDUP06 = 1[R=1 AND Q=1 AND C=1 AND A=1] = 0   (C=0, so unchanged regardless of A)
```

**Researcher decisions (2026-09-09):**
```
H-F_RESEARCHER_DECISION = DEFER_EPISODE_RULE
  Reason: no explicit, source-grounded parent-episode rule currently exists; same
  date/commissioner/place are relevant but insufficient alone; no retrospective
  episode rule may be authored merely to close DEDUP-06.

H-G_RESEARCHER_DECISION = KEEP_CODED_ROW_FROZEN_WITH_DOCUMENTED_CAVEAT_PENDING_GRANULARITY_RULE
  Reason: do not split/merge/delete/normalize/rewrite the coded row; do not treat
  the current row as definitively correct at the historical-event level; retain
  this representation-level caveat; defer corpus action until a prospective
  granularity and parent-episode rule is separately accepted.

DEDUP06_RESEARCHER_DECISION = RETAIN_AS_OPEN_PENDING_PROSPECTIVE_GRANULARITY_RULE
  Effective boundary: this is acceptance of keeping DEDUP-06 open under the
  stated caveat only. It is explicitly NOT acceptance of DEDUP-06 closure,
  NOT a promotion of R-O4, and NOT a mutation of AS86 or the coded row.
```

## 9. Estimand summary

```
P_local              = 6/6   = 1.00
P_locator            = 6/6   = 1.00
P_mapping            = 4/5   = 0.80
P_coding_provenance  = 5/6   = 0.833
P_reading            = 3/3   = 1.00
P_disc               = 3/6   = 0.50
```

Every denominator is enumerated above. None of these estimands establishes
historical truth, causal identification, or authorizes any corpus mutation.

## 10. Frozen state — confirmed unchanged

```
DEDUP-06 = UNRESOLVED
G_DEDUP06 = 0
R-O4 = FAIL
AS86 = FROZEN_UNCHANGED
D1_prior = NOT_EVALUABLE
G_seg_prospective = 1, prospective only
G_ontology = 0
G_causal = 0
G_reconsider_future = 0
Hawkes fitting = SUSPENDED
Hawkes visualization = SUSPENDED
V2-B = BLOCKED
Phase D = CLOSED / MUST NOT BE RERUN
SERVER_SYNC = NOT_EXECUTED
PRODUCTION_DEPLOYMENT = NOT_EXECUTED
```

## 11. Guardrail confirmation

No external source retrieved or downloaded in this operation. No committed
Wave 1 or earlier artifact edited. `docs/cd/CD3.pdf` not modified or copied.
The coded row was not split, merged, deleted, or rewritten. No parent
episode was asserted. H-E, H-F, and H-G were not suppressed to fit the
original A/B/C frame. No model execution, ontology/causal promotion, or
Git/server/production operation occurred. Exactly four new files created,
all under `.../evidence_acquisition/wave2_act01/`.

## 12. Recommendation

```
WAVE2_LOCAL_DOCUMENTARY_MAPPING_FROZEN_DEDUP06_RETAINS_OPEN
```

The researcher has accepted `DEFER_EPISODE_RULE` (H-F) and
`KEEP_CODED_ROW_FROZEN_WITH_DOCUMENTED_CAVEAT_PENDING_GRANULARITY_RULE`
(H-G), and `RETAIN_AS_OPEN_PENDING_PROSPECTIVE_GRANULARITY_RULE` for
DEDUP-06 as a whole. This is acceptance of keeping the case open under the
stated caveat only — not acceptance of DEDUP-06 closure. No episode rule
was authored; the coded row was not modified.

**Pausing for researcher adjudication.**
