# Sprint Plan: ATM Westkust Routes

## Sprint Goal

Peneliti dan pengunjung dapat menelusuri setiap voyage langsung ke sumber BGB/AMH, melihat detail historis pelabuhan, dan mengamati pola rute Outbound/Inbound secara visual di peta — menjadikan Westkust Routes sebagai alat riset yang dapat dikutip.

---

## Sprint Duration & Velocity

**Durasi:** 2 minggu (14 hari)

**Total Story Points:** 23 SP

| Minggu | Fokus | Item |
|--------|-------|------|
| Minggu 1 (Hari 1-7) | Schema migration + P0 backend | US-06, US-01, US-02, US-03 |
| Minggu 2 (Hari 8-14) | P1 frontend + animasi + QA gate | US-04, US-05, integrasi, regression suite |

**Kapasitas tim:** 4 orang x 5 hari efektif = 20 hari-orang. Buffer 10% untuk bug fix dan review.

---

## Team Assignments

| Role | Tanggung Jawab Sprint Ini |
|------|--------------------------|
| **PM** | Prioritas backlog, acceptance criteria sign-off, audit coverage `source_url` di hari 1, eskalasi jika data AMH belum tersedia |
| **DBA** | Alembic migration (US-06), seed helper query `periode_aktif`, index baru, review N+1 fix di `list_forts()` |
| **DevSecOps** | Update `nginx.conf` (CSP + security headers + rate limiting), verifikasi `.env` checklist, SSRF allowlist, review `rel="noopener noreferrer"` di semua template |
| **QA** | Tulis semua test file sebelum implementasi (TDD RED), jalankan regression suite di setiap merge, coverage gate `--cov-fail-under=80` |

---

## Backlog Items

### P0 — Sprint Ini (Minggu 1)

| ID | Story | Owner | SP | Status | Acceptance Criteria Singkat |
|----|-------|-------|----|--------|------------------------------|
| US-06 | Developer: Port Schema Migration Aman | DBA | 3 | TODO | Alembic migration idempoten; `upgrade()` + `downgrade()` tanpa error; semua existing tests tetap pass |
| US-01 | BGB Link-Through per Voyage | QA + Dev | 2 | TODO | Popup voyage tampilkan link BGB jika `source_url` tidak null; `target="_blank" rel="noopener noreferrer"`; null = tidak tampil |
| US-02 | Port Detail Page: Nama Historis & Komoditi | Dev | 5 | TODO | Halaman `/ports/<slug>` render 5 field baru; minimal 4 pelabuhan utama ada data seed; endpoint `/api/forts/{id}` backward-compatible |
| US-03 | AMH Link-Through dari Port Detail Page | Dev | 2 | TODO | Tombol "Lihat di AMH" jika `amh_url` tidak null; validasi URL Pydantic (422 jika invalid); null = teks "Data AMH belum tersedia" |

**Total P0: 12 SP**

### P1 — Sprint Ini (Minggu 2)

| ID | Story | Owner | SP | Status | Acceptance Criteria Singkat |
|----|-------|-------|----|--------|------------------------------|
| US-04 | Animated Route Lines per Voyage | Dev | 8 | TODO | `/api/voyages/routes` return GeoJSON LineString; Leaflet polyline dengan animasi; tooltip hover; render 50 rute < 2 detik |
| US-05 | Direction Toggle Outbound/Inbound | Dev | 3 | TODO | Toggle 3 tombol Bootstrap; `?direction=` filter real-time; warna biru/oranye; state dipertahankan saat zoom/pan |

**Total P1: 11 SP**

---

## Database Migration

### DDL Siap Pakai

