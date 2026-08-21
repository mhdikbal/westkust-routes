# Padang Institutional Schema V1 (Draft)

> **DRAFT METHODOLOGICAL SPECIFICATION**
> **NOT IMPLEMENTED**
> **NOT PRODUCTION DATA**
> **RESEARCHER REVIEW REQUIRED**

Disusun dari hasil pilot dua dokumen sebelumnya (tidak diubah):
`PADANG_1705_SUCCESSION_SCHEMA_DRAFT.md`, `PADANG_1671_1698_TERMINOLOGY_PILOT_DRAFT.md`.

---

## Status Values (berlaku lintas seluruh modul)

| Status | Definisi |
|---|---|
| `NOT STATED` | Sumber diperiksa; informasi tidak dinyatakan di dalamnya |
| `NOT AVAILABLE` | Sumber yang diperlukan belum tersedia untuk diperiksa |
| `CANNOT DETERMINE` | Bukti tersedia, tetapi ambigu atau tidak cukup untuk kesimpulan |
| `NOT APPLICABLE` | Field tidak relevan untuk dokumen/konteks ini |

**Confidence kategoris** (dipertahankan dari draft sebelumnya, tidak numerik): `high`, `moderate`, `low`, `cannot_assess`.

---

## Modul A — Source and Documentary Claim

| Field | Definisi | Allowed values |
|---|---|---|
| `source_document` | Identitas dokumen sumber persis | string bebas (mis. "CD2 CCCXXX") |
| `source_page` | Halaman cetak/idx PDF | string bebas |
| `term_as_written` | Istilah persis sebagaimana tertulis dalam sumber | string bebas (kutipan literal) |
| `term_language` | Bahasa istilah | `Belanda`, `Melayu`, `Lain`, `NOT STATED` |
| `documentary_claim` | Ringkasan klaim tekstual murni, tanpa interpretasi | text |
| `source_characterization` | Jenis dokumen (traktat, surat, dsb.) dan sifatnya (primer/editorial) | `primary_treaty_text`, `primary_administrative_letter`, `editorial_narrative`, `NOT STATED` |

---

## Modul B — Office and Classification

| Field | Definisi | Allowed values |
|---|---|---|
| `named_local_office` | Jabatan lokal yang disebut EKSPLISIT dalam teks | daftar string, atau salah satu status |
| `VOC_collective_designation` | Istilah kolektif Belanda yang dipakai VOC | string bebas (mis. "regenten") |
| `designation_scope` | Cakupan penyebutan | `individual`, `kolektif`, `NOT STATED` |
| `classification_target` | Pihak yang menjadi objek klasifikasi VOC | string bebas |
| `classification_relation` | Sifat hubungan antara istilah VOC dan jabatan lokal | `explicit_collective_VOC_classification`, `explicit_equivalence`, `no_relation_stated`, `CANNOT DETERMINE` |
| `formal_title_equivalence` | Apakah istilah VOC = gelar formal tunggal yang menggantikan jabatan lokal | `ESTABLISHED`, `NOT ESTABLISHED`, `CANNOT DETERMINE` |
| `underlying_local_office` | Jabatan/struktur adat yang mendasari, di luar istilah VOC | string bebas, atau `CANNOT DETERMINE` / `NOT STATED` |

---

## Modul C — Representation and Succession

| Field | Definisi | Allowed values |
|---|---|---|
| `representative_act` | Tindakan konkret yang dilakukan atas nama kelompok (mis. penyerahan tol) | text |
| `representative_scope` | **Cakupan PIHAK YANG TERIKAT oleh tindakan/klausul tertentu** — siapa yang dinyatakan terikat dalam SATU tindakan/dokumen ini | `named_signatories_only`, `named_signatories_and_named_descendants_of_signatories`, `entire_polity`, `NOT STATED`, `CANNOT DETERMINE` |
| `mandate_evidence` | Bukti tekstual bahwa tindakan mewakili mandat komunitas | text, atau `NOT STATED` |
| `community_selection_role` | Peran komunitas luas (di luar penanda-kontrak bernama) dalam pemilihan/suksesi | `NOT ESTABLISHED`, `stated`, `implied` |
| `customary_selection_basis` | Apakah pemilihan berdasar mekanisme adat | `NOT ESTABLISHED`, `stated`, `implied` |
| `hereditary_scope` | **Cakupan LINTAS-GENERASI yang dinyatakan dalam KLAUSUL SUKSESI spesifik** — apakah klausul ITU SENDIRI menyebut keturunan/generasi berikutnya | `explicit_in_this_clause`, `document_wide_only`, `NOT STATED` |
| `succession_rule` | Rujukan ke rule suksesi terkait (jika berlaku) | id rule, atau `NOT APPLICABLE` |

**Pemisahan yang diwajibkan (koreksi dari pilot sebelumnya)**: `representative_scope` menjawab **"siapa terikat pada tindakan/dokumen ini"** (pertanyaan tentang keanggotaan/cakupan pihak SAAT dokumen dibuat); `hereditary_scope` menjawab **"apakah klausul ini secara eksplisit memproyeksikan cakupannya ke generasi mendatang"** (pertanyaan tentang durasi/proyeksi waktu ke depan). Keduanya dapat diisi independen untuk dokumen yang sama — mis. 1671 punya `representative_scope: named_signatories_only` (kolektif tanpa nama individu, tapi terbatas pada penanda-kontrak) SEKALIGUS `hereditary_scope: explicit_in_this_clause` (krn klausul menyebut "nakomelingen").

---

## Modul D — Interpretation and Uncertainty

