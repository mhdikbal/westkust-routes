# ATM Analysis — Atlas of Mutual Heritage
**Amati → Tiru → Modifikasi untuk Westkust Routes**

Tanggal riset: 2026-06-24  
Sumber: https://www.atlasofmutualheritage.nl

---

## A — AMATI (Apa yang mereka punya)

### Stack & Infrastruktur (inferensi dari observasi)

| Komponen | Yang Teridentifikasi |
|---|---|
| Map library | Leaflet.js atau OpenLayers (standar heritage Belanda) |
| Tile basemap | OpenStreetMap atau PDOK BRT Achtergrondkaart (tile nasional Belanda) |
| Image viewer | IIIF Viewer (zoom pada peta arsip berukuran 99×80cm) |
| CMS | Custom atau Drupal (struktur URL `/page/<id>/<slug>`) |
| API | OpenSearch XML — `http://www.gahetna.nl/beeldbank-api/opensearch` |
| Lisensi data | CC-0 (seluruh metadata dan sebagian besar gambar) |
| Bahasa | NL + EN (bilingual toggle) |

### Fitur Peta

- Peta interaktif dunia — semua lokasi VOC/WIC diplot sebagai titik
- Kontrol: zoom in/out, home (reset view), fullscreen toggle
- Klik titik → buka halaman detail lokasi
- Historical map viewer per objek: zoom tinggi pada scan peta arsip

### Struktur Konten per Halaman Lokasi

**Contoh: Padang** (`/page/5751/padang`)

```
Nama lokasi      : Padang / Padangh (nama historis)
Negara           : Indonesia
Wilayah          : Sumatra
Designasi VOC    : Sumatras Westcust (VOC-gebied)
Fungsi historis  : Markas komandan perdagangan Pantai Barat Sumatra
Komoditi utama   : pepper, salt, camphor, benzoic resin
Galeri gambar    : 13 peta historis (karya Johannes van Keulen II, Isaac de Graaff)
Institusi terkait: Nationaal Archief, Rijksmuseum, UB Leiden
```

### Metadata per Rekaman Peta/Gambar

```
Creator    : nama surveyor/kartografer
Period     : tahun (contoh: 1733)
Material   : perkamen, kertas, dll.
Technique  : pen and brush, print, dll.
Dimensions : ukuran fisik (99 × 80 cm)
Catalog #  : nomor arsip (COLLBN 054-06-001)
Owner      : institusi penyimpan
Tags       : Map/Chart/Plan, estate/plantation, compass/dial
```

### Taksonomi Konten

- **By place**: Padang, Pariaman, Barus, Air Bangis — semua ada halamannya
- **By content type**: Map/Chart/Plan, Drawing, Photograph
- **By region**: Indonesia → Sumatra → Sumatras Westcust
- **By institution**: Nationaal Archief, Rijksmuseum, UB Leiden, dll.
- **By expedition**: Perjalanan + misi VOC (fitur baru 2022)

### Data Sumatra yang Ada di AMH (Relevan untuk Kita)

| URL AMH | Konten |
|---|---|
| `/page/5751/padang` | Padang — 13 peta historis, deskripsi VOC |
| `/page/5756/pariaman` | Pariaman |
| `/page/2518/map-of-sumatra-and-the-malacca-strait` | Peta Sumatra+Selat Malaka 1733 — CC-0 |
| `/page/4010/map-of-sumatra` | Peta Sumatra keseluruhan |
| `/page/3913/map-of-the-island-of-sumatra` | Peta pulau Sumatra |
| `/page/3909/map-of-malacca-and-sumatra` | Peta Malaka+Sumatra |
| `/page/2503/map-of-java-sumatra-borneo-and-malaysia` | Peta regional |

**Semua gambar/peta di atas CC-0 — legal untuk digunakan langsung.**

---

## T — TIRU (Apa yang bisa langsung kita adopsi)

### T1. Overlay Peta Historis AMH ke Leaflet

AMH memiliki scan peta tahun 1733 karya Isaac de Graaff (Sumatra + Selat Malaka, CC-0).
Kita bisa load gambar ini sebagai `L.imageOverlay()` di Leaflet dengan koordinat yang di-georeference.

**Cara implementasi:**
```javascript
// Georeference bounding box peta 1733 (perlu dikalibrasi)
const historicalBounds = [[-6, 95], [6, 110]]; // approx Sumatra
const historicalMap = L.imageOverlay(
  'https://www.atlasofmutualheritage.nl/image/AMH_SUMATRA_1733.jpg',
  historicalBounds,
  { opacity: 0.6 }
).addTo(map);
```

Atau lebih baik: download gambar CC-0, host lokal, georeference pakai QGIS → export sebagai tile WMS/WMTS → serve via tile server.

### T2. Halaman Detail Per Pelabuhan

AMH punya halaman kaya per lokasi. Kita tiru pola ini untuk setiap pelabuhan Westkust.

**Yang perlu ditambah di `/api/forts` dan Django view:**
```
nama_historis     : "Padangh", "Air Bangis", "Baros"
designasi_voc     : "Sumatras Westcust (VOC-gebied)"
komoditi_utama    : pepper, camphor, dll (sudah ada di voyage data)
fungsi_historis   : deskripsi paragraf (perlu content baru)
periode_aktif     : 1726–1794 (dari range data BGB)
galeri_referensi  : link ke AMH pages terkait (CC-0)
```

### T3. Taksonomi Tag per Voyage

