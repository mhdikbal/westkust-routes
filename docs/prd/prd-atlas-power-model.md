# PRD: Model Data Kekuasaan & Diplomasi untuk `/atlas`

**Status:** Draft desain model data — untuk handover ke tim UI/UX sebelum desain tampilan. Belum ada migrasi/kode ditulis.
**Konteks:** `/atlas` (view `index()` di `frontend/map_app/views.py`, template `index.html`, logic `frontend/map_app/static/map_app/js/atlas.js`) adalah peta VOC Trade Atlas — satu-satunya halaman `map_app` yang publik (bukan `noindex`, beda dari `/linimasa` dan `/riset/*`). Enam sesi sisir `docs/CD1.pdf`–`docs/CD6.pdf` (Corpus Diplomaticum Neerlando-Indicum jilid I–VI) menghasilkan `atjeh_trade_records` (152 baris) dan `linimasa_events` (101 peristiwa, 1600–1775, bertahun & bersitasi `text_asli`) — data politik/diplomatik Aceh↔pantai-barat yang jauh lebih presisi-tanggal dibanding apa pun yang tampil di `/atlas` sekarang. PRD ini merancang cara menghubungkan data itu ke peta.

---

## 1. Masalah yang Memicu PRD Ini

`atlas.js` punya fungsi `drawPowerRoutes()` (baris ~370–408) yang menggambar garis putus-putus ungu Aceh→setiap-fort untuk merepresentasikan "jalur kekuasaan". Cara kerjanya sekarang:

```js
// drawPowerRoutes(politicalRows, forts) — disederhanakan
forts.forEach(f => {
  if (f.name === "Aceh" || f.name === "Batavia") return;
  const matches = politicalNotesForFort(f.name, politicalRows); // string-match nama fort di notes
  if (matches.length === 0) return;
  // ...gambar garis Aceh→f, STATIS, tanpa syarat tahun...
});
```

Cukup ADA satu baris `atjeh_trade_records` dengan `direction='politik'` yang menyebut nama fort itu di mana saja (`notes`/`actor_raw`), garis langsung digambar dan berlaku **selamanya** — tidak berubah walau slider tahun (`drawRoutes()`, yang mengontrol rute pelayaran) digeser.

Ini keliru secara historis, dan kita punya buktinya sendiri dari sisir CD1–CD6:

| Fort | Realitas dari data kita | Direpresentasikan `drawPowerRoutes()` sekarang sebagai |
|---|---|---|
| Barus | Di bawah Aceh → lepas 1668 → VOC sendiri **mundur** 1775 (kalah saing Inggris) | Garis Aceh→Barus permanen |
| Pariaman | Lepas Aceh 1671 → **relaps** 1678, 1684, lagi ~1689–1712 → tunduk ulang 1712 | Garis Aceh→Pariaman permanen (tak bisa tunjukkan siklus relaps) |
| Salido/Zillida | Diserahkan ke VOC 1667, direnovasi 1755 (raja minta gelar "Siri-nara") | Garis Aceh→Salido permanen (padahal sejak 1667 bukan lagi soal Aceh) |
| — (Natal, belum di roster fort) | Belanda (1693) → **Inggris** duduki paksa → **Prancis** rebut 1760 → Belanda lagi | Tak tergambar sama sekali (bukan soal Aceh, jadi tak match) |

Model data baru harus: (a) bertahun/dinamis, sinkron dengan slider tahun yang sudah ada; (b) tertelusur ke event & kutipan sumber spesifik untuk tooltip; (c) tidak terbatas pada "status vs Aceh" saja — juga tangkap pergeseran ke Inggris/Prancis dan VOC mundur sendiri, yang justru tema besar CD5–CD6.

---

## 2. Audit Data yang Sudah Ada

