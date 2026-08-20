# Barus Episode Dossier (Draft)

> **DRAFT FOR RESEARCHER REVIEW — NOT IMPLEMENTED — NOT A FINAL HISTORICAL INTERPRETATION**

Sumber tunggal: `data/research/linimasa_events.csv` (baris dirujuk dengan nomor urut CSV, 1-indexed, urutan `year` menaik — bukan `id` database; `id` Postgres `NOT AVAILABLE` karena database tidak berjalan saat audit). Field `book_page`/`source_page` dikutip langsung dari CSV.

**BATASAN KHUSUS KLASTER INI (keputusan peneliti, wajib dipatuhi dalam dossier ini):**
- Model 6 (`docs/thesis/colab/model6_game_theory.py`) **tidak boleh digunakan sebagai bukti** di §15–19.
- Payoff Model 6 hanya boleh dicatat sebagai `interpretation_source: model_derived`, `eligible_as_evidence: false`.
- Label "merunduk bukan tunduk" **tidak boleh diberikan** berdasarkan output Model 6 — hanya berdasarkan bukti tekstual & kronologi episode ini sendiri.

---

## Episode Identity

| Field | Nilai |
|---|---|
| `episode_id` | EP-BARUS-01 |
| `cluster` | Barus |
| `title` | Rangkaian pembaruan traktat Barus–VOC, 1668–1690 |
| `start_date` / `end_date` | 1668 / 1690 (lihat §Unresolved untuk rentang lebih panjang sampai 1775) |
| `date_precision` | `year` (beberapa baris punya `event_date_raw` lebih presisi, lihat tabel event) |
| `location_ids` | Barus (fort roster) |
| `actor_ids` | landsheeren/radja Baros (berganti antar-baris — lihat kolom Aktor) |
| `counterparty_ids` | VOC (via pejabat berbeda tiap baris) |
| `end_date_status` | `evidence_exhausted` untuk sub-episode 1668→1690; rantai berlanjut ke 1693/1694/1707/1731/1755/1775 dengan `pairing_strength` menurun (lihat §Unresolved) |

## Reconstructed Events (tabel ringkas)

