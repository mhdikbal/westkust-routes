"""Disposable graph projection builder.

Implements the FROZEN Graph Projection Contract v1.0
(docs/thesis/pilot_annotation/ATLAS_GRAPH_PROJECTION_READINESS_REVIEW.md,
frozen per ATLAS_GRAPH_PROJECTION_CONTRACT_FREEZE_AUDIT.md, commit ba32eb0)
against the current 5 migrated V2.1 power-relations artifacts.

Explicitly NOT Graphify (the code-knowledge-graph tool at graphify-out/).
This is a local, disposable projection of historical-claim data. It is not
wired into Atlas, the multi-case prototype, or any production consumer.
Output is regenerable by rerunning this script -- it is not itself the
durable record; the durable record is the result summary committed
alongside this script (per the DELTA-09 process finding: a disposable
artifact's citable result must be captured durably, not left only in the
artifact's own output).

Node projection candidates (contract SS1.1): Actor, Location. Source is
listed as *eligible* but not required as a standalone node; this build
scopes it out (see result doc "Scoping decisions") to keep the disposable
build minimal and defensible -- source references remain fully present as
edge/claim metadata (source_document_ids, source_passage_locator), just
not materialized as their own node type this run.

Edge projection rules (contract SS2): only the closed 18-value vocabulary
(scripts/research_validators/power_relation_ontology_rules.json,
reused via validate_power_relation_ontology.ALLOWED_RELATION_TYPES -- same
source of truth the generalized validator uses, not a second copy of the
list) may become an edge, and only if it is the artifact's own real
relation_type. The seven auto-derivation traps (RESISTS, PATRON_OF,
CLIENT_OF, COMMANDS, PARTICIPATES_IN, HOLDS_COMMERCIAL_RIGHT,
MODIFIES_RIGHT) are structurally impossible here because this script
never reads CommercialRight/RightModification/CommandObservation/
OperationParticipation at all -- edges are derived exclusively from
artifact["relations"].

DEC-19 handling: a relation whose object_id is null and which instead
carries a `commodity` attribute (the post-remodel Tiku shape) has no
second node to connect to -- Commodity is explicitly not a node/endpoint
under DEC-19 option (b). Such relations are NOT forced into edge shape;
they are projected as a subject-scoped "unary claim" attached to the
subject Actor node, carrying the same full metadata. This is a
structural consequence of DEC-19's own attribute-only design, decided
here as the faithful representation, not assumed in advance.

Actor identity rule (contract SS4): every node is keyed by
(case_id, raw_id), never by raw_id alone. The same ACTOR_VOC in five
cases is five distinct nodes. No merge logic of any kind exists in this
script.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "research_validators"))

from validate_power_relation_ontology import ALLOWED_RELATION_TYPES  # noqa: E402

MIGRATED_DIR = REPO_ROOT / "data" / "power_relations" / "migrated_v2_1"

# Exactly the 5 current cases. Tiku uses the DEC-19-remodeled file
# (_v2_1_1_); the original _v2_1_ Tiku file is deliberately excluded from
# this input set (same case_id, would otherwise double-count/collide).
SOURCE_FILES = [
    "painan_1663_relational_research_artifact_v2_1_migrated.json",
    "natal_1760_relational_validation_artifact_v2_1_migrated.json",
    "koto_tangah_destruction_cycle_relational_validation_artifact_v2_1_migrated.json",
    "tiku_1625_1740_relational_validation_artifact_v2_1_1_migrated.json",
    "sillida_resource_governance_relational_validation_artifact_v2_1_migrated.json",
]

EDGE_METADATA_FIELDS = [
    "source_document_ids",
    "source_passage_locator",
    "valid_from",
    "valid_to",
    "date_precision",
    "open_ended",
    "evidence_strength",
    "provenance_status",
    "interpretive_status",
    "explicit_or_inferred",
    "researcher_review_required",
]


def node_id(case_id, raw_id):
    return f"{case_id}::{raw_id}"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    nodes = []
    node_index = {}  # node_id -> node dict, for endpoint lookup
    edges = []
    unary_claims = []
    excluded = []
    source_artifacts = []

    for fname in SOURCE_FILES:
        path = MIGRATED_DIR / fname
        artifact = json.loads(path.read_text(encoding="utf-8"))
        case_id = artifact["case_id"]
        source_artifacts.append({
            "file": fname,
            "case_id": case_id,
            "sha256": sha256_of(path),
        })

        local_actor_ids = set()
        local_location_ids = set()

        for a in artifact.get("actors", []):
            nid = node_id(case_id, a["actor_id"])
            node = {
                "node_id": nid,
                "type": "Actor",
                "case_id": case_id,
                "raw_id": a["actor_id"],
                "label": a.get("normalized_label") or a.get("source_label") or a.get("label"),
                "attributes": {
                    "mandate_status": a.get("mandate_status"),
                    "identity_continuity_status": a.get("identity_continuity_status"),
                    "explicit_non_identity_with": a.get("explicit_non_identity_with"),
                },
            }
            nodes.append(node)
            node_index[nid] = node
            local_actor_ids.add(a["actor_id"])

        for loc in artifact.get("locations", []):
            nid = node_id(case_id, loc["location_id"])
            node = {
                "node_id": nid,
                "type": "Location",
                "case_id": case_id,
                "raw_id": loc["location_id"],
                "label": loc.get("normalized_label") or loc.get("source_label") or loc.get("label"),
                "attributes": {},
            }
            nodes.append(node)
            node_index[nid] = node
            local_location_ids.add(loc["location_id"])

        known_local = local_actor_ids | local_location_ids

        for rel in artifact.get("relations", []):
            rel_id = rel.get("relation_id")
            rtype = rel.get("relation_type")
            subj_raw = rel.get("subject_actor_id")
            # Painan's pre-V2.1 relations carry the object endpoint under
            # `object_actor_id`, never `object_id` (confirmed by direct
            # inspection: 0/9 Painan relations have an `object_id` key,
            # 9/9 have `object_actor_id`). The generalized validator's own
            # R-REF-05 check reads only `object_id` and has therefore never
            # actually checked Painan's endpoint integrity -- a real,
            # previously undetected validator gap, documented in this run's
            # result summary rather than silently worked around. This
            # script reads both keys (object_id takes precedence if a file
            # ever had both) so the projection itself is not built on a
            # blind spot, without touching the validator itself.
            obj_raw = rel.get("object_id")
            if obj_raw is None and "object_id" not in rel and "object_actor_id" in rel:
                obj_raw = rel.get("object_actor_id")

            if rtype not in ALLOWED_RELATION_TYPES:
                excluded.append({
                    "case_id": case_id, "relation_id": rel_id, "relation_type": rtype,
                    "reason": "UNAPPROVED_RELATION_TYPE",
                })
                continue

            if subj_raw not in local_actor_ids:
                excluded.append({
                    "case_id": case_id, "relation_id": rel_id, "relation_type": rtype,
                    "reason": f"ORPHAN_SUBJECT_ENDPOINT subject_actor_id={subj_raw!r}",
                })
                continue

            subj_node_id = node_id(case_id, subj_raw)
            metadata = {k: rel.get(k) for k in EDGE_METADATA_FIELDS}
            metadata["case_id"] = case_id
            metadata["artifact_version"] = artifact.get("ontology_version") or artifact.get("ontology_contract_version")
            metadata["schema_version"] = artifact.get("schema_version")

            if obj_raw is None:
                # DEC-19-shaped relation: no second node, projected as a
                # subject-scoped unary claim, never forced into edge shape.
                unary_claims.append({
                    "claim_id": rel_id,
                    "subject_node_id": subj_node_id,
                    "relation_type": rtype,
                    "commodity": rel.get("commodity"),
                    "metadata": metadata,
                })
                continue

            if obj_raw not in known_local:
                excluded.append({
                    "case_id": case_id, "relation_id": rel_id, "relation_type": rtype,
                    "reason": f"ORPHAN_OBJECT_ENDPOINT object_id={obj_raw!r}",
                })
                continue

            obj_node_id = node_id(case_id, obj_raw)
            edges.append({
                "edge_id": rel_id,
                "case_id": case_id,
                "subject_node_id": subj_node_id,
                "object_node_id": obj_node_id,
                "relation_type": rtype,
                "metadata": metadata,
            })

    graph = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "contract": "Graph Projection Contract v1.0 (ba32eb0), ATLAS_GRAPH_PROJECTION_READINESS_REVIEW.md",
        "disposable": True,
        "not_graphify": True,
        "not_wired_to_atlas_or_prototype": True,
        "source_artifacts": source_artifacts,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "unary_claim_count": len(unary_claims),
        "excluded_count": len(excluded),
        "nodes": nodes,
        "edges": edges,
        "unary_claims": unary_claims,
        "excluded_relations": excluded,
    }
    return graph


def main():
    graph = build()
    out_path = REPO_ROOT / "scripts" / "graph_projection" / "disposable_projection_output.json"
    out_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"nodes={graph['node_count']} edges={graph['edge_count']} "
          f"unary_claims={graph['unary_claim_count']} excluded={graph['excluded_count']}")
    print(f"written: {out_path}")


if __name__ == "__main__":
    main()
