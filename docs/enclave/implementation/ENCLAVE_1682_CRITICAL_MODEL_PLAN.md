# Enclave 1682 — Critical Model & Interface Redesign Plan

Status: **design only, nothing implemented — REVISED, pending re-approval**
Scope: SALIDO-HDT model (`docs/enclave/salido_hdt_model_v0_4_1/`, read-only) and `/riset/enclave-1682/`
Canonical datasets, solver snapshots, solver source, and Docker configuration are **not modified by this plan, by writing this document, or by this revision**.

This plan was written after reading the current canonical dataset (`02_persons.csv`, `06_human_groups.csv`, `10_inventory_items.csv`, `03_roles.csv`, `05_locations.csv`, `11_claims.csv`) and the model's existing governance documents (`docs/HUMAN_CLASSIFICATION.md`, `docs/ETHICAL_MODELING.md`, `docs/UNCERTAINTY_POLICY.md`, `docs/ROLE_TAXONOMY.md`, `docs/SOURCE_PROVENANCE.md`, `docs/PETRI_NET_MODEL.md`). This revision additionally extracted and read the raw DOCX text of `docs/enclave/enklave-salido.docx` directly (via its `word/document.xml`), because the first draft's restraint-device finding turned out to be wrong precisely because it checked only the canonical CSVs and not the underlying source document — see §0.

---

## 0. Revision history — why the previous draft's claims changed

The first draft of this plan was rejected for two errors. Both are corrected below, and both were independently re-verified during this revision (not simply accepted on the requester's word) before being written in.

**Revision 1 — restraint devices were wrongly declared absent.**
The first draft searched only `10_inventory_items.csv` and `00_source_passages.csv` (the canonical, already-extracted CSVs) for shackle/chain/key terms, found one ambiguous padlock, and concluded no restraint-device evidence existed. That search missed the source entirely: this revision extracted the raw text of `docs/enclave/enklave-salido.docx` directly (`word/document.xml`, unzipped and stripped of markup) and found two explicit entries the CSV extraction never captured:

> `1 belenggu dengan lima gelang dan satu kunci` — "1 belenggu (shackle/fetter) with five rings and one key" — listed among cannon/musket ammunition in the main "Ammunitie van oorlogh" inventory (context: cannonballs, musket shot, gunpowder, bessagaijen spears; muskets in this same list are placed "15 di rumah kepala; 3 di Zuijder-Schacht; 1 di Princestolle").
>
> `1 belenggu dengan tiga gelang dan satu kunci` — "1 belenggu with three rings and one key" — listed in the Lieutenant Waker military-inventory transfer at Beneden-Pagger, signed 6 January 1682, handed over by Johan Hoffman and received by Johan Pleijtner (the same transfer that already appears in the canonical `transferred_military_inventory` rows for muskets and musket balls).

Neither entry appears in `10_inventory_items.csv` or `00_source_passages.csv` under any search term. This is a genuine gap between the DOCX source and the canonical extraction — not a disagreement about how to read the same row, but a row that is documented in the source and missing from the canonical dataset entirely. The first draft's error was treating "not found by my search of the canonical CSV" as equivalent to "not in the source," which is exactly the "absence of evidence as evidence of absence" fallacy `docs/UNCERTAINTY_POLICY.md` already prohibits — the draft cited that policy while violating it. §4 and §5 below are rewritten accordingly: restraint-device *presence* is now treated as explicit and confirmed (by direct DOCX read), while *use*, *target person*, and *date of use* remain unrecorded and their non-existence is not assumed either — both entries are routed into a required extraction audit (§5, §15) rather than either asserted or dismissed.

**Revision 2 — the 372-person aggregate total silently double-counted an entire cohort.**
The first draft summed the `count` column across all 17 rows of `06_human_groups.csv` and reported 372. Re-verified this revision: 11 non-Madagascar-arrival group records sum to **244**; the Madagascar-arrival cohort has one parent record (`G-MADA-64`, count 64) *and* five component records that independently sum to **64** (`G-MADA-VJ-10`+`G-MADA-HJ-8`+`G-MADA-VM-30`+`G-MADA-HM-10`+`G-MADA-K-6` = 10+8+30+10+6 = 64). The naive sum (244 + 64 + 64 = 372) counts the same 64-person cohort twice — once as the parent record, once as the sum of its own breakdown. This is a parent/child hierarchy relationship, not two disjoint populations, and the first draft's own §5 already *designed* a `23_group_hierarchy.csv` schema capable of describing exactly this relationship without ever applying it to its own headline number. The 11.8%-named statistic built on top of 372 is withdrawn along with it. §2, §8, and §9 below are rewritten to report record counts, cumulative (unsafe) sums, the identified duplicate, and a provisional de-duplicated estimate as separate, clearly labelled figures — never collapsed into one "the total is N" statement, and never used to compute a naming percentage until a verified unique-person count exists (§8's six-tier distinction).

**Revision 3 — the "canonical-extraction gap" itself was never real; withdrawn.**
Revision 1 (above) correctly found the two restraint-device passages in the DOCX, but its claim that "neither entry appears in `10_inventory_items.csv`" was never verified by a direct row-level check against that specific file for the literal Indonesian term "belenggu" — the search that produced that claim used a list of other restraint-related terms (`boei`, `ketting`, `slot`, `sleutel`, `gevangenis`, `rantai`, `gembok`, `borgol`, `kurungan`, `handboei`, `voetboei`, `iron ring`, `shackle`, `chain`) that did not include "belenggu" itself. A later, dedicated Phase A0 ticket (`A0-5`, read-only diagnosis) ran `grep -n "belenggu" 10_inventory_items.csv` directly and found both entries already present:

```text
SP-01267 -> INV-0343  (Ammunitie van oorlogh, category=military_inventory, location=L-SALIDO)
SP-01344 -> INV-0401  (Waker transfer, Beneden-Pagger, category=transferred_military_inventory, location=L-BENEDEN-PAGGER)
```

Both rows are sourced from `DOC-INVENTORY-1682-01-04`, their `source_translation_full` matches the corresponding source passage exactly, and both sit correctly among their neighboring rows by `source_paragraph_index`. There is no parser omission, section filter, vocabulary filter, range truncation, or deduplication defect — the "canonical-extraction audit" required elsewhere in this plan (§4, §5, §15) is accordingly **withdrawn as a requirement for these two records specifically**. `evidence_status`/`review_status` are blank on both rows, matching every other row in the 403-row file — the pre-existing, corpus-wide metadata-population gap (`REVIEW_QUEUE.md` §A), not evidence of absence, and not unique to these two rows. Everything else Revision 1 established remains true and unaffected: presence is explicit, and use/target person/date of use remain not_recorded and must never be inferred (P6, unchanged). §4, §5, §15, and §16 below are corrected accordingly; §10 and §11's broader coercion-infrastructure discussion is unaffected in substance (restraint-device presence was, is, and remains evidenced — only the "audit needed" framing is withdrawn).

Nothing else in the first draft is affected by these three corrections; sections not discussing restraint devices, the 372 figure, or the extraction-gap premise are unchanged from the approved-pending-revision draft.

---

## 1. Theoretical framing

**Critical Accounting Theory** (Tinker 1985; Hopper & Armstrong 1991; and its extension to slavery accounting — Fleischman & Tyson 2004; Rosenthal 2018 *Accounting for Slavery*) treats an accounting system not as a neutral record of economic fact but as a technology that constructs its objects: what gets a name, a rate, a column, a unit of measure is a decision with distributive consequences, not a mirror of reality. Rosenthal's core finding — that plantation double-entry bookkeeping rendered enslaved people simultaneously as labour, capital, and inventory through the same formal apparatus used for tools and stock — is the direct analytical precedent for this plan.