| CSV baris | Tahun | `event_type` | `dominion_status` | Aktor | Penerima | `source_document` | `book_page` |
|---|---|---|---|---|---|---|---|
| [45] | 1668 | perjanjian | independence | landsheeren Baros | Joannis Molman, Jacob Pits (VOC) | CD2 | 383-384 |
| [57] | 1679 | perjanjian | voc_alliance | radja d'Oulou & radja Sittia-moeda | Rijklof van Goens (VOC) | CD3 | 197-198 |
| [60] | 1681 | perjanjian | voc_alliance | Radja d'Ileir & d'Ouloe; raja Maninghcabou | VOC | 1681 | 547 |
| [61] | 1681 | perjanjian | voc_alliance | radja d'Oulou & d'Ilheer | Jan van Lene & Arent Silvius (VOC) | CD3 | 228-230 |
| [74] | 1690 | suksesi | voc_alliance | Mage Radia (penerus radja d'Ilhier) | Salomon Le Sage (VOC) | CD3 | 536-538 |
| [76] | 1693 | perjanjian | voc_alliance | regenten Batahan (bawahan Barus) | Joannes Sas (VOC) | CD4 | 18-21 |
| [86] | 1694 | perjanjian | voc_alliance | Battassers Deiryse gebergte (Dairi) | Abraham Bouden (VOC) | CD4 | 83-86 |
| [92] | 1707 | perjanjian | voc_alliance | pounglous Chincol (Singkil, bawahan Barus) | Abraham Schepmoes (VOC) | CD4 | 266-268 |
| [98] | 1731 | perjanjian | internal_conflict | pongoulous Passeriboe (Sorkam) | Jacobus Scholten (VOC) | CD5 | 98-100 |
| [114] | 1775 | administratif | voc_withdrawal | Lodewijk Kaysel & Johannes Leuftink (VOC, subjek sendiri) | koning/radja Baros | CD6 | 393 |

## Documentary Claim (kutipan `text_asli` verbatim, tidak diedit)

**[45] 1668:**
> *"...alsoo gemelte lantheeren en Grooten... geseten hebben onder een onwettige ende onbetamelijcke heerschappij der Aatchinse regeringe... die alle het onverdraeglijcke Aetchinse jock ende volck afgeworpen, ende deselve crone in der eeuwigheijt hebben afgeswooren..."*
`claim_type: normative_characterization` (deskripsi "kekuasaan tidak sah/tidak layak" adalah sudut pandang dokumen VOC-Barus tentang Aceh, bukan fakta netral) + `factual_assertion` (pelepasan diri dari Aceh dinyatakan sebagai tindakan).

**[57] 1679:**
> *"Vernieuwinge soo van 't eerste, twede, als derde vredeverbond... Wy, ondergeschrevene, radja d'Oulou en radja Sittia-moeda... beloven en sweren by dit nader geschriv't, dat wy alle de voorgaande articulen, soo in 't eerste, tweede, als derde vredeverbond... ter goeder trouwe sullen nakomen."*
`claim_type: factual_assertion`. **Rujukan eksplisit ke traktat "pertama/kedua/ketiga" sebelumnya** — traktat "kedua" dan "ketiga" (~1670/1673 menurut judul CSV, tapi tidak ada baris `linimasa_events` terpisah untuknya) TIDAK tercatat sebagai `HistoricalEvent` mandiri di data ini. `NOT AVAILABLE`.

**[61] 1681:**
> *"radja d'Ileer ende de syne, sig hebbenfde] verootmoedigt... beloven by desen nader contracte volkomen gehoorsaamheyd, ende sodanige verbondbreking noyt meer te sullen beginnen, met afswering van alle andre oppermagten... sullen aan d'E. Comp[agnie] afstaan ende overhandigen alle 't geweer ende ammonitie van oorloge van de crone Aetche."*
`claim_type: factual_assertion` (janji taat + serah senjata) bercampur `attribution_of_motive` implisit ("verootmoedigt" = merendahkan diri). **Pengakuan eksplisit atas "verbondbreking" (pelanggaran perjanjian) SEBELUMNYA** — insiden spesifik yang dirujuk tidak dikutip dengan tanggal/detail terpisah di baris ini. `NOT AVAILABLE` untuk detail insiden.

**[74] 1690:**
> *"...aan de E. Comp[agnie]... idem tot voorkoming van alle onlusten, twist, tweespalt... naedeelen der algemeene vyanden, wien hij mogte sijn (off die van Aatchin)."*
`claim_type: factual_assertion`. Sumpah suksesi bersifat **preventif** (mencegah kerusuhan di masa depan), bukan rujukan ke pelanggaran aktual antara 1681–1690.

## Commitment Classification

| CSV baris | `commitment_classification` (dugaan awal, `researcher_review_required: true`) | Dasar |
|---|---|---|
| [45] | `substantive_commitment` | aktor+penerima+kewajiban(sumpah lepas-Aceh)+bentuk(dokumen traktat)+provenance(CD2)+lingkup representasi ("lantsheren ende Grooten van 't geheele lant" — klaim mewakili SELURUH negeri, `representationally_contested`: belum diverifikasi apakah seluruh negeri benar terwakili) |
| [57] | `treaty_renewal` | Teks sendiri menyebut "vernieuwinge" (pembaruan) |
| [60]/[61] | `substantive_commitment` | Serah senjata adalah tindakan konkret, bukan formalitas |
| [74] | `substantive_commitment` (sub-tipe suksesi) | Sumpah individual penerus, bukan pembaruan kolektif |
| [76], [86], [92] | `substantive_commitment` | Kewajiban spesifik (kualitas kemenyan, eksklusivitas jual, monopoli kapur barus) |
| [98] | `treaty_renewal`/`administrative_repetition`? | `AMBIGUOUS` — judul CSV "berdamai usai sengketa perangkap ranjau", bukan traktat kesetiaan; perlu keputusan peneliti apakah ini komitmen substantif atau penyelesaian sengketa lokal |
| [114] | Bukan komitmen — `response_event`/tindakan VOC sendiri | VOC menarik diri, subjek tindakan adalah VOC |

## Obligation (contoh terekstrak dari §Documentary Claim — bukan daftar lengkap seluruh traktat)

| `obligation_id` | `obligated_actor` | `beneficiary_actor` | `obligation_modality` | Isi |
|---|---|---|---|---|
| OB-BARUS-01 | radja d'Ileer/d'Ouloe (Barus) | VOC | `surrender` | serahkan senjata & amunisi "mahkota Aceh" [61] |
| OB-BARUS-02 | radja d'Oulou & Sittia-moeda | VOC | `required_action` | patuhi seluruh pasal traktat 1/2/3 "ter goeder trouwe" [57] |
| OB-BARUS-03 | Battassers Dairi | VOC/Barus | `required_action` | jual kemenyan/kapur barus eksklusif ke Baros [86] |
| OB-BARUS-04 | Chincol (Singkil) | VOC/Barus | `required_action` + `prohibited_action` (tersirat) | monopoli kapur barus [92] |

## Reciprocal Obligation

| `obligation_id` | `reciprocal_obligation_id` | `reciprocal_actor` | `reciprocity_check_note` |
|---|---|---|---|
| OB-BARUS-01 | — | — | `no reciprocal obligation in text` — teks [61] tidak menyebut kewajiban VOC timbal-balik |
| OB-BARUS-02 | — | — | `no reciprocal obligation in text` |
| OB-BARUS-03 | — | — | `NOT AVAILABLE — text incomplete` (kutipan CSV terpotong, tidak mencakup pasal harga/perlindungan yang mungkin ada di traktat lengkap) |
| OB-BARUS-04 | — | — | `NOT AVAILABLE — text incomplete` |

**Catatan penting:** berbeda dari klaster Inderapura (lihat dossier terpisah), tidak satu pun dari empat kewajiban terekstrak di sini punya kewajiban VOC yang eksplisit dalam kutipan `text_asli` yang tersedia. Ini **tidak boleh dibaca sebagai bukti bahwa VOC tidak punya kewajiban** — kutipan CSV adalah cuplikan, bukan traktat lengkap; `NOT AVAILABLE` berarti tidak ditemukan dalam cuplikan yang tersimpan, bukan tidak ada dalam dokumen asli.

## Implementation Evidence & Commitment-Action Relationship (Dimensi A)

| Pasangan | `pairing_basis` | `pairing_strength` | `dimension_a_value` | Catatan `evaded` |
|---|---|---|---|---|
| [45]→[57] | [57] teks eksplisit: "Vernieuwinge... eerste, twede, als derde vredeverbond" | **explicit** | `partially_fulfilled` — pembaruan traktat mengindikasikan traktat sebelumnya perlu ditegaskan ulang, tapi tidak ada `implementation_event` terpisah yang membuktikan pelanggaran spesifik | Tidak dipakai `evaded` — tidak ada `DocumentaryClaim` eksplisit tentang tindakan menghindar. `deviation_status: partially_fulfilled`, `strategy_interpretation: possible_evasion`, `evidence_status: pattern_inferred`, `researcher_review_required: true` |
| [57]→[61] | [61] teks eksplisit: "sodanige verbondbreking noyt meer te sullen beginnen" | **explicit** | `contradicted` — dokumen SENDIRI mengakui pelanggaran perjanjian terjadi | Bukan `evaded` — ini `openly_refused`/`contradicted` bila insidennya diketahui, tapi insiden spesifik `NOT AVAILABLE`, sehingga `dimension_a_value: contested` lebih defensibel sampai insiden teridentifikasi. **`AMBIGUOUS` antara `contradicted` dan `contested` — perlu keputusan peneliti** |
| [61]→[74] | Kontinuitas sumpah lintas-suksesi, bukan rujukan ke pelanggaran | **possible** | `fulfilled` (tidak ada bukti deviasi 1681–1690) | — |

## VOC Response

| Episode | `response_type` | `response_date` | Catatan |
|---|---|---|---|
| [57] "vernieuwinge" | `renewal_of_treaty` | 1679 | — |
| [61] "verbondbreking" diakui | `renegotiation` (serah senjata sbg syarat baru) | 1681 | Tidak ada `military_action`/`destruction` tercatat untuk Barus, **berbeda dari Koto Tangah** — perbedaan ini sendiri adalah data yang layak dicatat, bukan diabaikan |
| [114] penarikan VOC | `withdrawal` | 1775 | Subjek tindakan VOC sendiri — `responding_actor: VOC`, bukan respons atas deviasi aktor lokal |

## Source Characterization (dipisah dari rekonstruksi)

| Sumber | `characterization_text` | Catatan |
|---|---|---|
| [45] | "onwettige ende onbetamelijcke heerschappij der Aatchinse regeringe" (kekuasaan Aceh tidak sah/tidak layak) | `normative_characterization` — sudut pandang traktat Barus-VOC tentang Aceh |
| [61] | "verootmoedigt" (merendahkan diri) | `normative_characterization` |

## Evidence Supporting Resistance Interpretation

- [57]/[61] menunjukkan pola pembaruan traktat berulang dengan pengakuan pelanggaran eksplisit — pola ini SECARA STRUKTURAL konsisten dengan interpretasi bahwa Barus berulang kali tidak sepenuhnya mengikatkan diri.

## Evidence Weakening Resistance Interpretation

- Tidak ada respons militer/represi VOC tercatat terhadap Barus di seluruh rentang 1668–1690 (berbeda tajam dari Koto Tangah) — bila "verbondbreking" [61] cukup serius untuk dianggap resistensi terbuka, ketiadaan represi militer perlu dijelaskan, bukan diabaikan.
- Insiden spesifik "verbondbreking" yang diakui di [61] `NOT AVAILABLE` — tidak dapat dipastikan apakah ini pelanggaran substantif (mis. berdagang dengan Aceh) atau ketidaksepakatan administratif (mis. sengketa suksesi internal).

## Alternative Explanations

| Alternatif | Didukung bukti? | Catatan |
|---|---|---|
| Ketidakmampuan menegakkan kontrol pedalaman | Tidak diuji | Barus punya bawahan tersebar (Batahan, Singkil, Sorkam, Dairi) — kontrol pusat atas wilayah luas plausibel lemah |
| Perubahan kepemimpinan | Sebagian didukung | [74] eksplisit tentang pergantian radja d'Ilhier; traktat 1668→1679→1681 melibatkan nama radja berbeda-beda |
| Perang/tekanan Aceh eksternal | Tidak diuji | Tidak ada `DocumentaryClaim` di baris yang dikutip yang menyebut tekanan Aceh aktif pada periode 1679–1681 spesifik |
| Bias pelaporan VOC | Berlaku struktural | Seluruh sumber (CD2/CD3) adalah traktat yang DIREDAKSI pihak VOC |

## Causal Readiness

| Kriteria | Nilai |
|---|---|
| `cause_defined` | Tidak — "verbondbreking" [61] tidak dirinci apa penyebabnya |
| `outcome_defined` | Ya (serah senjata, sumpah baru) |
| `temporal_order_reliable` | Ya, tapi `report_delay_known: false` (lihat ARCHIVAL_DENSITY_MEASUREMENT_PLAN.md) |
| `mechanism_evidence` | Tidak |
| `alternative_explanations_recorded` | Ya (tabel di atas) |
| `comparison_case_available` | `partial` — dibandingkan dengan Koto Tangah (tanpa represi militer di sini vs represi berulang di sana), tapi bukan pembanding formal |
| `actor_identity_stable` | `AMBIGUOUS` — radja berganti (d'Oulou/Sittia-moeda → d'Ileer/d'Ouloe → Mage Radia), tidak jelas ini garis suksesi sama atau faksi berbeda |
| `location_identity_stable` | Ya (Barus) |
| `report_delay_known` | Tidak |
| `archival_density_known` | Tidak (lihat Bagian B) |
| `ready_for_process_tracing` | **`partially_ready`** |

## Interpretive Status (Dimensi B)

| Field | Nilai |
|---|---|
| `dimension_b_value` | `ambiguous_noncompliance` |
| `evidence_for` | Pengakuan eksplisit "verbondbreking" [61]; pola pembaruan traktat berulang |
| `evidence_against` | Tidak ada represi militer tercatat (berbeda Koto Tangah); insiden spesifik tidak diketahui; kemungkinan besar sengketa suksesi/administratif, bukan penolakan aliansi |
| `alternative_explanations` | Ketidakmampuan kontrol pedalaman; perubahan kepemimpinan |
| `confidence` | Rendah — bukti terlalu tipis untuk membedakan resistensi dari sengketa internal |
| `interpretation_source` | `source_derived` |
| `eligible_as_evidence` | `true` |
| `researcher_review_required` | **`true`** |
| `decision_status` | `draft` |

**Payoff Model 6 (dicatat terpisah, TIDAK dipakai sebagai bukti di atas):**

| Field | Nilai |
|---|---|
| `interpretation_source` | `model_derived` |
| `eligible_as_evidence` | **`false`** |
| Isi | Bobot payoff Elite lokal `+0.4` di `voc_alliance` (`docs/thesis/colab/model6_game_theory.py` L94-99), berpijak eksplisit ke tesis CLD "merunduk bukan tunduk" — **sirkular bila dipakai untuk melabeli episode ini**, karena tesis itu sendiri yang menentukan bobotnya |
| Status label "merunduk bukan tunduk" untuk episode Barus ini | **TIDAK DIBERIKAN** pada dossier ini, sesuai batasan keputusan peneliti |

## Unresolved Questions

- [ ] Traktat "kedua" dan "ketiga" yang dirujuk [57] (~1670/1673) tidak punya baris `linimasa_events` sendiri — apakah perlu disisir ulang dari CD2/CD3?
- [ ] Insiden "verbondbreking" [61] — dapatkah diidentifikasi dari korpus GM/Daghregister periode 1679-1681?
- [ ] Apakah [98] 1731 (sengketa perangkap ranjau Pasariboe) termasuk episode ini atau episode terpisah?
- [ ] Rantai 1693→1694→1707→1755→1775 (bawahan Barus: Batahan/Dairi/Singkil/Pasariboe) — apakah ini sub-episode independen atau perpanjangan episode induk Barus? **Belum diputuskan dalam dossier ini.**
- [ ] `actor_identity_stable: AMBIGUOUS` — perlu genealogi radja Barus dari sumber sekunder untuk memastikan garis suksesi.
