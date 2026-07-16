# PRD: Redesign Kronik Pantai Barat — Anti AI Slop

**Status:** Disetujui untuk eksekusi — mulai Sprint 1.
**Sumber:** `docs/audit-ux-ui-ai-slop-salido.md` (audit UX/UI senior manager) + temuan susulan dari `docs/audit-redesign-ruang-kosong-django-tailwind.md` (lihat §2b).
**Target:** `/linimasa` di repo ini (Django template + vanilla JS + SVG)
**Scope:** P0 + P1 + P2 (full scope sesuai audit §16) + item susulan §2b

**Sudah dikerjakan di luar sprint (fix bug, bukan keputusan desain):**
- Path gambar panggung peta (`#chrMap`) menunjuk ke `amh-5147-na.jpg` yang filenya sudah tidak ada (peninggalan folder `astro-linimasa` yang dihapus) — diganti ke `map_app/img/peta-untukruangtengah.png` (aset engraving resmi, sama dengan yang dipakai desainer di `Designer-fix.png`). Overlay opacity/filter (`opacity:.5; grayscale(60%); brightness(.7)`) **belum diubah** — itu keputusan P1.6, lihat §2b.

---

## 1. Konteks

Dokumen audit (`audit-ux-ui-slop-salido.md`) mengidentifikasi bahwa tampilan Kronik Salido terkesan "AI slop" — banyak elemen visual menarik secara individual, tapi tanpa hierarki, kurasi, dan keputusan desain yang tegas. Audit ditujukan untuk linimasa.html di repo ini (konfirmasi user), meski disebut "AstroJS" ( referensi ke proyek salido-web yang terpisah).

**Gap platform:** Spec desain asli menulis AstroJS + Flask. Repo ini Django + vanilla JS. Keputusan: adopsi penuh filosofi visual, tipografi, palet, dan prinsip aksesibilitas — terjemahkan ke stack Django yang sudah ada.

**Yang sudah cocok tanpa perubahan** (dari PRD sebelumnya §3):
- Tipografi: EB Garamond + Space Grotesk sudah digunakan
- Model kepercayaan sumber: `confidence_flag`, `text_asli` wajib
- Traktat Painan sebagai klimaks naratif
- SSR fallback untuk konten utama

---

## 2. Pemetaan Audit → Kode Saat Ini

| Temuan Audit | Lokasi di Kode | Masalah Spesifik |
|---|---|---|
| §4 Peta terlalu sibuk | `linimasa.html:1006-1084` (SVG stage build) | 14 port selalu terlihat, semua orbit + VOC lines + ripples + kompas + rhumb lines + hatching + ridges + ships muncul bersamaan |
| §5 Gaya kapal tidak konsisten | `linimasa.html:1069-1075` | Dua kapal SVG — satu `.chr-ship` (animasi), satu `.chr-ship2` (statis, scale .55) — meski path sama, opacity/ukuran beda terasa seperti gaya berbeda |
| §6 Sidebar kiri seperti admin | `linimasa.html:278-288` (`.chr-era`) | Dot `::before` menyerupai radio button; era aktif cuma beda warna dot + tampilkan summary |
| §7 Panel kanan generic drawer | `linimasa.html:1118-1146` (`renderPanel()`) | Struktur: live indicator → tahun besar → judul → badges → meta → quote → src → actions. Terasa seperti detail drawer dashboard |
| §8 Tipografi belum disutradarai | CSS `:root` + `.chr-*` classes | Sudah pakai 2 font, tapi treatment belum disiplin — tahun di panel pakai mono, di scrubber pakai mono, di card pakai mono — tidak ada hierarki ukuran yang jelas |
| §9 Garis rute = efek, bukan informasi | `linimasa.html:1064-1066` | Orbit emas (semua port → Aceh) + VOC lines (Batavia → Padang → 8 port) — semua muncul tanpa konteks event aktif |
| §10 Label bertabrakan | `linimasa.html:1078-1084` | 14 label port selalu tampil — cluster selatan (Tiku–Inderapura) sangat rapat |
| §11 Background/data tidak terpisah | `linimasa.html:294-298` (`.chr-stage::before`) | Static image + scrim gelap — tidak ada pemisahan layer atmosfer/geografi/peristiwa |
| §12 Tidak ada focal point stabil | `setActive()` di `linimasa.html:1152-1164` | Perhatian berpindah ke 7 tempat — tidak ada urutan visual yang disutradarai |
| §13 Proporsi mekanis | `linimasa.html:265-268` (grid) | `minmax(200px,19%) 1fr minmax(300px,29%)` — garis pemisah keras, panel statis |
| §14 Microcopy data mentah | `linimasa.html:1136` | `vol. CD1 · hlm. 47 (19–20) · unverified` — campur bahasa, istilah teknis |

