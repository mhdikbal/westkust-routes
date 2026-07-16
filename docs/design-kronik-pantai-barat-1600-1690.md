# Design Specification — Kronik Pantai Barat Sumatra 1600–1690

**Produk:** Linimasa interaktif Salido  
**Platform:** Web desktop berbasis AstroJS  
**Layanan data:** FastAPI  
**Editorial/admin:** Flask  
**Arah desain:** Historical editorial, maritime, archival, cinematic, accessible  
**Konsep utama:** **Pusaran Kuasa — Arus yang Berbalik**

---

## 1. Ringkasan Eksekutif

Aplikasi linimasa tidak dirancang sebagai daftar tahun, scatter plot, atau dashboard data. Pengalaman harus menggambarkan perubahan kekuasaan seperti dinamika laut:

> **Aceh menjadi pusat pusaran; pelabuhan Pantai Barat masuk ke orbit kekuasaan; perdagangan, izin, dan diplomasi memperkuat jaringan; kemudian arus melemah dan berbalik menjelang Traktat Painan 1663.**

Pengguna tidak sekadar membaca data. Pengguna mengikuti **arus sejarah** yang menghubungkan Aceh, pelabuhan Pantai Barat Sumatra, izin perdagangan, kapal VOC, pergantian pemerintahan, serta perubahan tatanan politik sampai 1690.

### Prinsip pengalaman

- **Pusaran** menggambarkan pemusatan kekuasaan.
- **Riak** menggambarkan luas dan intensitas pengaruh.
- **Pasang-surut** menggambarkan perubahan stabilitas politik.
- **Kapal** menggambarkan perdagangan yang bergantung pada izin dan diplomasi.
- **Perubahan arah arus pada 1663** menggambarkan bergesernya tatanan Pantai Barat.
- **Peta** adalah ruang naratif, bukan sekadar ilustrasi latar.
- **Sumber primer** selalu menjadi fondasi setiap klaim peristiwa.

---

## 2. Ketepatan Urutan Narasi

Urutan pergantian pemerintahan harus ditampilkan secara akurat dan tidak disederhanakan sebagai perpindahan langsung dari Sultan Iskandar Muda kepada Sultanah.

```text
1636
Sultan Iskandar Muda wafat

1636–1641
Pemerintahan Sultan Iskandar Thani

1641
Pemerintahan Sultanah Safiatuddin Syah dimulai
```

Pergantian tersebut menjadi jembatan dramaturgi dari puncak hegemoni menuju perubahan metode pengendalian jaringan Pantai Barat.

---

## 3. Filosofi Visual

### 3.1 Metafora utama

Linimasa diperlakukan sebagai **laut sejarah**, bukan garis waktu mekanis.

```text
Pusat kekuasaan  → pusaran
Pengaruh         → riak konsentris
Perdagangan      → jalur kapal
Izin             → terbukanya rute
Ketidakstabilan  → pasang-surut
Pergeseran kuasa → perubahan arah arus
Sumber primer    → tinta dan lembar arsip
```

### 3.2 Karakter yang harus terasa

- Editorial
- Historis
- Maritim
- Akademik
- Kuratorial
- Sinematik tetapi tidak teatrikal berlebihan
- Kaya atmosfer tetapi tetap mudah dibaca
- Tidak menyerupai dashboard admin
- Tidak menyerupai permainan atau landing page startup

### 3.3 Hal yang harus dihindari

- Animasi bounce, spring, flip, atau zoom berlebihan
- Bayangan kartu tebal
- Gradient neon
- Efek kaca modern yang dominan
- Terlalu banyak kapal bergerak sekaligus
- Scroll locking
- Konten penting yang bergantung penuh pada JavaScript
- Pengelompokan era berdasarkan pengetahuan eksternal tanpa sumber yang dapat dilacak

---

## 4. Struktur Naratif 1600–1690

### Prolog — Laut Sebelum Pusaran

**Periode:** 1600–1607

Pantai Barat ditampilkan sebagai jaringan pelabuhan, bandar, perdagangan, dan kekuasaan lokal yang belum sepenuhnya berada dalam satu orbit.

**Visual:**

