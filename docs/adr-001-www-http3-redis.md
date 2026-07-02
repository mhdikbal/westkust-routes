# ADR-001: Kanonikalisasi www, HTTP/2 + HTTP/3, dan Redis Cache Layer

**Status:** Proposed
**Date:** 2026-07-02
**Deciders:** Muhammad Ikbal (owner salido.my.id / westkust-routes)

## Context

Stack production saat ini:

```
Browser ── (Cloudflare edge, orange-cloud, Full Strict)
              └── Host Nginx 1.31.2 :443 (TLS, Cloudflare Origin Cert)
                     ├── /           → Astro static (/var/www/salido/dist)
                     ├── /westkust/  → Docker voc_nginx :8084
                     └── /api/       → Docker voc_nginx :8084
                                          ├── voc_backend (FastAPI) :8000
                                          ├── voc_frontend (Django) :8001
                                          └── voc_db (PostGIS) :5432
```

Kondisi & kendala:

- `salido.my.id` dan `www.salido.my.id` saat ini dilayani **identik** di satu
  server block — duplicate content untuk SEO, tidak ada host kanonik.
- HTTP/2 sudah `on` di host Nginx (US-15). Nginx dalam Docker
  (`nginx:1.25-alpine`) hanya bicara HTTP/1.1 ke host — tidak masalah karena
  itu hop internal loopback.
- HTTP/3 belum aktif di manapun. Semua trafik publik lewat Cloudflare edge,
  sehingga koneksi browser↔edge lah yang menentukan protokol yang dirasakan
  pengguna; Cloudflare→origin selalu HTTP/1.1/HTTP/2, **tidak pernah** h3.
- Data VOC bersifat historis-statis (4.700+ voyage, berubah hanya saat
  re-seed), tapi setiap request `/api/voyages` tetap query PostGIS.
- Server: VPS 2 GB RAM — budget memori ketat; Postgres + 3 container sudah
  jalan di sana (rencana deploy westkust).

## Decision

1. **www → apex 301.** `www.salido.my.id` menjadi redirect permanen ke
   `https://salido.my.id` (apex kanonik) via server block terpisah di host
   Nginx + DNS record `www` (CNAME, proxied) di Cloudflare.
2. **HTTP/2 tetap di origin; HTTP/3 diaktifkan di Cloudflare edge** (toggle
   dashboard). QUIC di origin *tidak* diaktifkan — sia-sia di belakang
   orange-cloud dan menambah permukaan konfigurasi (UDP 443, firewall).
3. **Redis sebagai cache-aside di FastAPI** untuk endpoint read-heavy
   (`/api/voyages`, `/api/forts`, `/api/glossary`), TTL panjang (24 jam),
   `maxmemory 128mb` + `allkeys-lru`, container baru `voc_redis` di
   docker-compose (internal network, tanpa port publik).

## Options Considered

### Keputusan 1 — Penanganan www

#### Option A: 301 redirect www → apex (dipilih)

| Dimension | Assessment |
|-----------|------------|
| Complexity | Low — satu server block + satu DNS record |
| Cost | Nol |
| SEO | Satu host kanonik, link equity terkonsolidasi |
| Cert | Origin cert Cloudflare men-cover `*.salido.my.id` — aman |

**Pros:** konsisten dengan konvensi domain pendek modern; cocok dengan
`connect-src 'self'` di CSP (tidak ada cross-host fetch).
**Cons:** satu hop redirect ekstra bagi pengunjung yang mengetik `www.` (sekali,
lalu di-cache browser karena 301).

#### Option B: Melayani keduanya + `<link rel=canonical>`

**Pros:** tanpa redirect. **Cons:** canonical tag harus dijaga di Astro *dan*
Django; cookie/localStorage terpecah dua origin; CSP `'self'` bermakna ganda.
Ditolak.

### Keputusan 2 — HTTP/3

#### Option A: HTTP/3 di Cloudflare edge saja (dipilih)

| Dimension | Assessment |
|-----------|------------|
| Complexity | Low — satu toggle dashboard (Network → HTTP/3 with QUIC) |
| Cost | Nol |
| Dampak nyata | Browser↔edge pakai h3; inilah 100% latensi yang dirasakan user |
| Risiko | Nol di origin — tidak ada perubahan config |

#### Option B: QUIC juga di origin Nginx (`listen 443 quic`)

**Pros:** "lengkap" di atas kertas. **Cons:** Cloudflare tidak pernah memakai
h3 ke origin, jadi listener QUIC hanya terpakai jika ada klien bypass CDN —
yang justru ingin kita cegah (Full Strict). Buka UDP 443 = permukaan serang
baru tanpa manfaat. Ditolak; komentar persiapan h3 di `nginx/nginx.conf`
(baris 32–42) diperbarui agar tidak menyesatkan.

### Keputusan 3 — Caching layer

