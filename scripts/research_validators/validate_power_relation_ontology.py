#!/usr/bin/env python3
"""Generalized, deterministic validator for Atlas power-relation ontology
artifacts under the frozen Draft V2 contract and the Draft V2.1 design
contract (commit b54c8a6c05b13d75db864d0731105fe276fdce6d).

Governing precedence (highest first): decision ledger, decision audit,
Draft V2.1 contract, frozen Draft V2, changeset ledger, revalidation
matrix, changeset draft recommendations. See
power_relation_ontology_rules.json for the full rule-to-source mapping.

This validator enforces only machine-validatable structural rules. It
never adjudicates whether a historical claim is true, whether an actor
intended an outcome, whether resistance occurred, whether a patron-client
relationship existed, whether effective control existed, whether a source
is trustworthy, or whether an interpretation is persuasive -- those
findings are reported as REQUIRES_RESEARCHER_REVIEW, never fabricated as
PASS or FAIL.

Read-only: this script never writes to, mutates, or migrates any input
file. No network access, no database access, no environment secrets.

Usage:
    python3 validate_power_relation_ontology.py <artifact.json> [--json]
Exit code: 0 only if no ERROR/CRITICAL finding exists; 1 otherwise.
"""
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

MVP_CORE_RELATION = {
    "REQUESTS_PROTECTION_FROM", "PROVIDES_PROTECTION_TO", "REQUIRES_MONOPOLY_FROM", "NEGOTIATES_WITH",
    "RECONCILES_WITH", "SWITCHES_ALIGNMENT_TO", "CLAIMS_JURISDICTION_OVER", "CLAIMS_COMMODITY_MONOPOLY",
    "CONTESTS_SUCCESSION_WITH", "CONTESTS_RESOURCE_WITH", "RECOGNIZES_OFFICE_HOLDER",
    "COLLECTS_TOLL_FROM", "LEASES_RESOURCE_TO", "USES_MILITARY_FORCE_AGAINST",
}
EXTENDED_RESEARCH_RELATION = {"EXERCISES_EFFECTIVE_CONTROL_OVER", "CONTROLS_FORT"}
ALLOWED_RELATION_TYPES = MVP_CORE_RELATION | EXTENDED_RESEARCH_RELATION

RIGHT_MODIFICATION_ACTIONS = {"GRANTS", "WAIVES", "RELEASES", "REVOKES", "RENEWS", "EXEMPTS"}
COERCION_STATUS_VALUES = {"FREE", "COERCED", "CANNOT_DETERMINE"}
ABILITY_TO_REFUSE_VALUES = {"YES", "NO", "CANNOT_DETERMINE"}
VOICE_AVAILABILITY_VALUES = {"DOCUMENTED", "ABSENT", "CANNOT_DETERMINE"}
CONSTRAINED_AGENCY_VALUES = {"CONFIRMED", "SUSPECTED", "NOT_APPLICABLE", "CANNOT_DETERMINE"}
IDENTITY_UNKNOWN_MARKERS = {"CANNOT_DETERMINE", "NOT_TESTABLE", "UNKNOWN"}

RESEARCH_ONLY_PROMOTED_VALUES = {
    "PUBLIC", "PUBLIC_VOCABULARY", "PRODUCTION", "RUNTIME_APPROVED",
    "GRAPHIFY_APPROVED", "FACTUAL_EDGE",
}

CH04_ENTITY_TYPES = {"InstitutionalStateObservation", "InstitutionalPresenceObservation"}
CH05_FORBIDDEN_LOCATION_FIELDS = {"source_place_expression", "feature_type_confidence", "spatial_scope_status"}
CH08_ENTITY_TYPE = "DisputeSettlement"