- Permukaan laut tenang.
- Garis pantai Sumatra berupa engraving tipis.
- Titik pelabuhan menyala perlahan.
- Satu atau dua kapal lokal bergerak kecil di kejauhan.
- Belum ada pusaran dominan.

**Copy utama:**

> Sebelum kekuasaan berpusat, pantai barat adalah jaringan pelabuhan, bandar, dan jalur dagang yang saling berhubungan.

---

### Bab I — Pusaran Menguat

**Periode:** 1607–1636

Pusat gravitasi visual bergerak ke Aceh. Arus mulai mengikuti garis pesisir menuju pelabuhan Pantai Barat seperti Barus, Tiku, Pariaman, Padang, Salido, Painan, dan Inderapura.

**Visual:**

- Riak konsentris muncul dari Aceh.
- Jalur pesisir berkembang secara bertahap.
- Pelabuhan yang masuk orbit berubah dari abu-abu menjadi emas-tinta.
- Kapal dagang mengikuti arus.
- Besar pusaran meningkat sesuai perkembangan hegemoni.

**Headline:**

> Kekuasaan Datang dari Utara

**Tujuan UX:**

Pengguna melihat pelabuhan-pelabuhan memasuki medan gravitasi politik yang sama, bukan hanya membaca klaim penguasaan dalam daftar teks.

---

### Bab II — Izin, Dagang, dan Pengawasan

**Periode:** Puncak pemerintahan Sultan Iskandar Muda

Perdagangan divisualisasikan sebagai instrumen politik. Izin berdagang adalah pintu masuk ke dalam ruang kekuasaan.

**Visual:**

- Kapal VOC muncul dari sisi Samudra Hindia.
- Kapal berhenti di batas orbit sebelum izin aktif.
- Jalur pelayaran terbuka setelah peristiwa izin dipilih.
- Cap arsip muncul seperti tinta yang meresap.

**Copy utama:**

> Laut terbuka, tetapi perdagangan tidak bebas. Setiap kapal memasuki ruang yang dibentuk oleh izin, upeti, diplomasi, dan kekuasaan.

**Informasi saat hover/focus kapal:**

```text
Kapal dagang
Asal: Batavia
Tujuan: Pantai Barat
Status: Memerlukan izin
```

**Setelah event dipilih:**

```text
Izin diberikan
Rute aktif
Sumber primer tersedia
```

---

### Bab III — Pusat Kehilangan Pemegangnya

**Periode:** 1636–1641

Wafatnya Sultan Iskandar Muda menjadi perubahan atmosfer besar, bukan sekadar kartu event.

**Visual:**

- Pusaran berhenti membesar.
- Ritme gelombang melambat.
- Intensitas emas berkurang.
- Kapal tetap bergerak karena sistem belum langsung runtuh.
- Transisi 1641 memperkenalkan pemerintahan Sultanah Safiatuddin Syah.

**Copy transisi:**

> Pusat kekuasaan kehilangan pemegangnya, tetapi orbit yang dibentuknya belum serta-merta menghilang.

---

### Bab IV — Pasang Surut Kekuasaan

**Periode:** 1641–1662

Pemerintahan Sultanah tidak digambarkan sebagai keruntuhan langsung. Visual harus menunjukkan perubahan cara kekuasaan dipertahankan dan meningkatnya tekanan terhadap jaringan Pantai Barat.

**Visual:**

- Garis orbit menjadi lebih tipis.
- Beberapa pelabuhan berkedip antara emas dan tembaga.
- Gerak pasang-surut makin terlihat.
- Jalur VOC bertambah tegas.
- Jalur Aceh tetap hadir tetapi tidak lagi menjadi satu-satunya arus.

**Sistem arus:**

```text
Arus Aceh → emas gelap
Arus VOC  → tembaga atau merah-tanah
```

Warna tidak boleh terasa seperti peta geopolitik modern. Seluruh visual tetap berada dalam spektrum arsip.

---

### Bab V — Arus Berbalik

**Peristiwa klimaks:** Traktat Painan 1663

Saat pengguna mencapai 1663:

1. Gerak visual melambat tanpa mengunci scroll.
2. Kapal berhenti sesaat.
3. Riak dari Aceh mereda.
4. Garis Pantai Barat menjadi lebih jelas.
5. Jalur VOC menyala dari laut menuju pelabuhan.
6. Angka **1663** memenuhi bidang visual.
7. Judul **Traktat Painan** muncul.

