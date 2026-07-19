# PRD: Migrasi Linimasa dari Django+Vanilla JS ke Astro.js

**Status:** Draft untuk review — Stack dikonfirmasi
**Tanggal:** 2026-07-15
**Author:** opencode (otomatis)
**Depends on:** `prd/prd-linimasa-kronik-pantai-barat.md`, `prd/prd-redesign-kronik-anti-slop.md`, `design-kronik-pantai-barat-1600-1690.md`

**Stack dikonfirmasi (2026-07-15):**
- **Astro.js** — SSG, zero-JS by default
- **Preact** — interactive islands (3KB vs React 40KB)
- **Tailwind CSS** — scoped styling, design tokens
- **TypeScript** — type safety
- **Vanilla JS** — hal sederhana (view toggle, header scroll)

---

## 1. Executive Summary

Migrasi halaman `/linimasa` dari stack Django SSR + vanilla JS (1.217 baris template tunggal) ke Astro.js sebagai static site generator dengan component-based architecture. Backend FastAPI tetap menjadi satu-satunya sumber data; Django frontend dihapus untuk linimasa.

**Mengapa sekarang:**
- Template tunggal 1.217 baris sudah mencapai batas maintainability vanilla JS
- 412 baris JS interaktif (chronicle controller, scrubber, port map) sulit di-refactor tanpa component model
- Astro.js menawarkan zero-JS-by-default + island hydration — cocok untuk page yang 70% konten statis, 30% interaktif
- Design spec asli (`design-kronik-pantai-barat-1600-1690.md`) memang ditulis untuk Astro.js

**Yang TIDAK berubah:**
- Backend FastAPI (`/api/research/linimasa`) — tetap
- Database PostgreSQL + Redis cache — tetap
- Data pipeline (`seed_linimasa_events.py`, CSV) — tetap
- Nginx reverse proxy — tetap (arah ke Astro build output, bukan Django)

---

## 2. Current State Analysis

### 2.1 Arsitektur Sekarang

```
Browser → Nginx:8084 → Django:8001 (SSR view)
                          ↓ httpx.get()
                       FastAPI:8000 → Redis → PostgreSQL
```

### 2.2 Komponen Linimasa (1.217 baris)

| Layer | Baris | Fungsi |
|-------|-------|--------|
| CSS | 534 | Design tokens, hero, chronicle 3-col, maritime stage, scrubber, animations |
| HTML (template) | 249 | Hero, era sections, event cards (SSR), chronicle skeleton, footer |
| JavaScript | 412 | Chronicle controller, SVG axis, scrubber, port map, view toggle, reveal |
| **Django view** | 40 | `linimasa()` — fetch API, group by era, render template |

### 2.3 Data Flow Sekarang

1. Django view memanggil `GET /api/research/linimasa` (httpx, server-side)
2. Response di-group oleh `era_slug` ke 5 era editorial (`LINIMASA_ERAS`)
3. Template merender: hero (static), event cards (SSR `{% for %}`), chronicle skeleton (JS-built)
4. Inline JSON `#linimasa-data` + `#era-meta` dikonsumsi oleh client-side JS
5. JS membangun: SVG axis, scrubber, port map, panel renderer, navigation

### 2.4 Masalah Aktual

| Masalah | Dampak |
|---------|--------|
| Template tunggal 1.217 baris | Sulit navigasi, mudah typo, merge conflict |
| CSS 534 baris tanpa scoping | Style leak antar section |
| JS 412 baris tanpa module boundary | State management global, sulit test |
| Django view + template coupling | Perubahan UI harus touching Python + HTML + JS |
| Tidak ada type safety | JS runtime errors, tidak ada TypeScript |
| Tidak ada component reuse | Chronicle controller tidak bisa dipakai di page lain |

---

## 3. Target State: Astro.js Architecture

### 3.1 Arsitektur Target

```
                    BUILD TIME
FastAPI:8000 ──→ Astro SSG ──→ Static HTML/JS/CSS
                                      ↓
                    RUNTIME
Browser → Nginx:8084 → Static Files (CDN/nginx)
                          ↓ (client-side fetch)
                       FastAPI:8000 → Redis → PostgreSQL
```

