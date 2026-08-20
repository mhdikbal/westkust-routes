# Pariaman Episode Dossier (Draft)

> **DRAFT FOR RESEARCHER REVIEW — NOT IMPLEMENTED — NOT A FINAL HISTORICAL INTERPRETATION**

Sumber: `data/research/linimasa_events.csv` (baris dirujuk sbg nomor urut CSV). `id` Postgres `NOT AVAILABLE`.

**BATASAN KHUSUS KLASTER INI:** enam hipotesis alternatif wajib dipertahankan sejajar, **tidak boleh ditentukan interpretasi final pada tahap persiapan ini**: `resistance_to_voc_constraint` · `commercial_continuity` · `alliance_maintenance` · `market_constraint` · `local_political_competition` · `mixed_motive`.

---

## Episode Identity

| Field | Nilai |
|---|---|
| `episode_id` | EP-PARIAMAN-01 |
| `cluster` | Pariaman (Priaman) |
| `title` | Rangkaian aliansi-relaps-penundukan-ulang Priaman, 1671–1712 |
| `start_date` / `end_date` | 1671 / 1712 |
| `date_precision` | `year` |
| `location_ids` | Pariaman |
| `actor_ids` | landtheren/regenten Priaman (kolektif, komposisi berubah antar-baris) |
| `counterparty_ids` | VOC (via pejabat berbeda); Aceh (sebagai pihak yang dituju larangan) |
| `end_date_status` | `evidence_exhausted` — jeda 28 tahun ke [93] 1712 dicatat sbg *"jeda relaps terlama tercatat"* di `notes` sumber, kemungkinan generasi aktor berbeda |

## Reconstructed Events (tabel ringkas)

| CSV baris | Tahun | `event_type` | `dominion_status` | Aktor | Penerima | `source_document` | `book_page` |
|---|---|---|---|---|---|---|---|
| [51] | 1671 | perjanjian | voc_alliance | landtheren Priaman | Jacob Pits (VOC) | CD2 | 443-445 |
| [55] | 1678 | perjanjian | voc_alliance | regenten Priaman | Melchior Hurt (VOC) | CD3 | 160-161 |
| [66] | 1682 | perjanjian | voc_alliance | regenten Priaman, Oulaccan, dll. | Sultan Indrapoura & Panglima Radja Padang | CD3 | 290-291 |
| [68] | 1684 | konflik | voc_alliance | regenten Priaman | Jan van Leene (VOC) | CD3 | 351-355 |
| [93] | 1712 | perjanjian | voc_alliance | regenten Priaman, Oulaccan, Sonor, Bintoengantingi, Lima-cotta, Ticou | gezaghebber Sumatra's Westkust | CD4 | 388-392 |

## Documentary Claim (kutipan `text_asli` verbatim)

**[55] 1678 (dari `text_asli`, memuat catatan naratif peneliti/sumber sekunder yang dikutip di kolom yang sama):**
> *"Nader articulen van een eeuwig verbond... in 1678 sloot de meerderheid der Priamanse regenten zich weer bij de Atjehsche partijgangers aan... Tot een inleydinge deses werden de contracten en accoorden, in voortyden tusgen d'E. Comp[agnie] en de regeringe van Priaman gemaakt en besloten, by desen ten volle geconfirmeert."*

`claim_type: factual_assertion` untuk "sloot de meerderheid der Priamanse regenten zich weer bij de Atjehsche partijgangers aan" (mayoritas regenten kembali gabung faksi Aceh) — **klaim ini berasal dari narasi historiografis yang dikutip dalam `text_asli`, bukan traktat itu sendiri**; perlu dicatat sumbernya campuran (traktat + narasi sekunder dalam satu cuplikan). `NOT AVAILABLE` untuk memisahkan mana kalimat traktat asli dan mana narasi penulis sekunder tanpa membaca dokumen lengkap.