- **`Fort`** (`backend/models.py`): 13 baris — Aceh, Barus, Air Bangis, Padang, Pariaman, Salido, Bayang, Painan, Air Haji, Inderapura, Pulau Cingkuak, Tiku, Batavia. Punya `latitude`/`longitude` + `Geometry` point. `atlas.js` mengambilnya lewat `FORT_COORDS` (dari `GET /api/forts/routes/all`, `backend/routers/forts.py:241`).
- **`Voyage`**: data pelayaran riil, `year` terisi, sudah menggerakkan slider tahun (`drawRoutes()` dipanggil ulang tiap slider berubah). **Pola inilah yang ditiru** untuk layer kekuasaan baru — bukan pola baru bagi codebase ini.
- **`AtjehTradeRecord`**: `direction` (`naar_atjeh`/`van_atjeh`/`in_atjeh`/`politik`). Baris `direction='politik'` SENGAJA punya `commodity_raw`/`price_value` kosong (ditegakkan `test_political_facts_marked_not_trade` — pemisahan fakta-politik vs transaksi-dagang, jangan diubah).
- **`LinimasaEvent`**: `year`, `event_type` (suksesi/perjanjian/konflik/diplomasi/administratif — ini **tipe dokumen**, bukan status kekuasaan), `era_slug` (5 babak non-overlap 1600–1775), `ruler_actor`, `title`, `text_asli` (wajib), `notes`. **Belum punya `fort_id`** — nama tempat cuma teks bebas. Ini gap utama yang diisi PRD ini.
- Preseden pola resolve-fort-by-name sudah ada: commit `2b6d672 fix(data): resolve fort Inderapura by name, bukan hardcode id` — pola ini yang direplikasi untuk seeding, bukan hardcode `fort_id` di CSV.
- Migrasi terakhir: `010_add_linimasa_era_slug.py`.

---

## 3. Skema Baru: 3 Kolom Nullable di `LinimasaEvent`

**Keputusan desain: perluas `LinimasaEvent`, JANGAN buat tabel interval baru** (mis. `FortPowerStatus` dengan `start_year`/`end_year` eksplisit). Alasan: proyek ini sudah dua kali kena masalah tabel turunan yang lupa disinkronkan dari sumber primer — `linimasa_events` sendiri adalah "distilasi" dari `atjeh_trade_records`, dan sempat ketinggalan sinkron saat volume baru ditambah (GOTCHA yang didokumentasikan eksplisit di `seed_linimasa_events.py`, jadi alasan test seperti `test_cd6_treaties_present` selalu ditambah tiap sisir). Tabel interval kedua akan mengulang risiko drift yang sama. Status kekuasaan cukup **dihitung**, bukan disimpan sebagai interval: event berikutnya (bertahun lebih besar) untuk fort yang sama otomatis menggantikan status event sebelumnya.

```python
# tambahan ke LinimasaEvent (backend/models.py)
fort_id = Column(Integer, ForeignKey("forts.id"), nullable=True, index=True)
dominion_status = Column(String(30), nullable=True, index=True)
tags = Column(ARRAY(Text), nullable=True)  # pola sama CommodityGlossary.variants
```

### 3.1 `fort_id`

Diisi **hanya** kalau event jelas tentang satu fort di roster 13 yang sudah ada. Event yang menyebut banyak lokasi sekaligus (mis. traktat aliansi umum 29 Agustus 1680 yang menyatukan Indrapoura/Padang/Kottatenga/Sillida dalam satu dokumen) — pilih fort paling sentral/penanda-tanda-tangan saat backfill, dicatat ambiguitasnya di `notes` bila perlu. Event yang subjeknya bukan fort roster (Nias, Natal, Tigablas Cottas, dll — lihat §4) tetap `fort_id=NULL`, tetap tampil di `/linimasa`, sekadar belum masuk layer peta.

### 3.2 `dominion_status`

Vokabular terkendali, divalidasi di `seed_linimasa_events.py` (pola sama `ALLOWED_EVENT_TYPES`/`ALLOWED_ERAS`):

| Nilai | Makna | Contoh dari data kita |
|---|---|---|
| `aceh_dominion` | Di bawah kekuasaan/pungutan-tol Aceh | Titah tol Iskandar Muda 1632 |
| `voc_alliance` | Traktat aliansi/tunduk ke VOC | Traktat Painan 1663, aliansi umum 1680 |
| `independence` | Lepas dari kekuasaan luar | Penyerahan Sillida 1667 |
| `relapse_aceh` | Kembali berpaling ke Aceh setelah sempat lepas | Priaman 1678, 1684, ~1693–1712 |
| `foreign_orbit` | Di bawah pengaruh Eropa lain (Inggris/Prancis), bukan Aceh/VOC | Natal diduduki Inggris (CD6), lalu direbut Prancis 1760 |
| `voc_withdrawal` | VOC sendiri mundur/tutup pos | Penutupan loge Barus 1775 |
| `internal_conflict` | Pergolakan internal, tanpa pergantian kekuasaan luar | Suksesi Baros 1694, sengketa Kolang-Sorkam |
| `NULL` | Event tak merepresentasikan transisi status (mis. traktat teknis) | — |

