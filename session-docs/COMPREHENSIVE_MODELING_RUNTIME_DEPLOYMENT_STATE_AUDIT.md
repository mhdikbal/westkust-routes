# Comprehensive Modeling, Runtime, and Deployment State Audit

> **Read-only audit. No file edited, no migration run, no build/restart/reload, nothing staged/committed/pushed. CARTO remediation files (docs/security/ATLAS_CARTO_*, atlas.js, index.html, views.py, docker-compose.yml) were deliberately left untouched throughout — that workstream is mid-flight (key rotation pending) and is recorded here as-is.**

---

## Definitions (as specified by the researcher, used exactly as given)

```text
COMMITTED_LOCAL:          file is in a local commit
PUSHED_REMOTE:             commit is on origin/main
SERVER_SYNCED_NOT_RUNTIME: file is in the server checkout but not consumed by
                           any active container/API/route/database/frontend
VALIDATED_NONPRODUCTION:   modeling/prototype passed testing but is not
                           consumed at runtime
RUNTIME_DEPLOYED:          running production code actually reads, imports,
                           serves, renders, or materializes the item
PUBLICLY_ACCESSIBLE:       an internet user can reach the feature via a
                           production route
```
`DEPLOYED` requires proof via at least one of: runtime import, file read by an active service, active API response, active Django view, active frontend bundle, active DB table/migration, active route, active process/container consumer. **Server checkout sync is not runtime deployment.**

---

## Phase 1 — Authoritative Git State

```text
LOCAL:  branch main, HEAD = origin/main = 1bd96926000fb03cb1e816f7ba4ba4af1b1c7a20
        (0 ahead / 0 behind)
SERVER: /home/ubuntu/westkust-routes, branch main, HEAD = origin/main =
        1bd96926000fb03cb1e816f7ba4ba4af1b1c7a20 (identical to local)
```

Last 4 commits: `1bd9692` fix(atlas): apply CARTO basemap key to remove watermark → `64b0d59` docs(route): freeze westkust retirement decisions → `15178c9` docs(security): freeze Atlas /westkust/ route retirement planning evidence → `cfd715b` docs(security): clarify Atlas production route aliases.

**Uncommitted tracked file:** `docs/thesis/colab/POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` — working-diff fingerprint `d2805d16d33d36c7e63625f6a9af2c00eda739ce2528dcd36c4ea64c84155014`, verified unchanged throughout this audit. **Not touched by this audit.**

**Untracked work:** ~60 root/`docs/` files (mostly instruction/plan documents — see Phase 5), `data/salido_solver_snapshot/`, `docs/enclave/*`, `docs/prd/*`, `graphify-out/`, `docs/graphify-out/`, `frontend/map_app/data/`.

**CARTO fix status:** `1bd9692` is `PUSHED_REMOTE` + server-synced + container-rebuilt (confirmed live). **This is a WORKING_FIX, not a stable RUNTIME_DEPLOYED_FIX** — the mechanism is live, but the specific key currently in `.env` on `westkust-prod` was exposed in this session's terminal transcript and the researcher is waiting on CARTO to issue a replacement. Do not treat this as closed.

---

## Phase 2 — Project Milestone Chronology