### 3.2 Perubahan Fundamental

| Aspek | Sekarang (Django) | Target (Astro.js) |
|-------|-------------------|-------------------|
| Render | Server-side (Django view) | Static build + client-side islands |
| Data fetch | Server-side httpx | Build-time fetch + client-side hydration |
| CSS | Global, 534 baris | Scoped per component, zero-JS CSS |
| JS | 412 baris vanilla, semua dikirim | Islands only, zero-JS by default |
| Type safety | None | TypeScript |
| Component model | None (template tunggal) | `.astro` + `.tsx` components |
| Deploy | Docker container + Django runserver | Static files di nginx |

### 3.3 Component Tree

```
src/
├── layouts/
│   └── LinimasaLayout.astro        # HTML shell, meta, fonts
├── pages/
│   └── linimasa.astro              # Route: /linimasa/
├── components/
│   ├── linimasa/
│   │   ├── HeroSection.astro       # Static hero (zero JS)
│   │   ├── EraNav.astro            # Sidebar era navigation
│   │   ├── EventCard.astro         # SSR event card (details/summary)
│   │   ├── ChronicleStage.astro    # Maritime map + ports (Preact island)
│   │   ├── ChronicleController.tsx # State management (Preact island)
│   │   ├── Scrubber.tsx            # Timeline scrubber (Preact island)
│   │   ├── EventPanel.tsx          # Active event panel (Preact island)
│   │   ├── SVGAxis.tsx             # Timeline axis (Preact island)
│   │   ├── PortMap.tsx             # Port dots + routes (Preact island)
│   │   ├── ViewToggle.astro        # Toggle chronicle/list (vanilla JS)
│   │   └── TypeFilter.astro        # Event type filter (vanilla JS)
│   └── shared/
│       ├── SourceDetails.astro     # Expandable source provenance
│       └── ConfidenceBadge.astro   # Unverified/verified badge
├── data/
│   └── eras.ts                     # LINIMASA_ERAS editorial copy
├── styles/
│   ├── tokens.css                  # Design tokens (CSS custom properties)
│   ├── global.css                  # Reset, typography, base
│   └── linimasa.css                # Page-specific styles (scoped)
└── lib/
    ├── api.ts                      # FastAPI client (fetch + types)
    └── types.ts                    # LinimasaEvent, Era, Meta types
```

### 3.4 Data Fetching Strategy

```typescript
// src/pages/linimasa.astro
---
// Build-time: fetch all events from FastAPI
const res = await fetch(`${import.meta.env.API_BASE_URL}/api/research/linimasa`);
const { items, meta } = await res.json();

// Group by era (same logic as current Django view)
import { ERAS } from '../data/eras';
const eras = ERAS.map(era => ({
  ...era,
  events: items.filter(e => e.era_slug === era.slug)
}));
---

<!-- Static HTML: hero, era sections, event cards -->
<HeroSection />
{eras.map(era => (
  <EraSection era={era}>
    {era.events.map(ev => <EventCard event={ev} />)}
  </EraSection>
))}

<!-- Client-side islands: chronicle interactive -->
<ChronicleStage client:load items={items} eras={eras} meta={meta} />
```

**Build-time fetch:** Astro memanggil FastAPI saat `astro build`. Data di-embed sebagai JSON statis.
**Client-side fetch:** Filter/search memanggil API langsung dari browser (untuk interaktif real-time).
**Fallback:** Jika build-time fetch gagal, page tetap render dengan data kosong + error state.

---

## 4. Migration Scope

### 4.1 Phase 1: Foundation (Sprint 1 — 1 minggu)

**Goal:** Astro project setup, build pipeline, 1 halaman statis