**[66] 1682:**
> *"beloven ende sweren voortaen niet sullen vermogen eenige vaartuygen naar Aetchin te laten afvaren, nu nog nimmermeer niet... Radja Ebraim met alle syne medestanders, hulpers, aanhang ende dienaren... buyten 't destrict van Priaman te houden."*

`claim_type: factual_assertion`. Dua kewajiban berbeda dalam satu kutipan: (a) larangan berlayar ke Aceh — kewajiban KOLEKTIF regenten; (b) menjauhkan Radja Ebrahim & pengikutnya dari wilayah Priaman — **ini menunjukkan Radja Ebrahim adalah aktor SPESIFIK yang diidentifikasi sebagai musuh, tapi Radja Ebrahim TIDAK muncul sbg aktor di baris [55] sebelumnya** — kemungkinan aktor berbeda antar-siklus.

**[68] 1684:**
> *"dat niemand uyt Priaman ofte d'onderhorige plaatsen voortaen eenige correspondentie sal mogen houden met die van Aetchin, nog eenigen handel met deselve doen, nog derwaars varen... maar buyten houden ende verdryven."*

`claim_type: factual_assertion`. Larangan diperluas dari [66]: bukan hanya "berlayar", tapi juga "korespondensi" dan "dagang" — **pelebaran cakupan larangan** yang secara struktural mengindikasikan larangan sebelumnya dianggap tidak cukup, TANPA menyebutkan insiden pelanggaran spesifik apa yang memicu pelebaran ini.

## Commitment Classification

| CSV baris | `commitment_classification` | Dasar |
|---|---|---|
| [51] 1671 | `substantive_commitment` | Formula bagi-hasil tol — kewajiban konkret |
| [55] 1678 | `treaty_renewal` — `AMBIGUOUS` | Teks "confirmeert" traktat lama; tapi juga mencatat peristiwa politik baru (bergabung faksi Aceh) sebelum pembaruan — campuran renewal + respons atas peristiwa |
| [66] 1682 | `substantive_commitment` | Larangan spesifik-tindakan (berlayar) + pengucilan aktor spesifik (Radja Ebrahim) |
| [68] 1684 | `substantive_commitment` | event_type='konflik' bukan 'perjanjian' — **`representationally_contested`**: apakah ini persetujuan baru atau kontrak dipaksakan pasca-serangan perlu diperiksa lebih lanjut; judul CSV sendiri: "diserang ulang, ditundukkan lagi" |
| [93] 1712 | `treaty_renewal` | Judul: "kembali ke pangkuan Aceh, lalu ditundukkan ulang" — pola sama [55]/[66] berulang |

## Obligation

| `obligation_id` | `obligated_actor` | `beneficiary_actor` | `obligation_modality` | Isi |
|---|---|---|---|---|
| OB-PRIAM-01 | regenten Priaman | VOC | `prohibited_action` | tidak melepas kapal berlayar ke Aceh [66] |
| OB-PRIAM-02 | regenten Priaman | VOC | `prohibited_action` | menjauhkan Radja Ebrahim & pengikut dari distrik [66] |
| OB-PRIAM-03 | Priaman & wilayah bawahan | VOC | `prohibited_action` (diperluas dari OB-PRIAM-01) | tidak berkorespondensi, tidak berdagang, tidak berlayar ke Aceh [68] |

## Reciprocal Obligation

| `obligation_id` | `reciprocal_obligation_id` | `reciprocal_actor` | `reciprocity_check_note` |
|---|---|---|---|
| OB-PRIAM-01 | [51] formula bagi-hasil tol | VOC (tersirat) | "reciprocal obligation mentioned but unspecific" — [51] soal bagi-hasil tol adalah kewajiban timbal-balik dari episode SEBELUMNYA (1671), tapi tidak eksplisit dikaitkan ulang di [66] |
| OB-PRIAM-02 | — | — | `no reciprocal obligation in text` |
| OB-PRIAM-03 | — | — | `no reciprocal obligation in text` |

## Implementation Evidence & Commitment-Action Relationship (Dimensi A)