| # | Milestone | Evidence | Result | Push/Sync/Runtime |
|---|---|---|---|---|
| A | Model 3B-CD V1 (Hawkes simulator) | 10 commits `a8df8c2`→`5bd1f9f`, 2026-08-23/24 | **FAILED** (`SIMULATION_RECOVERY_FAILED`) | PUSHED, SERVER_SYNCED_NOT_RUNTIME |
| B | Provenance audit (Phase B, 141/141 events) | `MODEL_3B_EVENT_SOURCE_PROVENANCE_AUDIT.md` (untracked) | Executed, complete | Doc: LOCAL_ONLY. **Derived JSON artifact: RUNTIME_DEPLOYED + PUBLICLY_ACCESSIBLE** (`/api/forts/power-status`) |
| C | Interpretive modeling (resistance/patron-client/Barus I1) | `cd_resistance_signal_candidates.csv`, Barus dossier (`b637028`) | Barus I1 committed; Indrapura I2 not started | Barus: PUSHED, not runtime-consumed. Resistance CSV/79-row ledger: LOCAL_ONLY |
| D | Ontology Draft V2 | `ba1155c`, checksum unchanged | Frozen baseline | PUSHED, SERVER_SYNCED_NOT_RUNTIME |
| E | Painan relational prototype | `25ec3d2` | 30/30 PASS | PUSHED, SERVER_SYNCED, no route → VALIDATED_NONPRODUCTION |
| F | Natal V1 | `d78bd63` | 28/28 PASS | PUSHED, VALIDATED_NONPRODUCTION |
| G | Koto Tangah V2 | `099e936` + fix `1fd419a` | 34/34 PASS | PUSHED, VALIDATED_NONPRODUCTION |
| H | Tiku V3 | `d901a32` | 35/35 PASS | PUSHED, VALIDATED_NONPRODUCTION |
| I | Sillida V4 | `55812cb` | 32/32 PASS | PUSHED, VALIDATED_NONPRODUCTION |
| J | Cross-case failure synthesis | `e56102f` | 10 failures, 7 clusters, 8 changes, 10 tests, 18 decisions queued | PUSHED, SERVER_SYNCED_NOT_RUNTIME |
| K | Researcher adjudication | `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` (uncommitted working diff) | 5 decided (01/04/09/10/14), 13 PENDING | **Local-only, uncommitted**, fingerprint verified unchanged |
| L | PRD | `51b0bd9` | Long-term power-relations PRD | PUSHED, documentation-only |
| M | SEC-0 → SEC-3D | `38120d2` → SEC-3D docs (untracked) | All disposable, no production auth applied | PUSHED where frozen; live routes confirm **no Basic Auth active** |
| N | Route-boundary adjudication | `cfd715b` | Confirmed both `/atlas/` and `/westkust/` are real production aliases | PUSHED |
| O | `/westkust/` retirement planning | `15178c9`, `64b0d59` | 6 decisions recorded, execution `NOT_AUTHORIZED` | PUSHED; **no redirect live** (confirmed both prefixes return 200 directly) |
| P | CARTO diagnosis + remediation | `1bd9692` | Fix applied, key rotation pending | PUSHED, server-synced, **RUNTIME_DEPLOYED (WORKING_FIX, key pending rotation)** |
| Q | Production deployments | container rebuild 2026-08-28 08:19 UTC | frontend+backend rebuilt for CARTO fix; nginx/db/redis untouched (uptime unchanged) | confirmed via `docker ps` |

---

## Phase 3 — Mathematical and Statistical Model Inventory

Two distinct efforts exist under the "Model 3B" name — **do not conflate them**:

**Effort 1 — Model 3B-CD V1 (Hawkes-process density+excitation), simulation-recovery arm.** 10 tracked commits, PUSHED, SERVER_SYNCED_NOT_RUNTIME. Simulator code: `docs/thesis/colab/model3b_cd_simulator/`. Working results: `data/model3b_working/` (gitignored, LOCAL_ONLY).

**Effort 2 — Post-V1 postmortem/alternative-test phases (A–D).** Entirely **untracked**, despite being fully executed with real results (the entire `docs/thesis/` tree is gitignored).

| Item | Status | Evidence |
|---|---|---|
| Model 3B V1 | `FAILED` (`SIMULATION_RECOVERY_FAILED`) | `MODEL_3B_CD_FINAL_1000_RECOVERY_AUDIT.md` |
| Simulation-recovery test | `FAILED` | same |
| Postmortem Phase A | `EXECUTED_NONPRODUCTION`, LOCAL_ONLY | `MODEL_3B_CD_V1_POSTMORTEM.md` |
| Provenance audit Phase B | Doc: `EXECUTED_NONPRODUCTION`. **Derived artifact: RUNTIME_DEPLOYED + PUBLICLY_ACCESSIBLE** | `backend/routers/forts.py` loads `provenance_artifact.json` at import time; live-verified `GET /api/forts/power-status` returns real provenance objects |
| Leave-source-out Phase C | `EXECUTED_NONPRODUCTION`, LOCAL_ONLY, `PARTIALLY_FEASIBLE` | `MODEL_3B_LEAVE_SOURCE_OUT_FEASIBILITY.md` |
| Parent-episode feasibility | `EXECUTED_NONPRODUCTION`, LOCAL_ONLY, `PARTIALLY_FEASIBLE` | `MODEL_3B_PARENT_EPISODE_CONCENTRATION_REVIEW.md` |
| Phase D conditional clustering | **Actually executed**, not just prespecified | `MODEL_3B_CONDITIONAL_CLUSTERING_TEST_PLAN.md` + `_AUDIT.md` |
| FULL/LSO-A/LSO-B × event-level/episode-earliest/episode-latest | 9/9 arms complete | same |
| Primary 90-day event-pair statistic | Documented, applied | plan §1/§3 |
| Simulations per arm | **10,000/arm, 90,000 total** (read from result table, not a target) | audit §4 |
| Holm-Bonferroni | Applied across 9 p-values; smallest raw p 0.2486 vs. 0.05/9≈0.0056 | audit §5 |
| Result | 9/9 arms `RESIDUAL_CLUSTERING_NOT_SUPPORTED` | audit |
| Model V2 | `PLANNED_ONLY`, `NOT_AUTHORIZED` | postmortem plan |

