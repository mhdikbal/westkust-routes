# PRD: Kronik Pantai Barat 1600–1690 — Redesain `/linimasa`

**Status:** Draft untuk review. Belum ada baris kode ditulis.
**Sumber ide:** `docs/design-kronik-pantai-barat-1600-1690.md` (design spec visual, stack AstroJS+FastAPI+Flask — ditulis utk platform berbeda, lihat §1).
**Konteks teknis saat ini:** `/linimasa` sudah LIVE (Django template + vanilla JS + SVG, endpoint `GET /api/research/linimasa`), 30 event tersitasi (1625–1681), dibangun sesi 2026-07-14. PRD ini menilai apa dari design spec yang bisa/harus diadopsi ke implementasi yang sudah ada, dan apa yang perlu diubah.

---

## 1. Kenapa Ada Gap Platform, dan Keputusan yang Diambil

Design spec sumber menulis arsitektur untuk **AstroJS (frontend) + FastAPI (data) + Flask (editorial/admin)**. Repo `westkust-routes` ini adalah **Django (frontend, `map_app`) + FastAPI (backend)** — tidak ada AstroJS atau Flask di mana pun di repo ini.

Preseden yang relevan (dari memori proyek): `design_handoff_salido_beranda/` (17MB aset desain AstroJS) pernah nyasar masuk repo ini, ternyata milik proyek terpisah `salido-web`. Kemungkinan besar file design spec ini bernasib sama — ditulis dengan asumsi platform `salido-web`, tapi disimpan di repo yang salah.

**User mengonfirmasi eksplisit: target-nya `/linimasa` di repo ini** (bukan migrasi ke salido-web). Keputusan kerja:

- **Adopsi penuh:** narasi historis, filosofi visual, sistem warna/tipografi (sudah cocok — `/linimasa` sudah pakai EB Garamond + Space Grotesk), prinsip aksesibilitas, model data konseptual (event + sumber + confidence).
- **Terjemahkan ke stack nyata:** komponen AstroJS (`ChronicleHero.astro`, dst.) → section dalam template Django tunggal `linimasa.html`, mengikuti pola `riset_jaringan.html` (SVG hand-rolled, vanilla JS, tanpa framework). Endpoint `GET /api/chronicle/events` yang diusulkan → sudah ADA sebagai `GET /api/research/linimasa`, tinggal diperluas field-nya (§5).
- **Tidak diadopsi (untuk sekarang):** lapisan editorial/admin Flask. `seed_linimasa_events.py` + CSV manual (`data/research/linimasa_events.csv`) sudah menjalankan fungsi kurasi yang sama persis (tambah baris, wajib `text_asli`, `confidence_flag`) — servis Flask terpisah akan jadi duplikasi infrastruktur tanpa kebutuhan nyata saat ini. Dicatat sebagai kemungkinan Fase Lanjutan (§8), bukan Fase 1.

---

## 2. Verifikasi Fakta Kunci Sebelum Desain Jalan

Design spec §2 secara eksplisit mensyaratkan: *"Urutan pergantian pemerintahan harus ditampilkan secara akurat... Sultan Iskandar Muda wafat [1636] → Sultan Iskandar Thani (1636–1641) → Sultanah Safiatuddin Syah (1641)."*

Dicek terhadap data primer yang sudah kita sisir (`atjeh_trade.csv`, `linimasa_events.csv`) dan corpus lebih luas (`docs/thesis/dr/korpus_tema_slim.csv`, 1005 baris):

| Klaim | Status di data kita |
|---|---|
| Iskandar Muda wafat, ~14 hari sebelumnya mencekik satu-satunya putra/pewaris | **ADA**, sumber primer OCR sendiri (`atjeh_trade.csv` source_page=99, vol.1637), sudah di linimasa event id terkait |
| **Iskandar Thani (1636–1641) sebagai sultan** | **TIDAK ADA** di kedua sumber — 3 kecocokan kata "Iskandar"/"Thani" di korpus luas semuanya false-positive (nama "Nathaniel", dan satu gelar "Paduca Sulthan Iskandar Sulcornenny" di vol.1668-1669 yang perlu verifikasi terpisah, bukan bukti langsung era 1636-1641) |
| Safiatuddin Syah mulai 1641 | **TIDAK LANGSUNG ADA** — data kita punya "Hare Maijt van Atchin" dikonfirmasi berkuasa 1644 (vol.1643-1644), bukan eksplisit 1641 |

