# SALIDO-HDT Research Application — `/riset/enclave-1682` Plan

Read-only planning document. No application code is written by this
document. Canonical research inputs remain read-only:
`docs/enclave/salido_hdt_model_v0_3/`, `_v0_4/`, `_v0_4_1/`. Accepted
solver: commit `9caeec0708f32b64f77501356107b28893ee5907`.

---

## 0. Architecture audit findings (read-only)

Determined by direct inspection of the repository, not assumed:

| question | finding |
|---|---|
| Web framework(s) | **Two, coexisting, serving different concerns.** (1) Django 5.0.4 (`frontend/requirements.txt`) serving server-rendered templates for the main map + all `/riset/*` and `/linimasa` pages. (2) A Create React App (react-scripts 5.0.1, ejected via `@craco/craco`) with React 19, shadcn/ui-style components (Radix + `class-variance-authority`, `components.json`), Tailwind, `react-router-dom` v7 -- but its `src/pages/` contains exactly **one** page (`MapDashboard.jsx`); it is not used for `/riset/*` today. |
| Routing conventions | Django: `frontend/map_app/urls.py`, flat `path("riset/<slug>/", views.<name>, name="<name>")` entries, view functions in `frontend/map_app/views.py`. |
| App-router vs pages-router | N/A (not Next.js). Django URLconf + CRA `react-router-dom`, unrelated to each other. |
| Layout conventions | No shared Django base template exists yet -- each `/riset/*` template is a **self-contained** `<!DOCTYPE html>` document repeating an inline `<style>` block (CSS custom properties: `--ground/--panel/--ink/--muted/--line/--accent`, `--serif` = EB Garamond, `--sans`/`--mono` = Space Grotesk) and a `.topnav` with hardcoded sibling links. This is intentional, documented in-source: "*Identitas visual salido.my.id*", "*light-only, konsisten riset_tema/riset_jaringan/riset_atjeh*". |
| Existing `/riset/` routes | `riset/tema/`, `riset/petunjuk-arsip/`, `riset/jaringan/`, `riset/atjeh-dagang/`, `riset/pemodelan/` (plus top-level `linimasa/`, not under `/riset/`). All five carry `<meta name="robots" content="noindex, nofollow">` and are **excluded from the public navbar** (confirmed in view docstrings: "*thesis-only*"). |
| Server vs client data-loading | **Two established sub-patterns, both server-rendered shells:** (a) *client-side fetch*: `riset_tema`/`riset_jaringan`/`riset_atjeh` render a static template; JS fetches JSON from `/api/research/*` (nginx-proxied to the FastAPI backend) at browser load time. (b) *full SSR*: `riset_pemodelan`/`linimasa`/`port_detail` call `httpx.get()` **synchronously inside the view**, `try/except` wrapping every backend call, always falling back to a `backend_error` flag passed into the template context -- content is server-rendered, JS is progressive enhancement only. `riset_pemodelan` additionally embeds pre-rendered Bokeh HTML/JS fragments (script+div) returned directly by the backend. |
| API route conventions | All existing `/riset/*` data comes from the **FastAPI backend** (`backend/routers/research.py`, prefixed `/api/research/*`), reached via `API_BASE_URL` env var (`http://backend:8000` in compose, `http://voc_backend:8000` fallback in code). **This app's data source (`docs/enclave/salido_hdt_model_v0_4_1/` CSVs + solver JSON/CSV output) is NOT in that backend's database at all** -- see §5 for why this plan does not add it there. |
| Styling system | Hand-rolled CSS custom properties per page (no Tailwind on the Django side; Tailwind exists only inside the separate, unused-for-`/riset/*` CRA app). Fonts: Google Fonts EB Garamond (serif, headings) + Space Grotesk (sans/mono, body/data). Palette: cream/white light-only, explicitly overriding any viewer dark-mode preference (`:root[data-theme]{...}` pinned). |
| Chart/graph libraries already installed | **Bokeh** (vendored locally: `frontend/map_app/static/map_app/vendor/bokeh-3.9.1.min.js` + `bokeh-widgets-3.9.1.min.js`, per memory `Dashboard Bokeh Pemodelan` -- "BokehJS divendor lokal, bukan CDN") -- used server-side (Python `bokeh` in the FastAPI backend, embedded as HTML/JS fragments). No D3/Chart.js/Plotly on the Django side. (The unused CRA app separately has `d3` and `recharts` as npm deps, irrelevant here since `/riset/*` is Django-rendered.) |
| Localization | 100% Bahasa Indonesia across every `/riset/*` template and view docstring (`lang="id"`); this plan's UI copy follows suit. |
| Test framework | Django `SimpleTestCase`/`TestCase` + `django.test.Client`, `unittest.mock.patch` for mocking `httpx` calls (`frontend/map_app/tests.py`, 1,454 lines, extensive precedent). No pytest on the Django side (pytest is used only for the separate `salido_hdt` solver package under `tests/salido_hdt/`). |
| Build & deploy | `docker compose up -d --build frontend` (rebuild required -- **not** volume-mounted, per project memory `Network Graph Fase 1`/`Dagang Atjeh`: "*backend TAK volume-mounted, wajib --build*", same applies to frontend); `docker compose exec frontend python manage.py test map_app`; `curl http://localhost:8084/riset/enclave-1682/` for smoke verification; production deploy via SSH to `westkust-prod` + `git pull` + rebuild (per memory `Server Production Salido`). |

