# ATLAS PAINAN 1663 — LOCAL RELATIONAL PROTOTYPE AUDIT

> **NONPRODUCTION PROTOTYPE AUDIT — NO ATLAS, API, DATABASE, MIGRATION, GRAPHIFY, COMMIT, PUSH, OR DEPLOYMENT AUTHORIZED OR PERFORMED BY THIS DOCUMENT**
> Executed per `ATLAS_PAINAN_1663_LOCAL_RELATIONAL_RESEARCH_PROTOTYPE_PLAN.md` (repository root). Builds and validates one local, read-only research prototype against the reviewed Painan 1663 relational MVP artifact. No artifact content, prior research finding, or production code was modified.

---

## 1. Scope

This turn builds exactly one isolated, nonproduction local prototype that renders `data/power_relations/painan_1663_relational_research_artifact.json` for researcher visual/semantic review, plus a prototype-specific validator and this audit. It does not repeat artifact construction, does not alter the artifact, does not touch any production Atlas code, API, database, Nginx, Docker, or Graphify integration, and does not stage, commit, push, or deploy anything.

## 2. Frozen Research Inputs

Reused verbatim, not re-derived:

```text
PAINAN_I8A:                       COMPLETE
POWER_THEORY_DEEP_DIVE:           COMPLETE
PATRON_CLIENT_REVIEW:             COMPLETE
GAME_THEORY_REVIEW:               COMPLETE
PAINAN_RELATIONAL_MVP_PLAN:       READY
PAINAN_RELATIONAL_MVP_ARTIFACT:   READY (committed 23da0cc, pushed and server-synced)
ARTIFACT_VALIDATOR:               23/23 PASS (re-verified this turn)
ARTIFACT_SHA256:                  eeeeda8b368e255303c46dc245beb3c1179815d9f960cdff20b1ea59518b4bd7 (re-verified this turn)
PRODUCTION_INTEGRATION:           NOT AUTHORIZED (unchanged)
```

## 3. Artifact Integrity

Checked at the start of this turn, before any prototype file was written:

```text
$ sha256sum data/power_relations/painan_1663_relational_research_artifact.json
eeeeda8b368e255303c46dc245beb3c1179815d9f960cdff20b1ea59518b4bd7  -- MATCH

$ python3 scripts/research_validators/validate_painan_1663_relational_artifact.py
CHECKS PASSED: 23  ERRORS: 0  WARNINGS: 0  VALIDATION RESULT: PASS
```

Both were re-verified again after prototype construction and again after every prototype code edit in this turn (CSS/JS fixes described in §15/§18 below never touch the artifact file). The checksum and the 23/23 result were identical at every checkpoint. No rerun of artifact construction was needed or performed.

## 4. Prototype Architecture

Exact file paths, listed before writing (per plan §22 step 4) and created exactly as listed:

```text
research_prototypes/painan_1663_relational/index.html
research_prototypes/painan_1663_relational/prototype.js
research_prototypes/painan_1663_relational/prototype.css
research_prototypes/painan_1663_relational/README.md
scripts/research_validators/validate_painan_1663_relational_prototype.py
```

The prototype is a single static HTML page plus one vanilla-JS file (no build step, no framework, no CDN dependency, no npm package) and one CSS file. `index.html` defines the status banner, navigation, and six empty view containers; `prototype.js` fetches the artifact once and renders into those containers; `prototype.css` is self-contained (no external stylesheet, no Google Fonts, no icon library).

## 5. Data Flow

```text
browser --fetch(GET, relative path)--> ../../data/power_relations/painan_1663_relational_research_artifact.json
       <--JSON response--
in-memory JS object (never mutated, never written back, never cached to disk by the page itself)
       --> render functions (Overview, Actors, Timeline, Network, Claim/Control, Public-Copy)
```

No other network request is made. No `localStorage`/`sessionStorage`/`indexedDB` write occurs. No form submits data anywhere. Confirmed by the prototype validator (checks 24-26, §16) and by a live browser console check (§15) showing zero requests other than the artifact fetch and zero console errors.

## 6. Actor Rendering

