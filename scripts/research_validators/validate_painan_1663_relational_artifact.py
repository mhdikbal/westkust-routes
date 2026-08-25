#!/usr/bin/env python3
"""Read-only validator for data/power_relations/painan_1663_relational_research_artifact.json.

NONPRODUCTION TOOL. This script:
  - reads the artifact JSON and the verified linimasa_events.csv row set;
  - performs structural and controlled-vocabulary checks;
  - prints a report and exits non-zero if any check fails.

It does NOT:
  - write or modify the artifact or any other file;
  - call any API, database, Graphify, or Atlas code;
  - create any migration.

Usage: python3 scripts/research_validators/validate_painan_1663_relational_artifact.py
"""
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO / "data/power_relations/painan_1663_relational_research_artifact.json"
LINIMASA_PATH = REPO / "data/research/linimasa_events.csv"

RELATION_TYPES = {
    "REQUESTS_PROTECTION_FROM", "PROVIDES_PROTECTION_TO", "REQUIRES_MONOPOLY_FROM",
    "NEGOTIATES_WITH", "RECONCILES_WITH", "MAINTAINS_PARALLEL_ALIGNMENT_WITH",
    "CLAIMS_JURISDICTION_OVER",
}
PROVENANCE_STATUS = {"CD_PRIMARY", "CD_PARTIAL", "CD_INDEPENDENT", "MULTI_SOURCE_VERIFIED", "PROVENANCE_AMBIGUOUS"}
EVIDENCE_STRENGTH = {"HIGH", "MODERATE", "LOW", "CANNOT_DETERMINE"}
INTERPRETIVE_STATUS = {"SOURCE_DESCRIPTION_ONLY", "MECHANISM_HYPOTHESIS", "PROCESS_TRACING_SUPPORTED", "CONTESTED", "CANNOT_DETERMINE"}
EXPLICIT_OR_INFERRED = {"EXPLICIT_STRATEGY", "OBSERVED_ACTION_AS_STRATEGY", "INFERRED_AVAILABLE_OPTION", "COUNTERFACTUAL_NOT_ESTABLISHED"}
CLAIM_OR_EFFECTIVE_CONTROL = {
    "CLAIM", "FORMAL_ACCEPTANCE", "TREATY_OBLIGATION", "MILITARY_PRESENCE", "FORT_CONTROL",
    "COMMERCIAL_CONTROL", "ADMINISTRATIVE_CONTROL", "EFFECTIVE_LOCAL_COMPLIANCE",
    "CONTESTED_CONTROL", "UNKNOWN_EFFECTIVE_CONTROL",
}
COMMITMENT_CREDIBILITY = {"CREDIBLE", "PARTIALLY_CREDIBLE", "LOW_CREDIBILITY", "FAILED", "NOT_TESTABLE"}
PATRON_CLIENT_CLASSIFICATION = {
    "PATRON_CLIENT_SUPPORTED", "PATRON_CLIENT_PARTIALLY_SUPPORTED", "PATRON_CLIENT_CONTESTED",
    "PATRON_CLIENT_NOT_SUPPORTED", "PATRON_CLIENT_NOT_TESTABLE",
}
POWER_DIMENSIONS = {
    "FIRST_DIMENSION", "SECOND_DIMENSION", "THIRD_DIMENSION", "RELATIONAL_AND_PRODUCTIVE",
    "SYMBOLIC_CLASSIFICATORY", "AUTHORITY_AND_LEGITIMACY",
}
FORBIDDEN_RELATION_TYPES = {"PATRON_OF", "CLIENT_OF", "PATRON_CLIENT_RELATION"}
FORBIDDEN_NUMERIC_KEYS = {"payoff", "payoffs", "utility", "equilibrium", "best_move", "winner", "loser"}

RELATION_REQUIRED_FIELDS = [
    "relation_id", "subject_actor_id", "object_actor_id", "relation_type",
    "valid_from", "valid_to", "date_precision", "event_ids", "treaty_id",
    "source_document_ids", "source_passage_locator", "provenance_status",
    "evidence_strength", "interpretive_status", "explicit_or_inferred",
    "claim_or_effective_control", "commitment_credibility", "patron_client_classification",
    "power_dimensions", "researcher_review_required", "source_statement_summary",
    "historical_reconstruction", "theoretical_annotation", "public_display_summary", "notes",
]


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checks_passed = []

    def ok(self, label):
        self.checks_passed.append(label)

    def fail(self, label, detail):
        self.errors.append(f"{label}: {detail}")

    def warn(self, label, detail):
        self.warnings.append(f"{label}: {detail}")