**Constraint respected**: no new web framework introduced, no library
duplicated. This plan uses Django (already the framework for every
existing `/riset/*` page) and Bokeh (already vendored and used
server-side) exclusively.

---

## 1. Exact files to create

```
frontend/map_app/enclave_data.py                    # server-side data adapter (new module)
frontend/map_app/templates/map_app/riset_enclave_1682.html
frontend/map_app/static/map_app/js/enclave_1682.js   # progressive enhancement only (filters, tab switching)
frontend/map_app/data/enclave_1682_solver_run/       # committed, pre-generated solver output snapshot (see §5)
  ├── scenario_00.json .. scenario_04.json
  ├── validation_summary.json
  ├── equipment_capacity.csv
  ├── entity_presence.csv
  ├── candidate_entities.csv
  └── excluded_entities.csv
docs/enclave/implementation/ENCLAVE_1682_SOLVER_SNAPSHOT_PROVENANCE.md  # records exact commit + regeneration command for the snapshot above
```

## 2. Exact files to modify

```
frontend/map_app/urls.py    # add: path("riset/enclave-1682/", views.riset_enclave_1682, name="riset_enclave_1682")
frontend/map_app/views.py   # add: riset_enclave_1682(request) view function
frontend/map_app/tests.py   # add: RisetEnclave1682ViewTest class (append, do not restructure existing classes)
docker-compose.yml          # add a read-only volume mount for the frontend service (see §5) -- DECISION POINT, see below
```

**Decision point flagged for explicit confirmation, not silently
resolved**: the canonical dataset lives at `docs/enclave/salido_hdt_model_v0_4_1/`,
outside `frontend/`'s Docker build context (`COPY . .` in
`frontend/Dockerfile` only copies `frontend/`). Two options:

- **(A) recommended** -- add a read-only volume mount to the `frontend`
  service in `docker-compose.yml`:
  `- ./docs/enclave/salido_hdt_model_v0_4_1:/app/enclave_data/salido_hdt_model_v0_4_1:ro`.
  Preserves single-source-of-truth (matches this whole project's
  established "never duplicate canonical data" discipline); requires a
  `docker-compose.yml` change the user should review before `docker
  compose up`.
  For LOCAL (non-Docker) `python manage.py runserver` development, the
  adapter resolves the same path directly via the filesystem
  (`Path(__file__).resolve().parents[3] / "docs/enclave/salido_hdt_model_v0_4_1"`)
  when the mounted path does not exist -- i.e. two lookup locations,
  documented in `enclave_data.py`'s own docstring, no behaviour silently
  differing between dev and prod.
- (B) alternative, not recommended -- copy the dataset into `frontend/`
  at image-build time. Rejected: creates a second, driftable copy of
  canonical data, the exact anti-pattern this session's entire solver
  work was built to avoid.

