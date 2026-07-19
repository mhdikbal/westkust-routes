# PRD: Model & Promosi Data `port_tally_aggregate`

**Status:** P0 + P1.2 SELESAI (2026-07-07) — 98 baris `port_arrival_tallies` live, stat tampil di halaman Fort
**Disusun:** 2026-07-07
**Tim:** DBA (skema) + Tim Data (parsing) — Scrum Master: Muhammad Ikbal
**Melengkapi:** `docs/prd/prd-cleaning-daghregister-1660-1669.md` (P0.3 — keputusan "staging dulu" sudah dikunci di sana; PRD ini menjawab pertanyaan yang sengaja ditunda: **bentuk tabel promosi akhirnya apa**)

---

## 1. Latar Belakang

`docs/thesis/dr/daghregister_corpus.csv` punya 12 baris `record_type=port_tally_aggregate` (dari 511 total) — sudah masuk `staging_extractions` (`confidence_flag=unverified`), tapi TIDAK punya jalur promosi lebih lanjut. Bentuknya secara struktural tidak cocok dengan `Voyage`:

```
31 Maret, 7 dari Palembang, dengan 59 orang, 1627 pikol, 70 catty lada, 460 cadjang;
1 dari Ticco, dengan 15 orang, 77 pikol, 80 catty lada, 40 matjes, 4 pot minyak, 20 pikol benjol;
5 dari Priaman, dengan 34 orang, 1 last beras, 50 pot minyak, 159 pikol, 65 catty lada, ...;
1 dari Bencalis, dengan 10 orang, 210 cadjang, 2700 ikan kering...
```

Satu baris korpus = **satu rekap bulanan**, berisi **rata-rata 9 kelompok-pelabuhan-asal** (dihitung empiris: 12 baris → ~109 segmen "N dari [Tempat], dengan M orang"), masing-masing dengan jumlah kapal-tak-bernama + kargo agregat. `Voyage.ship_name` `nullable=False` — tidak ada nama kapal di sini sama sekali, cuma hitungan.

**Kenapa ini penting, bukan cuma diabaikan:** 109 kelompok-pelabuhan-asal itu justru **volume data lebih besar** dari 108 `single_voyage` yang sudah kita promosikan ke staging — membuang tipe ini berarti membuang mayoritas sinyal kuantitatif dari Dagh-register (berapa banyak kapal per pelabuhan per bulan), bukan cuma catatan sampingan.

## 2. Keputusan Desain

**Tabel baru: `port_arrival_tallies`** — BUKAN baris `voyages` per kapal-tak-bernama (sudah diputuskan di PRD sebelumnya, dikonfirmasi lagi di sini). Satu baris `staging_extractions` (`record_type=port_tally_aggregate`) **di-expand jadi banyak baris** `port_arrival_tallies` (satu per kelompok-pelabuhan-asal) saat promosi — 1-ke-N, bukan 1-ke-1 seperti `single_voyage`→`voyages`.

```python
class PortArrivalTally(Base):
    __tablename__ = "port_arrival_tallies"

    id = Column(Integer, primary_key=True, index=True)
    staging_extraction_id = Column(Integer, ForeignKey("staging_extractions.id"), nullable=False, index=True)
    volume = Column(String(100), nullable=False)              # jilid sumber
    tanggal_perkiraan = Column(String(50), nullable=True)      # teks tanggal asli, belum dinormalisasi ISO

    origin_port_raw = Column(String(100), nullable=False)      # nama pelabuhan asal apa adanya di teks, mis. "Palembang"
    origin_fort_id = Column(Integer, ForeignKey("forts.id"), nullable=True)  # diisi via NAME_MAPPING kalau match

    ship_count = Column(Integer, nullable=True)                # "7 dari..." -> 7
    person_count = Column(Integer, nullable=True)              # "dengan 59 orang" -> 59

    cargo_text = Column(Text, nullable=False)                  # segmen teks mentah utk grup ini
    cargo_items_json = Column(JSONB, nullable=True)            # best-effort parse (pola sama extract_data_perdagangan.py)

    confidence_flag = Column(String(20), nullable=False, server_default="unverified")  # sama siklus staging_extractions
    created_at = Column(String(30), nullable=False)
```

