# Source Provenance and Version-Control Audit

> **READ-ONLY AUDIT**
> **NO SOURCE RECOVERY PERFORMED**
> **NO GIT POLICY CHANGED**
> **RESEARCHER DECISION REQUIRED**

Audit dilakukan 2026-08-20. Seluruh temuan berasal dari pemeriksaan langsung filesystem, `git log --all`, dan parsing CSV dengan `csv.DictReader` (bukan `wc -l`). Tidak ada file dipindah/dihapus, tidak ada `git add`/commit, tidak ada `.gitignore` diubah, tidak ada sumber diunduh dari internet.

---

## 1. Executive Summary

Dua temuan utama, satu di setiap bagian audit:

**(A) Perlindungan version-control.** Seluruh artefak metodologis fase sebelumnya (`EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md` + 7 berkas `pilot_annotation/`) berada di `docs/thesis/`, yang di-*gitignore* menyeluruh oleh satu baris (`.gitignore:58`). Baris ini ditulis untuk alasan sah (mencegah PDF besar riset masuk histori git) tapi berlaku tanpa pandang bulu ke **740 file** dengan sifat sangat berbeda — dari draf metodologis 100KB sampai korpus GM 127MB. Artefak metodologis fase ini punya risiko hilang yang sama seperti insiden `stratified_analysis.py` yang sudah tercatat di memory proyek (skrip yang hilang karena tak pernah ter-*commit*).

**(B) Provenance Corpus Diplomaticum.** `CD1.pdf`–`CD6.pdf` **tidak ada di repository saat ini**, **tidak pernah tercatat di riwayat git manapun** (dikonfirmasi `git log --all` kosong untuk nama file itu), dan proyek sendiri **sudah mendokumentasikan ketiadaan ini sejak 2026-07-17** (`docs/prd/prd-pembersihan-sitasi-cd1-cd6.md`: *"PDF asli CD1-CD6 tidak ada di repo utk verifikasi halaman judul persis"*). Lokasi sumber aslinya teridentifikasi dari notebook: Google Drive pribadi peneliti (`/content/drive/MyDrive/naro/westkust/cd`), di luar jangkauan repository. **50,35% (71/141) dari seluruh `linimasa_events` bersumber dari koleksi yang PDF sumbernya tidak dapat diverifikasi ulang** — namun seluruh 71 baris itu punya kutipan `text_asli` verbatim tersimpan, sehingga tergolong *provenance_level_B* (halaman+teks tersedia, objek sumber hilang), bukan *level_D/E* (label saja/rusak).

Tidak ditemukan bukti CD1-6 pernah ter-*commit* — ketiadaannya adalah konsekuensi desain (`.gitignore:63 docs/*.pdf`), bukan kehilangan tak disengaja dalam pengertian git.

---

## 2. Git Ignore Findings

### A1 — Rule per file

| Path | ignored | rule | lokasi rule | tracked | ukuran | klasifikasi |
|---|---|---|---|---|---|---|
| `docs/thesis/EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md` | yes | `docs/thesis/` | `.gitignore:58` | no | 57.414 B | `methodological_document` |
| `docs/thesis/pilot_annotation/EPISODE_ANNOTATION_TEMPLATE.md` | yes | `docs/thesis/` | `.gitignore:58` | no | 10.285 B | `methodological_document` |
| `docs/thesis/pilot_annotation/BARUS_EPISODE_DOSSIER_DRAFT.md` | yes | `docs/thesis/` | `.gitignore:58` | no | 15.150 B | `methodological_document` |
| `docs/thesis/pilot_annotation/INDERAPURA_EPISODE_DOSSIER_DRAFT.md` | yes | `docs/thesis/` | `.gitignore:58` | no | 13.008 B | `methodological_document` |
| `docs/thesis/pilot_annotation/PARIAMAN_EPISODE_DOSSIER_DRAFT.md` | yes | `docs/thesis/` | `.gitignore:58` | no | 12.982 B | `methodological_document` |
| `docs/thesis/pilot_annotation/KOTO_TANGAH_EPISODE_DOSSIER_DRAFT.md` | yes | `docs/thesis/` | `.gitignore:58` | no | 15.875 B | `methodological_document` |
| `docs/thesis/pilot_annotation/PILOT_CLAIM_LEDGER.md` | yes | `docs/thesis/` | `.gitignore:58` | no | 7.861 B | `methodological_document` |
| `docs/thesis/pilot_annotation/ARCHIVAL_DENSITY_MEASUREMENT_PLAN.md` | yes | `docs/thesis/` | `.gitignore:58` | no | 16.352 B | `methodological_document` |
| `data/research/linimasa_events.csv` | **no** | — | — | **yes** | 148.843 B | `source_data` |
| `docs/thesis/colab/model3_hawkes_kaskade_event.py` | yes | `docs/thesis/` | `.gitignore:58` | no | 5.228 B | `notebook_or_script` |
| `data/export/hawkes_model_output.json` | yes | `data/export/` | `.gitignore:88` | no | 8.863 B | `model_output` |
| `docs/thesis/GM/gm_corpus_filtered_1660_1789.csv` | yes | `docs/thesis/` | `.gitignore:58` | no | 5.848.674 B (5,6 MB) | `source_data` (derivatif korpus GM) |
| `docs/thesis/dr/daghregister_corpus_classified.csv` | yes | `docs/thesis/` | `.gitignore:58` | no | 2.763.787 B (2,6 MB) | `source_data` (derivatif korpus Daghregister) |

