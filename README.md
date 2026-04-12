# Jalur Perdagangan VOC — Sumatera Westkust

Atlas interaktif jalur perdagangan VOC di Sumatera Barat abad ke-18, terinspirasi dari [atlasofmutualheritage.nl](https://www.atlasofmutualheritage.nl/). Proyek ini memvisualisasikan data pelayaran historis dengan estetika museum archival yang premium.

## 🚀 Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Web Server | Nginx (reverse proxy) |
| Frontend | Django 5 + Bootstrap 5 + Leaflet.js (AntPath + Bezier) |
| Backend API | FastAPI + SQLAlchemy (async) |
| Database | PostgreSQL + PostGIS |
| Containerization | Docker Compose |

## 🗺️ Fitur Utama

- **Premium Museum Archival UI**: Tema warna perkamen (*parchment*), tinta (*ink*), dan emas (*gold*) untuk kesan historis yang mendalam.
- **Dynamic Sea Routes**: Visualisasi jalur pelayaran menggunakan animasi `AntPath` dengan kurva Bezier yang halus.
- **Inbound/Outbound Logic**: Pembedaan otomatis antara kapal yang berangkat dari Sumatera Westkust (Outbound) dan yang kembali (Inbound) dengan pewarnaan yang kontras.
- **Interactive Forts**: Ikon kustom SVG untuk pos-pos perdagangan utama:
  - **Barus**, **Air Bangis**, **Padang**, **Pulau Cingkuak**, **Air Haji**.
  - **Batavia**, **Jambi**, **Palembang**, **Lampung** (Arrival points).
- **Comprehensive Data**: Detail kargo, komoditi utama, dan nilai gulden untuk setiap pelayaran.
- **Interactive Modal**: Tampilan detail kapal yang modern dengan daftar kargo lengkap.

## 🏃 Cara Menjalankan (Docker)

### Prasyarat
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (dengan fitur WSL 2 backend aktif jika di Windows)

### Jalankan Semua Services

```bash
git clone https://github.com/mhdikbal/westkust-routes.git
cd westkust-routes

# Jalankan orkestrasi
docker compose up --build -d
```

Buka browser: **http://localhost:8084** (Nginx Proxy)

### API Documentation
FastAPI Swagger docs tersedia di: **http://localhost:8000/docs**

---

## 🧪 Unit & Functional Tests

Pengujian otomatis mencakup validasi endpoint API, logika filter tahun, dan klasifikasi arah pelayaran (*direction logic*).

```bash
# Jalankan test di dalam container
docker compose exec backend pytest
```

**Hasil Terakhir:** `19 tests PASSED` ✅

## 📊 Sumber Data

Data dikumpulkan dari arsip VOC [Huygens Instituut](https://resources.huygens.knaw.nl/bgb/) — mencakup lebih dari 4.700 catatan perjalanan kapal di wilayah Sumatera Westkust (1700–1789).

## 📁 Struktur Proyek Utama

```
webjalur/
├── docker-compose.yml
├── backend/                 # FastAPI + SQLAlchemy
│   ├── models.py            # Data Architecture (2-way relationships)
│   ├── seed_data.py         # Advanced directionality-aware seeding
│   ├── routers/             # Fort & Voyage endpoints
│   └── tests/               # 19 Pytest items
├── frontend/                # Django
│   └── map_app/
│       └── templates/map_app/index.html  # Premium UI Logic
└── scrawling/
    └── Data_BGS_Sumatra_Full.json        # 4,700+ Records
```

## 📜 Lisensi & Attribution

Data: [Huygens Instituut KNAW](https://resources.huygens.knaw.nl/)  
Referensi Visual: [Atlas of Mutual Heritage](https://www.atlasofmutualheritage.nl/)