| Pasangan | `pairing_basis` | `pairing_strength` | `dimension_a_value` |
|---|---|---|---|
| [51]→[55] | Judul [55] eksplisit: "lepas lagi ke faksi Aceh" — kata "lagi" menandai pengulangan | **strong** | `contradicted` — sumber eksplisit menyatakan mayoritas regenten bergabung faksi Aceh, bertentangan dgn komitmen [51] |
| [55]→[66] | Sumpah baru [66] (larangan berlayar) secara implisit mengakui pola sebelumnya | **strong** | `partially_fulfilled`/`AMBIGUOUS` — aktor pemicu (Radja Ebrahim) tidak muncul di [55], indikasi kemungkinan episode BERBEDA, bukan lanjutan langsung |
| [66]→[68] | Tema & lokasi identik; larangan diperluas | **strong** | Lihat aturan `evaded` di bawah |
| [68]→[93] | Tema sama (relaps-ke-Aceh) tapi jarak 28 tahun | **possible** | `cannot_determine` — jeda terlalu panjang untuk menyimpulkan kontinuitas aktor yang sama |

**Penerapan aturan `evaded` (keputusan peneliti) untuk [66]→[68]:** tidak ada `DocumentaryClaim` yang secara eksplisit menyatakan Priaman "menghindar" — yang tersedia hanyalah larangan yang diperluas cakupannya, dari mana peneliti BISA menyimpulkan larangan pertama tidak efektif. Karena ini inferensi dari pola (pelebaran cakupan larangan), bukan pernyataan langsung:

| Field | Nilai |
|---|---|
| `deviation_status` | `partially_fulfilled` |
| `strategy_interpretation` | `possible_evasion` |
| `evidence_status` | `pattern_inferred` |
| `researcher_review_required` | `true` |

`dimension_a_value` **tidak** diisi `evaded` secara langsung untuk pasangan ini.

## VOC Response

| Episode | `response_type` | `response_date` |
|---|---|---|
| [55]→[66] | `renegotiation` — sumpah baru, pengucilan Radja Ebrahim | 1682 |
| [68] 1684 | `military_action` — judul CSV: "diserang ulang, ditundukkan lagi" | 1684 |
| [93] 1712 | `renegotiation`/`renewal_of_treaty` — "ditundukkan ulang" | 1712 |

## Source Characterization

Tidak ditemukan kosakata tuduhan bergaya `Meineyd`/`ontrouw`/`afvallig` di kutipan `text_asli` yang tersedia untuk klaster ini — larangan dinyatakan dalam bahasa kewajiban ke depan ("voortaen niet sullen vermogen"), bukan tuduhan retrospektif atas pelanggaran masa lalu secara eksplisit bernama.

## Evidence Supporting Resistance Interpretation

- Pola larangan yang terus diperluas (berlayar → korespondensi+dagang+berlayar) adalah bukti tidak langsung bahwa hubungan dengan Aceh terus berlanjut meski dilarang berulang kali.
- Pengucilan aktor spesifik (Radja Ebrahim) di [66] menunjukkan VOC mengidentifikasi kepemimpinan lokal yang secara aktif bertentangan dengan aliansi VOC.

## Evidence Weakening Resistance Interpretation

- Larangan berfokus pada **perdagangan dan pelayaran**, bukan pada isu politik-kesetiaan murni — motif ekonomi (mempertahankan jaringan dagang lama dengan Aceh) sama plausibelnya dengan motif resistensi politik.
- Tidak ada `implementation_event` yang mendokumentasikan pelanggaran SPESIFIK (kapal mana, kapan, membawa apa) — hanya larangan yang diperbarui. `evidence_of_absence_vs_absence_of_evidence: silence_only`.
- Aktor kolektif (`regenten Priaman`) berubah komposisi antar-episode — sulit memastikan ini pola berulang oleh pihak yang sama vs faksi berbeda yang kebetulan serupa posisinya.

## Alternative Explanations (enam hipotesis wajib, tidak diberi keputusan final)