COMMERCIAL_RIGHT_FIELDS = {
    "right_id", "holder_actor_id", "granting_actor_id", "concerns_relation_type", "commodity",
    "source_document_ids", "source_passage_locator", "event_ids", "parent_episode_ids",
    "provenance_status", "evidence_strength", "interpretive_status", "explicit_or_inferred",
    "researcher_review_required", "valid_from", "valid_to", "date_precision", "open_ended", "public_status",
}
RIGHT_MODIFICATION_FIELDS = {
    "modification_id", "right_id", "action", "acting_actor_id", "affected_actor_id",
    "modification_date", "date_precision", "source_document_ids", "source_passage_locator",
    "event_ids", "parent_episode_ids", "provenance_status", "evidence_strength", "interpretive_status",
    "explicit_or_inferred", "researcher_review_required", "public_status",
}
COMMAND_OBSERVATION_FIELDS = {
    "observation_id", "commanding_actor_id", "commanded_actor_id", "coercion_status", "ability_to_refuse",
    "dependency_status", "voice_availability", "constrained_agency", "political_intent",
    "source_document_ids", "source_passage_locator", "event_ids", "parent_episode_ids",
    "provenance_status", "evidence_strength", "interpretive_status", "explicit_or_inferred",
    "researcher_review_required", "valid_from", "valid_to", "date_precision", "open_ended", "public_status",
}
OPERATION_PARTICIPATION_FIELDS = {
    "participation_id", "command_observation_id", "participant_actor_id", "event_id", "parent_episode_id",
    "role_as_written", "source_document_ids", "source_passage_locator", "provenance_status",
    "evidence_strength", "interpretive_status", "explicit_or_inferred", "researcher_review_required",
    "public_status",
}

SEVERITY_ORDER = {"CRITICAL": 0, "ERROR": 1, "WARNING": 2, "REVIEW": 3, "INFO": 4}
FAILING_SEVERITIES = {"CRITICAL", "ERROR"}


@dataclass
class Finding:
    rule_id: str
    severity: str
    error_code: str | None
    path: str
    message: str


@dataclass
class ValidationResult:
    artifact_path: str
    ontology_version: str | None
    findings: list = field(default_factory=list)

    def add(self, rule_id, severity, error_code, path, message):
        self.findings.append(Finding(rule_id, severity, error_code, path, message))

    @property
    def passed(self):
        return not any(f.severity in FAILING_SEVERITIES for f in self.findings)

    def to_dict(self):
        return {
            "artifact_path": self.artifact_path,
            "ontology_version": self.ontology_version,
            "passed": self.passed,
            "findings": [asdict(f) for f in self.findings],
            "counts": {
                sev: sum(1 for f in self.findings if f.severity == sev)
                for sev in ("CRITICAL", "ERROR", "WARNING", "REVIEW", "INFO")
            },
        }


def _actor_ids(artifact):
    return {a.get("actor_id") for a in artifact.get("actors", []) if isinstance(a, dict)}


def _location_ids(artifact):
    return {loc.get("location_id") for loc in artifact.get("locations", []) if isinstance(loc, dict)}


def _normalize_legacy_version_marker(artifact):
    """Pre-V2.1 artifacts (Koto Tangah/Natal/Sillida/Tiku) carry a legacy
    ``ontology_contract_version`` string instead of this validator's own
    ``ontology_version`` marker. Recognizing that existing marker is a
    version-mapping fix, not a rule relaxation: it changes what counts as
    'declared V2', never what counts as valid V2 content."""
    legacy = artifact.get("ontology_contract_version")
    if isinstance(legacy, str) and legacy.strip().startswith("V2_DRAFT"):
        return "V2"
    return None


