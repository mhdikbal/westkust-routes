# Plan Perbaikan Linimasa Kronik — Post UI/UX Review

**Berdasarkan:** `docs/ui-ux-mockup-kronik-pantai-barat.md` + UI/UX Senior Review  
**Target:** Tingkatkan skor dari 5.5/7 → 7/7  
**File utama:** `frontend/map_app/templates/map_app/linimasa.html` (1195 lines)

---

## Status Saat Ini

| Kategori | Skor | Gap |
|----------|------|-----|
| Hero | ✅ 90% | Title size kecil |
| 3-Kolom Layout | ✅ 95% | — |
| Maritime Stage | ⚠️ 44% | 6/9 elemen hilang |
| Panel Peristiwa | ✅ 100% | — |
| Klimaks 1663 | ⚠️ 50% | Transisi tidak ada |
| Motion System | ✅ 100% | — |
| Accessibility | ✅ 100% | — |

---

## P0 — Harus Diperbaiki (Critical)

### P0.1: Hero Title Size
**Masalah:** `clamp(2.3rem, 5.6vw, 4rem)` = maks 64px, spec 78-104px  
**Impact:** Hero kurang powerful, text terlalu kecil di desktop besar

**CSS Change:**
```css
/* FROM */
.hero-title{font-size:clamp(2.3rem,5.6vw,4rem)}

/* TO */
.hero-title{font-size:clamp(2.3rem,6.5vw,4.8rem)}
```

**Effort:** 1 line CSS  
**Risk:** Minimal — hanya ukuran

---

### P0.2: --wax-red Token
**Masalah:** Token `--wax-red: #8f241c` hilang, dibutuhkan untuk cap merah 1663  
**Impact:** Klimaks 1663 kehilangan elemen visual penting

**CSS Change:**
```css
/* Add to :root */
--wax-red:#8f241c;
```

**Effort:** 1 line CSS  
**Risk:** Minimal

---

### P0.3: Era Progress Line
**Masalah:** Sidebar tidak ada "garis vertikal terisi mengikuti progres"  
**Impact:** User tidak melihat progress visual melalui era

**CSS Change:**
```css
.chr-nav{position:relative}
.chr-nav::after{content:"";position:absolute;left:18px;top:48px;bottom:20px;width:2px;
  background:var(--line);z-index:0}
.chr-nav::before{content:"";position:absolute;left:18px;top:48px;width:2px;
  background:var(--accent);z-index:1;transition:height .4s ease;height:0}
```

**JS Change:**
```javascript
// In setActive(), update progress line height
const navEl = document.getElementById('chrNav');
const eraIndex = ERAS_META.findIndex(e => e.slug === ev.era_slug);
const eraHeight = navEl.scrollHeight / ERAS_META.length;
navEl.style.setProperty('--era-progress', `${(eraIndex + 1) * eraHeight}px`);
```

**Effort:** ~10 lines CSS + JS  
**Risk:** Low — visual enhancement only

---

## P1 — Sebaiknya Diperbaiki (Important)

### P1.1: Maritime Route Lines
**Masalah:** Maritime stage kehilangan "network feel" — tidak ada garis rute  
**Impact:** Peta terasa statis, tidak ada hubungan visual antar port

**Approach:**
Tambahkan SVG tipis di overlay yang menghubungkan port aktif ke Aceh (orbit) dan VOC routes (copper).

**CSS:**
```css
.route-line{position:absolute;pointer-events:none;z-index:1;
  stroke-dasharray:4 6;stroke-width:1.2;opacity:.6;transition:opacity .5s ease}
.route-orbit{stroke:var(--route-aceh)}
.route-voc{stroke:var(--route-voc)}
.route-active{opacity:.9;stroke-dasharray:none;stroke-width:1.8}
```

**JS:**
```javascript
// Draw route lines between ports using Canvas or SVG overlay
function drawRoute(from, to, type) {
  const fromPos = PORT_PCT[from];
  const toPos = PORT_PCT[to];
  // Create SVG line element
  // Append to chrMapOverlay
}
```

**Effort:** ~40 lines  
**Risk:** Medium — harus careful dengan z-index dan pointer-events

---

### P1.2: Header Scroll State
**Masalah:** Header tidak shrink/blur saat scroll  
**Impact:** Polish feel berkurang

**CSS:**
```css
.hero-nav{transition:background .3s ease,padding .3s ease}
.hero-nav.scrolled{background:rgba(8,23,25,.85);backdrop-filter:blur(8px);
  padding:12px clamp(16px,4vw,44px)}
```

**JS:**
```javascript
const heroNav = document.querySelector('.hero-nav');
const io = new IntersectionObserver(([e]) => {
  heroNav.classList.toggle('scrolled', !e.isIntersecting);
}, {threshold: 0.1});
io.observe(document.querySelector('.hero'));
```

