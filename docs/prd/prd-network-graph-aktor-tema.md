# PRD / Planning — Network Graph "Siapa Terhubung dengan Siapa, di Bidang Apa"

**Status:** Draft planning (MLOps) — **REVISI 2026-07-09b** (probe data + frame polity-afiliasi user). **PILOT FASE 2 DIJALANKAN 2026-07-31 — GERBANG GAGAL (presisi 36% vs ambang 0,8)**, lihat §0★★. **FILTER DIRANCANG + RE-PILOT 2026-07-31 — GERBANG LOLOS (presisi 15/15=100%)**, lihat §0★★★: filter "≥2 istilah pantai-barat unik di teks baris sendiri" menaikkan presisi drastis. Fase 2 boleh lanjut scale ke 118 baris hasil filter (bukan 1.005/409 mentah) + audit berkala. **FILTER DITERAPKAN KE FASE 1 LIVE 2026-07-31** — lihat §0★★★★: `GET /api/research/network-pelabuhan` (`backend/routers/research.py`) sekarang jg pakai filter yg sama, scope SEMUA `tema_dominan` (bukan cuma sengketa/syahbandar).
**Tim (role framing):** Scrum Master, MLOps, DBA — Muhammad Ikbal
**Konteks:** lanjutan Sankey Tema-Korpus (`docs/prd/prd-sankey-tema-korpus.md`, SNK-1..5 SELESAI & LIVE di `salido.my.id/atlas/riset/tema`). Sumber data sama: `research_theme_rows` (1.005 baris terklasifikasi 7 tema + pelabuhan + teks).

---

## 0★. REVISI 2026-07-09b — Temuan Probe + Model Final (MENGGANTIKAN §3–§4 di bawah)

Frame user diperjelas: **node = polity pesisir (masing-masing punya jabatan politik/afiliasi) + aktor eksternal; edge = relasi bertipe (diplomasi / dagang / perang) ke VOC dll; split 1660–1699 vs 1700–1799.** Diprobe ke DB nyata (bukan asumsi):

### Bukti A — sinyal kelompok aktor per periode (keyword ILIKE, batas atas + noise)
| Periode | Baris | China | VOC | Kerajaan-lokal | Syahbandar | Inggris/Aceh |
|---|--:|--:|--:|--:|--:|--:|
| 1660–1699 | 561 | 137 | 333 | 271 | **4** | 120 |
| 1700–1799 | 407 | 31 | 235 | 111 | **0** | 30 |

### Bukti B — coverage polity (di `pelabuhan_disebut`)
Padang 654 · Barus 330 · Pulau Cingkuak 309 · Salido 276 · Pariaman 251 · Inderapura 228 · Air Bangis 109 · Air Haji 85 · Tiku 79 · Bayang 47 · **Painan 8 (tipis)** · **Tarusan 0 (TIDAK ADA di korpus, port maupun teks/"Taroesan")**. Backbone edge: **481 baris multi-polity**.

### Keputusan model (dari bukti)
1. **Node = 10 polity lokal** (Padang…Bayang) **+ eksternal** (VOC, Aceh, China, Inggris/EIC). **Drop Tarusan** (0 sinyal); Painan tandai lemah.
2. **"Syahbandar" BUKAN node** — kata harfiah cuma 4× (padahal tema `syahbandar` 511 baris) → itu **peran/tema**, dipakai sebagai **label-edge**, bukan aktor.
3. **Tambah Inggris (EIC) + Aceh** sebagai kelompok (segitiga VOC–Inggris–Aceh = inti konflik pesisir).
4. **Split periode bermakna:** 1660-99 jauh lebih padat (561 vs 407); semua kelompok menurun ke abad-18 → cerita yang layak divisualkan.
5. Edge = co-occurrence (polity↔polity dari multi-port; polity↔eksternal dari keyword+port).