def check_version(artifact, result):
    version = artifact.get("ontology_version")
    if version is None:
        version = _normalize_legacy_version_marker(artifact)
        if version is not None:
            result.add("R-SCH-01", "INFO", None, "$.ontology_contract_version",
                        f"No ontology_version field; normalized from legacy ontology_contract_version "
                        f"marker to {version!r}.")
    if version is None:
        result.add("R-SCH-01", "ERROR", "MISSING_ONTOLOGY_VERSION", "$.ontology_version",
                    "Artifact does not declare ontology_version, and no recognized legacy "
                    "ontology_contract_version marker is present either.")
        return None
    if version not in ("V2", "V2.1"):
        result.add("R-SCH-02", "ERROR", "UNKNOWN_ONTOLOGY_VERSION", "$.ontology_version",
                    f"ontology_version={version!r} is not V2 or V2.1.")
        return None
    return version


V2_1_ONLY_TOP_LEVEL_KEYS = (
    "commercial_rights", "right_modifications", "command_observations", "operation_participations",
)


def check_backward_compatibility(artifact, version, result):
    if version != "V2":
        return
    present = [k for k in V2_1_ONLY_TOP_LEVEL_KEYS if artifact.get(k)]
    for actor in artifact.get("actors", []):
        if any(k in actor for k in ("mandate_status", "mandate_scope", "identity_continuity_status",
                                     "explicit_non_identity_with")):
            present.append(f"actors[{actor.get('actor_id')}].<v2.1 field>")
    for rel in artifact.get("relations", []):
        rc = rel.get("resistance_candidate")
        if isinstance(rc, dict) and "resistance_target_actor_id" in rc:
            present.append(f"relations[{rel.get('relation_id')}].resistance_candidate.resistance_target_actor_id")
    if present:
        result.add("R-BC-02", "ERROR", "AMBIGUOUS_VERSION_DECLARATION", "$",
                    f"ontology_version=V2 but V2.1-only constructs present: {present}")
    else:
        result.add("R-BC-01", "INFO", None, "$.ontology_version",
                    "V2 artifact carries no V2.1 constructs -- backward compatible by construction.")


def check_relation_types(artifact, result):
    for rel in artifact.get("relations", []):
        rt = rel.get("relation_type")
        if rt not in ALLOWED_RELATION_TYPES:
            result.add("R-VOC-06", "ERROR", "UNAPPROVED_RELATION_TYPE",
                        f"relations[{rel.get('relation_id')}].relation_type",
                        f"relation_type={rt!r} is outside the closed 16-value V2/V2.1 vocabulary.")


def check_relation_endpoints(artifact, result):
    known = _actor_ids(artifact) | _location_ids(artifact)
    for rel in artifact.get("relations", []):
        for endpoint_key in ("subject_actor_id", "object_id"):
            val = rel.get(endpoint_key)
            if val is not None and val not in known:
                result.add("R-REF-05", "ERROR", "ORPHAN_RELATION_ENDPOINT",
                            f"relations[{rel.get('relation_id')}].{endpoint_key}",
                            f"{endpoint_key}={val!r} does not reference a known actor_id/location_id.")


def check_relation_temporal(artifact, result):
    for rel in artifact.get("relations", []):
        path = f"relations[{rel.get('relation_id')}]"
        for code, sev, ec, p, msg in check_temporal(artifact, path, rel):
            result.add(code, sev, ec, p, msg)


def check_temporal(artifact, path_prefix, obj):
    findings = []
    has_from = obj.get("valid_from") is not None
    has_to = obj.get("valid_to") is not None
    if (has_from or has_to) and not obj.get("date_precision"):
        findings.append(("R-TMP-01", "ERROR", "INVALID_TEMPORAL_RANGE", path_prefix,
                          "valid_from/valid_to present without date_precision."))
    if "open_ended" in obj and not isinstance(obj.get("open_ended"), bool):
        findings.append(("R-TMP-01", "ERROR", "INVALID_TEMPORAL_RANGE", path_prefix,
                          "open_ended must be boolean when present."))
    return findings