```sql
-- ============================================================
-- Migration: Add AMH enrichment columns to forts table
-- Sprint P0 — US-02 Port Detail Pages + US-03 AMH Link-Through
-- Jalankan via Alembic (JANGAN langsung psql di production):
--   docker compose exec backend alembic upgrade head
-- ============================================================

BEGIN;

-- Aktifkan btree_gist untuk index INT4RANGE
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE forts
    ADD COLUMN IF NOT EXISTS nama_historis   VARCHAR(255),
    ADD COLUMN IF NOT EXISTS designasi_voc   VARCHAR(100),
    ADD COLUMN IF NOT EXISTS fungsi_historis TEXT,
    ADD COLUMN IF NOT EXISTS periode_aktif   INT4RANGE,
    ADD COLUMN IF NOT EXISTS amh_url         VARCHAR(500);

-- Constraint: amh_url harus URL AMH valid jika diisi
ALTER TABLE forts
    ADD CONSTRAINT chk_forts_amh_url_format
    CHECK (
        amh_url IS NULL
        OR amh_url LIKE 'https://hdl.handle.net/%'
        OR amh_url LIKE 'https://www.atlasofmutualheritage.nl/%'
    );

-- Index GiST untuk time-slider (P1 M2)
CREATE INDEX IF NOT EXISTS idx_forts_periode_aktif
    ON forts USING GIST (periode_aktif);

-- Index untuk filter by designasi_voc
CREATE INDEX IF NOT EXISTS idx_forts_designasi_voc
    ON forts (designasi_voc)
    WHERE designasi_voc IS NOT NULL;

-- Index untuk time-slider voyages
CREATE INDEX IF NOT EXISTS idx_voyages_year
    ON voyages (year);

-- Composite index direction + year untuk filter kombinasi
CREATE INDEX IF NOT EXISTS idx_voyages_direction_year
    ON voyages (direction, year);

-- Spatial index forts (pastikan ada)
CREATE INDEX IF NOT EXISTS idx_forts_location
    ON forts USING GIST (location);

COMMIT;
```

### SQLAlchemy Model Update (`backend/models.py`)

```python
from sqlalchemy.dialects.postgresql import INT4RANGE

class Fort(Base):
    # ... kolom existing tidak diubah ...

    nama_historis   = Column(String(255), nullable=True)
    designasi_voc   = Column(String(100), nullable=True)
    fungsi_historis = Column(Text,        nullable=True)
    periode_aktif   = Column(INT4RANGE,   nullable=True)
    amh_url         = Column(String(500), nullable=True)
```

### Alembic Migration Template (`backend/alembic/versions/`)

```python
# alembic revision --autogenerate -m "add_fort_historis_amh_fields"

def upgrade():
    op.add_column('forts', sa.Column('nama_historis',   sa.String(255), nullable=True))
    op.add_column('forts', sa.Column('designasi_voc',   sa.String(100), nullable=True))
    op.add_column('forts', sa.Column('fungsi_historis', sa.Text(),      nullable=True))
    op.add_column('forts', sa.Column('periode_aktif',   postgresql.INT4RANGE(), nullable=True))
    op.add_column('forts', sa.Column('amh_url',         sa.String(500), nullable=True))
    op.create_check_constraint(
        'chk_forts_amh_url_format', 'forts',
        "amh_url IS NULL "
        "OR amh_url LIKE 'https://hdl.handle.net/%' "
        "OR amh_url LIKE 'https://www.atlasofmutualheritage.nl/%'"
    )

def downgrade():
    op.drop_constraint('chk_forts_amh_url_format', 'forts')
    op.drop_column('forts', 'amh_url')
    op.drop_column('forts', 'periode_aktif')
    op.drop_column('forts', 'fungsi_historis')
    op.drop_column('forts', 'designasi_voc')
    op.drop_column('forts', 'nama_historis')
```

### Seed Helper — `periode_aktif` dari Data Voyage

```sql
-- Generate periode_aktif proxy dari voyages — review manual sebelum UPDATE
SELECT
    f.id,
    f.name,
    MIN(v.year)                              AS tahun_awal,
    MAX(v.year)                              AS tahun_akhir,
    int4range(MIN(v.year), MAX(v.year) + 1) AS periode_proxy
FROM forts f
LEFT JOIN voyages v
    ON f.id = v.origin_id OR f.id = v.destination_id
GROUP BY f.id, f.name
ORDER BY f.name;
```