### Tipe edge (diplomasi/dagang/perang) — SEBAGIAN BESAR 0 GPU
Tipe relasi user **sudah tersedia** dari `tema_dominan` yang dulu di-GPU-kan:
| Tipe relasi user | Turunan dari tema existing? |
|---|---|
| perang/konflik | ✅ `sengketa` |
| dagang | ✅ `pelayaran` |
| administrasi/kepelabuhanan | ✅ `syahbandar` |
| **diplomasi / aliansi** | ❌ belum ada label — satu-satunya yang mungkin butuh run baru |

### Verdict GPU/Colab (REVISI, jawaban langsung ke user)
- **Tier 1 (struktur + tipe edge dari tema): tetap 0 GPU** — warna/tipe edge diturunkan dari `tema_dominan`. Dapat ~80% (termasuk dagang & perang) gratis.
- **GPU/Colab hanya relevan** bila mau label `diplomasi`/`aliansi` yang belum ada di 7 tema. **Bahkan itu pun 1.000 baris = CPU cukup** (zero-shot mDeBERTa ~beberapa menit; T4 hanya ~5-10× lebih cepat = kenyamanan iterasi, bukan syarat).
- **GPU tidak menyelesaikan risiko sebenarnya** = akurasi ekstraksi/typing di teks OCR historis ([[feedback_verify_entity_extraction_before_trusting]], gagal 2×). Itu urusan **validasi**, bukan compute.
- **MLOps: JANGAN nyalakan T4 dulu.** Nyalakan hanya untuk label `diplomasi/aliansi` bila user memang mau bedakan dari `sengketa`.

### Rencana bertahap (REVISI)
- **Tier 1a — sekarang, 0 GPU ⭐:** endpoint `GET /api/research/network-faksi?year_from=&year_to=` → `{nodes,edges}`; node polity+eksternal (keyword-tagging faksi), edge co-occurrence, **tipe/warna edge dari `tema_dominan`**, split 2 periode. UI `/riset/jaringan` (identitas salido.my.id, force-directed d3/Cytoscape, drill→`/rows`). **Gerbang: spot-check 25 baris** (keyword-tag cocok realita? refine daftar) SEBELUM render dipercaya.
- **Tier 1b — opsional:** kalau `diplomasi/aliansi` dibutuhkan & tak ada di tema → zero-shot kecil (Colab GPU *boleh*, CPU cukup) + validasi.
- **Tier 2 — nanti:** aktor bernama individu (Sultan Mahomettha, pejabat VOC, Kapitan Cina) — NER/LLM + validasi manual sample dulu.

**Open question baru:** (a) nama alternatif "Tarusan" bila memang ingin dipertahankan? (b) `diplomasi` cukup diturunkan dari kombinasi tema+konteks, atau wajib label baru (→ Tier 1b)? (c) afiliasi polity (pro-VOC / pro-Aceh / independen) per periode — dihitung dari pola edge, atau butuh anotasi manual?

---

## 0★★. Pilot Fase 2 — Gerbang Presisi 20-30 Baris (2026-07-31, next-step #5 riset Aktor Siri Nara)

**Metode:** 25 baris `data/research/korpus_tema_slim.csv` (tema `sengketa`/`syahbandar`, `low_confidence`≠true), sampel stride sistematis dari 409 baris eligible + 1 baris jangkar (`id=788`, contoh yg dikutip PRD §1 sendiri). Tiap baris dibaca PENUH (bukan keyword-match) lalu entitas (aktor+peran+polity) diekstrak manual dan diverifikasi thd `text`/`text_asli` — mengikuti protokol [[feedback_verify_entity_extraction_before_trusting]] (2 kegagalan sebelumnya krn keyword-match tanpa baca teks penuh).

**HASIL: GERBANG GAGAL — presisi 8/25 = 32%, jauh di bawah ambang 0,8.** Tapi bukan krn ekstraksi entitas salah — akar masalahnya BEDA dan lebih dasar:

| Kategori | Jumlah | Contoh id | Masalah |
|---|--:|---|---|
| **Baris genuinely pantai-barat, triple bisa diekstrak bersih** | 8/25 (32%) | 165, 375, 419, 619, 787, **788**, 848, 964 | Ini yg "benar" — lihat detail di bawah. |
| **False-positive tagging `pelabuhan_disebut`** — isi baris SAMA SEKALI bukan ttg pantai barat (Makassar/Palembang/Ceylon/Ambon/Banjarmasin/Lampung/keuangan VOC umum), tp kolom port tetap sebut Padang/Salido/dll | 10/25 (40%) | 2, 35, 77, 200, 244, 278, 347, 497, 525, 569 | Halaman REGISTER/INDEKS arsip (daftar surat multi-wilayah dlm 1 halaman) — nama pelabuhan pantai-barat "bocor" ke kolom tag krn muncul di BAGIAN LAIN halaman yg sama, bukan krn baris itu SENDIRI membahasnya. |
| **Ambigu/terlalu tipis/OCR rusak parah** | 5/25 (20%) | 135, 315, 448, 895, 929 | Halaman sampul/generik atau OCR "[tidak terbaca]" terlalu banyak utk verifikasi aman. |
| **Tag "Tidak diketahui" — konsisten, bukan error** | 2/25 (8%) | 675, 726 | Kontrol negatif: memang bukan ttg pantai barat DAN kolom port memang kosong — sistem tag benar di sini. |

**8 baris yg LOLOS verifikasi (contoh entitas terekstrak, semua dicek manual thd teks):**
- **id=375 (1720)** — "panglima Siri nara" (pengirim surat, bersama pengulu, dari **Sillida**) DAN "panglima Radja" (pengirim surat terpisah) muncul dlm baris yg SAMA sbg 2 pengirim surat berbeda — **korroborasi langsung** temuan §2c PRD aktor Siri Nara: keduanya jabatan terpisah, bukan 1 identitas.
- **id=788 (1668)** — baris contoh asli §1 PRD ini: Sultan Mahomettha (Indrapoura), gubernur Silida (peran tanpa nama), Radja de Hilmer (utusan, Cottatenga→Padang), Nachoda Poeti (utusan), Gatip Moeda (utusan, Silida+Indrapoury), Jan de Petuan (VOC, Maningcabo).
- **id=787 (1668)** — "Panglima 't Siaya Radja" (varian OCR gelar, mungkin "Panglima Setia Radja"), 12 anggota Dewan Padang, **Radja Adil** (cocok dgn temuan GM Deel03 hlm.670 riset aktor Siri Nara — figur yg sama muncul di 2 korpus beda).
- **id=848 (1677)** — "commandeur Jacob Jorissen Pits" (cocok Pits dari riset GM sblmnya), "opperkoopman Melchior Hurt" di Poeloe Chinco.
- **id=964 (1681)** — "Radja Mangsoor" ditangkap & dipenjara; regenten Sinckal; "Radja Lillas Sittia" (rumahnya dibakar) — Radja Mangsoor cocok dgn "Radja Mansur"/"Radja Mangsor" di temuan GM (§2c, "tot in 1714 als hoofd").
- id=165, 419, 619 — register pantai-barat genuin, aktor: Komandan Christiaan/Willem van der Feltz (Padang, 1747); Rhyn & van Velsen (opperhoofd P.Cingkuak), Meijert Joan van Jdsinga (Komandan Padang, 1752); Jan van Groenwegen (1663, cocok temuan `Padang Abad XVII-XVIII`).

