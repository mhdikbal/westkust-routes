# Koto Tangah Episode Dossier (Draft)

> **DRAFT FOR RESEARCHER REVIEW — NOT IMPLEMENTED — NOT A FINAL HISTORICAL INTERPRETATION**

Sumber: `data/research/linimasa_events.csv` (baris dirujuk sbg nomor urut CSV). `id` Postgres `NOT AVAILABLE`.

**BATASAN KHUSUS KLASTER INI (keputusan peneliti, wajib dipatuhi):**
- `ready_for_process_tracing` **tidak boleh melebihi `descriptive_only`** tanpa sumber pembanding independen dari Vogel.
- Karakterisasi Vogel ("Meineyd") **wajib** disimpan sbg `source_characterization`, terpisah dari klasifikasi peneliti.
- Tahun **1682** (disebut Vogel sbg salah satu dari 4 titik siklus) **tidak punya baris `linimasa_events`** — kekosongan ini **tidak diisi dengan asumsi apa pun**.
- GM 1676 [121] diperiksa eksplisit sbg kandidat sumber pembanding yang sudah tersedia di repository.

---

## Episode Identity

| Field | Nilai |
|---|---|
| `episode_id` | EP-KOTOTANGAH-01 |
| `cluster` | Koto Tangah |
| `title` | Siklus penghancuran-penundukan-ulang Koto Tangah, 1670–1705 |
| `start_date` / `end_date` | 1670 / 1705 |
| `date_precision` | `year` |
| `location_ids` | Koto Tangah |
| `actor_ids` | Penduduk Koto Tangah ("Cotatenga") |
| `counterparty_ids` | VOC |
| `end_date_status` | `evidence_exhausted` |

## Reconstructed Events (tabel ringkas)

| CSV baris | Tahun | `event_type` | `dominion_status` | Aktor | `source_document` | `book_page` |
|---|---|---|---|---|---|---|
| [48] | 1670 | konflik | internal_conflict | Penduduk Koto Tangah vs VOC | buku-padang-1718 | 238 |
| [52] | 1671 | perjanjian | voc_alliance | Penduduk Koto Tangah (pulang dari pengasingan) & Raja Minangkabau → VOC | buku-padang-1718 | 238 |
| [58] | 1680 | perjanjian | voc_alliance | radja Poeti (Kotta-tengah) & Paoeh → komisaris Laurens Pit | CD3 | 219-220 |
| **—** | **1682** | **NOT AVAILABLE** | **NOT AVAILABLE** | **NOT AVAILABLE** | **NOT AVAILABLE** | **NOT AVAILABLE** |
| [115] | 1678 | konflik | internal_conflict | Cotatenga vs VOC | buku-vogel-1690 | 674-675 |
| [116] | 1686 | konflik | internal_conflict | Cotatenga vs VOC | buku-vogel-1690 | 674-675 |
| [90] | 1705 | perjanjian | voc_alliance | Koto Tangah → VOC | buku-padang-1718 | 238 |
| [121] | 1676 | konflik | internal_conflict | Koto Tangah (Cottetenge) + Pauh vs Padang | gm-vol04-05 | RGP4/p101 |

**Catatan struktural penting:** [115] dan [116] adalah **DUA baris `linimasa_events`, satu `SourceRecord`, satu `DocumentaryClaim`**. Kutipan `text_asli` keduanya **identik persis** — bukan dua kesaksian independen tentang dua tahun berbeda, melainkan satu kalimat Vogel yang menyebut empat tahun sekaligus, dipecah manual oleh peneliti proyek menjadi dua baris data. Ini harus terlihat eksplisit di `supporting_claim_ids` bersama, bukan tersembunyi di balik dua ID event yang tampak independen.

## Documentary Claim (kutipan `text_asli` verbatim)

