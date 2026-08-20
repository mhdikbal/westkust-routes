# Inderapura Episode Dossier (Draft)

> **DRAFT FOR RESEARCHER REVIEW — NOT IMPLEMENTED — NOT A FINAL HISTORICAL INTERPRETATION**

Sumber: `data/research/linimasa_events.csv` (baris dirujuk sbg nomor urut CSV). `id` Postgres `NOT AVAILABLE`.

**BATASAN KHUSUS KLASTER INI (keputusan peneliti, default sementara — wajib dipakai sebagai titik berangkat, bukan kesimpulan tertutup):**

| Field | Nilai default |
|---|---|
| `relationship_status` | `reciprocal_breach` |
| `breach_attributed_to` | `voc` |
| `interpretive_status` | `contractual_dispute` |
| `researcher_review_required` | `true` |

**Larangan eksplisit:** JANGAN mengklasifikasikan tindakan Sultan Mametchia sebagai defeksi searah sebelum kewajiban resiprokal VOC diperiksa penuh.

---

## Episode Identity

| Field | Nilai |
|---|---|
| `episode_id` | EP-INDERAPURA-01 |
| `cluster` | Inderapura |
| `title` | Aliansi Inderapura-VOC, peralihan ke Inggris, dan pemulihan 1665–1716 |
| `start_date` / `end_date` | 1665 / 1716 |
| `date_precision` | `year` |
| `location_ids` | Inderapura (Indrapoura/Indrapoera) |
| `actor_ids` | Sultan Mametcha/Mametchia; sultan Radja Passisir Barat (1716, kemungkinan penerus) |
| `counterparty_ids` | VOC (Komandan Joan van Leene, dll.); Inggris/EIC (1686-1715) |
| `end_date_status` | `resolved` — 1716 mencatat pemulihan eksplisit, tapi lihat §Unresolved soal traktat 1663 yang dirujuk |

## Reconstructed Events (tabel ringkas)

| CSV baris | Tahun | `event_type` | `dominion_status` | Aktor | Penerima | `source_document` | `book_page` |
|---|---|---|---|---|---|---|---|
| [41] | 1665 | perjanjian | voc_alliance | VOC; Sultan Mametcha; orang-orang Padang | — | 1665 | NOT AVAILABLE (`?` di CSV) |
| [71] | 1686 | konflik | foreign_orbit | Sultan Mametchia | Komandan Joan van Leene (VOC) → EIC | buku-vogel-1690 | 682-683 |
| [96] | 1716 | perjanjian | voc_alliance | sultan Radja Passisir Barat + 20 mantrijs | Bernard Draypon (VOC) | CD4 | 483-484 |

## Documentary Claim (kutipan `text_asli` verbatim)

**[71] 1686 (Vogel):**
> *"Nunmehro ist der Sultaen zu Inderapoura mit seinem gantzen Königreich und Landen von der Niederländischen Ost-Indischen Compagnie (weiln er hülffloß gelassen und ungeacht vieles implorirens beym Commendeur... keine assistenz erlangen können) abgetreten, und hat sich Anno 1686 unter protection der Engellander begeben, welche in selbigen district den gantzen Pfeffer-Handel an sich gezogen."*

Dipecah per lapis:
- `claim_type: factual_assertion` — "abgetreten... unter protection der Engellander begeben" (Sultan menyerahkan diri dari VOC, masuk perlindungan Inggris). Tindakan yang diamati, bukan disimpulkan.
- `claim_type: causal_assertion` — **"weiln er hülffloß gelassen und ungeacht vieles implorirens... keine assistenz erlangen können"** (KARENA dibiarkan tanpa bantuan, dan meski berkali-kali memohon, tidak bisa memperoleh bantuan apa pun). **Ini pernyataan sebab-akibat yang dibuat SUMBER SENDIRI, bukan inferensi peneliti** — dan sebab yang dinyatakan adalah kegagalan VOC, bukan tindakan Sultan.
- `claim_type: factual_assertion` — "Engellander... den gantzen Pfeffer-Handel an sich gezogen" (Inggris kuasai perdagangan lada distrik itu) — indikasi motif ekonomi paralel, dicatat terpisah dari klaim kausal di atas.