**Kesimpulan gerbang:**
1. **JANGAN scale ke 1.005 baris sekarang** — presisi 32% jauh di bawah ambang 0,8, PERSIS pola kegagalan yg diperingatkan [[feedback_verify_entity_extraction_before_trusting]] (kegagalan ke-3 kalau dipaksa lanjut tanpa perbaikan).
2. **TAPI akar masalahnya BUKAN ekstraksi entitas** (8 baris yg lolos, entitasnya akurat & malah SALING KORROBORASI dgn riset GM/aktor Siri Nara terpisah — sinyal kualitas tinggi). **Akar masalahnya ada di HULU**: kolom `pelabuhan_disebut` di `korpus_tema_slim.csv` tercemar oleh halaman register/indeks arsip multi-wilayah (1 halaman archival berisi daftar surat dari BANYAK wilayah VOC sekaligus — Ambon, Ceylon, Makassar, dst — nama pelabuhan pantai-barat ikut "kebocor" ke tag meski baris ybs sama sekali bukan ttg pantai barat).
3. **Rekomendasi perbaikan sebelum coba lagi**: filter baris kandidat bukan cuma dari `pelabuhan_disebut` + `tema_dominan`, tp tambahkan filter konten-narasi (mis. exclude baris yg didominasi pola "daftar surat"/"register"/"salinan surat...tertanggal" tanpa narasi peristiwa, atau naikkan bobot ke baris dgn kata kerja peristiwa eksplisit). Fase 1 (`network-pelabuhan`, co-occurrence murni dari `pelabuhan_disebut`) **jg berisiko sama** — kalau 40% co-occurrence tag salah di sampel ini, edge Fase 1 kemungkinan besar jg mengandung noise serupa; layak di-spot-check terpisah (PRD Fase 1 §4 sudah minta "gerbang: spot-check 25 baris" — REKOMENDASI: jalankan spot-check itu dgn kriteria SAMA ketatnya spt pilot ini, bukan cuma "cocok realita?" longgar).
4. **Next steps pasca-pilot ini**: (a) desain filter konten-narasi di atas, (b) re-run pilot 20-30 baris dgn filter baru, (c) baru evaluasi ulang gerbang 0,8 — BUKAN langsung scale dari hasil sekarang.

---

## 0★★★. Filter Konten-Narasi + Re-Pilot (2026-07-31, sesi lanjutan)

**Koreksi kecil dulu:** saat merancang filter, 2 baris di pilot §0★★ yg tadinya divonis "off-topic" (id=569, id=842 belakangan — lihat re-pilot) ternyata SALAH nilai krn cuplikan awal yg dibaca cuma 700-900 karakter pertama (boilerplate finansial/gudang sblm narasi sesungguhnya muncul). Setelah baca teks PENUH: presisi asli §0★★ terkoreksi jadi **9/25 (36%)**, bukan 32% — tetap jauh di bawah ambang, kesimpulan gerbang-gagal tak berubah, tp dicatat demi akurasi.

### Desain Filter

**Aturan:** baris lolos filter HANYA jika teks barisnya SENDIRI (kolom `text`, bukan `pelabuhan_disebut`) memuat **≥2 istilah pantai-barat berbeda** dari daftar terkendali (termasuk varian ejaan arkais): `padang, silida/sillida/salido, pariaman, bayang, indrapoura/inderapura/indrapoera, tiku/ticco, air bangis, air haji, cingkuak/chinco/chinko, barus, sumatra barat/sumatra's westkust/westcust, maningcabo, sillebar, sinckal/singkil`.

**Kenapa ini beda dari `pelabuhan_disebut`:** kolom itu tercemar di level HALAMAN (lihat [[feedback_register_page_contamination.md]]) — filter baru ini re-verifikasi independen langsung dari teks baris, bukan mempercayai tag yg sudah ada.

**Validasi thd 25 baris pilot §0★★ (ground truth hasil baca manual, dikoreksi):** ambang "≥2 istilah unik" memberi **0 false-positive** pada 9 baris yg terkonfirmasi off-topic, dan menangkap **7/9 (78%)** baris yg terkonfirmasi genuine pantai-barat (2 gagal tertangkap krn cuma py 1 istilah unik — precision tinggi, recall cukup, trade-off yg wajar utk gerbang presisi).

