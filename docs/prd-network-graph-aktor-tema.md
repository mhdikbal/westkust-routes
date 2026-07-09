# PRD / Planning — Network Graph "Siapa Terhubung dengan Siapa, di Bidang Apa"

**Status:** Draft planning (MLOps) — 2026-07-09
**Tim (role framing):** Scrum Master, MLOps, DBA — Muhammad Ikbal
**Konteks:** lanjutan Sankey Tema-Korpus (`docs/prd-sankey-tema-korpus.md`, SNK-1..5 selesai + halaman `/riset/tema`). Sumber data sama: `research_theme_rows` (1.005 baris terklasifikasi 7 tema + pelabuhan + teks) + data voyage.

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