**[48] 1670 (buku Padang 1718, mengutip Valentijn):**
> *"Pada Maret 1670, Koto Tengah lagi-lagi memberikan demonstrasi mengenai 'sifat tidak setia orang Sumatra dengan melepaskan beban ketaatan dari pundak mereka'. Akibat ketidaktaatannya itu, Koto Tangah diserang, semua wilayah nagari itu direbut dan dibakar dalam waktu yang singkat oleh Kompeni."*

`claim_type: normative_characterization` untuk frasa "sifat tidak setia orang Sumatra dengan melepaskan beban ketaatan" — **ini kutipan Valentijn (via buku Padang 1718), karakterisasi generik tentang "orang Sumatra", bukan deskripsi spesifik Koto Tangah**. `claim_type: factual_assertion` untuk "diserang, semua wilayah nagari itu direbut dan dibakar".

**[52] 1671:**
> *"Kalah perang, penduduk Koto Tangah mengembara sebagai orang buangan yang terlunta-lunta. Setelah mendapat protes keras dari Raja Minangkabau, barulah mereka diizinkan kembali pulang ke kampung mereka, dan perjanjian baru dibuat antara mereka dengan Kompeni pada tanggal 8 September 1671."*

`claim_type: factual_assertion`. **Penting:** pemulihan terjadi setelah **protes Raja Minangkabau** — pihak ketiga aktif melakukan intervensi diplomatik, bukan Koto Tangah semata-mata "dibiarkan kembali" oleh VOC. Ini detail agensi eksternal yang sering hilang bila episode diringkas sebagai "dihukum lalu diterima kembali".

**[115]/[116] 1678/1686 (Vogel, ~1690, kutipan identik untuk dua baris):**
> *"dieses Refort Cotatenga ift A. 1670. 1678. 1682. und 1686. wegen ihres vielfältigen Meineydes durch der Niederländischen Ost-Indischen Compagnie Waffen gäntzlich ruinirt, nachmahls aber wieder zu Bundes-Genossen auf und angenommen worden."*

`claim_type: normative_characterization` untuk **"vielfältigen Meineydes"** (perjurian berulang-ulang) — **disimpan sebagai karakterisasi sumber, TIDAK sebagai fakta**, sesuai batasan keputusan peneliti. `claim_type: factual_assertion` untuk "durch... Waffen gäntzlich ruinirt, nachmahls... wieder zu Bundes-Genossen... angenommen" (dihancurkan senjata VOC, kemudian diterima kembali sbg sekutu).

**[121] 1676 (Generale Missiven — diperiksa sbg sumber pembanding, sesuai instruksi):**
> Ringkasan dari `notes`: Koto Tangah (Cottetenge) + Pauh (Paauw) menyerang Padang Juni 1676; regent memblokir dagang emas dari pedalaman; Koto Tangah mengirim barang/pesan ke Aceh via sungai Narra tahun sebelumnya.

`claim_type: factual_assertion` (serangan ke Padang, blokade dagang emas) + indikasi kontak dengan Aceh. **Ini adalah sumber PRIMER periode (Generale Missiven vol.04), berbeda dari Vogel yang retrospektif ~1690.**

## Comparison Source Check: GM 1676 [121] vs Vogel [115]/[116]

| Aspek | GM 1676 [121] | Vogel 1678/1686 [115]/[116] |
|---|---|---|
| Jenis sumber | Primer periode (laporan administratif VOC kontemporer) | Sekunder retrospektif (buku perjalanan, ~14-24 tahun setelah peristiwa) |
| Sifat tuduhan | Tindakan konkret (serang Padang, blokade dagang, kontak Aceh) | Karakterisasi moral umum ("Meineyd") tanpa rincian tindakan per-tahun |
| Tahun yang dicakup | 1676 (tidak termasuk dalam daftar Vogel: 1670/1678/1682/1686) | 1670/1678/1682/1686 |
| Independensi | Sumber berbeda (GM vs buku Vogel) | — |