**Solver output is never computed at request time** (`Do not run the
solver in the browser`, and equally must not run synchronously in a
Django view -- a CP-SAT solve can take up to
`config.SOLVE_TIME_LIMIT_SECONDS=30s` per re-solve, and
`collect_scenarios()` performs several). It is generated **offline**,
once, via the already-existing, already-tested CLI
(`python -m salido_hdt.solver.cli --scenarios 5 --output <dir>`), and the
resulting small JSON/CSV files (a handful of KB each -- confirmed during
the final release audit) are committed to
`frontend/map_app/data/enclave_1682_solver_run/`, with the exact commit
hash (`9caeec0`) and regeneration command recorded in a provenance doc.
Regenerating this snapshot after a future solver change is a manual,
explicit step (mirrors the project's existing "reseed wajib manual"
convention for `/riset/*` data, per memory `Server Production Salido`),
never automatic.

## 3. Route structure

```
GET /riset/enclave-1682/                 Phase 1 (this plan): single page, all sections, tab-based navigation within the page
GET /riset/enclave-1682/process-model/   Phase 1: static "in development" placeholder tab/section (see §10) -- may be a same-page tab, not a separate URL, to avoid a second Django view for a non-functional stub; decided in favor of a same-page <section id="process-model"> to minimize route surface, revisit if Petri Net work grows large enough to need its own template
```

Single route, `noindex`, excluded from the public navbar (consistent with
every existing `/riset/*` page).

## 4. Component structure

Since this is server-rendered Django + vanilla JS (no React on this
side), "components" means **template partials + CSS block conventions**,
matching `riset_pemodelan.html`'s existing `.section`/`.plate`/`.caption`
pattern:

```
riset_enclave_1682.html
├── <nav class="topnav">                         (reused verbatim from existing pages, add "Enclave 1682" self-link + sibling links)
├── <header> title + archival-source context      (MVP §1)
├── <section id="dataset-status">                 (MVP §2 -- banner)
├── <section id="summary-metrics">                (MVP §3)
├── <section id="timeline">                       (MVP §4)
├── <section id="entities">                       (MVP §5 -- human/group explorer)
├── <section id="locations">                      (MVP §6 -- location hierarchy)
├── <section id="weekly-operations">              (MVP §7)
├── <section id="hoffman-vogel-assay">            (MVP §8)
├── <section id="inventory">                      (MVP §9)
├── <section id="scenario-profiles">              (MVP §10)
├── <section id="evidence-legend">                (MVP §11)
├── <section id="process-model">                  (Petri Net stub, §10 of this plan)
├── <section id="methodology-limitations">        (MVP §12)
└── <footer>                                       (reused verbatim)
```

Each `<section>` independently handles its own loading/empty/error
sub-state via server-rendered conditional blocks (`{% if %}`), not a
client-side spinner -- consistent with the SSR-first `riset_pemodelan`/
`linimasa` pattern, since all data here is read at request time from
local files (fast, no network round-trip to wait on client-side).

## 5. Data-access architecture

```
frontend/map_app/enclave_data.py
```

A single new module, read-only by construction (every file opened with
`open(path, "r", ...)`, mirroring `salido_hdt.solver.data_loader`'s own
discipline -- deliberately re-implemented independently in pure-stdlib
`csv`/`json`, NOT by importing the `salido_hdt` package cross-tree, since
`src/salido_hdt/` is outside `frontend/`'s build context and adding it as
a runtime dependency would require either (a) the same volume-mount
question as the dataset itself, or (b) packaging `salido_hdt` for pip
install into the frontend image -- both larger changes than this MVP
needs; the adapter only needs to *read already-flat* CSV/JSON, not
re-derive presence/provenance/HARD-soft classification, so stdlib
`csv.DictReader`/`json.load` suffice).

