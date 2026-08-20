# Pilot Claim Ledger

> **DRAFT FOR RESEARCHER REVIEW — NOT IMPLEMENTED — NOT A FINAL HISTORICAL INTERPRETATION**

Konsolidasi seluruh `DocumentaryClaim` yang diekstrak di keempat dossier pilot (`BARUS_EPISODE_DOSSIER_DRAFT.md`, `INDERAPURA_EPISODE_DOSSIER_DRAFT.md`, `PARIAMAN_EPISODE_DOSSIER_DRAFT.md`, `KOTO_TANGAH_EPISODE_DOSSIER_DRAFT.md`). **Interpretasi tidak dimasukkan sebagai `documentary` fact** — lihat kolom `claim_level`.

| `claim_id` | `cluster` | `claim_text` (ringkas, kutipan penuh ada di dossier) | `claim_level` | `supporting_source` | `contradicting_source` | `provenance_status` | `confidence` | `researcher_review_required` |
|---|---|---|---|---|---|---|---|---|
| CL-BARUS-01 | Barus | "...alle het onverdraeglijcke Aetchinse jock ende volck afgeworpen..." (lepas dari kuk Aceh) | `documentary` | CD2 p383-384 [45] | — | folio lengkap | tinggi (kutipan verbatim tersedia) | true |
| CL-BARUS-02 | Barus | "Vernieuwinge soo van 't eerste, twede, als derde vredeverbond" (pembaruan traktat ke-1/2/3) | `documentary` | CD3 p197-198 [57] | — | folio lengkap; traktat "ke-2"/"ke-3" yg dirujuk `NOT AVAILABLE` sbg baris terpisah | tinggi utk keberadaan rujukan; rendah utk isi traktat yg dirujuk | true |
| CL-BARUS-03 | Barus | "sodanige verbondbreking noyt meer te sullen beginnen" (janji tak akan lagi memulai pelanggaran) | `documentary` | CD3 p228-230 [61] | — | folio lengkap; insiden spesifik pelanggaran `NOT AVAILABLE` | sedang | true |
| CL-BARUS-04 | Barus | Pengakuan `verbondbreking` [61] MENGINDIKASIKAN pelanggaran pernah terjadi | `reconstructed` | turunan CL-BARUS-03 | tidak ada respons militer tercatat (kontras Koto Tangah) | — | rendah | true |
| CL-BARUS-05 | Barus | Payoff Model 6 "+0.4 Elite lokal di voc_alliance" mencerminkan "otonomi ternegosiasi" | `causal_hypothesis` (sesungguhnya: `model_derived`, TIDAK dipromosikan) | `docs/thesis/colab/model6_game_theory.py` L94-99 | — | **`eligible_as_evidence: false`** — dicatat, tidak dipakai | — (model-derived, di luar skala confidence hermeneutis) | true |
| CL-INDRA-01 | Inderapura | "abgetreten... unter protection der Engellander begeben" (menyerahkan diri, masuk perlindungan Inggris) | `documentary` | buku-vogel-1690 p682-683 [71] | — | folio lengkap | tinggi | true |
| CL-INDRA-02 | Inderapura | "weiln er hülffloß gelassen und ungeacht vieles implorirens... keine assistenz erlangen können" (KARENA dibiarkan tanpa bantuan meski berkali-kali memohon) | `documentary` (klaim kausal DARI SUMBER, bukan inferensi peneliti) | buku-vogel-1690 p682-683 [71] | — | folio lengkap | tinggi utk keberadaan klaim; rendah utk verifikasi independen alasan sebenarnya | true |
| CL-INDRA-03 | Inderapura | "den sultan... 't contract, in den jare 1663... vernieuwt" (kontrak 1663 diperbarui) | `documentary` | CD4 p483-484 [96] | — | folio lengkap; traktat 1663 itu sendiri `NOT AVAILABLE` sbg baris terpisah utk Inderapura | tinggi utk rujukan; rendah utk isi 1663 | true |
| CL-INDRA-04 | Inderapura | Sebab peralihan 1686 adalah kegagalan resiprokal VOC, bukan defeksi searah | `hermeneutic` | turunan CL-INDRA-02 | tidak ada — ini interpretasi berbasis CL-INDRA-02 langsung, bukan bertentangan dengannya | — | sedang-tinggi (jarang ada dukungan sekuat ini di data lain) | true |
| CL-PARIAM-01 | Pariaman | "sloot de meerderheid der Priamanse regenten zich weer bij de Atjehsche partijgangers aan" (mayoritas regenten kembali ke faksi Aceh) | `documentary` — **campuran** dengan narasi sekunder dalam satu kutipan `text_asli` | CD3 p160-161 [55] | — | `AMBIGUOUS`: batas traktat-asli vs narasi-sekunder dalam satu cuplikan tidak jelas | rendah-sedang | true |
| CL-PARIAM-02 | Pariaman | "niet sullen vermogen eenige vaartuygen naar Aetchin te laten afvaren" (larangan berlayar ke Aceh) | `documentary` | CD3 p290-291 [66] | — | folio lengkap | tinggi | true |
| CL-PARIAM-03 | Pariaman | "niemand... eenige correspondentie... nog eenigen handel... nog derwaars varen" (larangan diperluas: korespondensi+dagang+berlayar) | `documentary` | CD3 p351-355 [68] | — | folio lengkap | tinggi | true |
| CL-PARIAM-04 | Pariaman | Pelebaran larangan [66]→[68] mengindikasikan larangan pertama tidak efektif | `reconstructed` (pola disimpulkan, BUKAN pernyataan langsung sumber) | turunan CL-PARIAM-02/03 | tidak ada `implementation_event` yg mendokumentasikan pelanggaran spesifik | — | rendah (`evidence_status: pattern_inferred`) | true |
| CL-KT-01 | Koto Tangah | "sifat tidak setia orang Sumatra dengan melepaskan beban ketaatan" | `documentary` — `normative_characterization`, generalisasi etnis-kolonial (Valentijn via buku Padang 1718) | buku-padang-1718 p238 [48] | — | folio lengkap, TAPI sumber adalah kompilasi 1718 mengutip Valentijn — rantai kutipan berlapis | rendah utk generalisasi; tinggi utk fakta "diserang & dibakar" | true |
| CL-KT-02 | Koto Tangah | "dieses Refort Cotatenga ift A. 1670. 1678. 1682. und 1686. wegen ihres vielfältigen Meineydes... gäntzlich ruinirt, nachmahls... wieder zu Bundes-Genossen... angenommen" | `documentary` — `normative_characterization` ("Meineyd") + `factual_assertion` (dihancurkan lalu diterima kembali) | buku-vogel-1690 p674-675 [115]&[116] — **SATU sumber utk DUA baris data** | — | folio lengkap utk sumber; **tahun 1682 dalam daftar ini `NOT AVAILABLE` sbg baris data terpisah** | tinggi utk keberadaan klaim Vogel; **rendah utk detail per-tahun 1678/1682/1686** (satu kalimat, tanpa rincian) | true |
| CL-KT-03 | Koto Tangah | Koto Tangah (Cottetenge) + Pauh serang Padang Juni 1676; blokade dagang emas; kontak Aceh via sungai Narra | `documentary` | gm-vol04-05 RGP4/p101 [121] | — | folio lengkap; sumber PRIMER periode (kontras Vogel retrospektif) | tinggi | true |
| CL-KT-04 | Koto Tangah | CL-KT-03 (GM 1676) memperkuat plausibilitas pola umum, TAPI tidak memverifikasi detail 1678/1682/1686 spesifik | `hermeneutic` — penilaian pembanding sumber | turunan CL-KT-02, CL-KT-03 | tahun tidak tumpang tindih (1676 vs 1678/1682/1686) | — | sedang | true |
| CL-KT-05 | Koto Tangah | Pemulihan [52] 1671 terjadi setelah "protes keras dari Raja Minangkabau" | `documentary` | buku-padang-1718 p238 [52] | — | folio lengkap | tinggi | true |
| CL-KT-06 | Koto Tangah | Episode ini konsisten dengan kandidat resistensi | `hermeneutic` | Dimensi B `possible_resistance_candidate` (dossier Koto Tangah) | Karakterisasi bersumber tunggal; intervensi pihak ketiga (CL-KT-05); tahun 1682 tanpa bukti | — | **rendah** | true |

