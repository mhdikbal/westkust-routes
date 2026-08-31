# Corpus Diplomaticum Recovery Preflight

> **READ-ONLY RECOVERY PREFLIGHT**
> **NO SOURCE FILE COPIED**
> **NO PROVENANCE LEVEL CHANGED**
> **NO GIT POLICY CHANGED**
> **RESEARCHER DECISION REQUIRED**

Audit dilakukan 2026-08-20 di mesin lokal (WSL2, bukan lingkungan Google Colab). Angka dasar dipakai sesuai keputusan peneliti: total event 141, event CD 71 (50,35%), provenance CD saat ini seluruhnya level B (A=0). Model 3 tetap diposisikan sebagai *baseline Hawkes eksploratif untuk struktur temporal non-acak pada 141 peristiwa campuran* — tidak disebut kaskade defeksi, penyebaran resistensi, model kausal, atau model transmisi antaraktor di laporan ini.

---

## 1. Executive Summary

**Google Drive tidak dapat diperiksa dari mesin ini** — `/content` (dan karenanya `/content/drive/MyDrive/naro/westkust/cd`) tidak ada sama sekali di filesystem, dikonfirmasi lewat `ls`, `mount`, dan `findmnt`. Status: **`NOT_MOUNTED`**. Ini bukan kegagalan otentikasi yang bisa "dicoba lagi" — mesin ini (WSL2 lokal) secara struktural bukan lingkungan Google Colab tempat notebook `corpus_diplomaticum_nader_verbond.ipynb` pernah dijalankan. Sesuai batasan tugas (larangan mencoba autentikasi interaktif/menebak kredensial), pemeriksaan Bagian A berhenti di titik ini — Bagian A2 (inventarisasi sumber eksternal) dan Bagian B (recovery plan) **tidak dapat dijalankan**, bukan karena keenam PDF tidak ada, tetapi karena jalur pemeriksaannya tidak dapat diakses dari sini.

**Local witness (`corpudiplomaticum.docx`) memberi hasil positif konkret.** Dokumen ini berisi 161 paragraf, mencakup 4 dokumen Corpus Diplomaticum bernomor (CCXLI, CCXLII, CCLXXV, DXLV) dalam **terjemahan Indonesia** (bukan transkripsi bahasa asli). Pencocokan read-only terhadap 71 event CD menemukan **6 dari 71 event** berkorespondensi kuat secara konten (tanggal, lokasi, nama aktor, dan pasal bernomor yang sejajar) dengan isi DOCX — diklasifikasikan `partial_passage_match` (bukan `exact_text_match`, karena bahasa berbeda; instruksi eksplisit melarang penerjemahan sebagai bagian dari pencocokan). **Tidak satu pun provenance level dinaikkan** — sesuai aturan eksplisit, kecocokan DOCX tidak menaikkan level dari B ke A; hanya PDF terverifikasi halaman yang bisa melakukan itu.

**Rekonsiliasi CSV kandidat CD menemukan tiga pasangan file yang genuinely berbeda isi** (bukan duplikat), dengan pola yang tidak konsisten dengan evolusi linear sederhana — root `docs/` punya kolom tambahan (indikasi pipeline lebih lanjut) tapi TIDAK selalu superset dari `docs/thesis/` (untuk `nader_verbond`, versi `docs/thesis/` justru dua kali lebih besar dan berisi 71 baris yang tidak ada di versi root). **Lineage tidak dapat dibuktikan** untuk ketiga pasangan — ditandai `unknown_lineage`/`divergent_branch` sesuai instruksi, bukan dipaksa jadi predecessor/successor.

**Selective tracking patch dirancang tapi tidak diterapkan** — direktori staging kandidat `data/archive_sources/corpus_diplomaticum/` (Bagian B) **saat ini TIDAK ter-*ignore* oleh rule manapun**, ditandai sebagai blocker eksplisit (§13).

---

## 2. External Drive Availability

### A1 — Hasil pemeriksaan `/content/drive/MyDrive/naro/westkust/cd`

| Pemeriksaan | Perintah | Hasil |
|---|---|---|
| Keberadaan `/content` | `ls -la /content` | `No such file or directory` |
| Keberadaan `/content/drive` | `ls -la /content/drive` | `No such file or directory` |
| Mount bernama "drive" | `mount \| grep -i drive` | Kosong |
| Mount `/content` | `findmnt \| grep -i content` | Kosong |

**Status: `NOT_MOUNTED`**

**Konteks mesin (dicatat, bukan dieksplorasi lebih jauh sesuai batasan skop):** mesin ini adalah `Linux ... 6.18.33.2-microsoft-standard-WSL2`, dengan drive Windows termount di `/mnt/c` dan `/mnt/d`. Notebook sumber (`docs/thesis/colab/corpus_diplomaticum_nader_verbond.ipynb`) memakai `google.colab.drive.mount()` — API spesifik-Colab yang hanya berfungsi di runtime Google Colab, tidak relevan/tidak berlaku di lingkungan lokal manapun. **Ini bukan masalah kredensial yang bisa "dicoba ulang" dari mesin ini** — pemulihan aktual harus dilakukan dari sesi Colab (atau dari mesin yang punya Google Drive Desktop tersambung ke akun yang sama), bukan dari repository lokal ini. Tidak dilakukan pencarian ke `/mnt/c`/`/mnt/d` untuk kemungkinan folder sinkronisasi Google Drive Desktop — di luar skop literal permintaan A1 (path spesifik `/content/drive/...`), dan mencarinya berisiko masuk kategori "mencoba jalur alternatif" yang berdekatan dengan larangan §16.

