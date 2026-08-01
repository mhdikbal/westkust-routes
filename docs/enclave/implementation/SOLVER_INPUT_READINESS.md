# SALIDO-HDT v0.4.1 — Solver Input Readiness Assessment

Date: 2026-08-02
Canonical input: `docs/enclave/salido_hdt_model_v0_4_1/` (read-only).
`docs/enclave/salido_hdt_model_v0_3/` and `docs/enclave/salido_hdt_model_v0_4/` were not touched — re-verified immutable (§6).
**No backfill was changed. No CSV was modified.** This report inspects what the v0.4.1 backfills actually point to and extends the same provenance-granularity test to every other hard-constraint candidate the solver would read, per `docs/enclave/salido_hdt_model_v0_4_1/docs/CONSTRAINT_SOLVER.md`.

---

## 1. SP-01236 — is it section-level, detail-level, or both?

**Answer: section-level only. It is not a detail-level passage, and it does not carry both.**

`SP-01236` (`00_source_passages.csv`, `paragraph_index=1236`) reads, in full: **"Lijfeijgenen in de mijns Beneden-Pagger"** ("Bondspeople in the Beneden-Pagger mine"). This is a bare heading — it names a topic and a location, and contains **zero quantities, zero role names, zero individual counts**.

Reading the surrounding passages in full confirms the document structure:

| Passage | Text | Function |
|---|---|---|
| SP-01236 | "Lijfeijgenen in de mijns Beneden-Pagger" | **Section heading** — the one all 10 backfills cite |
| SP-01237 | "Istilah lijfeijgenen secara literal menunjuk orang-orang yang tubuh dan tenaganya dianggap..." | Editorial glossary note (not part of the enumeration) |
| SP-01238 | "A. Budak laki-laki" | Subsection heading |
| SP-01239 | "erdapat 150 budak laki-laki, terdiri atas:" | Subsection summary total (150) |
| SP-01240 | "8 mandoor;" | **Detail line** — the actual count behind `G-MANDOOR-8` |
| SP-01241 | "1 voorslager;" | **Detail line** — behind `G-VOORSLAGER-1` |
| SP-01242 | "121 budak laki-laki dewasa;" | **Detail line** — behind `G-MS-121` |
| SP-01243 | "6 anak laki-laki kecil yang belum sepenuhnya dewasa;" | **Detail line** — behind `G-HWJ-6` |
| SP-01244 | "4 anak laki-laki yang masih tergolong anak-anak dan memperoleh uang makan;" | **Detail line** — behind `G-CHILD-KOST-4` (see note below) |
| SP-01245 | "7 grasjongens di Sillida;" | Detail line, but located at **Sillida generally**, not stated as Beneden-Pagger specifically — no corresponding `G-` group exists in `06_human_groups.csv` for this line |
| SP-01246 | "3 penduduk pribumi yang dijatuhi hukuman." | **Detail line** — behind `G-COND-3` |
| SP-01247 | "B. Budak perempuan dan anak-anak" | Subsection heading |
| SP-01248 | "erdapat 94 budak perempuan beserta anak-anak..." | Subsection summary total (94) |
| SP-01249 | "3 mandores perempuan;" | **Detail line** — behind `G-MANDORESS-3` |
| SP-01250 | "68 budak perempuan dewasa;" | **Detail line** — behind `G-SLAVIN-68` |
| SP-01251 | "4 anak yang memperoleh uang makan;" | **Detail line** — behind `G-CHILD-KOST-4` (see note below) |
| SP-01252 | "19 anak, baik anak perempuan maupun anak laki-laki, tanpa uang makan." | **Detail line** — behind `G-CHILD-NOKOST-19` |

**Note on `G-CHILD-KOST-4`**: two candidate detail lines exist (SP-01244, under subsection A / male, and SP-01251, under subsection B / female-and-children) that both read "4 anak ... yang memperoleh uang makan." `06_human_groups.csv`'s `sex_category_original` for `G-CHILD-KOST-4` is empty/unspecified, so which of the two passages is the true source cannot currently be determined from the CSV alone — flagged as an open ambiguity, not resolved in this report (no value was changed).