| Task | Estimasi | Owner |
|------|----------|-------|
| Init Astro project di `frontend/astro-linimasa/` | 2h | DevSecOps |
| Setup TypeScript, Tailwind CSS (atau vanilla CSS) | 2h | DevSecOps |
| Migrate design tokens ke `tokens.css` | 2h | QA (visual review) |
| Build `LinimasaLayout.astro` + `HeroSection.astro` | 4h | DevSecOps |
| Build `EventCard.astro` (SSR, static) | 4h | DevSecOps |
| Build `EraNav.astro` (sidebar, static) | 2h | DevSecOps |
| Connect FastAPI di build-time (`lib/api.ts`) | 3h | DevSecOps |
| Docker: tambah service `astro-linimasa` | 2h | DevSecOps |
| Nginx: route `/linimasa/` ke Astro static | 1h | DevSecOps |
| **QA:** Visual comparison Django vs Astro (list view) | 4h | QA |
| **QA:** Accessibility audit (WCAG 2.1 AA) | 3h | QA |
| **DBA:** Verify API response shape unchanged | 2h | DBA |

**Deliverable:** `/linimasa/` bisa diakses via Astro static, list view identik dengan Django

### 4.2 Phase 2: Interactive Islands (Sprint 2 — 1 minggu)

**Goal:** Chronicle 3-column view berjalan di Astro

| Task | Estimasi | Owner |
|------|----------|-------|
| Build `ChronicleController.tsx` (state management) | 8h | DevSecOps |
| Build `PortMap.tsx` (port dots + routes) | 6h | DevSecOps |
| Build `SVGAxis.tsx` (timeline axis) | 4h | DevSecOps |
| Build `Scrubber.tsx` (year scrubber) | 4h | DevSecOps |
| Build `EventPanel.tsx` (active event panel) | 4h | DevSecOps |
| Build `ChronicleStage.astro` (layout wrapper) | 2h | DevSecOps |
| Type definitions (`types.ts`) | 2h | DevSecOps |
| **QA:** Chronicle interaction testing | 6h | QA |
| **QA:** Responsive testing (980px, 640px breakpoints) | 4h | QA |
| **DBA:** Verify API latency < 200ms p95 | 2h | DBA |

**Deliverable:** Chronicle 3-column view berjalan penuh di Astro, semua interaktif berfungsi

### 4.3 Phase 3: Polish & Parity (Sprint 3 — 3 hari)

**Goal:** Feature parity 100%, zero regression

| Task | Estimasi | Owner |
|------|----------|-------|
| Animations: hero fog, ink-in, scroll reveal | 4h | DevSecOps |
| View toggle (chronicle ↔ list) | 2h | DevSecOps |
| Type filter (client-side) | 2h | DevSecOps |
| Keyboard navigation (arrow keys) | 2h | DevSecOps |
| Print styles | 1h | DevSecOps |
| Error state + backend_error handling | 2h | DevSecOps |
| SEO: meta tags, structured data, sitemap | 2h | DevSecOps |
| **QA:** Full regression test (semua fitur) | 8h | QA |
| **QA:** Cross-browser testing (Chrome, Firefox, Safari) | 4h | QA |
| **QA:** Performance audit (Lighthouse, Core Web Vitals) | 3h | QA |
| **Security:** CSP headers untuk Astro static | 2h | DevSecOps |
| **DBA:** Seed data integrity check | 2h | DBA |

**Deliverable:** 100% feature parity, semua test pass, performance ≥ Django

### 4.4 Phase 4: Cutover & Cleanup (Sprint 4 — 2 hari)

**Goal:** Django frontend dihapus, Astro jadi satu-satunya

| Task | Estimasi | Owner |
|------|----------|-------|
| Nginx: `/linimasa/` → Astro static (bukan Django) | 1h | DevSecOps |
| Hapus `linimasa.html` dari Django templates | 1h | DevSecOps |
| Hapus `linimasa()` view dari `views.py` | 1h | DevSecOps |
| Hapus `LINIMASA_ERAS` dari `views.py` → pindah ke `data/eras.ts` | 1h | DevSecOps |
| Cleanup Django static assets (linimasa images) | 1h | DevSecOps |
| Update `docker-compose.yml` (hapus frontend depend jika tidak dipakai) | 1h | DevSecOps |
| **QA:** Final smoke test di production | 2h | QA |
| **Security:** Full security re-audit | 3h | DevSecOps |
| **DBA:** Verify no data loss, API unchanged | 2h | DBA |
| Documentation update | 2h | DevSecOps |

**Deliverable:** Django tidak lagi melayani `/linimasa/`, Astro adalah satu-satunya frontend

---

## 5. Team Structure

