# CLAUDE.md — Westkust Routes

Panduan kerja untuk Claude Code di repository ini.

---

## Testing & Quality Gate (WAJIB)

### TDD Workflow — Urutan Tidak Boleh Dibalik

1. **Tulis test dulu** (RED) — `backend/tests/test_<fitur>.py` atau `frontend/map_app/tests.py`
2. **Jalankan → harus FAIL** — pastikan test benar-benar menguji sesuatu
3. **Implement** minimal code sampai test pass (GREEN)
4. **Refactor** tanpa break test (IMPROVE)
5. **Verifikasi coverage** ≥ 80% untuk path kritis

### Run Tests

```bash
# FastAPI backend (dari dalam container)
docker compose exec backend pytest

# Atau langsung di host (butuh venv)
cd backend && python -m pytest tests/ -v --tb=short

# Django frontend
docker compose exec frontend python manage.py test map_app
```

### Aturan Testing Per Layer

**FastAPI Backend (pytest + httpx):**
- Setiap endpoint baru HARUS ada test di `backend/tests/`
- Gunakan `AsyncClient` dari `httpx` untuk endpoint test
- Mock koneksi DB jika test unit; gunakan DB nyata di integration test
- Minimal per endpoint: happy path + filter edge case + 404

**Django Frontend:**
- Template logic dan view functions: Django `TestCase`
- API call ke backend: mock dengan `unittest.mock.patch`
- Cek context variable yang dikirim ke template

---

## Arsitektur

```
Browser
  └── Nginx (:8084) — reverse proxy
        ├── /api/     → voc_backend:8000  (FastAPI + SQLAlchemy async)
        └── /         → voc_frontend:8001 (Django 5 + Leaflet.js)
                            Django fetch data dari backend via API_BASE_URL
```

**Service → Container mapping:**
| Service   | Container    | Port internal |
|-----------|--------------|---------------|
| backend   | voc_backend  | 8000          |
| frontend  | voc_frontend | 8001          |
| db        | voc_db       | 5432          |
| nginx     | voc_nginx    | 80 → 8084     |

---

## Commands Utama

```bash
# Start semua
docker compose up -d

# Rebuild setelah edit source
docker compose up -d --build backend    # atau frontend
docker compose up -d --build           # semua

# Logs
docker compose logs -f backend
docker compose logs -f frontend

# Masuk psql
docker compose exec db psql -U vocuser -d vocdb

# Seed ulang data
docker compose exec backend python seed_data.py

# Test
docker compose exec backend pytest -v
docker compose exec frontend python manage.py test map_app
```

---

## Struktur Direktori Kritis

```
backend/
  main.py           # FastAPI app, semua router include
  models.py         # SQLAlchemy models (Fort, Voyage)
  database.py       # AsyncSession + sync engine untuk seed
  routers/
    forts.py        # /forts endpoints
    voyages.py      # /voyages endpoints
  tests/            # pytest items

frontend/
  map_app/
    views.py        # Django views — fetch dari FastAPI
    templates/map_app/index.html  # Leaflet UI utama
  config/settings.py

scrawling/
  Data_BGS_Sumatra_Full.json  # 4.700+ records VOC (sumber tunggal)
```

---

## Pola Kode

### FastAPI — Tambah Endpoint Baru
1. Buat atau edit `backend/routers/<nama>.py` dengan `router = APIRouter()`
2. Include di `backend/main.py` dengan prefix `/api/<nama>`
3. Gunakan `AsyncSession` dari `database.py`
4. Tambah test di `backend/tests/test_<nama>.py`

### Django — Tambah View / Template Baru
1. Tambah view di `map_app/views.py` — fetch dari `API_BASE_URL` via `httpx`
2. Tambah URL di `map_app/urls.py`
3. Buat template di `map_app/templates/map_app/<nama>.html`
4. Perhatikan: Django fetch backend via `API_BASE_URL` env var (internal Docker network)

### PostGIS — Query Spasial
- Gunakan `ST_AsGeoJSON`, `ST_Distance`, `ST_Within` untuk query spasial
- Jangan return raw geometry — selalu serialize ke GeoJSON di layer FastAPI
- Index spasial wajib ada untuk kolom geometry yang di-query sering

### Data Historis (4.700+ Voyages)
- Sumber tunggal: `scrawling/Data_BGS_Sumatra_Full.json`
- Jangan edit file ini langsung — seed ulang via `seed_data.py` jika ada perubahan schema
- `direction` field: `"Outbound"` (dari Sumbar) vs `"Inbound"` (kembali ke Sumbar)

---

## Security Checklist Sebelum Commit

```
[ ] Tidak ada hardcoded credential/secret di kode
[ ] DJANGO_SECRET_KEY tidak di-commit (gunakan env var)
[ ] DEBUG=False di production
[ ] Tidak ada raw SQL tanpa parameterized query
[ ] Input dari URL parameter di-validate di FastAPI (Pydantic)
[ ] Error response tidak expose stack trace ke client
```

---

## Deploy Checklist

```
[ ] docker compose exec backend pytest → semua pass
[ ] docker compose exec frontend python manage.py test → semua pass
[ ] docker compose up -d --build → 0 error
[ ] curl http://localhost:8084/ → HTTP 200
[ ] curl http://localhost:8084/api/voyages → JSON valid
[ ] docker compose logs backend --tail 20 → tidak ada error
```

---

## Workflow Mandatori

- **Plan mode** untuk setiap task non-trivial (3+ langkah atau keputusan arsitektur)
- **Verifikasi sebelum selesai** — jangan tandai task selesai tanpa curl atau browser check
- **Setelah rebuild container** — selalu cek `docker compose logs <service>` dan test endpoint
- **Data historis adalah sumber kebenaran** — jika ada inkonsistensi, cek `Data_BGS_Sumatra_Full.json` dulu sebelum debug kode

---

## Konteks Riset

Project ini terhubung dengan kerangka riset IETPD × Ekonomi Sumbar.
Lihat: `docs/thesis-ietpd-hefrizal-kerangka.md`

Jalur perdagangan VOC abad ke-18 memberikan konteks historis mengapa geografi ekonomi Sumbar terbentuk seperti sekarang — pos-pos dagang (Barus, Air Bangis, Padang, Pulau Cingkuak) adalah cikal bakal pusat ekonomi kabupaten yang kini masuk dalam panel riset d'Besto.
