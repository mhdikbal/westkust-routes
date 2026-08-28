#!/usr/bin/env python3
"""Read-only validator for the multi-case power-relation research prototype.

NONPRODUCTION TOOL. Checks the prototype's static source
(research_prototypes/multi_case_power_relations/{index.html,prototype.js,prototype.css})
against a checklist generalizing the Painan prototype's own 30-item checklist
(ATLAS_PAINAN_1663_LOCAL_RELATIONAL_RESEARCH_PROTOTYPE_PLAN.md SS13) across 5 cases, plus the
2 multi-case-specific checks named in CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md SS5:
closed relation-type vocabulary and an actor-ID cross-case namespace diagnostic.

Performs no writes, no network calls, no API/database/Graphify access, and imports nothing
from backend/ or frontend/.

Usage: python3 scripts/research_validators/validate_multi_case_power_relations_prototype.py
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROTO_DIR = REPO / "research_prototypes/multi_case_power_relations"
MIGRATED_DIR = REPO / "data/power_relations/migrated_v2_1"
GENERALIZED_VALIDATOR = REPO / "scripts/research_validators/validate_power_relation_ontology.py"

CASE_FILES = {
    "painan": "painan_1663_relational_research_artifact_v2_1_migrated.json",
    "natal": "natal_1760_relational_validation_artifact_v2_1_migrated.json",
    "kototangah": "koto_tangah_destruction_cycle_relational_validation_artifact_v2_1_migrated.json",
    "tiku": "tiku_1625_1740_relational_validation_artifact_v2_1_migrated.json",
    "sillida": "sillida_resource_governance_relational_validation_artifact_v2_1_migrated.json",
}
# Recorded by the migration-phase audit (ATLAS_POWER_RELATION_V2_1_ARTIFACT_MIGRATION_AUDIT.md SS10);
# re-verified here as this prototype's own chain-of-custody continuity check.
EXPECTED_SHA256 = {
    "painan": "af6ba01972f038f9b9bca9515f59db78f9e1e7b84dd2ba566f32b9c2af562bdc",
    "natal": "5b32aaabd38425103869dbb1d5c04e8924a4974df2f677bebdbb720e4734e873",
    "kototangah": "a57b20bd80d49ae44f5df1b5569800a106648815ba3ad208c00e048f4d1e7a7d",
    "tiku": "04da257f4153933a5fd0990ccf9cb49a8980410239ceefbfaf84c52bf554854b",
    "sillida": "c43f986530625f8996d60076cf68973018e4dca476904a5195e63ddeae4c65f8",
}

# Mirrors scripts/research_validators/power_relation_ontology_rules.json's own
# closed_relation_vocabulary (18 values). Must stay in sync with prototype.js's own
# AUTHORIZED_RELATION_TYPES array -- check 8 below verifies that.
AUTHORIZED_RELATION_TYPES = [
    "REQUESTS_PROTECTION_FROM", "PROVIDES_PROTECTION_TO", "REQUIRES_MONOPOLY_FROM", "NEGOTIATES_WITH",
    "RECONCILES_WITH", "SWITCHES_ALIGNMENT_TO", "CLAIMS_JURISDICTION_OVER", "CLAIMS_COMMODITY_MONOPOLY",
    "CONTESTS_SUCCESSION_WITH", "CONTESTS_RESOURCE_WITH", "RECOGNIZES_OFFICE_HOLDER",
    "COLLECTS_TOLL_FROM", "LEASES_RESOURCE_TO", "USES_MILITARY_FORCE_AGAINST",
    "EXERCISES_EFFECTIVE_CONTROL_OVER", "CONTROLS_FORT",
    "MAINTAINS_PARALLEL_ALIGNMENT_WITH", "APPOINTS_OFFICE_HOLDER",
]
FORBIDDEN_RELATION_TYPES = ["PATRON_OF", "CLIENT_OF", "PATRON_CLIENT_RELATION"]


class Report:
    def __init__(self):
        self.results = []

    def check(self, n, label, passed, detail=""):
        self.results.append((n, label, passed, detail))


def read(path):
    return path.read_text(encoding="utf-8")


def main():
    r = Report()

    html_path = PROTO_DIR / "index.html"
    js_path = PROTO_DIR / "prototype.js"
    css_path = PROTO_DIR / "prototype.css"
    readme_path = PROTO_DIR / "README.md"

    if not (html_path.exists() and js_path.exists() and css_path.exists()):
        print("FATAL: prototype files not found under", PROTO_DIR)
        sys.exit(2)

    html = read(html_path)
    js = read(js_path)
    css = read(css_path)
    combined_source = html + "\n" + js + "\n" + css

    # 1. all 5 migrated artifacts exist and checksum-match the migration audit's own recorded values
    checksum_mismatches = []
    case_data = {}
    for case_id, filename in CASE_FILES.items():
        p = MIGRATED_DIR / filename
        if not p.exists():
            checksum_mismatches.append(f"{case_id}: file missing")
            continue
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        if sha != EXPECTED_SHA256[case_id]:
            checksum_mismatches.append(f"{case_id}: got {sha}")
        else:
            case_data[case_id] = json.loads(p.read_text(encoding="utf-8"))
    r.check(1, "all 5 migrated_v2_1 artifacts exist and match the migration audit's recorded checksums",
            not checksum_mismatches, f"mismatches={checksum_mismatches}")

    # 2. generalized validator remains available and produces the expected pass/fail pattern
    # (Painan/Koto Tangah/Sillida PASS; Natal/Tiku FAIL only on pre-existing, disclosed gaps)
    expected_pass = {"painan": True, "natal": False, "kototangah": True, "tiku": False, "sillida": True}
    gv_mismatches = []
    for case_id, filename in CASE_FILES.items():
        proc = subprocess.run([sys.executable, str(GENERALIZED_VALIDATOR), str(MIGRATED_DIR / filename), "--json"],
                               capture_output=True, text=True)
        try:
            data = json.loads(proc.stdout)
            passed = data["passed"]
        except Exception:
            passed = False
        if passed != expected_pass[case_id]:
            gv_mismatches.append(f"{case_id}: expected pass={expected_pass[case_id]}, got {passed}")
    r.check(2, "generalized validator (commit 703634a+) produces the expected PASS/FAIL pattern per case",
            not gv_mismatches, f"mismatches={gv_mismatches}")

    # 3. all 5 cases registered in prototype.js's CASES_DEF
    missing_cases = [c for c in CASE_FILES if f'id: "{c}"' not in js]
    r.check(3, "all 5 cases registered in prototype.js CASES_DEF", not missing_cases, f"missing={missing_cases}")

    # 4. all 5 case fetch paths point only into data/power_relations/migrated_v2_1/ (never the originals)
    fetch_paths = re.findall(r'path:\s*"([^"]+)"', js)
    bad_paths = [p for p in fetch_paths if "migrated_v2_1" not in p or ".." not in p]
    r.check(4, "all 5 case paths are relative and point only into data/power_relations/migrated_v2_1/",
            len(fetch_paths) == 5 and not bad_paths, f"paths={fetch_paths}")

    # 5. case switcher implemented and wired
    r.check(5, "case switcher implemented (setupCaseSwitcher/switchCase) and case-switcher container in HTML",
            "function setupCaseSwitcher" in js and "function switchCase" in js and 'id="case-switcher"' in html)

    # 6. 8 views implemented and wired in HTML nav
    required_views = ["caseindex", "overview", "actors", "timeline", "network", "claimcontrol",
                       "v21additions", "publiccopy"]
    missing_views_html = [v for v in required_views if f'data-view="{v}"' not in html]
    missing_views_js = [v for v in required_views if f'{v}:' not in js]
    r.check(6, "all 8 views present in nav (index.html) and registered in VIEW_RENDERERS (prototype.js)",
            not missing_views_html and not missing_views_js,
            f"missing_html={missing_views_html}, missing_js={missing_views_js}")

    # 7. never merges actors across cases -- CASES keyed per-case, no cross-case actor merge function
    r.check(7, "no cross-case actor-merge function exists; CASES object keeps each case's data separate",
            "let CASES = {}" in js and "function mergeActors" not in js and "function mergeCases" not in js)

    # 8. closed 18-value relation-type vocabulary matches scripts/research_validators/power_relation_ontology_rules.json
    missing_types = [t for t in AUTHORIZED_RELATION_TYPES if t not in js]
    r.check(8, "all 18 authorized relation types (matching the rule registry) referenced in prototype.js",
            not missing_types, f"missing={missing_types}")

    # 9. namespace diagnostic panel present (CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md SS5)
    r.check(9, "cross-case actor_id namespace diagnostic implemented and rendered (SS5 requirement)",
            "function computeNamespaceDiagnostic" in js and "namespace-panel" in js)

    # 10. field-name divergence (object_id vs object_actor_id) handled via a single helper
    r.check(10, "objectIdOf() helper used to normalize object_id/object_actor_id divergence between cases",
            "function objectIdOf" in js and js.count("objectIdOf(") >= 10)

    # 11. V2.1 Additions view never renders CommercialRight/CommandObservation as a graph edge
    network_fn = js[js.find("function renderNetwork"):js.find("function relationDetailPanel")]
    r.check(11, "renderNetwork() never references commercial_rights/command_observations as edges",
            "commercial_rights" not in network_fn and "command_observations" not in network_fn)

    # 12. V2.1 Additions view covers all 4 new entity types
    v21_card_fn = js[js.find("function v21EntityCard"):js.find("function renderV21Additions")]
    v21_fn = js[js.find("function renderV21Additions"):]
    covers_all_four = all(x in v21_fn for x in
        ["commercial_rights", "right_modifications", "command_observations", "operation_participations"])
    r.check(12, "V2.1 Additions view covers all 4 Draft V2.1 entity types", covers_all_four)

    # 13. V2.1 entities always labeled RESEARCH-ONLY, closed by default (disclosureDrawer, not open)
    r.check(13, "V2.1 Additions entities rendered inside closed-by-default disclosure drawers, labeled RESEARCH-ONLY",
            "RESEARCH-ONLY" in v21_fn and "disclosureDrawer" in v21_card_fn and "<details open" not in html)

    # 14. no PATRON_OF/CLIENT_OF edge; renderer guards against it
    forbidden_guarded = "FORBIDDEN_RELATION_TYPES" in js and all(f in js for f in FORBIDDEN_RELATION_TYPES)
    forbidden_in_any_case = any(
        any(rel.get("relation_type") in FORBIDDEN_RELATION_TYPES for rel in d.get("relations", []))
        for d in case_data.values()
    )
    r.check(14, "no PATRON_OF/CLIENT_OF/PATRON_CLIENT_RELATION edge in any case; renderer guards against it",
            forbidden_guarded and not forbidden_in_any_case)

    # 15. no numeric payoff / equilibrium / winner-loser language
    payoff_hits = [t for t in ["payoff", "utility_score", "best_move"] if t.lower() in combined_source.lower()]
    r.check(15, "no numeric payoff / utility_score / best_move token in prototype source", not payoff_hits, f"hits={payoff_hits}")
    equilibrium_hits = re.findall(r"equilibrium", combined_source, re.IGNORECASE)
    r.check(16, "no 'equilibrium' language in prototype source", not equilibrium_hits)
    wl_hits = re.findall(r"\bwinner\b|\bloser\b", combined_source, re.IGNORECASE)
    r.check(17, "no winner/loser label in prototype source", not wl_hits)

    # 18. sovereignty not asserted
    r.check(18, "'sovereignty' not asserted anywhere in prototype source", "sovereignty" not in combined_source.lower())

    # 19. four interpretive layers rendered in visually separate containers
    four_layers = all(x in js for x in
        ["source_statement_summary", "historical_reconstruction", "theoretical_annotation", "public_display_summary"]) \
        and all(x in css for x in [".layer-card.source", ".layer-card.reconstruction", ".layer-card.theory", ".layer-card.public"])
    r.check(19, "four interpretive layers (source/reconstruction/theory/public) rendered in visually separate containers", four_layers)

    # 20. researcher_review_required rendered per relation
    r.check(20, "researcher_review_required rendered per relation", "researcher_review_required" in js)

    # 21. render-time validation errors surfaced, never silently dropped (per case)
    r.check(21, "render-time validation errors collected per case and surfaced in Overview, never silently dropped",
            "renderErrors" in js and "Render-time validation errors" in js)

    # 22. no production imports
    bad_imports = re.findall(r"(?:import|require|src=|href=)\s*['\"](?:/backend|/frontend|\.\./\.\./backend|\.\./\.\./frontend)", combined_source)
    r.check(22, "no import/reference to backend/ or frontend/ from prototype", not bad_imports, f"hits={bad_imports}")

    # 23. exactly 5 real fetch() calls, all targeting the local migrated_v2_1 paths, no /api/ or remote URL
    real_fetch_calls = re.findall(r"fetch\(\s*([A-Za-z_$'\"][^)]*)\)", js)
    remote_fetch_hits = [f for f in real_fetch_calls if re.match(r"""^['"](?:https?:)?//|^['"]/api/""", f)]
    r.check(23, "exactly one fetch() call site (def.path, looped over 5 cases), no /api/ or remote URL",
            len(real_fetch_calls) == 1 and "def.path" in real_fetch_calls[0] and not remote_fetch_hits,
            f"real_fetch_calls={real_fetch_calls}")

    # 24. no database access
    db_hits = re.findall(r"psycopg|sqlalchemy|SELECT\s+\*|pg_connect|postgres", combined_source, re.IGNORECASE)
    r.check(24, "no database-access code/reference in prototype source", not db_hits)

    # 25. no functional Graphify usage
    graphify_functional_hits = re.findall(
        r"graphify\s*\(|require\([^)]*graphify|import[^;]*graphify|graphify-out|graphify_client",
        combined_source, re.IGNORECASE)
    r.check(25, "no FUNCTIONAL Graphify usage (call/import/require/path) in prototype source",
            not graphify_functional_hits, f"hits={graphify_functional_hits}")

    # 26. never references or targets atlas.js or the production frontend index.html template
    references_atlas_js = "atlas.js" in combined_source
    references_production_index = "frontend/map_app/templates/map_app/index.html" in combined_source \
        or "map_app/templates/map_app/index.html" in combined_source
    r.check(26, "prototype never references or targets atlas.js or the production frontend index.html template",
            not references_atlas_js and not references_production_index)

    # 27. keyboard-accessible controls + focus-visible
    uses_native_interactive = "<button" in html or 'el("button"' in js
    has_focus_visible = ":focus-visible" in css
    r.check(27, "keyboard-accessible controls (native buttons/selects/details) and :focus-visible style present",
            uses_native_interactive and has_focus_visible)

    # 28. required status-banner lines present
    banner_lines = ["RESEARCH PROTOTYPE", "NONPRODUCTION",
                     "PAINAN / NATAL / KOTO TANGAH / TIKU / SILLIDA",
                     "NOT CONNECTED TO THE PUBLIC ATLAS, API, DATABASE, OR GRAPHIFY"]
    banners_present = all(b in html for b in banner_lines)
    r.check(28, "all required status-banner lines present in index.html", banners_present)

    # 29. README.md exists and discloses the same nonproduction status
    readme_ok = readme_path.exists() and "NONPRODUCTION" in read(readme_path) and "read-only" in read(readme_path).lower()
    r.check(29, "README.md exists and discloses NONPRODUCTION / read-only status", readme_ok)

    # --- report ---
    print("=" * 78)
    print("MULTI-CASE POWER-RELATION PROTOTYPE — VALIDATION REPORT")
    print("=" * 78)
    print(f"Prototype dir: {PROTO_DIR}")
    print(f"Cases checked: {list(CASE_FILES.keys())}")
    print()

    passed = [x for x in r.results if x[2]]
    failed = [x for x in r.results if not x[2]]
    total = len(r.results)

    for n, label, ok, detail in r.results:
        status = "PASS" if ok else "FAIL"
        line = f"  [{status}] {n:2d}. {label}"
        if detail and not ok:
            line += f"  -- {detail}"
        print(line)

    print()
    print(f"CHECKS PASSED: {len(passed)}/{total}")
    if failed:
        print(f"CHECKS FAILED: {len(failed)}/{total}")
        print("VALIDATION RESULT: FAIL")
        sys.exit(1)
    else:
        print("VALIDATION RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