Applied here: the VOC personnel register (`DOC-PERSONNEL-1682-01-09`) is a single administrative act that produces two structurally different kinds of record from the same page:
- **individuated entries** for VOC officers and specialists (name, role, often a specific location and time window) — this becomes `02_persons.csv` + `04_person_roles.csv` + `07_human_role_location_time.csv`;
- **aggregated entries** for enslaved people, convicts, and dependents (a category label + a count) — this becomes `06_human_groups.csv`, with no per-person row at all.

The **analytical claim** this plan operationalizes is narrow and falsifiable, not a general moral pronouncement: *the same 1682 document that names 50 individuals with roles and movements records other people only as category totals, and that structural difference — not any claim about who did what labour — is what the data can support.* (The exact count of "other people" is itself under review — see §0 Revision 2, §8.) Critical Accounting Theory supplies the vocabulary (visibility, aggregation, commensuration, calculative technology) for describing this difference precisely instead of impressionistically.

**§0 Revision 1 sharpens this framing rather than complicating it**: the fact that the *researcher-prepared DOCX* records a restraint device by object-type (a "belenggu" with rings and a key) while the *canonical extraction pipeline* dropped it entirely is itself a second-order instance of the same phenomenon Critical Accounting Theory describes — visibility is produced and lost at multiple layers (archive → transcription → structured extraction), not only at the point of original colonial recording. This plan's own data pipeline is not exempt from the critique it applies to the 1682 register.

