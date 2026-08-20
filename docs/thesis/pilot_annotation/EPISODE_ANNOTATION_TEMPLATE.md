# Episode Annotation Template

> **DRAFT FOR RESEARCHER REVIEW — NOT IMPLEMENTED — NOT A FINAL HISTORICAL INTERPRETATION**

Template kosong/instruksional. Dipakai untuk mengisi tiap dossier klaster (`BARUS_EPISODE_DOSSIER_DRAFT.md` dkk.) dan untuk episode tambahan di luar empat pilot bila pekerjaan ini dilanjutkan. Rujuk `docs/thesis/EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md` untuk definisi unit dan aturan.

**Aturan pengisian wajib (berlaku di seluruh template ini):**

- Gunakan nilai aktual **hanya** bila ditemukan langsung di repository (kutip path + baris/kolom sumbernya).
- Gunakan `NOT AVAILABLE` bila dicari dan tidak ditemukan.
- Gunakan `AMBIGUOUS` bila bukti yang ada saling bertentangan — jangan pilih salah satu secara diam-diam.
- Jangan menerjemahkan bebas bila terjemahan formal belum tersedia — tandai `translation_status: NOT AVAILABLE (literal gloss only)` bila hanya ada ringkasan Indonesia peneliti.
- Jangan menetapkan status resistensi final di field mana pun.
- Setiap field interpretatif (bagian 14–19) wajib disertai `researcher_review_required: true`.

---

## 1. Episode Identity

| Field | Nilai |
|---|---|
| `episode_id` | |
| `cluster` | |
| `title` (deskriptif-netral, dilarang memuat karakterisasi normatif) | |
| `start_date` / `end_date` | |
| `date_precision` | `day` \| `month` \| `year` \| `range` \| `inferred` |
| `location_ids` | |
| `actor_ids` (pemberi komitmen) | |
| `counterparty_ids` (penerima komitmen) | |
| `end_date_status` | `resolved` \| `evidence_exhausted` \| `ongoing_at_source_end` |

## 2. Source Record

| Field | Nilai |
|---|---|
| `source_id` | |
| `source_collection` (CD/Daghregister/GM/buku sekunder/dll.) | |
| `volume_or_inventory` | |
| `folio_or_page` (`source_page` + `book_page` dari `linimasa_events`) | |
| `document_genre` | `treaty` \| `oath_record` \| `journal_entry` \| `letter` \| `travel_account_compilation` \| `editorial_compilation` \| `secondary_history` \| lainnya |
| `document_language` | |
| `document_author` | |
| `document_recipient` | |
| `author_institutional_position` | |

## 3. Original Text

Kutipan verbatim dari `text_asli`. **Tidak diedit, tidak diperbaiki ejaan, tidak dirapikan.**

```
[kutipan]
```

## 4. Transcription

Status transkripsi: `AVAILABLE (as text_asli in linimasa_events.csv)` \| `NOT AVAILABLE` \| `PARTIAL`.

Catatan: `linimasa_events.csv` sudah berfungsi sebagai lapis transkripsi untuk baris yang dikutip — bukan transkripsi baru dari scan asli (proyek ini belum melakukan verifikasi scan-ke-teks; `confidence_flag` skema `LinimasaEvent` default `'unverified'`).

## 5. Literal Translation

| Field | Nilai |
|---|---|
| `translation_status` | `NOT AVAILABLE (formal)` — hanya ada ringkasan Indonesia peneliti di kolom `title`/`notes` |
| `researcher_gloss` (ringkasan, BUKAN terjemahan literal terverifikasi) | dikutip dari `title`/`notes`, ditandai jelas sebagai gloss |

**Dilarang** membuat terjemahan literal baru pada tahap persiapan ini — itu pekerjaan anotasi (langkah 5 protokol), bukan pekerjaan dokumen persiapan.

## 6. Documentary Claim

Satu baris per klaim yang diekstrak dari teks §3. Rujuk `PILOT_CLAIM_LEDGER.md` untuk daftar terkonsolidasi lintas-episode.