---

## TDD Sequence

Urutan ini wajib diikuti. Jangan mulai implementasi sebelum test file ada dan observed FAIL.

```
STEP 1 — RED: P0-T4 source_url contract
  File:    backend/tests/test_atm_p0_t4.py
  Run:     docker compose exec backend pytest tests/test_atm_p0_t4.py -v
  Ekspek:  PASS langsung (field sudah ada) — jika ada FAIL, itu regresi nyata, fix dulu
  Isi:     test_voyage_list_exposes_source_url
           test_voyage_list_source_url_null_when_absent
           test_fort_detail_voyage_brief_exposes_source_url

STEP 2 — RED: P0-T2 enrichment endpoint (endpoint BELUM ada)
  File:    backend/tests/test_atm_p0_t2.py
  Run:     pytest tests/test_atm_p0_t2.py -v
  Ekspek:  FAIL dengan 404 — endpoint belum exist
  Implement:
    a) Tambah 5 kolom ke Fort model (models.py)
    b) Jalankan alembic revision --autogenerate + alembic upgrade head
    c) Tambah FortEnrichmentSchema + GET /{fort_id}/enrichment di routers/forts.py
    d) Update seed_data.py dengan data 4 pelabuhan utama
  Run lagi: harus GREEN semua

STEP 3 — RED: P1-M3 direction filter edge cases
  File:    backend/tests/test_atm_p1_m3.py
  Run:     pytest tests/test_atm_p1_m3.py -v
  Ekspek:  case-normalization test PASS (router sudah lowercase),
           invalid direction test FAIL (belum ada validasi)
  Implement: tambah Literal["outbound","inbound","transit"] untuk param direction
  Run lagi: GREEN

STEP 4 — RED: P1-M2 year range edge cases
  File:    backend/tests/test_atm_p1_m2.py
  Run:     pytest tests/test_atm_p1_m2.py -v
  Ekspek:  non-integer → 422 sudah handled FastAPI (GREEN),
           inverted range — tentukan dulu: 400 atau empty list
  Implement: tambah guard inverted range jika keputusan = 400
  Run lagi: GREEN

STEP 5 — RED: P1-M1 route coordinate contract
  File:    backend/tests/test_atm_p1_m1.py
  Run:     pytest tests/test_atm_p1_m1.py -v
  Ekspek:  mayoritas PASS (endpoint sudah ada), FAIL = gap nyata di koordinat
  Implement: fix NULL-coord issue di DB query jika terdeteksi
  Run lagi: GREEN

STEP 6 — REGRESSION: full suite
  Run:     docker compose exec backend pytest tests/ -v --tb=short
           docker compose exec frontend python manage.py test map_app
  Ekspek:  0 failures

STEP 7 — COVERAGE gate
  Run:     docker compose exec backend pytest tests/ \
             --cov=routers --cov=models \
             --cov-report=term-missing \
             --cov-fail-under=80
  Ekspek:  exit 0

HARD RULE: git commit hanya boleh setelah Step 6 dan Step 7 keduanya exit 0.
```

---

## Security Checklist

### Per Fitur Baru

**US-01 / US-03 — Semua link eksternal (BGB + AMH)**
- [ ] Semua `<a href="...">` ke URL eksternal wajib punya `target="_blank" rel="noopener noreferrer"`
- [ ] `source_url` dan `amh_url` divalidasi prefix di FastAPI sebelum di-return:
  - `source_url`: harus dimulai dengan `https://resources.huygens.knaw.nl`
  - `amh_url`: harus dimulai dengan `https://www.atlasofmutualheritage.nl/` atau `https://hdl.handle.net/`
- [ ] Jika URL tidak lolos validasi prefix, return `null` — jangan raise 500