All six frozen actors render as distinct cards (`ACTOR_MUHAMMAD_SYAH_FACTION`, `ACTOR_RAJA_ADIL_FACTION`, `ACTOR_VOC`, `ACTOR_ACEH_COURT`, `ACTOR_GROENEWEGEN`, `ACTOR_MANSUR_SYAH`), each showing: label, `actor_type`, `actor_id`, named individuals (where present), description, a non-homogenization notice (verbatim on every card, per plan §5's non-goal against merging factions), outgoing/incoming relation lists, and — where `researcher_review_required` is true — a warning glyph plus an explicit Level-2 disclosure for the actor's `identity_caveat`/`notes`. Confirmed live: 6 actor cards render (§15).

## 7. Relation Rendering

All nine relations render, each restricted to the seven authorized `relation_type` values (`REQUESTS_PROTECTION_FROM`, `PROVIDES_PROTECTION_TO`, `REQUIRES_MONOPOLY_FROM`, `NEGOTIATES_WITH` ×2, `RECONCILES_WITH`, `MAINTAINS_PARALLEL_ALIGNMENT_WITH`, `CLAIMS_JURISDICTION_OVER` ×2). Every relation record is run through a client-side structural validator (`validateRelation()` in `prototype.js`) before rendering: missing required fields, forbidden relation types (`PATRON_OF`/`CLIENT_OF`/`PATRON_CLIENT_RELATION`), unauthorized relation types, or unresolved endpoints each produce a per-record validation error surfaced in the Overview view (§8.1 of the plan) rather than a silent skip or a full-page crash — consistent with plan §12's requirement. In this run, zero validation errors occurred (all nine relations passed).

## 8. Timeline Rendering

The Relation Timeline view renders all nine relations as independent, non-overwriting bars against a shared 1662-1666.5 axis, filterable by actor and by relation type. Overlapping validity ranges render simultaneously — directly demonstrated for the Oct 1663 window, where `PROVIDES_PROTECTION_TO` (VOC→Muhammad Syah faction, open-ended), `RECONCILES_WITH` (Muhammad Syah faction→Aceh court, Oct 1663 onward), and `MAINTAINS_PARALLEL_ALIGNMENT_WITH` (Muhammad Syah faction→VOC, Oct 1663 onward) all render as separate, visible bars rather than one bar replacing another. Open-ended `valid_to` is marked with a trailing arrow (`→`). Explicit relations render as a solid blue bar; `OBSERVED_ACTION_AS_STRATEGY` (secondary-source-only) relations render as a diagonally-striped orange bar — confirmed via live screenshot (§15).

## 9. Network Rendering

A hand-rolled SVG diagram (no charting library) places the six actors on a circle and draws directed, arrow-headed curves for each relation. Multiple edges between the same actor pair are drawn as separate offset curves (confirmed for the Muhammad Syah faction ↔ VOC pair, which carries four distinct relations). No relation is ever labeled `PATRON_OF` or `CLIENT_OF` — edges are labeled only by their `relation_type`; patron-client status exists solely inside each relation's Level 3 detail drawer below the diagram. Explicit relations render as solid lines; `OBSERVED_ACTION_AS_STRATEGY` relations render dashed; `CONTESTED_CONTROL` relations render in a distinct red hue in addition to the dash pattern (non-color-only distinction is also carried by the dash pattern itself). Confirmed live: 6 SVG nodes, 9 SVG edges (§15).

**Known limitation (not blocking):** with four edges converging on the same actor pair, edge labels sit close together in the densest region of the diagram; after a mid-build fix (staggering label position further along each curve's offset and adding a background plate behind each label — see §18), most labels are legible, but one pair (`MAINTAINS_PARALLEL_ALIGNMENT_WITH` near the Raja Adil node, and a `REQUESTS_PROTECTION_FROM`/`CLAIMS_JURISDICTION_OVER` pair near the diagram's lower-left) still partially overlap in the desktop screenshot. Every edge carries a full `<title>` tooltip and an `aria-label` with the complete relation type, actors, and claim/control status, so the information is not lost — only the always-on visual label is occasionally crowded. Flagged for researcher visual review per plan §10 ("do not adopt these semantics as final without visual review"), not silently accepted as finished.

## 10. Claim versus Effective Control

The dedicated view lists all ten values of the frozen `claim_or_effective_control` vocabulary, marking which are actually present in this artifact (5 of 10: `CONTESTED_CONTROL`, `UNKNOWN_EFFECTIVE_CONTROL`, `TREATY_OBLIGATION`, `FORMAL_ACCEPTANCE`, `MILITARY_PRESENCE`) versus not present, and groups the nine relations under their respective category with the fixed explanatory sentence: *"A claim or formal agreement does not by itself demonstrate effective control."* No value is invented and no value absent from the artifact is presented as if it were active data.

## 11. Evidence and Source Display

Every relation's Level 2 disclosure (closed by default) shows: `source_statement_summary`, `historical_reconstruction`, `source_document_ids`, `source_passage_locator`, `event_ids` (or an explicit "(none — secondary-source-only relation)" note when empty), `provenance_status`, `claim_or_effective_control`, `commitment_credibility`, `interpretive_status`, and `researcher_review_required`. All fields are rendered from the artifact verbatim — no field is summarized, reworded, or silently dropped.

## 12. Theory Display

Every relation's Level 3 disclosure (closed by default, never auto-opened by any other action) begins with a fixed notice — *"Level 3 research annotation — NOT a confirmed historical fact."* — followed by `power_dimensions`, `patron_client_classification`, `theoretical_annotation`, and `notes` (which carries counterevidence/limitations in this artifact's own schema). Confirmed live (§15): the first Level 3 drawer on the page starts closed and opens only after an explicit click on its summary control, and the first Level 2 drawer independently starts closed as well — no field renders open by default.