| Field | Definisi | Allowed values |
|---|---|---|
| `institutional_interpretation` | Pembacaan institusional peneliti, ditandai eksplisit sbg interpretasi | text (wajib dipisah dari Modul A-C) |
| `evidence_for` | Bukti tekstual yang mendukung interpretasi | text |
| `evidence_against` | Bukti tekstual yang melemahkan interpretasi | text |
| `interpretive_confidence` | Tingkat keyakinan interpretasi | `high`, `moderate`, `low`, `cannot_assess` |
| `researcher_review_required` | Penanda wajib tinjau peneliti | boolean |
| `uncertainty_status` | Ringkasan status ketidakpastian field-field kunci | ringkasan status dari empat nilai standar |
| `uncertainty_notes` | Catatan eksplisit hal yang belum diketahui | text |

---

## Pemetaan Tiga Dokumen

### 1671 — CD2 CCCXXX

| Field | Nilai |
|---|---|
| `term_as_written` | "algemeene regenten tot Padang" |
| `VOC_collective_designation` | "regenten" — **collective Dutch designation** |
| `designation_scope` | `kolektif` |
| `named_local_office` | **"panglima Radja"** — **dikoreksi dari `NOT STATED` (CONF-002 verification)**: badan akta eksplisit menyebut "panglima Radja ende d'algemeyne regenten tot Padang", membedakan panglima sbg jabatan individual dari kelompok "regenten" |
| `underlying_local_office` | **`CANNOT DETERMINE`** — identitas individu di balik "algemeene regenten" sendiri (berapa jumlahnya, siapa saja) tetap tak diketahui, meski panglima Radja sbg jabatan terpisah kini diketahui |
| `source_characterization` | **`primary_treaty_text_verified`** (CONF-002 verification) — istilah dikuatkan independen dlm badan akta notarial (Joannes Metman), bukan hanya caption editorial CD | 
| `classification_relation` | `explicit_collective_VOC_classification` — **dikoreksi**: "panglima Radja" TERNYATA disandingkan (via "ende"), TAPI didaftar sbg pihak TERPISAH dari "regenten", bukan bagian dari klasifikasi kolektif itu — relasinya `distinct_from`, bukan `included_in` |
| `formal_title_equivalence` | `NOT ESTABLISHED` |
| `representative_scope` | `named_signatories_only` (kolektif tapi terbatas pada pihak yang menyerahkan tol, bukan "entire_polity") |
| `mandate_evidence` | **`NOT STATED`** |
| `hereditary_scope` | `explicit_in_this_clause` — klausul menyebut "voor haar en alle haare nakomelingen" |
| `community_selection_role` | `NOT ESTABLISHED` |
| `customary_selection_basis` | `NOT ESTABLISHED` |
| symbolic_legitimation (turunan Modul D) | **`NOT STATED`** — tak ada rujukan adat/simbolik dalam teks |

### 1698 — CD4 DXCVII

**Koreksi nomor dokumen (CONF-002 verification)**: dokumen sebelumnya salah dikutip sebagai "DXCVIII" — verifikasi langsung terhadap PDF (`docs/cd/CD4.pdf`, idx145-147, halaman cetak 135-137) menunjukkan dokumen yang benar adalah **DXCVII** (597). "DXCVIII" (598) adalah dokumen LAIN yang dimulai di halaman berikutnya (Makassar–Zuid-Celebes, 20 Agustus 1698, topik sama sekali berbeda). Kesalahan ini diwarisi dari `linimasa_events.csv` dan V1 draft sebelumnya.

| Field | Nilai |
|---|---|
| `term_as_written` | "de wettelycke regenten van Padangh" |
| `named_local_office` | **panglimas, pounglous — named local offices, disebut LANGSUNG dalam kalimat yang sama** |
| `VOC_collective_designation` | "regenten" |
| `designation_scope` | `kolektif` (mencakup 2 lokasi: Padang + Sillida) |
| `classification_relation` | **`explicit_collective_VOC_classification`** (wajib) |
| `formal_title_equivalence` | **`NOT ESTABLISHED`** (wajib) |
| `customary_legitimacy` | **`NOT STATED`** (wajib) — kata "wettelycke" **tidak ditafsirkan** sebagai "sah secara adat"; dibaca murni sbg penilaian keabsahan VOC dalam konteks fiskal (bandaars resmi tempat lada ditimbang) |
| `underlying_local_office` | panglima, pounglou (sama dgn `named_local_office` — di sini keduanya identik krn jabatan lokal disebut eksplisit) |
| `representative_scope` | `named_signatories_only` |
| `mandate_evidence` | **`NOT STATED`** — hak "salimoet" disebut dinikmati turun-temurun, tapi tak ada pernyataan mandat komunitas atas pelepasannya |
| `hereditary_scope` | `document_wide_only` — "byna oneyndig getal van jaren" menunjukkan durasi historis hak, bukan proyeksi ke depan yang eksplisit dalam klausul pelepasan itu sendiri |

**Resolusi CONF-001 (Schema Freeze Review)** — record 1698 di atas digabung dua lokasi (Padang + Sillida) dalam satu tindakan kontraktual. Dipecah menjadi dua sub-record beririsan pada `source_document` yang sama, dihubungkan lewat `joint_action_id` bersama, TANPA menyamakan struktur internal kedua polity:

| Field | 1698a — Padang | 1698b — Sillida |
|---|---|---|
| `joint_action_id` | PADANG_1698_JOINT_SALIMOET | PADANG_1698_JOINT_SALIMOET (sama) |
| `classification_target` | panglimas + pounglous Padang | 8 regenten Sillida |
| `named_local_office` | panglimas, pounglous | "Panglima" (tunggal) + "8 mindere regenten" — **disebut langsung dalam deklarasi orang-pertama**, lihat CONF-002 verification |
| `VOC_collective_designation` | "regenten" — **muncul HANYA di narasi orang-ketiga (laporan landraad Beerningh), TIDAK di deklarasi orang-pertama Padang sendiri** (deklarasi Padang memakai "pounglous", bukan "regenten") | "regenten" — **muncul LANGSUNG di deklarasi orang-pertama**: "...benevens den Panglima en 8 mindere regenten van Sillida" |
| `classification_relation` | `explicit_collective_VOC_classification`, sumber = narasi administratif orang-ketiga | `explicit_collective_VOC_classification`, sumber = deklarasi orang-pertama sendiri |
| `underlying_local_office` | panglima, pounglou (identik dgn named_local_office) | "mindere regenten" — TIDAK diasumsikan identik dgn struktur Padang |
| `source_characterization` | `primary_administrative_narrative` (laporan landraad gesaghebber Beerningh, BUKAN editorial Heeres/Stapel — lihat CONF-002 verification) | `primary_treaty_text_verified` (deklarasi orang-pertama langsung) |
| `interpretive_confidence` (utk classification_relation) | **`moderate`** — teks primer terverifikasi, tapi lingkup gramatikal "regenten" (apakah mencakup panglima atau terdaftar terpisah) ambigu dalam kalimat "de panglima's ende de verdere gesamentlycke regenten" | **`high`** — muncul langsung dalam deklarasi orang-pertama, target jelas (8 regenten + 1 panglima, dibedakan eksplisit "benevens") |

Ini mencegah lompatan struktural "8 regenten Sillida = setara panglima+pounglou Padang" hanya karena berbagi satu klausul traktat — dan sekarang juga menunjukkan **1698a dan 1698b punya lapisan sumber (source layer) yang BERBEDA**, bukan hanya lokasi berbeda: 1698a bersumber dari narasi administratif orang-ketiga, 1698b dari deklarasi orang-pertama langsung.

### 1705 — CD4 DCXXXII

**Koreksi status terminologi (Schema Freeze Review)**: status sebelumnya (`NOT APPLICABLE` tunggal untuk `term_as_written`) mencampur dua hal berbeda — "istilah dicari tapi tidak ditemukan" (proposisi terujikan) dengan "relasi klasifikasi tidak relevan" (field structurally kosong). Dipisah:

| Field | Nilai |
|---|---|
| `term_as_written` | **panglima** |
| `regent_term_present` | **`false`** — istilah "Regent" dicari secara eksplisit dalam dokumen ini dan **tidak ditemukan**; ini proposisi yang dapat diuji dengan hasil negatif, bukan ketiadaan informasi (`NOT STATED`) atau ketidakrelevanan field (`NOT APPLICABLE`) |
| `VOC_collective_designation` | **`NOT STATED`** — dokumen tidak memuat istilah kolektif Belanda sejenis "regenten" sama sekali |
| `classification_relation` | **`NOT APPLICABLE`** — field ini menguji RELASI antara istilah VOC kolektif dan jabatan lokal; karena hanya SATU terminologi tersedia di dokumen ini (panglima), tidak ada relasi klasifikasi untuk diuji |
| `formal_title_equivalence` | **`NOT APPLICABLE`** — alasan sama: tidak ada dua istilah untuk dibandingkan kesetaraannya |
| `named_local_office` | **Mara Laout = panglima** — `primary_treaty_text_verified`, confidence `high` (CONF-002 verification) |
| `source_characterization` | **`primary_treaty_text_verified`** untuk badan traktat (idx249-250); paragraf pembuka idx248 dikonfirmasi **`editorial_heading_only`** (narasi latar 1704 oleh Heeres, terpisah dari badan traktat) — CONF-002 verification |
| `verkoren_status` | `primary_treaty_text_verified`, confidence `high` (status Mara Laout sbg "verkoren panglima" langsung di teks) |
| `verkoren_mechanism` | **`ambiguous_source_layer`**, confidence `moderate` — teks konfirmasi keterlibatan GG ("gunstige dispositie") tapi TIDAK menspesifikasi mekanisme lengkap (nominasi lokal vs pilihan VOC langsung) |
| `VOC_involvement_in_appointment` | `primary_treaty_text_verified` utk keberadaannya (disposisi baik GG + permohonan konfirmasi eksplisit), confidence `moderate` — batas seleksi-vs-konfirmasi tetap ambigu |
| `VOC_succession_control` | **Didokumentasikan lewat dua rule berbeda**, keduanya `primary_treaty_text_verified` confidence `high`: `succession_after_death` (VOC hak persetujuan) dan `replacement_for_improper_performance` (VOC hak memilih+mengangkat) |
| `community_selection_role` | **`NOT ESTABLISHED`** |
| `customary_selection_basis` | `NOT ESTABLISHED` |
| `representative_scope` | `named_signatories_only` (Mara Laout + 11 pounglou, disebut nama/jumlah eksplisit) |
| `hereditary_scope` | `explicit_in_this_clause` — HANYA pada Rule 2 (kinerja buruk); Rule 1 (kematian) tidak mengulanginya secara terpisah (`document_wide_only` untuk Rule 1) |

### Konteks Suksesi 1705 (Contextual Episode — TIDAK Mengubah Rule Suksesi)

> **Status: contextual_episode, non-normative.** Blok ini TIDAK mengubah,
> menambah syarat, atau menggantikan `succession_after_death` /
> `replacement_for_improper_performance` (dua rule di atas, sudah
> `primary_treaty_text_verified` confidence `high`, FROZEN). Blok ini
> menambahkan LATAR BELAKANG peristiwa yg mendahului penandatanganan CD4
> DCXXXII, terverifikasi lewat turn verifikasi identitas terpisah
> (`different_persons_supported`, confidence `high`).