**Formulas (verbatim from source):**
```
lambda0(t) = exp(theta0 + theta1 * standardized_log1p(CD_t))
standardized_log1p(CD_t) = (log1p(CD_t) - mean(log1p(CD_t))) / sd(log1p(CD_t))
w(Y) = exp(theta1_arm * standardized_log1p(CD_Y))
branching_ratio = alpha / beta
```
No Hawkes compensator/kernel formula was found restated at doc level (lives in `gamma_cluster_simulator.py` code, not opened line-by-line this pass).

**Runtime consumption check:** `grep -rli model3b backend/ frontend/` finds only a documentation citation in a code comment — **the statistical model itself is never loaded by any running service.** Only the Phase-B provenance-audit *byproduct* is runtime-deployed (see table above) — this is the one item in this entire audit where a "failed model's" research byproduct made it into production while the model itself did not.

---

## Phase 4 — Interpretive Model Inventory

**Cross-phase flag:** "game theory" refers to two unrelated things — do not conflate:
- **Model 6 / `game_theory_h2_reaffirmation.json`** — quantitative, payoff = revealed preference from Model 2's E[dwell]. **RUNTIME_DEPLOYED + PUBLICLY_ACCESSIBLE** via `backend/build_bokeh_dashboard.py` → `backend/routers/research.py:589` → `views.py:159` → `riset_pemodelan.html`. Confirmed live at `https://silida.org/atlas/riset/pemodelan/` (renders "Game Theory"/"h2" content).
- **Painan/Barus/Indrapura qualitative power-theory work** — this phase's actual subject, entirely separate, no runtime consumer.

| Artifact | Path | Rows | Tracked | Runtime | Public |
|---|---|---|---|---|---|
| Resistance-signal candidates (LLM, unreviewed — `dicek_kalibrasi_manual=False`) | `docs/cd_resistance_signal_candidates.csv` | 20 | untracked | none | no |
| Colonial-category/resistance interpretive ledger | `docs/thesis/colab/MODEL_3B_COLONIAL_CATEGORY_AND_RESISTANCE_INTERPRETIVE_WORKING.csv` | **79 data rows** (resolved — see note) | untracked, gitignored | none | no |
| Barus episode dossier (I1) | `docs/thesis/pilot_annotation/BARUS_EPISODE_DOSSIER_DRAFT.md` | 179 lines | **committed** `b637028` | none | no |
| Indrapura episode dossier (I2) | — | — | **does not exist** | — | — |
| 5 relational validation artifacts | `data/power_relations/*.json` | — | tracked, server-synced | none in runtime | no |

**Row-count note (resolved this turn):** two forks disagreed (79 vs. 83) on the interpretive ledger's row count. Independently re-verified: the file has 84 physical lines, of which 4 are `#`-comment/blank lines that `csv.reader` (without comment-skipping) mis-parses as data rows if only the first row is excluded. Correct count, matching both the Phase-4 fork's finding and the validator's own hardcoded `LOCAL_ONLY_LEDGER_EXPECTED_ROWS=79` (`validate_sillida_relational_artifact.py:70`): **79 data rows.**