**Cara endpoint menghitung "status pada tahun X"**: ambil `LinimasaEvent` ber-`fort_id` itu, `year <= X`, urut turun, ambil baris pertama (`dominion_status` terbaru sebelum/pada X). Prinsipnya identik dengan cara `atlas.js` sudah memfilter `Voyage` berdasarkan tahun — bukan konsep query baru bagi backend ini.

### 3.3 `tags`

Array bebas, independen dari `dominion_status`, untuk layer tematik terpisah (bukan garis kekuasaan, tapi marker diplomasi/hadiah): `"tol"`, `"hadiah"`, `"ekspansi_inggris"`, `"ekspansi_prancis"`, `"penyelundupan"`, `"suksesi"`, dll. **Tidak** mencoba menstrukturkan nilai (rijksdaalder, jenis kain, dst) ke kolom numerik baru — angka-angka itu tetap hidup sebagai kutipan di `text_asli`/`notes`, konsisten prinsip "text_asli wajib, tak ada klaim tanpa jejak sumber" yang sudah berjalan sejak CD1.

---

## 4. Cakupan Fase 1 vs Fase 2 (Backlog)

**Fase 1 (dirancang PRD ini):** hanya 13 fort yang sudah ada di roster. Confirmed dengan user — model data dibuat generik/scalable, tapi backfill awal dan endpoint hanya menyasar fort yang sudah punya titik di peta.

**Fase 2 (backlog, TIDAK dirancang detail di sini):** ekspansi roster `Fort` untuk lokasi yang berulang kali muncul signifikan di CD1–CD6 tapi belum punya titik:
- Pulau Nias & negeri-negerinya (Sillibo, Nay-Lambara, Malakerre-Telok Dalam, Hinako-Maros, Lahomi-Laoesa, Gunung Jarroe, Gomboe) — tujuh traktat terpisah ekspedisi Sas 1693 (CD4)
- Natal — episode Belanda→Inggris→Prancis→Belanda (CD6)
- Singkil/Cinkel — traktat 1672, 1681, 1707
- Sorkam, Pasariboe — sengketa lokal & mediasi Baros
- Tigablas Cottas & Doeapoeloeh-Kotta — konfederasi pedalaman, aliansi berulang 1727/1741/1763
- Batang Kapas, Tello, Tarato, dan sisa Sapuluh Buah Bandar (1687, direnovasi 1755)

Perlu riset lat/lon per lokasi sebelum masuk roster — di luar scope sesi ini.

---

## 5. Kontrak API

Ditambahkan ke `backend/routers/forts.py` (dekat `/routes/all` yang sudah ada), bukan router baru — UI/UX cukup satu domain endpoint untuk kebutuhan peta.

### `GET /api/forts/power-status?year=<int>`

Per fort ber-`fort_id`, status aktif pada tahun itu + event penanda untuk tooltip/sitasi.

```json
[
  {
    "fort_id": 1,
    "fort_name": "Barus",
    "dominion_status": "voc_withdrawal",
    "as_of_event": {
      "id": 187,
      "year": 1775,
      "event_date_raw": "23 Januari 1775",
      "title": "VOC tarik mundur dari loge Barus, kalah saing Inggris Bengkulu",
      "text_asli": "Sedert een eeuw had de Compagnie een loge op Baros gehad...",
      "source_document": "CD6"
    }
  }
]
```

Fort tanpa event ber-`fort_id` sama sekali (atau tanpa event `year <= X`) **tidak muncul** di response — bukan dikirim dengan status "netral"/default. Ini penting untuk UI/UX: absennya entri = "belum ada data", bukan klaim implisit "tak ada kekuasaan apa pun".

