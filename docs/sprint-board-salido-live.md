# Sprint Board — "SALIDO-LIVE"

**Sprint:** 2 – 16 Juli 2026 (2 minggu)
**Scrum Master:** Claude · **Product Owner:** Muhammad Ikbal
**Sumber backlog:** `~/salido-web/docs/prd-jurnal-blog.md`, `~/salido-web/docs/spec-sprint-jurnal.md`, `docs/adr-001-www-http3-redis.md`

---

## Sprint Goal

> **"Pembaca bisa membaca artikel jurnal perdana di salido.my.id yang tayang lewat jalur delivery yang kanonik (tanpa www), cepat (HTTP/3 + Redis), dan lolos gerbang QA."**

Sprint dianggap sukses bila ketiga kalimat ini benar pada 16 Juli:
1. `https://salido.my.id/jurnal/<slug>/` menampilkan ≥ 1 artikel nyata (bukan dummy).
2. `www.salido.my.id` → 301 ke apex; browser bicara HTTP/3 ke edge.
3. `GET /api/voyages` kedua kalinya dilayani dari Redis; seluruh suite test hijau.

## Target Terukur Sprint

| # | Target | Baseline | Cara ukur | Pemilik |
|---|--------|----------|-----------|---------|
| T1 | 1–2 artikel jurnal terbit | 0 | indeks /jurnal/ production | PO + QA |
| T2 | Lighthouse mobile artikel: Perf ≥ 90, A11y ≥ 90 | belum ada | Lighthouse manual | QA |
| T3 | www → apex 301 + `alt-svc: h3` di response edge | keduanya belum | `curl -sI` + devtools protocol | DevSecOps |
| T4 | Latensi p50 `/api/voyages` (cache hit) < 30 ms internal | ~ratusan ms (query PostGIS) | `curl -w '%{time_total}'` 2× | DBA |
| T5 | Test suite: backend pytest + Django test 100% pass, +≥ 6 test baru cache | 120 + 66 pass | `docker compose exec ... pytest / manage.py test` | QA |
| T6 | 0 secret/credential baru di kode (checklist CLAUDE.md) | — | review pre-commit | DevSecOps |

---

## Struktur Tim

Proyek solo — "tim" adalah topi peran dengan tanggung jawab dan gerbang keputusan yang jelas. Satu orang boleh pindah topi, **tetapi item tidak boleh pindah ke Done tanpa tanda tangan topi QA**.

### Tim DBA — data & cache
**Scope:** PostgreSQL/PostGIS, Redis, Alembic, seed pipeline.
**Tanggung jawab:** service `voc_redis` (maxmemory 128mb, allkeys-lru, tanpa port publik), modul `backend/cache.py` (cache-aside, degradasi anggun saat Redis down), invalidasi `voc:*` di `seed_data.py`, jaga migration Alembic tetap jalan.
**Gerbang keputusan:** skema key cache, TTL, kebijakan eviction, index spasial.

### Tim DevSecOps — delivery & keamanan
**Scope:** Nginx (host + Docker), Cloudflare, docker-compose, git hygiene, secrets.
**Tanggung jawab:** server block www→apex + DNS record, toggle HTTP/3 edge + verifikasi, perbarui komentar QUIC di `nginx/nginx.conf` (keputusan: edge-only), security checklist sebelum tiap commit, kompresi aset (icon 930KB → < 50KB), deploy `deploy.sh` + smoke check.
**Gerbang keputusan:** perubahan apa pun di config production, apa yang boleh di-commit.

### Tim QA — gerbang kualitas
**Scope:** TDD enforcement, acceptance criteria, verifikasi production.
**Tanggung jawab:** pastikan urutan RED→GREEN tidak dibalik (test cache ditulis & FAIL dulu sebelum `cache.py`), jalankan DoD tiap US (build Astro, cek 375px/1440px, kontras, Lighthouse), checklist deploy CLAUDE.md (curl 200, logs bersih), tolak item Done yang kriterianya tidak terpenuhi.
**Gerbang keputusan:** satu-satunya peran yang boleh memindahkan kartu ke **Done**.

### Tim Dev/Konten *(tambahan — tidak diminta, tapi wajib ada)*
Jurnal butuh eksekusi Astro + penulisan artikel (US-J1–J5). Tanpa lane ini board hanya berisi infra. **Scope:** komponen Astro/MDX, tulisan, optimasi gambar dari `research/`.

---

## Board

Kolom: **Backlog → Sprint (To Do) → In Progress → Review (QA) → Done**
Aturan: WIP limit **2 kartu** In Progress; kartu infra & kartu konten boleh paralel (beda tim); blocker ditulis di kartu, bukan didiamkan.