**Cross-check**: the count in every one of the 10 groups (`G-MS-121`=121, `G-HWJ-6`=6, `G-KJ-4`=4, `G-COND-3`=3, `G-MANDOOR-8`=8, `G-VOORSLAGER-1`=1, `G-SLAVIN-68`=68, `G-MANDORESS-3`=3, `G-CHILD-KOST-4`=4, `G-CHILD-NOKOST-19`=19) matches its corresponding detail passage exactly (verified directly against `06_human_groups.csv.count`). **The numbers are archivally sound** — this report is not questioning the data's accuracy, only which passage ID a structured citation should point to.

**The consequence for the v0.4.1 backfill**: `source_quote` on all 10 `07_human_role_location_time.csv` rows is the literal string "Lijfeijgenen in de mijns Beneden-Pagger" — i.e., every one of the 10 rows quotes the *section heading*, not its own detail line. The exact-substring-match rule that produced the backfill was applied correctly and exactly as specified (unique match → fill); the finding here is about what that unique match is *evidence for*, not about whether the rule was executed correctly. Per the task's own framing: **section-level provenance is sufficient to support "this group is present at this location" (entity grouping) but is not, by itself, sufficient to support the specific quantity each group asserts** — that support exists only in the unlinked detail passages (SP-01240–SP-01252), none of which is cited by any structured field in the current dataset (confirmed: `06_human_groups.csv.source_passage_id` is empty for all 17 rows, including these 10 — it was one of the columns v0.4 added empty and v0.4.1 did not touch).

---

## 2. Provenance-granularity classification scheme used below

| Level | Definition |
|---|---|
| `claim_level` | A structured citation (passage or paragraph-index join) resolves to a passage that **directly states** the specific fact/quantity/role the record asserts. |
| `section_level` | A structured citation resolves to a heading/summary passage that establishes topic and location context but does not itself state the specific fact. |
| `document_level` | Only a `source_document_id` is present — no passage-level granularity at all. |
| `missing` | No structured citation of any kind (no document, no passage, no paragraph index), regardless of whether free-text `evidence_basis` exists. |
| `ambiguous` | The record's own evidence signals an unresolved choice (an "X or Y" `evidence_status`/`relation_type`, or `evidence_basis` text that itself states the underlying identity/fact is not determined). |

Applied per table below, to every record that feeds one of `docs/CONSTRAINT_SOLVER.md`'s named hard-constraint categories (temporal presence, role compatibility, one-location-per-schicht, equipment capacity, topological feasibility, health exclusion) or its direct input-file list (`07`, `10`, `14`, `15`, `16`), plus `04_person_roles.csv` (the source of *named-individual* role compatibility, which `07` alone does not fully cover).

---

## 3. `04_person_roles.csv` (47 rows) — named-individual role compatibility

All 47 rows: **`document_level`**. Every row cites `source_document_id = DOC-PERSONNEL-1682-01-09`; `source_passage_id` is empty for all 47 (unchanged by v0.4.1 — this table was not touched). 46 rows carry `evidence_status = explicit`; one (`PR-STREIJT`, role `R-OPPERSTEIJGER`) carries `evidence_status = interpreted`, making that single row `document_level` **and** already self-flagged lower-confidence.

No `claim_level` or `section_level` rows exist in this table — `source_passage_id` was never populated here even at the section-heading granularity, unlike the 10 rows tested in §1.

---

## 4. `07_human_role_location_time.csv` (15 rows)