---

## 2b. Temuan Susulan — Design Critique atas `Designer-fix.png`

Sesi critique terpisah membandingkan mockup final desainer (`docs/Designer-fix.png`) terhadap audit ruang kosong. Dua temuan tervalidasi terhadap kode saat ini, dua lainnya sudah tercakup rencana P0/P1 yang ada:

| Temuan | Lokasi di Kode | Status | Item Baru |
|---|---|---|---|
| Bar statistik (tiles) murni display, tidak ada afordansi klik/filter — padahal ini akar kesan "dashboard BI" | `linimasa.html:149-154` (`.tiles`, `.tile`), markup `:601-608` | Belum ada di P0/P1 manapun | **P0.8** (baru, lihat §4) |
| Kapal engraving pada panggung peta berisiko tenggelam overlay gelap | `linimasa.html:634-637` (`#chrMap` inline style `opacity:.5; grayscale(60%); brightness(.7)`) | Sudah tercakup **P1.6** — tapi asumsi lama P1.6 memakai gambar peta lama yang filenya hilang; sekarang aset benar (`peta-untukruangtengah.png`, 3 kapal terlihat jelas di sumber), overlay harus diverifikasi ulang supaya tidak menutupi kapal | Update catatan implementasi P1.6, bukan item baru |
| Risiko konflik tinggi viewport bila footer sumber (5/2-kolom) dan timeline scrubber tampil bersamaan di satu state | `linimasa.html:644-652` (`.chr-scrub--full`, mode peta) vs `:655-801` (`#listView` + `.sources-footer`, mode daftar) | **Sudah aman** — footer ada di dalam `#listView` yang di-`display:none` saat mode peta aktif (`.js #listView{display:none}` di `:307`); scrubber cuma tampil di mode peta. Tidak ada konflik di kode saat ini. | Tidak perlu perubahan — catat sebagai **constraint**: jangan pernah render `.sources-footer` dan `.chr-scrub--full` di viewport yang sama saat P1.7 (responsive) dikerjakan |
| Kontras kutipan sumber primer (italic, kecil, di atas background gelap) belum diverifikasi WCAG AA | `linimasa.html` — cari `.chr-quote` / `.quote` | Belum diverifikasi | Ditambahkan ke checklist verifikasi Sprint 2 (§8) |

**Koreksi ground-truth saat mulai eksekusi Sprint 1 (2026-07-16):** Audit asli (dan draft P0/P1 di atas) menyebut kompas, rhumb lines, hatching, ridge, coastline vector, ripple, dan dua kapal (`.chr-ship`/`.chr-ship2`) sebagai elemen yang perlu diredupkan/disederhanakan. Penelusuran kode saat ini menunjukkan **CSS untuk semua kelas itu (`.chr-compass`, `.chr-rhumb`, `.chr-ridge`, `.chr-hatch`, `.chr-coast`, `.chr-isle`, `.ripple`, `.chr-ship`, `.chr-ship2`, `.orbit`, `.vocline`) tidak pernah dipasang ke elemen HTML manapun** — tidak ada di markup statis maupun di-generate JS (satu-satunya builder overlay adalah `drawRoutes()` di `:964-1011`, yang memakai class `route-voc`/`route-orbit`, bukan `.vocline`/`.orbit`). Kesimpulan: panggung peta sudah disederhanakan sebelumnya dari sistem SVG schematic penuh menjadi gambar raster (`#chrMap`) + dot pelabuhan + garis rute JS — CSS lama untuk sistem SVG schematic itu jadi *dead code*. Dampak ke scope:

- **P0.2 dianggap tidak berlaku** — tidak ada elemen kapal di overlay interaktif untuk distandarisasi (kapal cuma ada sebagai bagian gambar statis `peta-untukruangtengah.png`)
- **P0.5 bagian kompas/rhumb/ridge/hatch dianggap tidak berlaku** — tidak pernah dirender, tidak perlu diredupkan
- **P0.1 & P0.6 tetap valid dan jadi prioritas nyata**: 14 garis `route-voc`/`route-orbit` selalu tampil statis (opacity .3–.35) tanpa filter terhadap event aktif — ini persis masalah audit §9 ("garis rute = efek, bukan informasi") dan belum diperbaiki. Port dot aktif/related/dormant **sudah** diimplementasi di `setActive()` (`:1138-1172`) — verifikasi saja, bukan build baru.
- Rekomendasi: hapus CSS dead code (`.chr-compass` dkk.) di sprint pembersihan terpisah agar tidak membingungkan kontributor berikutnya — di luar scope P0/P1 saat ini.

**Bug tambahan ditemukan saat verifikasi Sprint 1 (screenshot Playwright):** `#chrMapWrap` dikunci `aspect-ratio:3/2` (`linimasa.html:633`) padahal parent-nya (`.chr-stage`, flex column yang mengisi tinggi grid `100dvh`) lebih tinggi dari rasio itu — menyisakan celah kosong di bawah gambar peta yang menampakkan `.chr-stage::before` (background `linimasa-hero.jpg`, gambar berbeda) tembus, menciptakan efek "dua peta bertumpuk". **Sudah diperbaiki**: `aspect-ratio:3/2` diganti `flex:1;min-height:0` supaya gambar mengisi penuh panggung tanpa celah. Diverifikasi via screenshot Playwright — kapal dan kompas dari `peta-untukruangtengah.png` sekarang terlihat penuh, bukan cuma sepotong.

---

## 3. Prinsip Desain

Dari audit §15 — yang menjadi north star redesign:

1. **Satu metafora dominan:** arus kekuasaan dari Aceh
2. **Satu sistem ilustrasi:** engraving konsisten
3. **Informasi muncul berdasarkan konteks:** tidak semua elemen tampil sekaligus
4. **Setiap detail visual punya fungsi:** hapus dekorasi tanpa makna
5. **Ruang kosong mengarahkan perhatian**
6. **Teks melewati proses editorial:** bukan data mentah
7. **Berani menghapus:** radical subtraction

---

## 4. Fase P0 — Hilangkan Kesan Slop

### P0.1 Kurangi elemen SVG stage simultan

**Masalah:** Semua orbit, VOC lines, ripples, compass, rhumb lines tampil bersamaan.
**Solusi:** Dalam satu state peristiwa, tampilkan maksimal:
- 1 pusat riak (Aceh)
- 1 rute utama aktif (berdasarkan event)
- 1-2 rute sekunder (opacity rendah)
- 5-7 port relevan (bukan semua 14)
- 1 legenda kontekstual

**Implementasi:**
- Saat `setActive(i)`, tentukan port mana yang relevan dengan event (sudah ada `portOf()`)
- Port non-relevan: sembunyikan label, kecilkan node (radius 2px, opacity 0.3)
- Orbit hanya tampilkan untuk port aktif + 2 tetangga terdekat
- VOC lines: hanya tampilkan yang melewati port aktif
- Compass: sembunyikan saat event aktif (hanya tampil di state default/awal)
- Rhumb lines: opacity 0.04 (saat ini 0.08), atau sembunyikan total

**File:** `linimasa.html` — modifikasi `setActive()` dan SVG build section

### P0.2 Standarisasi kapal

**Masalah:** Dua kapal dengan ukuran/opacity berbeda terasa seperti gaya berbeda.
**Solusi:** Satu kapal aktif (bergerak di rute), satu kapal dekoratif (statis, jauh lebih redup).

**Implementasi:**
- `.chr-ship2`: opacity turun ke 0.15 (dari 0.45), scale tetap 0.55
- Kapal aktif: warna `#d8cdb8` (sudah benar), animasi `sail` tetap
- Pertimbangkan: kapal dekoratif dihapus total jika masih terasa ramai