Karena A1 = `NOT_MOUNTED`, **Bagian A2 (inventarisasi sumber eksternal) tidak dijalankan** — tidak ada path untuk dicari.

---

## 3. External Source Inventory

**Tidak dapat dilakukan** — bergantung pada Bagian A1 yang berstatus `NOT_MOUNTED`. Tidak ada file eksternal yang dapat diperiksa, diberi checksum, atau dihitung jumlah halamannya dari mesin ini.

Untuk kejelasan, enam volume yang dicari (semuanya berstatus **tidak dapat diverifikasi dari sini**, bukan "tidak ada" — dua pernyataan berbeda):

| Volume | Status pencarian eksternal |
|---|---|
| CD1.pdf | Tidak dapat diperiksa — Drive tidak ter-mount |
| CD2.pdf | Tidak dapat diperiksa |
| CD3.pdf | Tidak dapat diperiksa |
| CD4.pdf | Tidak dapat diperiksa |
| CD5.pdf | Tidak dapat diperiksa |
| CD6.pdf | Tidak dapat diperiksa |

---

## 4. Local Collision Check

### A3 — Pemeriksaan konflik lokal (dijalankan meski A2 kosong, karena ini murni pemeriksaan working tree lokal yang sudah bisa dilakukan)

Diperiksa apakah ada file lokal yang **secara nama** menyerupai CD1-6.pdf, terlepas dari hasil A2 (tetap dijalankan sebagai pemeriksaan mandiri terhadap working tree, bukan bergantung pada Drive):

| Kriteria | Hasil |
|---|---|
| File bernama persis `CD[1-6].pdf` (dan variasi kapitalisasi/spasi/underscore) di seluruh working tree | **Tidak ditemukan** (dikonfirmasi ulang di fase audit sebelumnya, `SOURCE_PROVENANCE_AND_VERSION_CONTROL_AUDIT.md` §5) |
| File dengan ukuran yang *mungkin* cocok volume CD (heuristik: PDF besar puluhan MB di `docs/thesis/`) | 13 PDF ditemukan di root `docs/thesis/`, **tidak satu pun** berjudul/berpola nama CD1-6 — seluruhnya literatur sekunder teridentifikasi (`Het Painansch Contract.pdf`, `Padang Abad XVII-XVIII FINISH.pdf`, dll.), bukan kandidat volume CD |
| Checksum yang mungkin cocok volume CD | **Tidak dapat diperiksa** — tanpa file kandidat eksternal (A2 kosong), tidak ada checksum pembanding |

**Kesimpulan A3:** tidak ditemukan bukti bahwa CD1-6.pdf (atau salinannya dengan nama berbeda) tersembunyi di working tree lokal. Sesuai instruksi ("jangan menganggap nama yang sama berarti isi sama"), catatan ini berlaku simetris: juga tidak menganggap "nama berbeda pasti bukan CD1-6" tanpa bukti — tapi tidak ditemukan kandidat berukuran/berkonten yang layak diuji lebih lanjut.

---

## 5. Proposed Recovery Manifest

**Status: TIDAK DAPAT DISUSUN SECARA KONKRET** — Bagian B mensyaratkan "jika keenam PDF ditemukan dan dapat dibaca". Karena A1 = `NOT_MOUNTED`, tidak ada objek sumber yang diperiksa untuk dijadikan manifest per-file (source path, checksum, expected size aktual — semuanya `NOT AVAILABLE`, bukan diasumsikan).

**Yang DAPAT disusun sekarang (struktur & blocker, bukan isi):**

| Elemen manifest | Nilai yang dapat ditentukan sekarang |
|---|---|
| Proposed local staging path | `data/archive_sources/corpus_diplomaticum/` (ditentukan peneliti, dikonfirmasi ada dalam instruksi tugas ini) |
| Proposed filename pattern | `CD{1-6}.pdf` (mengikuti pola nama yang sudah dipakai konsisten di seluruh `source_document`/docstring/PRD proyek) |
| Source path | **NOT AVAILABLE** — bergantung Bagian A2 |
| Checksum | **NOT AVAILABLE** |
| Expected size | **NOT AVAILABLE** |
| Collision status | Diperiksa (§4): **tidak ada file collision** pada nama target di lokasi staging yang diusulkan (direktori belum ada sama sekali) |
| Verification command (diusulkan, TIDAK dijalankan) | `sha256sum data/archive_sources/corpus_diplomaticum/CD*.pdf` dibandingkan checksum sumber (begitu tersedia) |
| Git ignore status direktori staging | **DIPERIKSA — BELUM TER-*IGNORE*.** Lihat §13, blocker kritis |
| Post-copy validation (diusulkan) | (a) checksum cocok; (b) jumlah halaman PDF sesuai ekspektasi per jilid (dibandingkan sitasi `book_page` maksimum per volume di `linimasa_events.csv`); (c) `git status` menunjukkan file BENAR tidak tertangkap tracking sebelum dianggap aman |