**Temuan yang justru menguatkan**: catatan 1637 kita (raja mencekik satu-satunya putra pewaris sebelum wafat) **konsisten secara historis** dengan alasan Iskandar Thani (menantu, bukan anak kandung) naik takhta — anak kandung yang seharusnya mewarisi sudah dibunuh ayahnya sendiri. Sumber kita punya SEBAB-nya, tapi belum punya NAMA penerusnya.

**Keputusan**: bukan blocker untuk mulai Fase 1 (§7) karena struktur/desain bisa dibangun paralel, TAPI event 1636–1641 di linimasa **tidak boleh diklaim sebagai "Sultan Iskandar Thani"** sampai ada kutipan sumber primer. Sampai saat itu, timeline menampilkan gap eksplisit ("periode 1637–1644, penguasa antara Iskandar Muda dan konfirmasi ratu 1644 belum tersitasi") — bukan diisi diam-diam dari pengetahuan sejarah umum. Ini konsisten dengan prinsip design spec sendiri (§3.3: *"Pengelompokan era berdasarkan pengetahuan eksternal tanpa sumber yang dapat dilacak"* eksplisit masuk daftar yang harus dihindari) dan prinsip proyek ini sejak awal (`confidence_flag`, `text_asli` wajib).

**Tindak lanjut riset** (di luar scope PRD ini, tapi dicatat sbg prasyarat sebelum Bab III/IV design spec bisa diisi jujur): sisir volume Daghregister 1638–1642 (belum pernah disentuh) atau baca ulang vol.1668-1669 corpus_id=786 dgn konteks lebih luas utk konfirmasi/tolak "Paduca Sulthan Iskandar Sulcornenny".

---

## 3. Yang Sudah Cocok Tanpa Perubahan

Dibanding merancang dari nol, `/linimasa` versi sekarang sudah punya fondasi yang selaras dengan design spec:

- **Tipografi & warna**: EB Garamond (judul/kutipan) + Space Grotesk (nav/label) — identik dengan §7.2 design spec. Palet saat ini (`--evt-suksesi`, dst.) bisa diperluas ke palet arsip §7.1 (`--paper`, `--archive-gold`, `--sea-ink`) tanpa konflik.
- **Prinsip anti-JS-dependency**: linimasa saat ini render kartu via `fetch()` — BEDA dari prinsip §3.3/§12.2 design spec ("konten utama tidak boleh bergantung penuh pada JavaScript", "seluruh event dapat dibaca tanpa JavaScript"). **Ini gap nyata**, dicatat di §6.
- **Model kepercayaan sumber**: `confidence_flag`, `text_asli` wajib, provenance dua-pipeline (OCR sendiri vs `korpus_tema_slim.csv`) — sudah lebih ketat dari draf skema §10 design spec (yang cuma punya field `confidence: "unverified"` generik tanpa pemisahan sumber).
- **Traktat Painan sebagai klimaks naratif**: sudah jadi anchor event di data kita (4 baris, 1662-63), cocok jadi Bab V design spec.
- **Reciprocal links & noindex**: sudah ada, konsisten pola 3 halaman riset lain.

---

## 4. Gap Nyata yang Perlu Diputuskan

| Gap | Design spec minta | Kondisi sekarang | Dampak |
|---|---|---|---|
| **SSR / no-JS fallback** | Konten utama HTML semantik dari awal (Astro server-render) | Django render shell kosong, JS `fetch()` isi kartu — kalau JS gagal, halaman kosong total | **Tinggi** — pelanggaran prinsip aksesibilitas eksplisit di §12.2 |
| **Narasi berbab (Prolog–Epilog, 7 babak)** | Struktur naratif dgn headline & copy per babak, bukan cuma list kronologis | Linimasa sekarang murni list event terurut tahun + filter jenis | **Sedang** — perubahan struktur konten, bukan cuma gaya |
| **Peta interaktif + kapal animasi** | Peta SVG Sumatra dgn riak kekuasaan, pasang-surut, kapal bergerak per rute aktif | Tidak ada peta di `/linimasa` (peta VOC ada terpisah di `/` — atlas utama) | **Tinggi** — komponen visual baru sepenuhnya, effort besar |
| **Sinkronisasi scroll ↔ peta ↔ nav era** | `IntersectionObserver` tunggal menyinkronkan section aktif, peta, dan kapal | Tidak ada scroll-driven state di linimasa sekarang (klik-based) | **Sedang-Tinggi** — pola interaksi baru |
| **Cakupan tahun 1600–1690** | Prolog mulai 1600, Epilog sampai 1690 | Data kita 1625–1681 (title masih "Iskandar Muda ke Traktat Painan") | **Rendah-Sedang** — perlu riset tambahan 1600-1624 & 1682-1690, atau sesuaikan judul/scope ke rentang data yang benar-benar ada |
| **Wireframe 20/48/32 kolom (nav/peta/cerita)** | Layout 3-kolom sticky | Linimasa sekarang: header + axis SVG + card list, single column | **Sedang** — restrukturisasi layout |