def check_actors_v2_1(artifact, result):
    for actor in artifact.get("actors", []):
        aid = actor.get("actor_id")
        for f in ("mandate_status", "mandate_scope"):
            if f in actor:
                val = actor.get(f)
                if val == "":
                    result.add("R-TMP-02", "ERROR", "UNBOUNDED_MANDATE_FIELD", f"actors[{aid}].{f}",
                                f"{f} is present but empty -- must remain bounded, not blank.")
                elif val not in IDENTITY_UNKNOWN_MARKERS:
                    result.add("R-HRV-02", "REVIEW", None, f"actors[{aid}].{f}",
                                f"{f}={val!r} requires researcher review -- not auto-classified.")
        ics = actor.get("identity_continuity_status")
        if ics is not None and ics not in IDENTITY_UNKNOWN_MARKERS:
            result.add("R-HRV-02", "REVIEW", None, f"actors[{aid}].identity_continuity_status",
                        f"identity_continuity_status={ics!r} requires researcher review.")

        non_identity = actor.get("explicit_non_identity_with")
        if non_identity is not None:
            if not isinstance(non_identity, list):
                result.add("R-CARD-01", "ERROR", "INVALID_NON_IDENTITY_CARDINALITY",
                            f"actors[{aid}].explicit_non_identity_with",
                            "explicit_non_identity_with must be a list of {actor_id, rationale}.")
            else:
                for entry in non_identity:
                    other = entry.get("actor_id") if isinstance(entry, dict) else None
                    if other == aid:
                        result.add("R-REF-04", "ERROR", "INVALID_NON_IDENTITY_REFERENCE",
                                    f"actors[{aid}].explicit_non_identity_with",
                                    "An actor must not list itself as non-identical.")
                    elif other not in _actor_ids(artifact):
                        result.add("R-REF-04", "ERROR", "INVALID_NON_IDENTITY_REFERENCE",
                                    f"actors[{aid}].explicit_non_identity_with",
                                    f"references unknown actor_id={other!r}.")

        pub = actor.get("public_status")
        if pub is not None and pub in RESEARCH_ONLY_PROMOTED_VALUES:
            result.add("R-RO-02", "CRITICAL", "RESEARCH_ONLY_BOUNDARY_VIOLATION",
                        f"actors[{aid}].public_status",
                        f"Actor identity-continuity fields attempted promotion to {pub!r}.")

    # symmetry check across the whole actor set (R-REF-04 continued)
    by_id = {a.get("actor_id"): a for a in artifact.get("actors", []) if isinstance(a, dict)}
    for aid, actor in by_id.items():
        for entry in actor.get("explicit_non_identity_with") or []:
            if not isinstance(entry, dict):
                continue
            other = entry.get("actor_id")
            other_actor = by_id.get(other)
            if other_actor is None:
                continue
            back_refs = {e.get("actor_id") for e in (other_actor.get("explicit_non_identity_with") or [])
                         if isinstance(e, dict)}
            if aid not in back_refs:
                result.add("R-REF-04", "ERROR", "INVALID_NON_IDENTITY_REFERENCE",
                            f"actors[{aid}].explicit_non_identity_with",
                            f"asymmetric: {aid} lists {other} but {other} does not list {aid} back.")


def check_resistance_candidate(artifact, result):
    for rel in artifact.get("relations", []):
        rc = rel.get("resistance_candidate")
        if not isinstance(rc, dict):
            continue
        target = rc.get("resistance_target_actor_id")
        if target is None:
            continue
        if isinstance(target, list):
            result.add("R-CARD-02", "ERROR", "INVALID_RESISTANCE_TARGET_CARDINALITY",
                        f"relations[{rel.get('relation_id')}].resistance_candidate.resistance_target_actor_id",
                        "resistance_target_actor_id must be a single actor_id, not a list.")
            continue
        if target not in _actor_ids(artifact):
            result.add("R-REF-06", "ERROR", "ORPHAN_RESISTANCE_TARGET_REFERENCE",
                        f"relations[{rel.get('relation_id')}].resistance_candidate.resistance_target_actor_id",
                        f"references unknown actor_id={target!r}.")
        pub = rc.get("public_status")
        if pub is not None and pub in RESEARCH_ONLY_PROMOTED_VALUES:
            result.add("R-RO-02", "CRITICAL", "RESEARCH_ONLY_BOUNDARY_VIOLATION",
                        f"relations[{rel.get('relation_id')}].resistance_candidate.public_status",
                        f"resistance_target_actor_id attempted promotion to {pub!r}.")