### Done ✅ (carry-in, 2 Jul)
| ID | Kartu | Tim |
|----|-------|-----|
| HK-1 | Dedup repo salido-web → kanonik `~/salido-web` (b961350) | DevSecOps |
| HK-2 | Rapikan `research/` 141MB + hapus junk Zone.Identifier | DevSecOps |
| DOC-1 | ADR-001 (www/HTTP3/Redis) disepakati | — |
| DOC-2 | PRD + Spec Sprint Jurnal | — |
| INF-1 | Commit hygiene (2 Jul): ADR+board 6f7811a, branding atlas 9570cb1 (icon 930KB→3.4KB, rebuild+79 test pass, nginx restart karena stale upstream IP), salido-web 9ee929b | DevSecOps ✓QA |
| DBA-1 | test_cache.py 19 test — RED terbukti (ModuleNotFoundError: cache) sebelum implement | DBA ✓QA |
| DBA-2 | voc_redis (128mb/allkeys-lru) + cache.py + cache-aside di voyages/, forts/, forts/routes/all, glossary, glossary/lookup. Bukti: /api/forts MISS 76ms→HIT 3ms; suite 151 pass. Commit 3e04cbb | DBA ✓QA |
| DBA-3 | Flush voc:* di akhir seed_data.py (invalidate_prefix_sync) + 2 test | DBA ✓QA |
| FIX-1 | (Bonus) 8 test US-06 pre-existing fail — env SYNC_DATABASE_URL absen di compose (fallback ter-scrub US-07); ditambahkan → 151 pass 0 fail | DevSecOps ✓QA |
| JRN-1 | Collection `jurnal` + schema Zod + MDX + draft filter + `_contoh.mdx`. Bukti: build gagal jelas saat frontmatter invalid; draft absen dari dist/ | Dev ✓QA |
| JRN-2 | Layout artikel longform: hero full-bleed, drop cap, PullQuote/FullBleedImage/ArchiveNote, footnotes GFM, blok Sumber, prev/next | Dev ✓QA |
| JRN-3 | Indeks /jurnal/ (featured+grid+empty state+BookSpoiler→seksi Buku) + tag pages. Artikel demo draft: laporan-hoffman-1681 (seri Gunung Arum). Direview PO 2 Jul ("sudah bagus") → commit 4320bf2 | Dev ✓QA ✓PO |
| JRN-4 | SEO: @astrojs/sitemap + robots.txt, OG lengkap (og:type/site_name/twitter, og:image absolut), JSON-LD Article. Commit salido-web (JRN-4). DBA cache di-commit westkust 3e04cbb | Dev ✓QA |
| JRN-5 | Artikel #1 "Tembakan di Tambang" TERBIT (draft:false, cover 297KB) — 144a6c9 | Dev/Konten ✓QA |
| IMG-1 | public/img 30.6MB→3.3MB, semua ≤300KB, master ke research/img/master — 43e799e | Dev ✓QA |
| TYPE-1 | Token --font-display + --color-accent-bright + scrim hangat; Hero.astro tunggal utk ID+EN — 6d653b5 | Dev ✓QA |
| FTR-1 | Footer global (Base.astro, noFooter utk atlas) — 2cb7c2e | Dev ✓QA |
| HOME-1 | Beranda etalase: seksi Jurnal + Atlas full-bleed + Buku + scroll-hint — 316bb33 | Dev ✓QA |
| NAV-1 | Hub /sejarah (prolog+tambang+8 bab nonaktif); /tambang → 301 meta-refresh — 42e1818 | Dev ✓QA |
| ATLAS-1 | Atlas imersif: 1 navbar + chip ← salido.my.id, 100svh — 7b2ab61 | Dev ✓QA |
| INF-2-prep | nginx-prod.conf: block www→apex 301 (80+443); nginx -t wajib di server (runbook) — 088ab56 | DevSecOps ✓QA |
| JRN-6 | Draft artikel #2 "Tanah yang Tidak Mudah Diambil" (Bab 2 naskah, 685 kata, draft:true) — 9d9b9a6 | Dev/Konten ✓QA |
| NGX-1 | Fix 502 stale-IP: resolver 127.0.0.11 + proxy_pass variable; TERBUKTI rebuild backend → 200 tanpa restart nginx — e5140cb | DevSecOps ✓QA |
| INF-3-prep | Komentar QUIC kini merujuk ADR-001 (h3 edge-only) — 8953080 | DevSecOps ✓QA |
| RUNBOOK | docs/runbook-production-www-h3.md — langkah manual Cloudflare+deploy utk PO — 828ebba | DevSecOps ✓QA |
| DBA-AUDIT | Redis sehat (hit 79%, 1.35MB/128MB); index voyages sudah lengkap; ANALYZE 0.62→0.14ms; TEMUAN KRITIS: chain Alembic putus — b58aed9 | DBA ✓QA |
| BLUE | Audit defensif: rate-limit/CORS/headers/secret-scan PASS; 2 temuan SEDANG (port 8001, .env scaffold ter-track) — docs/audit-blueteam-2026-07.md | Blue ✓QA |
| QA-2 | Lighthouse (chrome-headless-shell) artikel production: A11y 93 ✅, Perf 74 ❌(<90), CLS 0, TBT 0 — 2 temuan a11y lanjutan | QA |