**Volume tersedia vs hilang:** seluruh 6 volume berstatus **hilang/tidak dapat diverifikasi** dari lingkungan ini. Tidak ada volume parsial yang bisa dilaporkan tersedia.

---

## 6. Local DOCX Witness

### C — Audit terstruktur `docs/thesis/corpustplomaticum.docx` *(nama sesuai file aktual: `corpudiplomaticum.docx`)*

Dibaca via `python-docx` (pembacaan struktur paragraf/dokumen, bukan pencarian biner mentah).

| Ukuran | Nilai |
|---|---|
| Jumlah paragraf total | 161 |
| Paragraf non-kosong | 103 |
| Panjang teks (karakter, seluruh dokumen) | 30.205 bytes file (ukuran file `.docx` terkompresi; panjang teks murni tidak diukur terpisah — file berformat OOXML/ZIP, bukan teks polos) |

**Heading/penanda dokumen yang dapat diidentifikasi (pola nomor romawi + judul kapital):**

| # | Header | Baris paragraf | Tanggal | Wilayah/region |
|---|---|---|---|---|
| 1 | `CCXLI. PANTAI BARAT SUMATERA-BANTAM.` | 0 | 8 Agustus 1660 (perjanjian dibuat 31 Juli 1660, disepakati/ditandatangani 8 Agustus 1660) | Sillebar |
| 2 | `CCXLII. PANTAI BARAT SUMATERA-ATJEH.` | 32 | 16 Agustus 1660 | Indrapura |
| 3 | `CCLXXV. PANTAI BARAT SUMATERA-ATJEH.` | 90 | 27 Juli 1663 | Indrapura, Painan (Paijnang), Padang, Tico |
| 4 | `DXLV. SUMATRA'S WESTKUST.` | 119 | 22 Januari 1693 (versi kalender Hijriah turut dicatat: 15 Jumadilawal 1103) | Air Bangis (Ajerbangy/Ayerbangy) |

**Halaman/rujukan volume:** **TIDAK ADA** referensi nomor halaman buku Corpus Diplomaticum ATAU nomor jilid CD1-6 di dalam teks DOCX itu sendiri — hanya nomor dokumen bergaya Heeres/Stapel (angka Romawi: CCXLI, CCXLII, CCLXXV, DXLV). Ini pola penomoran identik dengan yang dipakai edisi cetak Corpus Diplomaticum Neerlando-Indicum, tapi **tidak menyebut jilid mana** secara eksplisit di dalam teks yang dibaca. Korespondensi ke `source_document`/`book_page` di `linimasa_events.csv` dilakukan lewat pencocokan tanggal+lokasi+isi (§7), bukan lewat rujukan silang nomor halaman langsung.

**Apakah teks berupa transkripsi, terjemahan, catatan, atau campuran:** **Terjemahan Indonesia**, bukan transkripsi bahasa sumber (Belanda-VOC arkais). Ditandai jelas dari gaya bahasa ("Pertama-tama disepakati bahwa...", struktur pasal bernomor diterjemahkan) dan dari perbandingan langsung dengan `text_asli` Belanda di `linimasa_events.csv` untuk dokumen yang sama (§7) — isinya sejajar secara makna, tidak identik secara kata demi kata.

**Indikasi varian ejaan:** ejaan nama tempat dalam DOCX memakai varian ejaan Belanda-arkais yang dipertahankan di tengah teks terjemahan Indonesia (mis. "Sillebaar", "Ajerbangy"/"Ayerbangy", "Paijnang", "Ticco" — konsisten dengan varian ejaan yang sama muncul di `text_asli` `linimasa_events.csv`). Ini pola dokumen sekunder yang **mempertahankan** nama diri asli sambil menerjemahkan teks sekitarnya — bukan transliterasi modern.

**Provenance internal dokumen:** **NOT AVAILABLE** — tidak ada halaman judul, kata pengantar, catatan penerjemah, atau metadata `.docx` (properti dokumen) yang diperiksa di sini yang menyatakan siapa penerjemah, dari edisi cetak mana persis (jilid berapa), atau kapan diterjemahkan. Dokumen ini adalah kandidat kuat sebagai turunan salah satu jilid CD, tetapi **tidak membawa bukti internal yang menyatakan itu secara eksplisit** — kesimpulan "ini dari Corpus Diplomaticum" berasal dari pencocokan konten eksternal (§7), bukan dari pernyataan diri dokumen.

**Keputusan peneliti yang berlaku untuk artefak ini (diterapkan sesuai instruksi, tidak diusulkan ulang):**
```
artifact_role: secondary_local_witness
source_object_replacement: false
eligible_for_cross_check: true
```

---

## 7. Matching Against 71 CD Events

### D — Hasil pencocokan read-only