Sebelum Mara Laout menandatangani CD4 DCXXXII (13 Agustus 1705), jabatan
panglima radja Padang mengalami DUA transisi berurutan pada tahun yg sama:

| Field | Nilai |
|---|---|
| `contextual_episode_id` | PADANG_1705_SUCCESSION_CONTEXT |
| `predecessor_removed` | Raja Alam — digulingkan pertengahan 1705 stlh laporan VOC menilai kepemimpinannya "lemah/tidak memadai"; sumber: buku *Padang Abad XVII-XVIII* (Ikbal 2024, idx60-65), bersumber GM 30 Nov 1704/1705 |
| `interim_candidate` | Maharadja Indra — diusulkan Aliansi Pauh utk dikembalikan dari pembuangan Batavia; **diangkat "door dese Tafel" (dewan VOC) sbg panglima radja 1705** (GM 06/p0713.xml, 1711, kutipan literal), TAPI **dibunuh di Batavia SEBELUM sempat menjabat** |
| `actual_appointee` | Mara Laout — adik Maharadja Indra (buku Ikbal, footnote 142, TIDAK diverifikasi langsung dari kutipan GM primer yg dibaca); diangkat atas rekomendasi Wan Abdul Bagus (diplomat Melayu VOC); menandatangani CD4 DCXXXII 13 Agustus 1705 sbg "verkoren panglima"; gelar BARU "Regen"/Tuanku Regen — Regent Padang pertama tercatat (buku, tak diverifikasi literal dari GM/CD sesi ini) |
| `actor_identity_status` | **`different_persons_supported`**, confidence `high` — verifikasi terdedikasi turn terpisah; Maharadja Indra dan Mara Laout adalah **DUA actor_id terpisah, TIDAK di-merge**: `actor_maharadja_indra`, `actor_mara_laout_1705` |
| `evidence_status` | `primary_source_verified` untuk keberadaan & urutan peristiwa (GM 06/p0415.xml 30 Nov 1706; GM 06/p0713.xml 15 Jan 1711); `secondary_source_derived_from_primary` untuk detail relasi kekerabatan & gelar "Regen" (buku Ikbal, footnote 140-143, bersumber GM/CD tapi belum diverifikasi literal langsung sesi ini) |
| `implication_for_succession_rules` | **TIDAK ADA** — kedua rule suksesi (`succession_after_death`, `replacement_for_improper_performance`) dirumuskan dari KLAUSUL TRAKTAT CD4 DCXXXII itu sendiri, bukan dari narasi latar suksesi ini; blok ini murni kontekstual, tidak mengubah status `frozen_candidate` kedua rule |
| `candidate_mechanism_for_future_work` | `contested_local_selection` dan/atau `VOC_intervention_in_office_contestation` — **BELUM divalidasi** sbg `historical_mechanism_candidate` formal (di luar cakupan freeze review V1); dicatat sbg petunjuk kerja lanjutan, bukan klaim final |

---

## Konflik Schema yang Sudah Diselesaikan

1. **Tumpang tindih `representative_scope` vs `hereditary_scope`** (dicatat terbuka di pilot sebelumnya) — **diselesaikan** dengan pemisahan definisi eksplisit di atas: `representative_scope` = cakupan pihak terikat PADA SATU TINDAKAN; `hereditary_scope` = proyeksi lintas-generasi YANG DINYATAKAN DALAM KLAUSUL ITU SENDIRI. Kedua field sekarang dapat diisi independen tanpa duplikasi makna.
2. **Ketiadaan nilai `cannot_determine` terpisah dari `NOT STATED`** (dicatat terbuka di pilot sebelumnya) — **diselesaikan** lewat sistem empat status (`NOT STATED` / `NOT AVAILABLE` / `CANNOT DETERMINE` / `NOT APPLICABLE`) yang kini berlaku seragam di seluruh modul, memungkinkan `underlying_local_office` 1671 diisi `CANNOT DETERMINE` (bukan `NOT STATED`) karena ketiadaan pembanding, bukan sekadar ketiadaan penyebutan.
3. **Risiko "wettelycke" ditafsirkan sbg legitimasi adat** — **diselesaikan** dgn field `customary_legitimacy` terpisah dari `formal_title_equivalence`, keduanya wajib `NOT STATED`/`NOT ESTABLISHED` untuk 1698 kecuali ada bukti tekstual baru.

## Schema Freeze Review

### B. Tiga Konflik Schema Baru (sebagaimana tercatat sebelum diselesaikan)

**CONF-001**
```
conflict_id: CONF-001
affected_module: B (Office and Classification), C (Representation and Succession)
affected_fields: classification_target, representative_scope, designation_scope,
  underlying_local_office
conflicting_definitions: "designation_scope: kolektif" diterapkan pada SATU record
  yang mencakup DUA lokasi (Padang + Sillida) dengan kemungkinan struktur jabatan
  internal berbeda (panglimas+pounglous Padang vs "8 regenten Sillida") — desain
  satu-record berisiko menyamakan struktur kedua polity hanya krn berbagi satu
  klausul traktat
affected_pilot_records: 1698 (CD4 DXCVII, dikoreksi dari kutipan lama "DXCVIII")
epistemic_risk: risiko konflasi "8 regenten Sillida" dibaca setara struktural dgn
  "panglima+pounglou" Padang tanpa bukti tekstual langsung
proposed_resolution: pecah jadi dua sub-record (1698a Padang, 1698b Sillida)
  berbagi joint_action_id, TANPA menyamakan underlying_local_office
information_loss_risk: RENDAH jika dipecah (lebih granular); SEDANG jika tetap
  digabung (kehilangan pembedaan struktur internal dua polity)
backward_compatibility: 1671 (single-location, tidak terdampak); 1705
  (single-location, tidak terdampak); hanya 1698 yang perlu restrukturisasi
researcher_decision_required: true
```
**Keputusan**: **DISELESAIKAN** — dipecah menjadi 1698a/1698b (lihat tabel di atas pada bagian Pemetaan Tiga Dokumen §1698).