**Verification answers:**
- **I2 Indrapura:** not started — only appears as a planned batch label, no dossier/commit exists.
- **79-row ledger:** confirmed local-only, never committed (`git ls-files` — no match).
- **Public rendering of theory annotations:** none — zero matches for `patron_client`/`resistance_candidate`/`colonial_category`/`power_relations` in any runtime file.
- **Resistance/patron-client as factual graph edges:** **explicitly and deliberately no.** Every relational artifact's `vocabulary_notes.relation_type_restraint` states no `RESISTS`/`PATRON_OF`/`CLIENT_OF`/etc. relation type was ever created; `patron_client_classification` exists only as an annotation qualifier (`PATRON_CLIENT_NOT_TESTABLE`/`CONTESTED`), never an edge type.
- **Arbitrary payoff/equilibrium claims:** none found; explicitly prohibited by the governing instructions doc, and Model 6's one real payoff is labeled "revealed preference... BUKAN payoff riil semua pihak," explicitly barred from being used as evidence for historical claims (Barus dossier).

**Safeguards:** all 5 stated safeguards (analytical lens only / no arbitrary payoff / no perfect-rationality assumption / no unsupported equilibrium claim / resistance-patron-client remain annotations) — **PASS**, with one flagged caveat that Model 6's data-derived (not arbitrary) payoff is a live, real number in a public dashboard, which is a different category of claim than the qualitative interpretive work this phase covers.

---

## Phase 5 — Ontology State Inventory

| Item | File | Commit | Current verified count |
|---|---|---|---|
| Draft V2 | `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` | `ba1155c` | checksum unchanged, no runtime consumer |
| Painan artifact | — | `23da0cc` | **23/23 PASS** |
| Painan prototype | — | `25ec3d2` | **30/30 PASS** |
| Natal V1 | — | `d78bd63` | **28/28 PASS** |
| Koto Tangah V2 | — | `099e936`+`1fd419a` | **34/34 PASS** |
| Tiku V3 | — | `d901a32` | **35/35 PASS** |
| Sillida V4 | — | `55812cb` | **32/32 PASS** |
| Failure inventory | `POST_V1_V4_ONTOLOGY_FAILURE_INVENTORY.csv` | `e56102f` | **10 failures** |
| Failure clusters | `POST_V1_V4_ONTOLOGY_FAILURE_CLUSTERS.csv` | `e56102f` | **7 clusters** |
| Changeset ledger | `ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CHANGESET_LEDGER.csv` | `e56102f` | **8 changes** |
| Revalidation matrix | `ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv` | `e56102f` | **10 tests** |
| Generalized validator | `ATLAS_POWER_RELATION_V2_1_GENERALIZED_VALIDATOR_PLAN.md` | `e56102f` | **`PLANNED_ONLY`** — no executable script exists anywhere |
| PRD | `PRD_ATLAS_POWER_RELATIONS_LONG_TERM_SCALE.md` (+2 companions) | `51b0bd9` | pushed, documentation-only; untracked root copy is a byte-identical stray duplicate |
| Draft V2.1 | referenced only inside the uncommitted decision ledger's DEC-14 | not committed | package "BALANCED" selected but **implementation/migration/Graphify explicitly NOT_AUTHORIZED** |
| Graphify | `graphify-out/graph.json` (9MB, 2026-08-24), `docs/graphify-out/graph.json` (254KB, 2026-07-23) | untracked | `grep -rn graphify backend/ frontend/` = **zero matches — NOT DEPLOYED**, confirmed no consumer exists at all |

**Untracked-file clarification (important, resolves an apparent duplication):** `POST_V1_V4_ONTOLOGY_FAILURE_SYNTHESIS.md`, `POST_V1_V4_ONTOLOGY_FAILURE_SYNTHESIS_AND_V2_1_CHANGESET_PLAN.md`, `CROSS_CASE_POWER_ONTOLOGY_REVIEW_PLAN.md`, `ATLAS_PAINAN_1663_LOCAL_RELATIONAL_RESEARCH_PROTOTYPE_PLAN.md` are all **instruction/prompt documents** used to commission the real (committed) outputs — not competing or superseding results. `PRD_ATLAS_POWER_RELATIONS_LONG_TERM_SCALE.md` (root, untracked) is the one exception — it's a harmless byte-identical stray copy of the real committed PRD.

**Researcher decision ledger (uncommitted, verified this turn):** fingerprint `d2805d16...4155014` unchanged. Committed baseline (`e56102f`): 18/18 `PENDING`. Current uncommitted working tree: **5 decided** (DEC-01/04/09/10 `APPROVED_WITH_LIMITATIONS`, DEC-14 `DRAFT_V2_1`), **13 still PENDING**. Matches memory's "5 blocking: 01/04/09/10/14" claim exactly — no discrepancy.