**Effort:** ~15 lines  
**Risk:** Low

---

### P1.3: Port Active Glow
**Masalah:** Port aktif tidak ada glow effect (ripple dihapus)  
**Impact:** Port aktif kurang prominent

**CSS:**
```css
.chr-port.active .core{box-shadow:0 0 12px 3px rgba(243,234,217,.4);
  animation:portGlow 2s ease-in-out infinite alternate}
@keyframes portGlow{from{box-shadow:0 0 8px 2px rgba(243,234,217,.3)}
  to{box-shadow:0 0 16px 4px rgba(243,234,217,.5)}}
```

**Effort:** ~8 lines CSS  
**Risk:** Minimal

---

### P1.4: Klimaks 1663 Transition
**Masalah:** Tidak ada visual change saat user mencapai event 1663  
**Impact:** Climax moment kurang dramatic

**Approach:**
Saat `ev.title` mengandung "Traktat Painan":
1. Brighten map image (opacity ↑)
2. Add wax-red accent ke panel
3. Smooth transition 700ms

**CSS:**
```css
.chr-stage.climax::before{opacity:1 !important;filter:brightness(1.1)}
.chr-panel.climax{border-left:3px solid var(--wax-red)}
```

**JS:**
```javascript
// In setActive()
const isClimax = ev.title?.includes('Traktat Painan');
chrStage.classList.toggle('climax', isClimax);
panel.classList.toggle('climax', isClimax);
```

**Effort:** ~12 lines  
**Risk:** Low

---

## P2 — Nice to Have (Enhancement)

### P2.1: Source Details Collapsed
**Masalah:** Panel terlalu banyak info sekaligus  
**Impact:** Cognitive load tinggi

**Approach:**
Source details (arsip, halaman, confidence) default collapsed, expand on click.

**Effort:** ~25 lines  
**Risk:** Low

---

### P2.2: Keyboard Shortcut Hints
**Masalah:** User tidak tahu bisa pakai keyboard  
**Impact:** Discoverability

**Approach:**
Tooltip kecil di scrubber: "← → untuk navigate"

**Effort:** ~10 lines  
**Risk:** Minimal

---

### P2.3: Print Styles
**Masalah:** Tidak ada print optimization  
**Impact:** User yang ingin print kronik

**Approach:**
`@media print` — hide navigation, show all events expanded

**Effort:** ~30 lines  
**Risk:** Minimal

---

## Implementation Order

```
Phase 1 (Quick Wins — 30 menit):
├── P0.1: Hero title size (1 line)
├── P0.2: --wax-red token (1 line)
├── P0.3: Era progress line (10 lines)
└── P1.3: Port active glow (8 lines)

Phase 2 (Core Polish — 1 jam):
├── P1.2: Header scroll state (15 lines)
├── P1.4: Klimaks 1663 transition (12 lines)
└── P1.1: Maritime route lines (40 lines)

Phase 3 (Nice to Have — 30 menit):
├── P2.1: Source details collapsed (25 lines)
├── P2.2: Keyboard hints (10 lines)
└── P2.3: Print styles (30 lines)
```

**Total effort:** ~2.5 jam  
**Total lines:** ~190 lines  

---

## Success Metrics

| Metric | Before | After |
|--------|--------|-------|
| UI/UX Score | 5.5/7 | 7/7 |
| Hero title size | 64px max | 77px max |
| Maritime elements | 3/9 | 6/9 |
| Klimaks transition | None | Smooth |
| Header polish | Static | Scroll-aware |

---

## Risk Assessment

| Change | Risk | Mitigation |
|--------|------|------------|
| Hero title size | Low | Test responsive |
| --wax-red | Minimal | — |
| Era progress | Low | CSS only |
| Route lines | Medium | Careful z-index |
| Header scroll | Low | Threshold tuning |
| Klimaks transition | Low | Class toggle |
| Port glow | Minimal | Animation perf |

---

## Files to Modify

1. `frontend/map_app/templates/map_app/linimasa.html`
   - CSS: Lines 20-400 (tokens, hero, chronicle, ports)
   - JS: Lines 864-1195 (setActive, renderPanel)

2. No new files needed — all inline

---

## QA Checklist

- [ ] Hero title visible di 1440px dan 390px
- [ ] Era progress line mengikuti scroll
- [ ] Port glow terlihat di port aktif
- [ ] Header blur saat scroll
- [ ] 1663 transition smooth
- [ ] Route lines tidak block port clicks
- [ ] Print styles functional
- [ ] No JS errors
- [ ] prefers-reduced-motion respected
