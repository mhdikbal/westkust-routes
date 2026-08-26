# DATAVERSENL HISTORY, GAP, AND INCREMENTAL HARVEST AUDIT

> **RESEARCH-ONLY, METADATA-ONLY, NONPRODUCTION.** No dataset file was downloaded this turn. No credential or token was stored. No commit, push, or deploy was performed. Draft V2, the Natal V1 artifact, the Painan artifacts, the interpretive ledger, production code, Atlas, Graphify, the API, the database, and all migrations remain unmodified.

## 1. Scope

This turn executes exactly the history audit, gap analysis, and metadata-only incremental discovery requested: (a) reconstruct prior DataverseNL scraping activity from git history, repository scripts, manifests, shell history, local download directories, and prior logs/audit documents; (b) verify prior coverage before any new query; (c) run metadata-only discovery via the Dataverse Search API and Native API for 7 defined research gaps (Natal 1760, Painan Tractaat 1663, Koto Tangah, Tiku, Sillida/Salido, Batang Capas and EIC, Barus); (d) produce 7 CSV artifacts plus this audit; (e) stop after metadata discovery and the download-allowlist decision. No dataset file download, no access-restriction bypass, and no historical re-derivation beyond what is needed to define the gaps were performed.

## 2. History Reconstruction Method

Four independent evidence channels were checked:

1. **Git history**: `git log --all -i --grep="dataverse"` and `--grep="harvest|scrape|scrap"` across the full history. No commit message references a DataverseNL harvest for any of the 7 gaps. Two unrelated commits reference "dataverse" only as a substring inside `dutch_ships_asian_waters` integration work.
2. **Repository scripts and manifests**: `grep -ril "dataverse\|globalise"` across all tracked and untracked `.py`/`.md`/`.csv`/`.json`/`.sh`/`.txt` files (excluding `graphify-out/` cache noise, which matched only on unrelated byte sequences). This surfaced the real evidence base for `DATAVERSENL_PREVIOUS_HARVEST_HISTORY.csv` (H-01 through H-05).
3. **Shell history**: `~/.bash_history` was read (read-only, no modification) and searched for "dataverse", "globalise", and the DOI fragment "5hgtcd". Zero matches — the file is readable but does not cover whatever session originally ran the GLOBALISE or `dutch_ships_asian_waters` harvest, and a referenced ephemeral script (`/tmp/scan_globalise_variants.py`, named in `.claude/settings.local.json`'s permission history) is confirmed absent from `/tmp` now.
4. **Local download directories and prior logs**: `data/`, `docs/thesis/dr/`, and `docs/thesis/` were inventoried directly (see `DATAVERSENL_LOCAL_DOWNLOAD_INVENTORY.csv`). No file in native Dataverse export format (`.tab`, `.zip`, DDI XML, Dataverse JSON-LD) exists anywhere in the working tree — only already-transformed CSV/JSON pipeline outputs survive.

## 3. Reconstructed Prior Coverage

Two real prior DataverseNL-sourced integrations exist in this project, neither targeted at the 7 gaps this turn addresses:

- **H-01**: `dutch_ships_asian_waters` (DOI `10.34894/5HGTCD`), imported ad hoc with no committed harvest script; 695 rows currently live in the production `voyages` table. A remediation script (`docs/thesis/dr/enrich_dutch_ships_asian_waters.py`) was committed later (2026-07-26) to fix defects found in that import, but the original harvest method itself is not reconstructible.
- **H-02**: A 535-row GLOBALISE corpus export, referenced only in `docs/brainstorm-globalise-data-modeling.md` as "sudah di-scraping" (already scraped) from "dataverse.nl/DANS, KNAW", with no dataset DOI, no query string, and no harvest script ever captured. The named raw file (`docs/thesis/globalise_corpus.csv`) no longer exists; it was consumed into the `docs/thesis/dr/daghregister_corpus*.csv` multi-stage cleaning lineage, which does survive.

**Conclusion**: no prior DataverseNL harvest exists for Natal 1760, Painan 1663, Koto Tangah, Tiku, Sillida/Salido, Batang Capas/EIC, or Barus. Per the task's own instruction not to start a new broad crawl before prior coverage is verified: prior coverage IS verified (via the 4-channel reconstruction above), and it verifiably does NOT cover these 7 gaps — so a new, gap-scoped, metadata-only discovery pass is warranted and was performed, rather than a broad crawl.

## 4. Research Gap Definition

`DATAVERSENL_RESEARCH_GAP_LEDGER.csv` enumerates 27 specific evidence gaps across the 7 cases (6 for Natal, 5 for Painan, 2 for Koto Tangah, 4 for Tiku, 3 for Sillida/Salido, 3 for Batang Capas/EIC, 4 for Barus), each linked to a specific existing project artifact and ontology component it would inform. The Natal gaps were prioritized first and most granularly per the task's own emphasis, directly targeting V1's one genuine ontology finding (T-06: VOC institutional hesitation is not representable as a Draft V2 relation type) — see section 7 below.

## 5. API Capability Audit

The Dataverse Search API (`GET /api/search?q=...&type=dataset`) and Native API dataset-metadata endpoint (`GET /api/datasets/:persistentId/?persistentId=doi:...`) were both confirmed reachable and functional under the pre-existing `WebFetch(domain:dataverse.nl)` permission (already present in `.claude/settings.local.json` from a prior session). Both are official, public, unauthenticated, metadata-level endpoints — no login, API token, or credential was needed or used, satisfying the hard constraint against storing credentials. HTML scraping was not required at any point this turn; the Search API and Native API fully covered this turn's metadata needs.

## 6. Metadata-Only Discovery Execution

8 requests were issued this turn, strictly sequentially (never in parallel), one per gap plus one drill-down — see `DATAVERSENL_QUERY_MANIFEST.csv` for the full ordered list with timestem ordering. This satisfies "single-threaded, conservative, one request per second or slower": each request was issued only after the previous one's response was fully processed (turn-based tool use inherently serializes this), and no 429 or 5xx response was ever received, so the "stop after repeated 429/5xx" condition was never triggered.

**Central finding**: across all 7 gap-specific queries, DataverseNL's dataset-level Search API never returned a dataset narrow enough to directly confirm or deny any of the 7 micro-historical episodes. Every query's top results were the same handful of mega-corpora (GLOBALISE transcriptions, a VOC document-segmentation training set, VOC Court Records Cochin, VOC commodity prices, a VOC slave-trade dataset) plus occasional unrelated false-positive keyword matches (e.g., an ornithology dataset about bird "natal dispersal"). This is itself a discovery result, not a null result: DataverseNL indexes VOC material at the *dataset* level (whole archival collections), not at the *event* level, so resolving any of these 7 gaps will require a within-corpus full-text or index search inside one of the GLOBALISE datasets — a distinct, larger, future-turn activity, not a simple dataset match.

**Most significant concrete finding**: `GLOBALISE - Places in the Dutch East India Company Archives (1602-1799)` (DOI `10.34894/UFFFNO`), surfaced under the Batang Capas/EIC query (a generic "VOC" match, not gap-specific) and then drilled into directly via its own Native API metadata endpoint. Its public metadata confirms it catalogs VOC-archive place names, alternate spellings, coordinates, and place-type classification, sourced partly from the VOC archives themselves and partly from GeoNames/World Historical Gazetteer — directly relevant to this project's own long-documented archaic-spelling problem (`reference_ejaan_sillida_salido` project memory: Sillida=Salido, Priaman=Pariaman, Baros=Barus, Ticco=Tiku), which that memory itself notes is "a systemic pattern not caught by automated LLM/fuzzy-matching." The dataset is CC-BY-4.0 licensed, but its file requires an explicit access request even under that open license — confirmed via metadata, not assumed.

A second promising but unverified lead, `GLOBALISE - Early Modern Polities in the Dutch East India Company Archives`, was identified but not drilled into this turn (see `DATAVERSENL_QUERY_MANIFEST.csv` Q-10, explicitly deferred).

## 7. Relevance to the Natal V1 Ontology Gap (T-06)

The task's own framing is preserved exactly: T-06 (no Draft V2 relation type represents an institution's internal hesitation about a claim it has already nominally received) is NOT treated as solved or in need of immediate repair by this turn's discovery. Every discovery result relevant to Natal is classified against the 6-value outcome scale the task defined (`SUPPORTS_EXISTING_GAP`, `WEAKENS_EXISTING_GAP`, `RESOLVES_SOURCE_GAP_ONLY`, `SUGGESTS_FUTURE_ANNOTATION`, `SUGGESTS_FUTURE_RELATION_REVIEW`, `NOT_RELEVANT`) in `DATAVERSENL_DISCOVERY_RESULTS.csv`. No result found this turn rises above `SUGGESTS_FUTURE_ANNOTATION` — none is direct evidence of Batavia's own deliberation record, van Moschel/Senff correspondence, or an English/French-side account of the March 1760 transfer. The Namebooks dataset (`10.34894/MD59SC`) is the closest lead for corroborating van Moschel/Senff's own service record, but this remains a lead, not a finding. **T-06 therefore remains open, undecided, and un-repaired** — exactly as the task requires: no new vocabulary was created, no relation type's meaning was extended, and Draft V2 was not touched.