**Hasil pemeriksaan:** GM 1676 **BUKAN pembanding langsung** untuk klaim 1678/1686 Vogel — tahunnya berbeda dan tidak tumpang tindih dengan keempat titik siklus Vogel. Namun GM 1676 **secara independen mengonfirmasi pola umum** (Koto Tangah berulang kali berkonflik dengan otoritas Padang/VOC dan punya kontak dengan Aceh) dari sumber primer yang tidak bergantung pada Vogel. Ini **memperkuat plausibilitas pola berulang secara umum**, tetapi **TIDAK memverifikasi** detail spesifik tahun 1678/1682/1686 yang hanya berasal dari satu kalimat Vogel. `comparison_case_available: partial` — bukan `true` penuh.

## Commitment Classification

| CSV baris | `commitment_classification` | Dasar |
|---|---|---|
| [52] 1671 | `substantive_commitment` — `AMBIGUOUS` soal `representational_scope` | Persetujuan dibuat setelah intervensi Raja Minangkabau, bukan murni Koto Tangah-VOC bilateral — pihak ketiga terlibat dalam pembentukan komitmen |
| [58] 1680 | `coerced_or_constrained_commitment` | Teks [58] sendiri (di dossier lain, sumber sama CD3): ekspedisi militer Laurens Pit mendahului "tunduk" — `commitment_under_duress: military_action_preceding` |
| [90] 1705 | `treaty_renewal` | "akhiri sengketa berulang soal otoritas Panglima Padang" — **catatan: ini soal OTORITAS TAMBATAN KAPAL, isu ADMINISTRATIF, bukan soal kesetiaan-Aceh yang jadi tema Vogel** |

## Obligation

**`NOT AVAILABLE` secara rinci** — kutipan `text_asli` yang tersimpan untuk episode ini (terutama [48]/[52]/[115]/[116]) adalah **narasi ringkas**, bukan kutipan traktat berpasal. Berbeda dari Barus/Pariaman yang punya kutipan traktat verbatim berisi kewajiban spesifik, Koto Tangah hanya punya:

| `obligation_id` | `obligated_actor` | `obligation_modality` | Status |
|---|---|---|---|
| OB-KT-01 | Koto Tangah | `required_action` (tersirat: "ketaatan"/`ketaatan`) | `obligation_specificity: implied` — tidak ada kutipan pasal spesifik apa yang dilanggar |

## Reciprocal Obligation

`NOT AVAILABLE` untuk seluruh episode ini — tidak ada kutipan traktat berpasal yang bisa diperiksa untuk kewajiban VOC.

## Implementation Evidence & Commitment-Action Relationship (Dimensi A)

| Pasangan | `pairing_basis` | `pairing_strength` | `dimension_a_value` |
|---|---|---|---|
| [52] 1671 → [115] 1678 | Sumber TUNGGAL Vogel menyebut 1670/1678/1682/1686 sbg satu daftar berulang, memakai frasa "Meineyd" (perjurian berulang) — rujukan eksplisit ke pola, bukan inferensi peneliti | **explicit** (untuk keberadaan pola menurut Vogel) | `openly_refused`/`contradicted` menurut KARAKTERISASI Vogel — **TAPI** `cannot_determine` menurut standar bukti langsung (tidak ada rincian tindakan spesifik 1678, hanya label) |
| [115] 1678 ↔ [116] 1686 | Kutipan sumber **identik** — satu klaim, dua baris data | **explicit (by construction)** — bukan pemasangan dua peristiwa independen | Tidak berlaku sebagai "pasangan komitmen-deviasi" biasa; ini adalah **satu klaim tunggal tersebar ke dua titik waktu** |
| **1682** (disebut Vogel) | — | — | **`NOT AVAILABLE` — tidak ada `HistoricalEvent` untuk tahun ini di data. Kekosongan TIDAK diisi.** |
| [58] 1680 → [90] 1705 | Judul [90] eksplisit: "akhiri sengketa berulang soal otoritas Panglima Padang" | **possible** | `AMBIGUOUS` — sengketa yang dirujuk soal tambatan kapal, kemungkinan **isu berbeda** dari siklus kesetiaan-Aceh Vogel; tidak boleh disatukan tanpa verifikasi |

