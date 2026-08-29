"""Validates scripts/graph_projection/disposable_projection_output.json
against the FROZEN Graph Projection Contract v1.0 safety rules that
build_projection.py is supposed to guarantee by construction. This is a
belt-and-suspenders check, not a second independent implementation of the
contract -- it re-derives the same source artifacts and cross-checks the
output, so a bug in build_projection.py's own logic can still be caught
here rather than only trusted from its own code.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "research_validators"))

from validate_power_relation_ontology import ALLOWED_RELATION_TYPES  # noqa: E402
from build_projection import SOURCE_FILES, MIGRATED_DIR, EDGE_METADATA_FIELDS  # noqa: E402

FORBIDDEN_EDGE_TYPES = {
    "RESISTS", "PATRON_OF", "CLIENT_OF", "COMMANDS",
    "PARTICIPATES_IN", "HOLDS_COMMERCIAL_RIGHT", "MODIFIES_RIGHT",
}

RESEARCH_ONLY_ENTITY_KEYS = {"commercial_rights", "right_modifications", "observations"}


def check(cond, label, failures):
    if not cond:
        failures.append(label)
    return cond


def main():
    graph_path = REPO_ROOT / "scripts" / "graph_projection" / "disposable_projection_output.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    failures = []

    node_ids = {n["node_id"] for n in graph["nodes"]}
    node_by_id = {n["node_id"]: n for n in graph["nodes"]}

    # 1. No forbidden edge types anywhere (edges or unary claims).
    all_relation_types = {e["relation_type"] for e in graph["edges"]} | {
        u["relation_type"] for u in graph["unary_claims"]
    }
    check(not (all_relation_types & FORBIDDEN_EDGE_TYPES),
          f"FORBIDDEN_EDGE_TYPE_PRESENT: {all_relation_types & FORBIDDEN_EDGE_TYPES}", failures)

    # 2. Every edge/unary-claim relation_type is in the closed vocabulary.
    bad_types = all_relation_types - ALLOWED_RELATION_TYPES
    check(not bad_types, f"UNAPPROVED_RELATION_TYPE_LEAKED: {bad_types}", failures)

    # 3. Every edge endpoint resolves to a real node in the output.
    dangling = [
        e["edge_id"] for e in graph["edges"]
        if e["subject_node_id"] not in node_ids or e["object_node_id"] not in node_ids
    ]
    check(not dangling, f"DANGLING_EDGE_ENDPOINTS: {dangling}", failures)

    dangling_unary = [
        u["claim_id"] for u in graph["unary_claims"]
        if u["subject_node_id"] not in node_ids
    ]
    check(not dangling_unary, f"DANGLING_UNARY_CLAIM_SUBJECT: {dangling_unary}", failures)

    # 4. No unary claim carries an object_node_id (structural guarantee that
    #    DEC-19-shaped relations were never forced into edge shape).
    bad_unary = [u["claim_id"] for u in graph["unary_claims"] if "object_node_id" in u]
    check(not bad_unary, f"UNARY_CLAIM_HAS_OBJECT_NODE: {bad_unary}", failures)

    # 5. Actor-identity rule: every node_id is prefixed by its own case_id,
    #    and the same raw_id in different cases produces different node_ids
    #    (no merge). Spot-checked generically, not just for ACTOR_VOC.
    for n in graph["nodes"]:
        check(n["node_id"] == f"{n['case_id']}::{n['raw_id']}",
              f"NODE_ID_NOT_CASE_SCOPED: {n['node_id']}", failures)
    raw_id_to_cases = {}
    for n in graph["nodes"]:
        raw_id_to_cases.setdefault((n["type"], n["raw_id"]), set()).add(n["case_id"])
    reused_across_cases = {k: v for k, v in raw_id_to_cases.items() if len(v) > 1}
    # Reuse across cases is EXPECTED (e.g. ACTOR_VOC in every case) -- the
    # safety property is that each such raw_id still produced N distinct
    # node_ids, one per case, never a single merged node.
    for (ntype, raw_id), cases in reused_across_cases.items():
        expected_node_ids = {f"{c}::{raw_id}" for c in cases}
        check(expected_node_ids <= node_ids,
              f"CROSS_CASE_ACTOR_MERGE_SUSPECTED: {ntype}/{raw_id} in {cases}", failures)

    # 6. Every edge carries all required metadata keys (contract SS3),
    #    even if some individual values are legitimately null/None.
    required = set(EDGE_METADATA_FIELDS) | {"case_id", "artifact_version", "schema_version"}
    for e in graph["edges"]:
        missing = required - set(e["metadata"].keys())
        check(not missing, f"EDGE_MISSING_METADATA {e['edge_id']}: {missing}", failures)
    for u in graph["unary_claims"]:
        missing = required - set(u["metadata"].keys())
        check(not missing, f"UNARY_CLAIM_MISSING_METADATA {u['claim_id']}: {missing}", failures)

    # 7. No RESEARCH_ONLY entity type (CommercialRight/RightModification/
    #    CommandObservation/OperationParticipation) was ever read into the
    #    graph -- verified by reconstructing node/edge id sets from source
    #    artifacts and confirming zero overlap with those entities' own id
    #    fields.
    leaked = []
    for fname in SOURCE_FILES:
        artifact = json.loads((MIGRATED_DIR / fname).read_text(encoding="utf-8"))
        ro_ids = set()
        for cr in artifact.get("commercial_rights", []) or []:
            ro_ids.add(cr.get("right_id"))
        for rm in artifact.get("right_modifications", []) or []:
            ro_ids.add(rm.get("modification_id"))
        for obs in artifact.get("observations", []) or []:
            ro_ids.add(obs.get("observation_id") or obs.get("command_observation_id"))
        all_output_ids = node_ids | {e["edge_id"] for e in graph["edges"]} | {
            u["claim_id"] for u in graph["unary_claims"]
        }
        overlap = ro_ids & all_output_ids
        if overlap:
            leaked.append((fname, overlap))
    check(not leaked, f"RESEARCH_ONLY_ENTITY_LEAKED_INTO_GRAPH: {leaked}", failures)

    # 8. Node/edge/unary/excluded counts reconcile against total relations
    #    across the 5 source files (every relation is accounted for exactly
    #    once: edge, unary claim, or excluded -- never silently dropped).
    total_relations = 0
    for fname in SOURCE_FILES:
        artifact = json.loads((MIGRATED_DIR / fname).read_text(encoding="utf-8"))
        total_relations += len(artifact.get("relations", []))
    accounted = len(graph["edges"]) + len(graph["unary_claims"]) + len(graph["excluded_relations"])
    check(total_relations == accounted,
          f"RELATION_COUNT_MISMATCH: total={total_relations} accounted={accounted}", failures)

    print(f"Nodes: {len(graph['nodes'])}  Edges: {len(graph['edges'])}  "
          f"Unary claims: {len(graph['unary_claims'])}  Excluded: {len(graph['excluded_relations'])}")
    print(f"Checks run: 8 categories")
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(" -", f)
        print("VALIDATION RESULT: FAIL")
        return 1
    print("VALIDATION RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