| Rows | Provenance | Basis |
|---|---|---|
| HRLT-0001–HRLT-0005 (named individuals: Vogel, Pleijtner, Hesse, Hoffman, Roelingh) | `document_level` | `source_document_id` present for all 5; `source_passage_id` empty (their `source_quote` values do not uniquely match any passage — confirmed in `V0_4_SEMANTIC_QA.md` §2.1 and re-verified for this report — so v0.4.1's deterministic rule correctly left them empty rather than guessing). |
| HRLT-0006–HRLT-0015 (10 aggregate groups at `L-BENEDEN-PAGGER`) | **`section_level`** | `source_passage_id = SP-01236`, confirmed a heading passage (§1). Sufficient for the claim these rows actually make (`role_id` is **empty on all 10** — they assert group-presence-at-location only, not a specific role+count). Not sufficient, on its own, as citation for the quantities embedded in each group's identifier (e.g., the "8" in `G-MANDOOR-8`) — that support is `missing` at the `07`/`06` level (see §1) and only recoverable by direct archival reading, which this report performed but did not encode back into any CSV. |

---

## 5. `14_task_requirements.csv` (18 rows) — task requirements

This table has **no `source_document_id` or `source_passage_id` column at all** (excluded from the v0.4 evidence-quadruple addition, MIG-013). Every row's only evidentiary trace is free-text `evidence_basis`. Per the classification scheme, absence of a structured citation field is `missing` regardless of prose quality — but the table below distinguishes rows whose prose names facts independently verifiable elsewhere (marked *corroborated*) from rows that self-report weak grounding.

**Also newly noted in this report** (not covered in `V0_4_SEMANTIC_QA.md`, which only examined `constraint_type` on `15`, not `constraint_strength` on `14`): `constraint_strength` itself contains the same class of compound values found elsewhere — `hard_role_soft_tools`, `hard_location_soft_staffing`, `hard_role`, `hard_location`, `hard_role_soft_location` — conflating a hard/soft binary with a *scope* (role vs. location vs. tools vs. staffing), exactly the `constraint_type`/`constraint_scope` pattern `V0_4_SEMANTIC_QA.md` §1.4 already flagged for `15`. Not re-litigated in full here; flagged so it is not missed when `15`'s vocabulary fix is eventually scoped.

| task_id | constraint_strength | Provenance | Note |
|---|---|---|---|
| T-INSPECT-MINE | hard_role_soft_tools | `missing` (corroborated) | "Pleitner secara eksplisit memeriksa tambang" — corroborated by `04_person_roles.csv` (`PR-PLEIJTNER`, `R-MARKSCHEIDER`, `document_level`). |
| T-DRILL | hard_location_soft_staffing | `missing` (corroborated, partial) | "Jumlah tim simultan dibatasi jumlah bor serviceable" — the borer-count fact is `claim_level` once traced to `INV-0232` (§7), but `14` itself does not cite it. |
| T-BLAST | soft | `missing` | Basis text itself states "Jumlah pekerja per schoot tidak eksplisit" (not explicit) — weakest-grounded row in this table. |
| T-TIMBER | soft | `missing` (corroborated) | "Penyanggaan schacht dan tambang lama eksplisit" — plausible but no ID trace. |
| T-ORE-REMOVE | soft | `missing` | Basis explicitly says "diinferensikan" (inferred) — self-flagged as inference. |
| T-ORE-TRANSPORT | soft | `missing` | No ID trace. |
| T-SORT | soft | `missing` (corroborated) | "Jenis pertama dan kedua dicatat" — matches inventory categories seen in `10`. |
| T-CRUSH | hard_location_soft_staffing | `missing` (corroborated) | "Stampwerk berada di Beneden-Pagger" — matches `16_location_adjacency.csv` `LE-0014` (`L-BENEDEN-PAGGER`→`L-STAMPWERK`, `explicit`). |
| T-WASH | soft | `missing` | No ID trace. |
| T-ASSAY | hard | `missing` (corroborated) | "Hoffman, Vogel, Roelingh disebut Assaijeur" — all three independently confirmed `document_level` in `04_person_roles.csv`. |
| T-RECORD | hard_role | `missing` (corroborated) | "Elias Hesse disebut Berghschrijver" — confirmed in `04` (`PR-HESSE`). |
| T-SMITH | hard_location | `missing` (corroborated) | Bengkel pandai besi + workers — corroborated by `04`'s `R-SMIT`/`R-BAAS-SMIT` rows. |
| T-CARPENTRY | soft | `missing` (corroborated) | Corroborated by `04`'s `R-TIMMERMAN` rows. |
| T-WAGON | soft | `missing` (corroborated) | Corroborated by `04`'s `R-WAGENMAKER` rows. |
| T-MEDICAL | hard_role_soft_location | `missing` (corroborated) | Corroborated by `04`'s `R-OPPERMEESTER`/`R-SIECKENVADER`/`R-JONGEN-CHIRURGIJN` rows. |
| T-WAREHOUSE | hard_location | `missing` (corroborated) | Corroborated by `04`'s `R-PACKHUIJSKNEGT` row. |
| T-CHARCOAL | soft | `missing` (corroborated) | No `R-COOLBRANDER` person actually appears in `04_person_roles.csv`, despite the role existing in `03_roles.csv` — role is defined but never assigned to anyone; basis text asserts it without a person-level anchor. |
| T-SUPERVISE | soft | `missing` | Basis text itself states "penempatan rinci tidak..." (detailed placement not [available]) — self-flagged incomplete. |

---

## 6. `15_role_location_compatibility.csv` (31 rows)

Same structural gap as `14`: no `source_document_id`/`source_passage_id` column. Classified using `evidence_basis` plus, where relevant, the `constraint_type` compound findings already established in `V0_4_SEMANTIC_QA.md` §1.4.

| Rows | constraint_type | Provenance | Note |
|---|---|---|---|
| RLC-0011, RLC-0015, RLC-0016, RLC-0017, RLC-0022, RLC-0024, RLC-0025 (7 rows, `hard`) | hard / hard_for_* | `missing` (corroborated) | Each names a specific, independently-verifiable fact from `04`/`16` (e.g. RLC-0011 "jabatan dan keberadaan eksplisit" for Pleijtner↔Salido, corroborated by `PR-PLEIJTNER`). |
| RLC-0009, RLC-0010 (`hard_when_event_specific`) | compound, per QA §1.4 | `missing` (corroborated) | "Pleitner memeriksa Princestolle/Oude Mijne" — corroborated by `04`, but the *event-specific* conditionality itself has no passage citation to bound *when*. |
| RLC-0012, RLC-0013, RLC-0014 (`hard_for_assay`/`hard_for_roelingh`/`hard_for_hoffman_vogel`) | compound, per QA §1.4 | `missing` (corroborated) | Person-scoped hard rules; the named individuals are `document_level` in `04`, but the rule row itself has no citation. |
| RLC-0026, RLC-0028, RLC-0030 (`hard_group_location`) | compound, per QA §1.4 | **`section_level`, indirectly** | Basis text "kelompok dicatat dalam Beneden-Pagger" — this is precisely the claim `07`'s `SP-01236`-cited rows support (§1, §4). These three rows are the `15`-table counterpart of that same section-level fact; they inherit the same ceiling (adequate for "group recorded at Beneden-Pagger," not for a specific count). |
| RLC-0027, RLC-0029, RLC-0031 (`interpreted`) | **misplaced evidence value, per QA §1.4** | **`ambiguous`** | Basis text itself declares the fact unresolved: "identitas kelompok tidak diketahui" (group identity unknown). This is the clearest `ambiguous` case in the whole solver-input set — the row's own text says it does not know what it is describing. |
| RLC-0001–0008, RLC-0018–0021, RLC-0023 (13 rows, `soft`) | soft | `missing` | Lower-stakes by design (soft constraints), still uncited structurally. |

---

## 7. `16_location_adjacency.csv` (22 rows) — topological feasibility

Same structural gap (no `source_document_id`/`source_passage_id`).

| Rows | evidence_status | Provenance | Note |
|---|---|---|---|
| LE-0001, LE-0002, LE-0012–0016, LE-0020, LE-0021 (9 rows) | explicit | `missing` (high-confidence, uncited) | Clean single-category evidence, e.g. "Boven-Pagger dalam kompleks tambang" — no ID trace but unambiguous. |
| LE-0022 | explicit_route | `missing` (redundant-verified) | Per `V0_4_SEMANTIC_QA.md` §1.1, `relation_type` on this same row (`coerced_mobility_route`) already carries the "route" meaning — the value is safe, just uncited structurally. |
| LE-0003–LE-0011 (9 rows) | **explicit_or_structural** | **`ambiguous`** | The evidence_status itself is an unresolved disjunction (§1.1 of the QA report) — cannot be called `missing` (there is a basis) nor `document_level`/`claim_level` (nothing resolves which of the two applies). |
| LE-0017 | interpreted_from_explicit_report | `ambiguous` | Basis names a specific sensory inference ("suara pengeboran terdengar") but the relation itself (`approaches_or_audibly_connected`) is a compound "or" value (QA §1.5) — the geometry is explicitly not settled. |
| LE-0018 | uncertain | `ambiguous` | `relation_type = topological_relation_unknown` — the row's own vocabulary states the relation is not known; textbook `ambiguous`. |
| LE-0019 | strong_interpretation | `ambiguous` | Per QA §1.1, this row's distinguishing "strength" information has no field to live in and cannot be verified from `evidence_basis` alone. |

---

## 8. `10_inventory_items.csv` — equipment capacity (targeted subset)

Unlike `07`/`14`/`15`/`16`, `10_inventory_items.csv` retained its **pre-existing (v0.3) `source_paragraph_index` column**, which is populated for all 403 rows and joins deterministically and exactly to `00_source_passages.paragraph_index` (confirmed: 0 empty in the original audit, and the join was tested and verified for the row below). This gives most of `10` a materially better provenance ceiling than the other four solver-input tables, **even though its v0.4-added `source_passage_id` column (a separate field) is empty for all 403 rows** — the older `source_paragraph_index` field already does the job the newer column was meant to formalize.

**Concrete equipment-capacity example**, per `docs/CONSTRAINT_SOLVER.md`'s named hard constraint ("Simultaneous drilling teams cannot exceed available serviceable borers"):

`INV-0232`: `quantity=60`, `item_text_id="bor tambang, kemungkinand terbaca berghborers"`, `location_id=L-SMITSWINCKEL`, `source_paragraph_index=1108`. Joined to `00_source_passages.csv`: `paragraph_index=1108` → `SP-01108`, text **"60 bor tambang, kemungkinan terbaca berghborers."** — identical to `source_translation_full`. **Provenance: `claim_level`** (the cited passage directly and exclusively states the quantity and item). **Caveat, independent of provenance level**: `reading_status = unresolved` (this row is one of the 30 in `docs/UNRESOLVED_READINGS.md`) — the *reading* of the item name itself is uncertain, so `claim_level` provenance here confirms *what passage says 60 borers*, not that "60 borers, reliably read" is settled. These are two different axes (citation granularity vs. reading confidence) and this row is a clean example of scoring well on one and poorly on the other.

**General rule for the rest of `10`**: any row with `reading_status = translated_docx` (373/403 rows) and a resolvable `source_paragraph_index` join is `claim_level` by the same mechanism; the 30 `reading_status = unresolved` rows are `claim_level` for citation purposes but carry the same reading caveat as `INV-0232`. This report does not enumerate all 403 individually — the join mechanism and its one caveat class are established and apply uniformly.

---

## 9. Loadability list

### Hard constraints — safe to load now

- **`04_person_roles.csv`, 46 `explicit` rows** — `document_level`, uniform, no compound vocabulary issue. Directly supports the "Role compatibility" hard constraint for named individuals.
- **`10_inventory_items.csv`, the 373 `reading_status=translated_docx` rows** — `claim_level` via the `source_paragraph_index` join. Supports "Equipment capacity" where an item maps to a constrained resource (e.g. `INV-0232` for drilling capacity), row-by-row, once each relevant item is individually selected (not all 403 rows are equipment; most are unrelated inventory categories such as chemicals, currency-adjacent items, or medical supplies with no named hard constraint).
- **`16_location_adjacency.csv`, the 9 clean `explicit`-status rows (LE-0001, LE-0002, LE-0012–0016, LE-0020, LE-0021)** — `missing` citation but unambiguous single-category evidence; usable for "Topological feasibility" with the caveat that no passage ID backs them.

### Hard constraints — usable only with an explicit uncertainty weight, not as unconditional hard exclusions

- **`07_human_role_location_time.csv`, HRLT-0006–0015 (`section_level`)** — safe for "this group exists at Beneden-Pagger" (entity grouping / topological presence), **not safe** as the sole support for a role-specific hard constraint tied to the group's exact composition, since the composition numbers are `missing` at this table's own level (§1, §4).
- **`15_role_location_compatibility.csv`, the `hard`/`hard_for_*`/`hard_when_event_specific` rows corroborated by `04`** — usable, but only because a *different* table (`04`) supplies the actual citation; `15` itself supplies none. Recommend the solver's implementation resolve the corroboration join explicitly rather than trusting `15`'s `constraint_type=hard` label in isolation.
- **`10_inventory_items.csv`, the 30 `reading_status=unresolved` rows (including `INV-0232`)** — `claim_level` citation exists, but the reading itself is flagged uncertain. A hard constraint built directly on `INV-0232`'s "60" should carry that reading uncertainty forward (e.g. as a wide capacity bound), not treat 60 as an exact hard cap.

### Not safe to load as hard constraints (recommend soft, or context-only, until resolved)

- **`15_role_location_compatibility.csv`, RLC-0027/RLC-0029/RLC-0031 (`ambiguous`, `constraint_type=interpreted`)** — the row's own text says group identity is unknown; loading these as `hard` would let the solver assert a `1.0`-weighted contradiction penalty against evidence that does not exist. Recommend `soft`, or exclude until `15` gains an `evidence_status` column (§1.4 of the QA report) so this caveat has a proper home.
- **`16_location_adjacency.csv`, LE-0003–0011, LE-0017, LE-0018, LE-0019 (12 rows, all `ambiguous`)** — over half the table. None should anchor a hard topological-feasibility exclusion; `LE-0018` in particular explicitly states its relation type is unknown.
- **`14_task_requirements.csv`, T-BLAST, T-ORE-REMOVE, T-SUPERVISE** — each self-reports incomplete or inferred grounding in its own `evidence_basis` text; treat as soft or context-only regardless of the `constraint_strength` label until the `constraint_strength` compound-vocabulary question (§5) is resolved.

### Context-only (informational, not a constraint input)

- `06_human_groups.csv` composition counts (all 17 rows, `document_level` at best, `missing` at passage level) — safe as **descriptive context** for the enclave's population, per `docs/ETHICAL_MODELING.md`'s requirement to preserve aggregate counts; **not** to be loaded as a hard-constraint capacity bound on labour without the detail-passage citation this report identified as absent (SP-01240–SP-01252, none currently linked).
- `05_locations.csv`'s single-axis `I_f(t)`-style structural facts and `12_numeric_anomalies.csv`'s 5 open anomalies — already known non-solver inputs, listed here only to confirm none was silently reclassified as a constraint input by this report.

---

## 10. Ethical guard reaffirmed for §9's "context-only" list

Per `docs/enclave/salido_hdt_model_v0_4_1/docs/ETHICAL_MODELING.md`, the aggregate-group rows in `06`/`07` (`G-MS-121`, `G-SLAVIN-68`, etc.) must never be loaded into an objective function as an extraction-optimization resource, regardless of their provenance level. This report's `section_level`/`missing` findings for those rows are an *additional*, independent reason they should not anchor hard capacity constraints today — but even once fully cited to claim-level passages, the ethical restriction stands on its own and does not lift once provenance is completed.

---

## 11. Immutability re-check

`salido_hdt_model_v0_3/` and `salido_hdt_model_v0_4/`: SHA-256 of every file re-compared against the baselines established in the prior two tasks — **unchanged**. `salido_hdt_model_v0_4_1/`: no write operation was performed during this report — confirmed by tool-call history for this task (only `csv.DictReader`, string joins, and lookups were executed). No backfill value, and no other cell in any of the 17 canonical CSVs, was altered.
