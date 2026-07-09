# Sprint Board — Sankey Tema-Korpus (GLOBALISE + Dagh-register)

**Sprint Goal:** Sankey tema-korpus (jilid/tahun → tema → pelabuhan) hidup end-to-end sebagai *exhibit* Bab 3 thesis — dari CSV klasifikasi GPU yang sudah jadi, sampai endpoint + drill-down yang bisa diaudit reviewer.
**Scrum Master:** Muhammad Ikbal · **Disusun:** 2026-07-08 · **PRD:** `docs/prd-sankey-tema-korpus.md`
**Konteks kunci:** GPU T4 **sudah boleh dimatikan** — semua sisa pekerjaan CPU-side/backend.

---

## 0. Status Klasifikasi (fakta terverifikasi hari ini)

| Artefak | Isi | Status |
|---|---|---|
| `dr/korpus_tema_globalise_daghregister.csv` | 1.005 baris (535 globalise + 470 daghregister), 7 skor tema per baris | ✅ ada, tervalidasi |
| `dr/sankey_tema_agregat.csv` (Colab) | 314 baris agregat | ⚠️ cacat — 485 baris ter-drop, 236 node gabungan `;` |
| `dr/sankey_tema_agregat_fixed.csv` | 512 baris agregat | ✅ **hasil sprint ini** |
| `dr/fix_sankey_report.csv` | laporan verifikasi granular | ✅ **hasil sprint ini** |

**GPU:** step klasifikasi zero-shot (mDeBERTa, T4) selesai & final. **Matikan T4.** Re-run hanya jika 7 kategori berubah (sudah RESOLVED) atau korpus bertambah.

---

## 1. Pembentukan Tim (role framing — semua Ikbal)