**Yield di seluruh korpus:** dari 409 baris eligible (`sengketa`/`syahbandar`, `low_confidence`≠true), **118 baris (29%) lolos filter** — inilah kandidat kolam yg akan discale, bukan 409 mentah.

### Re-Pilot: 15 Baris Baru (Lolos Filter, Belum Overlap dgn 25 Baris §0★★)

Sampel random (seed tetap) dari 118 baris lolos filter, dibaca PENUH:

| id | Tahun | Verdict | Entitas kunci terverifikasi |
|---|---|---|---|
| 138, 142, 261, 409, 415, 436 | 1733-1764 | GOOD (register tipis tp valid) | Pejabat bernama+peran+Padang (Mumme, Bruijnink, von Erath, Feltz, dst) — tipis tp akurat |
| 357 | 1682 | **GOOD** | Jan van Leene (dewan Padang), **"Kerajaan Troessang"** (Tarusan lagi!), Francois Backer (resident Barus), Arent Silvius (opperkoopman P.Cingkuak) |
| 358 | 1686 | GOOD | Iacobus Couper (komandan Padang), kontrak "Sapoela Boabandaers" (Sapuluh Buah Bandar), radja Lakitan |
| 362 | 1692 | GOOD | Salom Lesage (komandeur), sultan Maningcabo, Werlinghoff (berghopman tambang) |
| 610 | 1663 | GOOD | Orangcay Kitchil, **Jan van Groenewegen** (cocok temuan `Padang Abad XVII-XVIII`) |
| **709** | **1666** | **GOOD — TEMUAN BESAR** | "**Ciery Radie Olebalang**" diangkat Gouverneur Cota Tenga — **MENJAWAB gap §2c**: ini "Sireradja Oeloebalang" (indeks DR-1663 hlm.701) yg blm terbaca! Plus orangcaya Quitschil→Gouverneur Padang, Radja Bougys→Radja Olakan, Radja Ambon→panglima Priaman. |
| **816** | **1676** | **GOOD — korroborasi** | "gubernur di Sirrenarroe hingga Sillida" (=Siri Nara) + Jacob Jorissen Pits — **kemungkinan SUMBER YG SAMA** dgn episode "obstinaetheyt" GM Deel04 hlm.83 (§2b), versi korpus beda |
| 842 | 1677 | GOOD (setelah re-baca penuh, awalnya salah nilai krn cuplikan pendek) | Jacob Jorissen Pits minta pasokan "tambang Sillidase"; nachoda Poety (Pauh, Kota Tengah) berontak-damai berulang |
| 860 | 1678 | GOOD | Melchior Hurt (komandan Padang), kerusuhan Priaman |
| **940** | **1680** | **GOOD** | Traktat: "Sirrenarra, gubernur lot Sillida" (Siri Nara lagi, titik data independen baru!), "Wanglinie Hadja gubernur Palaugb", Sultan Mamselchia Indrapoura, Catip Moed |

**Presisi re-pilot: 15/15 = 100%** (semua baris menghasilkan minimal 1 triple aktor+peran+polity terverifikasi & genuine pantai-barat) — **GERBANG LOLOS**, jauh di atas ambang 0,8. (Catatan jujur: n=15 kecil, interval kepercayaan lebar — rekomendasi tetap audit berkala sampel begitu discale, bukan anggap 100% permanen.)

**Bonus tak terduga:** 2 baris re-pilot LANGSUNG menjawab gap terbuka riset aktor Siri Nara sebelumnya — id=709 (1666) mengidentifikasi "Sireradja Oeloebalang" sbg Gubernur Cota Tenga (Kota Tengah), dan id=940 (1680) + id=816 (1676) menambah 2 titik data independen baru utk kronologi Siri Nara/Sillida. **Rekomendasi: salin temuan ini balik ke `prd-aktor-siri-nara-riset-kronologi.md` §2b/§2c** sbg tindak lanjut riset (di luar scope network-graph, tp sayang dilewatkan).