**[96] 1716:**
> *"...den sultan, Radja Passisir Barat en syne 20 mantrijs 't contract, in den jare 1663 met d'E. Comp[agnie] aengegaen, op een plegtige wyse door aflegginge van den eed op haren alcoran vernieuwt en gewillig aengenomen."*
> *(Konteks tambahan dari `text_asli`): "In April 1715 schreef hij een brief... waarin hij er onder allerlei schoone beloften, op aandrong 'een pagger en pakhuys vanwegens d'E. Comp[agnie] tot Indrapoura te stabileren'"*

`claim_type: factual_assertion`. **Rujukan eksplisit ke kontrak 1663** — BUKAN ke aliansi 1665 [41] yang ada di data ini. Sultan (atau penerusnya) yang berinisiatif mengirim surat memohon VOC mendirikan kembali pagar/gudang — indikasi bahwa inisiatif pemulihan datang dari pihak Inderapura, bukan represi VOC.

## Commitment Classification

| CSV baris | `commitment_classification` | Dasar |
|---|---|---|
| [41] 1665 | `substantive_commitment` (dugaan) — `AMBIGUOUS` soal kelengkapan syarat | Aktor+lokasi ada; kewajiban SPESIFIK, bentuk persetujuan detail, dan `folio_or_page` `NOT AVAILABLE` (`book_page='?'` di CSV) — provenance tidak lengkap |
| [96] 1716 | `treaty_renewal` | Teks eksplisit "vernieuwt" (diperbarui), merujuk kontrak 1663 |

## Obligation

| `obligation_id` | `obligated_actor` | `beneficiary_actor` | `obligation_modality` | Isi |
|---|---|---|---|---|
| OB-INDRA-01 | VOC | Sultan Mametchia/Inderapura | `required_action` | Memberi `assistenz` (bantuan/perlindungan) — **`obligation_specificity: implied`**, disimpulkan dari klaim [71] bahwa bantuan "diminta berkali-kali" (`vieles implorirens`), BUKAN dikutip langsung dari teks traktat 1663/1665 |
| OB-INDRA-02 | Sultan Radja Passisir Barat (1716) | VOC | `required_action` | Sumpah setia di atas Alquran, penerimaan kembali kontrak 1663 |

## Reciprocal Obligation

**Ini adalah pengujian utama dossier ini — dijalankan sesuai instruksi §"Khusus Inderapura" pada protokol.**

| `obligation_id` | `reciprocal_obligation_id` | `reciprocal_actor` | `reciprocity_check_note` |
|---|---|---|---|
| OB-INDRA-01 (kewajiban VOC memberi bantuan) | OB-INDRA-01 (menopang dirinya sendiri sbg premis aliansi) | Sultan Mametchia | **"reciprocal obligation mentioned but unspecific"** — klaim [71] menyatakan kewajiban ini secara implisit-retrospektif (baru terlihat ketika DILANGGAR), teks traktat 1663/1665 yang secara eksplisit mencantumkannya sbg pasal tertulis: `NOT AVAILABLE` di data ini |
| OB-INDRA-02 | — | — | `no reciprocal obligation in text` pada kutipan [96] yang tersedia — tapi surat April 1715 Sultan (dikutip di `text_asli` [96]) MEMOHON pendirian pagar/gudang VOC, yang secara fungsional adalah permintaan kewajiban VOC baru |

**Temuan uji:** schema **berhasil merepresentasikan** kegagalan VOC tanpa memaksa `obligated_actor: local_actor`. `OB-INDRA-01` secara eksplisit `obligated_actor: VOC`. Titik lemahnya bukan pada schema, melainkan pada data sumber: kewajiban VOC ini baru TERLIHAT retrospektif melalui klaim kausal Vogel, bukan tercatat sbg pasal tertulis independen. `obligation_specificity: implied` mencatat kelemahan ini secara eksplisit alih-alih menyembunyikannya.

