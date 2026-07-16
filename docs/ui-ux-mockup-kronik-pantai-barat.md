# UI/UX Design Specification
## Kronik Pantai Barat Sumatra 1600–1690

**Produk:** Aplikasi kronik sejarah interaktif Salido  
**Frontend:** AstroJS  
**Editorial/Admin:** Flask  
**Data/API:** FastAPI bila diperlukan  
**Target awal:** Desktop 1440 px  
**Arah visual:** Historical editorial, maritime, archival, cinematic  
**Konsep:** **Pusaran Kuasa, Arus yang Berbalik**

---

## 1. Tujuan Pengalaman

Aplikasi tidak boleh terasa seperti dashboard, daftar kartu, atau visualisasi CSV. Pengguna harus merasa sedang berlayar mengikuti perubahan kekuasaan, perdagangan, dan diplomasi di Pantai Barat Sumatra.

> **Pengguna tidak menggulir daftar tahun. Pengguna mengikuti arus sejarah.**

Gambar utama memperlihatkan peta pelayaran tua sebagai lapisan langit, lautan bergelombang sebagai foreground, beberapa kapal dagang VOC, garis pantai pegunungan, benteng pesisir, serta kompas. Semua elemen tersebut dipertahankan sebagai panggung naratif.

---

## 2. Struktur Pengalaman

Aplikasi memiliki tiga mode suasana:

1. **Hero sinematik**  
   Kapal, gelombang, benteng, peta, dan cahaya keemasan tampil penuh untuk membangun atmosfer.

2. **Kronik analitis-editorial**  
   Era, peta, jalur perdagangan, peristiwa, dan sumber primer tampil terstruktur.

3. **Klimaks Traktat Painan 1663**  
   Tampilan berubah menjadi lembar perjanjian dengan cap merah sebagai simbol perubahan tatanan.

---

## 3. Sketsa Mockup Hero Desktop

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ SALIDO       KRONIK   PETA   PERISTIWA   SUMBER   TENTANG          ID / EN  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   KRONIK PANTAI BARAT SUMATRA                                                │
│   1600—1690                                                                  │
│                                                                              │
│   Pusaran Kuasa,                                                             │
│   Arus yang Berbalik                                                        │
│                                                                              │
│   Sembilan dekade perubahan kekuasaan,                                       │
│   perdagangan, dan diplomasi di pesisir barat Sumatra.                       │
│                                                                              │
│   [ MULAI MENELUSURI ]     [ BUKA PETA ]                                     │
│                                                                              │
│             KAPAL BESAR       KAPAL TENGAH              BENTENG PESISIR      │
│                                                                              │
│                                                       01 / 06   GULIR ↓      │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Penempatan berdasarkan background

- Judul berada di kiri atas sampai tengah kiri.
- Kapal utama di kiri bawah tidak boleh tertutup blok teks.
- Kapal kedua menjadi pengarah pandangan menuju benteng.
- Benteng kanan tetap terlihat sebagai destination point.
- Laut dan gelombang di bawah tetap dominan.
- Peta pelayaran dan kompas di langit tetap terlihat sebagai lapisan sejarah.

---

## 4. Sketsa Mockup Kronik Desktop

```text
┌─────────────────┬───────────────────────────────────┬────────────────────────┐
│ NAVIGASI ERA    │ MARITIME STAGE                    │ PERISTIWA AKTIF        │
│                 │                                   │                        │
│ ○ 1600–1607     │               ACEH                │ 1663                   │
│ Laut sebelum    │                ◉ )))              │ TRAKTAT PAINAN         │
│ pusaran         │                 ╲                 │                        │
│                 │                  ╲ jalur kuasa    │ Diplomasi · Perjanjian │
│ ● 1607–1636     │     BARUS  ○      ╲               │                        │
│ Pusaran menguat │     TIKU   ○       ╲              │ 18 November 1663       │
│                 │     PADANG ○        ╲             │ Painan                 │
│ ○ 1636–1641     │     PAINAN ○  ← kapal VOC         │                        │
│ Pergantian      │                                   │ Ringkasan peristiwa    │
│                 │       riak · arus · pasang        │ dan konteks sejarah.   │
│ ○ 1641–1662     │                                   │                        │
│ Pasang surut    │ 1600 ─ 1632 ─ 1641 ─ 1663 ─ 1690 │ “Kutipan primer...”    │
│                 │                       ●           │                        │
│ ○ 1663          │                                   │ [BACA TRANSKRIP]       │
│ Arus berbalik   │                                   │ [LIHAT DI PETA]        │
└─────────────────┴───────────────────────────────────┴────────────────────────┘
```

### Proporsi

- Navigasi era: 18–20%.
- Maritime stage: 48–52%.
- Panel peristiwa: 28–32%.
- Lebar konten maksimum: 1440–1600 px.
- Panel sumber minimal 360 px pada layar 1366 px.

---

## 5. Header

### State hero