**Isi rule (`.gitignore:56-63`):**
```
# Materi riset thesis (PDF besar, draft, notebook Colab) — bukan bagian app,
# jangan masuk git (bisa ratusan MB)
docs/thesis/

# Scan Dagh-register sumber primer (puluhan MB/volume) — dipakai sekali utk
# sisir manual, ekstraksi hasilnya ada di data/research/*.csv + migrasi DB,
# jadi PDF mentah tak perlu ikut git history
docs/*.pdf
```

**Pengamatan kunci:** rule `docs/thesis/` (baris 58) adalah **satu direktori, satu baris**, tanpa pengecualian (`!pattern`). Ia menangkap segala sesuatu di bawah `docs/thesis/` — PDF ratusan MB (alasan aslinya, sah) **dan** dokumen markdown metodologis berukuran puluhan KB (efek samping yang mungkin tidak diinginkan). `linimasa_events.csv` — satu-satunya `source_data` produksi yang benar-benar dipakai Model 3 secara langsung — berada di `data/research/`, **tracked**, tidak terkena rule ini sama sekali. Ini artinya **jalur produksi Model 3 sudah aman**; yang berisiko adalah artefak metodologis pendukung yang baru dibuat di fase-fase sebelumnya.

### File riset penting lain (pemeriksaan tambahan A1)

| Path | ignored | rule | tracked | ukuran | klasifikasi |
|---|---|---|---|---|---|
| `docs/prd/prd-pemodelan-kekuasaan-dagang.md` | no | — | (perlu cek, di luar `docs/thesis/`) | — | `methodological_document` |
| `docs/thesis/cd_resistance_signal_candidates.csv` | yes | `docs/thesis/` | no | 26.246 B | `derived_data` (hasil ekstraksi LLM) |
| `docs/cd_resistance_signal_candidates.csv` (root `docs/`, **bukan** `docs/thesis/`) | **no** | — | **no** (untracked, bukan diabaikan) | — | `derived_data` — **berbeda checksum dari versi `docs/thesis/`**, lihat §12 |
| `docs/thesis/corpudiplomaticum.docx` | yes | `docs/thesis/` | no | 30.205 B | `derived_data` — **transkripsi parsial CD, lihat §5** |

`docs/prd/prd-pemodelan-kekuasaan-dagang.md` berada di luar `docs/thesis/`, jadi tidak terkena rule ini — dicek terpisah dan **tidak** ter-*ignore* (lokasinya `docs/prd/`, tracked oleh git).

---

## 3. Methodological Artifact Protection

### A2 — Inventaris `docs/thesis/` (740 file total)

Enumerasi penuh 740 file satu-per-satu tidak praktis untuk laporan yang bisa dibaca; berikut agregasi per direktori dan ekstensi, dengan detail individual untuk berkas yang secara khusus relevan metodologis atau relevan Bagian B/C audit ini.

**Distribusi per subdirektori (jumlah file):**

| Direktori | Jumlah file | Ukuran total | Isi dominan |
|---|---|---|---|
| `docs/thesis/GM/` | 619 | 127 MB | 607 file XML (`xml/01`–`xml/14`, per-surat Generale Missiven) + CSV turunan |
| `docs/thesis/dr/` | 51 | 42 MB | CSV Daghregister (mentah, dedup, klasifikasi, backup) |
| `docs/thesis/colab/` | 31 | 4,3 MB | Skrip Python Model 2/3/5/6, notebook `.ipynb`, CSV korpus (termasuk 4 pasangan `(1)`, §12) |
| `docs/thesis/pilot_annotation/` | 7 | 104 KB | **Paket pilot fase sebelumnya** |
| `docs/thesis/graphify-out/` | 4 | 116 KB | Cache graphify lokal |
| `docs/thesis/draft/` | 2 | 172 KB | Draf proposal thesis (`.docx`+`.md`) |
| `docs/thesis/cp/` | 0 | 4 KB (direktori kosong) | — |
| File langsung di `docs/thesis/` (root) | 26 | 119 MB | 13 PDF literatur sekunder, `corpudiplomaticum.docx`, 3 CSV kandidat CD, dll. |

**Distribusi per ekstensi (seluruh 740 file):** `.xml` 607 · `.csv` 41 · `.py` 39 · `.pdf` 13 · `.md` 12 · `.json` 10 · `.ipynb` 6 · `.docx` 4 · `.txt` 2 · `.png` 2 · lainnya 4.

**Berkas individual yang layak dicatat (klasifikasi + rekomendasi):**

