# Current Design — Linimasa Kronik Pantai Barat

**Status:** Live at `localhost:8084/linimasa`  
**Stack:** Django templates + inline CSS + vanilla JS  
**File:** `frontend/map_app/templates/map_app/linimasa.html` (1195 lines)

---

## 1. Design Tokens

```css
:root{
  /* Paper & Background */
  --paper:#f5f0e6; --paper-deep:#e8dfcf; --panel:#faf6ec; --panel-2:#e8dfcf;
  
  /* Text */
  --ink:#181611; --muted:#716b61; --muted-dark:#4d4638;
  
  /* Borders & Lines */
  --line:#d4c8b5; --border:#d4c8b5;
  
  /* Accent — DARK TEAL (replaced gold) */
  --accent:#29484b; --archive-gold:#29484b; --aceh-gold:#3a6366;
  --sea-ink:#29484b; --gold-ink:#1d3537;
  
  /* Routes */
  --route-aceh:#5a8a8d; --route-voc:#a04a35; --route-local:#29484b;
  --voc-copper:#8b4b33; --admin-umber:#6b5842;
  
  /* Nodes */
  --node-active:#f3ead9; --node-related:#f3ead9; --node-dormant:rgba(243,234,217,.25);
  
  /* Event Types */
  --evt-suksesi:var(--archive-gold); --evt-perjanjian:var(--sea-ink);
  --evt-konflik:var(--voc-copper); --evt-diplomasi:var(--aceh-gold);
  --evt-administratif:var(--admin-umber);
  
  /* Typography */
  --serif:"Cormorant Garamond",Georgia,"Times New Roman",serif;
  --sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:"IBM Plex Sans",ui-monospace,Menlo,Consolas,monospace;
}
```

---

## 2. Typography

| Element | Font | Weight | Size | Color |
|---------|------|--------|------|-------|
| Hero Title | Cormorant Garamond | 600 | clamp(2.3rem, 5.6vw, 4rem) | #f3ead9 |
| Hero Lede | Cormorant Garamond | 400 | clamp(1.02rem, 1.8vw, 1.2rem) | #efe8da |
| Era Label | Cormorant Garamond | 600 | 1.5rem | #181611 |
| Event Title | Cormorant Garamond | 600 | 1.05rem | #181611 |
| Panel Year | IBM Plex Sans | 600 | 2.4rem | #f3ead9 |
| Panel Quote | Cormorant Garamond | 400 italic | 0.94rem | #f3ead9 |
| Badge/Label | IBM Plex Sans | 600 | 0.68rem | uppercase, tracking 0.16em |
| Navigation | IBM Plex Sans | 400 | 0.82rem | #181611 |

---

## 3. Color Palette — Current State

```
Paper tones:    #f5f0e6 (base) → #e8dfcf (deep) → #faf6ec (panel)
Ink tones:      #181611 (primary) → #716b61 (muted) → #4d4638 (dark muted)
Accent:         #29484b (dark teal — PRIMARY ACCENT)
Secondary:      #3a6366 (lighter teal)
Routes:         #5a8a8d (Aceh orbit) → #a04a35 (VOC copper) → #29484b (local)
Nodes:          #f3ead9 (active/related) → rgba(243,234,217,.25) (dormant)
Borders:        #d4c8b5
```

**Key:** Gold/yellow has been COMPLETELY REMOVED. All accents are now teal-based.

---

## 4. Layout Structure

### Hero Section (Full-bleed, 100dvh)
```
┌──────────────────────────────────────────────────────┐
│ NAV BAR (transparent, z-index:3)                     │
│ Brand: "Salido" | Links: Kronik, Peta, Peristiwa...  │
├──────────────────────────────────────────────────────┤
│                                                      │
│ HERO CONTENT (bottom-left, z-index:2)                │
│ ┌────────────────────────────────────────┐           │
│ │ KRONIK PANTAI BARAT SUMATRA            │           │
│ │ 1600—1775                              │           │
│ │                                        │           │
│ │ Pusaran Kuasa,                         │           │
│ │ Arus yang Berbalik                     │           │
│ │                                        │           │
│ │ [MULAI MENELUSURI]  [BUKA PETA]        │           │
│ │                                        │           │
│ │ ↓ Gulir ke kronik                      │           │
│ └────────────────────────────────────────┘           │
│                                                      │
│ Background: linimasa-hero.jpg (cover, center 42%)    │
│ Scrim: multi-gradient overlay (left-heavy)           │
└──────────────────────────────────────────────────────┘
```