| `claim_id` | `claim_text` | `claim_type` |
|---|---|---|
| | | `factual_assertion` \| `attribution_of_motive` \| `evaluative_judgment` \| `causal_assertion` \| `normative_characterization` |

## 7. Reconstructed Event

| Field | Nilai |
|---|---|
| `event_role` | `commitment_event` \| `implementation_event` \| `response_event` |
| `event_summary` (netral, tanpa karakterisasi normatif dari §6) | |
| `supporting_claim_ids` | |
| `reconstruction_confidence` | |
| `report_date` | biasanya `NOT AVAILABLE` (lihat gap struktural, ARCHIVAL_DENSITY_MEASUREMENT_PLAN.md §4) |

## 8. Commitment Classification

Sesuai keputusan peneliti — `event_type='perjanjian'` **tidak otomatis** berarti `substantive_commitment`.

| Field | Nilai |
|---|---|
| `commitment_classification` | `substantive_commitment` \| `treaty_renewal` \| `administrative_repetition` \| `reported_commitment` \| `coerced_or_constrained_commitment` \| `representationally_contested` \| `insufficient_evidence` |
| Syarat minimum terpenuhi? | aktor pemberi ✓/✗ · pihak penerima ✓/✗ · kewajiban teridentifikasi ✓/✗ · bentuk persetujuan dalam sumber ✓/✗ · provenance ✓/✗ · lingkup representasi dapat dinilai ✓/✗ |
| `commitment_under_duress` | `none_documented` \| `military_action_preceding` \| `military_presence` \| `economic_coercion` \| `contested` \| `cannot_determine` |
| `representational_scope` | |

## 9. Obligation

| `obligation_id` | `obligated_actor` | `beneficiary_actor` | `obligation_modality` | Isi (teks sumber) |
|---|---|---|---|---|
| | | | `required_action` \| `prohibited_action` \| `payment` \| `surrender` \| `diplomatic_restriction` \| `other` | |

## 10. Reciprocal Obligation

**Wajib diperiksa untuk SETIAP `Obligation` di §9** — bukan hanya bila mencurigakan.

| `obligation_id` (dari §9) | `reciprocal_obligation_id` | `reciprocal_actor` | `reciprocity_check_note` |
|---|---|---|---|
| | | | `no reciprocal obligation in text` \| `reciprocal obligation mentioned but unspecific` \| `NOT AVAILABLE — text incomplete` |

## 11. Implementation Evidence

| Field | Nilai |
|---|---|
| `implementation_event_ids` | |
| `observed_action` | |
| `action_date` / `action_date_precision` | |
| `evidence_of_absence_vs_absence_of_evidence` | `documented_nonaction` \| `silence_only` |
| `implementation_degree` | `full` \| `partial` \| `none_observed` \| `not_observable` |

## 12. Commitment-Action Relationship (Dimensi A)

> Nilai: `fulfilled` · `substantially_fulfilled` · `partially_fulfilled` · `delayed` · `suspended` · `evaded` · `openly_refused` · `contradicted` · `reciprocal_breach` · `contested` · `cannot_determine`

**Aturan `evaded` (keputusan peneliti, wajib diikuti):** JANGAN gunakan `evaded` hanya karena kewajiban tidak dilaksanakan. Bila penghindaran hanya disimpulkan dari pola berulang (bukan pernyataan sumber eksplisit), gunakan struktur berikut, bukan `evaded`:

| Field | Nilai |
|---|---|
| `deviation_status` | (nilai deskriptif Dimensi A lain yang didukung bukti langsung, mis. `partially_fulfilled`/`cannot_determine`) |
| `strategy_interpretation` | `possible_evasion` |
| `evidence_status` | `pattern_inferred` |
| `researcher_review_required` | `true` |

`evaded` sebagai nilai Dimensi A langsung hanya sah bila ada `DocumentaryClaim` (§6) yang secara eksplisit menyatakan tindakan menghindar — bukan disimpulkan peneliti dari berulangnya larangan.

| Field | Nilai |
|---|---|
| `dimension_a_value` | |
| `pairing_basis` (dasar pemasangan commitment↔implementation) | |
| `pairing_strength` | `explicit` \| `strong` \| `possible` \| `speculative` |