**Kenapa `origin_port_raw` bukan ForeignKey wajib**: banyak nama pelabuhan di tally (Bencalis, Baly, Gilly, Passir, Serebon, Craoan, Bantam) ada di LUAR 10 pelabuhan pantai barat yang kita punya sbg `Fort` — Dagh-register mencatat SEMUA kedatangan VOC-wide, bukan cuma pantai barat Sumatra. `origin_fort_id` nullable, diisi lewat `NAME_MAPPING` (`backend/seed_data.py`) kalau cocok, `null` kalau bukan salah satu dari 10 pelabuhan target (tetap disimpan, cuma tidak terhubung ke peta pantai-barat).

## 3. Cakupan / Non-Goals

- **BUKAN** ditampilkan sbg rute di peta (garis asal→tujuan) — tidak ada "kapal" individual utk digambar sbg polyline. Bentuk visualisasi (kalau ada) adalah pertanyaan terpisah (lihat §6 Open Questions, kaitkan ke `docs/brainstorm-globalise-data-modeling.md` ide #3 "heatmap densitas-sebutan").
- **BUKAN** menjanjikan cargo_items_json 100% ter-parse — pola regex yang sama dgn `extract_data_perdagangan.py`/`cargo_sanity_check.py`, keterbatasan yang sama (bahasa prosa bervariasi).
- **TIDAK** mengubah `docs/prd/prd-cleaning-daghregister-1660-1669.md` P0.3 — keputusan "staging dulu" tetap, PRD ini cuma menjawab "lalu apa setelah staging".

## 4. Requirements

### P0 — Wajib

**P0.1 — Migration + model `PortArrivalTally`** ✅ **SELESAI (2026-07-07)**
- `backend/alembic/versions/005_add_port_arrival_tallies.py` + model di `models.py`.
- Catatan: tabel ter-create otomatis via `Base.metadata.create_all()` di seed_data.py startup (sebelum migration manual sempat jalan) — pola yg sama seperti migration 003 sebelumnya di project ini. Diselesaikan dgn `alembic stamp head`, bukan re-run create_table.
- Acceptance terpenuhi: `alembic current` → `005 (head)`.

**P0.2 — Script parsing + promosi (`staging_extractions` → `port_arrival_tallies`)** ✅ **SELESAI**
- `docs/thesis/dr/promote_port_tallies.py` — jalan di dalam container backend (`docker compose cp` + `exec`), krn `db` tidak expose port ke host.
- Hasil: **11 baris staging → 98 baris `port_arrival_tallies`** (rata-rata ~9 segmen/baris, sesuai estimasi §5). `origin_fort_id` ter-resolve **9/98** (mayoritas origin di luar 10 pelabuhan pantai-barat — Palembang, Bencalis, Baly, dst, sesuai dugaan §2). `cargo_items_json` terisi **79/98**.
- Idempotent-retry diverifikasi (jalan 2x, ke-2 kalinya 0 baris baru).

**P0.3 — `confidence_flag` tetap `unverified` sampai direview**
- Sama siklus dgn `staging_extractions` — TIDAK otomatis "promoted" atau tampil publik. Endpoint review (kalau dibuat) mengikuti pola `PATCH` yang sudah ada di `staging.py`.

### P1 — Nice-to-have

**P1.1 — Endpoint API baca `port_arrival_tallies`**
- `GET /api/staging/tallies?origin_fort_id=&confidence_flag=` — mirip `GET /api/staging/extractions`, paginated.

**P1.2 — Stat tambahan di halaman detail Fort** ✅ **SELESAI (2026-07-07)**
- Keputusan gerbang tampil: **tampil sekarang** dgn label jelas "belum diverifikasi" (bukan tunggu direview manual — belum ada UI review utk tabel ini, jadi opsi itu berarti stat kosong).
- `FortEnrichmentResponse` diperluas dgn `tally_ship_count`/`tally_person_count` (COALESCE ke 0, exclude `confidence_flag='rejected'`). 2 test backend baru (RED→GREEN).
- Frontend: section baru "Kedatangan Tercatat (Dagh-register)" di `port_detail.html`, terpisah visual dari "Statistik Pelayaran" (BGB), dgn caveat italic eksplisit — hanya render kalau `tally_ship_count > 0` (Barus dkk yg tidak ada data tally tidak menampilkan section kosong). 2 test Django baru.
- Diverifikasi: curl (`Padang: 6 kapal/39 orang`, `Barus: 0`, section hidden) + screenshot Playwright.

### P2 — Future considerations

- Heatmap/dashboard terpisah — tidak dipilih user, disimpan sbg opsi kalau nanti mau diperluas.
- Normalisasi `tanggal_perkiraan` jadi ISO date sungguhan (sekarang masih teks apa adanya, sama seperti `staging_extractions`).

## 5. Catatan Data (penting, dicek sebelum implementasi)

- Push sesi sebelumnya (`push_to_staging.py`) mengirim **11** baris `port_tally_aggregate` ke staging (dari 12 total di korpus) — 1 baris ter-exclude krn punya `duplicate_of` terisi (P0.2 dedup). Konsisten, bukan bug.
- Estimasi ekspansi: 11 baris staging × ~9 segmen/baris ≈ **~100 baris** `port_arrival_tallies` — bukan jumlah besar, aman utk satu kali migration+backfill run.

## 6. Open Questions

1. **(User)** Visualisasi `port_arrival_tallies` di aplikasi — heatmap densitas per pelabuhan/bulan (ide #3 brainstorm), stat tambahan di halaman detail Fort ("X kapal tercatat datang bulan Maret 1661"), atau tidak divisualisasikan sama sekali (cuma bahan riset thesis)? Menentukan prioritas P1.2/P2.
2. **(DBA)** `origin_port_raw` yang TIDAK match 10 Fort pantai-barat (Bencalis, Baly, Gilly, Passir, Serebon, Craoan, Bantam, dll — mayoritas VOC-wide, bukan pantai barat) — tetap disimpan (utk kelengkapan historis/thesis) atau di-filter keluar saat promosi (cuma simpan yg relevan pantai barat)? Rekomendasi: tetap simpan (harga penyimpanan murah, buang data historis lebih mahal utk dipulihkan nanti), tapi ini keputusan user.
3. **(Data)** Kualitas parsing `cargo_items_json` utk tally belum pernah divalidasi manual (beda dari `extract_data_perdagangan.py` yg sudah tervalidasi via P0.5 cross-check) — perlu sample-review sebelum dipakai sbg dasar klaim kuantitatif di thesis?
   **⏳ Workflow validasi dibangun (2026-07-07), review manual belum selesai:**
   - Glosarium (`commodity_glossary`, 201 istilah Belanda) diperluas dgn 10 varian Indonesia (`variants` array, via `UPDATE` langsung — **catatan: data glosarium tidak punya file sumber di repo**, cuma hidup di DB lokal, beda dari tabel lain yg selalu ada seed script; risiko hilang kalau volume DB di-reset, technical debt terpisah dari PRD ini): beras→rijst, lada→peper, garam→zout, benjol/benzoe→benzoin, asam/asam jawa/tamarin/tamarinda/tamberyn→tamarinde, timah→tin, gandum→tarwe, warna biru→indigo, kamper borneo→kamfer, lilin→was.
   - Dari **62 istilah produk unik** hasil parsing (98 baris, 79 punya ≥1 item), **17 kini cocok glosarium** (27%) — sisanya (gula generik+variannya, padi, pinang tua, bawang, kacang-kacangan, tembakau, kapuk, cassumba, produk daging/ikan, dll) TIDAK ditambahkan variant baru krn tidak ada padanan Belanda yg jelas di 201 entri existing — **sengaja dibiarkan tak-cocok** (flag jelas), bukan ditebak.
   - **Satuan ukur ditambahkan (2026-07-07)** — `commodity_glossary` sebelumnya 100% produk, TIDAK ADA satuan (pikol/kati/bahar/last/dll) sama sekali. User menunjukkan sumber otoritatif: *VOC-Glossarium* (Instituut voor Nederlandse Geschiedenis, 2000), diekstrak penuh via PyMuPDF (128 halaman, WebFetch gagal baca PDF terenkode, fitz berhasil). 6 entri baru `category='satuan'` ditambahkan dgn definisi terverifikasi dari sumber itu (bukan tebakan): **pikol** (~125 pon/61,75kg, dibagi 100 kati; variasi regional Batavia/Tayouan ~122 pon), **kati** (1/100 pikol ≈600g, varian ejaan "catty" dikonfirmasi ada di sumber), **bahar** (~500 pon rempah, nilai beda per wilayah — Maluku 550-625 pon, Jawa 220 pon, Arab 393¾ pon), **last** (1 last = 20 pikol ≈1.250kg), **taël** (asal Tionghoa, 1 kati = 16 taël), **pon** (pon Amsterdam = 0,494 kg persis). Bonus temuan: entri "kamfer baros" di sumber asli menyebut eksplisit "eerste kwaliteit kamfer. Afkomstig van Baros" (kamper kualitas pertama, dari Barus) — konfirmasi independen relevansi Barus utk kamper VOC.
   - Alat review (HTML interaktif, localStorage, self-contained): 98 kartu (asal+fort, jumlah kapal/orang, teks kargo mentah), tiap item kargo tampil dgn **dua tooltip terpisah** — nama produk (label Belanda kalau cocok glosarium, tooltip definisi Indonesia) DAN satuan ukur (sama, terpisah, underline titik-titik kalau ada definisi). Tombol ✓ Wajar/⚑ Tandai/✕ Tolak per baris, filter "ada istilah tak dikenal" (cek produk MAUPUN satuan)/"belum ditandai", pencarian teks bebas.
   - **Keputusan user (2026-07-07): review manual DILEWATI, tidak dianggap perlu sekarang.** Open Question #3 ditutup dgn keputusan ini — bukan krn selesai direview, tapi krn user menilai tidak perlu di titik ini. Alasan ini aman: stat di halaman Fort (P1.2) cuma tampilkan `ship_count`/`person_count` (parsing regex terpisah, sudah divalidasi tak langsung via P0.3-P0.5), BUKAN isi `cargo_items_json` itu sendiri — jadi melewati validasi cargo tidak mempengaruhi fitur yg sudah live. Kalau nanti `cargo_items_json` mau dipakai utk klaim kuantitatif spesifik di thesis, validasi manual (alat sudah ada, link tersimpan di memory) baru wajib dilakukan saat itu.
   - **Technical debt DIBERESKAN (2026-07-07)**: kolom `source_citation` (Text, nullable) ditambahkan ke `commodity_glossary` (migration `006_add_glossary_source_citation.py`). 6 entri satuan diisi eksplisit rujuk VOC-Glossarium (IHNG, 2000) + URL; **201 entri lama TETAP NULL** (asal tak tercatat, sengaja tidak ditebak). `GET /api/glossary` dan `GET /api/glossary/lookup` kini expose field ini. 3 test baru (`test_glossary.py`, file test glosarium pertama di project — sebelumnya endpoint ini 0% tercakup test). 174 backend test total, semua pass.

## 7. Success Metrics

- **Leading**: 100% dari 11 baris staging `port_tally_aggregate` berhasil di-parse jadi ≥1 baris `port_arrival_tallies` (tidak ada yang silently ke-skip krn gagal parse total).
- **Leading**: laporan eksplisit % `origin_fort_id` ter-resolve (jangan diasumsikan tinggi — banyak origin di luar 10 pelabuhan target).
- **Lagging**: kalau dipakai sbg exhibit thesis (Bab 3/4), tidak ada baris `port_arrival_tallies` yg terbukti salah parse saat sample-review manual (Open Question #3).

## 8. Timeline

Tidak ada deadline eksternal. Dependency: tidak ada — 11 baris sumber sudah di staging (P0 selesai per `docs/prd/prd-cleaning-daghregister-1660-1669.md`), PRD ini bisa dieksekusi kapan saja begitu Open Question #1/#2 dijawab user.