#### Option A: Redis cache-aside di FastAPI (dipilih)

| Dimension | Assessment |
|-----------|------------|
| Complexity | Medium — container baru + dekorator cache di 3 router |
| Cost | ~40–60 MB RSS (maxmemory 128 MB hard cap) |
| Scalability | Cache bertahan lintas restart backend; bisa dipakai Django juga |
| Team familiarity | Pola standar; `redis.asyncio` sudah async-native seperti stack |

**Pros:** menghilangkan query PostGIS berulang untuk data yang praktis
immutable; TTL + invalidasi eksplisit saat `seed_data.py` jalan
(`FLUSHDB`/prefix delete); satu tempat untuk kebutuhan cache berikutnya
(rate-limit state, session, SRI manifest).
**Cons:** satu proses lagi di VPS 2 GB; satu dependency baru (`redis` pip).

#### Option B: Nginx `proxy_cache` untuk /api/

**Pros:** nol kode Python, sangat cepat. **Cons:** invalidasi kasar (purge by
path saja, perlu modul komersial untuk wildcard); kombinasi query param
(`year_from`/`year_to`/`direction`) meledakkan cache key tanpa kontrol;
tidak reusable untuk kebutuhan non-HTTP. Layak sebagai *pelengkap* nanti,
bukan pengganti.

#### Option C: In-process LRU (functools/cachetools)

**Pros:** nol infra. **Cons:** hilang tiap restart/rebuild container (sering,
karena workflow `--build`); per-worker duplikat; tidak bisa dipakai Django.
Ditolak untuk production, boleh untuk dev.

## Trade-off Analysis

- **www:** biaya satu redirect 301 sekali per browser vs. kejelasan origin
  tunggal untuk SEO, CSP, dan cookie — jelas menang redirect.
- **HTTP/3:** semua kompleksitas QUIC dipindahkan ke Cloudflare yang memang
  sudah mengoperasikannya; origin tetap sederhana. Kita "kehilangan" h3
  origin yang memang tidak akan pernah dipakai.
- **Redis vs tanpa cache:** data VOC dibaca ribuan kali, ditulis hampir tidak
  pernah — rasio baca/tulis ekstrem adalah kasus terbaik cache-aside. Biaya
  memori di-cap 128 MB, jauh di bawah headroom VPS setelah Postgres
  (~300–400 MB). Risiko stale data ditangani dengan invalidasi di seeder,
  bukan TTL pendek.

## Consequences

- Lebih mudah: audit SEO, penulisan CSP, dan analitik (satu host);
  penambahan fitur cache berikutnya (Redis sudah ada).
- Lebih sulit: `seed_data.py` kini wajib flush cache — langkah baru yang bisa
  terlupa (mitigasi: flush dipanggil otomatis di akhir seeder).
- Perlu revisit: jika trafik `/westkust/` naik signifikan, tambahkan Nginx
  `proxy_cache` untuk HTML Django di atas Redis API cache; jika pindah dari
  Cloudflare, keputusan HTTP/3 origin harus dibuka lagi.

## Action Items

1. [ ] **www** — tambah DNS record `www` CNAME → `salido.my.id` (proxied) di
       Cloudflare; pecah server block di `salido-web/nginx-prod.conf`:
       block `www.salido.my.id` → `return 301 https://salido.my.id$request_uri;`
       (port 80 dan 443); hapus `www` dari block utama; deploy + `nginx -t` +
       `systemctl reload nginx`.
2. [ ] **HTTP/3** — aktifkan toggle "HTTP/3 (with QUIC)" di Cloudflare
       dashboard; verifikasi header `alt-svc: h3=...` dan protokol h3 via
       browser devtools; perbarui komentar persiapan QUIC di
       `nginx/nginx.conf` (keputusan: edge-only).
3. [ ] **Redis** — TDD sesuai CLAUDE.md:
   - [ ] Tulis test `backend/tests/test_cache.py` (hit/miss, TTL, invalidasi
         via prefix delete, backend tetap jalan saat Redis down → fallback DB).
   - [ ] Tambah service `redis:7-alpine` di `docker-compose.yml`
         (`command: redis-server --maxmemory 128mb --maxmemory-policy allkeys-lru`,
         `expose: 6379`, tanpa `ports`).
   - [ ] `backend/cache.py`: helper `redis.asyncio` + dekorator cache-aside;
         key = `voc:{router}:{sorted-query-params}`; `REDIS_URL` env var;
         degradasi anggun kalau koneksi gagal.
   - [ ] Terapkan di `routers/voyages.py`, `forts.py`, `glossary.py`
         (GET list/detail; **bukan** `/api/voyages/export` — streaming).
   - [ ] `seed_data.py`: flush prefix `voc:*` setelah seed sukses.
   - [ ] Verifikasi: `docker compose exec backend pytest`, curl 2× dan
         bandingkan latensi, `docker compose logs backend --tail 20`.