---

## Phase 6 — Validator Inventory

All six ontology validators, re-run **read-only, both locally and confirmed matching on the server** this session (and again independently this turn, locally):

```text
Painan artifact:    23/23 PASS
Painan prototype:   30/30 PASS
Natal:              28/28 PASS
Koto Tangah:        34/34 PASS
Tiku:               35/35 PASS
Sillida:            32/32 PASS
```
None run any runtime/production role — all are local CLI scripts under `scripts/research_validators/`, invoked manually, not imported by any service.

**Generalized validator:** confirmed `PLANNED_ONLY` (Phase 5) — a plan document exists, no executable implementation found anywhere in the repository.

**Statistical/provenance validators, security test matrices:** covered in Phase 3 (Model 3B has no dedicated automated validator, only manual audit docs) and in the SEC-2 through SEC-3D/CARTO test matrices already extensively documented this session under `docs/security/`.

---

## Phase 7 — Prototype Inventory

| Prototype | Path | Classification |
|---|---|---|
| Painan relational research prototype | `research_prototypes/painan_1663_relational/` | COMMITTED (`25ec3d2`), PUSHED, SERVER_SYNCED, VALIDATED_NONPRODUCTION — **no route, no nav link, not PUBLICLY_ACCESSIBLE** |
| Natal/Koto Tangah/Tiku/Sillida prototypes | — | **do not exist** — only Painan has an interactive prototype; the others have artifacts+validators only |
| Multi-case/cross-case prototype | `CROSS_CASE_POWER_ONTOLOGY_REVIEW_PLAN.md` | **LOCAL_ONLY**, planning document only, explicitly states "no production integration authorized" |
| Bokeh modeling dashboard (`/riset/pemodelan/`) | commit `814ddc7` | **RUNTIME_DEPLOYED, PUBLICLY_ACCESSIBLE** — live-verified real Bokeh chart markup rendered, not just a 200 shell |
| Security disposable prototypes (SEC-2A–3D) | `docs/security/*.md` | VALIDATED_NONPRODUCTION / SUPERSEDED — confirmed via live check: **no Basic Auth challenge on any route** |
| Route redirect prototype (`/westkust/`→`/atlas/`) | `15178c9` | COMMITTED, PUSHED, SERVER_SYNCED, VALIDATED_NONPRODUCTION — **live-confirmed no redirect exists**, both prefixes independently 200 |
| CARTO basemap remediation | `1bd9692` | **RUNTIME_DEPLOYED — flagged WORKING_FIX_PENDING_KEY_ROTATION**, not a stable RUNTIME_DEPLOYED_FIX |

---

## Phase 8 — Production Runtime Inventory

```text
Running commit (all environments): 1bd96926000fb03cb1e816f7ba4ba4af1b1c7a20

Containers:
  voc_db       postgis/postgis:15-3.3   Up 2 months (healthy)   unchanged
  voc_redis    redis:7-alpine           Up 7 weeks (healthy)    unchanged
  voc_nginx    nginx:1.25-alpine        Up 6 weeks              unchanged, port 8084 unchanged
  voc_backend  westkust-routes-backend  Up ~7 min (rebuilt for CARTO fix)
  voc_frontend westkust-routes-frontend Up ~7 min (rebuilt for CARTO fix)

Migrations applied (Alembic, 12 total): 001–012, covering fort_historis_amh,
  commodity_glossary, amh_images, voyage_source, port_arrival_tallies,
  glossary_source_citation, research_theme_rows, atjeh_trade_source_document,
  linimasa_events, linimasa_era_slug, linimasa_power_status, fort_model_metrics

Database tables (public schema): alembic_version, api_keys,
  atjeh_trade_records, cargo_items, commodity_glossary, fort_model_metrics,
  forts, linimasa_events, port_arrival_tallies, research_theme_rows,
  staging_extractions, voyages
  -- NO table for Model 3B/statistical results, NO table for ontology V1-V4
     artifacts. Confirms both are not database-backed in production.
```

**Route test matrix (all live-tested this turn):**

