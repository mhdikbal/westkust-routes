# Audit Blue Team — Juli 2026

**Tanggal:** 2026-07-02
**Ruang lingkup:** aset lokal milik sendiri — `http://localhost:8084` (nginx → FastAPI + Django), repo `/home/naro/westkust-routes`, repo `/home/naro/salido-web`. Audit defensif, read-only terhadap kode.
**Metode:** inspeksi header HTTP, uji burst rate limit, uji CORS origin jahat, review konfigurasi (nginx.conf, docker-compose, settings), grep statis pola secret, `npm audit`, inventaris pip.

---

## Ringkasan Eksekutif

Postur keamanan aplikasi lokal **baik secara umum**: security headers lengkap dan konsisten dengan `nginx/nginx.conf`, rate limit berfungsi persis sesuai desain (60 r/m + burst 20, 429 JSON dengan `Retry-After`), CORS menolak origin asing, error handling tidak membocorkan stack trace, `DEBUG=False`, tidak ditemukan secret di working tree maupun 5 commit terakhir kedua repo, dan `npm audit --omit=dev` bersih.

Dua temuan **Sedang**: (1) port frontend `8001` ter-publish ke `0.0.0.0` sehingga nginx (CSP, rate limit) bisa di-bypass, dan container menjalankan Django dev server (`WSGIServer`); (2) `backend/.env` dan `frontend/.env` ter-track di git — isinya sisa scaffold lama (Mongo/React) tanpa kredensial nyata, tetapi melanggar kebijakan repo dan berisiko jadi preseden.

---

## Tabel Temuan