```python
def sanitize_external_url(url: str | None, allowed_prefixes: tuple) -> str | None:
    if not url:
        return None
    if any(url.startswith(p) for p in allowed_prefixes):
        return url
    return None
```

**US-02 — Fetch gambar / data dari AMH (jika ada)**
- [ ] Jangan terima URL gambar dari input user — gunakan allowlist hardcoded
- [ ] Semua `httpx.get()` ke domain eksternal wajib punya `timeout=5.0` dan `follow_redirects=False`
- [ ] Gunakan `defusedxml` jika parsing XML dari Huygens OpenSearch (tambah ke `requirements.txt`)
- [ ] Django auto-escape aktif — jangan gunakan `|safe` filter untuk konten dari API eksternal

**US-04 / US-05 — CORS untuk AJAX time-slider**
- [ ] Verifikasi `allow_origins` di `backend/main.py` sudah include `http://localhost:8084`
- [ ] Jangan gunakan `allow_origins=["*"]` di production
- [ ] `allow_methods=["GET"]` — semua endpoint baru ini read-only

**Nginx CSP (update sebelum merge T2)**
```nginx
add_header Content-Security-Policy "
  default-src 'self';
  script-src 'self' 'unsafe-inline' unpkg.com cdn.jsdelivr.net;
  style-src 'self' 'unsafe-inline' cdn.jsdelivr.net;
  img-src 'self' data: atlasofmutualheritage.nl www.atlasofmutualheritage.nl;
  connect-src 'self' resources.huygens.knaw.nl;
  frame-ancestors 'none';
" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

**Nginx Rate Limiting (tambah sebelum US-04 live)**
```nginx
http {
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/m;
    server {
        location /api/ {
            limit_req zone=api_limit burst=10 nodelay;
            proxy_pass http://voc_backend:8000;
        }
    }
}
```

**Environment Variables baru di `.env`**
```
AMH_BASE_URL=https://atlasofmutualheritage.nl
HUYGENS_OPENSEARCH_URL=https://resources.huygens.knaw.nl/opensearch/
EXTERNAL_API_TIMEOUT=8
```

---

## Definition of Done

Sprint dinyatakan selesai hanya jika seluruh kondisi berikut terpenuhi:

- [ ] `docker compose exec backend pytest -v` — 0 failure, coverage >= 80% untuk path yang disentuh sprint ini
- [ ] `docker compose exec frontend python manage.py test map_app` — 0 failure
- [ ] Semua existing tests di `test_forts.py`, `test_voyages.py`, `test_seed_logic.py` tetap pass tanpa modifikasi
- [ ] Setiap endpoint baru dicurl dan mengembalikan response sesuai kontrak:
  - `curl http://localhost:8084/api/forts/1` — field `amh_url`, `nama_historis` ada di response
  - `curl http://localhost:8084/api/forts/1/enrichment` — 5 field historis ada
  - `curl "http://localhost:8084/api/voyages/routes?direction=outbound"` — hanya outbound
  - `curl http://localhost:8084/ports/padang` — HTTP 200, tidak ada JS error di console
- [ ] Semua link eksternal di template sudah pakai `rel="noopener noreferrer"`
- [ ] `amh_url` dan `source_url` divalidasi prefix sebelum di-return FastAPI
- [ ] CSP header di Nginx sudah diupdate dan tidak ada browser console error terkait CSP
- [ ] `docker compose logs backend --tail 20` — tidak ada ERROR atau Traceback
- [ ] Visual spot-check: halaman `/ports/<nama>` dan peta route lines dibuka di `http://localhost:8084` — tidak ada broken layout

---

## Risk Register