def _check_extra_fields(rule_id, allowed_fields, path, obj, result):
    extra = set(obj.keys()) - allowed_fields
    if extra:
        result.add(rule_id, "ERROR", "UNAUTHORIZED_EXTRA_FIELD", path,
                    f"Unrecognized field(s) not in the frozen V2.1 contract field set: {sorted(extra)}.")


def _check_provenance(path, obj, result):
    sdi = obj.get("source_document_ids")
    if not sdi:
        result.add("R-PROV-01", "ERROR", "MISSING_PROVENANCE", path,
                    "source_document_ids missing or empty.")
    if "researcher_review_required" not in obj or not isinstance(obj.get("researcher_review_required"), bool):
        result.add("R-PROV-02", "ERROR", "MISSING_RESEARCHER_REVIEW_FLAG", path,
                    "researcher_review_required must be present and boolean.")


def _check_public_status(rule_id, path, obj, result):
    pub = obj.get("public_status")
    if pub is not None and pub in RESEARCH_ONLY_PROMOTED_VALUES:
        result.add(rule_id, "CRITICAL", "RESEARCH_ONLY_BOUNDARY_VIOLATION", path,
                    f"Attempted promotion to {pub!r}; must remain RESEARCH_ONLY.")


def check_commercial_rights(artifact, result):
    right_ids = set()
    for cr in artifact.get("commercial_rights", []):
        rid = cr.get("right_id")
        right_ids.add(rid)
        path = f"commercial_rights[{rid}]"
        _check_extra_fields("R-SCH-03", COMMERCIAL_RIGHT_FIELDS, path, cr, result)
        _check_provenance(path, cr, result)
        _check_public_status("R-RO-01", f"{path}.public_status", cr, result)
        for code, sev, ec, p, msg in check_temporal(artifact, path, cr):
            result.add(code, sev, ec, p, msg)
        crt = cr.get("concerns_relation_type")
        if crt is not None and crt not in ALLOWED_RELATION_TYPES:
            result.add("R-VOC-06", "ERROR", "UNAPPROVED_RELATION_TYPE", f"{path}.concerns_relation_type",
                        f"concerns_relation_type={crt!r} is outside the closed vocabulary.")
    return right_ids


def check_right_modifications(artifact, right_ids, result):
    for rm in artifact.get("right_modifications", []):
        mid = rm.get("modification_id")
        path = f"right_modifications[{mid}]"
        _check_extra_fields("R-SCH-03", RIGHT_MODIFICATION_FIELDS, path, rm, result)
        _check_provenance(path, rm, result)
        _check_public_status("R-RO-01", f"{path}.public_status", rm, result)
        action = rm.get("action")
        if action not in RIGHT_MODIFICATION_ACTIONS:
            result.add("R-VOC-01", "ERROR", "INVALID_RIGHT_MODIFICATION_ACTION", f"{path}.action",
                        f"action={action!r} is not one of {sorted(RIGHT_MODIFICATION_ACTIONS)}.")
        rid = rm.get("right_id")
        if rid not in right_ids:
            result.add("R-REF-01", "ERROR", "ORPHAN_RIGHT_MODIFICATION_REFERENCE", f"{path}.right_id",
                        f"right_id={rid!r} does not reference an existing CommercialRight in this artifact.")


