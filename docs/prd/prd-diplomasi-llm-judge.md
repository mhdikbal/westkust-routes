# PRD — Label `diplomasi` via LLM-Judge (Cascade)

**Status:** Planning (MLOps) — 2026-07-09 · **Menggantikan** pendekatan zero-shot untuk label `diplomasi`
**Tim (role framing):** MLOps, DBA — Muhammad Ikbal
**Konteks:** lanjutan network-graph (`docs/prd/prd-network-graph-aktor-tema.md`). Zero-shot untuk `diplomasi` **GAGAL gerbang validasi** (over-fire 63% baris ≥0.5; presisi top-20 ≈10-20%: daftar kargo/register/laporan perang skor 1.00). Akar: mDeBERTa tak bisa bedakan **BENTUK** surat resmi dari **ISI** diplomatik. Keputusan: **Opsi 2 — LLM-judge**.

---

## 0. Ringkasan keputusan
- **Metode:** LLM-judge per-baris (ya/tidak + confidence + **alasan**), bukan zero-shot NLI.
- **Pola:** **CASCADE** — run zero-shot yang sudah ada dipakai sebagai **jaring recall** (630 kandidat skor≥0.5), LLM hanya menilai kandidat itu untuk **presisi**. Run Colab lama TAK sia-sia.
- **Compute:** **0 GPU.** ~630 teks pendek via API ≈ $1-3. (Menegaskan: yang mahal = akurasi, bukan compute.)
- **Additive:** hasil = kolom baru, `tema_dominan`/Sankey live **tidak disentuh**.

## 1. Problem
`diplomasi` memotong-silang tema existing (probe: nyangkut di syahbandar 103/pelayaran 53/sengketa 29) → butuh label sendiri, tapi zero-shot gagal (lihat konteks). Diplomasi **nyata ada** (surat Sultan Aceh→Gouverneur-Generaal) tapi tenggelam di false-positive. Butuh metode yang paham **nuansa isi vs bentuk** + **auditable** (untuk sidang thesis: "kenapa baris ini diplomasi?").

## 2. Pendekatan — Cascade retrieve-then-rerank

```
[Tier 0 — RECALL, sudah ada]  zero-shot skor_diplomasi ≥ 0.5  →  ~630 kandidat
                                        │  (baris < 0.5 diasumsikan non-diplomasi — DIVALIDASI, §4)
                                        ▼
[Tier 1 — PRESISI, baru]      LLM-judge tiap kandidat  →  {ya/tidak, confidence, alasan}
                                        ▼
                              skor_diplomasi_final (0/1 atau confidence) + alasan
```

Ambang kandidat 0.5 dipilih karena zero-shot **over-fire = recall tinggi** (jarang MISS diplomasi sejati). Bila validasi recall (§4) menemukan diplomasi ter-lewat di skor<0.5, turunkan ambang ke 0.4/0.3.

## 3. Desain teknis LLM-judge

### 3.1 Input
Kolom `text` (terjemahan Indonesia, potong ~1.500 char). BUKAN `text_asli` (bisa 4MB OCR mentah — irrelevan & mahal).

### 3.2 Rubrik (system/instruction)
> Nilai apakah teks INI **terutama** tentang **hubungan/aksi diplomatik antar penguasa atau negeri**: perundingan, perjanjian/kontrak politik, pengiriman/penerimaan **utusan resmi**, sumpah setia/aliansi, atau upaya perdamaian.
> **BUKAN diplomasi** (jawab tidak): daftar kargo/muatan, laporan perang murni tanpa perundingan, register/daftar dokumen, perkara hukum perdata/pidana, instruksi administratif rutin, surat dagang biasa.
> Fokus pada **ISI**, bukan sekadar bentuk surat resmi.
> Keluarkan JSON: `{"diplomasi": true|false, "confidence": 0.0-1.0, "alasan": "<=15 kata"}`.

### 3.3 Few-shot (dari FALSE-POSITIVE nyata run gagal — ini kekuatannya)
| Cuplikan | Label benar |
|---|---|
| "…000 potong kain linen guinee; 5090 bafta; siouters…" | `false` (daftar kargo) |
| "…dari Songeytrap dengan 12 benteng sedang berperang…" | `false` (laporan perang) |
| "Daftar semua kertas-kertas… diterima dari Bassoura…" | `false` (register dokumen) |
| "Proses perdata dalam perkara mendiang…" | `false` (perkara hukum) |
| "Surat dari Sultan Nulma Alam, memerintah negeri Achin, kepada Gouverneur Generaal Joan Maetsuyker…" | `true` (surat antar penguasa) |
| "…menghadap Sultan Indrapoura untuk perundingan damai…" | `true` (perundingan) |