**Explicit rejection of the ontological-equivalence claim** (per task instruction, and consistent with `docs/ETHICAL_MODELING.md`'s "Core rule"): the model records enslaved people as countable and administratively adjacent to inventory *in the archive's own accounting practice*. This plan does not adopt that practice as its own ontology. §6 below implements a **dual ontology** specifically so that the "administrative treatment" view and the "human being" view are structurally two different graphs that must be explicitly cross-referenced, never one collapsed table.

---

## 2. Claims directly supported by current data

Verified by direct query against the canonical v0.4.1 CSVs and, where noted, the raw DOCX source (commands and counts below are reproducible from the files as they exist today; none required interpretation):

| # | Claim | Verification |
|---|---|---|
| C1 | 50 named individuals exist in `02_persons.csv`, each `entity_level=individual`, `source_status=named_in_docx`, with an `identity_confidence` value (mean 0.944). | `wc -l` + column scan |
| C2 | `06_human_groups.csv` contains **17 aggregate-group records**. This is a safe, direct record count. | row count |
| C3 | The 11 non-Madagascar-arrival group records sum to **244** people (`status_category`: 16 `enslaved` records total 241 of these, 1 `convicted_coerced` record — `G-COND-3`, "inlandse gecondemneerden" — accounts for 3). | sum of `count` column, filtered |
| C4 | The Madagascar-arrival cohort has a parent record `G-MADA-64` (count 64, `evidence_status=explicit_route`) **and** five component records (`G-MADA-VJ-10`=10, `G-MADA-HJ-8`=8, `G-MADA-VM-30`=30, `G-MADA-HM-10`=10, `G-MADA-K-6`=6) whose counts independently sum to **64**. Parent and components are the same cohort described at two levels of granularity, not two populations — summing both, as the first draft did, double-counts 64 people. | sum of `count` column for the 5 `G-MADA-*` child rows vs. parent row value |
| C5 | The **naive, uncorrected** sum of all 17 group records' `count` column is **372** (244 + 64 + 64). This number is a real, reproducible arithmetic result — it is **not** a safe person-count and must never be presented as one (§8). | full-column sum |
| C6 | A **provisional, single-document de-duplicated estimate** (counting the Madagascar cohort once, via either the parent or the five children) is **308** (244 + 64). This is still not a *verified unique-person count* — it does not yet account for possible cross-document overlap (§0 Revision 2, §8, §15). | 244 + 64 |
| C7 | `G-MANDOOR-8` (8 people) and `G-MANDORESS-3` (3 people) exist with `status_category=enslaved` — i.e., the document's own category places overseers of forced labour inside the enslaved population, not outside it. Confirmed against `docs/ROLE_TAXONOMY.md`'s `R-MANDOOR` / `R-MANDORESS` role definitions ("pengawas kelompok kerja paksa" / "pengawas perempuan dalam kelompok kerja paksa"). | direct row read + cross-reference to role taxonomy |
| C8 | Children are recorded in 3 separate aggregate categories by `kostgelt` (food-allowance) status: `G-KJ-4` (4, receives kostgelt), `G-CHILD-KOST-4` (4, receives kostgelt), `G-CHILD-NOKOST-19` (19, `parallel_reading` evidence status, without kostgelt) — plus `G-MADA-K-6` (6, unspecified) within the Madagascar cohort. No child has an individual record. | direct row read |
| C9 | `10_inventory_items.csv` contains a `military_inventory` / `transferred_military_inventory` category (19 serviceable muskets + spare parts at `L-SALIDO`; 3 more muskets + 1000 musket balls + 78 lb of assorted musket shot at `L-BENEDEN-PAGGER`, transferred from Lieutenant Waker) — i.e., weapons are recorded with an explicit `location_id`, meaning the model already supports spatial allocation of coercive-capacity-relevant equipment. | `category` column filter |
| C10 | **(Revised twice — was wrongly stated absent in the first draft; a follow-on claim that they were canonically unextracted was also wrong, withdrawn per §0 Revision 3.)** The raw DOCX source and the canonical dataset both explicitly record two restraint-device entries, in the same two ammunition-inventory sections as C9's weapons: `1 belenggu dengan lima gelang dan satu kunci` (Ammunitie van oorlogh, main store, source passage `SP-01267`, canonical row **`INV-0343`**) and `1 belenggu dengan tiga gelang dan satu kunci` (Waker transfer, Beneden-Pagger, 6 Jan 1682, Hoffman→Pleijtner, source passage `SP-01344`, canonical row **`INV-0401`**). **Both entries exist in `00_source_passages.csv` and `10_inventory_items.csv`** — confirmed by direct row-level query (`A0-5`); there was never a canonical-extraction gap. | direct DOCX `word/document.xml` text extraction (Revision 1) and direct `10_inventory_items.csv` row-level query for the literal term "belenggu" (Revision 3, `A0-5`) |
| C11 | `05_locations.csv` records `L-BENEDEN-PAGGER` and `L-BOVEN-PAGGER` as the two zones where the enslaved workforce groups are located (per `06_human_groups.csv`'s `location_id`), distinct from `L-OPPERHOOFTSWONING` (the VOC chief's residence) and `L-SIECKENHUIJS` (hospital) — a spatial correlate of the administrative asymmetry. | join `06_human_groups.location_id` against `05_locations.csv` |
| C12 | `docs/ETHICAL_MODELING.md` and `docs/HUMAN_CLASSIFICATION.md` already exist and already state the "people are not production resources" principle and a `status_category` vocabulary including `convicted_coerced`; this plan extends rather than originates that governance layer. | file read |

## 3. Claims that remain interpretations

These are historically reasonable readings consistent with the data but are **not themselves stated in any single source row** — they require connecting multiple records or applying an external analytical frame (Critical Accounting Theory) and must always render with `interpretation_confidence` and a visible "interpretation" badge, never as fact:

| # | Interpretation | Basis | Why it is not C-tier |
|---|---|---|
| I1 | The register's aggregation of enslaved people into category+count, versus individuation of VOC staff, reflects a distinct administrative logic of *commensuration* (rendering heterogeneous people into comparable, summable units) rather than merely a difference in record-keeping habit or paper economy. | C1–C6, Critical Accounting Theory literature | The register itself gives no rationale for its own recording choices; the *interpretation* of why is ours, the *fact* of the asymmetry is not. |
| I2 | The co-location of military inventory (C9) *and now the two restraint devices* (C10) with the enslaved workforce's recorded zones (C11) is evidence that the enclave's spatial organization combined production and coercive capacity in the same footprint. **Strengthened from the first draft** by C10 (an object-class capable of physically restraining a person, not only a weapon capable of general force projection), but still an interpretation: a restraint device recorded in an *ammunition* inventory list is unusual and notable, but its presence there does not by itself establish it was used on a person, when, or on whom (§4, C10). | C9 + C10 + C11 join | Co-location and object-type are not proof of use; the object's *affordance* (it is the kind of thing that can restrain a person) is a different, weaker claim than *documented use* (§4). |
| I3 | `G-MANDOOR-8` / `G-MANDORESS-3` (C7) represent an internal supervisory hierarchy *imposed on* enslaved people by the VOC administration, not a status people held voluntarily or with attendant privilege equivalent to free overseers. | C7 + `docs/ROLE_TAXONOMY.md` role gloss | The register states the category, not the lived experience or degree of coercion attached to holding it. |
| I4 | The absence of individual identity fields for the aggregated people (C2–C6) is itself an archival act with epistemic consequences for later reconstruction (i.e., it is not merely "data we don't have," it is "a category the source system was not designed to produce"). | C2–C6 | A structural claim about the source's design, defensible from the schema, but goes beyond simply reporting the counts. |
| I5 | The **provisional de-duplicated estimate** of 308 (C6) is a more defensible working figure than the naive 372 (C5) for describing "how many people this document's aggregate records concern," but it is still an estimate, not a verified count, pending the cross-document temporal-overlap review required in §8/§15. | C3 + C4 | De-duplication within one document's own parent/child structure is a solid, mechanical correction; ruling out overlap with *other* documents describing the same enclave in the same period is a separate, unfinished research question. |

## 4. Claims that are prohibited because evidence is insufficient

This section exists specifically because of `docs/UNCERTAINTY_POLICY.md`'s prohibition on "using absence of evidence as evidence of absence" and "presenting the solver's best scenario as fact" — extended here to the new critical layer, which is exactly as capable of overclaiming as the production model was. **The first draft violated this same policy in the opposite direction** — see §0 Revision 1 — by asserting absence where the canonical CSVs simply hadn't captured the source yet. The corrected position (below) draws the prohibition line at *use*, not at *presence*.

**Restraint devices — corrected position.** C10 establishes, from a direct read of the source DOCX, that two restraint devices ("belenggu," each with rings and a key) are **explicitly and unambiguously present** in the archive, both catalogued within military/ammunition inventory sections. What is **not** recorded, and must not be inferred:

- **actual use is not recorded** — no source line states the device was applied to a person, ever, in the covered period;
- **target person is not recorded** — no source line names or otherwise identifies who, if anyone, was restrained by either device;
- **date of use is not recorded** — the inventory date (1682-01-04 / the 6 January 1682 Waker transfer) is the date of the *inventory count*, not a date of use;
- the object's *coercive affordance* (a device of this general type is capable of restraining a person) is a category-level, defensible inference from the object's description; a claim about *this specific instance's actual deployment* is not.

**No canonical-extraction audit is required for these two entries (§0 Revision 3).** Both already exist as canonical rows (`INV-0343`, `INV-0401`) — there is nothing to extract and nothing to add. A separate, narrower open item remains: neither row's `evidence_status`/`review_status` field is populated, matching the corpus-wide gap affecting all 403 rows of `10_inventory_items.csv` (`REVIEW_QUEUE.md` §A), not something specific to these two. That general population pass — not a restraint-specific audit — is what would eventually set those fields; it does not gate presentation of these rows as evidenced, since presence is already explicit and unambiguous.

Other prohibited claims:

| # | Prohibited claim | Why prohibited |
|---|---|---|
| P1 | Any claim that a specific named individual (e.g., a mandoor or mandoress) treated the enslaved workforce with a specific degree of cruelty or leniency. | No source row describes treatment; only category and count exist. |
| P2 | Any claim assigning a numeric age to a `growth_category` (`halfwasse`, `volle`, `cleene_kinders`). | Explicitly prohibited already in `docs/HUMAN_CLASSIFICATION.md` and `docs/UNCERTAINTY_POLICY.md`; the critical layer inherits this prohibition unchanged. |
| P3 | Ranking enslaved groups by productivity, or optimizing the Petri net's coercion subnet to find an "efficient" coercive arrangement. | Explicitly prohibited in `docs/ETHICAL_MODELING.md` ("Counterfactual limits"); extended explicitly to the new coercion subnet in §7 below. |
| P4 | Presenting **372** (C5, the naive uncorrected sum), **308** (C6, the provisional de-duplicated estimate), or any other aggregate figure as a *verified unique-person count*, or as if each unit represented a documentable individual biography recoverable by better modelling. | C5/C6 are, respectively, an arithmetic artifact and a provisional estimate — neither is a verified count (§8's six-tier distinction); claiming otherwise misrepresents both the source and what CP-SAT reconstruction or graph modelling can do. |
| P5 | Treating `G-COND-3` ("inlandse gecondemneerden", convicted/coerced local people) as equivalent in legal or social status to `G-MS-121` etc. (enslaved) merely because both are `status_category`-adjacent in the schema. | The source uses a different original category (`gecondemneerden` = condemned/convicted, distinct from `slaven`); the model's `status_category` enumeration groups them under a shared `convicted_coerced` vs `enslaved` split specifically to avoid this collapse — the UI must preserve that split visibly, never flatten it into one "coerced" bucket. |
| P6 | Any claim that either restraint device (C10) was used, was used on a specific person, or was used at a specific date. | Directly contradicts the "not recorded" findings above; this is the single most important new prohibition in this revision, replacing the first draft's now-withdrawn "no restraint-device evidence exists" claim with a narrower, correctly-scoped one. |
| P7 | Silently resolving the DOCX-vs-canonical-CSV discrepancy (C10) by either (a) adding the two rows directly to `10_inventory_items.csv` without going through the project's normal extraction/review process, or (b) treating the discrepancy as closed once this plan documents it. | Per task instruction: the discrepancy is a data-pipeline defect requiring its own audit (§5, §15), not something this planning document is entitled to resolve unilaterally — and canonical datasets are out of scope for this plan regardless. |

---

## 5. New CSV schemas

All new files are **additive** to `docs/enclave/salido_hdt_model_v0_4_1/` — none of the 17 existing canonical CSVs are altered, consistent with the project's standing rule (`docs/DATA_DICTIONARY.md`, `V0_4_MIGRATION_PLAN.md`'s "Design principle applied to every item") that archival readings are never edited in place. These are new files at a sibling directory (not a modification of `v0_4_1/`) — see §17. **This revision reduces and renames the schema set** to the five required by the correction, folds two schemas from the first draft into them (noted below), and keeps two supplementary schemas that remain necessary for provenance/uncertainty tracking.

### `archival_visibility.csv` *(was `17_archival_visibility.csv`)*
One row per human entity **record** (individual or group record — not per represented person; see `group_hierarchy_review.csv` for person-count handling). Purely a derived/join table.

```
visibility_id, entity_id, entity_type (individual|aggregate_group),
is_individually_named (bool), has_role_record (bool),
has_location_time_record (bool), has_health_or_medical_reference (bool),
identity_confidence, source_document_id, computed_from
```
**Change from first draft**: dropped `aggregate_count` and any percentage field entirely — this file is now scoped strictly to documentary-visibility properties of a *record*, never to person-count arithmetic, which lives solely in `group_hierarchy_review.csv` so the double-counting bug (§0 Revision 2) cannot recur by two files disagreeing about a count.

### `accounting_treatment.csv` *(was `19_accounting_treatment.csv`, unchanged in structure)*
Encodes *how the source document formally treats* each human entity — the core Critical-Accounting-Theory instrument. One row per entity record.

```
treatment_id, entity_id, recorded_as (named_person|category_and_count),
adjacent_record_types (list; e.g. "inventory_items,weekly_operations"),
appears_in_same_document_section_as_inventory (bool),
appears_in_same_document_section_as_restraint_device (bool),
unit_of_measure_used ("none"|"count"|other), evidence_status,
source_document_id, source_passage_id, critical_note
```
One field added: `appears_in_same_document_section_as_restraint_device` — makes the I2 co-location observation queryable per-entity rather than only assertable in prose. `critical_note` is a short, source-grounded observation, only written if independently verifiable against `00_source_passages.csv`/DOCX paragraph adjacency, never a general moral gloss.

### `coercion_evidence.csv` *(was `20_coercion_evidence.csv`, unchanged in structure)*
One row per *documented* coercion-relevant fact — role (mandoor/mandoress structural position), status category (`convicted_coerced`), or a physical/procedural fact such as a restraint-device record.

```
coercion_evidence_id, entity_id_or_group_id, evidence_type
  (supervisory_role|legal_status|restraint_device|punishment_record|other),
evidence_status, source_document_id, source_passage_id, source_quote,
interpretation_confidence, prohibited_inference_flag (bool, default true),
reviewer, review_date
```
**Change from first draft**: this file is **no longer described as empty-by-default in principle** — with C10, `evidence_type=restraint_device` now has two real candidate rows, sourced directly from the already-existing canonical rows `INV-0343`/`INV-0401` (§0 Revision 3 — no extraction audit gates this; presence was confirmed by direct row-level query, not by a pending audit). `prohibited_inference_flag=true` remains the enforcement mechanism: it gates *use*-type claims (P6), not *presence*-type claims — a row can have `prohibited_inference_flag=true` for "was this used on person X" while still truthfully stating "a restraint device is recorded here" in its `source_quote`.

### `restraint_device_review.csv` *(new name for the retired `21_restraint_device_evidence.csv`; structurally rewritten, no longer ships empty)*
One row per restraint-device-relevant source passage. This is the technical home of the P6 prohibition (never a claim of use, target person, or date of use) — **not** an extraction audit workbench, since §0 Revision 3 found no extraction defect to audit.

```
review_id, source_document_id, source_passage_id, canonical_inventory_row_id,
source_quote_translated, device_type_original ("belenggu"),
ring_count, key_count,
inventory_section_context (free text, e.g. "Ammunitie van oorlogh, main store" |
  "Waker transfer, Beneden-Pagger, 1682-01-06"),
presence_status (explicit|not_stated|contested),
coercive_affordance_status (inferred_from_object_type),
actual_use_status (not_recorded — no other value permitted without a new source finding),
target_person_status (not_recorded — no other value permitted without a new source finding),
date_of_use_status (not_recorded — distinct from inventory date, never conflated with it),
canonical_extraction_status (present|missing|extraction_rejected),
reviewer, review_date, reviewer_note
```
`extraction_audit_required` and `image_review_required` are **removed from this schema** relative to the first two drafts — they described a workflow state (auditing a suspected-missing row) that does not apply once presence is confirmed by direct row lookup. **Seed content proposed (not written to any file by this plan — for the future implementation to populate):** two rows, one per C10 entry, `source_passage_id`/`canonical_inventory_row_id` filled from the confirmed mapping (`SP-01267`/`INV-0343`, `SP-01344`/`INV-0401`), `canonical_extraction_status=present`, `actual_use_status=not_recorded`, `target_person_status=not_recorded`, `date_of_use_status=not_recorded`. No canonical-CSV addition is proposed or needed for these two rows (contrast with §17, which still applies to any *other, genuinely missing* future finding).

### `group_hierarchy_review.csv` *(new name for the retired `23_group_hierarchy.csv`; restructured specifically to prevent the §0 Revision 2 bug, and absorbs the retired `22_administrative_aggregation.csv`'s person-count fields)*

```
review_id, group_id, parent_group_id (nullable),
group_level (independent|subgroup|arrival_cohort_parent|arrival_cohort_component),
record_person_count (the group's own `count` column value, as recorded — a fact, not an estimate),
counts_toward_unique_person_estimate (bool — exactly one of {parent, each child} may be
  true per cohort; enforced by a derivation-layer test, §16, not by convention alone),
duplicate_of (nullable — e.g. for G-MADA-64: "sum of G-MADA-VJ-10/HJ-8/VM-30/HM-10/K-6"),
cross_document_temporal_overlap_checked (bool, default false),
cross_document_overlap_notes,
evidence_status, reviewer, review_date
```
**This is the schema that directly implements §0 Revision 2's fix.** `counts_toward_unique_person_estimate` is a boolean *decision field*, not a derived flag — for the Madagascar cohort, the plan recommends (but a future reviewer must confirm) setting it `true` on the parent (`G-MADA-64`) and `false` on all five children, so `SUM(record_person_count WHERE counts_toward_unique_person_estimate)` across the whole table always yields a de-duplicated total by construction, and a regression test (§16) enforces that invariant so it cannot silently regress the way the first draft's naive sum did.

### Supplementary schemas (carried over from the first draft, still required for provenance/uncertainty tracking, not part of the five explicitly requested but not retired either)

**`provenance_critical_layer.csv`** *(was `24_provenance_critical_layer.csv`)* — standard provenance chain (per `docs/SOURCE_PROVENANCE.md`) applied to every derived claim produced by the critical layer itself.
```
provenance_id, derived_claim_id, derivation_method (direct_query|join|interpretation),
source_tables (list), computed_by, computed_date, reproducible_query
```

**`uncertainty_critical.csv`** *(was `25_uncertainty_critical.csv`)* — extends `docs/UNCERTAINTY_POLICY.md`'s confidence-component model to interpretive claims, with `claim_tier` now explicitly required to be one of the tiers this revision defines (§2/§3/§4, and §8's six count-tiers for any person-count claim specifically).
```
uncertainty_id, claim_id, claim_tier (data_supported|interpretation|prohibited),
count_tier (named_person_record_count|aggregate_group_record_count|
  cumulative_recorded_count|parent_child_duplicated_count|
  unique_person_estimate|unique_person_verified_count|not_applicable),
reading_confidence, identity_confidence, relation_confidence,
interpretation_confidence, composite_note
```
`count_tier` is new in this revision — added specifically so no future claim about "how many people" can be logged without stating which of §8's six tiers it belongs to.