def check_command_observations(artifact, result):
    observation_ids = set()
    relation_pairs = {
        (rel.get("subject_actor_id"), rel.get("object_id")) for rel in artifact.get("relations", [])
    }
    for co in artifact.get("command_observations", []):
        oid = co.get("observation_id")
        observation_ids.add(oid)
        path = f"command_observations[{oid}]"
        _check_extra_fields("R-SCH-03", COMMAND_OBSERVATION_FIELDS, path, co, result)
        _check_provenance(path, co, result)
        _check_public_status("R-RO-01", f"{path}.public_status", co, result)
        for code, sev, ec, p, msg in check_temporal(artifact, path, co):
            result.add(code, sev, ec, p, msg)

        cs = co.get("coercion_status")
        if cs not in COERCION_STATUS_VALUES:
            result.add("R-VOC-02", "ERROR", "INVALID_COERCION_STATUS", f"{path}.coercion_status",
                        f"coercion_status={cs!r} is not one of {sorted(COERCION_STATUS_VALUES)}.")
        atr = co.get("ability_to_refuse")
        if atr not in ABILITY_TO_REFUSE_VALUES:
            result.add("R-VOC-03", "ERROR", "INVALID_ABILITY_TO_REFUSE", f"{path}.ability_to_refuse",
                        f"ability_to_refuse={atr!r} is not one of {sorted(ABILITY_TO_REFUSE_VALUES)}.")
        va = co.get("voice_availability")
        if va not in VOICE_AVAILABILITY_VALUES:
            result.add("R-VOC-04", "ERROR", "INVALID_VOICE_AVAILABILITY", f"{path}.voice_availability",
                        f"voice_availability={va!r} is not one of {sorted(VOICE_AVAILABILITY_VALUES)}.")
        ca = co.get("constrained_agency")
        if ca not in CONSTRAINED_AGENCY_VALUES:
            result.add("R-VOC-05", "ERROR", "INVALID_CONSTRAINED_AGENCY", f"{path}.constrained_agency",
                        f"constrained_agency={ca!r} is not one of {sorted(CONSTRAINED_AGENCY_VALUES)}.")
        pi = co.get("political_intent")
        if not isinstance(pi, str) or pi == "":
            result.add("R-VOC-07", "ERROR", "POLITICAL_INTENT_NOT_FREE_TEXT", f"{path}.political_intent",
                        "political_intent must be a non-empty free-text string.")
        elif pi != "CANNOT_DETERMINE":
            result.add("R-HRV-01", "REVIEW", None, f"{path}.political_intent",
                        "political_intent content requires researcher review -- no automated verdict computed.")

        pair = (co.get("commanding_actor_id"), co.get("commanded_actor_id"))
        if pair in relation_pairs or (pair[1], pair[0]) in relation_pairs:
            result.add("R-REF-03", "CRITICAL", "CONSTRAINED_AGENCY_RELATION_COLLISION", path,
                        f"Actor pair {pair} appears both as a CommandObservation subject/object AND as a "
                        "directed relation's subject/object -- this is exactly the consent-implying "
                        "misuse the entity split was designed to foreclose.")
    return observation_ids


def check_operation_participations(artifact, observation_ids, result):
    for op in artifact.get("operation_participations", []):
        pid = op.get("participation_id")
        path = f"operation_participations[{pid}]"
        _check_extra_fields("R-SCH-03", OPERATION_PARTICIPATION_FIELDS, path, op, result)
        _check_provenance(path, op, result)
        _check_public_status("R-RO-01", f"{path}.public_status", op, result)
        coid = op.get("command_observation_id")
        if coid not in observation_ids:
            result.add("R-REF-02", "ERROR", "ORPHAN_OPERATION_PARTICIPATION_REFERENCE",
                        f"{path}.command_observation_id",
                        f"command_observation_id={coid!r} does not reference an existing CommandObservation.")