## Implementation Evidence & Commitment-Action Relationship (Dimensi A)

| Pasangan | `pairing_basis` | `pairing_strength` | `dimension_a_value` |
|---|---|---|---|
| OB-INDRA-01 ([41]/traktat 1663 tersirat) → [71] 1686 | Klaim kausal eksplisit Vogel: kegagalan bantuan → peralihan | **explicit** (untuk kewajiban VOC) | **`reciprocal_breach`** (default keputusan peneliti — dipertahankan, bukan diusulkan ulang) |
| [71] 1686 → [96] 1716 | Rujukan eksplisit [96] ke "contract... 1663", sumpah dipulihkan | **strong** (rujukan tekstual eksplisit, TAPI ke titik 1663 yang bukan baris [41] 1665) | `substantially_fulfilled` — pemulihan penuh via sumpah Alquran, diinisiasi permintaan pihak Inderapura sendiri (surat 1715) |

`evaded` **tidak dipakai** untuk tindakan Sultan Mametchia — tidak ada `DocumentaryClaim` yang menyatakan Sultan "menghindar"; sebaliknya, klaim sumber justru menyatakan Sultan bertindak SETELAH permohonan berulang gagal, yaitu tindakan terbuka (`abgetreden`/menyerahkan diri secara eksplisit), bukan penghindaran diam-diam.

## VOC Response

| Episode | `response_type` | `response_date` | Catatan |
|---|---|---|---|
| [71] 1686 | `no_response_documented` dari VOC terhadap peralihan itu sendiri — tidak ada catatan represi/upaya rebut kembali segera | 1686 | Konsisten dengan klaim bahwa VOC memang tidak mampu memberi bantuan pada periode ini |
| [96] 1716 | `renegotiation` / `renewal_of_treaty`, diinisiasi permintaan Inderapura (surat April 1715) | 1716 | VOC merespons PERMINTAAN, bukan menghukum pembelotan |

## Source Characterization

| Sumber | `characterization_text` | Catatan |
|---|---|---|
| [71] Vogel | "hülffloß gelassen" (dibiarkan tanpa bantuan) | `normative_characterization` DARI SUDUT PANDANG kegagalan VOC — arah karakterisasi BERBEDA dari klaster lain (bukan menyalahkan aktor lokal) |
| [71] Vogel | tidak ada kata setara "Meineyd"/"ontrouw" dipakai untuk episode ini | Catatan penting: kosakata tuduhan yang dipakai untuk Koto Tangah/Barus TIDAK muncul di sini |

## Evidence Supporting Resistance Interpretation

- Peralihan ke kekuatan asing lain (Inggris) bisa dibaca sebagai bentuk agensi strategis (memanfaatkan aliansi alternatif) — **relevan untuk Dimensi B `possible_resistance_candidate`**, TAPI harus dibaca berdampingan dengan §Evidence Weakening berikut.

## Evidence Weakening Resistance Interpretation

- **Sumber utama sendiri (Vogel) menyatakan sebab peralihan adalah kegagalan VOC memberi bantuan yang diminta berkali-kali** — ini bukan bukti lemah, ini bukti langsung yang mengarah ke `contractual_dispute`/`probable_constraint_or_incapacity`, bukan resistensi.
- Pemulihan 1716 diinisiasi PERMINTAAN pihak Inderapura (surat 1715), bukan penaklukan VOC — pola ini tidak konsisten dengan narasi "resistensi yang ditumpas", melainkan lebih dekat ke "hubungan dagang yang diarahkan ulang lalu dipulihkan atas inisiatif kedua pihak".

## Alternative Explanations