### Sprint (To Do) — Wave 3, urutan disetujui PO 3 Jul

| # | ID | Kartu | Tim | SP | Status |
|---|----|-------|-----|----|--------|
| 1 | ALEMBIC-1 | ✅ DONE 3 Jul — down_revision → '002_amh_images', DB stamp 003 (head), upgrade no-op, 151 pass. Commit westkust | DBA ✓QA | 1 | **Done** |
| 2 | HIST-1b | Halaman /sejarah/historiografi: KartuBibliografi + SpineSumber + 9 lapis dari src/data/historiografi.ts (skema §3); masuk hub /sejarah | Dev/Konten | 3 | **In Progress** |
| 3 | PERF-2 | Lighthouse Perf 74→≥90 halaman artikel (LCP 3.9s): preload hero+font, srcset, cek render-blocking | Dev | 2 | To Do |
| 4 | A11Y-2 | Kontras ArchiveNote (.tahun/.archive-sumber 4.16→≥4.5), landmark <main> di layout, lengkapi security headers di respons 429 | Dev | 1 | To Do |
| 5 | SEC-1 | compose: hapus publish port 8001 (bypass nginx + dev server); untrack backend/.env & frontend/.env scaffold (+ .gitignore) | DevSecOps | 1 | To Do |
| 6 | HIST-1c | Aset domain publik historiografi (potret Camões Wikimedia, kliping Soerabajasch Handelsblad Delpher) + kredit + QA halaman | Dev/Konten | 2 | To Do |
| 7 | DEPLOY | Production: PO eksekusi runbook (Cloudflare CNAME www + toggle HTTP/3) + deploy nginx-prod.conf & build salido-web; QA verifikasi T3 | PO + DevSecOps | 2 | ⛔ Menunggu izin/aksi PO |

**Backlog (parkir — ditarik lewat keputusan PO)**
- Konten & fitur jurnal: RSS, halaman seri, related articles, `<AtlasLink>` embed peta di artikel, bilingual R6 + hreflang, Pagefind (>20 artikel), newsletter (≥10 artikel), sitasi akademik ("Salin sitasi")
- Desain: dark mode (tokens sudah CSS vars), scrollytelling peta artikel
- Teknis (temuan audit): drop 3 index redundan voyages (ix_voyages_year, ix_voyages_id, ix_voyages_direction — laporan DBA), hilangkan CSP 'unsafe-inline' (TODO US-11), hardcode #D8B13B sisa di tambang/atlas (catatan TYPE-1), publish artikel #2 setelah edit PO
- Infra: deploy westkust Docker ke VPS (atlas production menyatu /westkust → 301 /atlas per ATLAS-1)

**Wave 1–2 selesai: 30 kartu Done (≈49 SP). Wave 3: 12 SP** — muat dalam sisa sprint (s.d. 16 Jul) dengan longgar; DEPLOY di luar SP (aksi manual PO + verifikasi).

---

## Ceremonies (disesuaikan solo)

- **Daily (async, 5 menit):** update kolom board + tulis blocker di kartu. Bisa pakai `/standup`.
- **Mid-sprint review (9 Jul):** Lane INFRA harus Done. Jika DBA-2 molor > 1 hari, potong scope: cache hanya `/api/voyages` (endpoint terberat), sisanya ke backlog.
- **Sprint review (16 Jul):** demo 3 kalimat Sprint Goal, bukti target T1–T6.
- **Retro (16 Jul):** 3 pertanyaan — apa yang lambat, gerbang QA mana yang hampir dilewati, apa yang masuk sprint berikut (kandidat: bilingual R6 + RSS + artikel #3).

## Definition of Done (semua kartu)

1. Acceptance criteria kartu tercentang dengan bukti (output curl/test/screenshot).
2. Test relevan pass; untuk backend: TDD RED→GREEN terbukti (QA cek riwayat).
3. Checklist keamanan CLAUDE.md lolos sebelum commit.
4. Untuk yang menyentuh production: deploy + smoke check + logs bersih.
5. QA yang memindahkan kartu ke Done — bukan penulis kartu.