**File:** `linimasa.html` — CSS `.chr-ship2`

### P0.3 Ubah sidebar era dari radio button ke bab editorial

**Masalah:** Dot `::before` menyerupai radio button / stepper formulir.
**Solusi:** Format bab kronik:

```
01
1600–1637

Kontrak Pertama
dan Kekuasaan
Iskandar Muda
```

**Implementasi:**
- Hapus `.chr-era::before` (dot radio button)
- Ganti dengan nomor bab (urutan 01, 02, 03...) menggunakan `::before` counter
- Tahun range tetap
- Label era: font EB Garamond (dari Space Grotesk)
- Gunakan garis vertikal tipis sebagai pengganti dot (timeline rail)
- Era aktif: teks lebih tebal + garis terisi (bukan dot berwarna)

**File:** `linimasa.html` — CSS `.chr-era`, `.chr-era::before`, `.chr-era.active`

### P0.4 Redesign panel kanan menjadi lembar editorial

**Masalah:** Panel terasa seperti detail drawer dashboard.
**Solusi:** Format editorial:

```
PERISTIWA 01 / 101

1600
────────────

Kontrak Dagang Lada Pertama
VOC–Aceh

PERJANJIAN · PERDAGANGAN

Desember 1600
Aceh Darussalam

Ringkasan editorial peristiwa...

SUMBER PRIMER
"Kutipan sumber..."

Arsip CD1
Halaman 47

Status: Belum diverifikasi silang

[Baca transkrip]
Tampilkan pada peta →
```

**Implementasi:**
- Modifikasi `renderPanel()` di `linimasa.html:1121-1146`
- Tambahkan counter "PERISTIWA X / 101" (dari `active + 1` dan `SEQ.length`)
- Tahun berdiri sendiri, terpisah dari judul
- Garis horizontal pemisah setelah tahun
- Subtitle kota/lokasi di bawah judul
- Metadata source: bahasa Indonesia, bukan campur
- Tombol: "Baca transkrip" (sudah ada) + "Tampilkan pada peta" (ganti "Lihat di peta")
- Sembunyikan `confidence_flag` raw — ganti dengan status editorial

**File:** `linimasa.html` — fungsi `renderPanel()`

### P0.5 Hilangkan elemen tanpa makna langsung

**Daftar hapus/redupkan:**
- Orbit elips: sembunyikan saat event aktif (hanya tampil di state awal "semua rute")
- Panah kecil di sepanjang pesisir: tidak ada di kode saat ini (audit mungkin merujuk ke design lain) — skip
- Rhumb lines (kompas portolan): opacity dari 0.08 ke 0.03, atau hapus
- Kompas mawar: sembunyikan saat event aktif (`.chr-stage[data-era] .chr-compass { opacity: 0 }`)
- Label "SUMATRA" (landname): opacity dari 0.26 ke 0.12

**File:** `linimasa.html` — CSS rules untuk `.orbit`, `.chr-rhumb`, `.chr-compass`, `.chr-landname`

### P0.6 Tetapkan satu focal point per state

**Focal path yang ideal (audit §12):**
1. Tahun dan judul peristiwa (panel kanan atas)
2. Lokasi aktif pada peta (node emas bercahaya)
3. Rute yang menjelaskan hubungan (1 garis utama)
4. Konteks era (sidebar)
5. Sumber primer (panel kanan bawah)

**Implementasi:**
- Node port aktif: `r=8` + `fill:#e3c15c` + animated halo (sudah ada)
- Port lain: `r=2.5`, `opacity:0.25`, no label
- Rute utama: `stroke-width:2`, `opacity:0.8`
- Rute sekunder: `stroke-width:1`, `opacity:0.2`
- Panel kanan: tahun + judul harus paling terang dan paling besar

### P0.7 Microcopy bahasa Indonesia

**Masalah:** `vol. CD1 · hlm. 47 (19–20) · unverified`
**Solusi:**

```
STATUS SUMBER
Belum diverifikasi silang

Arsip CD1
Halaman 47
```