| Hipotesis | Evidence for | Evidence against | Status |
|---|---|---|---|
| `resistance_to_voc_constraint` | Larangan diperluas berulang; pengucilan aktor spesifik | Tidak ada bukti niat politik eksplisit dari pihak Priaman sendiri | `possible` |
| `commercial_continuity` | Isi larangan seluruhnya soal dagang/pelayaran, bukan soal kesetiaan politik abstrak | — | `possible` — **hipotesis dengan dukungan tekstual langsung terkuat** |
| `alliance_maintenance` | [93] menunjukkan pola akhir selalu kembali ke VOC, bukan lepas permanen | Jeda 28 tahun terlalu panjang untuk disebut "pemeliharaan" berkelanjutan | `possible` |
| `market_constraint` | Monopoli/tol VOC bisa mendorong pencarian jalur dagang alternatif (Aceh) | Tidak ada data harga/tol spesifik untuk periode Priaman ini di kutipan yang tersedia | `insufficient_evidence` |
| `local_political_competition` | Radja Ebrahim disebut spesifik sbg musuh, mengindikasikan faksi internal | Tidak ada rincian faksi lain di Priaman | `possible` |
| `mixed_motive` | Kombinasi dagang+politik paling konsisten dgn keseluruhan pola bukti | — | `possible` — **tidak dapat dipilih di atas yang lain tanpa bukti tambahan** |

**Keputusan final TIDAK ditetapkan pada dossier ini**, sesuai batasan tugas.

## Causal Readiness

| Kriteria | Nilai |
|---|---|
| `cause_defined` | Tidak |
| `outcome_defined` | Ya (larangan diperbarui, tindakan militer 1684) |
| `temporal_order_reliable` | Ya, `report_delay_known: false` |
| `mechanism_evidence` | Tidak |
| `alternative_explanations_recorded` | Ya (tabel di atas, enam hipotesis) |
| `comparison_case_available` | Tidak formal |
| `actor_identity_stable` | `AMBIGUOUS` — aktor kolektif berubah komposisi |
| `location_identity_stable` | Ya |
| `report_delay_known` | Tidak |
| `archival_density_known` | Tidak |
| `ready_for_process_tracing` | **`partially_ready`** |

## Interpretive Status (Dimensi B)

| Field | Nilai |
|---|---|
| `dimension_b_value` | **`possible_resistance_candidate`** — TIDAK dinaikkan ke `probable` karena `commercial_continuity` sama kuatnya secara tekstual |
| `evidence_for` | Larangan diperluas berulang; pengucilan aktor spesifik |
| `evidence_against` | Fokus larangan pada dagang, bukan politik; tidak ada bukti tindakan pelanggaran spesifik |
| `alternative_explanations` | Enam hipotesis di atas, semua dipertahankan sejajar |
| `confidence` | Rendah-sedang |
| `interpretation_source` | `source_derived` |
| `eligible_as_evidence` | `true` |
| `researcher_review_required` | **`true`** |
| `decision_status` | `draft` |

## Unresolved Questions

- [ ] Apakah Radja Ebrahim [66] dan aktor [55]/[68] adalah rangkaian kepemimpinan yang sama atau faksi berbeda? `NOT AVAILABLE` tanpa genealogi tambahan.
- [ ] Data harga/tol spesifik periode 1678-1684 untuk menguji `market_constraint` — `NOT AVAILABLE` di `linimasa_events`; mungkin ada di `atjeh_trade_records` (di luar cakupan dossier ini).
- [ ] Apakah [68] 1684 (`event_type='konflik'`) sebaiknya diperlakukan sebagai `implementation_event`/respons, atau sebagai `commitment_event` baru (traktat pasca-serangan)? `AMBIGUOUS`, perlu keputusan peneliti — dossier ini memperlakukannya sbg respons+komitmen sekaligus (dua peran), yang mungkin perlu direvisi di skema final.
- [ ] Jeda 28 tahun ke [93] 1712 — apakah ada event penghubung yang belum masuk `linimasa_events`?