```python
def load_canonical_summary() -> dict:
    """Row counts per canonical CSV (01-16 + MANIFEST), read live from the
    mounted/local dataset path. Never caches across requests in a way that
    could mask a dataset change -- read fresh every request (files are
    small, <1MB combined; no perf concern, see §13)."""

def load_solver_run() -> dict:
    """Reads the COMMITTED snapshot under
    frontend/map_app/data/enclave_1682_solver_run/ -- never the live
    canonical tree, never re-solves. Returns scenarios (grouped per §9),
    validation_summary, equipment_capacity rows, entity coverage rows."""

def group_scenarios_into_profiles(scenarios: list[dict]) -> list[dict]:
    """Pure function, no I/O. Implements the exact grouping decided in
    SOLVER_V0_1_4_FINAL_RELEASE_AUDIT.md Bagian C: scenario_00 (idle) is
    profile 1; scenario_01-04 (pairwise assignment_distinct_but_equivalent,
    mechanism-only differences) are profile 2, labeled 'diversification
    variants', never presented as 4 independent reconstructions."""
```

**Canonical dataset read-only guarantee (§6 below expands this)**: this
module never opens any canonical CSV in `"w"`/`"a"` mode -- enforced the
same way `salido_hdt`'s own `test_load_never_opens_files_in_write_mode`
does, via a dedicated Django test that monkeypatches `builtins.open` and
asserts every call against the canonical path uses `"r"`.

## 6. Canonical dataset read-only guarantees

1. `enclave_data.py` contains **zero** write-mode `open()` calls against
   any path under `salido_hdt_model_v0_4_1` -- verified by a dedicated
   test (§12).
2. The Docker volume mount (§2, option A) is declared `:ro` --
   filesystem-level enforcement, not just an application-level promise.
3. Solver output is a **committed, offline-generated snapshot**, never
   computed against the live tree inside a request -- so no request can
   ever trigger a solver run that (even read-only) touches the dataset
   under load.
4. `test_no_source_mutation.py`-style SHA-256 before/after checks are
   re-run manually as part of this plan's own acceptance step (§15), the
   same discipline used for every solver patch this session.

## 7. API schemas

