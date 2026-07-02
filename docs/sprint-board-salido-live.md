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
| DBA-2 | voc_redis (128mb/allkeys-lru) + cache.py + cache-aside di voyages/, forts/, forts/routes/all, glossary, glossary/lookup. Bukti: /api/forts MISS 76ms→HIT 3ms; suite 151 pass. **Belum di-commit — menunggu review PO** | DBA ✓QA |
| DBA-3 | Flush voc:* di akhir seed_data.py (invalidate_prefix_sync) + 2 test | DBA ✓QA |
| FIX-1 | (Bonus) 8 test US-06 pre-existing fail — env SYNC_DATABASE_URL absen di compose (fallback ter-scrub US-07); ditambahkan → 151 pass 0 fail | DevSecOps ✓QA |
| JRN-1 | Collection `jurnal` + schema Zod + MDX + draft filter + `_contoh.mdx`. Bukti: build gagal jelas saat frontmatter invalid; draft absen dari dist/ | Dev ✓QA |
| JRN-2 | Layout artikel longform: hero full-bleed, drop cap, PullQuote/FullBleedImage/ArchiveNote, footnotes GFM, blok Sumber, prev/next | Dev ✓QA |
| JRN-3 | Indeks /jurnal/ (featured+grid+empty state+BookSpoiler→seksi Buku) + tag pages. Artikel demo draft: laporan-hoffman-1681 (seri Gunung Arum). Direview PO 2 Jul ("sudah bagus") → commit 4320bf2 | Dev ✓QA ✓PO |
| JRN-4 | SEO: @astrojs/sitemap + robots.txt, OG lengkap (og:type/site_name/twitter, og:image absolut), JSON-LD Article. Commit salido-web (JRN-4). DBA cache di-commit westkust 3e04cbb | Dev ✓QA |

### Sprint (To Do)

**Lane INFRA — minggu 1 (3–9 Jul)**
| ID | Kartu | Tim | SP | Acceptance (ringkas) |
|----|-------|-----|----|----------------------|
| INF-2 | www→apex: DNS `www` (proxied) + server block 301 di `nginx-prod.conf`, deploy, `nginx -t`, reload | DevSecOps | 2 | `curl -sI https://www.salido.my.id/x` → 301 `https://salido.my.id/x` |
| INF-3 | HTTP/3: toggle Cloudflare + verifikasi h3 + update komentar QUIC `nginx/nginx.conf` | DevSecOps | 1 | devtools protocol = h3; komentar tidak lagi menyarankan QUIC origin |
| QA-1 | Verifikasi infra: full suite + T4 latency + logs + deploy checklist CLAUDE.md | QA | 2 | T3–T6 tercentang dengan bukti |

**Lane JURNAL — minggu 1–2 (3–15 Jul)**
| ID | Kartu | Tim | SP | Acceptance (ringkas) |
|----|-------|-----|----|----------------------|
| JRN-5 | US-J5: artikel perdana #1 (tambang 1681) + optimasi gambar WebP ≤ 300KB | Dev/Konten | 5 | terbit non-draft, kredit arsip lengkap |
| JRN-6 | Artikel perdana #2 (bab Gunung Arum) — *stretch* | Dev/Konten | 3 | boleh jatuh ke sprint berikut |
| QA-2 | Gerbang QA Jurnal: Lighthouse T2, kontras, reduced-motion, deploy + smoke production | QA | 2 | T1–T2 tercentang dengan bukti |

**Usulan dari tinjauan desain 2 Jul (`~/salido-web/docs/desain-skema-web.md`) — menunggu keputusan PO**
| ID | Kartu | Prioritas |
|----|-------|-----------|
| HOME-1 | Beranda: seksi jurnal terbaru + teaser atlas + teaser buku + petunjuk scroll | 1 — usul masuk sprint |
| IMG-1 | Diet gambar public/ (9.2MB/7.6MB/6MB → WebP ≤300KB; master ke research/) | 2 — usul masuk sprint |
| FTR-1 | Footer global (kolofon, kontak, kredit arsip, ©) | 3 — usul masuk sprint |
| NAV-1 | IA: /tambang → /sejarah/tambang, prolog → /sejarah/prolog, hub sejarah | backlog |
| TYPE-1 | Konsolidasi: display Crimson 600 semua judul, token --color-accent-bright, scrim seragam, satu Hero.astro | backlog |
| ATLAS-1 | Mode imersif /atlas (hapus double navbar) + 301 /westkust/ → /atlas | backlog |

**Backlog (parkir — jangan ditarik tanpa menukar kartu keluar)**
RSS, halaman seri, related articles, `<AtlasLink>`, bilingual R6 + hreflang, Pagefind, dark mode, newsletter, scrollytelling, deploy westkust Docker ke VPS, sitasi akademik.

**Total sprint: 37 SP** (INFRA 15 · JURNAL 22, termasuk stretch 3). Kapasitas solo ±2 SP/hari kerja efektif → realistis dengan stretch sebagai penyangga.

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