- Transparan.
- Tinggi 76 px.
- Logo dan menu menggunakan warna krem terang.
- Border bawah tipis dan transparan.
- Tidak menggunakan shadow.

### State setelah scroll

- Background gelap transparan.
- Tinggi mengecil menjadi 64 px.
- Backdrop blur sangat ringan.
- Menu aktif menggunakan garis emas tipis.
- Tidak menggunakan tombol kapsul ala aplikasi SaaS.

---

## 6. Hero Copy

```text
KRONIK PANTAI BARAT SUMATRA
1600—1690

Pusaran Kuasa,
Arus yang Berbalik

Sembilan dekade perubahan kekuasaan,
perdagangan, dan diplomasi di pesisir barat Sumatra.

[MULAI MENELUSURI]  [BUKA PETA]
```

### Tipografi

- Eyebrow: Space Grotesk, 12–13 px, uppercase, tracking 0.20em.
- Hero title: EB Garamond, 78–104 px.
- Tahun: EB Garamond, 30–38 px.
- Deskripsi: EB Garamond, 20–22 px.
- Tombol: Space Grotesk, 12–13 px, uppercase.

---

## 7. Treatment Background

```css
.hero {
  position: relative;
  min-height: 100svh;
  background:
    linear-gradient(
      90deg,
      rgba(10, 14, 14, 0.76) 0%,
      rgba(10, 14, 14, 0.38) 38%,
      rgba(10, 14, 14, 0.08) 64%,
      rgba(10, 14, 14, 0.20) 100%
    ),
    linear-gradient(
      180deg,
      rgba(10, 12, 12, 0.10) 0%,
      rgba(10, 12, 12, 0.05) 54%,
      rgba(10, 12, 12, 0.66) 100%
    ),
    url('/images/kronik-pantai-barat-1920.avif');

  background-size: cover;
  background-position: center center;
}
```

Overlay kiri melindungi keterbacaan judul tanpa menghilangkan kapal, peta, gelombang, dan benteng.

---

## 8. Navigasi Era

```text
1600–1607  Laut Sebelum Pusaran
1607–1636  Pusaran Menguat
1636–1641  Pusat Kehilangan Pemegangnya
1641–1662  Pasang Surut Kekuasaan
1663       Arus Berbalik
1663–1690  Lautan yang Berubah
```

- Sidebar sticky.
- Titik aktif berwarna emas.
- Garis vertikal terisi mengikuti progres.
- Deskripsi singkat hanya muncul pada era aktif.
- Era bukan kumpulan kartu.

---

## 9. Maritime Stage

Elemen utama:

- peta Sumatra sebagai underlay;
- riak dari pusat kekuasaan Aceh;
- garis orbit menuju pelabuhan;
- rute perdagangan Aceh;
- rute VOC;
- pelabuhan sebagai node;
- kapal yang bergerak sesuai event;
- pasang-surut transparan;
- label lokasi kontekstual.

### Bahasa warna

```text
Emas tua       = orbit kekuasaan Aceh
Tembaga merah  = jalur VOC
Biru tinta     = jalur maritim lokal
Putih gading   = pelabuhan netral
Titik redup    = lokasi belum aktif
```

Marker modern berbentuk pin tidak digunakan. Pelabuhan memakai lingkaran, cap kecil, atau simbol navigasi maritim.

---

## 10. Panel Peristiwa

```text
PERISTIWA AKTIF

1663
TRAKTAT PAINAN

Diplomasi · Perjanjian
18 November 1663
Painan, Pantai Barat Sumatra

Ringkasan perubahan hubungan kekuasaan,
perdagangan, dan persekutuan.

“Kutipan sumber primer...”

SUMBER PRIMER
Judul arsip · Volume · Halaman

[BACA TRANSKRIP]
[LIHAT DI PETA]
```

Panel menggunakan kertas tua yang halus. Benteng, kapal, cap merah, potret, dan peta dipakai secara kontekstual, bukan sekaligus pada semua event.

---

## 11. Klimaks Traktat Painan 1663

Ketika pengguna mencapai 1663:

1. Gerak gelombang melambat.
2. Kapal utama berhenti singkat.
3. Riak Aceh menurun.
4. Rute VOC menjadi lebih tegas.
5. Peta menjadi lebih terang.
6. Angka `1663` memenuhi bidang layar.
7. Panel lembar perjanjian terbuka.
8. Cap merah muncul di kanan bawah.

```text
1663
TRAKTAT PAINAN

Arus Tidak Lagi
Menuju Satu Pusat
```

Perubahan kekuasaan divisualisasikan sebagai arus yang berbalik, bukan ledakan atau peta pecah.

---

## 12. Motion System

Animasi harus terasa seperti:

- kabut laut tersibak;
- tinta meresap;
- arsip ditemukan;
- pasang-surut;
- arus berubah perlahan.

Hindari bounce, flip, spring, glow, dan zoom agresif.

### Reveal event