**CONF-002 — status SEBELUM verifikasi ini**
```
conflict_id: CONF-002
affected_module: A (Source and Documentary Claim)
affected_fields: source_characterization
conflicting_definitions: field didefinisikan dgn allowed values
  (primary_treaty_text/primary_administrative_letter/editorial_narrative/NOT STATED)
  tapi diterapkan ke ketiga pemetaan (1671/1698/1705) TANPA pemeriksaan ulang
  khusus yang membedakan porsi teks-traktat murni dari kemungkinan narasi
  editorial Heeres/Stapel yang mengelilinginya di halaman PDF yang sama
affected_pilot_records: 1671, 1698, 1705 (ketiganya) — verifikasi turn ini
  DIBATASI hanya pada 1698a/1698b sesuai instruksi
epistemic_risk: jika narasi editorial ikut terhitung sbg primary_treaty_text,
  documentary_claim bisa mewarisi framing editor tanpa ditandai
status_sebelumnya: DISELESAIKAN SEBAGIAN, interpretive_confidence: moderate
  utk ketiga record, verifikasi khusus belum dijadwalkan
```

**CONF-002 — Verifikasi 1698a & 1698b (turn ini)**

Sumber: `docs/cd/CD4.pdf`, idx145-147 (halaman cetak 135-137), dibaca langsung.

| # | Item | 1698a — Padang | 1698b — Sillida |
|---|---|---|---|
| 1 | document number | **DXCVII** (koreksi dari "DXCVIII" — lihat catatan di §1698 di atas) | DXCVII (sama) |
| 2 | printed page | 135-136 | 136 |
| 3 | PDF page index | idx145-146 | idx146 |
| 4 | kalimat sumber lengkap | *"...tenzy de panglima's ende de verdere gesamentlycke regenten van Padangh en Sillida... haar genegen toonde om... eens voor al afstant te doen van de geregtigheyt ofte soo genoemde salimoet"* (narasi laporan landraad Beerningh, orang-ketiga) | *"Soo hebben wy, ondergeschreven, Panglima-radja en 12 pounglous van Padang, benevens den Panglima en 8 mindere regenten van Sillida, de bovengenoemde voorslagen... beslooten en vastgesteld"* (deklarasi orang-pertama) |
| 5 | istilah yang diklasifikasikan | "regenten" (bagian frasa "de verdere gesamentlycke regenten van Padangh en Sillida") | "8 mindere regenten van Sillida" |
| 6 | aktor/jabatan dirujuk | panglima's + regenten (Padang DAN Sillida digabung dalam satu frasa narasi) | Panglima (tunggal) + 8 mindere regenten, Sillida SAJA, dipisah eksplisit dari Padang lewat kata "benevens" (di samping/bersama) |
| 7 | dinyatakan langsung oleh teks? | Ya, tapi dalam narasi ORANG-KETIGA (laporan proposal Beerningh), bukan deklarasi diri Padang sendiri (yg memakai "pounglous", bukan "regenten") | **Ya, langsung dalam deklarasi orang-pertama** — "wy... benevens... 8 mindere regenten van Sillida" |
| 8 | heading / isi traktat / editor / interpretasi? | **Isi dokumen primer, narasi administratif** (laporan landraad, dikutip dari "Overgecomen brieven 1699") — **BUKAN editorial Heeres/Stapel** (catatan editor di idx145 hanya *"Het volgende stuk behoeft geen inleiding"* — editor eksplisit TIDAK menambah narasi) | **Isi traktat/deklarasi primer langsung** — bagian "Soo hebben wy..." adalah teks komitmen orang-pertama itu sendiri |
| 9 | hubungan 1698a-1698b | Berbagi satu `joint_action_id` (satu tindakan kontraktual), TAPI berasal dari **lapisan sumber berbeda** dalam dokumen yang sama: 1698a dari narasi laporan (baris atas), 1698b dari deklarasi diri (baris bawah) | (sama, dua arah) |
| 10 | pencampuran Padang-Sillida? | **Ya, DI NARASI (poin 4)** — frasa "regenten van Padangh en Sillida" menggabungkan keduanya; **TAPI deklarasi diri (poin 4, 1698b) memisahkan tegas** lewat "benevens" — dokumen sendiri membedakan dua kelompok penanda tangan meski satu tindakan | (sama) |

**Status source layer**:
- 1698a: **`primary_treaty_text_verified`** untuk keberadaan dokumen (bukan editorial) — TAPI `ambiguous_source_layer` untuk **cakupan** istilah "regenten" itu sendiri, karena gramatika "de panglima's ende de verdere gesamentlycke regenten" secara linguistik ambigu apakah panglima termasuk kategori "regenten" atau didaftar terpisah darinya.
- 1698b: **`primary_treaty_text_verified`** tanpa syarat — istilah, aktor, dan cakupannya (8, dibedakan dari panglima via "benevens") semua eksplisit dalam satu kalimat deklarasi diri.