### Chronicle Stage (3-Column Grid)
```
┌─────────────┬────────────────────────────┬───────────────┐
│ SIDEBAR     │ MARITIME STAGE             │ EVENT PANEL   │
│ (19%)       │ (52%)                      │ (29%)         │
│             │                            │               │
│ ERA NAV     │ ┌────────────────────────┐ │ EVENT DETAIL  │
│ sticky      │ │ Historical Map Image   │ │ counter       │
│             │ │ (AMH-5147-NA.jpg)      │ │ year          │
│ ○ 1600-1607 │ │                        │ │ divider       │
│   Laut      │ │  [Port dots overlay]   │ │ title         │
│   Sebelum   │ │  - Aceh (active)       │ │ subtitle      │
│   Pusaran   │ │  - Barus               │ │ meta          │
│             │ │  - Singkil             │ │ quote         │
│ ● 1607-1636 │ │  - Nias               │ │ notes         │
│   Pusaran   │ │  - ...14 ports total   │ │ source        │
│   Menguat   │ │                        │ │ status        │
│             │ └────────────────────────┘ │ [transcript]  │
│ ○ 1636-1641 │ Legend:                    │ [peta →]      │
│   ...       │ ● Aceh ● Pelabuhan        │               │
│             │ --- Orbit --- Jalur VOC    │               │
│             │                            │               │
│             │ ────── Scrubber ────────── │               │
│             │ 1600 ─ ● ─ 1750 ─ 1775    │               │
│             │ ◀  42/101  ▶               │               │
└─────────────┴────────────────────────────┴───────────────┘
```

---

## 5. Key CSS Classes

### Hero
```css
.hero — position:relative, min-height:100dvh, flex column
.hero .bg — position:absolute, object-fit:cover, object-position:center 42%
.hero .scrim — position:absolute, multi-gradient overlay
.hero-nav — position:relative, z-index:3, flex, space-between
.hero-content — position:relative, z-index:2, max-width:760px, margin-top:auto
```

### Chronicle Grid
```css
.js .chronicle — display:grid, grid-template-columns:minmax(200px,19%) 1fr minmax(300px,29%)
  width:100vw, margin:18px calc(50% - 50vw) 30px
  border-top/bottom:1px solid var(--line)
  background:var(--panel), min-height:100dvh
```

### Sidebar Navigation
```css
.chr-nav — counter-reset:cera, background:var(--paper-deep), border-right:1px
  flex column, overflow-y:auto
.chr-era — position:relative, block, text-align:left, border-left:2px solid transparent
.chr-era.active — border-left-color:var(--accent), background:rgba(41,72,75,.06)
```

### Maritime Stage
```css
.chr-stage — position:relative, flex column
.chr-eratag — position:absolute, top:14px, left:14px, z-index:2
  pointer-events:none, border:1px solid rgba(90,138,141,.55)
#chrMapWrap — position:relative, aspect-ratio:3/2, background:#1a1a1a
#chrMap — width:100%, object-fit:cover, opacity:0.85, filter:sepia(15%)
#chrMapOverlay — position:absolute, inset:0, pointer-events:none
```

### Port Dots
```css
.chr-port — position:absolute, cursor:pointer, z-index:2, pointer-events:auto
.chr-port .core — border-radius:50%, background:#f3ead9, border:2px solid #29484b
.chr-port .lbl — position:absolute, font:600 10.5px var(--sans), color:#cfc4ab
.chr-port.active .core — width:13px, height:13px, border-color:#29484b
.chr-port.dormant .core — opacity:0.25, width:6px, height:6px
```

### Event Panel
```css
.chr-panel — aside, overflow-y:auto
  padding, background, border-left:1px solid var(--line)
.chr-year — font-family:var(--mono), font-weight:600, font-size:2.4rem, color:#f3ead9
.chr-title — font-family:var(--serif), font-weight:600, font-size:1.35rem
.chr-quote — border-left:3px solid var(--accent), background:var(--paper)
```

### Scrubber
```css
.chr-scrub — flex, align-items:center, gap, padding
.chr-lane — position:relative, flex:1, height:32px
.chr-dot — position:absolute, width:8px, height:8px, border-radius:50%
  background:var(--muted), top:50%, transform:translateY(-50%)
.chr-dot.active — background:var(--accent), width:10px, height:10px
```

---

## 6. Motion System

```css
/* Hero fog: scale 1.06 → 1 */
.js-anim .hero .bg { animation: heroFog 2.8s ease-out both }

/* Ink reveal: fade + blur + translateY */
.js-anim .hero-eyebrow, .hero-title, .hero-lede, .hero-actions, .hero-scroll {
  opacity: 0; animation: inkIn .9s ease-out forwards
}

/* Scroll drift: translateY 0 → 4px */
.js-anim .hero-scroll svg { animation: tideDrift 2.2s ease-in-out infinite alternate }

/* Entry reveal: opacity 0 + blur 5px + translateY 20px */
.js-anim .reveal, details.card {
  opacity: 0; filter: blur(5px); transform: translateY(20px);
  transition: opacity .7s ease, filter .7s ease, transform .7s ease
}
```