| # | Severity | Temuan | Bukti (perintah → hasil ringkas) | Rekomendasi |
|---|----------|--------|----------------------------------|-------------|
| 1 | **Sedang** | Port frontend `8001` ter-publish ke `0.0.0.0` — akses langsung mem-bypass nginx: tanpa CSP, tanpa `X-Frame-Options`, tanpa Permissions-Policy, tanpa rate limit. Respons juga mengungkap `Server: WSGIServer/0.2 CPython/3.11.15` → Django **dev server** (`runserver`) dipakai, bukan WSGI server production. | `docker compose ps` → `voc_frontend 0.0.0.0:8001->8001`; `curl -D- http://localhost:8001/` → 200, header hanya `X-Content-Type-Options`, `Referrer-Policy: same-origin`, `COOP` (set Django), **tanpa CSP/XFO** | Hapus mapping `ports: 8001:8001` di `docker-compose.yml` (nginx mengakses via network internal Docker, publish tidak diperlukan) atau minimal bind `127.0.0.1:8001:8001`. Untuk production: ganti `manage.py runserver` → gunicorn/uvicorn worker. |
| 2 | **Sedang** | `backend/.env` dan `frontend/.env` **ter-track di git** meski pola `.env` ada di `.gitignore` (baris 38) — file di-commit sebelum ignore berlaku. Isinya sisa scaffold lama (kunci `MONGO_URL`, `DB_NAME`, `CORS_ORIGINS`, `REACT_APP_BACKEND_URL`, dst — tidak dipakai stack FastAPI/Postgres saat ini) dan **tidak mengandung kredensial `user:pass`**. Root `.env` (berisi secret asli) sudah benar ter-gitignore dan tidak ter-track. | `git ls-files \| grep .env` → `backend/.env`, `frontend/.env` muncul; inspeksi nilai (diredaksi) → tidak ada pola kredensial `://user:pass@`; `git check-ignore -v .env` → `.gitignore:38` | `git rm --cached backend/.env frontend/.env` lalu commit (file tetap di disk). Karena tanpa kredensial nyata, rewrite histori tidak wajib. Pastikan `.env.example` tetap jadi satu-satunya template yang di-commit. |
| 3 | **Rendah** | Respons **429 kehilangan sebagian security headers**: hanya `X-Frame-Options` + `X-Content-Type-Options` + `Retry-After` yang di-set ulang di `location = /rate_limited`; `Referrer-Policy`, `Permissions-Policy`, dan `CSP` hilang (perilaku inheritance `add_header` nginx — sudah disadari di komentar nginx.conf baris 76–79 tetapi implementasinya belum lengkap). | Burst 25× lalu `curl -D-` → `HTTP 429` dengan `Retry-After: 60`, XFO, XCTO — **tanpa** Referrer-Policy/Permissions-Policy/CSP | Tambahkan tiga `add_header` yang hilang di blok `/rate_limited` (Referrer-Policy, Permissions-Policy, CSP). Dampak praktis kecil (body JSON statis), tapi konsistensi murah dicapai. |
| 4 | **Rendah** | CSP memakai `script-src 'unsafe-inline'` — melemahkan proteksi XSS. Sudah tercatat sebagai TODO di nginx.conf (menunggu US-11 onclick cleanup). | `curl -D- http://localhost:8084/` → CSP `script-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net` | Selesaikan US-11 (pindahkan handler inline ke file JS eksternal), lalu hapus `'unsafe-inline'`; pertimbangkan nonce/hash bila masih perlu inline. |
| 5 | **Rendah** | Versi nginx terekspos di header `Server: nginx/1.25.5` — memudahkan fingerprinting CVE. | Semua respons via :8084 → `Server: nginx/1.25.5` | Tambahkan `server_tokens off;` di blok `http {}` nginx.conf. |
| 6 | **Rendah** | `/docs` (Swagger UI) dan `/openapi.json` terbuka publik. Sudah di-rate-limit (burst 5), API memang read-only, tapi di production dokumen skema memperluas permukaan recon. | `curl` → keduanya `HTTP 200` | Untuk production: nonaktifkan via `FastAPI(docs_url=None, openapi_url=None)` yang dikendalikan env var, atau batasi per-IP di nginx. Untuk dev lokal boleh tetap terbuka. |
| 7 | **Info** | Security headers halaman `/` dan `/api/voyages/` **lengkap dan konsisten** dengan nginx.conf: XFO `DENY`, XCTO `nosniff`, Referrer-Policy `strict-origin-when-cross-origin`, Permissions-Policy (geolocation/mic/camera/payment dimatikan), CSP dengan `frame-ancestors 'none'`, `base-uri`, `form-action`. HSTS belum ada — wajar karena masih plain HTTP lokal; aktifkan bersama TLS (US-13). | `curl -D-` kedua path → header identik sesuai nginx.conf baris 54–74 | Tidak ada aksi sekarang; tambah `Strict-Transport-Security` saat TLS aktif. |
| 8 | **Info** | Rate limit **berfungsi sesuai desain**: zona 60 r/m + burst 20 nodelay → request ke-22 dst mendapat 429 JSON `{"error":"rate_limit_exceeded",...}` dengan `Retry-After: 60`. | 30× `curl` cepat → `200 ×21, 429 ×9` | — (lihat temuan #3 untuk header 429). |
| 9 | **Info** | CORS **aman**: `Origin: https://evil.example` pada GET → 200 **tanpa** `Access-Control-Allow-Origin`; preflight OPTIONS origin sama → **400** tanpa ACAO. Konfigurasi backend: `allow_origins` dari env `ALLOWED_ORIGINS` (default `http://localhost:8084`), `allow_credentials=False`, methods `GET, OPTIONS` saja. | `curl -H "Origin: https://evil.example"` GET & OPTIONS | — |
| 10 | **Info** | Error handling **bersih**: `/api/voyages/999999999` → 404 JSON `{"detail":"Voyage with id=... not found"}`; `/api/voyages/abc` → 422 Pydantic JSON; path traversal `/api/../../etc/passwd` → halaman 404 generik Django; path aneh ber-null-byte → 400. `DEBUG = False` terverifikasi runtime di container frontend. Tidak ada stack trace di respons mana pun. | `curl` masing-masing path; `python -c "...settings.DEBUG"` di container → `False` | — |
| 11 | **Info** | Statis bersih: grep pola secret (`password=`, `api_key`, `token`, `BEGIN PRIVATE KEY`, dll.) di working tree kedua repo → nihil (di luar temuan #2); `git log -5 --stat` kedua repo → tidak ada file sensitif baru; `DJANGO_SECRET_KEY` dibaca dari env var (`settings.py:6`), tidak hardcoded. | grep + git log kedua repo | — |
| 12 | **Info** | Dependensi: `npm audit --omit=dev` (salido-web, Node 22) → **0 vulnerabilities**. Inventaris pip backend (informasional): fastapi 0.111.0, httpx 0.27.0, asyncpg 0.29.0, alembic 1.13.1, GeoAlchemy2 0.15.0, dll. | perintah audit masing-masing | Jadwalkan `npm audit` & pemindaian pip (mis. `pip-audit`) berkala. |
| 13 | **Info** | Dev server salido `:4321` sedang hidup — respons 200 tanpa security headers (hanya `Vary: Origin`). **Wajar untuk dev Astro**; header production di-set nginx di host salido, di luar lingkup audit ini. | `curl -D- http://localhost:4321/` | Tidak ada aksi; pastikan port dev tidak ter-expose keluar WSL/host. |
| 14 | **Info** | Exposure port compose: hanya `8084` (nginx) dan `8001` (frontend — lihat #1) yang ter-publish. Backend `8000`, Postgres `5432`, Redis `6379` **tidak** ter-publish ke host — baik. | `docker compose config` → blok `ports:` hanya di frontend & nginx | — |

---

## Batasan Audit

- Tidak menguji server production/remote (di luar aturan tugas — tanpa SSH, tanpa Cloudflare).
- Isi file `.env` tidak ditampilkan; hanya nama kunci dan hasil uji pola kredensial (negatif).
- Histori git hanya diperiksa 5 commit terakhir per repo.
- Tidak ada perubahan kode/konfigurasi dilakukan; semua rekomendasi menunggu kartu perbaikan terpisah.