| Tim | Tanggung jawab di sprint ini | Boundary |
|---|---|---|
| **MLOps** | Pipeline klasifikasi, fix agregat CPU-side, matikan/hidupkan GPU, idempotency re-run | TIDAK sentuh backend API |
| **DBA** | Skema namespace `research`, muat korpus ke Postgres, query agregasi endpoint, drill-down, investigasi bloat `text_asli` | TIDAK ubah data klasifikasi |
| **DevSecOps** | 552MB CSV jangan masuk git, `.gitignore`/artefak, akses thesis-only (Open Q#4), CI hijau sebelum push | Gate deploy |
| **QA** | Verifikasi row-count granular (bukan total), regression endpoint, cek tidak ada drop diam-diam, DoD | Veto rilis |

---

## 2. Backlog (prioritas P0 → P1, story points relatif)

### ✅ DONE sprint ini
- **[MLOps][3]** Fix #1 — pulihkan tahun dari `volume` (458 baris daghregister balik), bucket eksplisit "Tak bertahun" (27 globalise, tak di-drop).
- **[MLOps][2]** Fix #2 — explode multi-pelabuhan (481 baris → 2.609 kontribusi link, node `;` 236→0).
- **[QA][1]** Verifikasi granular: sum(jumlah)=2.609 cocok; spot-check volume 1664→dekade 1660 benar.

### TODO — P0 (blok Sankey layak pakai)
- ✅ **[DBA][5]** SNK-1 · **SELESAI** — tabel `research_theme_rows` (model + migrasi 007), muat `data/research/korpus_tema_slim.csv` via `backend/seed_research_tema.py` (idempotent by `corpus_id`). Verifikasi: 1005 baris (470 DR + 535 globalise), tema cocok sumber, dekade DR 470/470 (fix #1), 27 null asli, 251 low_conf. Re-run tetap 1005.
- ✅ **[DBA][5]** SNK-2 · **SELESAI (TDD)** — `routers/research.py` `GET /api/research/sankey-tema?year_from=&year_to=` → `{nodes,links}` (reuse `SankeyResponse`), 3-tingkat dekade→tema→pelabuhan, multi-port explode, NULL→"Tak bertahun". Test 6 RED→GREEN; suite in-container **181 pass 0 fail**. Curl nyata: 200, **sum link=5218=2×2609** (cocok agregat terkoreksi), 22ms.
- ✅ **[DBA][3]** SNK-3 · **SELESAI (TDD)** — `GET /api/research/sankey-tema/rows` → `List[ResearchRowOut]` (teks, text_asli, 7 skor, tanggal, sumber, inventaris_ref, low_conf). Filter pelabuhan cocok **keanggotaan token** (bukan substring); limit negatif→422 (SEC-2). Test 6 RED→GREEN; in-container **187 pass 0 fail**. Curl nyata `sengketa+Salido`: 200, 3 baris, membership benar, 26ms.
- ✅ **[DBA][2]** SNK-4 · **SELESAI via SNK-3** — `low_confidence` ada di CSV + response drill-down (`ResearchRowOut`), test `test_drilldown_exposes_low_confidence`.
- ✅ **[DevSecOps][3]** SEC-SNK-1 · **SELESAI** — `.gitignore` blok SEC-SNK-1 (`data/research/raw/`, `*_raw.csv`, `data/**/*.raw`, `*.raw`, `*text_asli*`) + whitelist `!korpus_tema_slim.csv`. Keputusan: slim 3.5MB DI-COMMIT (artefak reproducible, seed bergantung; konsisten konvensi repo — `scrawling/*.json` 30M sudah tracked tanpa lfs), raw 552MB diblokir permanen. Verifikasi: `git check-ignore slim` → exit 1 (trackable), raw/`*_raw.csv`/`text_asli` → ter-ignore; `find data -size +50M` kosong. Catatan: batas ukuran tak bisa lewat gitignore → gate manual `find data -size +50M` sebelum `git add`.
- ✅ **[QA][3]** QA-SNK-1 · **SELESAI** — `backend/tests/test_research_qa_granular.py` **integration test** (pola `sync_engine` real-DB dari `test_atm_p0_us06.py`, bukan mock — 470/470 mustahil dibuktikan via unit mock). 8 test hijau: total=1005, DR=470 (assert 470 eksplisit, sebelumnya nihil di grep), glob=535, null_dekade=27, **DR-dgn-dekade=470/470** (fix#1 backfill), multi-port=481, membership `_split_ports` baris nyata, distinct corpus_id DR=470. Full suite **195 pass** (187+8) / 41 skip / 0 fail.

### TODO — P1 (nice-to-have)
- ✅ **[DBA][5]** SNK-5 · **SELESAI & DEPLOY (lokal)** — halaman Django `GET /riset/tema/` (thesis-only, `noindex`, tak di navbar). Identitas **salido.my.id** (EB Garamond + Space Grotesk, hitam/putih). Sankey inline-SVG dari endpoint baru `GET /api/research/sankey-tema/triples` (agregasi dekade→tema→pelabuhan + meta; 3 unit test), drill-down klik→`/rows` teks penuh. Verifikasi live nginx :8084: page 200, triples 200 (188ms, 512 triples), /rows 200, log bersih, screenshot browser OK. Test: backend **198 pass** (+3 triples), frontend **4 pass** (200/noindex/endpoint/font). **Catatan: baru deploy ke stack lokal, BELUM push production salido.my.id.**
- **[DBA][2]** SNK-6 · Toggle `low_confidence` di UI.
- **[DBA][2]** SNK-7 · Export CSV/JSON lampiran thesis.
- **[DevSecOps][2]** SEC-SNK-2 · Putuskan proteksi akses halaman thesis-only (Open Q#4: noindex/password vs by-obscurity).

### ✅ INVESTIGATE — SELESAI
- **[DBA][3]** DATA-SNK-1 · **Akar masalah:** `text_asli` GLOBALISE = dump OCR MENTAH seluruh inventaris arsip (350KB–4,2MB/baris, 538MB dari 552MB total); daghregister sehat (2,7KB). **Klasifikasi AMAN** — model pakai kolom `text`, bukan `text_asli`. **Fix:** `slim_corpus_for_db.py` → `korpus_tema_slim.csv` (**3,6MB, −99,3%**); `text_asli` GLOBALISE diganti pointer sitasi `inventaris_ref` (NL-HaNA). Muat DB pakai file SLIM ini. Sisa: 1 baris globalise tanpa `inventaris_ref` (edge case, non-blok).

---

## 3. Target & Definition of Done

**Target sprint:** SNK-1..4 + SEC-SNK-1 + QA-SNK-1 selesai → Sankey bisa dirender & diaudit dari data FIXED.

**DoD per item (WAJIB, dari CLAUDE.md):**
1. TDD — test ditulis dulu (RED), lalu implement (GREEN).
2. `docker compose exec backend pytest` hijau.
3. Endpoint diverifikasi `curl` nyata (bukan asumsi).
4. QA sign-off: **row-count granular** — 1.005 baris masuk, 470/470 daghregister terwakili, tidak ada drop diam-diam (pelajaran `feedback_sisir_semua_titik_pemakaian`).
5. DevSecOps: tidak ada artefak besar/secret ter-commit; `docker compose logs backend` bersih.

---

## 4. Workflow (swim-lane, urutan dependency)

```
 MLOps ──[✅ fix agregat]──► sankey_tema_agregat_fixed.csv
                                     │
                                     ▼
 DBA ──[SNK-1 muat DB]──► [SNK-2 endpoint sankey]──► [SNK-3 drill-down]──► [SNK-4 low_conf]
                                     │                                          │
 DevSecOps ──[SEC-SNK-1 gitignore 552MB]──(gate)──────────────────────────────┤
                                                                                ▼
 QA ──[QA-SNK-1 pytest + verifikasi granular]──(veto)──► RILIS exhibit Bab 3
                                                                                │
 P1 (opsional) ─────────────────────────────► UI /research/tema (SNK-5..7)
```

**Aturan main:** tidak ada item pindah ke "Done" tanpa QA sign-off. DevSecOps gate sebelum `git add`. P2 (Sankey Huygens "Perdagangan Klasik") tetap DITUNDA sampai P0 sprint ini kelar (PRD §P2).