**Implementasi:**
- Di `renderPanel()`: format ulang `.chr-src`
- `confidence_flag: "unverified"` → "Belum diverifikasi silang"
- `confidence_flag: "verified"` → "Terverifikasi silang"
- `source_document` → "Arsip CD1" (bukan "vol. CD1")
- `source_page` → "Halaman 47" (bukan "hlm. 47")
- Hapus `book_page` dari tampilan utama (simpan di tooltip/hover)
- Konsistensi: "Aceh" di narasi modern, "Atjeh" hanya di kutipan sumber

**File:** `linimasa.html` — fungsi `renderPanel()`, juga template kartu di `#listView`

### P0.8 Statistik sebagai filter interaktif (baru, dari §2b)

**Masalah:** `.tiles` di header (`101 peristiwa`, `4 suksesi`, `51 perjanjian`, dst.) murni display — tanpa afordansi klik, semua kotak berbobot visual sama. Ini akar kesan "dashboard BI" yang justru disebut sebagai masalah inti, bukan cuma efek samping ruang kosong.

**Solusi:**
- `101 peristiwa` dan rentang tahun (`1600–1775`) tetap sebagai anchor metric — beri ukuran font/berat lebih besar daripada tile kategori (bukan grid seragam seperti sekarang)
- Tile kategori (`suksesi`, `perjanjian`, `konflik`, `diplomasi`, `administratif`) jadi `<button>` yang mem-filter `#listView` dan menyorot event bertipe sama di panggung peta/scrubber
- State aktif: background gading solid; state lain: border tipis (selaras token warna P1.1)
- `aria-pressed` pada tiap tile-button, `:focus-visible` eksplisit

**Implementasi:**
- Ubah markup `.tile` di `:601-607` dari `<div>` ke `<button type="button" data-filter="perjanjian">`
- Tambah handler klik yang reuse logic filter yang sudah ada di `#typeFilter` (`:670-677`) supaya satu sumber kebenaran filter, bukan duplikasi state
- CSS: pisahkan `.tile--primary` (peristiwa + rentang tahun, font lebih besar) dari `.tile--filter` (kategori, interaktif)

**File:** `linimasa.html` — markup `.tiles` (`:601-608`), CSS `.tile`, JS filter handler

---

## 5. Fase P1 — Bangun Sistem Visual

### P1.1 Semantik warna dan garis

Dari audit §9 — formalisasikan makna setiap elemen visual:

| Elemen | Makna | Warna/Style |
|---|---|---|
| Riak konsentris | Pusat kekuasaan Aceh | `#e3c15c`, `stroke-width:1.2` |
| Garis emas solid | Pengaruh politik Aceh | `#c49a47`, `stroke-dasharray:none` |
| Garis tembaga putus | Rute VOC | `#a04a35`, `stroke-dasharray:7 4` |
| Node emas | Port aktif (event) | `fill:#e3c15c`, `r:8` |
| Node putih | Port terkait | `fill:#f3ead9`, `r:4.5` |
| Node abu-abu | Port tidak relevan | `fill:#f3ead9`, `opacity:0.25`, `r:2.5` |

**Implementasi:**
- Buat CSS custom properties baru: `--route-aceh`, `--route-voc`, `--route-local`, `--node-active`, `--node-related`, `--node-dormant`
- Terapkan ke SVG elements yang sudah ada
- Hapus SEMUA orbit emas (ganti dengan 1 garis solid Aceh→port aktif)

**File:** `linimasa.html` — `:root` CSS vars + SVG build

### P1.2 Sistem ukuran kapal dan node

| Elemen | Ukuran | Keterangan |
|---|---|---|
| Aceh (pusat) | `r:8` + halo | Selalu paling besar |
| Port aktif | `r:6` + gold fill | Muncul saat event |
| Port terkait | `r:4.5` + white fill | Tetangga dalam rute |
| Port dorman | `r:2.5` + low opacity | Tidak relevan |
| Kapal aktif | `scale:1` + animasi | Bergerak di rute |
| Kapal dekoratif | `scale:0.4` + opacity 0.12 | Statis, background |

### P1.3 Batasi tipografi

Dari audit §8:

| Elemen | Font | Size | Weight |
|---|---|---|---|
| Tahun (panel) | EB Garamond | 2.5rem | 600 |
| Judul peristiwa | EB Garamond | 1.3rem | 600 |
| Kutipan sumber | EB Garamond italic | 0.93rem | 400 |
| Narasi era | EB Garamond | 1.05rem | 400 |
| Label port (SVG) | Space Grotesk | 10.5px | 600 |
| Navigasi era | Space Grotesk | 0.94rem | 600 |
| Metadata | Space Grotesk | 0.8rem | 400 |
| Badge event type | Space Grotesk | 0.68rem | 600 |
| Tombol | Space Grotesk | 0.78rem | 600 |

**Implementasi:**
- Tahun di panel: ganti dari `var(--mono)` ke `var(--serif)` — konsisten dengan audit §8
- Tahun di scrubber: tetap mono (tabular nums untuk alignment)
- Judul era di sidebar: ganti ke EB Garamond (sudah benar di `.era-label`)

**File:** `linimasa.html` — CSS `.chr-year`, `.chr-title`, `.era-label`

### P1.4 Ubah sidebar kiri menjadi daftar bab kronik

Dari P0.3 + enhancement:

```
┌──────────────┐
│ BAB KRONIK   │
│              │
│ ────────── 01
│ 1600–1637    │
│              │
│ Kontrak      │
│ Pertama &    │
│ Kekuasaan    │
│ Iskandar Muda│
│              │
│ ────────── ● 02  ← aktif
│ 1641–1650    │
│              │
│ Ratu Atjeh & │
│ Puncak       │
│ Kekuasaan    │
│              │
│ ────────── 03
│ ...          │
└──────────────┘
```

**Implementasi:**
- Garis vertikal tipis di kiri (timeline rail)
- Nomor bab di atas garis
- Tahun range di bawah nomor
- Label judul: EB Garamond, wrap natural
- Era aktif: garis terisi emas, judul lebih gelap
- Era lain: garis abu-abu tipis, judul muted
- Hilangkan headline/summary dari sidebar (pindah ke panel kanan atau hapus)
- `overflow-y:auto` + `scroll-snap` untuk navigasi panjang

**File:** `linimasa.html` — CSS `.chr-nav`, `.chr-era`, `.chr-era::before`

### P1.5 Buat legenda kontekstual

Saat ini legenda statis (`.chr-legend`). Ubah menjadi dinamis:

```
┌─────────────────────┐
│ ● Aceh (pusat)      │
│ ─ Rute aktif        │
│ ·· Rute terkait     │
│ ○ Port aktif        │
│ ○ Port terkait      │
└─────────────────────┘
```

- Hanya tampilkan elemen yang ADA di state saat ini
- Sembunyikan legenda saat compass/rhumb lines tidak terlihat
- Format: horizontal di bawah scrubber, bukan overlay kiri bawah

**File:** `linimasa.html` — buat `renderLegend()` baru, CSS `.chr-legend`

### P1.6 Pisahkan layer atmosfer/geografi/peristiwa

Dari audit §11:

| Layer | Isi | Z-index |
|---|---|---|
| ATMOSFER | Background image, vignette, texture | 0 |
| GEOGRAFI | Coastline, islands, equator, labels, Bukit Barisan | 1 |
| PERISTIWA | Routes, active port, ripples, ship, annotations | 2 |

**Implementasi:**
- Saat event aktif: `.chr-stage::before` opacity turun (image lebih redup)
- Coastline + islands: tetap visible tapi muted
- Routes + active port: paling tajam dan kontras
- Ripple Aceh: opacity mengikuti era (sudah ada di CSS `data-era` rules)
- **Update (§2b):** aset `#chrMap` sekarang benar (`peta-untukruangtengah.png`, 3 kapal engraving terlihat jelas di sumber asli). Inline style saat ini (`opacity:.5; grayscale(60%); brightness(.7)` di `linimasa.html:636`) belum diverifikasi terhadap aset baru — cek apakah kombinasi ini masih menenggelamkan siluet kapal. Jika ya, naikkan opacity dasar atau turunkan darkness overlay `#chrMapOverlay` (`:638`), bukan menghapus kapal dari aset