| Alternatif | Didukung bukti? | Catatan |
|---|---|---|
| **Kegagalan pihak lawan memenuhi kewajiban timbal-balik** | **Ya, eksplisit di sumber** | Kandidat terkuat di seluruh empat klaster pilot |
| Persoalan ekonomi | Ya, sebagian | "Engellander... den gantzen Pfeffer-Handel an sich gezogen" — Inggris menguasai dagang lada, motif ekonomi paralel |
| Perang/persaingan Eropa | Sebagian | Persaingan VOC-Inggris pasca-1684 (Inggris diusir dari Bantam) adalah konteks periode ini |
| Ketidakmampuan (pihak VOC, bukan lokal) | Ya, tersirat | Kegagalan beri bantuan mengindikasikan keterbatasan kapasitas VOC pada periode itu, bukan pilihan sepihak |

## Causal Readiness

| Kriteria | Nilai |
|---|---|
| `cause_defined` | **Ya** — kegagalan bantuan VOC, dinyatakan sumber |
| `outcome_defined` | Ya — peralihan ke perlindungan Inggris |
| `temporal_order_reliable` | Ya, tapi `report_delay_known: false` (Vogel menulis ~1690 tentang klaim yang mungkin berasal dari periode berbeda) |
| `mechanism_evidence` | `partial` — mekanisme naratif jelas ("ditinggal → cari pelindung lain"), tapi tidak dirinci proses institusionalnya |
| `alternative_explanations_recorded` | Ya |
| `comparison_case_available` | Tidak (kasus tunggal di pilot ini) |
| `actor_identity_stable` | Ya — Sultan Mametcha/Mametchia konsisten disebut di [41] dan [71] |
| `location_identity_stable` | Ya |
| `report_delay_known` | Tidak |
| `archival_density_known` | Tidak |
| `ready_for_process_tracing` | **`partially_ready`** — kasus terkuat di antara 4 klaster untuk kriteria ini, karena mekanisme dan alternatif sudah tersurat di sumber primer sendiri |

## Interpretive Status (Dimensi B)

| Field | Nilai |
|---|---|
| `dimension_b_value` | **`contractual_dispute`** (default keputusan peneliti, dipertahankan setelah tinjauan bukti di dossier ini) |
| `evidence_for` (constraint/dispute) | Klaim kausal eksplisit Vogel; ketiadaan respons represif VOC; pemulihan atas inisiatif Inderapura sendiri |
| `evidence_against` (utk resistensi) | Sumber tidak memakai kosakata tuduhan (`Meineyd`/`ontrouw`) untuk episode ini — kontras eksplisit dengan Barus/Koto Tangah |
| `alternative_explanations` | Kegagalan resiprokal VOC (utama); motif ekonomi (Inggris kuasai lada); persaingan geopolitik Eropa |
| `confidence` | Sedang-tinggi untuk `contractual_dispute`; rendah untuk klaim resistensi murni |
| `interpretation_source` | `source_derived` |
| `eligible_as_evidence` | `true` |
| `researcher_review_required` | **`true`** |
| `decision_status` | `draft` |
| `breach_attributed_to` | **`voc`** (dipertahankan sesuai default keputusan peneliti — TIDAK ditemukan bukti di dossier ini yang membalikkan default ini) |

## Unresolved Questions

- [ ] Traktat 1663 yang dirujuk [96] tidak punya baris `linimasa_events` tersendiri untuk Inderapura — rantai rujukan tekstual dan rantai data tidak berimpit sempurna. `commitment_event_id` yang sebenarnya dirujuk [96]: **NOT AVAILABLE**.
- [ ] `book_page` [41] 1665 tercatat `?` di CSV sumber — provenance folio tidak lengkap, perlu verifikasi ulang terhadap `1665` (source_document).
- [ ] Apakah "sultan Radja Passisir Barat" (1716) individu yang sama dengan "Sultan Mametchia" (1686), atau penerus? `actor_identity_stable` dinilai `Ya` di atas berdasarkan kontinuitas gelar dan rujukan kontrak yang sama — tapi identitas individu tidak diverifikasi silang.
- [ ] Kondisi Inderapura 1665-1686 (antara aliansi awal dan peralihan) — apakah ada bukti permohonan bantuan sebelum 1686 yang tidak masuk `linimasa_events`? Perlu sisir GM/Daghregister periode itu.