### `GET /api/forts/diplomacy-markers?year=<int>&tag=<optional>`

Event ber-`fort_id` **dan** `tags` non-null, untuk layer marker terpisah dari garis dominion (mis. ikon hadiah/tol, bukan garis). `year` opsional filter kumulatif (semua event hingga tahun itu) atau exact-year — diputuskan bareng tim UI/UX (lihat §7).

```json
[
  {
    "fort_id": 6,
    "fort_name": "Salido",
    "year": 1755,
    "tags": ["hadiah"],
    "title": "Raja Salida minta & terima gelar kehormatan Siri-nara",
    "text_asli": "...Teffens versoekt Syne Majesteid, dat mag werden gehonoreert met den eernaam van Siri-nara...",
    "source_document": "CD6"
  }
]
```

---

## 6. Migrasi & Backfill

- **Migrasi** `011_add_linimasa_power_status.py` (`backend/alembic/versions/`): 3 kolom nullable + index di `fort_id` dan `dominion_status`, ikuti pola persis `010_add_linimasa_era_slug.py`.
- **CSV** (`data/research/linimasa_events.csv`): tambah kolom `fort_name` (BUKAN `fort_id` — resolve by name saat seed, pola commit Inderapura), `dominion_status`, `tags` (pipe-separated, mis. `"tol|hadiah"`). Kolom opsional per baris.
- **`seed_linimasa_events.py`**: tambah `ALLOWED_DOMINION_STATUS` set, validasi di `parse_row()` (pola sama `ALLOWED_EVENT_TYPES`), resolve `fort_name` → `fort_id` via query `Fort` by name (bukan hardcode).
- **Backfill data**: BERTAHAP di sesi terpisah, bukan sekaligus 101 baris. Mulai dari event yang paling jelas satu-fort (traktat aliansi/pelepasan/relaps eksplisit) — realistis mencakup mungkin 30–50 dari 101 baris di iterasi pertama; sisanya (event multi-lokasi, event tanpa fort di roster 13) tetap `fort_id=NULL` sampai Fase 2 atau evaluasi kasus-per-kasus.

---

## 7. Pertanyaan Terbuka untuk Tim UI/UX

1. **Skema warna per `dominion_status`** — 7 status di §3.2 perlu palet berbeda (bukan satu ungu `POWER_ROUTE_COLOR` untuk semua seperti sekarang). Disarankan: dua sumbu (Aceh-tone vs VOC-tone vs Eropa-lain-tone) daripada 7 warna lepas — tapi keputusan visual final di tim UI/UX.
2. **Marker hadiah/tol** — ikon kustom (mis. simbol hadiah/koin) atau titik warna berbeda dari garis dominion? `tags` (§3.3) menyediakan datanya, bentuk visualnya belum diputuskan.
3. **Default layer ON/OFF** — garis kekuasaan tampil default saat `/atlas` dibuka, atau opt-in via toggle (seperti direction toggle pelayaran yang sudah ada)? Mengingat data baru ini jauh lebih padat-info (101 event vs sebelumnya statis), overlay-default berisiko ramai.
4. **Fort tanpa data** (§5, absen dari response) — ditampilkan sbg titik abu-abu netral, atau memang tak dirender apa pun untuk fort itu di layer kekuasaan (tapi tetap muncul di layer pelayaran)?
5. **Filter tahun kumulatif vs snapshot** — `diplomacy-markers?year=X`: tampilkan SEMUA event historis hingga tahun X (akumulasi), atau hanya event PADA tahun X (snapshot, konsisten cara `power-status` bekerja)? Berdampak ke UX slider.

---

## 8. Non-Goals Sesi Ini

- Parsing nilai tol/hadiah (rijksdaalder, jenis kain/komoditas) ke kolom numerik terstruktur — tetap kutipan teks di `text_asli`/`notes`.
- Ekspansi roster `Fort` untuk lokasi Fase 2 (§4) — perlu riset lat/lon terpisah.
- Implementasi migrasi, endpoint, atau perubahan `atlas.js` — PRD ini murni desain model data untuk direview, bukan kode yang sudah jalan. Follow-up terpisah setelah sign-off tim UI/UX.