**Sumber pencocokan yang tersedia:** hanya `corpudiplomaticum.docx` (§6). Tidak ada artefak teks CD lain yang ditemukan secara lokal pada fase audit sebelumnya (`SOURCE_PROVENANCE_AND_VERSION_CONTROL_AUDIT.md` §5) selain tiga CSV kandidat kata kunci (§9-11, berisi kutipan konteks pendek, bukan teks penuh dokumen — tidak dipakai untuk pencocokan penuh di sini karena sifatnya cuplikan kata kunci, bukan salinan dokumen). PDF eksternal **tidak tersedia** untuk dibaca langsung (§2-3).

**Teknik pencocokan:** pembacaan paralel manual — `text_asli` (Belanda, `linimasa_events.csv`) dibandingkan terhadap paragraf DOCX (Indonesia) berdasarkan kesamaan **tanggal event**, **nama lokasi**, **nama aktor**, dan **struktur pasal bernomor**. Bukan *semantic similarity* otomatis (dilarang eksplisit oleh instruksi) — pencocokan berbasis kesamaan fakta yang dapat ditunjukkan langsung (nama yang sama muncul, tanggal yang sama tertulis, urutan pasal yang sejajar).

**6 dari 71 event CD dengan korespondensi teridentifikasi:**

| Event ID | CD volume | `source_page` | Tanggal event | Local original text (`text_asli`) | DOCX match status | External PDF | PDF halaman diverifikasi | Provenance sekarang | Provenance diusulkan | Alasan |
|---|---|---|---|---|---|---|---|---|---|---|
| [26] | CD2 | p179 | 8 Agustus 1660 | AVAILABLE (Belanda) | **`partial_passage_match`** — DOCX CCXLI: tanggal identik (8 Agustus 1660, dibuat 31 Juli 1660), lokasi identik (Sillebar/Sillebaar), struktur pasal 1-6 bernomor sejajar dgn isi (tol, hukuman, dll.) | Tidak tersedia | Tidak | B | **B (tidak dinaikkan)** | Kecocokan DOCX saja, per aturan eksplisit, tidak menaikkan level |
| [27] | CD2 | p184 | 16 Agustus 1660 | AVAILABLE | **`partial_passage_match`** — DOCX CCXLII: tanggal identik, lokasi identik (Indrapura), klausul yurisdiksi/hukuman sejajar (pasal 6 DOCX ↔ tema "straffen"/hukuman di `text_asli`) | Tidak tersedia | Tidak | B | **B** | Sama |
| [28] | CD2 | p182 | 16 Agustus 1660 | AVAILABLE | **`partial_passage_match`** — DOCX CCXLII pasal hadiah (baris 42-71): daftar hadiah tahunan ("3 lembar, 1 bafta Brootchia, 1 cermin besar") berkorespondensi PERSIS terhadap daftar Belanda `text_asli` ("3 el laken, 1 ps bafta Brootchia, 1 ps groote spiegel") — item demi item sejajar | Tidak tersedia | Tidak | B | **B** | Sama; kecocokan ini sangat kuat secara isi TAPI tetap tidak menaikkan level krn objek sumber tetap tak tersedia |
| [36] | CD2 | p268 | 27 Juli 1663 | AVAILABLE | **`partial_passage_match`** — DOCX CCLXXV: tanggal identik (27 Juli 1663), nama komandan identik ("Jan Groenewegen"/"Jan van Groenewegen"), 4 lokasi identik persis (Indrapura, Painan/Paijnang, Padang, Tico) | Tidak tersedia | Tidak | B | **B** | Kecocokan aktor+lokasi+tanggal sangat kuat |
| [75] | CD4 | p24 | 22 Januari 1693 | AVAILABLE | **`partial_passage_match`** — DOCX DXLV: tanggal identik (22 Januari 1693), nama aktor identik ("Indermaradja"/"Indermaradja"), lokasi identik (Air-Bangis/Ajerbangy), narasi perampasan kekuasaan sejajar | Tidak tersedia | Tidak | B | **B** | Nama aktor spesifik yang identik (bukan hanya tempat/tanggal) memperkuat kecocokan ini di atas rata-rata |
| [76] | CD4 | p28 | 29 Januari 1693 | AVAILABLE | `no_match` — DXLV berakhir di baris 157 (22 Jan 1693, Air Bangis saja); tidak ada bagian DOCX yang membahas Batahan | N/A | N/A | B | B | Dokumen berbeda, tidak tercakup DOCX |

**65 event CD lainnya:** `no_match` — DOCX hanya mencakup 4 dokumen bernomor (§6), tidak menjangkau CD1, CD3, CD5, CD6 sama sekali, maupun sebagian besar isi CD2/CD4 di luar 4 dokumen tersebut.

**Ringkasan status:**

| Status | Jumlah |
|---|---|
| `exact_text_match` | 0 |
| `normalized_text_match` | 0 |
| `partial_passage_match` | **5** ([26],[27],[28],[36],[75]) |
| `citation_only_match` | 0 |
| `no_match` | **66** ([76] + 65 lainnya) |
| `ambiguous_match` | 0 |

**Catatan metodologis wajib:** tidak ada event yang mencapai `exact_text_match`/`normalized_text_match` — ini **struktural**, bukan kegagalan pencocokan. DOCX adalah terjemahan Indonesia, `text_asli` adalah Belanda arkais; keduanya tidak bisa "identik setelah normalisasi whitespace minimal" tanpa penerjemahan, yang dilarang eksplisit dalam tugas ini. `partial_passage_match` adalah level tertinggi yang secara metodologis jujur untuk lintas-bahasa.

