# PRD: Integrasi Data Pelayaran Abad 17 dari Daghregister Batavia

**Status:** Staging SELESAI (via `staging_extractions` generik, §3.1 di bawah SUDAH DIGANTI — lihat §7). **Promosi 12 baris `single_voyage` DIBATALKAN/ROLLBACK (2026-07-07)** — verifikasi manual thd teks asli menemukan 0/12 valid (lihat §7.1). Jalur promosi `single_voyage` → `voyages` ditutup sampai ada metode ekstraksi nama-kapal+arah yang lebih andal; `port_arrival_tallies` (jalur terpisah, docs/prd-port-tally-aggregate.md) TIDAK terdampak.
**Disusun:** 2026-07-06
**Konteks:** turunan riset thesis (`docs/thesis/chapter-plan-sia-kualitatif-kritis.md`), tapi ini spec level aplikasi westkust-routes, bukan dokumen akademik

---

## 1. Latar Belakang

Sumber data pelayaran VOC yang sudah ada di westkust-routes (`scrawling/Data_BGS_Sumatra_Full.json`, 4.700+ record) berasal dari database terstruktur Huygens KNAW (Bookhouder-Generaal Batavia/BGB) — setiap field (kapal, kargo, nilai gulden) sudah bersih sejak sumbernya.

Selama sesi riset thesis, 13 jilid *Dagh-register gehouden int Casteel Batavia* (1661-1681) diproses lewat notebook Colab (`docs/thesis/colab/daghregister_extraction.ipynb`): scan kata kunci → verifikasi + terjemahan via LLM (sumopod/GPT). Hasilnya, `docs/thesis/dr/daghregister_corpus.csv`, berisi 282 entri naratif (bukan tabel terstruktur) yang di antaranya menyinggung pelayaran dengan detail kapal/kargo/nilai — tapi diekstrak dari teks bebas oleh LLM dan regex, bukan dari database yang sudah terstruktur.

**Pertanyaan produk:** apakah dan bagaimana data ini masuk ke aplikasi westkust-routes, mengingat provenance dan tingkat kepercayaannya berbeda jauh dari data BGB yang sudah ada?

## 2. Temuan Kualitas Data (Wajib Dibaca Sebelum Desain)

| Aspek | Kondisi |
|---|---|
| Cakupan jilid | 6 dari 13 jilid (1661, 1663, 1664, 1665, 1666-1667, 1668-1669) — **7 jilid (1670-1671, 1676-1681) tidak punya lapisan OCR sama sekali**, perlu OCR ulang sebelum bisa diproses |
| Total entri terverifikasi | 282 (dari scan awal, sudah difilter relevansi + diterjemahkan) |
| Entri yang terlihat sbg catatan pelayaran (kapal+kargo) | 119 dari 282 (42%) |
| Ekstraksi nama kapal otomatis (regex) | 38 dari 119 (32%) — sisanya perlu ekstraksi manual/LLM tambahan |
| Ekstraksi nilai gulden otomatis (regex) | 66 dari 119 (55%) |
| Arah pelayaran eksplisit dalam teks | 49 dari 119 (32 keluar dari Sumatra, 17 ke Sumatra); 70 entri tidak eksplisit |
| Struktur kargo | Teks bebas per entri, TIDAK ternormalisasi jadi item per baris seperti `CargoItem` yang ada |
| Tingkat kepercayaan | Ekstraksi LLM (`gpt-5` via sumopod) — belum divalidasi manusia sama sekali (berbeda dari korpus VOC utama yang sudah lewat validasi kappa manual) |

**Kesimpulan kualitas:** data ini *jauh* lebih mentah dari `Data_BGS_Sumatra_Full.json`. Memaksakannya langsung ke tabel `voyages` production tanpa lapisan validasi akan mencemari data yang sudah bersih dengan record yang confidence-nya tidak diketahui.

## 3. Keputusan Desain

**TIDAK menggabungkan langsung ke tabel `voyages`/`cargo_items` production.** Sebagai gantinya, diusulkan model staging terpisah, mengikuti pola arsitektur yang sudah ada (JSON sumber → `seed_data.py` → DB — lihat CLAUDE.md "Data Historis").

### 3.1 Tabel Baru: `daghregister_voyages` (staging) — ⚠️ SUPERSEDED, lihat §7

**Tidak dibangun seperti ini.** Implementasi aktual (`docs/spec-daghregister-ingestion-api.md`, 2026-07-06) memilih tabel generik `staging_extractions` (dgn `metadata_json` JSONB) supaya dipakai ulang lintas sumber (Daghregister, GLOBALISE) tanpa migrasi baru tiap kali — bukan tabel khusus per-sumber di bawah ini. Desain di bawah dibiarkan sbg catatan sejarah keputusan, JANGAN diimplementasikan.

<details><summary>Desain lama (tidak dipakai)</summary>


```python
class DaghregisterVoyage(Base):
    __tablename__ = "daghregister_voyages"

    id = Column(Integer, primary_key=True, index=True)
    volume = Column(String(100), nullable=False, index=True)       # nama file jilid sumber
    book_page_start = Column(Integer, nullable=True)
    book_page_end = Column(Integer, nullable=True)
    tanggal_perkiraan = Column(String(50), nullable=True)          # teks tanggal asli, mis. "16 EN 17 FEBRUARIUS" -- BELUM dinormalisasi ke ISO date

    ship_name_raw = Column(String(200), nullable=True)             # hasil regex, BISA NULL
    direction_raw = Column(String(30), nullable=True)               # "keluar"/"masuk"/null
    cargo_text = Column(Text, nullable=True)                        # teks kargo mentah, belum di-parse jadi CargoItem
    value_gulden_raw = Column(Float, nullable=True)                 # hasil regex, BISA NULL

    text_indonesia = Column(Text, nullable=False)                   # hasil terjemahan LLM
    text_belanda_asli = Column(Text, nullable=True)                 # teks sumber

    extraction_method = Column(String(50), nullable=False, default="regex+llm_v1")
    confidence_flag = Column(String(20), nullable=False, default="unverified")  # unverified | reviewed | promoted | rejected
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(String(30), nullable=True)

    # kalau reviewer memutuskan record ini valid & lengkap, boleh di-link ke voyage resmi setelah promosi manual
    promoted_to_voyage_id = Column(Integer, ForeignKey("voyages.id"), nullable=True)
```
</details>

Field `confidence_flag` adalah mekanisme utama: semua data masuk sebagai `unverified`. Hanya record yang direview manusia (`reviewed`) dan dinyatakan lengkap boleh naik status jadi `promoted` — barulah *itu* yang ditulis ulang secara manual (bukan otomatis) sebagai baris baru di tabel `voyages`/`cargo_items` resmi, dengan `source_url` menunjuk ke jilid Daghregister asal.

### 3.2 Kenapa Bukan Langsung ke `voyages`