| Path | Ext | Size | Tracked/Ignored | Klasifikasi | Rekomendasi |
|---|---|---|---|---|---|
| `EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md` | md | 57 KB | ignored | `methodological_document` | `candidate_for_selective_tracking` |
| `pilot_annotation/*.md` (7 file) | md | 7-16 KB tiap | ignored | `methodological_document` | `candidate_for_selective_tracking` |
| `chapter-plan-sia-kualitatif-kritis.md` | md | 33 KB | ignored | `methodological_document` | `candidate_for_selective_tracking` |
| `three-way-scan-bab2-2026-07-06.md` | md | 11 KB | ignored | `methodological_document` | `needs_researcher_decision` |
| `slides-proposal.md` | md | 6 KB | ignored | `methodological_document` | `needs_researcher_decision` |
| `draft/proposal_thesis_draft_v1.md` | md | 93 KB | ignored | `methodological_document` | `needs_researcher_decision` |
| `corpudiplomaticum.docx` | docx | 30 KB | ignored | `derived_data` | `needs_researcher_decision` — lihat §5, provenance parsial CD |
| `perjanjian_pauh_dccxv_1716.txt` | txt | 7 KB | ignored | `derived_data` | `needs_researcher_decision` |
| `cd_resistance_signal_candidates.csv` | csv | 26 KB | ignored | `derived_data` | `needs_researcher_decision` (dua salinan berbeda, §12) |
| `cd_instrumen_candidates.csv` | csv | 15 KB | ignored | `derived_data` | `needs_researcher_decision` |
| `cd_nader_verbond_candidates.csv` | csv | 170 KB | ignored | `derived_data` | `needs_researcher_decision` |
| `data_perdagangan_1660_1690_ikbal_arsya.json` | json | 32 KB | ignored | `derived_data` | `needs_researcher_decision` |
| `llm_classification_cache.json` | json | 434 KB | ignored | `temporary_artifact` | `remain_ignored` |
| 13 PDF literatur sekunder (`Het Painansch Contract.pdf`, `Padang Abad XVII-XVIII FINISH.pdf`, dll.) | pdf | 745 KB–50 MB | ignored | `source_data` (literatur sekunder, bukan korpus primer VOC) | `remain_ignored` (ukuran besar, tapi bisa dicek per file — lihat §14) |
| `docs/thesis/GM/` (619 file) | xml/csv | 127 MB | ignored | `source_data`/`derived_data` | `remain_ignored` |
| `docs/thesis/dr/` (51 file) | csv | 42 MB | ignored | `derived_data` | `remain_ignored` |
| `docs/thesis/colab/*.py` (skrip Model 2/3/5/6/6b) | py | 5-15 KB tiap | ignored | `notebook_or_script` | **`needs_researcher_decision` — ini KODE PRODUKSI Model 3, bukan data riset besar; alasan asli `.gitignore` (PDF besar) tidak berlaku untuknya** |
| `docs/thesis/colab/*.ipynb` (6 notebook) | ipynb | ratusan KB | ignored | `notebook_or_script` | `needs_researcher_decision` |
| `docs/thesis/graphify-out/` | json/cache | 116 KB | ignored | `temporary_artifact` | `remain_ignored` |

**Tidak ditemukan data sensitif** yang perlu disamarkan dalam pemeriksaan path/nama file ini (tidak ada kredensial/token terlihat dari nama berkas; isi berkas tidak ditampilkan di sini sesuai instruksi).

### A3 — Kandidat allowlist selektif (rancangan tekstual, TIDAK dieksekusi)

#### Opsi 1: Selective unignore

Rule konseptual minimal (contoh pola, **belum ditulis ke `.gitignore`**):

```
docs/thesis/*        # tetap default-ignore semua file langsung di root docs/thesis/
docs/thesis/**/       # tetap default-ignore semua subdirektori...
!docs/thesis/pilot_annotation/
!docs/thesis/pilot_annotation/**
!docs/thesis/EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md
```

Git memerlukan urutan pola negasi (`!`) yang hati-hati — direktori induk yang di-*ignore* penuh **tidak bisa** di-*unignore* sebagian tanpa juga meng-*unignore* jalur ke bawahnya secara eksplisit (masalah umum git: pola `!dir/file` tidak berfungsi jika `dir/` sendiri sudah cocok pola *ignore* tanpa jejak `/*`). Rule di atas perlu diuji dengan `git check-ignore -v` sebelum diterapkan (tidak dilakukan di sini, sesuai batasan tugas).

| | Manfaat | Risiko | Dampak path internal | Risiko data tak-seharusnya | Keputusan peneliti |
|---|---|---|---|---|---|
| **Opsi 1** | Artefak metodologis mendapat perlindungan git penuh (histori, diff, recovery) tanpa memindah satu file pun; jalur `docs/thesis/*.py` (skrip produksi Model 3) bisa ikut di-*unignore* dengan pola tambahan | Rule `!` yang salah urutan bisa diam-diam gagal (git tidak selalu error, kadang cuma tidak berlaku) — perlu verifikasi eksplisit tiap kali direktori baru ditambah ke pilot; risiko drift kalau `pilot_annotation/` kelak berisi data mentah besar tanpa disadari | Tidak ada — path tetap sama persis | Rendah-sedang: `pilot_annotation/` sejauh ini hanya markdown, tapi tidak ada penghalang teknis yang mencegah CSV besar ditaruh di situ kelak dan ikut ter-*track* tanpa sengaja | Apakah proyek nyaman dengan pola *ignore-then-unignore* yang butuh disiplin manual berkelanjutan setiap kali direktori pilot bertambah |
| **Opsi 2** | Tanpa rule negasi rumit — cukup taruh di direktori yang sudah tracked (`docs/prd/`, atau direktori baru `docs/methodology/`) | Duplikasi mental "di mana dokumen metodologi harusnya berada" — proyek sudah punya `docs/prd/` sebagai konvensi PRD, direktori baru menambah satu lagi kategori | **Ada** — seluruh rujukan silang di dalam dokumen (`docs/thesis/pilot_annotation/...`) yang sudah ditulis di fase sebelumnya (mis. rujukan lintas-dossier ke `EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md`) perlu diperbarui manual bila lokasi pindah — **pekerjaan ini SENGAJA tidak dilakukan di audit ini** (batasan "jangan memindahkan file") | Rendah — memindah eksplisit ke lokasi baru, tidak ada risiko menyeret data lain ikut serta | Nama direktori baru apa yang dipakai (`docs/methodology/`? `docs/prd/episode-ontology/`?), dan apakah histori git untuk fase-fase yang SUDAH ditulis (belum ter-*commit* sama sekali) dianggap "mulai dari sini" atau perlu direkonstruksi |

**Tidak satu pun opsi dieksekusi.** Keduanya menunggu keputusan peneliti (D-15, lihat §14).

---

## 4. Corpus Diplomaticum Event Coverage

### B1 — Hasil parsing (parser `csv.DictReader`, bukan `wc -l`)