### 3.4 Output tersimpan per baris
`is_diplomasi` (bool) · `conf_diplomasi` (0-1) · `alasan_diplomasi` (teks pendek, audit).

### 3.5 Robustness
- Retry + JSON-parse guard (kalau LLM tak balas JSON valid → retry 1×, lalu tandai `null`/manual).
- Batching + rate-limit aware. Idempotent (simpan per `corpus_id`, bisa resume).

## 4. Gerbang validasi (WAJIB sebelum integrasi) — 2 arah
1. **Presisi:** spot-check 30 baris `is_diplomasi=true` acak → manusia setuju? target **≥0.8**.
2. **Recall (validasi asumsi cascade):** spot-check 20 baris **NON-kandidat** (skor_diplomasi<0.5) → pastikan tak ada diplomasi sejati yang ter-lewat. Bila ada → turunkan ambang kandidat, ulang.
- Hanya lolos KEDUA → boleh integrasi. (Pelajaran [[feedback_verify_entity_extraction_before_trusting]]: gagal 3× tidak boleh.)

## 5. Skema & integrasi (0 GPU, DBA)
1. **Migrasi 008:** `ALTER TABLE research_theme_rows ADD COLUMN is_diplomasi bool, conf_diplomasi float, alasan_diplomasi text` (+ opsional `skor_diplomasi_raw` dari zero-shot sbg provenance).
2. **Merge:** hasil LLM (key `corpus_id`) → regenerasi `korpus_tema_slim.csv` (+ kolom baru). File 552MB TIDAK dipakai (hanya `corpus_id`+skor yang diambil).
3. **Re-seed** `seed_research_tema.py` (idempotent by corpus_id) — tambah handling kolom baru + invalidate cache.
4. **Network graph:** edge-type `diplomasi` = `is_diplomasi=true` (independen dari tema perang/dagang/administrasi yang diturunkan dari `tema_dominan`).

## 6. Model & environment
- **LLM-agnostik** (antarmuka OpenAI-compatible) supaya bebas colok: Claude API / Gemini / lokal.
- Jalan di **Colab atau lokal** (CPU/API — TIDAK butuh GPU). Colab tetap dipakai kalau nyaman (secret API key di Colab).
- **OPEN:** model mana yang tersedia untuk Ikbal di lingkungan itu? → menentukan client di script. (Default siapkan generic OpenAI-compatible + varian Claude.)

## 7. Risiko & mitigasi
| Risiko | Mitigasi |
|---|---|
| LLM tetap over/under-fire | few-shot dari false-positive nyata + rubrik "isi bukan bentuk" + gerbang presisi |
| Diplomasi ter-lewat di skor<0.5 (recall) | validasi recall §4; turunkan ambang bila perlu |
| Teks terjemahan bias/ambigu | LLM diberi `text` Indonesia; bila ragu, bisa sertakan `tema_dominan` sbg konteks |
| Biaya membengkak | cascade (judge 630, bukan 1005); truncate 1500 char; model murah cukup |
| Non-determinisme | temperature=0; simpan alasan utk audit; idempotent by corpus_id |

## 8. Langkah eksekusi
| # | Langkah | Siapa | Compute |
|---|---|---|---|
| 1 | Script LLM-judge (cascade, rubrik, few-shot, JSON-guard, resume) | **Saya** | — |
| 2 | Sediakan API key + pilih model; jalankan script (630 kandidat) | Ikbal | API/CPU |
| 3 | **Gerbang validasi 2-arah** (presisi 30 + recall 20) | Ikbal + saya | — |
| 4 | Lolos → migrasi 008 + regen slim + re-seed + deploy | Saya (+VPS: Ikbal) | 0 GPU |
| 5 | Integrasi ke network-graph edge-type diplomasi | Saya | 0 GPU |

**Gate keras:** langkah 4 hanya setelah langkah 3 lolos. Tak lolos → revisi rubrik/few-shot, ulang dari langkah 2.

## 9. Open Questions
1. Model LLM yang tersedia (Claude/Gemini/lokal)? → bentuk client.
2. Output diplomasi: **boolean** (edge ada/tidak) cukup, atau butuh **confidence berskala** untuk tebal-tipis edge?
3. `aliansi` — label terpisah, atau dilebur ke `diplomasi` (aliansi ⊂ diplomasi)? (zero-shot aliansi juga meragukan; sarankan lebur dulu.)