**Penerapan aturan `evaded`:** tidak dipakai untuk episode ini sama sekali. Klaim yang tersedia (`Meineyd`) adalah karakterisasi normatif sumber, bukan `DocumentaryClaim` tentang tindakan spesifik menghindar — menyimpannya sebagai `dimension_a_value: evaded` akan memindahkan penilaian Vogel langsung menjadi fakta terklasifikasi, melanggar aturan pemisahan lapis.

## VOC Response

| Episode | `response_type` | `response_date` |
|---|---|---|
| [48] 1670 | `destruction` — "diserang, wilayah direbut dan dibakar" | 1670 |
| [58] 1680 | `military_action` mendahului penundukan (170 tentara + 500 bantuan Padang) | 1680 |
| [115]/[116] (menurut Vogel, tanpa rincian per-tahun) | `destruction`, berulang, diikuti `renewal_of_treaty` ("wieder zu Bundes-Genossen... angenommen") | 1678, 1686 (tanpa detail proses) |

## Source Characterization

| Sumber | `characterization_text` | `claim_type` |
|---|---|---|
| Valentijn (via buku Padang 1718), ttg [48] | "sifat tidak setia orang Sumatra" | `normative_characterization` — generalisasi etnis-kolonial, bukan spesifik Koto Tangah |
| Vogel, ttg [115]/[116] | "vielfältigen Meineydes" (perjurian berulang) | `normative_characterization` |

**Kedua karakterisasi ini TIDAK dipindahkan ke `event_summary` mana pun di dossier ini** — dikutip di sini secara eksplisit dan tidak di tempat lain.

## Evidence Supporting Resistance Interpretation

- Pola berulang empat kali (menurut Vogel) dari perspektif VOC dibaca sebagai "perjurian" — pengulangan itu sendiri, terlepas dari label moralnya, adalah pola faktual yang dicatat sumber independen dari periode berbeda (buku Padang 1718 utk 1670/1671; Vogel utk 1678/1686).
- [121] GM 1676 (sumber primer, independen dari Vogel) mengonfirmasi pola umum konflik berulang Koto Tangah dengan otoritas Padang/VOC dan kontak dengan Aceh — bukan bukti langsung untuk 1678/1686, tapi memperkuat plausibilitas pola.

## Evidence Weakening Resistance Interpretation

- **Satu-satunya sumber untuk 3 dari 4 titik siklus (1678/1682/1686) adalah SATU kalimat Vogel yang ditulis retrospektif ~1690** — tidak ada kesaksian independen untuk detail per-tahun.
- Karakterisasi "Meineyd" adalah kata pihak yang merasa dikhianati (VOC/Vogel) — motif AKTUAL Koto Tangah tidak pernah dinyatakan dari sudut pandangnya sendiri di sumber manapun yang tersedia.
- [52] 1671 menunjukkan pemulihan terjadi setelah intervensi Raja Minangkabau — bukan murni dinamika dua pihak VOC-Koto Tangah, mengindikasikan struktur kekuasaan regional lebih kompleks dari sekadar "tunduk-lepas-tunduk".
- Tahun 1682 (bagian dari daftar Vogel) **tidak punya bukti independen apa pun** di repository — satu dari empat titik "siklus" tidak dapat diverifikasi sama sekali.

## Alternative Explanations

| Alternatif | Didukung bukti? | Catatan |
|---|---|---|
| Bias pelaporan VOC/Eropa | **Tinggi** | Vogel menulis retrospektif dari sudut pandang VOC; kata "Meineyd" adalah karakterisasi pihak yang merasa dikhianati |
| Konflik internal Minangkabau | Sebagian didukung | [52] melibatkan Raja Minangkabau sbg pihak ketiga aktif |
| Perang/tekanan Aceh | Sebagian ([121] GM 1676 mencatat kontak Koto Tangah dengan Aceh) | Tidak diuji formal untuk 1678/1682/1686 spesifik |
| Sengketa administratif independen (bukan siklus tunggal) | Sebagian | [90] 1705 soal otoritas tambatan kapal — kemungkinan isu berbeda yang salah disatukan dengan siklus kesetiaan |
| Kehilangan arsip | Berlaku struktural utk tahun 1682 | Ketiadaan total data tidak dapat dibedakan dari ketiadaan peristiwa |

