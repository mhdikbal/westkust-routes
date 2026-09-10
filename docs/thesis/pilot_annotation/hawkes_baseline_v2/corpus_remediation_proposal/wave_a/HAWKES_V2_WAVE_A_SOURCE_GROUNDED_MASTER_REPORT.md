# HAWKES V2 — WAVE A SOURCE-GROUNDED REMEDIATION PROPOSAL

```
Authoritative pre-operation HEAD = e0b682d958e4305b898eec70c373b0bee3683dbb
Operation type = source-grounded read-only adjudication, proposals only
Corpus mutation = NOT AUTHORIZED (none performed)
```

## 0. Scope lineage

`N_audit=141` (source table, sha256 `40c3affe6c8a431273fb4d20e10f0b1ddfe4350b2870722c9691bb4ed5b39f0c`) →
`N_B_metadata=118` (METADATA_LEVEL_CANDIDATE_UNIVERSE — a mechanical 5-flag union, not a completed rule application, not a model-input denominator) →
`N_A=9` (Wave A: `I_i^A = 1[D_i=1 OR M_i=1]`, recomputed from the source table; **overlap between the 6 dedup rows and 3 multi-source rows = 0**, so `N_A=9` exactly, not assumed).

Wave A primary IDs (9): `EVT-1687-gm-vol04-05-162-a6b1`, `EVT-1681-CD3-239-27a2`, `EVT-1682-CD3-309-b42a`, `EVT-1687-CD3-436-b331`, `EVT-1686-buku_vogel_1690-722-2078`, `EVT-1755-buku-padang-1718-238-0727`, `EVT-1686-buku-vogel-1690-458-fa01`, `EVT-1781-botham-letter-1781-1-d154`, `EVT-1781-kathirithamby-1965-314-6c8a`.

Dependency IDs (3, not counted in N_A): `EVT-1686-eic-bl-ior-g35-198-171c`, `EVT-1781-botham-letter-1781-1-5a01`, `EVT-1781-botham-letter-1781-1-5333`.

## 1. GM passage — read directly this operation

**Locator**: `docs/thesis/GM/xml/05/p0162.xml`, line 987 (`<note mark="1">`) and a second, separate `<remark>` block a few lines later (same file, printed page 179 region).

**Quoted (note mark 1, attached to "den Radja Itam" in the main paragraph)**:
> "...genegen sijnde tot het verevenen harer verschillen den Radja Itam [note: Met dezen Radja Hitam werd door Lobs 22 dec. 1687 een contract afgesloten, zo ook met de 12 penghulus van Bajang, vgl. Corpus III, nr. D.] tot Troessang altoos te versoeken..."

**Quoted (separate remark block, same file)**:
> "«Daarmee zijn de Sapuluh Buah Bandar weer in rust; contract met Tarusan, Corpus III nr. Dl, 22 dec. 1687, de bedoeling is, dat het hoofd niet onder 'panglima radja staat...»"

The main narrative paragraph is genuinely about **both** facts at once: the Bajang regents' preference to defer unresolved disputes to Radja Itam of Tarusan, *and* their own joint-governance arrangement. Note mark 1 cites "nr. D" loosely for this combined narrative point. The separate remark block — a distinct, more precise editorial layer in the same source file — cites **"nr. Dl"** explicitly and only for the Tarusan contract. This is the textual basis for treating D and Dl as related-but-distinct instruments, not one citation loosely covering both.

## 2. CD3 Document D and Document Dl — read directly this operation

| | Document D | Document Dl |
|---|---|---|
| Heading | *(untitled, "Acte van authorisatie...")* | "Dl. SUMATRA'S WESTKUST." |
| Printed pages | 442–443 | 444–446 |
| PDF pages (index) | 452–453 | 454–456 |
| Actors | Jacob Lobs; 12 named Bajang regents | Jacob Lobs; Radja Itam (king of Tarusan) |
| Place | Bajang | Tarusan/Troessang |
| Act | Authorization of 12 regents' joint interim rule | Tarusan king accepts VOC as protector/arbiter |
| Date | 22 December 1687 | 22 December 1687 |
| Archival register | Overgecomen brieven 1691, 22e boeck, folio 547 | same register, folio 545v |

**GM_SOURCE_INSPECTION_STATUS = FULLY_INSPECTED** (this operation). **CD3_DOCUMENT_D_INSPECTION_STATUS = FULLY_INSPECTED**. **CD3_DOCUMENT_DL_INSPECTION_STATUS = FULLY_INSPECTED**.