| Route | Status | Content-Type | Auth required |
|---|---|---|---|
| `/atlas/` | 200 | text/html | no |
| `/westkust/` | 200 | text/html | no |
| `/atlas/linimasa/` | 200 | text/html | no |
| `/westkust/linimasa/` | 200 | text/html | no |
| `/atlas/riset/pemodelan/` | 200 | text/html | no |
| `/westkust/riset/pemodelan/` | 200 | text/html | no |
| `/atlas/riset/pemodelan/panduan/` | 200 | text/html | no |
| `/westkust/riset/pemodelan/panduan/` | 200 | text/html | no |
| `/api/research/linimasa` | 200 | application/json | no |
| `/api/research/pemodelan-dashboard` | 200 | application/json | no |

No credentials, cookies, or sensitive body content captured — status codes and content-type only.

---

## Phase 9 — Deployed Truth Table

```text
Model 3B-CD V1 (Hawkes statistical model):
  PUSHED_REMOTE (simulator code) / SERVER_SYNCED_NOT_RUNTIME -- FAILED, not consumed anywhere

Model 3B Phase B provenance-audit derived JSON:
  RUNTIME_DEPLOYED + PUBLICLY_ACCESSIBLE (/api/forts/power-status)
  -- the one case where a "failed" research thread's byproduct reached production

Model 3B Phases A/C/D (postmortem, LSO, conditional clustering):
  EXECUTED_NONPRODUCTION, LOCAL_ONLY (gitignored docs/thesis/ tree) --
  never pushed, never on server, never runtime-consumed

Model 6 game-theory (quantitative, revealed-preference payoff):
  RUNTIME_DEPLOYED + PUBLICLY_ACCESSIBLE (/atlas/riset/pemodelan/) --
  DO NOT confuse with the qualitative Painan/Barus game-theory interpretive
  work, which is not deployed

Interpretive work (resistance/patron-client/colonial-category, Barus I1):
  LOCAL_ONLY or COMMITTED-but-not-runtime-consumed -- annotations only, never
  promoted to factual graph edges (deliberately, per explicit vocabulary
  restraint rules)

Draft V2 / V1-V4 ontology artifacts / PRD / SEC-0-3D evidence:
  PUSHED_REMOTE, SERVER_SYNCED_NOT_RUNTIME -- documentation/validation
  evidence, no runtime consumer, matches the researcher's own expected
  pattern exactly

Painan prototype:
  VALIDATED_NONPRODUCTION -- no route serves it, confirmed not
  PUBLICLY_ACCESSIBLE

Bokeh modeling dashboard (/riset/pemodelan/):
  RUNTIME_DEPLOYED + PUBLICLY_ACCESSIBLE -- confirmed via live chart markup,
  not just a 200 status

Graphify:
  NOT_DEPLOYED -- zero consumers found anywhere in backend/frontend code,
  confirmed per the researcher's own stated rule

/westkust/ retirement redirect:
  NOT_IMPLEMENTED -- both prefixes independently live, no redirect exists

CARTO basemap fix:
  RUNTIME_DEPLOYED as a WORKING_FIX, key rotation pending -- not yet a
  stable closed remediation

Basic Auth / SEC-2A-3D access control:
  NOT_IMPLEMENTED -- confirmed live, no auth challenge on any tested route;
  SECURITY_ACCESS_CONTROL_GATE remains NOT_PASSED
```

---

## What Remains Pending / Blocked / Deferred

```text
- Ontology decision ledger: 13/18 decisions still PENDING (uncommitted, local-only)
- Draft V2.1: package selected but NOT_AUTHORIZED for implementation/migration/Graphify
- Generalized validator: PLANNED_ONLY, no implementation
- I2 Indrapura interpretive dossier: not started
- 79-row colonial-category/resistance ledger: local-only, uncommitted
- cd_resistance_signal_candidates.csv: LLM-classified, unreviewed (dicek_kalibrasi_manual=False)
- Model 3B V2: PLANNED_ONLY, NOT_AUTHORIZED, not started
- /westkust/ redirect: 6 decisions recorded, execution NOT_AUTHORIZED
- Basic Auth: still not implemented anywhere in production
- CARTO fix: WORKING_FIX only -- key rotation pending, not a closed remediation
- SEC3-F-02 (numeric rate-limit closure): still open, blocked pending a
  genuinely different host
- Graphify: built locally, zero runtime consumers, not deployed
```

---

## Final Status

```text
COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT_COMPLETE
```

Read-only throughout. No file edited, no CARTO file touched, nothing staged/committed/pushed. Ontology decision-ledger working diff (`d2805d16...4155014`) verified unchanged at both the start and end of this audit.