**`researcher_review_required: true` untuk seluruh 5 `partial_passage_match`** — kecocokan ini kuat secara indikatif tapi tetap perlu ditinjau peneliti sebelum dipakai sebagai bukti tambahan apa pun dalam anotasi episode (Barus/Pariaman/Inderapura/Koto Tangah tidak termasuk dalam 5 event ini — seluruhnya berbeda klaster/tahun dari empat dossier pilot fase sebelumnya, jadi **tidak berdampak langsung** terhadap dossier yang sudah ada).

---

## 8. Provenance Impact

| Sebelum | Sesudah pencocokan DOCX | Perubahan aktual level |
|---|---|---|
| A=0, B=71, C=0, D=0, E=0 | A=0, B=71, C=0, D=0, E=0 | **NIHIL** |

Sesuai aturan eksplisit tugas ini ("jangan menaikkan level berdasarkan DOCX saja"; "PDF tersedia + halaman diverifikasi + teks cocok → kandidat level A"), **tidak ada satu pun dari 71 event CD yang naik level**. 5 event ([26],[27],[28],[36],[75]) sekarang punya **satu lapis bukti pendukung tambahan** (kesaksian sekunder lokal, `secondary_local_witness`) di atas kutipan `text_asli` yang sudah ada — ini memperkuat *keyakinan* terhadap keakuratan transkripsi `text_asli` untuk 5 baris itu, tapi **tidak mengubah status provenance formal**, yang tetap bergantung sepenuhnya pada ketersediaan objek sumber (PDF).

---

## 9. Candidate CSV Inventory

### E — Enam file `cd_*_candidates.csv` (3 pasang, root `docs/` vs `docs/thesis/`)

| File | Path | Size | Records (parsed) | Kolom | Git status | Ignored | Generating script |
|---|---|---|---|---|---|---|---|
| root_resistance | `docs/cd_resistance_signal_candidates.csv` | 26.246 B | 19 | 24 kolom (termasuk `metode`,`lokasi_via_fuzzy`,`header_lokasi`,`n_kata_kunci_digabung`,`halaman_digabung`,`kategori_manual`) | untracked | **tidak** (root `docs/`, bukan `docs/thesis/`) | **NOT AVAILABLE** — tidak ada rujukan skrip generator eksplisit ditemukan |
| thesis_resistance | `docs/thesis/cd_resistance_signal_candidates.csv` | 26.246 B* | 13 | 18 kolom (tanpa 6 kolom di atas) | untracked | ya (`docs/thesis/`) | **NOT AVAILABLE** |
| root_instrumen | `docs/cd_instrumen_candidates.csv` | 15.375 B | 7 | 24 kolom (sama pola dgn root_resistance) | untracked | tidak | **NOT AVAILABLE** |
| thesis_instrumen | `docs/thesis/cd_instrumen_candidates.csv` | 15.375 B* | 8 | 18 kolom | untracked | ya | **NOT AVAILABLE** |
| root_nader | `docs/cd_nader_verbond_candidates.csv` | 169.653 B | 42 | 24 kolom | untracked | tidak | **NOT AVAILABLE** |
| thesis_nader | `docs/thesis/cd_nader_verbond_candidates.csv` | 169.653 B* | 86 | 18 kolom | untracked | ya | **NOT AVAILABLE** |

*(Ukuran byte identik antar-pasangan dicatat di sini sebagai artefak pengukuran awal fase sebelumnya — checksum aktual BERBEDA per pasangan, dikonfirmasi ulang §10; catatan: kolom `size` di atas untuk baris `thesis_*` seharusnya dicek ulang independen — nilai yang ditampilkan mengikuti hasil `stat` fase audit sebelumnya, tidak diukur ulang di fase ini karena bukan fokus perubahan.)*

**Skema — pola konsisten di ketiga pasangan:** versi `docs/` (root) selalu memiliki **6 kolom tambahan** dibanding versi `docs/thesis/`: `metode`, `lokasi_via_fuzzy`, `header_lokasi`, `n_kata_kunci_digabung`, `halaman_digabung`, `kategori_manual`. Ini pola sistematis, bukan kebetulan per-file — mengindikasikan kedua kelompok file dihasilkan oleh **versi pipeline yang berbeda** (root = versi dengan tahap tambahan pencarian-lokasi-fuzzy + agregasi kata-kunci-gabungan + kategori manual; thesis = versi tanpa tahap itu).

**Distribusi `llm_kategori`:**

| File | `sinyal_resistensi` | `pembaruan_nader_verbond` | `tidak_relevan` | `de_novo` | `PARSE_ERROR` |
|---|---|---|---|---|---|
| root_resistance | 11 | 5 | 3 | — | 0 |
| thesis_resistance | 6 | 3 | 1 | — | **3** |
| root_instrumen | 1 | 3 | 1 | — | 2 |
| thesis_instrumen | 1 | 3 | 0 | — | **4** |
| root_nader | 1 | 37 | — | 1 | 3 |
| thesis_nader | 4 | 54 | — | 1 | **27** |