**File:** `linimasa.html` — CSS `.chr-stage::before`, `.chr-coast`, `.chr-isle`, inline style `#chrMap`

### P1.7 Responsive: panel kanan menyempit/melebar

Dari audit §13:
- Saat eksplorasi peta: panel kanan menyempit (300px)
- Saat membaca sumber: panel kanan melebar (400px)
- Panel kiri: rail yang lebih ringan (180px → 160px)

**Implementasi:**
- Tambahkan state "reading mode" yang dipicu saat user klik "Baca transkrip"
- CSS transition pada `grid-template-columns`
- Mobile (< 980px): sudah single column, pertahankan

**File:** `linimasa.html` — CSS `.chronicle` grid, JS state management

---

## 6. Fase P2 — Motion Setelah Desain Statis Matang

### P2.1 Riak Aceh bergerak lambat

Sudah ada animasi `.ripple` (4.8s linear infinite). Pertahankan, tapi pastikan:
- Hanya muncul saat Aceh adalah pusat kekuasaan aktif
- `prefers-reduced-motion` sudah didukung (sudah ada)
- Durasi bisa diperlambat ke 6s untuk kesan lebih tenang

### P2.2 Satu kapal bergerak pada rute aktif

Sudah ada animasi `.chr-ship` (26s ease-in-out infinite alternate). Enhancement:
- Animasi kapal mengikuti path rute aktif (bukan translate statis)
- Implementasi: `offset-path` + `offset-distance` pada SVG ship
- Fallback: tetap translate statis jika browser tidak support

### P2.3 Rute tergambar secara bertahap

Saat event berubah, garis rute "tertulis" dari port asal ke port tujuan:
- Gunakan `stroke-dashoffset` animation
- Durasi: 800ms ease
- Hanya pada transisi antar event (bukan saat load pertama)

### P2.4 Perubahan era memudarkan layer lama

Saat user pindah era:
- Layer atmosfer: opacity transition 600ms
- Port lama: fade out 400ms
- Port baru: fade in 400ms (staggered 100ms per port)

### P2.5 prefers-reduced-motion

**Wajib didukung** (audit §16 P2.6):
- Semua animasi dihentikan
- Transisi tetap jalan (opacity, transform) tanpa `animation`
- Kapal statis di posisi tengah rute
- Ripples statis di scale 0.5, opacity 0.3

Sudah ada di kode saat ini — pastikan SEMUA animasi baru juga punya fallback ini.

---

## 7. File yang Diubah

| File | Perubahan |
|---|---|
| `frontend/map_app/templates/map_app/linimasa.html` | CSS: P0.3, P0.5, P1.1, P1.3, P1.4, P1.6, P1.7, P2.1-P2.5. JS: P0.1, P0.2, P0.4, P0.6, P0.7, P0.8, P1.2, P1.5. HTML: legenda dinamis, `.tiles` → filter buttons |
| `frontend/map_app/static/map_app/img/peta-untukruangtengah.png` | **Sudah ditambahkan** — aset panggung peta pengganti `amh-5147-na.jpg` yang hilang |
| `frontend/map_app/views.py` | Tidak berubah (data model sudah cukup) |
| `backend/models.py` | Tidak berubah |
| `backend/routers/research.py` | Tidak berubah |

**Total: 1 file utama** (`linimasa.html`) — semua perubahan CSS + JS + SVG inline.

---

## 8. Urutan Implementasi

### Sprint 1: Radical Subtraction (P0)
0. ~~Fix aset panggung peta (`amh-5147-na.jpg` hilang → `peta-untukruangtengah.png`)~~ — **selesai di luar sprint**, prasyarat sebelum verifikasi P1.6
1. P0.1 — Kurangi elemen SVG simultan (port, orbit, rute)
2. P0.5 — Hapus/redupkan elemen tanpa makna
3. P0.2 — Standarisasi kapal
4. P0.6 — Tetapkan focal point per state
5. **Verifikasi:** Buka `/linimasa`, pastikan tampilan lebih bersih, fokus ke event aktif; pastikan gambar panggung peta termuat (bukan broken image) — **SELESAI (2026-07-16)**, diverifikasi via Playwright headless: gambar termuat, filter rute aktif/sekunder/dorman bekerja di 6 event/port berbeda, tanpa console/page error, celah kosong `#chrMapWrap` diperbaiki (`flex:1` ganti `aspect-ratio:3/2`)