**Headline:**

> Arus Tidak Lagi Menuju Satu Pusat

**Copy pendamping:**

> Traktat Painan menandai perubahan besar dalam hubungan kekuasaan, perdagangan, dan persekutuan di Pantai Barat Sumatra.

Perubahan tidak divisualisasikan sebagai ledakan atau peta yang pecah, tetapi sebagai arah arus yang perlahan berbalik.

---

### Epilog — Pantai Barat Setelah Pusaran

**Periode:** 1663–1690

Bagian akhir menampilkan jaringan kekuasaan baru, bukan ruang kosong setelah keruntuhan.

**Visual:**

- Pusaran besar menghilang.
- Beberapa arus kecil muncul.
- Pelabuhan menjadi node dengan hubungan beragam.
- Kapal VOC semakin sering terlihat, tetapi tetap dibatasi agar tidak ramai.
- Kabut peta berkurang.
- Linimasa tetap berlanjut sampai 1690.

**Copy utama:**

> Kekuasaan tidak lenyap. Kekuasaan berganti bentuk, berpindah jalur, dan menemukan pusat-pusat baru.

---

## 5. Wireframe Desktop

```text
┌────────────────────────────────────────────────────────────────────┐
│ HEADER SALIDO                                                      │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  KRONIK PANTAI BARAT                    PETA SUMATRA                │
│  1600—1690                                + ARUS LAUT               │
│                                                                    │
│  Pusaran Kuasa,                         ◉ Aceh                      │
│  Arus yang Berbalik                      ╰──── Barus                │
│                                             ╰── Tiku                │
│  [Mulai Menelusuri]                         ╰ Padang                │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│ BAB AKTIF          TAHUN BESAR            EVENT AKTIF              │
│ Pusaran Menguat    1632                   Izin dagang               │
│                    │                      Kutipan primer            │
│ 1600 ○             ●────────────────      Interpretasi             │
│ 1636 ●             │                      [Buka sumber]             │
│ 1641 ○             │                                               │
│ 1663 ○             │                      Kapal bergerak di peta    │
│ 1690 ○             │                                               │
└────────────────────────────────────────────────────────────────────┘
```

### Pembagian layar

- **20% kiri:** navigasi bab dan tahun, sticky.
- **48% tengah:** peta, arus, kapal, dan visualisasi waktu.
- **32% kanan:** cerita, peristiwa, sumber, dan kutipan.
- **Lebar konten maksimum:** sekitar 1440 px.
- Ruang pada monitor besar digunakan sebagai napas visual, bukan untuk memperbesar semua elemen.

---

## 6. Komponen Antarmuka

### 6.1 Hero Kronik

```text
KRONIK PANTAI BARAT SUMATRA
1600—1690

Pusaran Kuasa,
Arus yang Berbalik

Sembilan dekade perubahan kekuasaan,
perdagangan, dan diplomasi di Pantai Barat.

[Mulai Menelusuri]
```

Hero menggunakan peta Pantai Barat beresolusi tinggi dengan gerak parallax sangat halus. Angka tahun dapat berubah perlahan dari 1600 menuju 1690, tetapi tidak boleh mengganggu keterbacaan.

### 6.2 Navigasi era

```text
○ Laut Sebelum Pusaran
● Pusaran Menguat
○ Pusat Kehilangan Pemegangnya
○ Pasang Surut Kekuasaan
○ Arus Berbalik
○ Pantai Barat Setelah Pusaran
```

Navigasi bersifat sticky dan status aktif diperbarui oleh satu `IntersectionObserver`.

### 6.3 Event kronik

```text
1663
TRAKTAT PAINAN

Perjanjian · Diplomasi · Pergeseran Kekuasaan

Ringkasan naratif dua sampai tiga baris.

“Kutipan primer yang mendukung peristiwa...”

Sumber primer
Nama dokumen · Volume · Halaman

[Buka Transkrip]   [Tampilkan di Peta]
```

### 6.4 Tingkatan informasi