---

## 5. Perluasan Model Data (bila Fase 1 dijalankan)

Skema `LinimasaEvent` sekarang sudah lebih kaya dari draf §10 design spec di beberapa hal (dua-pipeline provenance, `event_type` taksonomi 5 nilai). Yang **belum ada** dan perlu ditambah bila mau mendukung fitur peta+narasi-berbab:

```python
# tambahan potensial ke LinimasaEvent, BUKAN keputusan final -- didiskusikan di §7
era_slug = Column(String(40), nullable=True)      # "pusaran-menguat" | "arus-berbalik" | dst -- utk pengelompokan babak
location_fort_id = Column(Integer, ForeignKey("forts.id"), nullable=True)  # reuse tabel forts yg sudah ada (Aceh, Salido, dst sudah py koordinat)
headline = Column(String(200), nullable=True)     # copy dramaturgis pendek, terpisah dari `title` yg lebih deskriptif-faktual
```

`location_fort_id` penting: design spec §10 mengusulkan `lat`/`lng` baru per event, tapi tabel `forts` **sudah punya koordinat semua pelabuhan relevan** (Aceh, Salido, Tiku, Pariaman, Inderapura, dst — dipakai atlas utama). Reuse ini menghindari duplikasi data lokasi.

---

## 6. Rekomendasi Fase 1 (Scope Realistis)

Design spec §13 (Fase 1–6) ditulis untuk build dari nol di AstroJS. Karena `/linimasa` sudah live dan dipakai, Fase 1 yang diusulkan di sini **bukan rebuild total**, tapi penambahan bertahap di atas fondasi yang ada:

1. **SSR fallback** (gap tertinggi dampaknya, effort kecil): render kartu event langsung di template Django (`{% for %}` dari context, bukan cuma `fetch()` client-side) — JS jadi enhancement (filter, klik-expand, animasi SVG), bukan syarat baca konten. Selaras §12.2 design spec DAN prinsip aksesibilitas proyek ini sendiri.
2. **Narasi berbab**: kelompokkan 30 event yang ADA ke dalam babak yang punya bukti (bukan skema 7-babak 1600-1690 penuh dulu) — mis. "Klaim Yurisdiksi Awal (1625-1637)", "Puncak & Ratu (1643-1657)", "Perang & Damai (1656-1659)", "Pemberontakan Painan (1660-1667)", "Penataan Ulang (1681)". Nama & batas babak historis (bukan gaya "Pusaran Menguat") ditentukan dari isi data, bukan diimpor mentah dari design spec yang mengasumsikan cakupan 1600-1690 lengkap.
3. **Palet & tone visual**: adopsi §7.1 palet arsip (`--paper`, `--archive-gold`, dll.) menggantikan palet putih-solid sekarang — perubahan CSS murni, effort rendah, dampak visual besar.
4. **Motion minimal**: riak kekuasaan (§8.2) sbg elemen dekoratif `aria-hidden`, HANYA di hero, bukan di seluruh timeline — hindari over-animasi yang dilarang §3.3 sendiri.

**Ditunda ke Fase Lanjutan** (effort besar, ketergantungan pada riset data tambahan):
- Peta interaktif + kapal animasi bersinkronisasi scroll.
- Cakupan penuh 1600–1690 (butuh sisir volume 1600-1624 yang belum disentuh, dan 1682-1690).
- Layanan editorial Flask terpisah.

---

## 7. Pertanyaan Terbuka untuk User

1. **Cakupan tahun**: kejar 1600–1690 penuh (butuh riset tambahan signifikan, minimal 2 volume baru: pra-1624 dan 1682+), atau judul/scope disesuaikan jujur ke rentang yang sudah tersitasi (1625–1681)?
2. **Prioritas Fase 1**: mulai dari SSR fallback + narasi berbab + palet (rendah risiko, cepat terlihat), atau langsung ke peta interaktif (paling sesuai visi design spec, tapi effort & risiko jauh lebih besar)?
3. **Iskandar Thani**: sisir volume 1638–1642 dulu sebelum Bab III/IV design spec ditulis dgn nama eksplisit, atau jalan dengan gap eksplisit dulu (§2) sambil riset berjalan paralel?
4. **Flask editorial**: benar-benar dibutuhkan, atau CSV+`seed_linimasa_events.py` yang sudah ada cukup sbg alur kurasi (menghindari servis baru tanpa kebutuhan nyata)?