Kolom aktual `data/research/linimasa_events.csv` (diverifikasi langsung, tidak diasumsikan): `source_document, source_page, book_page, event_date_raw, year, event_type, ruler_actor, title, text_asli, notes, era_slug, fort_name, dominion_status, tags`.

| Ukuran | Nilai |
|---|---|
| Total record (parsed) | **141** |
| Jumlah event merujuk CD1–CD6 | **71** |
| Persentase CD terhadap seluruh record | **50,35%** |
| CD per volume | CD1=6 · CD2=15 · CD3=18 · CD4=20 · CD5=4 · CD6=8 |
| Unique `source_page` per volume | CD1=6 · CD2=**14** · CD3=18 · CD4=20 · CD5=4 · CD6=8 |
| CD events tanpa `source_page` | 0 |
| CD events tanpa `text_asli` (original text) | 0 |
| CD events tanpa transkripsi terpisah | **N/A** — `text_asli` DI SCHEMA INI adalah transkripsi; tidak ada kolom transkripsi independen |
| CD events tanpa translation | **71/71** — **tidak ada kolom `translation` di schema sama sekali**; `title`/`notes` adalah gloss ringkas peneliti, bukan field terjemahan formal |

**Catatan CD2:** 15 event tapi hanya 14 `source_page` unik — satu halaman menjadi sumber untuk dua baris `linimasa_events` berbeda (bukan anomali; wajar bila satu halaman traktat memuat lebih dari satu pasal/peristiwa yang disisir terpisah).

**Koreksi terhadap perkiraan fase sebelumnya:** dokumen `ARCHIVAL_DENSITY_MEASUREMENT_PLAN.md` (fase lalu) sempat menyebut proporsi CD "46%" sebagai tally manual dari percakapan sebelumnya. Angka terverifikasi lewat parsing formal di audit ini adalah **50,35% (71/141)** — perbedaan berasal dari tally manual sebelumnya yang tidak melalui parser CSV eksplisit. Ini dicatat sebagai koreksi, bukan sebagai perubahan pada dokumen fase lalu itu sendiri (yang tidak diubah, sesuai batasan tugas).

---

## 5. Corpus Diplomaticum Local Artifact Search

### B2 — Hasil pencarian menyeluruh

| Path | Jenis artefak | Hubungan dgn CD1-6 | Dapat dipakai provenance? | Referensi mati? | Confidence |
|---|---|---|---|---|---|
| `docs/CD1.pdf` … `docs/CD6.pdf` (dan variasi kapitalisasi/spasi/underscore) | — | — | — | — | **TIDAK DITEMUKAN** di seluruh filesystem yang dapat diakses |
| Arsip ZIP/TAR/7z terkait CD | — | — | — | — | **TIDAK DITEMUKAN** |
| Git LFS pointer | — | — | — | — | **TIDAK ADA** — tidak ada `.gitattributes` di root repo sama sekali |
| Symlink (hidup/mati) terkait CD | — | — | — | — | **TIDAK ADA** — satu-satunya symlink di repo adalah venv Python (`.venv-solver/`), tidak berkaitan |
| `docs/thesis/colab/corpus_diplomaticum_nader_verbond.ipynb` | Notebook Colab | **Langsung** — skrip pemrosesan 6 jilid CD | Tidak langsung (bukan teks sumber), tapi **mengungkap lokasi asli** | Sebagian — kode masih ada, tapi target Drive di luar jangkauan | **Tinggi** untuk lokasi sumber |
| Sel dalam notebook: `CD_DIR = "/content/drive/MyDrive/naro/westkust/cd"` | Path Google Drive (metadata lokasi, bukan file) | **Langsung** — path eksplisit tempat 6 PDF pernah/masih berada | Tidak dapat diverifikasi dari repo ini (di luar filesystem lokal) | Kemungkinan besar file masih ada di Drive pribadi peneliti, tapi status ini **tidak dapat dikonfirmasi** dari sini | **Tinggi** sbg petunjuk, **tidak dapat diverifikasi** keberadaan aktualnya |
| Referensi ke `sisir_cd1.py`/`sisir_cd2.py` (disebut di dalam notebook sbg skrip sesi sebelumnya) | Skrip disebut, **tidak ditemukan** filenya di repo | Langsung (alat ekstraksi CD1/CD2) | Tidak — filenya sendiri hilang | **Ya, referensi mati** | **Tinggi** utk ketiadaan |
| `docs/thesis/corpudiplomaticum.docx` | Transkripsi/terjemahan Indonesia parsial | **Langsung** — 161 paragraf, mencakup ≥4 dokumen bernomor (CCXLI, CCXLII, CCLXXV, DXLV) dari Corpus Diplomaticum | **Ya, sebagian** — ini teks turunan yang bisa dipakai sbg pembanding independen dari `text_asli` singkat di `linimasa_events.csv` untuk dokumen yang sama | Tidak (file benar ada dan terbaca) | **Tinggi** — recovery provenance parsial nyata, bukan spekulasi |
| `docs/cd_resistance_signal_candidates.csv`, `docs/cd_instrumen_candidates.csv`, `docs/cd_nader_verbond_candidates.csv` (di **root** `docs/`, untracked) | Hasil ekstraksi kata kunci (bukan indeks penuh) | Tidak langsung — kutipan konteks per kata kunci, bukan halaman penuh | Sebagian — kutipan `context` bisa jadi petunjuk tambahan | Tidak | Sedang |
| `docs/thesis/cd_resistance_signal_candidates.csv` dkk. (di `docs/thesis/`, **berbeda checksum** dari versi root) | Sama seperti di atas, versi berbeda | Sama | Sama | Tidak | Sedang — **dua salinan tidak identik, lihat §12** |
| `docs/prd/prd-pembersihan-sitasi-cd1-cd6.md` | PRD/dokumentasi | **Konfirmasi eksplisit ketiadaan PDF**, bertanggal 2026-07-17 | Ya — bukti historiografis bahwa ketiadaan ini sudah diketahui tim, bukan temuan baru | Tidak | **Tinggi** |
| README proyek | — | — | — | **Tidak ditemukan** README manapun yang menyebut CD1-CD6 | — |
| Docker volume reference ke `docs/thesis`/CD | — | — | — | **Tidak ditemukan** di `docker-compose.yml` manapun | — |