---

## 7. Event Types & Colors

| Type | Badge Color | CSS Variable |
|------|-------------|--------------|
| Suksesi | #29484b (teal) | --evt-suksesi |
| Perjanjian | #29484b (teal) | --evt-perjanjian |
| Konflik | #8b4b33 (copper) | --evt-konflik |
| Diplomasi | #3a6366 (lighter teal) | --evt-diplomasi |
| Administratif | #6b5842 (umber) | --evt-administratif |

---

## 8. Responsive Breakpoints

```css
/* Mobile: stack columns */
@media(max-width:640px) {
  .hero { min-height: 100svh }
  .hero .bg { object-position: 34% center }
  .hero-nav .nav-l .sib { display: none }
}

/* Tablet: reduce sidebar */
@media(max-width:900px) {
  .chr-nav { min-width: 168px; padding: 8px 8px 8px 22px }
  .chr-era .sum { display: none !important }
}
```

---

## 9. Accessibility

- Keyboard navigation: ArrowLeft/ArrowRight for scrubber
- `aria-label` on all interactive elements
- `aria-pressed` on toggle buttons
- `aria-live="polite"` on event panel
- `prefers-reduced-motion` respected (no animations)
- Content readable without JavaScript (card list fallback)

---

## 10. Original Design Spec Reference

**Source:** `docs/ui-ux-mockup-kronik-pantai-barat.md`

**Original Intent:**
- "Pengguna tidak menggulir daftar tahun. Pengguna mengikuti arus sejarah."
- Maritime stage should feel like "pelayaran mengikuti perubahan kekuasaan"
- Ships, waves, forts, maps as narrative stage
- 1663 as climax moment (Traktat Painan)

**What Was Implemented:**
- ✅ Hero cinematic section (ships, waves, fort)
- ✅ 3-column chronicle grid (era nav | maritime stage | event panel)
- ✅ Port dots with active/dormant states
- ✅ Scrubber timeline
- ✅ Keyboard navigation
- ✅ Responsive design
- ⚠️ Ships removed (replaced with historical map image)
- ⚠️ Waves/ripples removed (simplified)
- ⚠️ Color palette shifted from gold to teal

**What Was NOT Implemented (by design):**
- SVG orbit lines (replaced by port dot states)
- Ship animations (simplified for performance)
- Complex wave effects (simplified)
- Red wax seal for 1663 climax (simplified to panel highlight)

---

## 11. Known Issues / AI Slop Audit

**Source:** `docs/audit/audit-ux-ui-ai-slop-salido.md`

**Addressed:**
- ✅ P0.2: Ship opacity reduced
- ✅ P0.3: Panel editorial format
- ✅ P0.4: Panel editorial rules
- ✅ P0.5: Compass, rhumb, landname hidden
- ✅ P1.1: 6 new CSS variables
- ✅ P1.2: Port 3-state system
- ✅ P1.3: Year font updated
- ✅ P1.5: Legend hidden
- ✅ P1.6: Layer dimming
- ✅ P1.7: Responsive reading mode

**Remaining:**
- ⚠️ Fonts changed (Cormorant Garamond + IBM Plex Sans)
- ⚠️ Colors changed (dark teal replaces gold)
- ⚠️ SVG map replaced with historical image

---

## 12. File Locations

| File | Purpose |
|------|---------|
| `frontend/map_app/templates/map_app/linimasa.html` | Main template (1195 lines) |
| `frontend/map_app/static/map_app/img/amh-5147-na.jpg` | Historical map (125KB) |
| `frontend/map_app/static/map_app/img/linimasa-hero.jpg` | Hero background |
| `frontend/map_app/static/map_app/img/treaty-panel.jpg` | Treaty highlight |
| `docs/ui-ux-mockup-kronik-pantai-barat.md` | Original design spec |
| `docs/audit/audit-ux-ui-ai-slop-salido.md` | AI slop audit |
| `docs/prd/prd-redesign-kronik-anti-slop.md` | Redesign PRD |

---

**Questions for Claude:**
1. Is the dark teal accent (`#29484b`) appropriate for historical/archival content?
2. Does Cormorant Garamond work better than EB Garamond for this use case?
3. Is the historical map image (AMH-5147-NA) effectively replacing the SVG visualization?
4. Are there any "AI slop" patterns remaining in the current design?
5. What improvements would make this feel more "editorial" and less "dashboard"?