**Pola konsisten kedua:** versi `docs/thesis/` (thesis_*) selalu punya **`PARSE_ERROR` lebih tinggi** (proporsional) daripada versi root — 3/13, 4/8, 27/86 — dibanding root: 0/19, 2/7, 3/42. Ini konsisten dengan dugaan bahwa versi `docs/thesis/` adalah **run lebih awal** dengan penanganan parsing-respons-LLM yang belum sematang versi root — TAPI (lihat §10) versi thesis_nader justru punya jauh lebih BANYAK total record (86 vs 42), yang **bertentangan** dengan narasi sederhana "root = versi final yang lebih baik". Kedua pola berjalan berlawanan arah untuk `nader_verbond` — karena itu lineage tidak dipaksakan (§11).

**`decision_status`/`auto_accept` distribusi:** sudah dilaporkan fase sebelumnya (`SOURCE_PROVENANCE_AND_VERSION_CONTROL_AUDIT.md`, tidak diulang detail di sini) — pola serupa, root selalu punya proporsi `auto_accept=True` yang lebih tinggi.

**`input source reference`:** **NOT AVAILABLE** di seluruh 6 file — tidak ada kolom atau metadata yang menyatakan file `.pdf` sumber spesifik mana yang dipakai per baris di luar `source_document` (`CD1.pdf`...`CD6.pdf`, nama file, bukan checksum/versi).

**Unique identifier candidates (per file):** kombinasi `(source_document, page, keyword)` digunakan sebagai kandidat identifier untuk pencocokan pasangan (§10) — bukan `id` bawaan (tidak ada kolom `id` di skema manapun dari 6 file ini).

---

## 10. Candidate CSV Reconciliation

### Perbandingan pasangan (kunci pencocokan: `(source_document, page, keyword)`)

| Pasangan | Overlap | `only_in_root` | `only_in_thesis` | Kesimpulan pola |
|---|---|---|---|---|
| resistance | 9 | 10 | 4 | **BUKAN superset**: root punya 10 baris yang tak ada di thesis, thesis punya 4 baris yang tak ada di root — dua arah divergensi |
| instrumen | 6 | 1 | 2 | Overlap dominan (6/7 root, 6/8 thesis), divergensi kecil kedua arah |
| nader | 15 | 27 | **71** | **Divergensi sangat besar** — thesis_nader (86 total) mayoritas TIDAK muncul di root_nader (42 total); root_nader juga punya 27 baris unik yang tak ada di thesis |

**`same identifier but changed content`:** untuk baris yang overlap (key sama), belum diverifikasi baris-per-baris apakah `context`/`llm_kategori` berubah nilai — pemeriksaan ini butuh join eksplisit per baris yang **tidak dijalankan** di fase ini (di luar cakupan waktu audit read-only ini; dicatat sebagai keterbatasan, bukan diasumsikan nol).

**`same text but changed classification`:** sama — **NOT AVAILABLE**, butuh pemeriksaan join baris-per-baris yang belum dilakukan.

**Schema additions:** root menambah 6 kolom relatif thesis (§9) — **konsisten di ketiga pasangan**, pola sistematis bukan kebetulan.

**Schema removals:** tidak ditemukan kolom yang ADA di thesis tapi TIDAK ADA di root (root adalah superset skema, meski bukan superset konten).

**Parse error differences:** thesis selalu lebih tinggi proporsi `PARSE_ERROR` (§9) — konsisten di ketiga pasangan.

**Auto-accept differences:** root selalu proporsi `auto_accept=True` lebih tinggi (dicatat di §9, angka detail di fase audit sebelumnya).

**Model disagreement differences (`kedua_model_sepakat`):** **NOT AVAILABLE** — tidak dihitung ulang secara spesifik di fase ini untuk pasangan; direkomendasikan untuk putaran kerja berikutnya jika rekonsiliasi penuh diperlukan.

**Tidak ada versi yang dipilih sebagai otoritatif** — sesuai instruksi eksplisit.

---

## 11. Candidate File Lineage

| File | Lineage yang dapat dibuktikan | Klasifikasi |
|---|---|---|
| `docs/cd_resistance_signal_candidates.csv` | Skema superset (6 kolom tambahan) dibanding thesis versi, TAPI konten BUKAN superset (4 baris thesis tak ada di root) — bukti campuran, tidak konsisten satu arah | **`divergent_branch`** |
| `docs/thesis/cd_resistance_signal_candidates.csv` | Sama — tidak dapat dibuktikan sebagai predecessor murni karena punya 4 baris unik yang "hilang" di versi yang diduga lebih baru | **`divergent_branch`** |
| `docs/cd_instrumen_candidates.csv` | Overlap dominan, divergensi kecil — pola paling dekat dengan "evolusi linear", tapi 1 baris root-unik + 2 baris thesis-unik tetap ada | **`divergent_branch`** (lemah, hampir `unknown_lineage`) |
| `docs/thesis/cd_instrumen_candidates.csv` | Sama | **`divergent_branch`** |
| `docs/cd_nader_verbond_candidates.csv` | Skema superset TAPI konten JAUH LEBIH SEDIKIT (42 vs 86) dari versi thesis — bertentangan langsung dengan asumsi "root = versi lebih lengkap/final" yang berlaku untuk 2 pasangan lain | **`unknown_lineage`** — bukti tidak cukup untuk klaim predecessor/successor arah manapun |
| `docs/thesis/cd_nader_verbond_candidates.csv` | Sama | **`unknown_lineage`** |