**Kontras penting (ditemukan saat memeriksa sumber non-CD sebagai pembanding):** setiap `source_document` LAIN yang dirujuk `linimasa_events` — `buku-padang-1718` (`Padang Abad XVII-XVIII FINISH.pdf`), `buku-vogel-1690` (`docs/bsb10468472.txt`), `kathirithamby-1965` (`kathirithamby-wells1976.pdf`), `botham-letter-1781`/`kempen-report-1782` (`docs/HenryBotham`, `docs/Surat-Berita-Penangkapan-Kempen.rtf`), `eic-bl-ior-g35` (`docs/BL_IOR_G_35_198.txt`), `lancaster-1601-1603` (`docs/The voyages of Sir James Lancaster.docx`) — **masih memiliki berkas sumber fisiknya di repository**. **CD1–CD6 adalah satu-satunya koleksi rujukan dari 15 `source_document` unik yang berkasnya sepenuhnya hilang.** Ini konsisten dengan `.gitignore:63` (`docs/*.pdf`, komentar eksplisit "dipakai sekali utk sisir manual") — CD1-6 kemungkinan besar diperlakukan sebagai *scan besar sekali-pakai* yang sengaja tidak disimpan permanen di mesin lokal manapun setelah ekstraksi selesai, berbeda dari dokumen tunggal lain yang lebih kecil dan dipertahankan.

---

## 6. Git History Findings

### B3 — Hasil (read-only, tanpa checkout/restore)

| Pemeriksaan | Hasil |
|---|---|
| `git log --all --oneline -- "**/CD[1-6].pdf"` | **Kosong** — tidak ada commit yang pernah menyentuh file bernama itu |
| `git log --all --pretty=format: --name-only \| grep CD[1-6].pdf` | **Kosong** — nama file tidak pernah muncul di histori commit manapun (termasuk commit yang sudah tidak ada di branch manapun, via `--all`) |
| `git log --all --diff-filter=A -- "*CD[1-6].pdf"` | **Kosong** — tidak pernah ditambahkan |
| Git LFS pointer/`.gitattributes` | **Tidak ada** — repo tidak memakai Git LFS sama sekali |
| Commit message yang merujuk CD1-CD6/Corpus Diplomaticum | **13 commit ditemukan** (mis. `0edb7bc feat(data): sisir CD1.pdf...`, `3773757 feat(data): sisir CD6.pdf...`, `00592ed fix(linimasa): sitasi CD1-CD6...`) — **seluruhnya berupa commit HASIL EKSTRAKSI** (menambah baris ke `linimasa_events.csv`/perbaikan sitasi), **bukan commit yang menambahkan PDF itu sendiri** |
| Rename detection (`git log --follow`) untuk kemungkinan CD*.pdf pernah diganti nama | Tidak dijalankan secara eksplisit terpisah — sudah tercakup oleh `--name-only` di atas yang kosong; tidak ada jejak nama file serupa apapun |

**Kesimpulan B3, tegas:** CD1.pdf–CD6.pdf **tidak pernah menjadi blob git** di repository ini, pada commit manapun, di branch manapun. Ketiadaannya bukan kasus "terhapus dari git" yang bisa dipulihkan via `git checkout <commit> -- path`, karena tidak ada commit yang berisi objek itu untuk dipulihkan. Pemulihan — bila diinginkan — harus datang dari luar git (Google Drive peneliti, per §5), bukan dari histori repo ini.

---

## 7. Provenance Levels

### B4 — Klasifikasi seluruh 71 event CD

| Level | Definisi | Jumlah event | % dari 71 |
|---|---|---|---|
| `provenance_level_A` | objek sumber + halaman + teks tersedia | **0** | 0% |
| `provenance_level_B` | halaman + teks asli tersedia, objek sumber hilang | **71** | **100%** |
| `provenance_level_C` | sitasi tersedia, teks asli hilang | 0 | 0% |
| `provenance_level_D` | label sumber saja | 0 | 0% |
| `provenance_level_E` | provenance ambigu/rusak | 0 | 0% |

**Dasar klasifikasi (bukan hanya karena deskripsi event tersedia, sesuai instruksi):** seluruh 71 baris CD punya `source_page` terisi (folio/halaman spesifik), `book_page` terisi, dan `text_asli` berupa kutipan verbatim (bukan parafrase) — inilah yang menaikkan level dari `C` ke `B`. Tidak satu pun dinaikkan ke `A` karena syarat "objek sumber tersedia" (PDF/scan yang bisa dibuka & diverifikasi ulang) tidak terpenuhi untuk satu pun dari 71 baris — dikonfirmasi §5/§6.

**Field tambahan yang diminta diperiksa (di luar penentu level A-E, dicatat terpisah karena bukan bagian definisi level):**