- **Level 1:** tahun dan headline.
- **Level 2:** kategori, tanggal, dan ringkasan.
- **Level 3:** kutipan primer dan terjemahan.
- **Level 4:** provenance, transkrip lengkap, dan catatan editorial.

### 6.5 Status sumber

Status tidak ditampilkan sebagai alarm merah. Gunakan label dokumenter:

```text
STATUS SUMBER
Belum diverifikasi silang
```

Catatan metodologi yang panjang dipindahkan ke panel yang dapat dibuka:

```text
Tentang sumber, batas bukti, dan metodologi
```

Konten tetap tersedia dalam HTML agar dapat diakses tanpa JavaScript.

---

## 7. Sistem Warna dan Tipografi

### 7.1 Palet

```css
:root {
  --paper: #f5f0e6;
  --paper-deep: #e8dfcf;
  --ink: #181611;
  --muted: #716b61;
  --archive-gold: #8c6a21;
  --aceh-gold: #a77a2e;
  --voc-copper: #8b4b33;
  --sea-ink: #29484b;
  --border: #d4c8b5;
}
```

### 7.2 Tipografi

- **Judul, tahun monumental, kutipan:** EB Garamond.
- **Navigasi, label, metadata, tombol:** Space Grotesk.
- Tahun menggunakan ukuran besar sebagai penanda ruang waktu, tetapi opacity harus rendah agar tidak mengalahkan judul peristiwa.
- Kutipan asli menggunakan italic serif dengan panjang baris yang terkendali.

---

## 8. Motion System

### 8.1 Prinsip motion

Animasi harus terasa seperti:

- kabut laut yang tersibak;
- tinta yang meresap ke kertas;
- halaman arsip yang ditemukan;
- arus yang perlahan berubah;
- pasang-surut yang tidak pernah benar-benar berhenti.

Animasi tidak boleh terasa seperti komponen UI modern yang dipamerkan.

### 8.2 Riak kekuasaan

Riak menggambarkan intensitas pengaruh.

```css
.power-ripple {
  position: absolute;
  width: 12rem;
  aspect-ratio: 1;
  border: 1px solid rgb(140 106 33 / 45%);
  border-radius: 50%;
  transform: scale(.35);
  opacity: 0;
  animation: archive-ripple 6s ease-out infinite;
}

.power-ripple:nth-child(2) {
  animation-delay: 2s;
}

.power-ripple:nth-child(3) {
  animation-delay: 4s;
}

@keyframes archive-ripple {
  0% {
    transform: scale(.35);
    opacity: 0;
  }

  18% {
    opacity: .6;
  }

  100% {
    transform: scale(2.2);
    opacity: 0;
  }
}
```

Riak bergerak lambat agar terbaca sebagai medan pengaruh, bukan loading indicator.

### 8.3 Pasang-surut

```css
.tide-layer {
  position: absolute;
  inset: auto -5% -6% -5%;
  height: 34%;
  border-radius: 50% 50% 0 0;
  background:
    linear-gradient(
      180deg,
      rgb(43 73 76 / 8%),
      rgb(43 73 76 / 24%)
    );
  transform-origin: center bottom;
  animation: tide 11s ease-in-out infinite alternate;
}

@keyframes tide {
  from {
    transform: translateY(8%) scaleX(1.02);
  }

  to {
    transform: translateY(-5%) scaleX(.98);
  }
}
```

Lapisan pasang-surut dibuat abstrak agar konsisten dengan estetika editorial.

### 8.4 Kapal dagang

Kapal bergerak hanya ketika rute terkait aktif.

```css
.trade-ship {
  offset-path: path("M 20 420 C 210 370, 390 270, 620 220");
  offset-rotate: auto;
  animation: sail-route 18s linear infinite;
}

@keyframes sail-route {
  from {
    offset-distance: 0%;
    opacity: 0;
  }

  8%,
  88% {
    opacity: .82;
  }

  to {
    offset-distance: 100%;
    opacity: 0;
  }
}
```

Aturan penting:

- Maksimal satu sampai tiga kapal terlihat dalam satu bab.
- Kapal berhenti jika izin belum aktif.
- Kapal menghilang ke kabut saat rute selesai.
- Jalur kompleks menggunakan SVG dan dikontrol dengan CSS.