### Sprint 2: Editorial Polish (P0 continued)
6. P0.3 — Ubah sidebar ke format bab kronik
7. P0.4 — Redesign panel kanan ke lembar editorial
8. P0.7 — Microcopy bahasa Indonesia
9. P0.8 — Statistik sebagai filter interaktif (baru, §2b)
10. **Verifikasi:** Bandingkan dengan wireframe audit §17; cek kontras `.chr-quote`/`.quote` (kutipan sumber primer) terhadap WCAG AA; cek `aria-pressed` dan `:focus-visible` pada tile filter baru

### Sprint 3: Sistem Visual (P1)
10. P1.1 — Semantik warna dan garis
11. P1.2 — Sistem ukuran node
12. P1.3 — Batasi tipografi
13. P1.5 — Legenda kontekstual
14. **Verifikasi:** Periksa konsistensi semua elemen visual

### Sprint 4: Layout & Motion (P1 + P2)
15. P1.4 — Sidebar bab kronik (enhanced)
16. P1.6 — Pisahkan layer
17. P1.7 — Responsive panel
18. P2.1-P2.5 — Motion system
19. **Verifikasi:** Full test aksesibilitas + `prefers-reduced-motion`

---

## 9. Kriteria Keberhasilan

Dari audit §19 — target penilaian:

| Aspek | Saat ini | Target | Cara Ukur |
|---|---|---|---|
| Hierarki informasi | 4.5/10 | 9/10 | User test: "Apa peristiwa pertama yang kamu lihat?" → harus tahun + judul |
| Konsistensi ilustrasi | 4/10 | 8.5/10 | Audit visual: semua kapal = 1 gaya, semua node = 3 state |
| Keterbacaan peta | 4/10 | 8.5/10 | Jumlah elemen visible simultan ≤ 12 (dari ~25 saat ini) |
| Editorial polish | 5/10 | 9/10 | Microcopy bahasa Indonesia konsisten, tidak ada data mentah |
| Kesan dirancang manusia | 4.5/10 | 9/10 | Cek §15 checklist: 1 metafora dominan, 1 sistem ilustrasi, ruang kosong sengaja |

**Checklist audit §15 "Terlihat didesain manusia":**
- [ ] Satu metafora dominan (arus kekuasaan Aceh)
- [ ] Satu sistem ilustrasi (engraving konsisten)
- [ ] Informasi muncul berdasarkan konteks
- [ ] Setiap detail visual punya fungsi
- [ ] Ruang kosong mengarahkan perhatian
- [ ] Teks melewati proses editorial
- [ ] Semua elemen dapat dijelaskan maknanya
- [ ] Sebagian besar dekorasi berani dihapus

---

## 10. Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Terlalu banyak pengurangan → tampilan kosong | User bingung tidak ada yang dieksplorasi | Pertahankan 1 rute utama + 5-7 port + 1 kapal — minimalis bukan kosong |
| Sidebar editorial terlalu tinggi | User harus scroll panjang | Batasi 5 era (sudah ada), gunakan scroll snap |
| Panel kanan terlalu banyak teks | User overwhelmed | Gunakan progressive disclosure: ringkasan → kutipan → transkrip |
| SVG path berubah → broken di mobile | Layout rusak | Test di 375px width, pastikan viewBox scale |
| Motion mengganggu pembacaan | User tidak bisa fokus baca | `prefers-reduced-motion` + pause button |

---

## 11. Pertanyaan Terbuka

1. **Kapal dekoratif:** hapus total atau pertahankan dengan opacity sangat rendah (0.08)?
2. **Rhumb lines (kompas portolan):** hapus total atau pertahankan sebagai elemen arsip redup?
3. **Headline era di sidebar:** pertahankan atau pindahkan ke panel kanan?
4. **Treaty highlight (Traktat Painan):** pertahankan treatment khusus atau standardisasi ke format panel lain?
5. **Angka counter "PERISTIWA X / 101":** tampil selalu atau hanya saat hover/focus?