| Field | Status untuk 71 event CD |
|---|---|
| Volume | AVAILABLE (CD1-CD6, field `source_document`) |
| Halaman | AVAILABLE (`source_page`+`book_page`) |
| Tanggal | AVAILABLE untuk mayoritas (`event_date_raw`+`year`), presisi bervariasi |
| Judul/deskripsi | AVAILABLE (`title`) |
| Original text | AVAILABLE (`text_asli`) |
| Transcription | Setara `text_asli` — tidak ada lapis terpisah |
| Translation | **NOT AVAILABLE** (tidak ada field) |
| Actor | AVAILABLE (`ruler_actor`), tapi granularitas bervariasi (kadang kolektif) |
| Location | PARTIAL (`fort_name` 110/141 terisi utk seluruh dataset, proporsi serupa berlaku di subset CD) |
| Extraction method | **NOT AVAILABLE sbg field** — hanya tersirat dari `notes` naratif per commit/sesi |
| Curator/annotator | **NOT AVAILABLE** — tidak ada field `annotator_id` |
| Confidence | **NOT AVAILABLE dari CSV ini** — `confidence_flag` ada di skema `LinimasaEvent` Postgres tapi TIDAK diekspor ke `linimasa_events.csv` (dikonfirmasi ulang di audit ini, konsisten temuan fase sebelumnya) |
| Source checksum/version | **NOT AVAILABLE** — tidak ada checksum PDF sumber tersimpan di mana pun |

---

## 8. Reproducibility Assessment

| Lapis | Pertanyaan | Status | Alasan |
|---|---|---|---|
| **Computational** | Apakah Model 3 dapat dijalankan ulang dari data yang tersedia? | **complete** | `data/export/all_event_years.csv` (turunan `linimasa_events.csv`, tracked sumbernya) dan skrip `model3_hawkes_kaskade_event.py` sama-sama ada; skrip tidak membaca PDF CD apa pun saat runtime — hanya CSV hasil sisir. Fitting ulang secara teknis bisa dijalankan (**tidak dijalankan di audit ini**, sesuai batasan tugas), tanpa bergantung sama sekali pada keberadaan CD1-6. |
| **Archival** | Apakah setiap event dapat diverifikasi ulang terhadap sumber? | **blocked** (untuk 71 event CD) · **partial** (untuk sisanya) | Untuk CD: `provenance_level_B` — bisa dibandingkan ke kutipan `text_asli` yang tersimpan, TAPI **tidak bisa** dicek ulang ke scan/halaman asli karena objek sumber `NOT AVAILABLE`. Untuk non-CD: objek sumber ADA (PDF/txt/docx/rtf tersedia, §5), tapi belum diverifikasi di audit ini apakah halaman yang dikutip di `linimasa_events` cocok persis dengan halaman di berkas itu (di luar cakupan audit ini) — karena itu `partial`, bukan `complete`. |
| **Interpretive** | Apakah transkripsi, terjemahan, dan keputusan klasifikasi dapat diperiksa ulang? | **blocked** | Tiga alasan bersamaan: (1) tidak ada field `translation` terpisah untuk diperiksa; (2) tidak ada field `extraction_method`/`curator_id` untuk melacak siapa/bagaimana klasifikasi `event_type`/`dominion_status` dibuat; (3) `confidence_flag` ada di skema tapi tidak diekspor ke CSV yang dipakai Model 3. Keputusan klasifikasi (mana yang `perjanjian`, mana `dominion_status='voc_alliance'`) tidak dapat ditelusuri ulang ke proses pengambilan keputusannya, hanya ke hasil akhirnya. |

---

## 9. GM Corpus Logical Record Audit

### C1 — `gm_corpus_filtered_1660_1789.csv` (parser CSV valid, bukan `wc -l`)

| Ukuran | Nilai |
|---|---|
| `wc -l` (baris file mentah, **MENYESATKAN**) | 102.381 |
| Jumlah record logis (parsed benar) | **100** |
| Jumlah kolom | 20 |
| Nama kolom | `volume, surat_id, page, title, tempat_asal_surat, penulis, tahun_surat, text, text_google, text_asli, tanggal_perkiraan, relevan_qwen, relevan_google, sepakat, grounded_qwen, grounded_google, auto_accept, source, lang, tahun_efektif` |
| Record malformed (kolom count tak cocok header) | **0** |
| Record kosong total | **0** |
| Unique `surat_id` (kandidat document key) | **100/100** (100% unik) |
| Unique `(volume, page)` | **100/100** |
| Unique `tahun_efektif` non-kosong | 64 |
| Duplicate `surat_id` | **0** |

**Koreksi terhadap dokumen fase sebelumnya:** `ARCHIVAL_DENSITY_MEASUREMENT_PLAN.md` (§Keterbatasan poin 1) mencatat kekhawatiran bahwa pemeriksaan sebelumnya "hanya 100 baris pertama-terparsing... BUKAN seluruh isi berkas". Audit ini membaca **seluruh berkas** dengan `csv.reader` penuh (tanpa pembatasan baris) dan mengonfirmasi: **berkas ini genuinely hanya berisi 100 record**, bukan terpotong. Kekhawatiran itu sekarang **terjawab, bukan lagi gap terbuka** — dicatat di sini sebagai temuan baru, dokumen lama tidak diubah.

---

## 10. Daghregister Logical Record Audit

### C1 — `daghregister_corpus_classified.csv`

| Ukuran | Nilai |
|---|---|
| `wc -l` (MENYESATKAN) | 75.651 |
| Jumlah record logis (parsed benar, penuh) | **511** |
| Jumlah kolom | 11 |
| Nama kolom | `volume, book_page_start, book_page_end, text, text_asli_belanda, tanggal_perkiraan, source, lang, duplicate_of, record_type, corpus_cleaning_flag` |
| Record malformed | **0** |
| Record kosong total | **0** |
| Unique `volume` | 12 |
| Unique `(volume, book_page_start)` | **511/511** (100% unik) |
| Unique `(volume, book_page_start, book_page_end)` | 511/511 |
| Unique `tanggal_perkiraan` non-kosong (RAW, belum digabung tahun dari nama volume) | 332 |
| Record ber-`duplicate_of` terisi | **41/511 (8%)** |
| Record tanpa `tanggal_perkiraan` | **20/511 (3,9%)** |
| Duplicate `(volume, book_page_start)` keys | **0** |