**Keputusan confidence**:
- **1698a**: **`moderate`** dipertahankan (TIDAK naik ke `high`) — teks primer terverifikasi (bukan editorial), tapi cakupan/target istilah "regenten" ambigu secara gramatikal dalam sumber itu sendiri, sesuai definisi "moderate: primary text available but target/scope ambiguous".
- **1698b**: **`high`** — dinaikkan dari `moderate` — karakterisasi muncul langsung dalam teks primer (deklarasi orang-pertama) DAN target referensinya jelas (8 regenten + 1 panglima, dibedakan eksplisit dari delegasi Padang).

**Keputusan CONF-002 akhir**: **DISELESAIKAN untuk 1698a dan 1698b** (cakupan verifikasi turn ini). Confidence **dipecah per-record**, bukan lagi satu nilai blanket untuk seluruh dokumen 1698 — 1698a tetap `moderate`, 1698b naik ke `high`. Verifikasi untuk 1671 dan 1705 **TIDAK dilakukan turn ini** (di luar cakupan yang diminta) — residual CONF-002 untuk kedua record itu **tetap terbuka**.

**CONF-003**
```
conflict_id: CONF-003
affected_module: C (Representation and Succession)
affected_fields: succession_rule
conflicting_definitions: NOT APPLICABLE dipakai utk "field tak relevan pada
  record ini" — tapi utk 1671/1698, KETIADAAN klausul suksesi bisa dibaca juga
  sbg CANNOT DETERMINE (apakah ketiadaan itu sendiri bermakna) — schema
  sebelumnya tidak membedakan "genre dokumen ini memang tak pernah memuat
  klausul suksesi" (NOT APPLICABLE struktural) dari "kita tak tahu kenapa tak
  ada klausul suksesi" (CANNOT DETERMINE)
affected_pilot_records: 1671, 1698
epistemic_risk: default diam-diam ke NOT APPLICABLE bisa menutupi pertanyaan
  riset yg sah: apakah dokumen jenis fiskal/delegasi secara sistematis berbeda
  dari dokumen jenis konfirmasi-jabatan dlm hal ada/tidaknya klausul suksesi?
proposed_resolution: pertahankan nilai field NOT APPLICABLE (secara teknis
  benar — 1671/1698 adalah tindakan fiskal/delegasi, bukan tindakan konfirmasi-
  jabatan, sehingga klausul suksesi memang di luar topik genre ini), TAPI
  tambahkan catatan level-field baru di uncertainty_notes: "ketiadaan berbasis
  genre, bukan ketiadaan bukti — korelasi genre-klausul-suksesi belum diuji
  lintas korpus lebih luas"
information_loss_risk: RENDAH
backward_compatibility: penuh, aditif saja
researcher_decision_required: true — apakah korelasi genre-suksesi layak diuji
  lintas korpus lebih besar (kerja masa depan, di luar pilot ini)
```
**Keputusan (final, terverifikasi per-record)**:

| Record | `succession_rule` | Alasan |
|---|---|---|
| 1671 | **`NOT APPLICABLE`** | Claim fiskal (transfer tol 10%); tidak membahas pengangkatan/pergantian jabatan; "nakomelingen" memperluas KEWAJIBAN FISKAL ke keturunan, bukan suksesi jabatan |
| 1698a | **`NOT APPLICABLE`** | Claim fiskal (pelepasan salimoet, negosiasi harga lada); tidak menyentuh pengangkatan/pergantian jabatan |
| 1698b | **`NOT APPLICABLE`** | Sama — bagian dari tindakan fiskal bersama 1698a, tidak menyentuh suksesi |

`uncertainty_notes` dipertahankan: *"ketiadaan berbasis genre dokumen (instrumen fiskal), bukan ketiadaan bukti — korelasi genre-klausul-suksesi belum diuji lintas korpus lebih luas."*

**CONF-003 SELESAI untuk ketiga record (1671, 1698a, 1698b).**

---

### C. Uji Sistem Status

Audit pemakaian enam kategori status + boolean di seluruh dokumen V1 (termasuk koreksi di atas):

| Status | Definisi | Perkiraan pemakaian di V1 | Catatan |
|---|---|---|---|
| `NOT STATED` | Sumber diperiksa, informasi tidak dinyatakan | ~9× (mis. 1671 `named_local_office`, `mandate_evidence`; 1698 `mandate_evidence`, `customary_legitimacy`; 1705 `VOC_collective_designation`) | Konsisten dipakai hanya saat sumber SUDAH dibaca |
| `NOT AVAILABLE` | Sumber yang diperlukan belum tersedia | **0×** | Temuan jujur — tidak ada satu pun field di tiga dokumen ini yg butuh sumber TAMBAHAN yang belum ada; seluruh field bisa dijawab (dgn status apa pun) dari 3 dokumen yg sudah dibaca |
| `CANNOT DETERMINE` | Bukti tersedia tapi ambigu/tak cukup | ~3× (1671 `underlying_local_office`; 1698b `named_local_office`, `underlying_local_office` — baru ditambah lewat resolusi CONF-001) | Dipakai HANYA saat ada bukti parsial yg tak cukup, bukan ketiadaan total |
| `NOT APPLICABLE` | Field tak relevan pada record ini | ~5× (mis. `succession_rule` 1671/1698; 1705 `classification_relation`, `formal_title_equivalence` — baru dikoreksi) | Dipakai HANYA saat pertanyaan fieldnya sendiri tak bermakna utk record ybs |
| `NOT ESTABLISHED` | Klaim analitis tak dapat dibuktikan dari bukti tersedia | ~6× (`formal_title_equivalence` 1671/1698; `community_selection_role`, `customary_selection_basis` di ketiganya) | Dipakai utk KLAIM (bukan field kosong) yg diuji dan gagal terbukti |
| `false` (boolean) | Proposisi dapat diuji, hasilnya negatif | 2× (`researcher_review_required` sbg tipe field; **`regent_term_present: false`**, baru ditambah) | **Dibedakan tegas** dari lima status di atas — `false` HANYA dipakai utk proposisi ya/tidak yg benar-benar diuji langsung terhadap teks, bukan utk ketiadaan informasi |