AMH tag kontennya (Map/Chart/Plan, estate/plantation, dll.). Kita tiru untuk voyage:
```
direction    : Outbound / Inbound
era          : 1726–1750 / 1751–1775 / 1776–1800
komoditi     : pepper / camphor / salt / cloth / spices
nilai_kargo  : rendah (<500 gulden) / sedang / tinggi (>5000 gulden)
```

### T4. Atribusi Sumber (BGB Huygens Link-through)

AMH setiap item diklik → link ke institusi asli. Kita harus tiru ini:
- Per voyage: link ke URL BGB originalnya (`resources.huygens.knaw.nl/bgb/...`)
- Per fort/lokasi: link ke halaman AMH terkait (`atlasofmutualheritage.nl/page/5751/padang`)

Ini penting untuk kredibilitas riset (thesis connection).

### T5. Fullscreen Map Toggle

AMH sudah implement ini. Kita sudah punya di Layout B. Pastikan tetap ada.

---

## M — MODIFIKASI (Apa yang kita adaptasi / tambahkan yang AMH tidak punya)

### M1. Animated Route Lines (AMH tidak punya ini)

AMH hanya titik statis di peta. Westkust Routes punya data PERGERAKAN kapal:
- Asal → Tujuan per voyage
- Kapan berangkat, kapan tiba, durasi
- Muatan dan nilai kargo

**Implementasi**: polyline animasi per voyage, atau heatmap route density.
AMH tidak bisa ini karena mereka database gambar, bukan database rute.

### M2. Time-Slider (1726–1800)

AMH tidak ada filter waktu. Kita bisa tambahkan:
```javascript
// Slider tahun → filter voyages yang ditampilkan di peta
<input type="range" min="1726" max="1800" id="year-slider">
```

Ini memungkinkan visualisasi "aktivitas perdagangan per dekade" — sangat relevan untuk riset IETPD.

### M3. Dual-Direction Toggle

AMH tidak bedakan arah. Kita punya:
- **Outbound** (Sumatera→Batavia): 4,738 voyage, komoditi keluar
- **Inbound** (Batavia→Sumatera): 375 voyage, komoditi masuk

Toggle ini memberi insight unik: apa yang VOC kirim masuk vs. apa yang mereka ekstrak keluar.

### M4. Economic Value Heatmap

AMH: informasi komoditi per lokasi, statis.
Kita bisa: **heatmap nilai gulden total per pelabuhan** — visualisasi eksploitasi ekonomi.

```
Padang:         ƒ X,XXX,XXX
Pulau Cingkuak: ƒ X,XXX,XXX
Air Bangis:     ƒ X,XXX,XXX
```

Ini adalah kontribusi penelitian original yang AMH tidak punya.

### M5. Koneksi Masa Kini (AMH murni historis)

AMH berhenti di sejarah kolonial. Westkust Routes bisa bridging:
- Port historis → Kabupaten sekarang (Padang = Kota Padang)
- Komoditi VOC → PAD sekarang (lada dulu → apa sekarang?)
- Volume ekspor abad 18 vs. PDRB kabupaten sekarang

Ini adalah angle riset IETPD × Ekonomi Sumbar yang membuat project ini unik.

### M6. Gunakan Data CC-0 AMH sebagai Layer Kontekstual

**Yang bisa langsung dipakai dari AMH (CC-0):**
1. Gambar peta historis Sumatra 1733 → image overlay di Leaflet
2. Teks deskripsi per pelabuhan → enrichment konten port pages kita
3. Nama-nama historis → `nama_historis` field di database

**Cara akses programmatic:**
```python
# Nationaal Archief OpenSearch API (XML)
import requests
from xml.etree import ElementTree

BASE = "http://www.gahetna.nl/beeldbank-api/opensearch"
r = requests.get(BASE, params={
    "q": "Sumatra Westkust padang",
    "count": 100,
    "startIndex": 0
})
# Returns XML with image metadata, archival numbers, dates
```

---

## Ringkasan Prioritas Implementasi

| Prioritas | Fitur | Effort | Impact |
|---|---|---|---|
| P0 | T4: Atribusi sumber (BGB link-through) | Rendah | Tinggi (kredibilitas riset) |
| P0 | T2: Port detail pages (/ports/padang) | Sedang | Tinggi |
| P1 | M1: Animated route lines | Sedang | Tinggi |
| P1 | M3: Direction toggle Outbound/Inbound | Rendah | Tinggi |
| P1 | M2: Time-slider 1726–1800 | Sedang | Sedang |
| P2 | T1: Historical map overlay (image dari AMH) | Tinggi | Tinggi (visual impact) |
| P2 | M4: Economic value heatmap | Sedang | Sedang |
| P3 | M5: Koneksi masa kini (PAD, PDRB) | Tinggi | Tinggi (riset) |
| P3 | M6: AMH OpenSearch API integration | Sedang | Sedang |

---

## Referensi & Link

- AMH Padang: https://www.atlasofmutualheritage.nl/page/5751/padang
- AMH Sumatra 1733: https://www.atlasofmutualheritage.nl/page/2518/map-of-sumatra-and-the-malacca-strait
- Nationaal Archief OpenSearch API: http://www.gahetna.nl/beeldbank-api/opensearch
- AMH tentang proyek: https://www.atlasofmutualheritage.nl/over
- Peluncuran versi baru 2022: https://english.cultureelerfgoed.nl/latest/news/2022/10/28/new-version-atlas-of-mutual-heritage-launched