No new HTTP API endpoints are introduced (`Do not run the solver in the
browser`, and this page is fully SSR -- no client-side fetch to a new
JSON endpoint is needed for MVP Phase 1, unlike `riset_tema`/
`riset_jaringan`/`riset_atjeh`'s client-fetch pattern). All data
schemas below are **Python dict shapes returned by `enclave_data.py`**,
consumed directly by the Django template context -- not wire-format
JSON APIs (no versioning/backward-compat concern beyond this repo).

```python
# load_canonical_summary() ->
{
    "row_counts": {"01_documents": 5, "02_persons": 51, ..., "16_location_adjacency": 22},
    "manifest_file_count": 37,
    "file_hashes": {...},  # sha256 per file, for the dataset-status banner
}

# load_solver_run() ->
{
    "solver_commit": "9caeec0708f32b64f77501356107b28893ee5907",
    "profiles": [
        {"profile_id": "idle", "label": "Rekonstruksi tanpa penugasan (biaya 0)", "scenario_ids": ["scenario_00"], "objective_value": 0},
        {"profile_id": "active-cluster", "label": "Klaster aktif ~9 entitas (biaya 1, varian diversifikasi)", "scenario_ids": ["scenario_01","scenario_02","scenario_03","scenario_04"], "objective_value": 1},
    ],
    "assignments": [ {...one row per active_assignments entry, all 17 fields from cli.py's schema, unmodified... } ],
    "entity_coverage": [ {"entity_id":..., "state": "assigned"|"present_but_unassigned"|"reporting_only_presence"|"excluded_with_reason", ...} ],  # computed via the SAME union-across-scenarios logic as the final release audit, not the scenario-0-only CSV
    "equipment_capacity": [ {...all columns from equipment_capacity.csv, unmodified...} ],
    "unused_terms": [  # health/movement/equipment-preference disclosure, hardcoded from the final release audit's Bagian A findings (not re-derived at request time -- these are static facts about the accepted solver commit)
        {"term": "q[h,t] health-state variables", "status": "not solver-active", "note": "constructed but referenced by no constraint or objective term"},
        {"term": "add_minimum_movement_penalty", "status": "not objective-active", "note": "called, return value discarded, not a penalty_breakdown key"},
        {"term": "add_serviceable_equipment_preference_penalty", "status": "not objective-active", "note": "defined, never imported or called"},
    ],
}
```

## 8. Evidence and uncertainty UI

Directly reuses this dataset's OWN controlled vocabularies -- never
invents a new severity scale:

- **Evidence status** (`explicit` / `normalized` / `interpreted` /
  `reconstructed` / `parallel_reading` / `uncertain` /
  `needs_image_review` / `rejected`, per `UNCERTAINTY_POLICY.md`) --
  rendered as a small set of visually distinct badges (color + icon,
  never color-alone, for accessibility -- see §11). `explicit`,
  `interpreted`, and `reconstructed` are the three states the acceptance
  criteria explicitly require to be visually distinct (criterion 8);
  the other five vocabulary values get their own badge too, for
  completeness, not folded into the three.
- **Provenance precision** (`claim_level` / `section_level` /
  `document_level` / `missing` / `ambiguous`, per `validation.
  ProvenanceLevel`) -- shown per assignment, not collapsed.
- **Reconstruction warning**: every solver assignment row displays the
  literal string **"not an archival statement"** adjacent to the
  assignment (acceptance criterion 7), plus `assignment_state:
  solver_reconstructed` and `evidence_status: reconstructed` badges --
  these three fields are ALWAYS present together per assignment (per the
  final release audit, this is a fixed constant for every solver
  assignment), never displayed selectively.
- **Numeric anomalies** (`12_numeric_anomalies.csv`, 5 rows): rendered
  as-is with their own `validation_result`/`difference`/`status` columns
  visible -- never silently corrected or hidden (acceptance criterion
  10; matches `UNCERTAINTY_POLICY.md`'s "prohibited practice: silently
  correcting totals").
- **Unresolved readings** (30 inventory lines per
  `UNRESOLVED_READINGS.md`): each rendered inventory row shows its
  `reading_status` plainly; unresolved rows are never dropped from the
  inventory explorer (acceptance criterion 11).

## 9. Scenario-profile handling

Implements `SOLVER_V0_1_4_FINAL_RELEASE_AUDIT.md` Bagian C's finding
directly, per the explicit scenario policy in the prompt:

- All 5 solver files are read and their existence disclosed (a small
  "5 solver output files" fact in the dataset-status banner), but the
  UI **groups** them into exactly 2 profiles (per §7's schema above):
  `idle` (`scenario_00` alone) and `active-cluster`
  (`scenario_01`-`04`, labeled explicitly as "varian diversifikasi
  setara" -- equivalent diversification variants).
  - Never rendered as "Scenario 1 of 5" / "Scenario 2 of 5" framing
    (which would imply 5 independent reconstructions).
  - The `active-cluster` profile's UI shows ONE representative assignment
    set (e.g. `scenario_01`) plus an explicit note: "4 file solver
    menghasilkan klaster penugasan yang hampir identik (beda hanya
    1-2 penugasan per pasangan, dipicu oleh mekanisme diversifikasi,
    bukan oleh bukti arsip berbeda) -- ditampilkan sebagai satu profil."
- Every assignment displayed carries its full evidence quadruple (§8),
  regardless of which profile it belongs to.

## 10. Petri Net implementation phases

Per the explicit instruction: **specification work may proceed in
parallel with the MVP; simulation must not be enabled.**

- **Phase 1 (this plan, concurrent)**: the `/riset/enclave-1682/`
  page's "Process Model" tab renders two static status lines only:
  *"Petri Net specification in development"* and *"Simulation not yet
  enabled"*. No transitions, places, or tokens are computed or rendered.
  No new data adapter function is needed for this stub -- it is inline
  template content.
- **Phase 2 (future, separate plan)**: author the Petri Net structural
  specification itself (places/transitions mapped from
  `docs/enclave/salido_hdt_model_v0_4_1/docs/PETRI_NET_MODEL.md`, which
  already exists in the canonical docs) as a new markdown document,
  still no executable simulation.
  a Petri Net implementation likely lives in `src/salido_hdt/` (a new
  `petri_net` subpackage, offline/CLI-driven, matching the solver's own
  architecture) rather than in the Django app directly.
- **Phase 3 (future, separate plan, requires explicit go-ahead)**:
  wire a read-only, pre-computed Petri Net visualization into the
  Process Model tab, following the exact same "pre-generate offline,
  commit/mount the output, never compute in the browser or per-request"
  discipline established in §5 for the solver.
- **Explicitly not in scope for any phase of this plan**: enabling
  live simulation, either server-side-per-request or client-side.

## 11. Accessibility

- Every evidence/status badge (§8) pairs an icon + text label with
  color -- never color-only encoding (WCAG 1.4.1).
- `lang="id"` on `<html>` (matches every existing `/riset/*` page).
- Heading hierarchy: single `<h1>` (page title), `<h2>` per §4 section,
  `<h3>` for sub-groups within a section -- no skipped levels.
- All interactive elements (tab switches, filters in
  `enclave_1682.js`) are real `<button>`/`<a>` elements with visible
  `:focus-visible` outlines (matches existing `.home:focus-visible`
  pattern already in `riset_pemodelan.html`), operable via keyboard,
  `aria-selected`/`aria-controls` on tab controls.
- Data tables (entity explorer, inventory explorer, weekly operations)
  use real `<table>` markup with `<th scope="col">`, not div-grids --
  screen-reader-navigable.
- `prefers-reduced-motion` respected for any CSS transitions (existing
  pages already use short, subtle transitions; carried forward, gated).
- Automated check: `eslint-plugin-jsx-a11y` is already a frontend
  devDependency but applies to the (unused-here) React app only: for
  this Django-rendered page, accessibility is verified via the Django
  test suite asserting presence of `aria-*`/`scope`/`lang` attributes,
  mirroring `tests.py`'s existing "*Accessibility markup*" test class
  precedent (§12).

## 12. Testing strategy

`frontend/map_app/tests.py`, new `RisetEnclave1682ViewTest` class(es),
following the exact established idioms (`SimpleTestCase`, `Client`,
`unittest.mock.patch` where needed):

- `test_riset_enclave_1682_returns_200`.
- `test_dataset_status_banner_shows_row_counts` -- asserts real row
  counts appear (e.g. persons=51) matching a direct CSV read in the test
  itself (reconciliation, acceptance criterion 3).
- `test_all_60_entities_accounted_for` -- asserts the rendered entity
  coverage table's row count equals `len(persons) + len(aggregate_groups)`
  (acceptance criterion 4).
- `test_five_solver_files_grouped_into_two_profiles` -- asserts exactly
  2 profile blocks rendered, never 5 (acceptance criterion 5).
- `test_no_numeric_schicht_value_rendered` -- asserts the string
  `SCHICHT-` appears (controlled ids only) and no bare digit appears
  adjacent to a schicht label (acceptance criterion 6).
- `test_every_assignment_labeled_reconstructed` -- asserts "not an
  archival statement" appears once per rendered assignment row
  (acceptance criterion 7).
- `test_evidence_status_badges_visually_distinct` -- asserts distinct
  CSS classes for `explicit`/`interpreted`/`reconstructed` (criterion 8).
- `test_inventory_parent_rows_not_double_counted` -- asserts the
  rendered inventory total matches `compute via child rows only`, cross-
  checked against a direct read of `10_inventory_items.csv` in the test
  (criterion 9).
- `test_numeric_anomalies_rendered_uncorrected` -- asserts all 5
  `12_numeric_anomalies.csv` rows appear with their own `difference`
  value, not a "corrected" number (criterion 10).
- `test_unresolved_readings_visible` -- asserts unresolved inventory
  rows are present, not filtered out (criterion 11).
- `test_process_model_tab_shows_specification_in_development_status`.
- `test_canonical_csvs_never_opened_in_write_mode` -- `enclave_data.py`-
  focused, monkeypatches `builtins.open`, asserts every call against a
  canonical path uses mode `"r"` (mirrors `salido_hdt`'s own read-only
  test discipline, §6).
- `test_existing_riset_routes_unaffected` -- smoke-tests all 5 existing
  `/riset/*` routes still return 200 after this change (criterion 14).
- `enclave_data.py` unit tests (no `Client`, direct function calls):
  `test_load_canonical_summary_row_counts_match_real_csvs`,
  `test_group_scenarios_into_profiles_matches_audit_finding`,
  `test_load_solver_run_reads_committed_snapshot_not_live_solver`.

Run via: `docker compose exec frontend python manage.py test
map_app.tests.RisetEnclave1682ViewTest` (and the full `map_app` suite
for the "existing routes unaffected" check), matching `CLAUDE.md`'s
documented command.

## 13. Performance considerations

- Canonical CSVs total well under 1MB combined (`v0.4.1`'s `MANIFEST.csv`
  lists 37 files, largest ~180KB); solver snapshot files are a handful of
  KB each. Reading all of them fresh per request is inexpensive (single-
  digit milliseconds) -- **no caching layer is introduced for MVP Phase
  1** to avoid a staleness/invalidation problem for a page that isn't
  high-traffic (thesis-only, `noindex`). Revisit with Django's cache
  framework only if real request volume ever warrants it.
- No client-side data fetching, so no additional network round-trip
  beyond the initial page load (all data is SSR'd into the template).
- `enclave_1682.js` is progressive enhancement only (tab switching,
  client-side table filtering on already-rendered rows) -- the page is
  fully readable and correct with JavaScript disabled, consistent with
  `linimasa`'s documented requirement ("*Konten utama harus terbaca
  tanpa JavaScript*").

## 14. Deployment assumptions

- `docker compose up -d --build frontend` required after this change
  (frontend is not volume-mounted for code; confirmed §0).
- The new read-only dataset volume mount (§2 option A) must be present
  in `docker-compose.yml` on whichever host runs the container --
  local dev and production `docker-compose.yml` need the same addition;
  flagged as a manual deploy-checklist item, not automatic.
- No new environment variables required (no new backend API is called).
- No database migration required (no new Django model; all data is
  file-backed).
- Production verification: `curl http://localhost:8084/riset/enclave-1682/`
  returns 200, matching the existing `CLAUDE.md` "Deploy Checklist"
  pattern.

## 15. Acceptance criteria

Restating the 14 criteria given, each mapped to its concrete
verification method:

| # | criterion | verified by |
|---|---|---|
| 1 | page loads | `test_riset_enclave_1682_returns_200` + manual `curl` |
| 2 | no canonical CSV modified | `test_canonical_csvs_never_opened_in_write_mode` + manual SHA-256 before/after (§6.4) |
| 3 | summaries reconcile with canonical row counts | `test_dataset_status_banner_shows_row_counts` |
| 4 | all 60 entities accounted for | `test_all_60_entities_accounted_for` |
| 5 | 5 files grouped into 2 profiles | `test_five_solver_files_grouped_into_two_profiles` |
| 6 | no numeric schicht value displayed | `test_no_numeric_schicht_value_rendered` |
| 7 | every reconstructed assignment labelled | `test_every_assignment_labeled_reconstructed` |
| 8 | explicit/interpreted/reconstructed visually distinct | `test_evidence_status_badges_visually_distinct` |
| 9 | inventory parent rows not double-counted | `test_inventory_parent_rows_not_double_counted` |
| 10 | numeric anomalies visible, uncorrected | `test_numeric_anomalies_rendered_uncorrected` |
| 11 | unresolved readings visible | `test_unresolved_readings_visible` |
| 12 | build passes | `docker compose up -d --build frontend` exits 0, `collectstatic` succeeds |
| 13 | tests pass | `docker compose exec frontend python manage.py test map_app` |
| 14 | existing routes unaffected | `test_existing_riset_routes_unaffected` |

Additional, plan-specific acceptance (not in the original 14 but implied
by the task's own constraints): the Docker volume-mount decision (§2) is
presented to the user for explicit confirmation before being applied;
canonical dataset SHA-256 hashes re-verified unchanged immediately before
and after implementation, matching every prior solver patch's discipline
this session.

---

**Stop here per instruction.** No application code, template, URL
pattern, or `docker-compose.yml` change has been written. Implementation
awaits review of this plan.