## 13. Public-Copy Boundaries

The Public-Copy Preview view places all four interpretive layers — source statement, historical reconstruction, theoretical annotation, public-display summary — side by side in four visually distinct, separately colored cards for every relation, so a reviewer can see at a glance that the public-copy text is not simply a copy of the theory text. The base artifact validator's own checks (u/v/w) already confirm no two of these four fields are byte-identical for any relation; the prototype adds a visual confirmation of that separation on top of the data-level guarantee.

## 14. Accessibility

Implemented and verified:

- **Keyboard access:** all navigation controls are native `<button>` elements; all disclosures are native `<details>/<summary>`; the only custom-tabindex elements are the SVG network edges (`tabindex="0"`, each with its own `aria-label`) needed because SVG `<path>` is not natively focusable. A clean, fresh-page-load Playwright test (§15) confirmed Tab order reaches all six nav buttons first, in the correct left-to-right order, and that pressing Enter on a focused nav button correctly switches the active view.
- **Focus visibility:** a `:focus-visible` outline (3px, high-contrast gold) is defined once and applies to every interactive element.
- **Semantic structure:** one `<h1>` per view, `<h2>`/`<h3>` for subsections, `role="banner"`/`role="status"`/`aria-live="polite"` on the status regions, `role="img"` plus `aria-label` on the SVG diagram and on each edge.
- **Non-color distinction:** explicit-vs-inferred and claim/control states are carried by border style (solid/dashed/dotted), badge text, and stroke-dasharray on SVG edges — never by color alone.
- **Reduced motion:** a `prefers-reduced-motion` media query collapses all animation/transition durations to near-zero.
- **No hover-only information:** every piece of information available via a tooltip (`title` attribute) is also available via a click-to-open disclosure or a visible label; nothing is hover-exclusive.

**Known limitation:** an early automated keyboard-focus test produced a misleading `false` result for "reached a nav button," which on investigation was a test-script artifact (the sampling loop began mid-session, after a nav button was already programmatically focused by a prior `.click()` call, so the recorded sequence only showed elements *after* that point). A corrected, fresh-page-load test (§15) shows the real behavior is correct. This is recorded here for transparency, not concealed.

## 15. Responsive Behavior

The prototype was served locally (`python3 -m http.server`, repository root) and exercised with a real headless Chromium browser (via `npx playwright`, using the browser binary already cached at `~/.cache/ms-playwright`) at two viewports:

**Desktop (1280×900):** 0 console errors, 0 page errors; banner visible with the exact required text; 6 actor cards; network SVG with 6 nodes and 9 edges; 9 timeline bars; Level 2 and Level 3 disclosures both start closed and Level 3 opens correctly on click; keyboard Tab order (fresh-load test) correctly reaches all six nav buttons in order, and Enter activates the focused button.

**Narrow (375×812, iPhone-SE class):** banner and nav both remain visible; network SVG still renders; **an initial run found genuine horizontal overflow (125px)** — traced via element-by-element bounding-box inspection, direct screenshot review, and a `scrollWidth`/`scrollTo` probe to a single unwrapped text run in the `#load-status` banner (the artifact's long relative path had no `overflow-wrap` rule, so it pushed the document 125px wider than the viewport). This was a real defect in newly-written prototype CSS, not a change to reviewed research data, so it was fixed directly: `overflow-wrap: anywhere` was added to `#load-status` and, as a general safety net, `overflow-wrap: break-word` was added to `body`. **Re-verified after the fix: 0px horizontal overflow, 0 offending elements, confirmed both by measurement and by visual screenshot review.** The same fix pass also improved network-diagram label legibility (§9).

All screenshots (`proto_desktop_overview.png`, `proto_desktop_actors.png`, `proto_desktop_network.png`, `proto_desktop_timeline.png`, `proto_narrow_overview.png`, `proto_narrow_network.png`) were captured to the session scratchpad for this review; they are not part of the repository and were not committed.

## 16. Prototype Validation

`scripts/research_validators/validate_painan_1663_relational_prototype.py` — read-only, no writes, no network calls, checks the prototype's static source against the artifact and the base validator. Final result after the fixes in §15:

```text
CHECKS PASSED: 30/30
VALIDATION RESULT: PASS
```

Two rounds of false positives in the validator's own first draft (items 24, 26, 27 — naive string matching flagged the prototype's own explanatory comments/banner text that *describe the absence* of fetch-to-other-hosts, Graphify usage, and production-template references, mistaking prose for functional usage) were corrected by refining the validator's matching logic to require actual functional-usage patterns (a real `fetch(` call argument, a `graphify(` call/import/path, a literal production-template path) rather than a bare word match — the underlying prototype code did not need to change for these three; only the validator's precision did. This correction is disclosed here rather than silently applied.

## 17. Researcher Review Questions

The ten questions from plan §14 map onto the prototype as follows (answerable directly from the rendered page, not requiring source-code reading):

1. **Distinct factions vs. locations** — Actors view: all six cards are named factions/institutions/individuals; none is a place name.
2. **Explicit vs. inferred** — every relation carries a visible badge (`EXPLICIT_STRATEGY` green solid / `OBSERVED_ACTION_AS_STRATEGY` orange striped) in both the Actors list and the relation detail panel.
3. **Jurisdictional claim vs. control** — Claim vs Effective Control view groups relations by exactly this distinction, with the fixed explanatory sentence.
4. **Protection-bargain evidence** — `REQUESTS_PROTECTION_FROM`/`PROVIDES_PROTECTION_TO` Level 2 drawers show `source_statement_summary` and `source_passage_locator` directly.
5. **Why reconciliation weakens clean substitution** — the `RECONCILES_WITH` relation's Level 3 drawer states this explicitly in `theoretical_annotation`.
6. **Why patron-client is only partial/contested** — every relation's Level 3 `patron_client_classification` value is visible per-relation (never a single case-level verdict), and the artifact-level distribution (3 `PARTIALLY_SUPPORTED`, 1 `CONTESTED`, 5 `NOT_TESTABLE`, 0 `SUPPORTED`) is shown in the Overview.
7. **Unresolved actors/mandates** — Overview's dedicated section lists all `researcher_review_required` actors with their reason.
8. **Source-supported vs. theoretical** — the four-layer Public-Copy Preview view makes this explicit side by side, per relation.
9. **Implied VOC sovereignty?** — the prototype validator confirms (`check 18`) the word "sovereignty" never appears anywhere in the prototype source; `claim_or_effective_control` values are shown as a spectrum, never collapsed to a single "VOC controls" statement.
10. **Implied local homogeneity?** — every actor card carries the non-homogenization notice verbatim; Painan/Padang/Tiku and Bandar X are absent from the actor set entirely (per the frozen scope), not merged into a proxy actor.