### 8.5 Reveal arsip

```css
.chronicle-event {
  opacity: 0;
  filter: blur(5px);
  transform: translateY(18px);
  transition:
    opacity 700ms ease,
    filter 700ms ease,
    transform 700ms ease;
}

.chronicle-event[data-visible="true"] {
  opacity: 1;
  filter: blur(0);
  transform: translateY(0);
}
```

Fallback harus memastikan konten tetap terlihat apabila JavaScript gagal.

---

## 9. Struktur AstroJS

```text
src/
├── pages/
│   └── linimasa.astro
├── components/
│   └── chronicle/
│       ├── ChronicleHero.astro
│       ├── EraNavigation.astro
│       ├── MaritimeStage.astro
│       ├── TradeShip.astro
│       ├── PowerRipples.astro
│       ├── ChronicleEvent.astro
│       ├── SourceDrawer.astro
│       └── MethodologyNote.astro
├── data/
│   └── chronology.json
└── scripts/
    └── chronicle-controller.ts
```

### Prinsip implementasi

- Render konten utama sebagai HTML semantik.
- Gunakan CSS Grid, sticky positioning, dan SVG ringan.
- Gunakan satu controller kecil untuk status aktif, event visible, dan sinkronisasi peta.
- Jangan memasukkan ChartJS atau D3 apabila kebutuhan dapat dipenuhi CSS dan SVG.
- Jangan melakukan hydration pada keseluruhan halaman.
- Komponen interaktif harus mengikuti prinsip islands architecture.

---

## 10. Model Data

```json
{
  "id": "painan-treaty-1663",
  "year": 1663,
  "dateLabel": "1663",
  "era": "arus-berbalik",
  "title": "Traktat Painan",
  "type": ["diplomasi", "perjanjian"],
  "location": {
    "name": "Painan",
    "lat": -1.35,
    "lng": 100.58
  },
  "summary": "Peristiwa yang menandai perubahan hubungan kekuasaan di Pantai Barat Sumatra.",
  "confidence": "unverified",
  "source": {
    "title": "Judul sumber primer",
    "volume": "Volume",
    "page": "Halaman",
    "quotation": "Kutipan sumber asli"
  }
}
```

Data era, interpretasi, dan hubungan sebab-akibat tidak boleh dibuat hanya untuk kebutuhan visual. Setiap klaim harus dapat ditelusuri ke sumber atau ditandai sebagai interpretasi editorial.

---

## 11. Integrasi AstroJS, FastAPI, dan Flask

### AstroJS

- Merender halaman utama dan konten editorial.
- Menangani SEO, metadata, canonical URL, dan structured data.
- Menyediakan progressive enhancement.
- Mengontrol animasi antarmuka yang ringan.
- Menyediakan HTML awal tanpa menunggu API browser.

### FastAPI

- Endpoint peristiwa dan filter.
- GeoJSON pelabuhan dan rute.
- Pencarian tahun, lokasi, dan jenis event.
- Detail sumber dan provenance.
- Export CSV atau JSON.

```text
GET /api/chronicle/events?from=1600&to=1690
GET /api/chronicle/events/1663-painan-treaty
GET /api/chronicle/routes?era=aceh-hegemony
GET /api/chronicle/ports
GET /api/chronicle/sources/{source_id}
```

### Flask

Jika Flask dipertahankan sebagai aplikasi editorial/admin:

- kurasi event;
- pemeriksaan sumber;
- preview transkrip;
- pengelolaan status verifikasi;
- editorial notes;
- workflow publikasi.

Konten utama sebaiknya diperoleh Astro saat build atau server render. FastAPI dipakai untuk filter, pencarian, dan detail lanjutan agar render awal tidak bergantung pada request client-side.

---

## 12. Accessibility dan Performance