### 5.1 DevSecOps (1 orang)

**Role:** Full-stack developer + infrastructure + security

**Responsibilities:**
- Astro component development (TypeScript/React islands)
- Build pipeline setup (Astro SSG)
- Docker containerization
- Nginx configuration
- CI/CD pipeline
- Security hardening (CSP, headers, input validation)
- Deployment ke production

**Skills required:**
- Astro.js, React, TypeScript
- Docker, Nginx
- Linux server administration
- Basic security (OWASP, CSP)

**Sprint allocation:**
- Sprint 1: 80% setup + foundation
- Sprint 2: 90% interactive islands
- Sprint 3: 60% polish + security
- Sprint 4: 50% cutover + cleanup

### 5.2 DBA (1 orang, part-time)

**Role:** Database administrator + data integrity

**Responsibilities:**
- Verify API response shape unchanged setelah migrasi
- Monitor query performance (p95 < 200ms)
- Seed data integrity check
- Redis cache behavior verification
- Alembic migration review (jika ada schema change)

**Skills required:**
- PostgreSQL, PostGIS
- Redis
- SQLAlchemy
- Data validation

**Sprint allocation:**
- Sprint 1: 20% (API verification)
- Sprint 2: 20% (latency check)
- Sprint 3: 20% (integrity check)
- Sprint 4: 20% (final verification)

### 5.3 QA (1 orang)

**Role:** Quality assurance + visual testing

**Responsibilities:**
- Visual comparison (Django vs Astro)
- Responsive testing (desktop, tablet, mobile)
- Cross-browser testing (Chrome, Firefox, Safari)
- Accessibility audit (WCAG 2.1 AA)
- Performance audit (Lighthouse ≥ 90)
- Regression testing (semua fitur)
- Print styles verification

**Skills required:**
- Manual testing
- Browser DevTools
- Lighthouse
- axe-core (accessibility)
- Visual regression testing

**Sprint allocation:**
- Sprint 1: 40% (visual comparison + a11y)
- Sprint 2: 50% (interaction testing)
- Sprint 3: 80% (full regression + performance)
- Sprint 4: 60% (smoke test + final audit)

---

## 6. Workflow

### 6.1 Sprint cadence

```
Sprint 1 (Minggu 1):  Foundation    → List view statis berjalan
Sprint 2 (Minggu 2):  Islands       → Chronicle interaktif berjalan
Sprint 3 (Rabu-Jumat): Polish       → Feature parity 100%
Sprint 4 (Senin-Selasa): Cutover    → Django dihapus, Astro production
```

### 6.2 Definition of Done

| Criteria | Verification |
|----------|-------------|
| `/linimasa/` mengembalikan HTTP 200 | `curl -sI` |
| Semua event cards render dengan benar | Visual comparison |
| Chronicle view interaktif (scrubber, panel, navigation) | Manual testing |
| View toggle berfungsi | Manual testing |
| Type filter berfungsi | Manual testing |
| Responsive di 980px dan 640px | Browser resize |
| Lighthouse Performance ≥ 90 | Lighthouse audit |
| WCAG 2.1 AA compliant | axe-core audit |
| Zero JS errors di console | Browser DevTools |
| API response unchanged | DBA verification |
| Security headers present | `curl -sI` |

### 6.3 Branch strategy

```
main (production)
  └── feat/astro-linimasa (long-running branch)
       ├── sprint-1-foundation
       ├── sprint-2-islands
       ├── sprint-3-polish
       └── sprint-4-cutover
```

### 6.4 Review process

- **DevSecOps → QA:** Setiap sprint deliverable di-review oleh QA sebelum merge
- **DevSecOps → DBA:** API changes di-review oleh DBA sebelum deploy
- **QA → DevSecOps:** Bug report via GitHub Issues
- **DBA → DevSecOps:** Performance report via Slack/notifikasi

---

## 7. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Build-time fetch gagal (API down saat build) | Medium | High | Fallback: data kosong + error state; retry 3x |
| Chronicle JS behavior regression | High | High | Visual regression test; screenshot comparison |
| Performance degradation (Astro static vs Django SSR) | Low | Medium | Lighthouse audit; CDN caching |
| Data shape mismatch (API → Astro) | Low | High | TypeScript types + DBA verification |
| Merge conflict dengan Django template | Medium | Low | Feature branch; isolate Astro di folder terpisah |
| Team member unavailable | Medium | Medium | Cross-training; documentation |