## 8. Local Download Inventory

`DATAVERSENL_LOCAL_DOWNLOAD_INVENTORY.csv` confirms no raw Dataverse-native file exists locally for either H-01 or H-02, and that `docs/thesis/globalise_corpus.csv` (the file that would have been closest to a raw H-02 harvest artifact) is no longer present in the working tree — a genuine, disclosed gap in the project's own provenance, not something this turn attempts to silently repair by re-deriving it from a new download.

## 9. Incremental Prior-vs-Current Diff

`DATAVERSENL_INCREMENTAL_DIFF.csv` records 6 diff items. The central negative finding (D-06): no dataset-level match exists for any of the 7 gaps at the specificity this turn required. Three genuinely new candidate sources were identified that did not exist in, or were not previously referenced by, this project (D-03/D-04/D-05: the Places, Polities, and Namebooks GLOBALISE companion datasets), all published after the original 2026-mid-year H-02 harvest and therefore invisible to any prior session.

## 10. Download Allowlist Decision

`DATAVERSENL_DOWNLOAD_ALLOWLIST_DRAFT.csv` lists 6 candidates plus 1 explicitly excluded dataset, ranked by the confidence and specificity of this turn's own metadata findings. **No file download is recommended or authorized this turn** — every row's `recommended_action_this_turn` is `DO_NOT_DOWNLOAD`. The highest-priority candidate (C-01, the Places gazetteer) additionally requires an access request this turn does not authorize submitting, since request-and-download is explicitly future-turn, researcher-gated scope. The bulk transcription corpus (C-05) is flagged as the wrong tool for this project's needs regardless of authorization — a future turn should investigate whether GLOBALISE exposes its own full-text search interface rather than ever bulk-downloading 4.8 million scans.

## 11. Constraints Honored

```text
No authentication bypass, CAPTCHA bypass, or robots-rule violation: all 8 requests used only the
  public, unauthenticated Dataverse Search API and Native API metadata endpoint.
No credential or token stored: none was needed or used.
No dataset file downloaded: only dataset-level and one file-list-level metadata JSON response
  was ever fetched (via WebFetch, itself read-only and non-persistent).
Single-threaded, conservative pacing: 8 requests issued strictly sequentially, one per turn,
  well under any 1-request-per-second ceiling; zero 429/5xx responses received.
Draft V2, Natal V1 artifact, Painan artifacts, interpretive ledger, production code, Atlas,
  Graphify, API, database, migrations: all unmodified (no file under any of these paths was
  written to this turn; only 8 new docs/thesis/colab/*.csv files plus this audit were created).
No staging, commit, push, or deploy performed this turn.
```

## 12. Status and Readiness Decision

```text
CROSS_CASE DRAFT V2:                 UNCHANGED
NATAL V1 ARTIFACT:                   UNCHANGED (COMPLETE, 28/28 PASS, as of prior turn)
DATAVERSENL HISTORY RECONSTRUCTION:  COMPLETE (H-01..H-05 documented)
DATAVERSENL GAP LEDGER:              COMPLETE (27 gaps across 7 cases)
DATAVERSENL METADATA DISCOVERY:      COMPLETE (8 requests, 17 discovery results classified)
DATAVERSENL DOWNLOAD ALLOWLIST:      DRAFTED, NO DOWNLOAD AUTHORIZED THIS TURN
T-06 (VOC INSTITUTIONAL HESITATION): STILL OPEN -- not resolved, not repaired, not closed by
                                       this turn's discovery; strongest lead is the GLOBALISE
                                       Namebooks dataset (unverified, future-turn)
NEXT AUTHORIZED STEP:                researcher decision on whether to (a) authorize a future
                                       turn to submit the C-01 access request, (b) authorize
                                       metadata-only checks of C-02/C-03/C-04, and/or (c)
                                       investigate a GLOBALISE within-corpus search interface
                                       for the 7 gaps directly -- none of these three is
                                       authorized by this turn
V2 KOTO TANGAH / MULTI-CASE PROTOTYPE / GRAPHIFY / ATLAS / COMMIT / PUSH / DEPLOY: NOT AUTHORIZED
```