### Kesimpulan & Rekomendasi

1. **Filter konten-narasi (≥2 istilah pantai-barat unik di teks baris sendiri) TERVALIDASI** — naikkan presisi dari 36% → 100% pada sampel kecil.
2. **Fase 2 boleh lanjut ke scale**, TAPI scope-nya 118 baris (hasil filter), BUKAN 1.005/409 mentah. Endpoint `network-faksi`/`network-pelabuhan` (§0★ Tier 1a) sebaiknya jg terapkan filter yg sama sblm construct edge, bukan cuma pakai `pelabuhan_disebut` mentah — [[feedback_register_page_contamination.md]] berlaku jg utk Fase 1 yg sudah live.
3. **Audit berkala tetap wajib** kalau scale ke 118 baris penuh — sampel 15 baris terlalu kecil utk klaim final, tp cukup kuat utk lanjut ke tahap scale-terbatas dgn spot-check susulan.

---

## 0★★★★. Filter Diterapkan ke Fase 1 Live (2026-07-31)

Filter §0★★★ diterapkan langsung ke endpoint **produksi** `GET /api/research/network-pelabuhan` (`backend/routers/research.py`), bukan cuma pilot riset. **Keputusan scope (arahan user):** diterapkan ke **SEMUA** `tema_dominan`, bukan cuma `sengketa`/`syahbandar` yg jadi basis validasi §0★★★ — alasannya mekanisme kontaminasi (halaman register/indeks arsip multi-wilayah, lih. [[feedback_register_page_contamination]]) tak spesifik-tema, jadi kemungkinan besar menggeneralisasi. Transparansi dijaga lewat counter baru `meta.n_filtered_relevance`.

**Implementasi:**
- `WESTCOAST_TERMS` + `_is_westcoast_relevant()` — helper baru di `research.py`, daftar istilah SAMA persis dgn yg divalidasi §0★★★.
- Query endpoint sekarang jg `SELECT ResearchThemeRow.text` (kolom teks mentah sudah ada di DB, dimuat via `seed_research_tema.py` dari `korpus_tema_slim.csv` — tak perlu ETL/backfill baru).
- Filter diterapkan in-Python di awal loop (pola sama dgn filter `tema` yg sudah ada), SEBELUM baris masuk hitungan node/edge/`n_rows`.
- 5 test TDD baru di `backend/tests/test_research_network.py` (total 19, semua hijau): baris off-topic tersingkir total meski `pelabuhan_disebut`-nya kelihatan valid, ambang 1-istilah tetap tersingkir, baris genuine lolos & bentuk edge, filter jalan independen dari `tema`, dan konsistensi counter pd batch campuran.

**Dampak nyata di data produksi (dicek langsung stlh deploy):**
```
n_rows: 212 (dari 902 total baris)
n_filtered_relevance: 690  (76% tersingkir sbg noise)
n_nodes: 11   (SAMA PERSIS dgn baseline sblm filter — lihat memori project_network_graph_fase1)
n_edges: 48   (baseline sblm filter: 49 — turun 1)
```
**Interpretasi:** meski 76% baris tersingkir sbg noise, struktur graf (jumlah node & edge) nyaris tak berubah — bukti kuat bahwa baris yg disingkirkan memang noise (tak pernah membentuk co-occurrence pasangan pelabuhan yg genuine), bukan sinyal asli yg ikut terbuang. Node weight (bobot mention per pelabuhan) turun signifikan krn tak lagi dobel-hitung mention palsu dari halaman register tercemar — lebih akurat merepresentasikan kepadatan sinyal riil per pelabuhan.

**Gotcha operasional yg diikuti** (`[[project_network_graph_fase1]]`): endpoint ini cache-aside Redis (TTL 24 jam, key HANYA dari `year_from`/`year_to`/`tema` — TIDAK dari versi kode), jadi cache namespace `voc:research_network_pelabuhan:*` WAJIB di-flush saat deploy supaya payload lama (tanpa filter) tak terus disajikan sampai TTL alami habis. Sudah dijalankan sesi ini (1 key ditemukan & dihapus, verifikasi ulang X-Cache: MISS → payload baru benar).