1. **Provenance berbeda** — `voyages.source_url` saat ini semua mengarah ke BGB Huygens (database terstruktur). Mencampur record hasil ekstraksi LLM tanpa penanda akan membingungkan siapa pun yang audit data nanti (termasuk reviewer thesis).
2. **Field wajib tidak lengkap** — `Voyage.ship_name` adalah `nullable=False`, tapi 68% kandidat Daghregister belum berhasil diekstrak nama kapalnya. Memaksakan nilai default akan menyembunyikan ketidaklengkapan data.
3. **Kargo tidak ternormalisasi** — `CargoItem` mengharapkan baris per produk (produk, qty, unit, nilai). Teks Daghregister butuh parsing tambahan (kemungkinan LLM lagi) untuk dipecah jadi baris-baris begitu, dan itu pekerjaan terpisah dari sekadar "menyimpan data".
4. **Belum ada validasi manusia** — beda dengan korpus VOC utama thesis yang sudah lewat pengkodean manual (Cohen's kappa dihitung), Daghregister voyage extraction ini murni output LLM tanpa spot-check.

## 4. Alur Kerja (Workflow)

```
1. [Sudah ada] Colab notebook scan + verifikasi + terjemahan -> daghregister_corpus.csv
2. [Baru] Skrip Python: parse daghregister_corpus.csv -> insert ke daghregister_voyages (confidence_flag=unverified)
3. [Manual, di luar kode] Reviewer (user) buka dashboard/query sederhana, filter yang ada ship_name_raw + value_gulden_raw lengkap,
   spot-check terhadap teks asli, ubah confidence_flag jadi 'reviewed' atau 'rejected'
4. [Baru] Skrip promosi: untuk confidence_flag='reviewed' yang dikonfirmasi lengkap, tulis ulang manual sbg Voyage + CargoItem resmi,
   isi promoted_to_voyage_id di baris staging
```

## 5. Test Plan (sesuai TDD wajib CLAUDE.md)

Sebelum implementasi:
1. `backend/tests/test_daghregister_voyages.py` — test model `DaghregisterVoyage` (CRUD dasar, constraint `confidence_flag` hanya menerima 4 nilai valid)
2. Test endpoint GET `/api/daghregister-voyages?confidence_flag=unverified` — filter berjalan benar
3. Test skrip parsing CSV→DB — pastikan idempotent (re-run tidak duplikasi baris untuk `volume`+`book_page_start` yang sama)
4. Test promosi: memindahkan 1 record `reviewed` ke `voyages` tidak merusak `voyage_ref` uniqueness constraint yang ada

## 6. Keputusan & Yang Masih Terbuka

**Sudah diputuskan (2026-07-06):** fitur ini untuk **keduanya** — data pendukung thesis (Bab 3/4/5) DAN memperkaya aplikasi peta westkust-routes yang publik. Implikasi: begitu record staging naik status `promoted`, ia otomatis tampil di peta publik (via tabel `voyages`/`cargo_items` resmi yang sudah dipakai frontend) — bukan cuma dokumen thesis yang terpisah dari aplikasi. Aplikasi peta sendiri (dengan pin pelayaran Daghregister 1661-1669 yang sudah dipromosikan) berpotensi jadi salah satu artefak/figur yang dirujuk di Bab 4/5 thesis nanti — mengikuti pola yang sudah ada di mini research Salido sebelumnya ("Gambar 1. Aplikasi Westkust Routes"). Konsekuensi tambahan: karena hasil `promoted` akan publik, ambang kualitas review manual sebelum promosi harus lebih ketat daripada sekadar "cukup untuk sitasi thesis" — data yang salah di peta publik lebih sulit diperbaiki diam-diam dibanding di draft akademik.

**Masih terbuka:**
1. Apakah endpoint API baru (`/api/daghregister-voyages`) perlu dibuat sekarang, atau cukup tabel + skrip import dulu (tanpa expose ke frontend) sampai ada record yang `promoted`?
2. Siapa yang melakukan review manual (`confidence_flag` unverified→reviewed) — user sendiri, atau dibuatkan tool bantu (mis. skrip CLI interaktif)?
3. Prioritas: selesaikan dulu OCR 7 jilid yang kosong sebelum bangun pipeline ini, atau jalan paralel dengan data yang sudah ada (6 jilid, 282 entri)?
4. ~~Perlu ditandai di peta publik...~~ **RESOLVED (2026-07-07):** ya, wajib — sekarang requirement P0.3b di `docs/prd-cleaning-daghregister-1660-1669.md`. Bentuk konkret pembeda (warna/ikon/layer) masih open question di sana.

---

## 7. Workflow & Board — Promosi staging_extractions → voyages (2026-07-07)

**Kenapa dibuat:** user cek app, toggle sumber "Dagh-register" (P0.3b) ada di navbar TAPI tidak menampilkan apa pun — karena memang belum ada satu pun baris `Voyage` dgn `source='daghregister_batavia'`. Infrastruktur tampilan (toggle, label modal) sudah selesai dari sesi sebelumnya; yang belum pernah dibangun adalah **langkah promosi staging→voyages itu sendiri** — ini P1.1 yang sengaja "Ditunda ke P1" di `docs/spec-daghregister-ingestion-api.md`, sekarang waktunya dikerjakan.

**Temuan angka nyata (dicek dulu sebelum janji apa pun):**

| Cek | Jumlah |
|---|---|
| Baris `single_voyage` di staging (non-duplikat) | 108 |
| ...punya `ship_name` yg bisa diresolusi (via join `pelayaran_daghregister_final.csv`) | 29 |
| ...punya `ship_name` **DAN** `direction != unknown` | **13** |

**Implikasi**: hanya **13 dari 108** baris siap dipromosikan langsung — `Voyage.ship_name` `NOT NULL`, jadi 95 sisanya (ship_name tidak ke-detect ATAU arah tak eksplisit) tidak bisa dipaksa masuk tanpa mengarang data. **Gap tambahan yang baru ketemu**: bahkan 13 baris ini cuma punya `direction` GENERIK (pantai_barat_ke_batavia / batavia_ke_pantai_barat) — bukan pelabuhan SPESIFIK (Barus? Padang? Salido?). `Voyage.origin_id`/`destination_id` nullable, TAPI endpoint `/api/voyages/routes` yg menggambar garis di peta mensyaratkan `origin_id IS NOT NULL OR destination_id IS NOT NULL` — kalau dipromosikan dgn origin_id/destination_id NULL, baris itu masuk `voyages` tapi **tetap tidak akan muncul sbg garis di peta**, toggle masih akan terlihat kosong. Perlu satu langkah ekstraksi baru: cocokkan teks tiap baris ke salah satu 10 pelabuhan target (pola sama `NAME_MAPPING`/`promote_port_tallies.py`).

### Tim & Gerbang Keputusan

**DBA** — skema, resolusi pelabuhan, script promosi.
**QA Engineer** — acceptance criteria promosi, tentukan apakah 13 baris ini butuh gerbang review manusia SEBELUM live (beda taruhannya dari stat agregat tally: ini pin individual berlabel kapal+tanggal+kargo spesifik di peta publik — PRD §6 sendiri bilang "data yang salah di peta publik lebih sulit diperbaiki diam-diam").
**DevSecOps** — verifikasi cache invalidation & re-test P0.3b toggle dgn data nyata (sebelumnya cuma teruji dgn 0 baris).
**Scrum Master** — urutan kerja, blocking chain di bawah.

### Board

| # | Kartu | Tim | Blocking? |
|---|-------|-----|-----------|
| # | Kartu | Tim | Status |
|---|-------|-----|--------|
| 1 | Ekstraksi pelabuhan spesifik per baris `single_voyage` (reuse pola `NAME_MAPPING`) utk 13 kandidat | DBA | ✅ Done — 3/12 ter-resolve (Barus, Tiku, Pulau Cingkuak); sisanya generik "Pantai Barat Sumatra" |
| 2 | Script promosi: `staging_extractions` → `Voyage` (`source='daghregister_batavia'`) | DBA | ✅ Done — `docs/thesis/dr/promote_single_voyages.py`, 12 baris (13 kandidat − 1 duplikat konkret dikecualikan) |
| 3 | Test idempotency + `voyage_ref` tetap NULL (bukan collision) | QA Engineer | ✅ Done — rerun script 2x, kedua kali 0 insert baru (idempotent via `source_url` unik) |
| 4 | **Keputusan (User)**: lewati review manual atau tidak? | User | ✅ **Keputusan: lewati review** (2026-07-07) — sama seperti kebijakan tally, TAPI 1 duplikat yg SUDAH terbukti konkret ("17 JULY"/"15--17 JULY") tetap dikecualikan eksplisit sebelum promosi, bukan diikutkan lalu didiamkan |
| 5 | Jalankan promosi, invalidate cache, re-test toggle dgn data nyata | DevSecOps | ✅ Done — cache Redis di-invalidate manual, `/api/voyages/routes?source=daghregister_batavia` mengembalikan 5 grup (4 dgn koordinat lengkap, tergambar sbg garis), diverifikasi visual via Playwright |
| 6 | Sisa 95 baris (ship_name tak ke-detect/arah tak eksplisit) | DBA usul, User putuskan | ⏳ Masih terbuka — didiamkan di staging, belum ada jadwal ekstraksi tambahan |

**Gap UI ditemukan + dibereskan (2026-07-07):** setelah promosi, toggle sumber tetap menampilkan 0 rute — bukan bug promosi, tapi slider tahun navbar defaultnya `1700-1790` (dikalibrasi utk BGB), sementara semua voyage Dagh-register ini 1663-1669/tahun tak diketahui. **Keputusan user: perlebar slider.** Diimplementasikan: `min`/default digeser 1700→1660 di `index.html` + `atlas.js` (test Django `test_year_defaults_are_1660_and_1790` diupdate). **Sekaligus**, atas permintaan user, toggle 3-tombol pill diganti jadi `<select id="source-select">` dropdown (`SourceToggleTest` di `frontend/map_app/tests.py` diupdate menyesuaikan) — supaya gampang diperluas kalau sumber baru muncul (GLOBALISE OBP dll) tanpa navbar penuh tombol. ⚠️ **Klaim "4 rute aktif, 3 garis tergambar" di paragraf ini SUPERSEDED — lihat §7.1, ke-12 voyage yg dimaksud sudah di-rollback.** UI fix (slider+dropdown) sendiri TETAP VALID dan tidak di-revert.

**Bug kedua ditemukan + dibereskan (2026-07-07, giliran berikutnya)**: bahkan setelah slider diperlebar, toggle masih tampil aneh — diselidiki, ternyata `Voyage.year >= year_from` di SQL mengembalikan NULL (bukan false) kalau `year IS NULL`, jadi baris dgn tahun tak diketahui **disenyapkan dari SEMUA filter tahun apa pun** (sama persis kelas bug dgn NULL-array guard di commodity_glossary, ditemukan sesi yg sama). 8/12 voyage yg baru dipromosikan py `year=NULL` (jilid rentang 2 tahun, sengaja tak ditebak) — jadi tak pernah tampil di app sama sekali sebelum fix ini. **Fix**: helper `_year_gte()`/`_year_lte()` di `backend/routers/voyages.py` yg eksplisit ikutkan `year IS NULL`, diterapkan ke SEMUA 7 titik filter tahun di file itu (bukan cuma yg dipakai peta). Test regresi `backend/tests/test_null_year_filter.py` (RED→GREEN, integration test dgn DB nyata krn mock tidak akan menangkap bug level-SQL ini). Backend 175 pass. **Fix ini independen dari §7.1 — tetap berlaku utk voyage manapun yg py year=NULL di masa depan**, apa pun sumbernya.

### 7.1 ROLLBACK — 0/12 voyage yg dipromosikan lolos verifikasi manual (2026-07-07)

**User minta lanjut ke cargo enrichment, tapi eksplisit minta verifikasi hati-hati dulu.** Saat menelusuri teks asli tiap satu dari 12 baris utk isi kargo, ditemukan masalah jauh lebih dasar: **nama kapal & arah yg dipakai utk PROMOSI ITU SENDIRI (bukan cuma kargonya) salah utk 12/12 baris.** Rinci per baris (nama kapal dari `pelayaran_daghregister_final.csv`, dicek manual thd `daghregister_corpus.csv.text`):

| Baris | Nama kapal (candidate) | Temuan verifikasi |
|---|---|---|
| jung Cina, 1664 | "jung Cina" | **Bukan nama kapal** — kalimat aslinya "kapal-kapal Holland...menyerang jung Cina atau perahu-perahu lain" = deskripsi GENERIK "jung Tionghoa" (kategori kapal), bukan kapal bernama. Tidak ada kargo, tidak ada Sumatra. |
| jung Spanyol, 1663 | "jung Spanyol" | Kapal riil, TAPI rute aslinya Zamboanga→Ternate (Maluku), tidak ada hubungan Pantai Barat Sumatra/Batavia sama sekali. |
| jung Barbaquet, 1665 | "jung Barbaquet" | **Bukan nama kapal** — "tikungan Barbaquet" = nama tempat (tikungan selat dekat Malaka), bukan kapal. |
| fluit Waterhoen, 1665 | "fluit Waterhoen" | Kapal riil, TAPI tujuan asli KAMBOJA, bukan Pantai Barat Sumatra — kapal yg benar2 ke Pantai Barat Sumatra (nilai f45685) adalah "Vinck", kapal lain di paragraf yg sama. |
| jung Harapan ×4 (23-26 Maret, 7-8 Agustus, 17 Juli, 11-15 Okt 1666-1667/1668-1669) | "jung Harapan" | **Bukan nama kapal, 4× berturut-turut** — "Tanjung Harapan" = Cape of Good Hope (titik transit kapal dari Belanda), keliru ke-parse sbg "[jung] Harapan". Kapal asli yg disebut: Rynland, den Achilles, fluit Loosduynen, Dordreght — semua dari Belanda, tidak satu pun dari Sumatra. |
| hoeker De Quickstaert, 1666-1667 | "hoeker De Quickstaert" | Kapal riil (disebut "de Quickstaert"), TAPI teks cuma bilang "tiba, isi air, berangkat lagi" — tidak ada kargo, tidak ada indikasi Sumatra. |
| fluit De Swarte, 1666-1667 | "fluit De Swarte" | Nama sebenarnya "de Swarte Leeuw", TAPI datang dari MALAKA (bukan Sumatra) membawa penumpang (pedagang), bukan kargo. Nilai f85920 yg terpasang sebenarnya milik "jacht Rammekens", kapal LAIN di paragraf yg sama yg justru datang dari Pantai Barat Sumatra. |
| jung Pulau Pemakan, 1666-1667 | "jung Pulau Pemakan" | **Bukan nama kapal** — "pulau pemakan manusia" = deskripsi geografis ("pulau kanibal"), bukan nama kapal. |
| hoeker De Haringh, 1666-1667 | "hoeker De Haringh" | Kapal riil ("Haringh"), TAPI rutenya lewat Japara ke MAKASSAR, bukan Pantai Barat Sumatra. |

**Hasil: 0/12 baris valid.** 3 murni salah-tangkap nama (tempat/kategori disangka nama kapal), 4 lagi (semua "jung Harapan") salah-tangkap krn tabrakan dgn "Tanjung Harapan", dan 5 sisanya adalah kapal SUNGGUHAN tapi rute/nilai yg terpasang bukan miliknya — kargo/nilai gulden yg terdeteksi regex ternyata kepunyaan kapal LAIN yg disebut di paragraf/entri harian yg sama.

**Root cause**: `pelayaran_daghregister_final.csv` (candidate CSV, sumber `nama_kapal`+`nilai_gulden_terdeteksi` utk promosi) py kelemahan ekstraksi nama-kapal yg SUDAH DIKETAHUI dari kerja lebih awal sesi ini — P0.5 cargo sanity-check sempat mencoba match berbasis `kapal_nama` dan "0/5 lolos verifikasi manual", match method itu DIHAPUS TOTAL dari P0.5 karenanya. **Kesalahan saya: tidak menerapkan kehati-hatian yg sama saat membangun jalur promosi `single_voyage`** — memakai `nama_kapal`+`nilai_gulden_terdeteksi` dari file yg SAMA tanpa verifikasi ulang, padahal precedent-nya sudah ada di sesi yg sama.

**Tindakan**: ke-12 baris di-`DELETE FROM voyages WHERE source='daghregister_batavia'` (rollback penuh, cache Redis di-invalidate). Toggle "Dagh-register" kembali menampilkan 0 rute — **ini kondisi jujur yg benar**, lebih baik drpd menampilkan data salah. `port_arrival_tallies` (jalur promosi terpisah, agregat tanpa nama kapal) TIDAK terdampak temuan ini — desainnya memang tidak bergantung pada `nama_kapal`.

**Status jalur promosi `single_voyage` → `voyages`: heuristik CSV-kandidat DITUTUP; jalur pengganti = transkripsi manual terverifikasi (lihat §7.2).**

### 7.2 Promosi ULANG — 6 voyage hasil transkripsi manual (2026-07-07, LIVE)

User menunjukkan (dgn benar) bahwa struktur data yg dibutuhkan MEMANG ADA di teks — "tiba di sini dari Pantai Barat Sumatra [kapal], bermuatan [kargo], bernilai f [nilai]" — dan investigasi rollback §7.1 sendiri sudah menemukan record yg benar. Kesalahan sebelumnya bukan "data tidak bisa", tapi jangkar nama kapal dari CSV kandidat yg salah.

`docs/thesis/dr/promote_verified_voyages.py` — 6 voyage, tiap baris ditranskripsi manual dari teks asli (BUKAN dari CSV kandidat): **jacht Rammekens** (f85.920; lada/kamper/emas/perlengkapan perang), **jacht de Cabellauw** (f20.920; lada/emas), **yacht Meliskercke + fluyt De Mees** (f86.975 gabungan — nilai dicatat di Meliskercke saja agar agregat tidak dobel, keduanya ber-catatan silang di cargo_items), **fluit Vinck** (Batavia→pantai barat, f45.685, isi muatan tak dirinci di sumber), **kapal kecil Stompneus** (f32.216; emas/lada). Idempotent via source_url (dgn fragmen `&kapal=` krn Meliskercke/De Mees berbagi entri sumber).

**Keputusan DBA — fort regional "Pantai Barat Sumatra" (id=15)**: entri ini cuma menyebut wilayah, bukan pelabuhan spesifik — dibuat node agregasi regional (koordinat lepas pantai -1.05, 99.55, deskripsi menjelaskan statusnya) alih-alih menebak ke Padang. Muncul sbg kartu sendiri di grid pelabuhan (5 keluar / 1 masuk).

**Bug frontend ke-4 ditemukan + fix**: `FORT_COORDS` di atlas.js hardcode 9 pelabuhan awal — fort yg ditambah belakangan (Tiku/Pariaman/Salido/Bayang/Painan + node regional) marker & garis rutenya DIAM-DIAM tidak tergambar (`if (!s || !e) return`). Berarti klaim garis Tiku sebelumnya juga tidak pernah benar-benar tergambar. Fix: `loadForts()` kini mengisi `FORT_COORDS` dinamis dari API; + `SEA_WAYPOINTS` utk 5 pelabuhan baru & node regional (koridor Samudra Hindia→Selat Sunda, tidak motong daratan). 2 test regresi baru (`test_fort_coords_populated_dynamically_from_api`, `test_regional_node_has_sea_waypoints`), Django 92 pass.

**Verifikasi end-to-end (Playwright)**: dropdown→Dagh-register: 2 rute, **4 garis tergambar**; panel fort regional menampilkan 6 kapal; klik jacht Rammekens → modal: Batavia / f86K / Lada / label "Dagh-register Batavia (belum diverifikasi penuh)" / detail kargo Lada+Kamper+Emas+Perlengkapan Perang. Screenshot tersimpan.

Catatan minor tersisa: tombol "Lihat sumber di BGB" di modal mengarah ke source_url lokal (path CSV) utk voyage Dagh-register — harusnya disembunyikan/diganti label utk source non-BGB. Non-blocking.

**rev.2 (2026-07-07)**: rev.1 keliru pakai istilah kargo terjemahan Indonesia — melanggar konvensi project (nama asli Belanda, tooltip glosarium menjelaskan dlm Indonesia). "Emas Jepang" bahkan salah makna ("636 Japanse taylen swaerte gout" = emas seberat 636 tael Jepang — satuannya yg Jepang). 6 voyage ditulis ulang dari `text_asli_belanda` verbatim: peper/campher/gout/oorloghs gereetschappen, nama kapal asli (jachtje de Stompneus dst). Varian glosarium ditambah (gout→goud, campher→kamfer), tooltip diverifikasi nyala via Playwright. Pelajaran dikunci: kolom `text` corpus = terjemahan LLM, data yg tampil di app SELALU transkrip dari `text_asli_belanda`.

**rev.4 (2026-07-07): sumber ketiga — kompilasi buku (JSON Colab user) → 104 voyage total.** `data_perdagangan_1660_1690_ikbal_arsya.json` (63 entri bertanggal penuh 1661-1680, mengisi gap 1670-1675 yg tanpa OCR) diolah via `promote_book_voyages.py`: 73 voyage baru + 5 update konfirmasi-silang thd baris parser-Belanda (year Ilpendam/Bunschoten/Ulissis=1667, nilai Handelaer & Vinck-dep2). Ship-list per entri di-hardcode dari pembacaan manusia atas semua 63 entri. Overlap antar 2 sumber saling konfirmasi nilai (Duynvliet ✓, Ilpendam ✓). Temuan thesis: "1786 pon emas dari tambang Silida" (1676), "63 gentong bijih dari tambang emas" (1678), "5 peti peralatan pekerja tambang" dikirim ke pantai barat (1679). Total: **104 voyage (47 masuk/57 keluar), ƒ3.761.375, 1661-1680.** Belum diolah: `dr_scan_mentah-update.json` (606 excerpt Belanda, termasuk jilid 1676-1681 yg baru sebagian ter-cover).

### 7.3 Workflow Perbaikan rev.5 — Tim DBA (DISUSUN 2026-07-07, MENUNGGU GO USER)

**Dua cacat rev.4 yg dilaporkan user (keduanya benar):**
1. **Catatan QA internal bocor ke tampilan publik** — mis. baris Elburg 1664: `all_products` berisi "(nilai OCR buku tidak koheren: 'f 33:01:14:4')". Artinya: OCR buku mencetak angka uang rusak "f 33:01:14:4" (bukan jumlah gulden valid), jadi nilai dibiarkan NULL — keputusan itu benar, tapi PENJELASANNYA salah tempat: masuk field yg tampil di modal publik, seolah bagian kargo. Kargonya sendiri (238 bahar lada, 1484 tahil emas) sah dari buku.
2. **Jangkar pelabuhan malas** — semua 104 voyage dijangkar ke node generik "Pantai Barat Sumatra", padahal teks sumber menyebut pelabuhan spesifik: Pariaman, Tiku, Barus, Padang, Salido, Tarusan, Pulau Cingkuak, Indopuro (Inderapura), Air Haji.

**Rencana langkah (eksekusi HANYA setelah GO):**

| # | Langkah | Detail | Risiko |
|---|---------|--------|--------|
| 1 | **Audit** (read-only) | Scan 104 baris: (a) pola catatan internal di `all_products` — regex "(nilai/teks/tanggal ... terpotong/tidak koheren/verbatim buku)"; (b) sebutan 9+ pelabuhan spesifik di teks sumber per entri (buku + excerpt Belanda) — hasilkan tabel usulan re-anchor per baris | Nol — cuma baca |
| 2 | **Bersihkan catatan** | Strip semua parentetikal editorial dari `all_products` (data kargo tetap); penjelasan QA CUKUP hidup di script promosi + PRD ini. Update script promosi supaya reproducible | Rendah — UPDATE terukur, reversible |
| 3 | **Resolusi pelabuhan — ATURAN** | Re-anchor `origin_id`/`destination_id` HANYA jika teks menyebut kapal *berlayar dari/ke/singgah* pelabuhan itu ("dari Padang", "van Sillida vertrocken"). **Sebutan asal BARANG ("emas dari tambang Silida") ≠ asal KAPAL** — tidak dipakai re-anchor, tetap tampil di kargo. Sebutan ambigu/multi-pelabuhan → tetap node regional | Sedang — per baris, pakai tabel audit langkah 1, bukan borongan |
| 4 | **Fort baru: Tarusan & Indopuro** | HANYA jika audit menemukan data menyebutnya sbg titik pelayaran. Koordinat usulan DBA (perkiraan kota modern): Tarusan ≈ -1.21, 100.46; Inderapura ≈ -2.20, 100.90 — **butuh konfirmasi/koreksi user** (preseden: koordinat Tiku/Pariaman/Salido/Bayang/Painan dulu dari user) | Butuh keputusan user |
| 5 | **Verifikasi** | SQL audit ulang (0 catatan bocor tersisa), Playwright modal spot-check, backend+Django test penuh, screenshot | — |

**GO diberikan user 2026-07-07 — EKSEKUSI SELESAI (`fix_rev5_cleanup_and_anchor.py`):**
- **Langkah 1 (audit)**: 8/9 sebutan "Padang" di buku = header halaman ("PADANG ABAD XVII-XVIII"); semua sebutan Salido/Cingkuak = konteks BARANG (sesuai aturan: tidak re-anchor); **Tarusan/Indopuro/Air Bangis = 0 sebutan pelayaran di kedua sumber → langkah 4 (fort baru) GUGUR sesuai syaratnya sendiri**. Corpus Belanda punya ratusan sebutan Priaman/Padang/Sillida/Indrapoura tapi di baris surat/laporan (non-formula) — mis. kutipan emas thesis: "Padang is zeer wel gelegen tot het hoofdcomptoir van de Westcust, hebbende Ticco ende Priaman aen de noordzyde, mitsgaders Sillida, Indrapoura ende Sillebar aen de zuydzyde".
- **Langkah 2 (bersih)**: catatan QA di-strip dari 13 baris `all_products` (regexp `\((nilai|teks|tanggal)[^)]*\)`), kapital penekanan dinormalkan (TAMBANG SILIDA→tambang Silida dll), catatan gabungan-nilai DIPERTAHANKAN (konteks akunting yg perlu). Audit ulang: 0 bocor tersisa. Baris Elburg kini bersih: "238 bahar lada | 1484 tahil emas".
- **Langkah 3 (jangkar + entri tersembunyi)**: split rev.4 ternyata melewatkan entri berbulan ejaan lain ("Mai", "Agusutus") — **5 voyage baru**: fluit Duynvliet 4 Mei 1673 **berjangkar destination=PADANG** (satu-satunya sebutan pelabuhan-layar spesifik: "Komandan Pits ke Padang"), jacht Wyngaert 10 Mei 1674 (ƒ19.618), Couwerve 25 Mei 1675, hoeker Goutvink + chialoup Sturgeon 4 Agt 1675 (ƒ32.723). Nilai penuh Duynvliet Agt 1668 ketemu di audit (ƒ112.835) → baris 161 diperbaiki dgn data nyata, bukan catatan.
- **Langkah 5 (verifikasi)**: total **109 voyage**; peta kini **3 rute/6 garis** (Batavia→Padang baru!); modal Elburg bersih (Playwright); backend 175 + Django 92 pass.

**rev.6 (2026-07-08): sisir `dr_scan_mentah-update.json` 1676-1681 dgn formula parser** (permintaan user). 233 excerpt → 4 kandidat unik, semua dibaca: (1) **KOREKSI NILAI**: chialoup Neptunus 30 Apr 1678 — teks Belanda asli "tesamen tot f 16798:15"; OCR buku mencetak ƒ167798 (salah tambah 1 digit; kecurigaan rev.4 terbukti). Baris dikoreksi 167798→16798 + kargo ke verbatim Belanda (benjuin Baros/camphur Baros/clappusoly). (2) **BARU**: fluyt Goylant 1681 — arrival bawa missive komisaris Laurens Pit de Jonge dari Poelo Chinco 18 Mei 1681 + laporan tambang ("myns-rapporten") → **cakupan meluas ke 1681, total 110 voyage**. (3) Sparendam 1678 = dup (skip). (4) Saxenburgh 1679 = kemungkinan sama dgn baris buku 22 Jun 1679 (missive 5 Juni dari Padang, isi: kemunduran goutmyne) — tidak di-insert dobel. Temuan thesis rev.6: jejak tambang emas berlanjut di arsip — 1679 "goutmyne... saeken weder vrywat mede teruggeliepen" (kemunduran), 1681 laporan tambang dikirim dari Poelo Chinco. Kenapa cuma 4 hit dari 233: entri 1676-1681 mayoritas ringkasan surat ("largo missive"), bukan manifes kargo — perdagangan kargo 1676-1680 sudah ter-cover buku (entri 42-63).

**rev.7 (2026-07-08): pendalaman kargo semua kedatangan Batavia** (GO user "perdalam lagi setiap muatan/kargo yg tiba di Batavia"). 49 voyage arrival yg baru py `all_products` string kini py **cargo_items terstruktur (179 item)** — parser vocab satuan/produk + 8 koreksi manual hasil baca (Pipely/Stockvisch/Swaren dipisah per kapal sesuai buku, +Stockvisch dpt nilai sendiri ƒ11.257; gumpalan Wiltenburgh dipecah; qty kapur-barus-hitam Wytingh dipulihkan; segmen Pulau Chinco di Cattenburgh/Wapen van der Goes jadi item ber-catatan provenance). 22 varian glosarium baru (kemenyan→benzoin, kapur barus→kamfer, emas→goud, lada hitam/putih→peper, dll) — tooltip modal nyala utk istilah Indonesia buku. Goylant 1681: missive/laporan = dokumen, sengaja TANPA cargo_items. Item tak dikenal dibiarkan verbatim + catatan ("Peguwse gans" = ganza logam Pegu; "schilpatshoorn" = tempurung penyu). **Agregat indikatif kedatangan 1663-1681**: kemenyan ≈363rb pon (komoditas volume terbesar!), lada ≈11,5rb bahar + 2,4jt pon + 358rb kati, emas ≈5.651 tahil + ribuan maes/maas, kapur barus ≈7,8rb pon, minyak kelapa ≈71rb kendi, gading gajah ≈813 pon — angka pertama qty, heterogenitas satuan tidak dipaksakan dikonversi. Backend 175 + Django 92 pass.

**rev.8 (2026-07-08): lapisan pelayaran PESISIR + fort Inderapura** (GO user). 16 pelayaran lokal antar-pelabuhan pantai barat dari narasi surat komandan (`lapis=surat` di source_url; year = tahun jilid, presisi lebih rendah dari manifes Batavia — semua konteks dibaca manusia, `promote_coastal.py`). Fort **Inderapura** (id=16, ≈-2.20,100.87) dibuat — jangkarnya bukan Cabeljauw (ternyata cuma "via"), tapi temuan koreksi-bacaan: **jacht de Haes DITEMPATKAN di Indrapoura 1661** sbg kapal residen Pieter Ketting + stok dagang ƒ40.530. Kutipan thesis dari konteks yg sama: *"Indrapoura levert alleen meer peper uyt als Sillida, Priaman en Ticco te zamen"* (1661). Direction `transit` dipakai utk leg antar-pesisir (garis abu putus, konsisten palet lama); Batavia→Padang (Casuwaris) = inbound; Pariaman→Batavia (vaertuyg pribumi tanpa nama — ship_name deskriptif, bukan nama karangan) & Tiku→Bantam (jonk sabandar Kaytsoe, muat camfer baros+gout — kapal pribumi!) = outbound. Tujuan non-fort dicatat raw (Bantam, "Majutte (via Indrapoura)" utk ekspedisi militer Cabeljauw+Casuares 1665). +11 SEA_WAYPOINTS pasangan pesisir. **Total Dagh-register: 126 voyage (52 in / 61 out / 13 transit), 15 rute, 26 garis.** Backend 175 + Django 92 pass.

### 7.5 Workflow rev.9 — Traceability kargo + jangkar Padang + seragam Belanda (2026-07-08, parameter dari user)

| # | Kartu | Aturan |
|---|---|---|
| 1 | **Jangkar Padang**: semua voyage ber-node "Pantai Barat Sumatra" (fort 15) di-repoint ke fort Padang (hoofdcomptoir — dasar: kutipan VOC "Padang is zeer wel gelegen tot het hoofdcomptoir"); `origin/destination_name_raw` TETAP "Pantai Barat Sumatra" (jujur thd teks); fort 15 dihapus setelah kosong. Kasus self-loop (de Mees regional→Padang) → origin NULL. |
| 2 | **Seragam Belanda di cargo_items**: rename produk ke istilah Belanda HANYA yg atest di sumber sendiri/standar VOC (lada→peper, emas→gout, kemenyan→benjuin, kapur barus→campher Baros, minyak kelapa→clappusoly, gading gajah→eliphants tanden, dll); istilah asli buku disimpan di `catatan` "(buku: X)". Istilah tanpa padanan atest (minyak kapur barus, kayu secang, baja) TETAP versi buku — tidak mengarang. `all_products` dibiarkan = lapisan transkrip verbatim buku; `cargo_items` = lapisan presentasi Belanda. |
| 3 | **Tanggal yg terlewat**: isi departure/arrival_date utk voyage parser-Belanda/rev.2 yg tanggal+tahunnya pasti (Tortelduyf & Saphier dep 1661-08-17; Meliskercke & De Mees arr 1665-03-09; Vinck dep 1665-05-27 & 1665-09-13; Sparendam dep 1678-07-12). Tanggal tanpa tahun pasti (jilid rentang) tetap kosong. |
| 4 | **Traceability**: artifact tabel penuh per-komoditas → kapal, tanggal, qty verbatim, arah — jawab "kapal mana, tanggal berapa" utk tiap angka agregat. |

**EKSEKUSI SELESAI (2026-07-08)**: fort 15 "Pantai Barat Sumatra" dihapus, 113 referensi voyage di-repoint ke Padang (raw name tetap; 1 self-loop de Mees → origin NULL) — kartu Padang kini 220/192. 156 cargo_items diseragamkan ke Belanda (istilah buku pindah ke catatan "buku: X"), 24 main_product ikut, varian glosarium +swarte/witte peper. 7 tanggal keberangkatan/kedatangan yg terlewat diisi (Tortelduyf/Saphier 1661-08-17, Meliskercke/De Mees 1665-03-09, Vinck 1665-05-27 & 1665-09-13, Sparendam 1678-07-12). Artifact traceability (235 item, 8 kelompok komoditas + lainnya): https://claude.ai/code/artifact/0ef949cc-f37f-4a25-87f8-6401b2f259d6 . Verifikasi: modal Ilpendam 1669 kini "Gout | Eliphants Tanden | Campher Baros | Benjuin | Peper" semua ber-tooltip; 13 rute/20 garis (rute regional melebur ke Padang); backend 175 + Django 92 pass.

**rev.10 (2026-07-08): penanggalan** (permintaan user — "yg belum ada di data kargo"). Dari 41 voyage tanpa tanggal, **24 terisi** dgn 3 metode berjenjang: (a) hari eksplisit di teks + jilid tahun-tunggal ("22 d. des morgens vertrecken" → 1665-04-22; Cabeljauw/Casuares dep 1665-03-25 arr 1665-04-02; Elburg pesisir 1663-02-15; Elburgh 1664-12-16/29); (b) jangkar tanggal-penuh buku utk entri yg sama (Duynvliet 1666-06-05, Handelaer 1667-10-25, konvoi Verspreet 1667-08-16, Ilpendam grup 1667-08-21, Zandtlooper/Pipely 1666-09-30 — buku menyelesaikan konflik jilid); (c) **jangkar historis**: entri Westwout menyebut jatuhnya benteng Samboupo Makassar (Juni 1669) → "17 JULY" = **1669-07-17**. Kebijakan label-rentang-2-hari tanpa penanda hari: pakai hari TERAKHIR rentang (Vinck-arr 1665-08-27, Zeehondt-arr 1665-10-31) — dicatat di sini & artifact. **17 voyage tetap tanpa tanggal secara jujur** (Rammekens, Cabellauw-arr, Stompneus, Durgerdam-arr, Pipely-arr: jilid rentang tanpa jangkar tahun; + pesisir tanpa hari eksplisit di narasi). Status: 109/126 bertanggal. Modal kini menampilkan "Berangkat/Tiba YYYY-MM-DD" (bukan cuma tahun; test `test_modal_shows_full_dates_when_present`, Django 93 pass). Artifact traceability di-redeploy dgn tanggal (v2, URL sama).

**rev.10b (2026-07-08): tanggal TAMPIL di semua permukaan** (laporan user: "fluyt Remedie 1663" tanpa tanggal). Root cause ganda: (1) fix rev.10 baru menyentuh modal — daftar kapal panel samping & dropdown pencarian masih render `v.year` mentah, padahal jacht Remedie SUDAH punya arrival 1663-03-27; (2) fluyt Remedie pesisir memang tanpa ISO, tapi info parsial sumber ("dikirim ke Ticco sebelum 15 Feb") dibuang saat tampil. Fix: helper `voyageDateText()` dipakai seragam di modal + sidebar + dropdown + aria-label — berjenjang: ISO dep→arr, lalu label tanggal sumber dari source_url (+tahun/jilid), lalu tahun. Label parsial "sebelum 15 FEBRUARY" ditambahkan ke source_url Remedie pesisir. Verifikasi Playwright: dropdown kini "jacht Remedie **1663-03-27**" & "fluyt Remedie **sebelum 15 FEBRUARY 1663**"; modal Rammekens "26 EN 27 FEBRUARY · jilid 1666-1667" (label sumber tampil meski tahun tak pasti — tidak lagi cuma "?"). Django 93 pass.

### 7.6 Workflow rev.11 (2026-07-08, GO user): fokus Westkust murni + kelengkapan BGB

| # | Kartu | Tim |
|---|---|---|
| 1 | Hapus Jambi, Palembang, Lampung (pelabuhan pantai TIMUR, di luar skope atlas Westkust): fort + voyage cascade + tally origin→NULL + FORTS_META/NAME_MAPPING seed + FORT_COORDS/SEA_WAYPOINTS frontend | DBA-1 |
| 2 | Hapus frasa "(terverifikasi)"/"(belum terverifikasi penuh)" dari label sumber — verifikasi sudah dilakukan tim | DBA-2 |
| 3 | Scout endpoint pencarian BGB Huygens → scraping ulang SEMUA pelabuhan pantai barat (Barus→Indopuro + varian ejaan), sopan (rate-limit), via **Workflow ≤5 agen DBA** → banding `voyage_ref` vs DB → laporan gap | DBA-3..5 + Scrum Master |

**HASIL EKSEKUSI rev.11 (2026-07-08):**
- Kartu 1 ✅: 3 fort timur + 545 voyage terkait dihapus (total 4.328→4.329 setelah kartu 3); `seed_data.py` disesuaikan (EAST_PORTS_EXCLUDED) + koreksi mapping historis `Indrapoera/Indrapura → Inderapura` (dulu keliru ke Pulau Cingkuak; 1 voyage BGB lama di-re-anchor); test seed & baseline count diupdate.
- Kartu 2 ✅: frasa "(terverifikasi)/(belum terverifikasi penuh)" dihapus dari dropdown, label modal, caveat halaman Fort. Label GLOBALISE OBP dipertahankan apa adanya (datanya memang belum diverifikasi tim, belum ada yg dipromosikan).
- Kartu 3 ✅: **Temuan struktural** — kosakata tempat BGB utk pantai barat HANYA 3: Padang(926), Pulau Tjinkuk(858), Airhadji(854), + region "Sumatra's Westkust"(3120); Barus/Tiku/Pariaman/Salido/Indopuro TIDAK pernah jadi place-entry BGB (mereka lapisan Dagh-register). Sweep Workflow 5 agen (2 stream region selesai; 3 stream place kena limit sesi, diselesaikan inline): **361 voyage unik**; sweep place = subset penuh sweep region (validasi silang). Banding vs 4.202 voyage_ref DB: **HANYA 1 GAP — voyage 7324 Ouwerkerk (Batavia→Sumatra's Westkust, berangkat 6-8-1757, f266.827 India, 28 item kargo tekstil Kust/Bengaals/Surats + realen)**; remarks BGB: "Padang, Pulau Tjinkuk and Airhadji are listed as places of destination". Di-ingest lengkap dgn cargo_items (jangkar Padang per kebijakan rev.9, raw dipertahankan). **Kesimpulan audit: data BGB pantai barat kini 100% lengkap (361/361).**

**Jalur skala rev.3: formula parser lokal, TANPA LLM/API.** Rencana Colab+sumopod DIBATALKAN user (biaya API tidak perlu utk riset) — dan analisis membuktikan user benar: juru tulis VOC menulis pelayaran dgn formula baku di teks Belanda, jadi regex berjangkar formula cukup. **Akar kegagalan v1 DIREVISI**: regex v1 jalan di TERJEMAHAN Indonesia — "Tanjung Harapan" tidak ada di teks Belanda (aslinya "Caeb de Bonne Esperance"); jebakan diciptakan lapisan terjemahan, bukan sifat sumbernya. `docs/thesis/dr/promote_formula_voyages.py`: parser di `text_asli_belanda` (267/470 baris menyebut Westcust) → 11 kedatangan formula-ketat + 13 keberangkatan; SEMUA window bukti dibaca manusia sebelum masuk daftar promosi. **25 voyage baru → total Dagh-register 31 baris, ƒ798.262.** Temuan thesis: entri Tortelduyf 1661 eksplisit memerintahkan singgah "Sillebar, SILLIDA en andere ... tot Padang"; fluyt Bunschoten (contoh motivasi awal riset) kini live dgn nilai gabungan f146.551. Cross-jilid dup dipromosikan sekali; nilai OCR ambigu → null + catatan. Backend 175 + Django 92 pass.

**Bukti konkret ditemukan saat spot-check (2026-07-07):** dari 13 kandidat, **"17 JULY" (jilid 1666-1667) dan "15--17 JULY" (jilid 1668-1669) adalah baris DUPLIKAT** (teks nyaris identik — soal serah-terima pemerintahan Japare, kapal tiba dari Macassar) yang LOLOS dari P0.2 dedup. Sebab: dedup P0.2 mengelompokkan pasangan berdasar `tanggal_perkiraan` yg SAMA PERSIS — "17 JULY" vs "15--17 JULY" adalah label tanggal berbeda utk hari yg sama (rentang tanggal beda krn OCR/LLM run beda), jadi tidak pernah dibandingkan satu sama lain oleh script. **Ini gap baru di P0.2**, ditemukan justru krn card #4 (review manual) dijalankan sebagian — bukti langsung kenapa spot-check masih bernilai meski utk kumpulan kecil.

---

## 8. Code Review Sebelum Commit (2026-07-08)

Sebelum commit+push+deploy, seluruh diff sesi ini (16 file tracked + file baru) direview via 7 sudut paralel (correctness ×2 selesai dari 3 — 1 dihentikan user, removed-behavior, cross-file tracer, reuse, simplification, efficiency, altitude, konvensi CLAUDE.md). 8 temuan lolos verifikasi, semua langsung diperbaiki:

1. **`seed_data.py` — Indrapura terbelah 2 fort**: mapping "Indrapoura" masih menunjuk Pulau Cingkuak sisa sebelum fort Inderapura dibuat, sementara "Indrapoera"/"Indrapura" sudah benar. Diperbaiki: ketiganya → Inderapura.
2. **`forts.py` — `compare_ports` & `list_fort_voyages` belum ikut migrasi `_year_gte`/`_year_lte`**: voyage Dagh-register ber-`year=NULL` hilang diam-diam di 2 endpoint ini saat filter tahun, tidak konsisten dgn `/api/voyages`. Diperbaiki: import & pakai helper yg sama.
3. **`atlas.js` — `innerHTML` tanpa `esc()`** di modal meta (baris `dateText`): satu-satunya call-site `voyageDateText()` yg tak dibungkus escape, inkonsisten dgn 2 call-site lain. Diperbaiki: `esc(dateText)`.
4. **`test_null_year_filter.py` — password DB asli ter-hardcode** (`vocpassword`) di fallback `os.getenv`, melanggar Security Checklist CLAUDE.md & konvensi repo sendiri (`test_atm_p0_us06.py` pakai `***REDACTED***`). Diperbaiki: redacted.
5. **`voyages.py` — param `source` tanpa validasi Pydantic**: string bebas padahal domain cuma 3 nilai, pola sama dgn bug SEC-2 lama. Diperbaiki: `Literal["bgb_huygens","daghregister_batavia","globalise_obp"]` — verifikasi live: `?source=invalid` kini 422.
6. **`seed_data.py` — varian ejaan pantai timur lolos exclusion di reseed baru**: `EAST_PORTS_EXCLUDED` dicek pasca `clean_name()`, tapi mapping ejaan varian (Djambi/Lampongs dst) dihapus bersamaan sehingga tidak lagi dinormalisasi ke nama kanonik yg di-exclude. Diperbaiki: helper `_split_raw_name()` baru, exclusion dicek thd RAW name sebelum `NAME_MAPPING`.
7. **`atlas.js` — `FORT_COORDS` Pulau Cingkuak basi**: hardcode lama (`-1.3528370,100.5599951`) menyimpang dari `seed_data.py` yg sudah dikoreksi sesi ini (`-1.3531125710383205,100.55921198502948`); guard `!FORT_COORDS[f.name]` bikin API tak pernah menang. Diperbaiki: samakan nilai hardcode.

**Dipertimbangkan tapi TIDAK diubah**: `get_voyage_routes` men-`GROUP BY Voyage.source` tanpa syarat filter aktif (flagged sudut cross-file) — setelah ditelaah ulang, ini SESUAI desain P0.3b yg disengaja (provenance tidak boleh dibaurkan diam-diam ke satu angka blended, prinsip yg sudah ditetapkan sejak rollback §7.1). Efeknya cuma kosmetik (badge "rute aktif" menghitung per-provenance, bukan per-pasangan-pelabuhan) — didokumentasikan di sini, bukan bug.

**Tidak diblokir commit** (cleanup/dupe, dicatat utk nanti): `NAME_MAPPING` tersalin sebagian & divergen di `promote_port_tallies.py`; boilerplate INSERT+idempotency identik di 6 script `docs/thesis/dr/promote_*.py`; helper timestamp `.replace(microsecond=0)` tertulis 3x; script promosi tidak memanggil `cache.invalidate_prefix_sync()` sendiri (masih manual via `redis-cli FLUSHALL` tiap kali).

**Regresi penuh pasca-fix**: backend 175 pass, Django 93 pass, curl smoke (homepage/voyages/glossary/port_detail/forts-compare/fort-voyages) semua 200, `console errors: none` (Playwright), data intact (4.329 voyage, 12 fort tidak berubah — restart bukan reseed krn tabel tidak kosong).

---

## 9. Deploy Production (2026-07-08)

Push ke `main` (`73f2b5f`) → deploy ke `salido.my.id` (VPS, lihat memory `project_server_salido`). **Insiden singkat**: rebuild container backend sempat 500 (kode baru butuh kolom yg belum ada) — root cause sama persis dgn kejadian lokal migration 005 (`seed_data.py`'s `create_all()` mendahului alembic). Fix: `alembic upgrade 004` (isolasi), `alembic stamp 005` (tabel sudah match via create_all), `alembic upgrade head` (jalankan 006). Downtime ~5 menit.

**Replikasi data** (bukan cuma kode+skema — `staging_extractions` production kosong sebelum ini, artinya SELURUH data Dagh-register sesi ini cuma ada di dev lokal): dibangun bundle JSON **name-keyed** (fort dirujuk via nama, bukan ID — ID production berbeda dari lokal krn histori insert/delete berbeda) berisi forts, glossary, staging_extractions, tallies, voyage Dagh-register+cargo, dan BGB gap-fill (Ouwerkerk). Diimpor via script idempotent (cek existing sebelum insert per tabel).

**2 gap ditemukan saat verifikasi paritas baris-demi-baris** (bukan cuma cek total count — keduanya lolos krn idempotency-check terlalu longgar, cuma bandingkan produk+qty tanpa spesifikasi/catatan pembeda):
- cargo_items voyage "Wapen van der Goes" (entri 61): 2 baris "mineral" beda `catatan` (generik vs "dari Pulau Cingkuak") — baris kedua ke-skip krn dianggap duplikat baris pertama.
- cargo_items Ouwerkerk (BGB gap-fill 7324): 2 baris "lakenrassen, 1, pees" beda `spesifikasi`/nilai — sama, baris kedua ke-skip.

Keduanya di-insert manual setelah ditemukan. **Verifikasi paritas akhir (lokal vs production, sama persis)**: voyages 4.329 (bgb 4.203 + dagh 126), forts 12, cargo_items 53.028, tallies 98, staging 119, glossary 207 (6 ber-citation). Live: `salido.my.id/atlas` dropdown Dagh-register → 13 rute termasuk jaringan pesisir penuh (Padang↔Tiku↔Salido↔Pariaman↔Inderapura), glosarium tooltip aktif.

**Pelajaran**: idempotency-check utk baris yg bisa legitimately duplikat di kolom utama (produk sama, qty sama) HARUS ikutkan kolom pembeda (catatan/spesifikasi/nilai) di klausa WHERE — bukan cuma kolom "identitas" yg kelihatan unik. Verifikasi migrasi data sebaiknya selalu row-count PER TABEL/PER-SUMBER, bukan cuma total gabungan (total yg cocok bisa menyembunyikan 2 kesalahan yg saling meniadakan secara kebetulan — untungnya di sini tidak terjadi, tapi count granular tetap yg mengungkap gap-nya).