**Hasil**: **Tidak ditemukan pencampuran** boolean/status-ketersediaan/putusan-epistemik dalam pemakaian saat ini. Perbaikan `regent_term_present: false` (1705) adalah contoh pertama boolean sejati di luar `researcher_review_required` — ditambahkan tepat karena field lama (`term_as_written: NOT APPLICABLE`) SEBELUMNYA mencampur "dicari-tak-ketemu" (seharusnya boolean) dengan "field tak relevan" (`NOT APPLICABLE` sejati). Ini persis kelas kesalahan yang diperbaiki di bagian A.

---

### D. Validation Matrix

Diperiksa terhadap **ketiga** dokumen (1671, 1698 — dua sub-record 1698a/1698b, dan 1705) untuk field kunci lintas empat modul:

| Field | 1671 | 1698a (Padang) | 1698b (Sillida) | 1705 |
|---|---|---|---|---|
| `term_as_written` | "algemeene regenten tot Padang" — documentary, high, sumber ada | "de wettelycke regenten van Padangh" — documentary, high, sumber ada | (sama, frasa gabungan) — documentary, high, sumber ada | "panglima" (bukan "regent") — documentary, high, sumber ada |
| `named_local_office` | `NOT STATED` — documentary, high, sumber ada | panglimas, pounglous — documentary, high, sumber ada | `CANNOT DETERMINE` — documentary, moderate, sumber ada tapi tak eksplisit | Mara Laout=panglima — documentary, high, sumber ada |
| `classification_relation` | `explicit_collective_VOC_classification` — interpretive, high, sumber ada | sama — interpretive, high, sumber ada | sama — interpretive, high, sumber ada | `NOT APPLICABLE` — meta, high, sumber ada (tak relevan) |
| `formal_title_equivalence` | `NOT ESTABLISHED` — interpretive, high, sumber ada | `NOT ESTABLISHED` — interpretive, high, sumber ada | `NOT ESTABLISHED` — interpretive, high, sumber ada | `NOT APPLICABLE` — meta, high, sumber ada (tak relevan) |
| `underlying_local_office` | `CANNOT DETERMINE` — interpretive, moderate, sumber ada tapi tak cukup | panglima, pounglou — documentary, high, sumber ada | `CANNOT DETERMINE` — interpretive, moderate | `NOT APPLICABLE` (hanya 1 istilah) — meta, high |
| `mandate_evidence` | `NOT STATED` — documentary, high, sumber ada | `NOT STATED` — documentary, high, sumber ada | `NOT STATED` — documentary, high, sumber ada | `NOT ESTABLISHED` (community_selection_role) — interpretive, high |
| `community_selection_role` | `NOT ESTABLISHED` — interpretive, high, sumber ada | `NOT ESTABLISHED` — interpretive, high, sumber ada | `NOT ESTABLISHED` — interpretive, high, sumber ada | `NOT ESTABLISHED` — interpretive, high, sumber ada |
| `customary_selection_basis`/`customary_legitimacy` | `NOT ESTABLISHED` — interpretive, high, sumber ada | `NOT STATED` — documentary, high, sumber ada | `NOT STATED` — documentary, high, sumber ada | `NOT ESTABLISHED` — interpretive, high, sumber ada |
| `succession_rule` | `NOT APPLICABLE` (genre fiskal) — meta, moderate (lihat CONF-003) | `NOT APPLICABLE` (genre fiskal) — meta, moderate | `NOT APPLICABLE` — meta, moderate | 2 rule eksplisit (kematian, kinerja buruk) — documentary, high |
| `source_characterization` | `primary_treaty_text_verified` — meta, **moderate** (CONF-002 terverifikasi) | `primary_administrative_narrative` — meta, **moderate** (CONF-002 terverifikasi) | `primary_treaty_text_verified` — meta, **high** (CONF-002 terverifikasi) | `primary_treaty_text_verified` (badan traktat) / `editorial_heading_only` (paragraf pembuka) — meta, **high** utk klaim inti, **moderate** utk mekanisme pemilihan (CONF-002 terverifikasi) |
| `researcher_review_required` | `true` (semua record) | `true` | `true` | `true` |

**Delapan Guard — Hasil Uji**:

| # | Lompatan yang diuji | Dicegah? | Mekanisme |
|---|---|---|---|
| 1 | `regenten` → gelar resmi individual | **Lulus** | `formal_title_equivalence` terpisah, `NOT ESTABLISHED`/`NOT APPLICABLE` di seluruh record |
| 2 | `wettelycke` → legitimasi adat | **Lulus** | `customary_legitimacy` field terpisah dari `formal_title_equivalence`, `NOT STATED` konsisten |
| 3 | tindakan kolektif → mandat seluruh masyarakat | **Lulus** | `representative_scope: named_signatories_only` konsisten di semua record; `mandate_evidence: NOT STATED` |
| 4 | `verkoren` → bukti pemilihan komunitas | **Lulus** | `community_selection_role: NOT ESTABLISHED` dipertahankan terpisah dari `selection_actor`/`contractants_selection_role` |
| 5 | persetujuan VOC → hak memilih langsung | **Lulus** | `VOC_approval_required` (Rule 1) terpisah tegas dari `VOC_direct_selection_right` (Rule 2) sejak koreksi turn sebelumnya |
| 6 | penggantian VOC → prosedur pemberhentian eksplisit | **Lulus** | `explicit_removal_term: false` + `formal_removal_procedure: NOT STATED` dipertahankan terpisah dari `VOC_appointment_right` |
| 7 | kontraktan → sinonim masyarakat adat | **Lulus** | `contractants_selection_role`/`selection_actor` tak pernah disamakan dgn `community_selection_role` di field manapun |
| 8 | rule kontraktan → hukum umum seluruh Padang | **Lulus** | `subject_group`/`representative_scope` dibatasi nilai `named_signatories_only`/`panglima_and_pounglous` — tak ada nilai "seluruh Padang" yg diizinkan schema |