def check_exclusions(artifact, result):
    for key, label in (("institutional_observations", "institutional_observations"),
                        ("dispute_settlements", "dispute_settlements")):
        for i, entry in enumerate(artifact.get(key, [])):
            etype = entry.get("entity_type") if isinstance(entry, dict) else None
            path = f"{label}[{i}]"
            if etype in CH04_ENTITY_TYPES:
                result.add("R-EXC-01", "ERROR", "DEFERRED_STRUCTURE_NOT_AUTHORIZED", path,
                            f"entity_type={etype!r} is CH-04 (DEC-05/DEC-06 DEFERRED) -- not authorized in V2.1.")
            elif etype == CH08_ENTITY_TYPE:
                result.add("R-EXC-03", "ERROR", "DEFERRED_STRUCTURE_NOT_AUTHORIZED", path,
                            "entity_type=DisputeSettlement is CH-08 (DEC-11 DEFERRED) -- not authorized in V2.1.")

    for i, loc in enumerate(artifact.get("locations", [])):
        if not isinstance(loc, dict):
            continue
        bad = set(loc.keys()) & CH05_FORBIDDEN_LOCATION_FIELDS
        if bad:
            result.add("R-EXC-02", "ERROR", "REJECTED_STRUCTURE_NOT_AUTHORIZED", f"locations[{i}]",
                        f"field(s) {sorted(bad)} are CH-05 (DEC-07 REJECTED) -- not authorized in any version.")


def check_interpretive_review_flags(artifact, result):
    for rel in artifact.get("relations", []):
        rid = rel.get("relation_id")
        for field_name in ("interpretive_status", "claim_or_effective_control", "patron_client_classification"):
            if field_name in rel:
                result.add("R-HRV-03", "REVIEW", None, f"relations[{rid}].{field_name}",
                            f"{field_name} conformance checked structurally only; the underlying historical "
                            "claim is not adjudicated by this validator.")


def validate_artifact(artifact, artifact_path):
    result = ValidationResult(artifact_path=str(artifact_path), ontology_version=None)
    version = check_version(artifact, result)
    result.ontology_version = version
    if version is None:
        return result

    check_backward_compatibility(artifact, version, result)
    check_relation_types(artifact, result)
    check_relation_endpoints(artifact, result)
    check_relation_temporal(artifact, result)
    check_exclusions(artifact, result)
    check_interpretive_review_flags(artifact, result)

    if version == "V2.1":
        check_actors_v2_1(artifact, result)
        check_resistance_candidate(artifact, result)
        right_ids = check_commercial_rights(artifact, result)
        check_right_modifications(artifact, right_ids, result)
        observation_ids = check_command_observations(artifact, result)
        check_operation_participations(artifact, observation_ids, result)

    return result


def format_human(result: ValidationResult) -> str:
    lines = [f"Artifact: {result.artifact_path}", f"ontology_version: {result.ontology_version}"]
    for f in sorted(result.findings, key=lambda x: SEVERITY_ORDER.get(x.severity, 9)):
        code = f" [{f.error_code}]" if f.error_code else ""
        lines.append(f"  [{f.severity}]{code} {f.path}: {f.message} (rule={f.rule_id})")
    counts = result.to_dict()["counts"]
    lines.append(
        "Counts: " + ", ".join(f"{k}={v}" for k, v in counts.items())
    )
    lines.append("VALIDATION RESULT: " + ("PASS" if result.passed else "FAIL"))
    return "\n".join(lines)


def main(argv):
    if len(argv) < 2:
        print("usage: validate_power_relation_ontology.py <artifact.json> [--json]", file=sys.stderr)
        return 2
    path = Path(argv[1])
    as_json = "--json" in argv[2:]
    try:
        artifact = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        result = ValidationResult(artifact_path=str(path), ontology_version=None)
        result.add("R-SCH-01", "ERROR", "MALFORMED_JSON", "$", f"JSON parse error: {e}")
        if as_json:
            print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_human(result))
        return 1

    result = validate_artifact(artifact, path)
    if as_json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(format_human(result))
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
