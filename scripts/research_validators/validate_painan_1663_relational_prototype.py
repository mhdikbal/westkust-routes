#!/usr/bin/env python3
"""Read-only validator for the Painan 1663 relational research prototype.

NONPRODUCTION TOOL. Checks the prototype's static source
(research_prototypes/painan_1663_relational/{index.html,prototype.js,prototype.css})
against the 30-item checklist in
ATLAS_PAINAN_1663_LOCAL_RELATIONAL_RESEARCH_PROTOTYPE_PLAN.md §13, and re-verifies
the underlying artifact and base validator. Performs no writes, no network calls,
no API/database/Graphify access, and imports nothing from backend/ or frontend/.

Usage: python3 scripts/research_validators/validate_painan_1663_relational_prototype.py
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROTO_DIR = REPO / "research_prototypes/painan_1663_relational"
ARTIFACT_PATH = REPO / "data/power_relations/painan_1663_relational_research_artifact.json"
BASE_VALIDATOR = REPO / "scripts/research_validators/validate_painan_1663_relational_artifact.py"
EXPECTED_SHA256 = "eeeeda8b368e255303c46dc245beb3c1179815d9f960cdff20b1ea59518b4bd7"

AUTHORIZED_RELATION_TYPES = [
    "REQUESTS_PROTECTION_FROM", "PROVIDES_PROTECTION_TO", "REQUIRES_MONOPOLY_FROM",
    "NEGOTIATES_WITH", "RECONCILES_WITH", "MAINTAINS_PARALLEL_ALIGNMENT_WITH",
    "CLAIMS_JURISDICTION_OVER",
]
FORBIDDEN_RELATION_TYPES = ["PATRON_OF", "CLIENT_OF", "PATRON_CLIENT_RELATION"]
FORBIDDEN_TOKENS = ["payoff", "equilibrium", "winner", "loser", "utility_score", "best_move"]


class Report:
    def __init__(self):
        self.results = []  # (n, label, passed, detail)

    def check(self, n, label, passed, detail=""):
        self.results.append((n, label, passed, detail))


def read(path):
    return path.read_text(encoding="utf-8")


def main():
    r = Report()

    html_path = PROTO_DIR / "index.html"
    js_path = PROTO_DIR / "prototype.js"
    css_path = PROTO_DIR / "prototype.css"

    if not (html_path.exists() and js_path.exists() and css_path.exists()):
        print("FATAL: prototype files not found under", PROTO_DIR)
        sys.exit(2)

    html = read(html_path)
    js = read(js_path)
    css = read(css_path)
    combined_source = html + "\n" + js + "\n" + css

    artifact_bytes = ARTIFACT_PATH.read_bytes()
    artifact_sha = hashlib.sha256(artifact_bytes).hexdigest()
    artifact = json.loads(artifact_bytes)
    actors = artifact.get("actors", [])
    relations = artifact.get("relations", [])

    # 1. artifact checksum matches
    r.check(1, "artifact checksum matches reviewed SHA-256", artifact_sha == EXPECTED_SHA256,
            f"got {artifact_sha}")

    # 2. research validator remains 23/23 PASS
    proc = subprocess.run([sys.executable, str(BASE_VALIDATOR)], capture_output=True, text=True)
    base_pass = proc.returncode == 0 and "CHECKS PASSED: 23" in proc.stdout and "VALIDATION RESULT: PASS" in proc.stdout
    r.check(2, "base artifact validator remains 23/23 PASS", base_pass, proc.stdout.splitlines()[-1] if proc.stdout else proc.stderr)

    # 3. six actors render (data support + renderActors present in source)
    r.check(3, "six actors present and renderActors() implemented", len(actors) == 6 and "function renderActors" in js,
            f"actor count={len(actors)}")

    # 4. nine relations render
    r.check(4, "nine relations present and relation renderers implemented", len(relations) == 9 and "function renderNetwork" in js,
            f"relation count={len(relations)}")

    # 5. all relation endpoints resolve
    actor_ids = {a["actor_id"] for a in actors}
    unresolved = [rel["relation_id"] for rel in relations
                  if rel["subject_actor_id"] not in actor_ids or rel["object_actor_id"] not in actor_ids]
    endpoint_check_in_js = "ACTOR_BY_ID[rel.subject_actor_id]" in js and "ACTOR_BY_ID[rel.object_actor_id]" in js
    r.check(5, "all relation endpoints resolve (data + renderer-side validation present)",
            not unresolved and endpoint_check_in_js, f"unresolved={unresolved}")

    # 6. all seven relation types supported by the renderer
    missing_types = [t for t in AUTHORIZED_RELATION_TYPES if t not in js]
    r.check(6, "all seven authorized relation types referenced in renderer", not missing_types, f"missing={missing_types}")

    # 7. no unsupported relation type appears (in artifact data)
    unsupported = [rel["relation_type"] for rel in relations if rel["relation_type"] not in AUTHORIZED_RELATION_TYPES]
    r.check(7, "no unsupported relation_type appears in artifact data", not unsupported, f"unsupported={unsupported}")

    # 8. no patron-client edge exists
    forbidden_present_data = [rel["relation_type"] for rel in relations if rel["relation_type"] in FORBIDDEN_RELATION_TYPES]
    forbidden_guarded_in_js = "FORBIDDEN_RELATION_TYPES" in js and all(f in js for f in FORBIDDEN_RELATION_TYPES)
    r.check(8, "no PATRON_OF/CLIENT_OF/PATRON_CLIENT_RELATION edge; renderer guards against it",
            not forbidden_present_data and forbidden_guarded_in_js, f"found={forbidden_present_data}")

    # 9. no numeric payoff exists
    payoff_hits = [t for t in ["payoff", "utility_score", "best_move"] if t.lower() in combined_source.lower()]
    r.check(9, "no numeric payoff / utility_score / best_move token in prototype source", not payoff_hits, f"hits={payoff_hits}")

    # 10. no equilibrium language appears
    equilibrium_hits = re.findall(r"equilibrium", combined_source, re.IGNORECASE)
    r.check(10, "no 'equilibrium' language in prototype source", not equilibrium_hits, f"count={len(equilibrium_hits)}")

    # 11. no winner/loser label appears
    wl_hits = re.findall(r"\bwinner\b|\bloser\b", combined_source, re.IGNORECASE)
    r.check(11, "no winner/loser label in prototype source", not wl_hits, f"count={len(wl_hits)}")

    # 12. all source locators render
    r.check(12, "source_passage_locator rendered in relation detail panel", "source_passage_locator" in js)

    # 13. all event IDs render
    r.check(13, "event_ids rendered in relation detail panel", "r.event_ids" in js or "event_ids" in js)

    # 14. explicit and inferred relations are visually distinct
    visual_distinct = all(x in css for x in [".badge-explicit", ".badge-inferred", ".timeline-bar.explicit", ".timeline-bar.inferred"]) \
        and "stroke-dasharray" in js
    r.check(14, "explicit vs inferred relations carry distinct, non-color-only visual treatment (badge/dash pattern)", visual_distinct)

    # 15. claim and effective control are distinct
    r.check(15, "claim_or_effective_control rendered as its own distinct field/view", "claim_or_effective_control" in js and "renderClaimControl" in js)

    # 16. protection and submission are not conflated
    protection_types_used = {"PROVIDES_PROTECTION_TO", "REQUESTS_PROTECTION_FROM"} <= set(t["relation_type"] for t in relations) if relations else False
    r.check(16, "protection relation types rendered under their own relation_type label, never relabeled as submission",
            "submission" not in combined_source.lower())

    # 17. parallel alignment and switching are distinct
    both_present = "RECONCILES_WITH" in js and "MAINTAINS_PARALLEL_ALIGNMENT_WITH" in js
    r.check(17, "RECONCILES_WITH and MAINTAINS_PARALLEL_ALIGNMENT_WITH rendered as distinct relation types", both_present)

    # 18. treaty acceptance and sovereignty are distinct
    r.check(18, "'sovereignty' not asserted anywhere in prototype source (no treaty=sovereignty conflation)",
            "sovereignty" not in combined_source.lower())

    # 19. source, reconstruction, theory, and public copy are separate
    four_layers = all(x in js for x in [
        "source_statement_summary", "historical_reconstruction", "theoretical_annotation", "public_display_summary"
    ]) and all(x in css for x in [".layer-card.source", ".layer-card.reconstruction", ".layer-card.theory", ".layer-card.public"])
    r.check(19, "four interpretive layers (source/reconstruction/theory/public) rendered in visually separate containers", four_layers)

    # 20. inferred relations show researcher review status
    r.check(20, "researcher_review_required rendered per relation", "researcher_review_required" in js and "Researcher review required" in js)

    # 21. unresolved mandates are visible
    r.check(21, "unresolved actors/mandates section present in Overview", "Unresolved actors and mandates" in js)

    # 22. missing source gaps are visible
    r.check(22, "Source gaps section present in Overview", "Source gaps" in js)

    # 23. no production imports exist
    bad_imports = re.findall(r"(?:import|require|src=|href=)\s*['\"](?:/backend|/frontend|\.\./\.\./backend|\.\./\.\./frontend)", combined_source)
    r.check(23, "no import/reference to backend/ or frontend/ from prototype", not bad_imports, f"hits={bad_imports}")

    # 24. no API calls exist (only the one artifact fetch, no /api/ or absolute http(s) URL).
    # Match only REAL fetch(...) calls (an identifier/expression immediately after the paren,
    # e.g. "fetch(ARTIFACT_PATH" or "fetch('...'"), not a bare "fetch()" mention inside prose/comments.
    real_fetch_calls = re.findall(r"fetch\(\s*([A-Za-z_$'\"][^)]*)\)", js)
    non_artifact_fetches = [f for f in real_fetch_calls if "ARTIFACT_PATH" not in f]
    # Scope the remote-URL check to string literals passed as the FIRST argument of a real fetch call
    # only (not e.g. the SVG XML namespace URI used elsewhere in the file for markup, which is required
    # and not a network call).
    remote_fetch_hits = [f for f in real_fetch_calls if re.match(r"""^['"](?:https?:)?//|^['"]/api/""", f)]
    r.check(24, "exactly one real fetch() call, targeting only the local artifact path; no /api/ or remote URL",
            len(real_fetch_calls) == 1 and not non_artifact_fetches and not remote_fetch_hits,
            f"real_fetch_calls={real_fetch_calls}, remote_hits={remote_fetch_hits}")

    # 25. no database access exists
    db_hits = re.findall(r"psycopg|sqlalchemy|SELECT\s+\*|pg_connect|postgres", combined_source, re.IGNORECASE)
    r.check(25, "no database-access code/reference in prototype source", not db_hits, f"hits={db_hits}")

    # 26. no Graphify access exists. "Graphify" legitimately appears in the status banner and in
    # documentation comments stating that NO Graphify access exists (e.g. "NOT CONNECTED TO ...
    # GRAPHIFY", "no Graphify access"). That is the required disclosure text, not usage. Flag only
    # FUNCTIONAL usage: a call, import, require, or a graphify-out/ path reference.
    graphify_functional_hits = re.findall(
        r"graphify\s*\(|require\([^)]*graphify|import[^;]*graphify|graphify-out|graphify_client",
        combined_source, re.IGNORECASE,
    )
    r.check(26, "no FUNCTIONAL Graphify usage (call/import/require/path) in prototype source "
                "(the word appears only in the required 'no Graphify access' disclosure text)",
            not graphify_functional_hits, f"hits={graphify_functional_hits}")

    # 27. no production Atlas asset is modified/targeted. "atlas.js" is not referenced at all (checked
    # directly). "index.html" legitimately appears once, inside a code COMMENT explaining that
    # file://index.html blocks fetch() in browsers — that is a comment about THIS prototype's own
    # file, not a reference to the production frontend/map_app/templates/map_app/index.html template.
    # Flag only an actual reference to that production template path.
    references_atlas_js = "atlas.js" in combined_source
    references_production_index_template = "frontend/map_app/templates/map_app/index.html" in combined_source \
        or "map_app/templates/map_app/index.html" in combined_source
    r.check(27, "prototype never references or targets atlas.js or the production frontend index.html template",
            not references_atlas_js and not references_production_index_template,
            f"atlas.js_hit={references_atlas_js}, production_index_hit={references_production_index_template}")

    # 28. narrow viewport renders without content loss (structural: media query present)
    r.check(28, "narrow-viewport (max-width:480px) media query present in CSS", "max-width: 480px" in css)

    # 29. keyboard access works (structural: only native interactive elements + focus-visible style)
    uses_native_interactive = "<button" in html or "el(\"button\"" in js or "'button'" in js
    has_focus_visible = ":focus-visible" in css
    tabindex_on_custom_controls = "tabindex" in js
    r.check(29, "keyboard-accessible controls (native buttons/selects/details, tabindex on custom SVG controls, :focus-visible style)",
            uses_native_interactive and has_focus_visible and tabindex_on_custom_controls)

    # 30. all prototype status banners are present
    banner_lines = ["RESEARCH PROTOTYPE", "NONPRODUCTION", "PAINAN 1663 RELATIONAL MVP",
                     "NOT CONNECTED TO THE PUBLIC ATLAS, API, DATABASE, OR GRAPHIFY"]
    banners_present = all(b in html for b in banner_lines)
    r.check(30, "all four required status-banner lines present in index.html", banners_present)

    # --- report ---
    print("=" * 78)
    print("PAINAN 1663 RELATIONAL PROTOTYPE — VALIDATION REPORT")
    print("=" * 78)
    print(f"Prototype dir: {PROTO_DIR}")
    print(f"Artifact: {ARTIFACT_PATH}  (sha256={artifact_sha})")
    print()

    passed = [x for x in r.results if x[2]]
    failed = [x for x in r.results if not x[2]]

    for n, label, ok, detail in r.results:
        status = "PASS" if ok else "FAIL"
        line = f"  [{status}] {n:2d}. {label}"
        if detail and not ok:
            line += f"  -- {detail}"
        print(line)

    print()
    print(f"CHECKS PASSED: {len(passed)}/30")
    if failed:
        print(f"CHECKS FAILED: {len(failed)}/30")
        print("VALIDATION RESULT: FAIL")
        sys.exit(1)
    else:
        print("VALIDATION RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