---

*(§0–§7 di bawah = draft awal, dipertahankan sebagai riwayat; model final ada di §0★ di atas.)*

---

## 0. Reality-check GPU — BACA DULU (jawaban langsung untuk pertanyaan user)

**Pertanyaan user:** "perlu kita buat coding T4 GPU di colab sepertinya nih?"

**Jawaban jujur: kemungkinan besar TIDAK — beda kasus dengan Sankey.**

- Sankey **butuh** GPU karena itu inferensi model (zero-shot mDeBERTa mengklasifikasi 1.005 baris ke 7 tema — beban model nyata).
- Network graph **beban komputasinya ringan**: 1.005 teks pendek. Bagian sulitnya bukan *compute*, tapi **akurasi ekstraksi entitas + validasi** — dan GPU tidak menyelesaikan itu.
- **Peringatan keras dari memori proyek** ([[feedback_verify_entity_extraction_before_trusting]]): ekstraksi entitas di korpus ini **sudah GAGAL 2×** (0/5 dan 0/12 nama kapal/tempat tak cocok teks asli). Menjalankan pipeline NER/GPU penuh tanpa validasi kecil dulu = mengulang kegagalan yang sudah tercatat.

**Kesimpulan:** Fase 1 (graph pelabuhan↔pelabuhan per tema) **0 GPU, 0 ML** — murni SQL/CPU dari kolom `pelabuhan_disebut` yang SUDAH ada. Fase 2 (aktor: Sultan, syahbandar, pejabat VOC) butuh ekstraksi teks, tapi untuk 1.005 baris cukup **CPU (spaCy/NER) atau LLM API** — bukan T4. GPU baru relevan kalau nanti pakai LLM lokal besar / embedding skala besar (belum perlu).

---

## 1. Problem Statement

Sankey menunjukkan **konsentrasi** tema per pelabuhan sepanjang waktu, tapi tidak menunjukkan **relasi antar-entitas**: pelabuhan mana yang muncul bersama dalam peristiwa yang sama, aktor mana (raja, syahbandar, pejabat VOC) yang terkait dengan siapa, dalam bidang apa (sengketa / pelayaran / syahbandar / hak adat). Teks drill-down membuktikan relasi ini ADA dan kaya — mis. satu baris sengketa 1668 menyebut *Sultan Mahomettha dari Indrapoura*, *gubernur Silida*, *utusan dari Padang*, *Radja de Hilmer*, *Nachoda Poeti*, *Jan de Petuan* dalam satu peristiwa. Pola relasional ini tak terbaca di Sankey (yang tri-partit dekade→tema→pelabuhan, bukan graf).

## 2. Goal

Graf jaringan: **node = entitas**, **edge = keterhubungan dalam peristiwa/baris yang sama**, **warna/label edge = bidang (tema)**. Menjawab "siapa terhubung dengan siapa, di bidang apa" secara visual & bisa di-drill ke baris teks penyusun (audit, konsisten pola Sankey).

## 3. Sumber Data & Jenis Node (tanpa ekstraksi baru vs butuh ekstraksi)

| Jenis node | Sumber | Butuh ML/GPU? |
|---|---|---|
| **Pelabuhan** | `pelabuhan_disebut` (SUDAH ada; 481 baris multi-port = co-occurrence siap pakai) | ❌ tidak — SQL/CPU |
| **Tema** (sbg edge-label) | `tema_dominan` (SUDAH ada) | ❌ tidak |
| **Korpus/sumber, dekade** | kolom yang ada | ❌ tidak |
| **Aktor** (Sultan, syahbandar, pejabat VOC, nachoda) | ekstraksi dari `text` / `text_asli` | ⚠️ ekstraksi — CPU/LLM, **BUKAN wajib T4** |
| **Relasi bertipe** (aliansi/konflik/otoritas/dagang) | relation extraction dari teks | ⚠️ paling sulit — validasi manual wajib |