### 12.1 Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .trade-ship,
  .power-ripple,
  .tide-layer {
    animation: none !important;
  }
}
```

### 12.2 Persyaratan aksesibilitas

- Jangan mengunci scroll.
- Jangan menggunakan audio otomatis.
- Kapal, riak, dan pasang-surut dekoratif menggunakan `aria-hidden="true"`.
- Tahun dan event tetap tersedia sebagai HTML semantik.
- Setiap tombol mempunyai focus state yang jelas.
- Peta memiliki alternatif berupa daftar lokasi dan event.
- Seluruh event dapat dibaca tanpa JavaScript.
- Status tidak disampaikan hanya melalui warna.
- Kutipan asli dan terjemahan diberi label bahasa yang tepat.

### 12.3 Persyaratan performa

- Gunakan hanya satu `IntersectionObserver`.
- Hentikan animasi saat section berada di luar viewport.
- Gunakan SVG teroptimasi untuk rute dan ikon kapal.
- Hindari canvas berat kecuali performanya terbukti lebih baik melalui profiling.
- Gunakan image `srcset`, AVIF/WebP, dan ukuran eksplisit.
- Jangan menyembunyikan konten utama dengan `opacity: 0` tanpa fallback.
- Targetkan Total Blocking Time di bawah 200 ms pada pengujian mobile Lighthouse.

---

## 13. Urutan Pengerjaan

### Fase 1 — Fondasi informasi

1. Validasi kronologi dan sumber 1600–1690.
2. Tentukan event yang menjadi anchor dramaturgi.
3. Tetapkan status sumber dan provenance.
4. Susun model data JSON.
5. Pastikan event tanpa sumber tidak dijadikan blok era faktual.

### Fase 2 — Static prototype

1. Bangun `linimasa.astro` tanpa animasi.
2. Terapkan pembagian 20/48/32.
3. Buat navigasi era sticky.
4. Buat event kronik bertingkat.
5. Uji keterbacaan pada desktop 1366, 1440, dan 1920 px.

### Fase 3 — Maritime stage

1. Tambahkan peta SVG.
2. Hubungkan lokasi event ke peta.
3. Tambahkan riak kekuasaan.
4. Tambahkan jalur perdagangan.
5. Tambahkan maksimal tiga kapal kontekstual.

### Fase 4 — Motion dan sinkronisasi

1. Tambahkan reveal arsip.
2. Sinkronkan event aktif dengan navigasi era.
3. Sinkronkan event dengan peta dan kapal.
4. Bangun transisi khusus Traktat Painan 1663.
5. Implementasikan reduced-motion.

### Fase 5 — API dan editorial workflow

1. Hubungkan FastAPI untuk pencarian/filter/detail.
2. Hubungkan Flask untuk kurasi dan verifikasi.
3. Tambahkan source drawer.
4. Tambahkan export dataset.
5. Tambahkan audit log perubahan editorial apabila diperlukan.

### Fase 6 — Quality assurance

1. Audit keyboard navigation.
2. Audit screen reader.
3. Audit warna dan focus state.
4. Audit Lighthouse dan Web Vitals.
5. Uji tanpa JavaScript.
6. Uji koneksi lambat dan perangkat dengan CPU lemah.

---

## 14. Kriteria Keberhasilan

Desain dianggap berhasil apabila:

- Pengguna memahami dalam lima detik bahwa halaman membahas perubahan kekuasaan di Pantai Barat Sumatra.
- Pengguna dapat mengenali 1663 sebagai titik balik tanpa harus membaca seluruh halaman.
- Pengguna dapat membuka sumber primer dari setiap event.
- Peta, kapal, riak, dan pasang-surut memperkuat narasi, bukan mengalihkan perhatian.
- Seluruh konten tetap dapat dibaca tanpa animasi dan tanpa JavaScript.
- Identitas visual konsisten dengan Salido sebagai arsip sejarah editorial premium.
- Pengalaman tidak terasa seperti dashboard, scatter plot, atau hasil ekspor CSV.

---

## 15. Pernyataan Desain

> **Linimasa ini bukan daftar tahun. Linimasa ini adalah visualisasi bagaimana kekuasaan Aceh membentuk, mengendalikan, dan kemudian kehilangan dominasi atas jaringan Pantai Barat Sumatra. Pengguna tidak sedang menelusuri data; pengguna sedang mengikuti arus sejarah.**

Hasil akhir yang dituju adalah sebuah **kronik interaktif**: tenang, tajam, atmosferik, dapat dipertanggungjawabkan secara sumber, dan cukup ringan untuk memanfaatkan kekuatan AstroJS tanpa membebani pengalaman pengguna.
