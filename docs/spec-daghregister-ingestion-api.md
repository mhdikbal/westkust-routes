# Spec: API Ingesti Data Hasil Pemrosesan Colab (Daghregister/GLOBALISE)

**Status:** Draft spec — belum diimplementasikan
**Disusun:** 2026-07-06
**Melengkapi:** `docs/prd-daghregister-voyage-data.md`
**Constraint kunci:** server production (`salido.my.id`, 2GB RAM / 32GB disk) HANYA menjalankan API ringan (terima+simpan hasil) — semua pemrosesan berat (OCR, keyword-scan skala besar, panggilan LLM) tetap di Colab.

---

## Problem Statement

Pipeline riset (notebook Colab: `daghregister_extraction.ipynb`, calon notebook GLOBALISE) menghasilkan data terstruktur (CSV/JSON) di luar server production. Saat ini, satu-satunya cara data itu masuk ke database westkust-routes adalah manual (download dari Colab, lalu proses lokal). Dibutuhkan endpoint API supaya Colab bisa **push** hasil langsung ke server, dan supaya proses ini bisa diulang untuk sumber baru (GLOBALISE, scraping lain) tanpa menulis endpoint baru tiap kali.

## Goals

1. Colab dapat mengirim batch hasil ekstraksi (voyage/teks/skor model) langsung ke server via satu endpoint generik, tanpa perlu akses SSH manual
2. Data masuk sebagai staging (`confidence_flag=unverified`) — tidak otomatis mencemari tabel `voyages` production (lihat keputusan desain PRD sebelumnya)
3. Endpoint idempotent — Colab bisa retry/resume tanpa duplikasi baris
4. Tidak membebani server 2GB RAM — endpoint hanya menyimpan payload, tidak memproses/menghitung apa pun secara berat di sisi server

## Non-Goals

1. **Server TIDAK melakukan OCR, scraping, atau panggilan LLM** — itu tetap kerja Colab. Kalau ke depan ada kebutuhan pemrosesan server-side, itu spec terpisah dengan pertimbangan kapasitas server dulu (kemungkinan perlu upgrade VPS).
2. **Bukan endpoint publik untuk pengguna aplikasi peta** — ini endpoint internal (butuh API key), dipakai notebook Colab kamu sendiri, bukan untuk pihak ketiga.
3. **Tidak menangani upload file besar (PDF, ZIP arsip)** — endpoint ini hanya menerima JSON hasil ekstraksi yang sudah diproses (kilobyte-megabyte per batch), bukan file mentah ratusan MB.
4. **Belum termasuk dashboard review manual** — endpoint `PATCH` untuk ubah `confidence_flag` ke `reviewed`/`promoted` disediakan, tapi UI/dashboard untuk itu di luar scope spec ini (lihat Open Questions).

## User Stories

- Sebagai peneliti yang menjalankan notebook Colab, saya ingin mengirim hasil scan+terjemahan langsung ke server lewat satu panggilan API, supaya tidak perlu download-lalu-upload manual.
- Sebagai peneliti, saya ingin proses kirim data ini aman diulang (retry) kalau koneksi Colab putus di tengah, tanpa data terduplikasi.
- Sebagai peneliti, saya ingin bisa menandai record staging tertentu sebagai "sudah saya review dan valid" lewat API yang sama, supaya proses promosi ke tabel `voyages` resmi bisa dijalankan terpisah.
- Sebagai admin sistem, saya ingin endpoint ini butuh API key (bukan terbuka publik), supaya tidak disalahgunakan pihak lain.

## Requirements

### Must-Have (P0)

**P0.1 — `POST /api/staging/extractions`** — terima batch hasil ekstraksi generik
```json
{
  "source": "daghregister_batavia" | "globalise_obp" | lainnya (string bebas, bukan enum tertutup),
  "batch_id": "uuid-v4-dibuat-colab",  // untuk idempotency
  "items": [
    {
      "external_ref": "volume:1664|page:57",  // pengenal unik dari sisi sumber, dipakai cek duplikasi
      "text_indonesia": "...",
      "text_asli": "...",
      "metadata": { "tanggal_perkiraan": "...", "matched_terms": [...], ... }  // JSONB bebas, skema beda per sumber
    }
  ]
}
```
- Acceptance: kalau `external_ref` sudah ada utk `source` yang sama, item itu di-skip (bukan error, bukan duplikat) — supaya retry aman
- Acceptance: respons berisi jumlah `inserted` vs `skipped_duplicate` per batch
- Butuh header `X-API-Key` — request tanpa/salah key ditolak 401