```css
.chronicle-entry {
  opacity: 0;
  filter: blur(5px);
  transform: translateY(20px);
  transition:
    opacity 700ms ease,
    filter 700ms ease,
    transform 700ms ease;
}

.chronicle-entry.is-visible {
  opacity: 1;
  filter: blur(0);
  transform: none;
}
```

### Aturan kapal

- Maksimal tiga kapal aktif.
- Durasi perjalanan 16–24 detik.
- Kapal bergerak hanya saat event perdagangan aktif.
- Animasi berhenti pada tab tidak aktif.
- Animasi mati saat `prefers-reduced-motion` aktif.

---

## 13. Komponen AstroJS

```text
src/
├── pages/
│   └── kronik.astro
├── components/
│   └── chronicle/
│       ├── ChronicleHero.astro
│       ├── EraSidebar.astro
│       ├── MaritimeStage.astro
│       ├── EventPanel.astro
│       ├── TimelineScrubber.astro
│       ├── SourceDrawer.astro
│       └── MethodologyPanel.astro
├── scripts/
│   └── chronicle-controller.ts
└── styles/
    └── chronicle.css
```

Astro merender konten faktual sebagai HTML. JavaScript hanya digunakan untuk status aktif, sinkronisasi peta, kapal, scrubber, source drawer, dan filter.

---

## 14. Peran Flask dan FastAPI

### Flask

```text
/admin/events
/admin/sources
/admin/routes
/admin/locations
/admin/publication
```

Digunakan untuk kurasi event, transkrip, status verifikasi, metadata sumber, dan workflow publikasi.

### FastAPI, bila dipakai

```text
GET /api/chronicle/events?from=1600&to=1690
GET /api/chronicle/events/{id}
GET /api/chronicle/routes?era=aceh-hegemony
GET /api/chronicle/ports
GET /api/chronicle/sources/{id}
```

Render awal tidak boleh menunggu API browser. Astro membaca data ketika build atau SSR.

---

## 15. Design Tokens

```css
:root {
  --paper: #f3ead9;
  --paper-deep: #dfcfb2;
  --ink: #18150f;
  --ink-soft: #5f584c;
  --sea: #14282a;
  --sea-deep: #081719;
  --aceh-gold: #a77a2e;
  --archive-gold: #c49a47;
  --voc-copper: #8b4030;
  --wax-red: #8f241c;
  --line: rgba(203, 167, 92, 0.35);
}
```

---

## 16. Asset Strategy

```text
kronik-pantai-barat-2560.avif
kronik-pantai-barat-1920.avif
kronik-pantai-barat-1440.webp
kronik-pantai-barat-mobile.avif
archive-paper.webp
voc-ship.svg
aceh-ripples.svg
painan-wax-seal.webp
```

Target ukuran:

- 2560 px: 500–700 KB.
- 1920 px: 350–500 KB.
- Mobile: 180–300 KB.
- Semua gambar memiliki ukuran eksplisit untuk mencegah layout shift.

---

## 17. Accessibility dan Performance

- Konten utama dapat dibaca tanpa JavaScript.
- Tidak ada scroll locking.
- Tidak ada audio otomatis.
- Kapal dan riak dekoratif menggunakan `aria-hidden="true"`.
- Timeline dapat dioperasikan dengan keyboard.
- Peta memiliki alternatif daftar lokasi.
- Status tidak bergantung hanya pada warna.
- Satu `IntersectionObserver` dipakai bersama.
- Animasi dihentikan saat keluar viewport.
- `prefers-reduced-motion` wajib didukung.
- Target Total Blocking Time di bawah 200 ms.

---

## 18. Urutan Implementasi

1. Validasi kronologi dan sumber.
2. Bangun hero statis.
3. Bangun layout 20/50/30.
4. Bangun navigasi era sticky.
5. Hubungkan event dan panel sumber.
6. Tambahkan peta SVG dan node pelabuhan.
7. Tambahkan riak dan rute.
8. Tambahkan kapal kontekstual.
9. Bangun adegan khusus 1663.
10. Hubungkan Flask/FastAPI.
11. Audit accessibility.
12. Audit Lighthouse dan Web Vitals.

---

## 19. Kriteria Keberhasilan

- Pengguna memahami tema aplikasi dalam lima detik.
- Kapal, benteng, peta, dan gelombang tetap terlihat pada hero.
- Tahun 1663 terbaca sebagai titik balik utama.
- Setiap event menampilkan sumber yang dapat ditelusuri.
- Motion memperkuat narasi dan tidak mengganggu pembacaan.
- Aplikasi tidak terasa seperti dashboard atau kumpulan kartu.
- Tampilan konsisten dengan identitas editorial Salido.

---

## 20. Pernyataan Desain

> **Kronik ini bukan daftar tahun. Kronik ini memperlihatkan bagaimana kekuasaan membentuk jalur perdagangan, menghubungkan pelabuhan, dan akhirnya mengubah arah arus sejarah Pantai Barat Sumatra.**