| ID | Risiko | Owner | Probabilitas | Dampak | Mitigasi |
|----|--------|-------|--------------|--------|----------|
| R1 | Migrasi schema Fort gagal atau merusak data existing | DBA | Sedang | Tinggi | Semua kolom `nullable=True`; test di fresh `docker compose down -v && up` sebelum merge; `seed_data.py` diupdate dalam PR yang sama |
| R2 | Data `source_url` tidak lengkap — fitur US-01 kurang impactful | PM | Sedang | Sedang | Audit di hari 1: `SELECT COUNT(*) FROM voyages WHERE source_url IS NOT NULL`; jika < 30%, tampilkan fallback link BGB generic |
| R3 | Animasi polyline Leaflet terlalu berat untuk 4.700+ voyages | Dev | Tinggi | Sedang | `/api/voyages/routes` agregasi per rute unik, bukan per voyage; default `?limit=50` saat load awal; acceptance criteria US-04 mensyaratkan render 50 rute < 2 detik |
| R4 | XML parsing dari Huygens OpenSearch mengandung XXE atau malformed XML | DevSecOps | Rendah | Tinggi | Gunakan `defusedxml`; wrap semua `ET.fromstring()` dalam try/except; return `[]` saat `ParseError` |
| R5 | SSRF via URL fetch ke AMH/Huygens | DevSecOps | Rendah | Tinggi | Hardcode allowlist domain; `follow_redirects=False`; `timeout=5.0`; jangan terima URL dari input user |

---

## Deploy Checklist

Jalankan langkah-langkah ini secara urut setelah sprint selesai dan semua test pass.

```bash
# 1. Pastikan test semua pass di environment lokal
docker compose exec backend pytest tests/ -v --tb=short --cov=routers --cov-fail-under=80
docker compose exec frontend python manage.py test map_app

# 2. Jalankan Alembic migration
docker compose exec backend alembic upgrade head

# 3. Verifikasi kolom baru ada di database
docker compose exec db psql -U vocuser -d vocdb -c \
  "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='forts' AND column_name IN ('nama_historis','amh_url','periode_aktif');"

# 4. Seed data historis 4 pelabuhan utama
docker compose exec backend python seed_data.py

# 5. Rebuild semua container
docker compose up -d --build

# 6. Cek status semua container (semua harus Up)
docker compose ps

# 7. Cek log 5 menit pertama — tidak boleh ada ERROR
docker compose logs backend --tail 50 | grep -E "(ERROR|Exception|Traceback)"
docker compose logs frontend --tail 50 | grep -E "(ERROR|500|ImportError)"
docker compose logs nginx --tail 30 | grep -E "(502|503|error)"

# 8. Smoke test endpoint existing (pastikan tidak ada regresi)
curl -s http://localhost:8084/api/forts/ | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d),'forts')"
curl -s "http://localhost:8084/api/voyages/?limit=5" | python3 -c "import sys,json; d=json.load(sys.stdin); print([v['source_url'] for v in d])"
curl -s "http://localhost:8084/api/voyages/routes" | python3 -c "import sys,json; d=json.load(sys.stdin); r=d[0]; print(r['origin_lat'],r['dest_lat'])"

# 9. Smoke test endpoint baru sprint ini
curl -s http://localhost:8084/api/forts/1 | python3 -m json.tool | grep -E "(amh_url|nama_historis)"
curl -s http://localhost:8084/api/forts/1/enrichment | python3 -m json.tool
curl -s "http://localhost:8084/api/voyages/routes?direction=outbound" | python3 -c "import sys,json; d=json.load(sys.stdin); print('directions:',{r['direction'] for r in d})"
curl -s http://localhost:8084/ports/padang | grep -c "<html>"

# 10. Verifikasi CSP header aktif
curl -sI http://localhost:8084/ | grep -i "content-security-policy"

# 11. Buka browser manual — visual spot-check
# - http://localhost:8084/ — peta load, route lines muncul, toggle Outbound/Inbound berfungsi
# - http://localhost:8084/ports/padang — nama historis, badge VOC, link AMH tampil
# - Klik popup voyage — link BGB muncul jika source_url ada, tidak muncul jika null
# - Buka DevTools Console — tidak ada JS error

# 12. Jika semua OK: commit dan push
git push origin main
```