## 13. VOC Response

| Field | Nilai |
|---|---|
| `response_event_ids` | |
| `responding_actor` | |
| `response_type` | `military_action` \| `destruction` \| `expulsion` \| `sanction` \| `renegotiation` \| `renewal_of_treaty` \| `incentive_or_gift` \| `withdrawal` \| `no_response_documented` |
| `response_date` | |
| `sanction_or_incentive` / `renegotiation` / `escalation` / `de_escalation` | |

## 14. Source Characterization

Karakterisasi normatif/evaluatif dari **pembuat sumber** (bukan peneliti), disimpan terpisah dari rekonstruksi §7.

| `source` | `characterization_text` | `claim_type` |
|---|---|---|
| | | `normative_characterization` |

Contoh nilai yang HARUS masuk di sini, bukan di §7: kata-kata seperti *Meineyd*, "tidak setia", "memberontak", "ontrouw", "afvallig" — lihat §9 kata kunci VOC (batasan keputusan peneliti #9, berlaku juga untuk `linimasa_events`).

## 15. Evidence Supporting Resistance Interpretation

`researcher_review_required: true` — daftar kutipan/rujukan `claim_id` yang mendukung.

## 16. Evidence Weakening Resistance Interpretation

`researcher_review_required: true` — wajib diisi, tidak boleh kosong tanpa keterangan `NOT AVAILABLE` beralasan.

## 17. Alternative Explanations

Dipertimbangkan dari sebelas kandidat baku (protokol §6.3): ketidakmampuan · konflik internal · perubahan kepemimpinan · salah komunikasi · keterlambatan administratif · gangguan transportasi · persoalan ekonomi · perang · kehilangan arsip · bias pelaporan VOC · kegagalan pihak lawan memenuhi kewajiban timbal-balik.

| Alternatif dipertimbangkan | Didukung bukti? | Catatan |
|---|---|---|
| | | |

## 18. Causal Readiness

| Kriteria | Nilai |
|---|---|
| `cause_defined` | |
| `outcome_defined` | |
| `temporal_order_reliable` | |
| `mechanism_evidence` | |
| `alternative_explanations_recorded` | |
| `comparison_case_available` | |
| `actor_identity_stable` | |
| `location_identity_stable` | |
| `report_delay_known` | |
| `archival_density_known` | (lihat `ARCHIVAL_DENSITY_MEASUREMENT_PLAN.md` — status korpus saat ini) |
| `ready_for_process_tracing` | `ready` \| `partially_ready` \| `descriptive_only` \| `not_testable` |

**Tidak boleh menyatakan hubungan kausal di field mana pun bagian ini.**

## 19. Interpretive Status (Dimensi B)

> Nilai: `explicit_resistance_candidate` · `probable_resistance_candidate` · `possible_resistance_candidate` · `ambiguous_noncompliance` · `probable_constraint_or_incapacity` · `contractual_dispute` · `insufficient_evidence`

| Field | Nilai |
|---|---|
| `dimension_b_value` | |
| `evidence_for` | (rujukan §15) |
| `evidence_against` | (rujukan §16) |
| `alternative_explanations` | (rujukan §17) |
| `confidence` | |
| `interpretation_source` | `source_derived` \| `researcher_theoretical` \| `model_derived` |
| `eligible_as_evidence` | `true` bila `interpretation_source: source_derived`; **`false` wajib bila `model_derived`** |
| `researcher_review_required` | **selalu `true`** |
| `decision_status` | `draft` \| `under_review` \| `researcher_approved` \| `rejected` \| `deferred` |

## 20. Researcher Decision

*(Kosong pada tahap persiapan ini — diisi peneliti setelah tinjauan.)*

| Field | Nilai |
|---|---|
| `decision` | |
| `decided_by` | |
| `date` | |
| `rationale` | |

## 21. Unresolved Questions

Daftar pertanyaan terbuka spesifik episode ini yang tidak dapat dijawab dari repository saat ini.

- [ ] ...