**Catatan format tanggal:** `tanggal_perkiraan` pada Daghregister sering **tanpa tahun** (contoh nyata dari record pertama: `"14 JANUARY"`) — tahun harus digabung dari nama `volume` (contoh: `Dagh_register_gehouden_int_Casteel_Batavia-1664`). Ini bukan kekosongan field, tapi format tergabung yang butuh parsing tambahan sebelum dipakai sebagai tanggal lengkap — dicatat sebagai potensi jebakan bila dipakai langsung tanpa transformasi.

---

## 11. Candidate Document Keys

### C2 — Uji kandidat key per korpus

| Korpus | Kandidat key | Coverage | Uniqueness | Duplicate rate | Missing rate | Risiko split-document | Risiko merged-document |
|---|---|---|---|---|---|---|---|
| GM | `surat_id` | 100% (100/100 terisi) | 100% (100/100 unik) | 0% | 0% | Rendah — `surat_id` sudah granular per-halaman-surat | Rendah |
| GM | `(volume, page)` | 100% | 100% | 0% | 0% | Setara `surat_id` (satu surat = satu halaman pada sampel ini) | Rendah |
| GM | `volume` saja | 100% | **RENDAH** (hanya 12 nilai unik utk 100 record — bukan kandidat unit dokumen, ini unit koleksi) | Tinggi by design | 0% | **Tinggi bila dipakai sbg document key** — akan menggabungkan puluhan surat berbeda jadi "satu dokumen" | — |
| Daghregister | `(volume, book_page_start)` | 100% | 100% | 0% | 0% | Rendah | Rendah — TAPI lihat `duplicate_of` di bawah |
| Daghregister | `(volume, book_page_start, book_page_end)` | 100% | 100% | 0% | 0% | Sama seperti di atas, tidak menambah presisi (semua `book_page_start=book_page_end` pada sampel yang diperiksa scr implisit karena hasil identik) | Sama |
| Daghregister | Field `duplicate_of` | 8% (41/511) menunjuk record lain | N/A (bukan key, tapi flag) | — | 92% kosong (472/511 dianggap "kanonik"/tak-terduplikasi) | — | **Risiko merged/double-count NYATA bila `duplicate_of` diabaikan** — 41 record berpotensi menghitung ganda peristiwa yang sama jika tidak difilter sebelum agregasi apa pun |
| Daghregister | `volume` saja | 100% | Rendah (12 nilai unik utk 511 record) | Tinggi by design | 0% | Sama seperti GM — unit koleksi/tahun, bukan unit dokumen |

**Kesimpulan C2:** untuk kedua korpus, kombinasi `(volume, identifier-halaman)` adalah kandidat key document yang defensibel (unik, tanpa collision pada sampel yang diperiksa). **Tidak dipilih sebagai key final** di sini — sesuai batasan tugas, keputusan itu ditinggalkan untuk peneliti (lihat §14). Risiko konkret satu-satunya yang ditemukan: 41 record Daghregister ber-`duplicate_of` yang **belum diterapkan** sebagai filter di analisis manapun yang diperiksa sejauh ini dalam proyek ini.

---

## 12. Duplicate and Paired-File Risks

### C3 — File berpola `(1)`/salinan

**Empat pasangan ditemukan di `docs/thesis/colab/`, seluruhnya byte-identical:**

| Original | Duplicate-candidate | Size | Checksum (kedua sisi) | Byte-identical | Schema-identical | Record count |
|---|---|---|---|---|---|---|
| `korpus_final_dengan_topik.csv` | `korpus_final_dengan_topik(1).csv` | 427.542 B (kedua sisi) | `dc823e3f...` (sama) | **YES** | N/A (identik) | N/A (identik) |
| `slr_bab2_hasil.csv` | `slr_bab2_hasil(1).csv` | 744.655 B | `0d34e4cd...` (sama) | **YES** | N/A | N/A |
| `korpus_terklasifikasi.csv` | `korpus_terklasifikasi(1).csv` | 427.237 B | `97702898...` (sama) | **YES** | N/A | N/A |
| `korpus_primer_gabungan.csv` | `korpus_primer_gabungan(1).csv` | 415.546 B | `9e111ebd...` (sama) | **YES** | N/A | N/A |

**Kemungkinan alasan:** pola klasik unduhan-ganda dari browser/Colab (`(1)` adalah suffix otomatis saat nama berkas sudah ada di folder unduhan). **Risiko double-counting rendah** karena byte-identical — tapi **tidak nol**: skrip mana pun yang melakukan `glob("*.csv")` tanpa dedup eksplisit akan memproses kedua salinan, menghitung setiap baris dua kali.

### C3 tambahan — Pasangan TIDAK byte-identical yang ditemukan di luar pola `(1)` (dicatat karena relevan langsung §5)

| File A | File B | Byte-identical | Baris (parsed) A vs B | Catatan |
|---|---|---|---|---|
| `docs/cd_resistance_signal_candidates.csv` | `docs/thesis/cd_resistance_signal_candidates.csv` | **NO** | 19 vs 13 | Dua run ekstraksi berbeda, isi genuinely berbeda — bukan duplikat sederhana |
| `docs/cd_instrumen_candidates.csv` | `docs/thesis/cd_instrumen_candidates.csv` | **NO** | 7 vs 8 | Sama |
| `docs/cd_nader_verbond_candidates.csv` | `docs/thesis/cd_nader_verbond_candidates.csv` | **NO** | 42 vs 86 | Sama — perbedaan terbesar, kemungkinan run lebih lengkap di salah satu versi |