## Causal Readiness

| Kriteria | Nilai |
|---|---|
| `cause_defined` | Tidak — Vogel tidak menjelaskan MENGAPA "Meineyd" terjadi berulang, hanya mencatat akibatnya |
| `outcome_defined` | Ya (dihancurkan, diterima kembali) |
| `temporal_order_reliable` | `AMBIGUOUS` — presisi tahun saja, dan Vogel menulis ~1690 (jeda pelaporan besar utk 1670) |
| `mechanism_evidence` | Tidak |
| `alternative_explanations_recorded` | Ya |
| `comparison_case_available` | **`partial`** — GM 1676 memberi konteks umum, TIDAK memverifikasi detail spesifik 1678/1682/1686 |
| `actor_identity_stable` | Ya (Koto Tangah sbg entitas kolektif konsisten disebut) |
| `location_identity_stable` | Ya |
| `report_delay_known` | Tidak, kecuali estimasi kasar (Vogel ~1690 utk peristiwa 1670-1686) |
| `archival_density_known` | Tidak |
| `ready_for_process_tracing` | **`descriptive_only` — BATAS KERAS, tidak dinaikkan** |

## Interpretive Status (Dimensi B)

| Field | Nilai |
|---|---|
| `dimension_b_value` | **`possible_resistance_candidate`** — tidak dinaikkan ke `probable` karena ketergantungan sumber-tunggal untuk 3 dari 4 titik |
| `evidence_for` | Pola berulang menurut Vogel; konfirmasi umum dari GM 1676 (kontak Aceh, konflik dgn Padang) |
| `evidence_against` | Sumber tunggal retrospektif untuk detail; karakterisasi moral pihak yang dikhianati; intervensi pihak ketiga (Minangkabau) di [52]; tahun 1682 tanpa bukti sama sekali |
| `alternative_explanations` | Bias pelaporan VOC (tinggi); konflik internal Minangkabau; kemungkinan penggabungan keliru dua isu berbeda (kesetiaan-Aceh vs otoritas tambatan kapal) |
| `confidence` | **Rendah** |
| `interpretation_source` | `source_derived` |
| `eligible_as_evidence` | `true` |
| `researcher_review_required` | **`true`** |
| `decision_status` | `draft` |

## Unresolved Questions

- [ ] **Tahun 1682 tetap `NOT AVAILABLE` — tidak diisi dengan asumsi apa pun di dossier ini, sesuai instruksi eksplisit.** Pencarian tambahan di CD3 (rentang tahun yang sesuai) mungkin diperlukan untuk menemukan baris yang hilang, tapi ini pekerjaan sisir arsip baru, di luar cakupan dossier persiapan ini.
- [ ] Apakah [90] 1705 (soal otoritas tambatan kapal) benar-benar bagian dari siklus kesetiaan-Aceh Vogel, atau isu administratif terpisah yang keliru disatukan secara naratif? `AMBIGUOUS`, perlu keputusan peneliti.
- [ ] Apakah ada entri di `daghregister_corpus_classified.csv`/`gm_corpus_filtered_1660_1789.csv` untuk tahun 1678/1682/1686 spesifik terkait Koto Tangah yang belum pernah disisir ke `linimasa_events`? Ini bisa menjadi sumber pembanding independen KEDUA — di luar cakupan dossier ini, dicatat sbg rekomendasi untuk `PILOT_CLAIM_LEDGER.md`.
- [ ] Genealogi kepemimpinan Koto Tangah antar-1670-1705 — `NOT AVAILABLE`, aktor selalu disebut kolektif ("penduduk"/"Cotatenga").