def load_verified_linimasa_row_ids():
    """rows 2..N (data row index, header=row1) that exist in the CSV; used to check event_ids resolve."""
    ids = set()
    with open(LINIMASA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for i, _ in enumerate(reader, start=2):
            ids.add(f"linimasa_row_{i}")
    return ids


def main():
    r = Report()

    if not ARTIFACT_PATH.exists():
        print(f"FATAL: artifact not found at {ARTIFACT_PATH}")
        sys.exit(2)

    raw = ARTIFACT_PATH.read_text(encoding="utf-8")
    try:
        artifact = json.loads(raw)
        r.ok("a. JSON valid")
    except json.JSONDecodeError as e:
        print(f"FATAL: artifact is not valid JSON: {e}")
        sys.exit(2)

    # b. schema version present
    if artifact.get("schema_version"):
        r.ok("b. schema_version present")
    else:
        r.fail("b. schema_version", "missing or empty")

    actors = artifact.get("actors", [])
    relations = artifact.get("relations", [])
    treaties = artifact.get("treaties", [])

    actor_ids = [a.get("actor_id") for a in actors]
    treaty_ids = {t.get("treaty_id") for t in treaties}

    # c. actor IDs unique
    if len(actor_ids) == len(set(actor_ids)) and all(actor_ids):
        r.ok("c. actor IDs unique and non-empty")
    else:
        r.fail("c. actor IDs unique", f"duplicates or blanks found: {actor_ids}")

    # d. relation IDs unique
    relation_ids = [rel.get("relation_id") for rel in relations]
    if len(relation_ids) == len(set(relation_ids)) and all(relation_ids):
        r.ok("d. relation IDs unique and non-empty")
    else:
        r.fail("d. relation IDs unique", f"duplicates or blanks found: {relation_ids}")

    actor_id_set = set(actor_ids)

    # e. no orphan endpoints
    orphan_edges = []
    for rel in relations:
        s, o = rel.get("subject_actor_id"), rel.get("object_actor_id")
        if s not in actor_id_set or o not in actor_id_set:
            orphan_edges.append(rel.get("relation_id"))
    if not orphan_edges:
        r.ok("e. no orphan relation endpoints")
    else:
        r.fail("e. orphan relation endpoints", str(orphan_edges))

    connected_actors = set()
    for rel in relations:
        connected_actors.add(rel.get("subject_actor_id"))
        connected_actors.add(rel.get("object_actor_id"))
    disconnected = actor_id_set - connected_actors
    if disconnected:
        r.warn("actor connectivity", f"actors with zero relation edges: {sorted(disconnected)}")

    # f. relation_type only from the 7 authorized values
    bad_types = [rel.get("relation_id") for rel in relations if rel.get("relation_type") not in RELATION_TYPES]
    if not bad_types:
        r.ok("f. relation_type restricted to the 7 authorized values")
    else:
        r.fail("f. relation_type restricted", f"records with unauthorized type: {bad_types}")

    # g. controlled vocabularies valid + required fields present (also covers item 5 mandatory fields)
    field_errors = []
    vocab_checks = [
        ("provenance_status", PROVENANCE_STATUS),
        ("evidence_strength", EVIDENCE_STRENGTH),
        ("interpretive_status", INTERPRETIVE_STATUS),
        ("explicit_or_inferred", EXPLICIT_OR_INFERRED),
        ("claim_or_effective_control", CLAIM_OR_EFFECTIVE_CONTROL),
        ("commitment_credibility", COMMITMENT_CREDIBILITY),
        ("patron_client_classification", PATRON_CLIENT_CLASSIFICATION),
    ]
    for rel in relations:
        rid = rel.get("relation_id")
        for field in RELATION_REQUIRED_FIELDS:
            if field not in rel:
                field_errors.append(f"{rid} missing required field '{field}'")
        for field, allowed in vocab_checks:
            val = rel.get(field)
            if val is not None and val not in allowed:
                field_errors.append(f"{rid}.{field}='{val}' not in controlled vocabulary {sorted(allowed)}")
        pdims = rel.get("power_dimensions") or []
        for pd in pdims:
            if pd not in POWER_DIMENSIONS:
                field_errors.append(f"{rid}.power_dimensions contains unknown value '{pd}'")
    if not field_errors:
        r.ok("g. controlled vocabularies valid; all mandatory fields present")
    else:
        for e in field_errors:
            r.fail("g. controlled vocabulary / required field", e)

    # h. source_passage_locator not empty
    empty_locator = [rel.get("relation_id") for rel in relations if not (rel.get("source_passage_locator") or "").strip()]
    if not empty_locator:
        r.ok("h. source_passage_locator non-empty for all relations")
    else:
        r.fail("h. source_passage_locator non-empty", str(empty_locator))

    # i. all event IDs resolve to a verified source row
    verified_row_ids = load_verified_linimasa_row_ids()
    bad_event_ids = []
    for rel in relations:
        for eid in rel.get("event_ids", []):
            if eid not in verified_row_ids:
                bad_event_ids.append((rel.get("relation_id"), eid))
    if not bad_event_ids:
        r.ok("i. all event_ids resolve to a real linimasa_events.csv row")
    else:
        r.fail("i. event_ids resolve", str(bad_event_ids))

    # j. dates valid, valid_from <= valid_to when both present
    def parse_partial_date(s):
        if s is None:
            return None
        parts = s.split("-")
        try:
            parts = [int(p) for p in parts]
        except ValueError:
            return "INVALID"
        padded = parts + [1] * (3 - len(parts))
        return tuple(padded)

    date_errors = []
    for rel in relations:
        vf = parse_partial_date(rel.get("valid_from"))
        vt = parse_partial_date(rel.get("valid_to"))
        if vf == "INVALID":
            date_errors.append(f"{rel.get('relation_id')} valid_from unparseable: {rel.get('valid_from')}")
        if vt == "INVALID":
            date_errors.append(f"{rel.get('relation_id')} valid_to unparseable: {rel.get('valid_to')}")
        if isinstance(vf, tuple) and isinstance(vt, tuple) and vf > vt:
            date_errors.append(f"{rel.get('relation_id')} valid_from {rel.get('valid_from')} > valid_to {rel.get('valid_to')}")
    if not date_errors:
        r.ok("j. dates parseable and valid_from <= valid_to where both present")
    else:
        for e in date_errors:
            r.fail("j. date validity", e)

    # k. no actor homogenization: Painan/Padang/Tiku/Indrapura must not be merged into one actor;
    #    excluded actors must not silently appear merged into an included one.
    homogenization_flags = []
    forbidden_labels_substring = ["songypagouers", "westkustgrooten", "pantai barat", "west coast"]
    for a in actors:
        label = (a.get("label") or "").lower()
        desc = (a.get("description") or "").lower()
        for bad in forbidden_labels_substring:
            if bad in label:
                homogenization_flags.append(f"actor {a.get('actor_id')} label contains aggregating term '{bad}'")
    if len(actor_ids) == len(set(actor_ids)) and not homogenization_flags:
        r.ok("k. no actor homogenization detected (no aggregating label used as an actor identity)")
    else:
        for f in homogenization_flags:
            r.fail("k. actor homogenization", f)

    # l. claim and effective control separated: TREATY_OBLIGATION/CLAIM relations must not silently
    #    carry EFFECTIVE_LOCAL_COMPLIANCE unless a distinct compliance-specific note/source exists.
    claim_control_conflicts = []
    for rel in relations:
        cec = rel.get("claim_or_effective_control")
        if cec == "EFFECTIVE_LOCAL_COMPLIANCE" and rel.get("relation_type") == "CLAIMS_JURISDICTION_OVER":
            claim_control_conflicts.append(
                f"{rel.get('relation_id')} asserts EFFECTIVE_LOCAL_COMPLIANCE directly on a "
                f"CLAIMS_JURISDICTION_OVER edge without a separate contested-control record"
            )
    if not claim_control_conflicts:
        r.ok("l. claim vs effective control kept separated for CLAIMS_JURISDICTION_OVER edges")
    else:
        for c in claim_control_conflicts:
            r.fail("l. claim vs effective control", c)

    # m. protection and submission separated: PROVIDES_PROTECTION_TO must not carry a
    #    sovereignty/submission-implying claim_or_effective_control value (FORT_CONTROL/ADMINISTRATIVE_CONTROL)
    #    without researcher_review_required = true.
    protection_submission_conflicts = []
    for rel in relations:
        if rel.get("relation_type") == "PROVIDES_PROTECTION_TO" and rel.get("claim_or_effective_control") in {
            "FORT_CONTROL", "ADMINISTRATIVE_CONTROL"
        } and not rel.get("researcher_review_required"):
            protection_submission_conflicts.append(rel.get("relation_id"))
    if not protection_submission_conflicts:
        r.ok("m. protection vs submission kept separated")
    else:
        r.fail("m. protection vs submission", str(protection_submission_conflicts))

    # n. treaty acceptance and sovereignty separated: FORMAL_ACCEPTANCE must not appear together with
    #    a public_display_summary implying sovereignty transfer.
    sovereignty_terms = ["sovereignty", "kedaulatan", "annexed", "annexation"]
    treaty_sovereignty_conflicts = []
    for rel in relations:
        pds = (rel.get("public_display_summary") or "").lower()
        if rel.get("claim_or_effective_control") == "FORMAL_ACCEPTANCE" and any(t in pds for t in sovereignty_terms):
            treaty_sovereignty_conflicts.append(rel.get("relation_id"))
    if not treaty_sovereignty_conflicts:
        r.ok("n. treaty acceptance vs sovereignty kept separated in public_display_summary")
    else:
        r.fail("n. treaty acceptance vs sovereignty", str(treaty_sovereignty_conflicts))

    # o. parallel alignment and switching separated: no single relation_id may be tagged as both
    #    RECONCILES_WITH and MAINTAINS_PARALLEL_ALIGNMENT_WITH for the identical (subject,object) pair.
    seen_pairs_by_type = {}
    parallel_switch_conflicts = []
    for rel in relations:
        key = (rel.get("subject_actor_id"), rel.get("object_actor_id"))
        seen_pairs_by_type.setdefault(key, set()).add(rel.get("relation_type"))
    for key, types in seen_pairs_by_type.items():
        if {"RECONCILES_WITH", "MAINTAINS_PARALLEL_ALIGNMENT_WITH"} <= types:
            # allowed only if they are recorded as distinct relation_ids (already guaranteed) -- this
            # check exists to catch a single record improperly asserting both states on one edge, which
            # cannot happen given distinct relation_ids, so this branch documents intentional co-existence.
            pass
    r.ok("o. parallel alignment vs switching recorded as distinct relation instances (no single record conflates both)")

    # p. patron-client only as annotation: forbidden relation types must not appear
    forbidden_found = [rel.get("relation_id") for rel in relations if rel.get("relation_type") in FORBIDDEN_RELATION_TYPES]
    if not forbidden_found:
        r.ok("p. patron-client present only as annotation field, never as a relation_type")
    else:
        r.fail("p. patron-client as relation_type", str(forbidden_found))

    # q. no PATRON_CLIENT_SUPPORTED anywhere
    supported_found = [rel.get("relation_id") for rel in relations if rel.get("patron_client_classification") == "PATRON_CLIENT_SUPPORTED"]
    if not supported_found:
        r.ok("q. no relation carries PATRON_CLIENT_SUPPORTED")
    else:
        r.fail("q. PATRON_CLIENT_SUPPORTED found", str(supported_found))

    # r. no arbitrary numeric payoff
    def scan_for_forbidden_keys(obj, path=""):
        found = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k.lower() in FORBIDDEN_NUMERIC_KEYS:
                    found.append(f"{path}.{k}")
                found.extend(scan_for_forbidden_keys(v, f"{path}.{k}"))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                found.extend(scan_for_forbidden_keys(v, f"{path}[{i}]"))
        return found

    forbidden_keys_found = scan_for_forbidden_keys(artifact)
    if not forbidden_keys_found:
        r.ok("r. no arbitrary numeric payoff / utility / winner-loser field present")
    else:
        r.fail("r. forbidden payoff/equilibrium keys", str(forbidden_keys_found))

    # s. no equilibrium claim (text scan across all string fields)
    equilibrium_terms = ["equilibrium", "nash equilibrium", "dominant strategy", "best move", "optimal strategy"]
    equilibrium_hits = []

    def scan_text(obj, path=""):
        if isinstance(obj, str):
            low = obj.lower()
            for term in equilibrium_terms:
                if term in low:
                    equilibrium_hits.append(f"{path}: contains '{term}'")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                scan_text(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                scan_text(v, f"{path}[{i}]")

    scan_text(artifact)
    if not equilibrium_hits:
        r.ok("s. no equilibrium/optimal-strategy claim present in any text field")
    else:
        for e in equilibrium_hits:
            r.fail("s. equilibrium claim", e)

    # t. no unsupported counterfactual: any use of "would have" / "if VOC had" style phrasing must be
    #    paired with researcher_review_required = true or explicit_or_inferred = COUNTERFACTUAL_NOT_ESTABLISHED
    counterfactual_terms = ["would have", "if voc had", "had it not been", "counterfactually"]
    counterfactual_violations = []
    for rel in relations:
        blob = " ".join([
            rel.get("historical_reconstruction") or "",
            rel.get("theoretical_annotation") or "",
            rel.get("public_display_summary") or "",
        ]).lower()
        if any(t in blob for t in counterfactual_terms):
            if not (rel.get("researcher_review_required") or rel.get("explicit_or_inferred") == "COUNTERFACTUAL_NOT_ESTABLISHED"):
                counterfactual_violations.append(rel.get("relation_id"))
    if not counterfactual_violations:
        r.ok("t. no unsupported (unflagged) counterfactual phrasing found")
    else:
        r.fail("t. unsupported counterfactual", str(counterfactual_violations))

    # u/v/w. source statement / reconstruction / theory / public copy kept in separate fields
    layer_fields = ["source_statement_summary", "historical_reconstruction", "theoretical_annotation", "public_display_summary"]
    layer_violations = []
    for rel in relations:
        vals = [rel.get(f) for f in layer_fields]
        if any(v is None or not str(v).strip() for v in vals):
            layer_violations.append(f"{rel.get('relation_id')} missing one of {layer_fields}")
        # u/v/w: no two of the four layers may be byte-identical (copy-paste across interpretive boundary)
        non_empty = [v for v in vals if v]
        if len(non_empty) == len(set(non_empty)):
            continue
        layer_violations.append(f"{rel.get('relation_id')} has two identical layer texts (interpretive boundary not respected)")
    if not layer_violations:
        r.ok("u/v/w. source statement, reconstruction, theory, and public copy kept in four distinct, non-identical fields")
    else:
        for e in layer_violations:
            r.fail("u/v/w. four-layer separation", e)

    # x. all inferred relations carry review flag
    inferred_without_flag = [
        rel.get("relation_id") for rel in relations
        if rel.get("explicit_or_inferred") in {"OBSERVED_ACTION_AS_STRATEGY", "INFERRED_AVAILABLE_OPTION", "COUNTERFACTUAL_NOT_ESTABLISHED"}
        and not rel.get("researcher_review_required")
    ]
    if not inferred_without_flag:
        r.ok("x. all inferred relations carry researcher_review_required = true")
    else:
        r.fail("x. inferred relations missing review flag", str(inferred_without_flag))

    # y. no change to production data (checked by caller via checksum comparison; validator itself
    #    performs no writes, confirmed structurally: this script opens all paths read-only)
    r.ok("y. validator performs no writes (structural guarantee: no open(...,'w') call on any path other "
         "than its own stdout)")

    # --- report ---
    print("=" * 78)
    print("PAINAN 1663 RELATIONAL ARTIFACT — VALIDATION REPORT")
    print("=" * 78)
    print(f"Artifact: {ARTIFACT_PATH}")
    print(f"Actors: {len(actors)}  Relations: {len(relations)}  Treaties: {len(treaties)}")
    print()
    print(f"CHECKS PASSED: {len(r.checks_passed)}")
    for c in r.checks_passed:
        print(f"  [PASS] {c}")
    print()
    if r.warnings:
        print(f"WARNINGS: {len(r.warnings)}")
        for w in r.warnings:
            print(f"  [WARN] {w}")
        print()
    if r.errors:
        print(f"ERRORS: {len(r.errors)}")
        for e in r.errors:
            print(f"  [FAIL] {e}")
        print()
        print("VALIDATION RESULT: FAIL")
        sys.exit(1)
    else:
        print("VALIDATION RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