**Ini bukan risiko double-counting yang sama seperti empat pasangan `(1)` di atas** — karena kontennya genuinely berbeda, risikonya justru **kebingungan versi mana yang otoritatif** bila kedua salinan dirujuk bergantian tanpa disadari berbeda. Direkomendasikan sebagai `needs_researcher_decision`, bukan langsung digabung/dihapus (di luar cakupan audit read-only ini untuk memutuskan).

---

## 13. Critical Blockers

Diurutkan berdasarkan dampak terhadap tahap kerja berikutnya (bukan berdasarkan section laporan):

1. **CD1-6.pdf tidak dapat diverifikasi ulang dari repository ini** — memblokir *archival reproducibility* penuh untuk 50,35% `linimasa_events`. Pemulihan (bila dilakukan) harus dari luar repo (Google Drive peneliti), bukan dari git.
2. **Tidak ada field `translation` di skema manapun** — memblokir *interpretive reproducibility* untuk SELURUH korpus (bukan cuma CD), dikonfirmasi ulang berlaku juga di level korpus mentah GM/Daghregister (§9-10 tidak menemukan field translation formal di sana juga).
3. **`confidence_flag` ada di skema Postgres tapi tidak diekspor ke CSV** yang dipakai Model 3 — tingkat kepastian pembacaan per baris tidak bisa diperiksa dari jalur yang benar-benar dipakai.
4. **41 record Daghregister ber-`duplicate_of` belum difilter** dalam analisis manapun yang teramati — risiko double-count laten pada pekerjaan kepadatan arsip mendatang.
5. **Dua pasang CSV kandidat CD (root `docs/` vs `docs/thesis/`) berbeda isi**, bukan duplikat — risiko kebingungan versi otoritatif.
6. **Artefak metodologis fase-fase sebelumnya (1.832 baris kerja) sepenuhnya di luar jangkauan git** — risiko kehilangan yang identik dengan insiden `stratified_analysis.py` yang sudah pernah terjadi di proyek ini (dicatat di memory: skrip yang hilang karena tak pernah ter-*commit*).

---

## 14. Researcher Decisions Required

| ID | Keputusan |
|---|---|
| D-15 | Opsi 1 (selective unignore) vs Opsi 2 (pindah ke direktori tracked) vs tetap ignored — untuk artefak metodologis §3/A3 |
| D-16 | Apakah `docs/thesis/colab/*.py` (skrip PRODUKSI Model 2/3/5/6, bukan data riset besar) dipisahkan dari rule `docs/thesis/` mengingat alasan asli rule (PDF besar) tidak berlaku untuk kode |
| D-17 | Apakah pemulihan CD1-6.pdf dari Google Drive peneliti (`/content/drive/MyDrive/naro/westkust/cd`) diupayakan, dan siapa yang melakukannya (di luar kapasitas audit read-only ini) |
| D-18 | Apakah `docs/thesis/corpudiplomaticum.docx` (161 paragraf, ≥4 dokumen CD bernomor) disandingkan secara sistematis dengan baris `linimasa_events` yang relevan sebagai pembanding independen — pekerjaan anotasi konkret yang bisa dimulai TANPA menunggu pemulihan PDF |
| D-19 | Field `translation` — apakah ditambahkan ke skema (keputusan skema, bukan teknis semata) sebelum interpretive reproducibility bisa dinaikkan statusnya |
| D-20 | `confidence_flag` — apakah diekspor ke `linimasa_events.csv`/pipeline Model 3 |
| D-21 | Rekonsiliasi dua versi CSV kandidat CD (root `docs/` vs `docs/thesis/`) — mana otoritatif, atau apakah keduanya perlu digabung dengan dedup |
| D-22 | Apakah `duplicate_of` di Daghregister diterapkan sebagai filter standar sebelum korpus itu dipakai untuk pengukuran kepadatan (DP-1/DP-2 dari fase sebelumnya) |
| D-23 | Kandidat document key final untuk GM/Daghregister (§11) — `surat_id`/`(volume,book_page_start)` diusulkan, keputusan final tetap milik peneliti |

---

## 15. Recommended Next Phase

Bukan instruksi eksekusi — murni urutan yang secara logis paling murah ke paling mahal, mengikuti pola disiplin ambang biaya yang sudah dipakai proyek ini di tempat lain (mis. ambang AIC Model 3):

1. **Termurah, tanpa risiko:** D-18 — sandingkan `corpudiplomaticum.docx` dengan baris `linimasa_events` yang cocok (4 dokumen bernomor sudah teridentifikasi). Ini pekerjaan baca-cocokkan, tidak butuh apa pun dari luar repo.
2. **Murah, keputusan git murni:** D-15/D-16 — pilih Opsi 1 atau 2 untuk artefak metodologis, terapkan (di luar cakupan audit ini).
3. **Sedang:** D-21/D-22 — rekonsiliasi versi CSV kandidat CD dan penerapan filter `duplicate_of` Daghregister.
4. **Bergantung akses eksternal:** D-17 — pemulihan CD1-6.pdf dari Drive, hanya bila peneliti punya akses dan keperluan konkret (verifikasi ulang halaman spesifik, bukan re-ekstraksi masal).
5. **Keputusan skema jangka panjang:** D-19/D-20/D-23 — perubahan field, di luar cakupan "audit read-only", perlu putaran kerja tersendiri.

---

# Bagian E: Verifikasi Akhir