### Retired from the first draft

- `18_naming_asymmetry.csv` — retired. Its safe, structural findings (schema asymmetry, evidence-status asymmetry) are kept as prose in §9, sourced directly from `02_persons.csv`/`06_human_groups.csv` column presence, with no rate/percentage field; its unsafe field (`pct_individually_named`, computed from the now-withdrawn 372) is deleted, not replaced.
- `22_administrative_aggregation.csv` — retired; its `individuals_represented` field was structurally the exact place the double-counting bug could recur, so its person-count responsibility is fully absorbed into `group_hierarchy_review.csv` above (single source of truth for person-count arithmetic), and its `aggregation_basis`/`individuation_possible` fields are absorbed into `archival_visibility.csv`'s `computed_from` and `accounting_treatment.csv`'s `recorded_as`.

---

## 6. Ontology and knowledge-graph design

### Dual ontology

**View A — Colonial Accounting Ontology** (what the source document does):
```
Document --records--> AccountingEntry
AccountingEntry --classifies_as--> {NamedPersonEntry | AggregateGroupEntry}
AccountingEntry --uses_unit--> {name+role | category+count}
AccountingEntry --co-located_with--> InventoryEntry | OperationEntry | RestraintDeviceEntry
```
`RestraintDeviceEntry` added this revision (was absent — the first draft's ontology had nowhere to put C10 even hypothetically). This graph is intentionally structured to mirror the archive's own logic, including its aggregation — it is not sanitized. Its purpose is to make the accounting logic itself analyzable (Critical Accounting Theory's object of study), not to be presented to a reader as the primary or default lens.

**View B — Human-Centred Critical Ontology** (who the record is about):
```
Person (named or represented-in-aggregate)
  --has_documentary_visibility--> VisibilityRecord (archival_visibility.csv)
  --subjected_to_status--> StatusCategory (VOC_employee | enslaved | convicted_coerced | dependent_child | ...)
  --if_named--> IndividualBiographyFragment (role, location, time — from existing 02-07 tables)
  --if_aggregated--> AggregateGroupMembership (group_hierarchy_review.csv — record_person_count only,
      never a synthetic per-person node)
      --part_of--> GroupHierarchy (group_hierarchy_review.csv)
  --coercion_context--> CoercionEvidence (coercion_evidence.csv, gated by prohibited_inference_flag)
```
`Person` here is a superclass that both a `02_persons.csv` row and a "share of a `06_human_groups.csv` count" can instantiate — critically, **an aggregate-group membership does not get a synthetic per-person node**. `AggregateGroupMembership` stays at group granularity; this is the technical implementation of the "no invented identities" rule already stated in `docs/HUMAN_CLASSIFICATION.md`'s Scope section, and it is also, as of this revision, the mechanism that keeps person-count arithmetic in exactly one place (`group_hierarchy_review.csv`) instead of being re-derivable (and re-breakable) from graph traversal.

**Explicit cross-reference layer** (not a merge): a single `same_document_event` edge type connects nodes in View A and View B when they derive from the same `source_document_id` + `source_passage_id`, so a reader can move between "how the archive recorded this" and "who this was about" without the two views ever being silently collapsed into one table.

### Knowledge-graph node/edge types

Nodes: `Document`, `Passage`, `NamedPerson`, `AggregateGroup`, `Role`, `Location`, `InventoryItem`, `RestraintDeviceRecord` (new — instantiated only from `restraint_device_review.csv` rows, always carrying `actual_use_status=not_recorded` etc. as node properties, never omitting them), `AccountingEntryType`, `CoercionEvidenceItem` (only instantiated for reviewer-approved rows), `Claim`.

Edges: `records`, `classifies_as`, `performs_role`, `located_at`, `co_located_with` (same document section — now includes `AggregateGroup`↔`RestraintDeviceRecord` edges per C10), `part_of_hierarchy`, `has_visibility_record`, `has_coercion_evidence` (gated), `interprets` (View-A-to-View-B cross-reference, always carries `interpretation_confidence`).

---

## 7. Critical Petri Net design

Extends, does not replace, the existing `docs/PETRI_NET_MODEL.md` (production-only net, "Specification in Development," not yet simulated per the current `/riset/enclave-1682/` page). Three subnets, sharing token types with the existing model plus one new token type.

### New token type: `CoercionContextToken`
```text
entity_id_or_group_id, coercion_evidence_ids (list, only approved rows),
supervisory_role_present (bool), restraint_device_present_in_section (bool),
status_category, evidence_confidence
```
`restraint_device_present_in_section` added this revision — a boolean *presence* flag only, never a use/intensity value. Carries **context**, never a "coercion intensity" scalar — there is no numeric coercion score anywhere in this design, precisely to foreclose the productivity-ranking-of-coerced-groups prohibition (P3, `docs/ETHICAL_MODELING.md`).

### Subnet 1 — Production
Identical in structure to the existing `docs/PETRI_NET_MODEL.md` (Workers_Available → ... → Shipment_Ready). Unchanged by this plan; referenced, not modified.

### Subnet 2 — Reproduction and maintenance
New places modelling the *conditions of continued presence* that production-only models omit: `Housing_Assigned`, `Food_Allowance_Recorded` (fed by `kostgelt` status), `Medical_Care_Available` (`L-SIECKENHUIJS`, `R-SIECKENVADER`/`R-OPPERMEESTER` roles), `Child_Dependent_Status`, `Arrival_Cohort_Processed` (for the Madagascar cohort — reads `group_hierarchy_review.csv` to process it once, at whichever hierarchy level `counts_toward_unique_person_estimate=true` designates, never once per parent-and-children). Transitions: `Assign_Housing`, `Record_Kostgelt_Status`, `Provide_Medical_Care`, `Process_Arrival_Cohort`.

### Subnet 3 — Coercion and control
Places: `Supervisory_Assignment_Active` (fed by `R-MANDOOR`/`R-MANDORESS` role tokens), `Legal_Status_Recorded` (`convicted_coerced` category), `Movement_Constrained` (only instantiated where `07_human_role_location_time.csv` shows an explicit spatial/temporal constraint — not inferred generally), `Restraint_Device_Context` (**revised**: this place is now populated by tokens once the extraction audit in `restraint_device_review.csv` completes and a `coercion_evidence.csv` row exists with `evidence_type=restraint_device` — but its outgoing guard still requires `target_person_status != not_recorded` before any arc can connect it to a *specific* `HumanToken`, which under current evidence can never fire, per P6. The place can therefore hold "a restraint device is documented in this section" context tokens today, while remaining structurally incapable of asserting "this device restrained this person" until new evidence changes `target_person_status`). Transitions: `Assign_Supervision`, `Record_Legal_Status`, `Apply_Movement_Constraint` (guarded), `Record_Restraint_Device_Presence` (new — fires on audit completion; deliberately has no counterpart transition asserting use).

**Cross-subnet arcs**: shared places connect Subnet 1 and Subnet 3 — e.g., `Workers_Assigned` (production) requires a token from `Supervisory_Assignment_Active` (coercion) when the assigned entity's `status_category` is `enslaved` or `convicted_coerced`, but not when it is `VOC_employee`. This makes the differential administrative structure a *structural* property of the net (different token paths for different status categories) rather than a narrative claim layered on top.

**Explicit guard against P3**: no transition in Subnet 3 has an `objective_value`, cost function, or optimization target. The solver (`salido_hdt.solver.cli`, CP-SAT) is explicitly scoped in `docs/ETHICAL_MODELING.md` to feasibility/uncertainty questions only; this plan does not propose extending CP-SAT optimization into Subnet 3, and any future implementation must not do so without new, explicit ethical review — this is a hard boundary, not a phase-2 TODO.

**Explicit guard against P6**: `Restraint_Device_Context`'s guard structurally cannot connect to a specific `HumanToken` under current evidence, as described above — this is enforced at the net-specification level, not left to implementation discipline alone.

**Simulation status**: like the existing production net, this remains **specification only**. No simulation engine is proposed or scheduled in this plan.

---

## 8. Archival visibility metrics

**This section is rewritten in full.** The first draft's single "11.8% individually named" statistic is withdrawn (§0 Revision 2) and replaced with an explicit six-way distinction the task requires. Only the first two tiers are currently safe to present as direct canonical summary metrics; the remaining four require the review work described in §5/§15 before any of them can be shown as a finished number.

| Tier | Definition | Current value | Status |
|---|---|---|---|
| 1. Named-person record count | Rows in `02_persons.csv` | **50** | ✅ Safe direct canonical summary metric |
| 2. Aggregate-group record count | Rows in `06_human_groups.csv` | **17** | ✅ Safe direct canonical summary metric |
| 3. Cumulative recorded count value | Naive sum of all 17 groups' `count` column | **372** | ⚠️ Real arithmetic result, but **not a person count** — includes the Madagascar parent/child duplication (§0 Revision 2); may be shown only labelled explicitly as "cumulative recorded value, includes a known duplication," never as "total people" |
| 4. Parent-child duplicated count | The identified overlap between `G-MADA-64` and its five children | **64** | ⚠️ Identified, mechanically certain (parent count exactly equals sum of children) |
| 5. Unique-person estimate | Provisional single-document de-duplication: 244 + 64 | **308** | ⚠️ Provisional — resolves the *within-document* duplication only; does not account for possible cross-document overlap |
| 6. Unique-person verified count | A count confirmed not to double-count within *or across* documents describing this enclave in this period | **currently unresolved** | ❌ Not computable from this dataset alone — requires the cross-document temporal-overlap review specified in §15 before any number may be published here |

No naming-rate percentage (individually-named ÷ total) is computed anywhere in this plan, because every candidate denominator above tier 2 is either an unsafe cumulative value (tier 3) or a provisional/unresolved estimate (tiers 5–6). A future implementation may compute and display a rate **only** once tier 6 is populated, and even then it should be presented as "at least X%, pending further cross-document review" rather than a bare percentage, consistent with `docs/UNCERTAINTY_POLICY.md`'s prohibition on silently correcting totals.

**Per-status breakdown (tier-3-safe subcomponents, still not summed into a person total)**: `VOC_employee`-adjacent named persons make up effectively all 50 named individuals (all hold roles per `03_roles.csv`/`04_person_roles.csv`; no named person in the current dataset is recorded as `enslaved`). Group records by `status_category`: 16 `enslaved` records (summing, at tier 3, to 369 before de-duplication / 305 after, since 4 of those 16 are the double-counted Madagascar-related component/parent rows), 1 `convicted_coerced` record (3 people, `G-COND-3`).

These metrics — specifically tiers 1, 2, and the *labelled* tier-3/4/5 figures — are the quantitative backbone of the redesigned page's opening section (§11); they replace the current "KPI cards" framing (persons/groups/inventory/operations/anomalies as equivalent tiles) with an explicitly tiered set of figures instead of one collapsed asymmetry statistic.

---

## 9. Naming-asymmetry analysis

Structural, not narrative — sourced directly from `02_persons.csv`/`06_human_groups.csv` column presence, cross-tabulated by `status_category` and `growth_category_original`. No rate/percentage is computed (§8). Three findings, all directly derivable from existing columns and unaffected by the §0 Revision 2 count correction:

1. **Role-bearing named individuals** (50) span `Administration`, `Craft`, `Governance`, `Logistics`, `Medical`, `Military`, `Production`, `TechnicalMining` role families (`docs/ROLE_TAXONOMY.md`) — the full breadth of the taxonomy. Every aggregate group's only "role" field, where present at all, is a coarse category (`mandoors`, `voorslager`) with no individual attached.
2. **The schema itself encodes the asymmetry**: `02_persons.csv` has an `identity_confidence` column; `06_human_groups.csv` has none — there is structurally no place to record "how confident are we in this specific person's identity" for an aggregated person, because there is no specific person in the row.
3. **Evidence-status asymmetry**: named-person claims (`11_claims.csv`) are predominantly `explicit`; one aggregate group (`G-CHILD-NOKOST-19`, 19 children without kostgelt) carries `evidence_status=parallel_reading` — the model's existing uncertainty vocabulary already flags that this particular count required cross-reading, worth surfacing prominently rather than left undifferentiated from `explicit` rows.

A fourth finding is added this revision: **the extraction-layer asymmetry (§0 Revision 1)** — the two restraint-device entries (C10) were captured in the researcher-prepared DOCX but dropped during canonical CSV extraction, while comparable weapon entries in the same inventory sections (muskets, ammunition) *were* captured. Whether this reflects a systematic pattern (e.g., object categories the extraction pipeline's category vocabulary didn't anticipate) or an isolated omission is itself an open question the required extraction audit (§15) should establish, since it bears on whether other non-canonical-vocabulary items might also be missing.

---

## 10. Coercion-infrastructure model

**Revised.** What the current data (including the DOCX-level finding, C10) supports:

- **Administrative/supervisory infrastructure**: `R-MANDOOR`/`R-MANDORESS` roles (C7) — a documented supervisory structure over the enslaved workforce, itself staffed by enslaved people (`status_category=enslaved` for both `G-MANDOOR-8` and `G-MANDORESS-3`).
- **Legal-coercive category**: `G-COND-3`, `status_category=convicted_coerced`, distinct from `enslaved` — the source's own category for judicially coerced labour.
- **Spatial co-location of military capacity and restraint devices**: muskets/ammunition (C9) *and now two restraint devices* (C10) at `L-SALIDO` and `L-BENEDEN-PAGGER` (C11) — presented as co-location, explicitly flagged as interpretation (I2) when connected to workforce control rather than, e.g., generic armory storage practice of the period.
- **Physical restraint apparatus**: **explicitly present** (C10), unlike the first draft's finding. **Use, target, and date of use are not recorded** (§4) and must never be inferred (P6). Both entries are pending a required extraction audit (§5, §15) before appearing in any UI as reviewed evidence.

The "coercion-infrastructure model" therefore now has three evidenced components (supervisory hierarchy, legal-coercive category, and confirmed-but-unaudited restraint-device presence) plus one interpretation (spatial co-location as evidence of combined production/control function) — a materially stronger evidentiary basis than the first draft's single padlock, but still bounded tightly at the "use" question by design.

---

## 11. Revised page information architecture

`/riset/enclave-1682/` — new section order (solver explicitly moved below archival/critical content, per task instruction; **revised from the first draft** at items 2 and 6):

1. **Header** — title, subtitle, provenance strip (unchanged).
2. **Archival Visibility Summary** (replaces current flat KPI-tile grid) — §8's tiered table (named-person record count, aggregate-group record count, then the labelled cumulative/duplicate/estimate/unresolved figures), **not** a single headline percentage. Each figure individually sourced and clickable through to its CSV row(s).
3. **Dual Ontology Toggle** — two labelled views over the same underlying data:
   - *Colonial Accounting View*: current-style tiles (named persons / aggregate groups / inventory rows / operations / anomalies), explicitly captioned "this is how the 1682 register itself organizes this information."
   - *Human-Centred Critical View*: person-and-group cards showing role/location/status for named individuals, and group-cards for aggregates showing category, `record_person_count`, `kostgelt` status, and hierarchy position — explicitly not attempting to individuate, and explicitly not summing group counts into a headline total on this view either (§8).
4. **Naming Asymmetry** — §9's four findings (including the new extraction-layer finding), with the schema-level evidence shown, no headline ratio.
5. **Administrative Aggregation & Group Hierarchy** — `group_hierarchy_review.csv` rendered as a tree (independent groups → subgroups; Madagascar parent → its five components, visually marked so a reader can see the parent/child relationship that prevents double-counting, not just the tree shape), replacing the current adapter's hardcoded, internally-inconsistent `HUMAN_GROUP_HIERARCHY` (see §5, §15 Phase A).
6. **Coercion Context** (§10) — supervisory hierarchy, legal-coercive category, spatial co-location (interpretation-flagged), **and** restraint-device presence with its full "explicit presence / affordance vs. use / not recorded: use, target, date" breakdown, plus an explicit "canonical-extraction audit pending" status badge on both entries.
7. **Methodology & Evidence Legend** — current section, extended with the new evidence-tier definitions (§3/§4) and §8's six count-tier definitions, alongside the existing evidence-status badges.
8. **Solver Snapshot (Offline)** — current section, **moved here** (previously section 2 of the page). Framing sentence unchanged from the first draft: "The figures below describe a CP-SAT feasibility reconstruction of task assignment. They are downstream of, and subordinate to, the archival and critical-interpretation sections above — they do not describe coercion, only tool/location/task feasibility."
9. **Petri Net Status** — current section, extended to mention all three subnets (§7) as "specification in development," unchanged simulation status, with `Restraint_Device_Context`'s guard behaviour (§7) explicitly documented.
10. **Footer** — as today, entity counts corrected per the recently-shipped fix (`ce74aca`) **and** per §8's tiered figures (no single "N total entities" footer line; if a footer summary is kept, it must state the tier it refers to), extended with a link to this plan document.

---

## 12. Visual design principles

- **No single color scale spans both ontology views.** The Colonial Accounting View keeps the existing neutral tile palette; the Human-Centred Critical View uses a visually distinct (but still accessible, non-alarmist) palette so a reader always knows, from color alone, which lens they are in.
- **No count figure is ever shown without its tier label visible in the same glance** (§8) — replaces the first draft's narrower "no percentage bar chart" rule, generalized to cover all six count tiers, not just the withdrawn percentage.
- **Aggregate group cards are visually distinct from individual person cards** by shape/density (denser, count-forward, no portrait/name slot) — a deliberate anti-pattern against later feature requests to "make it feel more personal" by inventing avatars or names for aggregate entries, which `docs/HUMAN_CLASSIFICATION.md` already forbids.
- **Restraint-device entries are represented as plain, labelled text/table rows only — no illustrative iconography of bondage, restraint, or violence anywhere on the page, regardless of section.** **Revised rationale**: the first draft justified this by claiming no such evidence existed; that claim is now withdrawn (C10). The rule itself is *kept*, but for the correct reason — presence is confirmed, but use/target/date are not, and any illustrative depiction (even a neutral icon) would visually imply a use-claim the text explicitly disclaims. The restriction is now evidentiary-scope discipline, not evidentiary absence.
- Typography/layout otherwise inherits the current page's established system (EB Garamond/Space Grotesk, existing token set) — this plan does not propose a visual identity change, only new sections within it.

---

## 13. Accessibility and language policy

- All new sections meet the same standard already implicit in the current page (semantic headings, `aria-labelledby`, no color-only encoding — confirmed by the existing `design:accessibility-review` skill available in this environment; a formal audit pass is listed as an implementation-phase task, §15).
- **Bilingual sourcing preserved**: original-language category terms (`slaven`, `slavinnen`, `mandoors`, `gecondemneerden`, `kostgelt`, and now `belenggu`) are always shown alongside their mapped category, never replaced by it — per `docs/ETHICAL_MODELING.md`'s Language section, extended here explicitly to Bahasa Indonesia UI copy (this project's primary interface language): analytical prose uses "orang yang diperbudak" (people subjected to slavery) rather than a bare "budak" label as the primary UI term, while `source_category_original` fields retain the archival terms unmodified. `belenggu` is kept as the archival Indonesian-translation term (this corpus's `translated_docx` convention already renders Dutch source text into Indonesian, per `docs/SOURCE_PROVENANCE.md`), not replaced by "shackle" or "restraint device" in any field that claims to quote the source.
- No claim in the new sections is phrased in a way that requires a reading level beyond the existing page's methodology section — critical-theory vocabulary (commensuration, aggregation, individuation) and the new count-tier vocabulary (§8) are each introduced with a one-sentence plain-language gloss the first time used per section.

---

## 14. Ethical safeguards

1. **`prohibited_inference_flag` gate** (§5, `coercion_evidence.csv`) — no coercion-evidence row reaches the UI without an explicit reviewer flip, enforced at the data layer, not just by documentation. **Revised**: this gate now explicitly covers restraint-device *use* claims (P6) as its primary current application, not a hypothetical future one.
2. **No optimization objective ever attaches to Subnet 3** (§7) — a standing implementation constraint; any future PR adding a cost function to the coercion subnet should be treated as a policy violation requiring explicit new ethical sign-off.
3. **Dual-ontology structural separation** (§6) prevents the single most likely failure mode of this kind of redesign: quietly merging the "administrative treatment" and "human" views into one table where the accounting view's units (count, category) end up being treated as the human view's units by default.
4. **Every new interpretive claim carries `interpretation_confidence`** (§5, `uncertainty_critical.csv`) and a `claim_tier`/`count_tier` — nothing in the new critical layer is exempt from the tiering this plan itself establishes in §2–§4 and §8.
5. **New this revision — inference-against-a-specific-person is structurally prohibited, not just documented**: `restraint_device_review.csv`'s `target_person_status` field only accepts `not_recorded` under current evidence (§4, §5) — a future contributor cannot casually set a person's name there without the schema itself flagging that no other value is currently permitted absent new source evidence, and the Petri net's `Restraint_Device_Context` guard (§7) is specified to be structurally incapable of firing an arc to a specific `HumanToken` under this state.
6. **New this revision — the extraction discrepancy is tracked, not resolved, by this plan**: §5/§15's required audit exists precisely so that this document does not become the mechanism by which the DOCX-vs-canonical-CSV gap (C10) gets silently closed by a planning document rather than by the project's normal review process.
7. **This document itself is subject to review** before any implementation phase begins — `REVIEW_QUEUE.md`-style tracking should log open questions, including (carried over) whether `G-COND-3` needs scholarly review before interpretive prose is written about it, and (new) the extraction-audit and cross-document overlap-review findings once available.

---

## 15. Implementation phases (proposed, not scheduled or started)

**Phase A0 — Required audits (new, gates Phase A).** One audit and one diagnosis were originally scoped here; the diagnosis found the audit's premise false:
  - ~~Canonical-extraction audit for the two restraint rows~~ **(withdrawn, §0 Revision 3).** A read-only diagnosis (`A0-5`) found both entries already exist as canonical rows (`SP-01267 -> INV-0343`, `SP-01344 -> INV-0401`) — there is no extraction gap, no scan/folio confirmation dependency, and no canonical-CSV addition to propose. The remaining open item is narrower: recording exact original Dutch spelling, folio number, viewer scan sequence, and IVdNT lemma in `A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` — a philological-completeness question, not an extraction-defect question.
  - **Cross-document temporal-overlap review** for the Madagascar cohort and the wider aggregate-group population (§8 tier 6): establish whether any other document in the corpus (or a later/earlier personnel register) describes an overlapping time window for any of the same people, which would affect whether 308 (tier 5) is even the right *single-document* estimate to carry forward, let alone a verified unique-person count. (Completed — see `CROSS_DOCUMENT_OVERLAP_FINDINGS.md`.)

**Phase A — Schema and derivation layer.** Build `archival_visibility.csv`, `accounting_treatment.csv`, `coercion_evidence.csv`, `restraint_device_review.csv`, `group_hierarchy_review.csv`, plus the two supplementary schemas, as derivations/joins of existing canonical data (no new archival extraction beyond what Phase A0 already audited). Write and run tests verifying every derived number against a hand-computed value, **including a regression test that the tier-3/tier-5 distinction (§8) can never collapse back into a single "total" number** (§16). Migrate `HUMAN_GROUP_HIERARCHY` out of `enclave_data.py` into `group_hierarchy_review.csv`, resolving the divergence from the solver snapshot's own `entity_coverage` grouping noted in this session's earlier diagnostic — this migration must also encode the Madagascar parent/child de-duplication decision, not just the independent/subgroup split the first draft's version tracked.

**Phase B — Ontology/graph layer.** Implement the dual-ontology read model (§6) as adapter methods (`EnclaveDataAdapter.get_colonial_accounting_view()` / `get_human_centred_view()`), read-only, following the existing adapter's "never opens write mode" pattern.

**Phase C — Page redesign.** Implement §11's revised information architecture, §12's visual rules, §13's language policy, behind the existing route (`/riset/enclave-1682/`) — additive template sections, solver section relocated per instruction.

**Phase D — Petri Net specification (not simulation).** Author the Subnet 2/3 specification, including the revised `Restraint_Device_Context` guard behaviour (§7), as a documentation extension of `docs/PETRI_NET_MODEL.md` (or a new `docs/CRITICAL_PETRI_NET_MODEL.md`) — no simulation engine work in this phase.

**Phase E — Review and ethical sign-off.** §14 item 7 and any open items logged during A0–D; this phase gates whether Phase C ships to the live route or stays behind a feature flag. **Phase A0's two audits are a hard prerequisite for Phase E sign-off**, not an optional nice-to-have.

Each phase is independently revertable; none requires any change to `docs/enclave/salido_hdt_model_v0_4_1/` itself.

---

## 16. Test strategy

Following this project's TDD convention (`CLAUDE.md` root): write the failing test first, per layer.

- **Derivation-layer tests** (Phase A): `test_archival_visibility_named_count_equals_50`, `test_group_hierarchy_review_madagascar_parent_and_children_not_both_counted` (asserts `SUM(record_person_count WHERE counts_toward_unique_person_estimate)` across the Madagascar rows equals 64, not 128 — the direct regression guard for §0 Revision 2), `test_cumulative_recorded_count_equals_372_and_is_labelled_unsafe` (locks the arithmetic fact while asserting the UI-facing label/tier metadata is always attached), `test_unique_person_verified_count_is_absent_or_explicitly_unresolved` (fails if any code path renders a bare number for tier 6 without the "unresolved" state, until Phase A0's cross-document review changes that state deliberately).
- **Restraint-device tests** (new): `test_restraint_device_review_rows_map_to_existing_canonical_inventory_ids` (both rows must carry `canonical_inventory_row_id` values that resolve to real `10_inventory_items.csv` rows — `INV-0343`, `INV-0401`), `test_restraint_device_actual_use_status_only_accepts_not_recorded` (schema-level enforcement of P6, unaffected by this correction), `test_coercion_evidence_restraint_device_row_requires_confirmed_presence` (a `coercion_evidence.csv` row with `evidence_type=restraint_device` requires `canonical_extraction_status=present` on its corresponding `restraint_device_review.csv` row — no extraction-audit gate remains, since none is needed).
- **Gate-enforcement tests**: `test_coercion_evidence_hidden_when_prohibited_flag_true`, `test_no_optimization_objective_attaches_to_coercion_subnet` (static check against the Petri net spec document, not a running simulation, since none exists), `test_restraint_device_context_guard_cannot_target_specific_human_token` (static check against the Subnet 3 spec).
- **Dual-ontology separation tests**: `test_colonial_view_and_human_view_never_share_a_mutable_object`.
- **Page tests** (Phase C, Django `SimpleTestCase`, matching existing `Enclave1682ViewTest` conventions): section-order test asserting the solver section's DOM position is after the archival/critical sections; a test asserting the page never renders a bare "372" or "308" without its tier label adjacent in the DOM; language-policy test asserting original-language terms (including `belenggu`) co-occur with their mapped category wherever shown.
- **Accessibility tests**: extend existing coverage with the new sections, run through `design:accessibility-review` skill as a pre-ship gate (§13).
- No test in this plan asserts on solver *optimization* outcomes for the coercion subnet, because no such outcome should ever exist (§14.2) — `test_coercion_subnet_has_zero_transitions_with_objective_value` remains a standing negative test once Phase D's spec document exists in machine-readable form.

---

## 17. Migration and provenance policy

- **Canonical dataset immutability preserved exactly as today**: `docs/enclave/salido_hdt_model_v0_4_1/` (and v0.3/v0.4) remain untouched by this plan. New CSVs live in a sibling directory, tentatively `docs/enclave/salido_hdt_critical_layer_v0_1/`, versioned independently.
- **The two restraint-device rows (C10) already exist in the canonical CSV (`INV-0343`, `INV-0401`) and require no addition, migration, or new canonical version.** §0 Revision 3 withdrew the earlier "missing, pending future addition" framing. `restraint_device_review.csv` (critical layer) references these existing rows by ID; it does not stand in for them pending a migration that isn't needed.
- **Every derived claim traces back to source rows** via `provenance_critical_layer.csv` — no critical-layer number should ever be quoted without a `reproducible_query` a reviewer can re-run against the canonical CSVs, mirroring `docs/SOURCE_PROVENANCE.md`'s citation rule. This now explicitly includes the requirement that any published count carry its §8 tier label as part of that provenance record.
- **No retroactive edits to existing MANIFEST.csv or hash-verified files** — the critical layer gets its own manifest/hash file, following the same `verify_hashes()` pattern the adapter already implements for the canonical dataset.
- **Schema changes to the critical layer itself go through the same MIG-NNN pattern** already established in `V0_4_MIGRATION_PLAN.md`, for consistency and auditability — including this revision's own schema renames, which should be logged as a MIG-NNN-style entry once implementation begins, referencing this plan's §0.

---

## 18. Exact files proposed for a future implementation

*(Listed for planning purposes only — none of these are created by this document. This revision, like the first draft, only writes the plan file itself.)*

**New data files:**
- `docs/enclave/salido_hdt_critical_layer_v0_1/archival_visibility.csv`
- `docs/enclave/salido_hdt_critical_layer_v0_1/accounting_treatment.csv`
- `docs/enclave/salido_hdt_critical_layer_v0_1/coercion_evidence.csv`
- `docs/enclave/salido_hdt_critical_layer_v0_1/restraint_device_review.csv`
- `docs/enclave/salido_hdt_critical_layer_v0_1/group_hierarchy_review.csv`
- `docs/enclave/salido_hdt_critical_layer_v0_1/provenance_critical_layer.csv`
- `docs/enclave/salido_hdt_critical_layer_v0_1/uncertainty_critical.csv`
- `docs/enclave/salido_hdt_critical_layer_v0_1/MANIFEST.csv`

**New documentation:**
- `docs/enclave/salido_hdt_critical_layer_v0_1/docs/CRITICAL_ACCOUNTING_MODEL.md` (formal write-up of §1, §6)
- `docs/enclave/implementation/CRITICAL_PETRI_NET_MODEL.md` (§7, extending `docs/enclave/salido_hdt_model_v0_4_1/docs/PETRI_NET_MODEL.md` by reference, not edit)
- `docs/enclave/implementation/CRITICAL_LAYER_REVIEW_QUEUE.md` (§14 item 7 tracking, including Phase A0's two audits)
- `docs/enclave/implementation/RESTRAINT_DEVICE_EXTRACTION_AUDIT.md` (new — Phase A0 deliverable, documents the audit outcome for the two C10 rows before any canonical-CSV proposal is drafted)

**Modified application files (Phase B/C, future PRs — not this turn):**
- `frontend/map_app/enclave_data.py` — new adapter methods for the dual-ontology read model; migration of `HUMAN_GROUP_HIERARCHY` to `group_hierarchy_review.csv`
- `frontend/map_app/enclave_config.py` — new path resolution for `salido_hdt_critical_layer_v0_1/` (read-only, mirroring existing `SALIDO_HDT_DATA_DIR` pattern)
- `frontend/map_app/templates/map_app/riset_enclave_1682.html` — §11 section reorder and additions
- `frontend/map_app/tests.py` — new test classes per §16
- `docker-compose.yml` — new read-only mount for the critical-layer directory, following the existing `salido_hdt_model_v0_4_1:ro` mount pattern exactly

**Not modified, ever, by any phase of this plan:**
- `docs/enclave/salido_hdt_model_v0_3/`, `docs/enclave/salido_hdt_model_v0_4/`, `docs/enclave/salido_hdt_model_v0_4_1/` (all 17 canonical CSVs + existing docs) — **including the two restraint-device rows found this revision**, which are not added to any canonical file by this plan (§17)
- `docs/enclave/enklave-salido.docx` (read this revision, not modified)
- `frontend/map_app/data/enclave_1682_solver_run/` (solver snapshot)
- any solver source (`salido_hdt.solver.cli` — not present in this repository checkout; out of scope regardless)
- `docker-compose.yml`'s existing service/mount definitions beyond the one addition above

---

*End of revised plan. No canonical dataset, solver snapshot, source DOCX, or Docker configuration was modified — the DOCX was read, not written. No commit was made.*