**Hasil**: **Kedelapan guard lulus** pada validasi terhadap ketiga dokumen + dua sub-record baru.

---

### E. Freeze Decision

```
methodological_baseline_status: frozen_candidate
deployment_status: NOT_READY_FOR_DEPLOYMENT
```

**Keputusan keseluruhan**: **`READY_TO_FREEZE_AS_METHODOLOGICAL_BASELINE`**

Dasar: ketiga konflik baru (CONF-001, CONF-002, CONF-003) sudah diberi resolusi konkret dan diterapkan pada dokumen ini; sistem status (6 kategori + boolean) diaudit dan tidak ditemukan pencampuran; validation matrix terhadap 3 dokumen (4 record dgn pemecahan 1698a/1698b) konsisten; kedelapan guard lulus. **Status "frozen_candidate" TIDAK berarti siap deployment** — dipertahankan terpisah dan eksplisit sbg `NOT_READY_FOR_DEPLOYMENT`, sesuai batas yg diwajibkan.

---

## Konflik yang Masih Terbuka (pasca-freeze-review)

1. **CONF-002: SELESAI SEPENUHNYA** — verifikasi 1671, 1698a, 1698b, dan 1705 seluruhnya tuntas (lihat §Schema Freeze Review + turn-turn verifikasi berikutnya). Tidak ada residual CONF-002 tersisa. Catatan halus yang bertahan (bukan residual terbuka, hanya nuansa permanen): (a) 1671 & 1705 sama-sama punya paragraf editorial Heeres MENDAHULUI badan traktat, tapi badan traktatnya sendiri terverifikasi primer independen; (b) mekanisme persis pemilihan awal Mara Laout (1705) tetap `ambiguous_source_layer`/`moderate` — ini bukan kegagalan verifikasi, melainkan batas genuine dari apa yang dinyatakan sumber.
2. **CONF-003 residual**: korelasi genre-dokumen dengan ada/tidaknya klausul suksesi belum diuji lintas korpus lebih luas dari 3 dokumen pilot ini.
3. **1698b (Sillida) `underlying_local_office`**: tetap `CANNOT DETERMINE` — memerlukan dokumen tambahan spesifik-Sillida (di luar cakupan freeze review ini) untuk diselesaikan.

---

## Hasil Validation Checks (Pilot Sebelumnya — Dipertahankan)

| Cek wajib | Hasil |
|---|---|
| 1671: regenten = collective Dutch designation | **Terpenuhi** |
| 1671: `named_local_office` = NOT STATED | **Terpenuhi** |
| 1671: `underlying_local_office` = CANNOT DETERMINE | **Terpenuhi** |
| 1671: `representative_mandate`/`mandate_evidence` = NOT STATED | **Terpenuhi** |
| 1671: `symbolic_legitimation` = NOT STATED | **Terpenuhi** |
| 1698: panglima + pounglou = named local offices | **Terpenuhi** |
| 1698: regenten = explicit collective VOC classification | **Terpenuhi** |
| 1698: formal title equivalence = NOT ESTABLISHED | **Terpenuhi** |
| 1698: customary legitimacy = NOT STATED | **Terpenuhi** |
| 1705: Mara Laout = panglima | **Terpenuhi** |
| 1705: term Regent = NOT STATED (dikoreksi di sini menjadi NOT APPLICABLE, krn istilah memang tak muncul sama sekali — bukan "diperiksa tapi tak dinyatakan" dalam arti sempit, melainkan absen total dari korpus dokumen ini) | **Terpenuhi, dengan catatan penghalusan status** |
| 1705: VOC succession control = documented through two distinct rules | **Terpenuhi** |
| 1705: community mandate = NOT ESTABLISHED | **Terpenuhi** |

**Seluruh 13 kondisi validasi yang diwajibkan terpenuhi.** Satu catatan penghalusan dicantumkan (status 1705 utk istilah "Regent" lebih tepat `NOT APPLICABLE` daripada `NOT STATED` menurut definisi empat-status baru, karena kata itu memang tak pernah muncul di dokumen — bukan kasus "diperiksa tapi tak dinyatakan").

---

## Deployment Readiness

```
methodological_baseline_status: frozen_candidate
deployment_status: NOT_READY_FOR_DEPLOYMENT
```

**Status akhir (pasca Schema Freeze Review): `NOT_READY_FOR_DEPLOYMENT`** — dipertahankan meski schema sudah `frozen_candidate` sbg baseline metodologis. Alasan deployment tetap ditolak: (a) tiga item residual di §Konflik yang Masih Terbuka (pasca-freeze-review) belum tuntas; (b) schema baru diuji pada 1 lokasi (Padang, 3 dokumen + 1 pemecahan sub-record) — belum ada uji-silang ke lokasi lain (Sillida, Priaman, Barus) yang sudah dianalisis terpisah dalam sesi ini dgn kerangka process-tracing berbeda, bukan schema anotasi ini; (c) tidak ada implementasi, migrasi, atau perubahan ontologi produksi yang dijalankan atau diusulkan untuk dieksekusi.
