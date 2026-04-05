# 🕷️ Scraping Pipeline — BGB Sumatra

Folder ini berisi skrip scraping data voyage VOC dari sumber arsip Belanda:
**[Boekhouding Generale Batavia (BGB) — Huygens KNAW](https://resources.huygens.knaw.nl/bgb/search)**

---

## 📂 File

| File | Deskripsi |
|------|-----------|
| `bgb_sumatra_scraper.py` | **Scraper utama** — scrape semua voyage dari pos Sumatera |
| `bgb_colab_pipeline.py`  | **Template Colab** — pipeline lengkap dengan statistik |
| `bgb_goud_final.py`      | *(Legacy)* Scraper lama khusus emas dari Padang |

---

## 🗺️ Pos Keberangkatan yang Di-scrape

| ID BGB | Nama | Wilayah | Keterangan |
|--------|------|---------|------------|
| `926`  | **Padang** | Sumatera Barat | Fort de Goede Hoop — pos VOC utama |
| `858`  | **Pulau Cingkuak** | Sumatera Barat | Fort Indrapura (Pulau Tjinkuk) |
| `854`  | **Air Haji** | Sumatera Barat | Airhadji — pos selatan |
| `850`  | **Jambi** | Sumatera Tengah | Lada & benzoin |
| `851`  | **Palembang** | Sumatera Selatan | Lada, timah, benzoin |

> **Catatan:** Aceh, Barus, Tiku, Pasaman **tidak terdaftar** sebagai *departure place* di BGB. Data dari wilayah tersebut kemungkinan tercatat di bawah "Padang" atau tidak terekam dalam arsip BGB. Untuk data yang lebih luas, perlu penelusuran manual di [bgb/search](https://resources.huygens.knaw.nl/bgb/search).

---

## 📊 Data yang Dikumpulkan (vs versi lama)

| Field | Scraper Lama | Scraper Baru |
|-------|:---:|:---:|
| Nama kapal | ✅ | ✅ |
| Kapten | — | ✅ |
| Tonaj kapal | — | ✅ |
| **Hari keberangkatan** | ❌ | ✅ |
| **Bulan keberangkatan** | ❌ | ✅ |
| **Tahun keberangkatan** | ✅ (partial) | ✅ |
| **Tanggal kedatangan** | ❌ | ✅ |
| **Durasi pelayaran (hari)** | ❌ | ✅ |
| Tujuan | ✅ | ✅ |
| Produk utama | ✅ | ✅ |
| Semua produk | ✅ | ✅ |
| **Detail kargo per item** | ❌ | ✅ |
| Nilai gulden | ✅ | ✅ |
| **Nilai gulden per item** | ❌ | ✅ |
| Pos selain Padang | ❌ | ✅ |
| **Checkpoint (resume)** | ❌ | ✅ |

---

## 🚀 Cara Pakai di Google Colab

### Metode 1: Upload file manual

```python
# Di Colab, upload bgb_sumatra_scraper.py
from google.colab import files
uploaded = files.upload()  # pilih bgb_sumatra_scraper.py

# Install dependencies
!pip install requests beautifulsoup4 pandas lxml -q

# Jalankan
!python bgb_sumatra_scraper.py
```

### Metode 2: Clone dari GitHub

```python
!git clone --branch scrawlingdata --depth 1 \
    https://github.com/mhdikbal/westkust-routes.git

%cd westkust-routes/scrawling
!pip install requests beautifulsoup4 pandas lxml -q
!python bgb_sumatra_scraper.py
```

### Metode 3: Pipeline lengkap dengan statistik

Buka `bgb_colab_pipeline.py` dan jalankan sel per sel di Colab.

---

## ⚙️ Konfigurasi

Edit bagian atas `bgb_sumatra_scraper.py`:

```python
# Tambah/kurangi tempat berangkat
DEPARTURE_PLACES = {
    "926": ("Padang", ...),
    "858": ("Pulau Cingkuak", ...),
    # dst.
}

# Filter produk: None = semua, atau "goud", "peper", "kamfer"
PRODUCT_FILTER: Optional[str] = None

# Batas halaman per tempat (1 hal = ~10 voyage)
MAX_PAGES_PER_PLACE = 200

# Jeda antar request — jangan terlalu cepat!
DELAY_DETIK = 1.5
```

---

## 📋 Format Output JSON (`Data_BGS_Sumatra_Full.json`)

```json
[
  {
    "ID": 13447,
    "URL": "https://resources.huygens.knaw.nl/bgb/voyage/13447",
    "Nama_Kapal": "Theeboom",
    "Kapten": "Jan de Vries",
    "Tonaj": "200 last",
    "Asal": "Padang",
    "Asal_ID": "926",
    "Asal_Lat": -0.9655545,
    "Asal_Lon": 100.353889,
    "Wilayah": "Sumatera Barat",
    "Tujuan": "Batavia",
    "Tahun_Buku": 1700,
    "Tahun": 1700,
    "Tgl_Berangkat": {
      "hari": 15,
      "bulan": 3,
      "tahun": 1700,
      "iso": "1700-03-15"
    },
    "Tgl_Tiba": {
      "hari": 28,
      "bulan": 4,
      "tahun": 1700,
      "iso": "1700-04-28"
    },
    "Durasi_Hari": 44,
    "Produk_Utama": "goud",
    "Semua_Produk": "goud | kamfer | peper",
    "Total_Gulden_NL": 98358.05,
    "Jumlah_Item_Kargo": 3,
    "Kargo": [
      {
        "produk": "goud",
        "spesifikasi": "bij gewicht",
        "qty_asli": "29,17,1",
        "unit": "mark fijns",
        "nilai_numerik": 29.0,
        "gram": 0.0,
        "gulden_nl": 85000.0,
        "gulden_india": 0.0,
        "catatan": ""
      }
    ],
    "Scraped_At": "2026-04-05T12:00:00Z"
  }
]
```

---

## 🔄 Pipeline ke Aplikasi Peta

```
Google Colab                   GitHub (branch: scrawlingdata)
  ↓ scraping BGB                  ↓ commit hasil JSON
Data_BGS_Sumatra_Full.json  →  data/Data_Westkust_Map.json
  ↓                               ↓
  └──────────────────────────→ backend/seed_data.py → PostgreSQL → Peta
```

---

## 📌 Catatan Wilayah yang Belum Terdaftar di BGB

Wilayah berikut **tidak ditemukan** sebagai *departure place* di dropdown BGB:
- **Aceh** (Banda Aceh) — data perdagangan Aceh berbeda, mungkin di database lain
- **Barus** (Fansur) — kota lada & kamfer kuno, sebelum era BGB
- **Tiku** — komoditi dari sini mungkin tercatat sebagai "Padang" di BGB
- **Pasaman** — wilayah pedalaman, tidak punya pos pantai langsung

Untuk data wilayah tersebut, sumber alternatif:
- [TANAP Database](http://www.tanap.net/)
- [VOC-kenniscentrum](https://www.vockennis.nl/)
- [Nationaal Archief Den Haag](https://www.nationaalarchief.nl/)