### Three-way mapping (corrected, kept separate, not conflated)

- **GM Bayang clause vs. Document D**: `EVIDENCE_COMPATIBLE_BUT_TEXTUALLY_DEPENDENT`, `X_dep=TEXTUALLY_DEPENDENT` — GM's note mark 1 explicitly cites "Corpus III, nr. D." This is textual dependence on the CD3 editorial apparatus, **not independent corroboration**.
- **GM Radja Itam/Tarusan clause vs. Document Dl**: `EVIDENCE_COMPATIBLE_BUT_TEXTUALLY_DEPENDENT`, `X_dep=TEXTUALLY_DEPENDENT` — the separate remark block explicitly cites "Corpus III nr. Dl, 22 dec. 1687." Also textual dependence, **not independent corroboration**.
- **Document D vs. Document Dl**: `NOT_SAME_OCCURRENCE` (different polities, different instruments). **Shared representation proposal**: `EVIDENCE_SUPPORTS_SHARED_PARENT_WITH_SEPARATE_CHILDREN` (same commissaris, date, place, consecutive archival folios: one Lobs mission, two child instruments). Same-occurrence and shared-parent are kept as two distinct classifications, not conflated.

### DEDUP-06 recommendation (no closure)

`PROPOSE_COMPOUND_GM_REPORT_MAPPED_TO_TWO_SEPARATE_CHILD_OCCURRENCES_UNDER_ONE_SHARED_PARENT_EPISODE` — the GM report is textually dependent on both CD3 Document D and Document Dl, which are themselves two separate child instruments under one shared administrative parent (Lobs's 22 Dec 1687 Tarusan-area mission). **This is a proposal requiring researcher adjudication, not a corpus edit.** `DEDUP-06=UNRESOLVED`, `G_DEDUP06=0`, `R-O4=FAIL` preserved.

### Row 1 gates at the correct object level (date readiness does not erase identity)

```
G_date_document_D            = 1
G_date_document_Dl           = 1
G_date_coded_row             = 1
G_identity_coded_row         = 0   (ambiguous anchor: D, Dl, or composite)
G_unit_coded_row              = 0   (instrument not pinned to one document)
G_eligible_coded_row_proposal = 0
```

## 3. CD3 mismatched cases (239, 309, 436) — corrected framing

For all three: `DOCUMENT_TO_CODED_EVENT_MAPPING = CONFLICTING`.

- `EVT-1681-CD3-239-27a2` (printed p.239): VOC–Susuhunan–Cirebon fugitive-slave treaty clause (Java). No dateline in the inspected excerpt.
- `EVT-1682-CD3-309-b42a` (printed p.309): Ternate–Bouton–Saleyer territorial treaty (Maluku, references Governor Padbrugge 1677). No dateline in the inspected excerpt.
- `EVT-1687-CD3-436-b331` (printed p.436): Bantam treaty renewal.
  ```
  RETRIEVED_DOCUMENT_DATE       = 1687-12-04
  RETRIEVED_DOCUMENT_DATE_ROLE  = RESOLUTION_DATE
  CODED_EVENT_DATE_VALUE_STATUS = NOT_VERIFIABLE_FROM_CITED_DOCUMENT
  ```
  This is the Bantam act's own date — it is **not** evidence about the coded event's true date, because the cited document is mismatched and therefore cannot adjudicate anything about the coded event.

## 4. CD3 pagination validation (5 checkpoints, not 1)

```
printed 20  -> pdf idx 30  -> offset 10
printed 150 -> pdf idx 160 -> offset 10
printed 309 -> pdf idx 319 -> offset 10
printed 442 -> pdf idx 452 -> offset 10
printed 600 -> pdf idx 608 -> offset 8   <- discontinuity (back-matter index)
```
`G_pagination_uniform = 1` for the validated main-text range (20–442, covering all four Wave A CD3 citations); **not** claimed for the whole 625-page volume. The three content mismatches are preserved regardless of offset — retrieval is sound, content is mismatched.

## 5. Botham letter — corrected temporal reading

`docs/HenryBotham`, read in full. *"In the beginning of August an Express Packet arrived... a few days after... five Indiamen [arrived]... we... immediately ordered them on an Expedition against Padang."*

```
packet_receipt_interval : beginning of August 1781 (news of war arrives at Fort Marlborough)
letter/report date       : 12 October 1781
expedition_sequence      : packet arrives -> few days later 5 Indiamen arrive -> expedition ordered
                            -> Botham proceeds, summons Dutch Governor -> Governor surrenders "immediately"
                            -> subsequent possession of Pulau Cingkuak, Air Bangis, Pariaman
Padang capture date       : PADANG_EVENT_DATE_NOT_ESTABLISHED_BY_THIS_PASSAGE
```
No lower/upper event bound manufactured. The letter dates only its own composition (12 Oct 1781, `REPORT_DATE`) and the packet's arrival (early Aug); it never states a calendar day for the surrender.

## 6. Source-availability reconciliation (mutually exclusive, sums to N_A=9)

```
PRIMARY_SOURCE_AVAILABLE_AND_ON_TOPIC               : 2  (GM/D-Dl row; Botham d154)
PRIMARY_SOURCE_AVAILABLE_BUT_CONTENT_CONFLICTING    : 3  (CD3-239; CD3-309; CD3-436)
PRIMARY_SOURCE_UNAVAILABLE_WITH_DEPENDENCY_AVAILABLE: 1  (buku-vogel-1690-458, dependency BL_IOR available)
PRIMARY_SOURCE_UNAVAILABLE_NO_DEPENDENCY            : 2  (buku_vogel-722; buku-padang-1718)
CITATION_OBJECT_MISMATCH                            : 1  (kathirithamby-1965-314)
——————————————————————————————————————————————————————
TOTAL = 9 = N_A
```
Dependency rows excluded from this count, as required.

## 7. Estimands and descriptive proportions (no inferential test performed)

```
P_A            = 9/118  = 0.076
P_source       = 6/9    = 0.667  (located, on-topic or conflicting)
P_Gamma        = 0/9             (no row has all seven Gamma_i components SATISFIED)
P_date_assessed= 7/9    = 0.778  (sources actually inspected for date role)
P_date_ready   = 1/9    = 0.111  (G_date,i=1 -- row 1 only)
P_eligible     = 0/9
P_open         = 9/9    = 1.0
```
`G_binomial,q=0` throughout — descriptive only.

## 8. Wave A gates

```
G_scope,A       = 1
G_source,A      = 0   (P_source=0.667, not 1 -- reported honestly as partial, not forced to 1)
G_application,A = 0   (blocked by G_source,A)
G_proposal,A    = 0   (blocked by G_application,A; N_silent_mutations=0, N_unsupported_closures=0, N_denominator_shifts=0)
```
Even if these were 1: `G_corpus=0, G_reconsider=0, G_fit,m=0 for every model` — unconditionally preserved.

## 9. Frozen state confirmed unchanged

```
DEDUP-06=UNRESOLVED  G_DEDUP06=0  R-O4=FAIL
AS86=FROZEN_UNCHANGED  141-row table=UNCHANGED
G_corpus=0  G_reconsider=0  G_fit,m=0 for every model
```

## 10. Confirmation

No corpus file modified. No model fit, likelihood, AIC/BIC, residual, forecast, simulation, or Phase D rerun. ACT-07 not executed. Graphify not rebuilt. `.gitignore` not modified. Frontend/API/production untouched. `CORPUS_MUTATION_AUTHORIZATION=NOT_AUTHORIZED` on every row. Not staged, committed, or pushed — deferred to a separate researcher adjudication step.

## 11. Outputs

```
HAWKES_V2_WAVE_A_SOURCE_GROUNDED_MASTER_REPORT.md          (this file)
HAWKES_V2_WAVE_A_ROW_LEVEL_ONTOLOGY_AND_REMEDIATION.csv    (9 rows, key=event_id)
HAWKES_V2_WAVE_A_DATE_ROLE_SOURCE_STATEMENT_LEDGER.csv     (13 rows, key=date_statement_id DS-001..DS-013)
HAWKES_V2_WAVE_A_REPORT_TO_OCCURRENCE_AND_DEDUP_LEDGER.csv (6 rows, key=pair_id)
HAWKES_V2_WAVE_A_RESEARCHER_DECISION_MANIFEST.csv          (67 rows, key=row_id)
```
No sixth output. No candidate model-input corpus file created.

**Strongest allowed status**: `WAVE_A_SOURCE_GROUNDED_REMEDIATION_PROPOSAL_COMPLETE_RESEARCHER_ADJUDICATION_REQUIRED`