## 18. Known Limitations

- Network-diagram edge-label crowding in the densest region of the graph (§9) — partially improved this turn, not fully resolved; flagged for researcher visual review, not treated as final.
- The prototype's own validator required two rounds of self-correction (§16) — disclosed rather than hidden; the final 30/30 result reflects the corrected, more precise checks.
- No live browser automation tool was pre-configured in this environment (the Playwright MCP tool's browser resolution failed — `chrome` executable not found at its expected path); the equivalent check was performed instead via `npx playwright` (which downloaded only the already-locally-cached browser driver package, no new browser binary) driving the already-installed Chromium at `~/.cache/ms-playwright`. This is disclosed as a deviation from the most direct tool path, not a skipped verification — the live-browser evidence in §14/§15 is real, not simulated.
- The timeline view's narrowest bars (e.g. a same-month `NEGOTIATES_WITH` relation) can visually clip their own date label inside the bar; the full date is still available via the bar's `title` attribute and `aria-label`.
- No automated cross-browser (Firefox/Safari) check was performed — only Chromium. Not required by the governing plan, noted for completeness.

## 19. Production Isolation

Checksums of five representative production files, recorded immediately before any prototype file was written and re-recorded after all prototype and validator work in this turn:

```text
frontend/map_app/static/map_app/js/atlas.js        -- UNCHANGED
frontend/map_app/templates/map_app/index.html       -- UNCHANGED
backend/main.py                                     -- UNCHANGED
nginx/nginx.conf                                     -- UNCHANGED
docker-compose.yml                                   -- UNCHANGED
```

No file under `backend/`, no production frontend template, no `atlas.js`, no Nginx config, no Docker config, no migration, no database, no API endpoint, and no Graphify integration was created, modified, or invoked at any point in this turn. `git status --short` shows only the new `research_prototypes/` directory and the new prototype-validator script as additions relevant to this task (plus pre-existing, unrelated untracked files already present in the working tree before this turn began, including the governing plan document itself, which arrived in the repository root outside this session's own actions). Nothing was staged (`git add` was never run) and nothing was committed, pushed, or deployed.

## 20. Readiness Decision

```text
PAINAN_LOCAL_RELATIONAL_PROTOTYPE_READY_FOR_RESEARCHER_REVIEW
```

All 30 prototype validations pass, the underlying artifact and base validator are unchanged and re-confirmed, production isolation is confirmed both before and after by checksum, and a real (not simulated) headless-browser pass confirms the prototype loads, renders all six actors and nine relations, keeps Level 2/3 disclosures closed by default, and — after one genuine responsive-CSS defect was found and fixed — renders without horizontal content loss at a 375px viewport. The one open item (network-label crowding, §9/§18) is cosmetic, does not hide or misrepresent any data (full information remains available via tooltip/aria-label), and is explicitly flagged for the researcher's own visual-semantics review rather than presented as finished.

---

## 21. Researcher Visual Review Preparation

Conducted as a separate, later turn, strictly after §1-20 above (technical validation) were already complete. No artifact content or research finding was touched. Purpose: produce the concrete screenshot and interaction evidence a human reviewer needs before accepting the prototype, and fix any concrete rendering/interaction defect found — not aesthetic preference.

### 21.1 Local server

```text
python3 -m http.server 8899 --bind 127.0.0.1
```

Confirmed bound to `127.0.0.1` only via `ss -tlnp` (`LISTEN 127.0.0.1:8899`, not `0.0.0.0`) before any screenshot was taken. Stopped at the end of the session; confirmed unreachable afterward (`curl` to port 8899 failed after kill).

### 21.2 Browser tool used

The Playwright MCP tool's browser resolution failed again in this turn with the same error as the prior technical-validation pass (`"chrome" executable not found`). Per instruction, no browser was installed and no environment change was made. An already-available, already-cached Chromium binary (`~/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome`, downloaded in a prior session, not re-downloaded this turn) was driven directly via the `playwright` npm package (also already present from the prior turn's `npm install` in the session scratchpad; no new package version or browser binary was fetched). This is disclosed as the "other available browser" path used, per instruction item 3, rather than a substitute for a genuinely missing browser.

### 21.3 Screenshots captured

All saved to the session scratchpad only (not part of the repository, not committed):

```text
proto_review_desktop_overview.png       -- 1280x900, Overview
proto_review_desktop_actors.png         -- 1280x900, Actors
proto_review_desktop_timeline.png       -- 1280x900, Relation Timeline
proto_review_desktop_network.png        -- 1280x900, Relation Network
proto_review_desktop_claimcontrol.png   -- 1280x900, Claim vs Effective Control
proto_review_desktop_publiccopy.png     -- 1280x900, Public-Copy Preview
proto_review_narrow_overview.png        -- 375x812, Overview
proto_review_narrow_timeline.png        -- 375x812, Relation Timeline
proto_review_narrow_network.png         -- 375x812, Relation Network
proto_review_level2_drawer.png          -- 1280x900, Relation Network detail panel, Level 2 open / Level 3 closed
proto_review_level3_drawer.png          -- 1280x900, Relation Network detail panel, Level 3 open / Level 2 closed
```

`proto_review_findings.json` (same directory) holds the structured per-screenshot metadata and interactive-test results referenced below.

### 21.4 Per-screenshot findings

For all eleven screenshots: **0px measured horizontal overflow** (per-element bounding-box scan, `document.body`/`documentElement.scrollWidth` cross-check, and direct visual confirmation), **0 clipping**, **0 browser console errors or page errors** across the full desktop session. Text was reviewed manually from each screenshot and found readable at both viewports. Full per-screenshot detail (view, selected relation where applicable, drawer state, overflow measurement) is recorded in `proto_review_findings.json`; summarized findings:

- **Overview (desktop & 375px):** stat tiles, distribution lists, unresolved-actors section, and source-gaps section all legible; warning box border/background renders without color-only reliance (bordered box + explicit "RESEARCH-ONLY WARNING" text).
- **Actors (desktop):** all 6 cards render with visible non-homogenization notice on every card and a warning glyph (⚠) next to `researcher_review_required` actors — not color-only.
- **Relation Timeline (desktop & 375px):** all 9 bars render on independent, non-overwriting rows; the Oct 1663 overlap (`PROVIDES_PROTECTION_TO`, `RECONCILES_WITH`, `MAINTAINS_PARALLEL_ALIGNMENT_WITH`, all open-ended) is directly visible as three separate simultaneous bars — this is the single most important visual confirmation the plan's research question asks for, and it renders correctly. Minor, previously-disclosed cosmetic limitation reconfirmed: the narrowest bar (`NEGOTIATES_WITH`, Mansur Syah→VOC, a same-month event) visually crowds its own date label inside a very short bar; the full date remains available via the bar's `title` tooltip and `aria-label`. No content is lost, so this is not treated as a blocking defect.
- **Relation Network (desktop & 375px):** 6 nodes, 9 edges confirmed present in the SVG DOM at both viewports; legend renders; solid/dashed/red-dashed distinctions visible without relying on color alone (dash pattern differs per category).
- **Claim vs Effective Control (desktop):** all 10 controlled-vocabulary values listed, only the 5 present in this artifact shown as active with counts; relations correctly grouped under their category heading; no invented or overclaimed category.
- **Public-Copy Preview (desktop):** all 9 relations render as four side-by-side, distinctly colored/labeled cards (Source statement / Historical reconstruction / Theoretical annotation / Public-display summary). Manually reviewed every `public_display_summary` shown: none asserts VOC sovereignty, none states a patron-client relation as settled fact, none omits the "contested" qualifier where the underlying record carries one (e.g. the `CLAIMS_JURISDICTION_OVER` summary explicitly states "whether that authority was actually enforced afterward is contested by the sources"). This is the direct check the requester asked for — that the display does not produce a stronger claim than the source — and it passes on manual read-through.
- **Level 2 / Level 3 drawers (desktop):** confirmed independently toggleable (Level 2 closed while Level 3 open, and vice versa, in the two respective screenshots); the Level 3 drawer's fixed notice ("NOT a confirmed historical fact") is visible as bordered, non-color-dependent text above the theory content.

### 21.5 Interactive test results

Executed against a fresh page load (desktop viewport):

```text
Keyboard Tab order (first 6 stops):      Overview -> Actors -> Timeline -> Network -> Claim/Control -> Public-Copy
                                          (matches on-screen left-to-right nav order exactly)          PASS
Enter activates a focused nav button:    focused "network" button + Enter -> active view = network     PASS
Space toggles a details/summary:         closed -> open on Space keypress (scoped, visible element)    PASS
Visible focus outline on nav button:     3px solid rgb(255,209,102) computed style                     PASS
Actor filter (Timeline):                 9 rows -> 1 row when filtered to "Raja Adil faction"           PASS
Relation-type filter (Timeline):         9 rows -> 1 row when filtered to "RECONCILES_WITH"              PASS
Timeline overlap / parallel alignment:   PROVIDES_PROTECTION_TO, MAINTAINS_PARALLEL_ALIGNMENT_WITH, and
                                          RECONCILES_WITH all present simultaneously in the filtered-out
                                          (unfiltered) row set -- none overwrites another                PASS
Source/theory layer separation:          Public-Copy Preview renders exactly 4 headers per relation:
                                          "Source statement", "Historical reconstruction",
                                          "Theoretical annotation (Level 3)", "Public-display summary"    PASS
```

### 21.6 Defects found and disposition

**Zero defects in the prototype's own code were found in this review pass.** Two anomalies surfaced during test authoring, both investigated to a definitive root cause, and both attributed to the *test script*, not the prototype:

1. An unscoped Playwright locator (`details.disclosure.level2 summary` without a view-container prefix) matched a hidden, non-visible drawer inside the `#view-actors` section (the single `identity_caveat` disclosure on the Muhammad Syah faction card) instead of the intended visible drawer inside `#view-network`, causing `.focus()` to silently fail and making Space/Enter appear not to toggle anything. Rescoping the locator to `#view-network details.disclosure.level2` reproduced correct behavior (Enter: closed→open; Space: open→closed) on the first attempt. **No prototype code was changed** — confirmed via a minimal, isolated repro script before touching the main test.
2. An earlier keyboard-focus sample (from the prior technical-validation turn, re-confirmed here) showed `false` for "reached a button" purely because the sampling loop began after a nav button was already focused by a prior programmatic click; a fresh-load Tab sequence (§21.5 above) shows the real, correct behavior.

Because no concrete defect exists in the prototype itself, **no prototype file was edited in this turn** (per instruction item 6 — no change without a concrete defect). This is a deliberate difference from the earlier technical-validation pass, which *did* find and fix one real CSS overflow defect (`#load-status` unwrapped text) before reaching 30/30 — that fix remains in place and was re-confirmed unaffected by this turn's testing.

### 21.7 Before/after

Not applicable this turn — no fix was required, so there is no before/after pair to document beyond what §15/§18 (technical-validation turn) already recorded for the one CSS fix made then.

### 21.8 Post-review verification

```text
Base artifact validator:      23/23 PASS, 0 warnings, 0 errors
Prototype validator:          30/30 PASS
Artifact SHA-256:              eeeeda8b368e255303c46dc245beb3c1179815d9f960cdff20b1ea59518b4bd7  (unchanged)
Production isolation:          atlas.js, production index.html, backend/main.py, nginx.conf,
                                docker-compose.yml -- all 5 checksums unchanged before vs. after
Local server:                  stopped; port 8899 confirmed unreachable after stop
```

### 21.9 Visual Review Readiness Decision

```text
PAINAN_LOCAL_RELATIONAL_PROTOTYPE_VISUALLY_READY_FOR_RESEARCHER_REVIEW
```

Screenshot and interaction evidence is now available for a human reviewer at both required viewports, covering every required view and both disclosure levels, with zero concrete defects outstanding (the two candidate anomalies were test-script artifacts, disclosed and resolved without touching prototype code) and one previously-fixed defect re-confirmed stable. Manual read-through of every `public_display_summary` found no claim stronger than its underlying source record. This readiness decision covers the *prototype's* fitness for human visual review only — it does not itself constitute researcher acceptance, and does not authorize staging, committing, pushing, or any production/Atlas integration.