## Ringkasan menurut `claim_level`

| `claim_level` | Jumlah | Catatan |
|---|---|---|
| `documentary` | 11 | Klaim langsung dari kutipan `text_asli` — termasuk klaim normatif sumber (`Meineyd`, "tidak setia"), yang tetap `documentary` karena itu **klaim yang dibuat dokumen**, bukan penilaian peneliti |
| `reconstructed` | 2 | Sintesis peneliti dari beberapa `documentary claim`, tanpa penilaian nilai |
| `evaluative` | 0 | **Tidak ada klaim di level ini pada pilot ini** — seluruh penilaian yang mengandung nilai jatuh ke `hermeneutic` di bawah, bukan dibiarkan mengambang sbg "evaluative" tanpa status interpretif |
| `hermeneutic` | 3 | Penilaian eksplisit peneliti; seluruhnya `researcher_review_required: true` |
| `causal_hypothesis` | 1 | CL-BARUS-05 (payoff Model 6) — **secara sengaja ditandai `eligible_as_evidence: false`, tidak dipromosikan ke `hermeneutic` manapun** |

## Larangan yang dipatuhi dalam ledger ini

- Tidak ada baris `documentary` yang memuat kata "resistensi"/"defeksi" sebagai fakta — kata itu hanya muncul di kolom `claim_level: hermeneutic` (CL-INDRA-04, CL-KT-06) dengan `researcher_review_required: true`.
- CL-BARUS-05 (Model 6) dicatat **tapi tidak dipakai** untuk mendukung CL-BARUS-04 atau interpretasi Barus manapun — konsisten dengan batasan §5 keputusan peneliti.