**P0.2 — `GET /api/staging/extractions?source=...&confidence_flag=...`** — daftar record staging untuk direview manual
- Filter minimal: `source`, `confidence_flag` (unverified/reviewed/promoted/rejected)
- Paginasi wajib (default 50, max 200 per halaman) — jangan `SELECT *` tanpa batas ke tabel yang bisa berisi ratusan ribu baris (GLOBALISE)

**P0.3 — `PATCH /api/staging/extractions/{id}`** — update status review manual
```json
{ "confidence_flag": "reviewed", "reviewed_by": "muhammad.ikbal" }
```
- Acceptance: hanya bisa ubah `confidence_flag` dan `reviewed_by`/`reviewed_at` — tidak bisa ubah `text_indonesia`/`text_asli` lewat endpoint ini (kalau perlu koreksi teks, itu kasus terpisah, bukan bagian P0)

### Nice-to-Have (P1)

- **P1.1** — `POST /api/staging/promote/{id}` — otomatis pindahkan 1 record `reviewed` jadi baris resmi di `voyages`/`cargo_items` (saat ini di PRD masih manual). Ditunda ke P1 karena butuh mapping field yang lebih matang dulu (banyak field Daghregister/GLOBALISE tidak match langsung ke skema `Voyage`).
- **P1.2** — Rate limit sederhana per API key (mis. 100 request/menit) supaya kalau ada bug retry-loop di Colab, tidak membanjiri server 2GB RAM itu sendiri.

### Future Considerations (P2)

- Endpoint publik read-only untuk menampilkan record `promoted` di peta (setelah UI/legend beda-provenance diputuskan — lihat pertanyaan terbuka PRD sebelumnya)
- Webhook/notifikasi kalau ada batch masuk (mis. ping Slack/email) — tidak perlu sekarang, notebook Colab masih dijalankan manual oleh kamu sendiri

## Model Tabel Pendukung (ringkasan, detail penuh di PRD)

Satu tabel generik `staging_extractions` (bukan tabel per-sumber) supaya P0.1 bisa dipakai ulang untuk GLOBALISE nanti tanpa migrasi skema baru:

```python
class StagingExtraction(Base):
    __tablename__ = "staging_extractions"
    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False, index=True)
    external_ref = Column(String(200), nullable=False)
    batch_id = Column(String(36), nullable=True, index=True)
    text_indonesia = Column(Text, nullable=False)
    text_asli = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    confidence_flag = Column(String(20), nullable=False, default="unverified")
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(String(30), nullable=True)
    created_at = Column(String(30), nullable=False)

    __table_args__ = (
        Index("ix_staging_source_ref", "source", "external_ref", unique=True),  # kunci idempotency
    )
```

## Success Metrics

- Leading: 100% batch dari notebook Colab berhasil masuk tanpa duplikasi saat di-retry (uji manual: kirim batch sama 2x, cek `skipped_duplicate` = jumlah item)
- Lagging: waktu dari "notebook selesai jalan" sampai "data siap direview" turun dari proses manual (download-upload) ke satu panggilan API

## Test Plan (TDD wajib, CLAUDE.md)

1. `backend/tests/test_staging_extractions.py`:
   - POST batch baru → 201, `inserted` sesuai jumlah item
   - POST batch sama persis (retry) → `skipped_duplicate` = jumlah item, `inserted` = 0
   - POST tanpa API key → 401
   - GET dengan filter `source`+`confidence_flag` → hanya baris yang cocok
   - GET tanpa paginasi eksplisit → default 50 baris, bukan semua
   - PATCH ubah `confidence_flag` ke nilai di luar 4 pilihan valid → 422

## Open Questions

1. **(Engineering)** API key generik untuk semua notebook, atau per-notebook (daghregister vs globalise beda key)? Mempengaruhi cara audit siapa yang push data apa.
2. **(User)** `metadata_json` per sumber akan beda struktur (Daghregister: `matched_terms`+`tanggal_perkiraan`; GLOBALISE: mungkin field lain) — perlu skema JSONB per-`source` didokumentasikan di mana? (usul: satu file `docs/staging-metadata-schemas.md`, diupdate tiap kali sumber baru ditambah)
3. **(User)** Endpoint ini dibuat sekarang (P0.1-3) sebelum GLOBALISE mulai diproses, atau setelah? Kalau GLOBALISE prioritas duluan, endpoint bisa nyusul — Colab tetap bisa simpan ke CSV dulu, push belakangan.