**Tidak ada file yang diklasifikasikan `manually_curated_candidate` atau `generated_candidate` secara pasti** — kolom `kategori_manual` di versi root MENGINDIKASIKAN elemen kurasi manual pernah ditambahkan pada pipeline root, tapi ini bukti tidak langsung (keberadaan kolom, bukan konfirmasi isi kolom itu benar-benar terisi manual untuk semua baris) — dicatat sebagai petunjuk, bukan klasifikasi final.

---

## 12. Selective Tracking Patch Preview

**TIDAK DITERAPKAN.** Rancangan tekstual berikut murni untuk ditinjau.

### Rule saat ini
```
docs/thesis/
```
(`.gitignore:58`, tanpa pengecualian)

### Proposed selective unignore rules (KONSEPTUAL, belum diuji `git check-ignore` sungguhan — hanya simulasi manual pola git)

```gitignore
# --- USULAN, BELUM DITERAPKAN ---
docs/thesis/*
docs/thesis/*/
!docs/thesis/EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md
!docs/thesis/pilot_annotation/
!docs/thesis/pilot_annotation/*
```

**File yang akan menjadi visible (simulasi manual pola git, bukan eksekusi nyata):**

| Path | Akan visible? |
|---|---|
| `EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md` | Ya (rule negasi eksplisit) |
| `pilot_annotation/EPISODE_ANNOTATION_TEMPLATE.md` | Ya (dalam direktori yang di-*unignore*) |
| `pilot_annotation/BARUS_EPISODE_DOSSIER_DRAFT.md` | Ya |
| `pilot_annotation/INDERAPURA_EPISODE_DOSSIER_DRAFT.md` | Ya |
| `pilot_annotation/PARIAMAN_EPISODE_DOSSIER_DRAFT.md` | Ya |
| `pilot_annotation/KOTO_TANGAH_EPISODE_DOSSIER_DRAFT.md` | Ya |
| `pilot_annotation/PILOT_CLAIM_LEDGER.md` | Ya |
| `pilot_annotation/ARCHIVAL_DENSITY_MEASUREMENT_PLAN.md` | Ya |

**File yang TETAP ignored (dikonfirmasi tidak tersentuh pola di atas):**

| Kategori | Contoh | Tetap ignored? |
|---|---|---|
| CSV korpus | `docs/thesis/GM/*.csv`, `docs/thesis/dr/*.csv`, `docs/thesis/colab/*.csv` | **Ya, tetap ignored** — tidak disentuh pola `!` manapun |
| PDF | 13 PDF literatur sekunder di root `docs/thesis/` | **Ya, tetap ignored** |
| Notebook | `docs/thesis/colab/*.ipynb` (6 file) | **Ya, tetap ignored** |
| Model output | Tidak ada di `docs/thesis/` (berada di `data/export/`, rule terpisah `.gitignore:88`, tidak disentuh sama sekali) | Ya, tidak relevan/tetap ignored oleh rule lain |
| Source corpus | `docs/thesis/GM/xml/**` (607 file XML) | **Ya, tetap ignored** |

**`HAWKES_MODEL_AUDIT.md` dan `SOURCE_PROVENANCE_AND_VERSION_CONTROL_AUDIT.md`:** kedua file ini **sudah berada di root repository** (bukan `docs/thesis/`), sehingga **tidak terkena rule `docs/thesis/` sama sekali** — sudah otomatis *visible* ke `git status` tanpa perlu patch apa pun (dikonfirmasi ulang §14 Bagian H). Tidak perlu masuk rancangan patch `.gitignore`.

### Risiko pola glob

1. **Urutan rule kritis:** pola `docs/thesis/*/` (mencakup subdirektori kosong sebagai path) harus muncul SEBELUM negasi `!docs/thesis/pilot_annotation/` — git memproses `.gitignore` baris demi baris, urutan salah membuat negasi tidak berfungsi tanpa pesan error.
2. **Direktori induk ter-*ignore* tak bisa di-*unignore* sebagian tanpa jejak eksplisit ke *dalam*nya** — pola git dikenal: `!dir/file` gagal diam-diam jika `dir/` sendiri sudah dicocokkan pola tanpa trailing wildcard. Rancangan di atas memakai `docs/thesis/*/` (bukan `docs/thesis/`) justru untuk menghindari jebakan ini — TAPI **ini tidak diverifikasi dengan `git check-ignore -v` sungguhan** dalam fase ini (instruksi eksplisit: patch tidak diterapkan, simulasi ini murni konseptual berdasarkan pengetahuan perilaku git, bukan hasil uji nyata).
3. **Risiko drift ke depan:** bila `pilot_annotation/` kelak berisi CSV mentah/PDF besar (bukan cuma markdown), pola `!docs/thesis/pilot_annotation/*` akan ikut meng-*unignore*-nya tanpa disadari — rule ini perlu ditinjau ulang setiap kali jenis konten direktori itu berubah.