## 4. Rencana Bertahap (ship yang murah & pasti dulu)

### Fase 1 — Graph Pelabuhan↔Pelabuhan per Tema (P0, 0 GPU) ⭐ MVP
- **Node** = pelabuhan; **edge** = dua pelabuhan disebut di baris yang sama; **bobot** = jumlah co-occurrence; **warna edge** = tema dominan baris. Filter dekade (reuse pola SNK-2).
- Endpoint baru `GET /api/research/network-pelabuhan?year_from=&year_to=&tema=` → `{nodes:[{id,label,weight}], edges:[{source,target,weight,tema}]}`. Murni agregasi SQL dari `pelabuhan_disebut` (explode pasangan). **TDD, CPU, idempotent.**
- UI: halaman `/riset/jaringan` (identitas salido.my.id, sama seperti `/riset/tema`), render force-directed ringan (mis. d3-force atau Cytoscape.js) + drill ke `/rows`.
- **Menjawab 80% pertanyaan user** ("pelabuhan mana terhubung, di bidang apa") tanpa risiko ekstraksi.

### Fase 2 — Ekstraksi Aktor (P1, PILOT-DULU, tetap tanpa T4)
- **Gerbang wajib** (pelajaran [[feedback_verify_entity_extraction_before_trusting]]): pilot 20–30 baris sengketa/syahbandar → ekstrak entitas (aktor + peran + polity) → **cek manual thd teks asli** → hitung presisi. **Hanya jika ≥ ambang (mis. presisi ≥0,8) → scale ke 1.005 baris.**
- Alat: spaCy NER (CPU) ATAU LLM via API dengan prompt ekstraksi triple `(aktor, relasi, aktor/tempat, tema)`. Untuk 1.005 teks pendek, **CPU/API cukup — T4 tidak memberi nilai tambah**.
- Tantangan historis (harus ditangani): varian ejaan (Indrapoura/Inderapura), peran-vs-nama ("gubernur Silida" = jabatan+tempat, bukan orang), noise OCR.

### Fase 3 — Relasi Bertipe (P2, riset)
- Tipe edge (aliansi/konflik/otoritas/dagang) — relation extraction, paling rawan. Untuk klaim thesis: kombinasi LLM-assisted + **koding manual** pada subset, bukan otomasi penuh.

## 5. Non-Goals
- Bukan menggantikan Sankey (pelengkap: Sankey=konsentrasi, graph=relasi).
- Bukan di peta publik `/atlas` (thesis-only, noindex — sama SEC-SNK-2).
- Fase 1 TIDAK menunggu ekstraksi aktor — dirilis lebih dulu.

## 6. Open Questions
1. Prioritas: cukup graph **pelabuhan** (Fase 1) untuk exhibit Bab 3, atau aktor (Fase 2) memang dibutuhkan untuk argumen thesis? (menentukan apakah masuk ke ekstraksi sama sekali).
2. Ambang presisi pilot Fase 2 sebelum boleh scale?
3. Library render graf: d3-force (kontrol penuh) vs Cytoscape.js (fitur graf matang) — konsisten pola "lib-agnostik desain dulu" seperti Sankey?

## 7. Rekomendasi MLOps (ringkas)
1. **Kerjakan Fase 1 sekarang** — CPU, cepat, pasti, menjawab inti pertanyaan.
2. **JANGAN nyalakan T4 dulu** untuk ini — tidak diperlukan; nyalakan hanya bila pilot Fase 2 tervalidasi DAN kita sengaja pilih model lokal besar (belum).
3. Fase 2 hanya setelah **pilot kecil tervalidasi manual** — hindari kegagalan ekstraksi ke-3.
