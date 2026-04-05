# Jalur Perdagangan VOC — Sumatera Westkust

Atlas interaktif jalur perdagangan VOC di Sumatera Barat abad ke-18, terinspirasi dari [atlasofmutualheritage.nl](https://www.atlasofmutualheritage.nl/).

## 🚀 Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Web Server | Nginx (reverse proxy) |
| Frontend | Django 5 + Bootstrap 5 + Leaflet.js |
| Backend API | FastAPI + SQLAlchemy (async) |
| Database | PostgreSQL + PostGIS |
| Containerization | Docker Compose |

## 🗺️ Fitur

- Peta interaktif bergaya antik (CartoDB dark tiles)
- Ikon benteng kustom (SVG) di 4 lokasi historis VOC:
  - **Padang** — Fort de Goede Hoop
  - **Pulau Cingkuak** — Fort Indrapura
  - **Air Haji** — Pos perdagangan selatan
  - **Batavia** — Pusat VOC di Asia
- Klik benteng → side panel: info fort, statistik, daftar kapal & komoditi
- Filter perjalanan berdasarkan tahun dan produk
- Animasi polyline rute perdagangan antar pelabuhan

## 🏃 Cara Menjalankan

### Prasyarat
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) terinstall dan berjalan

### Jalankan Semua Services

```bash
git clone https://github.com/mhdikbal/westkust-routes.git
cd westkust-routes
git checkout sumatrawestkust

docker compose up --build
```

Buka browser: **http://localhost**

### API Documentation

FastAPI auto-docs tersedia di: **http://localhost/docs**

### Jalankan Unit Tests (tanpa Docker)

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

## 📁 Struktur Proyek

```
webjalur/
├── docker-compose.yml
├── nginx/
│   └── nginx.conf
├── backend/                 # FastAPI
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── seed_data.py
│   ├── routers/
│   │   ├── forts.py
│   │   └── voyages.py
│   └── tests/
│       ├── test_forts.py    # 6 unit tests
│       └── test_voyages.py  # 9 unit tests
├── frontend/                # Django
│   ├── config/
│   └── map_app/
│       └── templates/map_app/index.html
└── data/
    └── Data_Westkust_Map.json
```

## 📊 Data

Data berasal dari arsip VOC [Huygens Instituut](https://resources.huygens.knaw.nl/bgb/) — berisi ratusan catatan perjalanan kapal dari Sumatera Westkust ke Batavia (1700–1780), termasuk:
- Nama kapal & kapten
- Tahun pelayaran
- Komoditi dagang (emas, lada, kamfer, benzoin, dll.)
- Nilai total dalam Gulden Belanda

## 🧪 Unit Tests

```
tests/test_forts.py    → 6 tests (endpoints /api/forts/)
tests/test_voyages.py  → 9 tests (endpoints /api/voyages/)
Total: 15 tests — semua PASSED ✅
```

## 📜 Lisensi

Data: [Huygens Instituut KNAW](https://resources.huygens.knaw.nl/) | Atlas referensi: [Atlas of Mutual Heritage](https://www.atlasofmutualheritage.nl/)