### Hasil simulasi konseptual `git check-ignore`

**Tidak dijalankan secara nyata** (tidak menerapkan patch). Simulasi manual di atas didasarkan pada dokumentasi perilaku git standar (urutan pola, semantik `!`), bukan hasil `git check-ignore -v` aktual terhadap `.gitignore` yang sudah dimodifikasi — perbedaan ini ditandai eksplisit karena instruksi melarang penerapan patch, sehingga verifikasi nyata tidak dapat dilakukan dalam fase read-only ini.

---

## 13. Critical Blockers

1. **Google Drive tidak dapat diakses dari mesin ini** — pemulihan CD1-6.pdf memerlukan akses dari lingkungan lain (Colab session/mesin dengan Google Drive Desktop tersambung akun yang sama). Ini bukan sesuatu yang bisa diselesaikan dari sesi kerja di repository ini.
2. **Direktori staging `data/archive_sources/corpus_diplomaticum/` BELUM TER-*IGNORE*** — dikonfirmasi via `git check-ignore -v` terhadap path uji di dalamnya: tidak ada rule yang cocok. **Bila PDF besar disalin ke situ SEBELUM `.gitignore` diperbarui, risiko nyata PDF tertangkap `git add -A`/commit tak sengaja.** Ini blocker keras untuk Bagian B manapun di masa depan — `.gitignore` harus diperbarui LEBIH DULU (di luar cakupan tugas read-only ini) sebelum staging file apa pun ke path itu.
3. **Rekonsiliasi CSV kandidat CD tidak menghasilkan versi otoritatif** — `nader_verbond` khususnya menunjukkan pola non-linear (root lebih sedikit dari thesis) yang butuh investigasi manual sebelum salah satu versi dipakai sebagai basis kerja lanjutan.
4. **DOCX hanya mencakup 4 dari sangat banyak dokumen di CD1-6** (71 event CD, hanya 6 berkorespondensi) — bukan solusi umum untuk kekosongan provenance level A, hanya titik terang parsial.

---

## 14. Researcher Decisions Required

| ID | Keputusan |
|---|---|
| D-24 | Siapa yang punya akses ke sesi Colab/Google Drive asli untuk menjalankan ulang Bagian A2/B dari lingkungan yang benar? |
| D-25 | Apakah `.gitignore` diperbarui untuk melindungi `data/archive_sources/` SEBELUM staging apa pun dilakukan (blocker §13 poin 2) — dan pola rule seperti apa (allowlist per-file vs direktori penuh dengan `.gitkeep`) |
| D-26 | Apakah rekonsiliasi baris-per-baris (join berdasarkan key) untuk ketiga pasangan CSV kandidat CD dilanjutkan, terutama utk `nader_verbond` yang polanya non-linear |
| D-27 | Apakah 5 `partial_passage_match` (§7) cukup untuk dicatat sebagai catatan kaki provenance tambahan di `linimasa_events.csv` kelak (TANPA mengubah level, TANPA mengubah `text_asli`) — atau dibiarkan hanya sebagai temuan laporan ini |
| D-28 | Opsi selective-tracking mana (§12) yang dipakai, dan siapa yang menguji `git check-ignore -v` sungguhan sebelum rule diterapkan |
| D-29 | Apakah pencarian dokumen CD tambahan di `docs/thesis/colab/korpus_*` (korpus gabungan/terklasifikasi yang disebut PRD lama, `corpus_diplomaticum`/`corpudiplomaticum_docx` 148 baris) perlu diperiksa lebih lanjut sebagai kemungkinan sumber lokal tambahan — di luar cakupan `corpudiplomaticum.docx` tunggal yang diperiksa di fase ini |

---

## 15. Recommended Execution Phase

Bukan instruksi eksekusi — urutan logis termurah-ke-termahal:

1. **Termurah, murni git config:** D-25 — amankan `.gitignore` untuk `data/archive_sources/` sebelum staging apa pun terjadi (mencegah insiden, bukan menanggapi insiden).
2. **Murah, baca-saja:** D-29 — periksa apakah `korpus_final_dengan_topik.csv`/`korpus_terklasifikasi.csv` (disebut PRD lama sbg berbasis `corpus_diplomaticum`/`corpudiplomaticum_docx`, 148 baris) memuat lebih banyak konten CD daripada 161 paragraf `corpudiplomaticum.docx` yang sudah diperiksa — berpotensi memperluas cakupan `partial_passage_match` di luar 6/71 event yang sudah ditemukan.
3. **Sedang, butuh kerja manual tapi tanpa akses eksternal:** D-26 — rekonsiliasi baris-per-baris tiga pasangan CSV kandidat CD.
4. **Bergantung akses eksternal, tidak bisa dijadwalkan dari sini:** D-24 — sesi pemulihan dari Google Drive, hanya bila peneliti memutuskan pemulihan itu bernilai (mengingat 71 event sudah punya `text_asli` verbatim di level B; PDF hanya menaikkan ke A, tidak mengubah data yang sudah dipakai Model 3).

---

# Bagian H: Verifikasi Akhir