---

## 8. Rollback Plan

Jika migrasi gagal atau regression parah:

1. **Nginx:** Route `/linimasa/` kembali ke Django frontend
2. **Django:** `linimasa.html` dan `views.py` masih di `main` branch (tidak dihapus sampai Phase 4)
3. **Timeline:** Rollback bisa dilakukan dalam 5 menit (1 nginx config change + reload)

**Trigger rollback:**
- Lighthouse Performance < 70
- Feature regression (fitur berhenti berfungsi)
- Security vulnerability ditemukan
- User acceptance test gagal

---

## 9. Success Metrics

| Metric | Current (Django) | Target (Astro) |
|--------|-----------------|----------------|
| Lighthouse Performance | ~75 (est.) | ≥ 90 |
| First Contentful Paint | ~1.2s (est.) | < 0.8s |
| Total Blocking Time | ~200ms (est.) | < 100ms |
| Cumulative Layout Shift | ~0.05 (est.) | < 0.1 |
| JavaScript bundle size | ~15KB (all) | < 8KB (islands only) |
| Time to Interactive | ~2s (est.) | < 1.5s |
| Test coverage | 0% (no frontend tests) | ≥ 80% (component tests) |
| Build time | N/A (Django runserver) | < 30s (static build) |

---

## 10. Keputusan yang Sudah Diambil

| Pertanyaan | Keputusan | Alasan |
|-----------|-----------|--------|
| CSS strategy | **Tailwind CSS** | Scoped per component, zero global leak, responsive prefix rapi untuk chronicle breakpoints |
| Framework islands | **Preact** | 3KB vs 40KB (React), API identik, Astro integration built-in |
| Vanilla JS untuk | View toggle, header scroll state | Terlalu sederhana untuk butuh framework |

## 11. Open Questions

1. **Deploy target:** Static files di nginx yang sama, atau CDN terpisah (Cloudflare Pages, Vercel)?
2. **Django frontend lainnya:** Apakah `/riset/atjeh-dagang/`, `/riset/tema/`, `/riset/jaringan/` juga akan dimigrasi? Atau hanya linimasa?
3. **Editorial admin:** Apakah perlu CMS/admin interface untuk mengelola `LINIMASA_ERAS` (headlines, summaries)? Saat ini hardcoded di TypeScript.

---

## Appendix A: File Mapping (Django → Astro)

| Django File | Astro Equivalent | Notes |
|-------------|-----------------|-------|
| `templates/map_app/linimasa.html` | `pages/linimasa.astro` + 12 components | Split by concern |
| `views.py:linimasa()` | `pages/linimasa.astro` (build-time fetch) | Python → TypeScript |
| `views.py:LINIMASA_ERAS` | `data/eras.ts` | Same data, TypeScript |
| Static CSS (in template) | `styles/tokens.css` + component CSS | Scoped |
| Static JS (in template) | `components/*.tsx` (React islands) | Component-based |
| `static/map_app/img/*` | `public/img/*` | Same images |

## Appendix B: Current Test Coverage

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_linimasa_events.py` | 36 | CSV integrity, seed validation |
| `test_research_linimasa.py` | 6 | API endpoint (mock DB) |
| **Total** | **42** | Backend API + data only |

**Gap:** Zero frontend tests. Migrasi ke Astro.js membuka peluang untuk component testing (Vitest + Testing Library).

## Appendix C: Estimated Total Effort

| Phase | Duration | Effort (person-hours) |
|-------|----------|----------------------|
| Sprint 1: Foundation | 1 minggu | ~30h |
| Sprint 2: Islands | 1 minggu | ~36h |
| Sprint 3: Polish | 3 hari | ~30h |
| Sprint 4: Cutover | 2 hari | ~15h |
| **Total** | **~3.5 minggu** | **~111h** |

Dengan 1 DevSecOps full-time + 1 QA part-time + 1 DBA part-time, estimasi selesai dalam **3-4 minggu**.
