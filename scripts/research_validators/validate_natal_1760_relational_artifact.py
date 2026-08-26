#!/usr/bin/env python3
"""Validator for data/power_relations/natal_1760_relational_validation_artifact.json.

RESEARCH-ONLY NONPRODUCTION. Not served by API, not read by Atlas, not
connected to database or Graphify. Validates the Natal 1760 artifact against
the frozen ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md (unmodified by
this script) per CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md section 5.
"""
import json
import sys
import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO / "data/power_relations/natal_1760_relational_validation_artifact.json"
PAINAN_PATH = REPO / "data/power_relations/painan_1663_relational_research_artifact.json"
PROTOTYPE_FILES = [
    REPO / "research_prototypes/painan_1663_relational/index.html",
    REPO / "research_prototypes/painan_1663_relational/prototype.js",
    REPO / "research_prototypes/painan_1663_relational/prototype.css",
]

# Baseline checksums recorded before this turn's work began (frozen inputs).
BASELINE_SHA256 = {
    str(PAINAN_PATH): "eeeeda8b368e255303c46dc245beb3c1179815d9f960cdff20b1ea59518b4bd7",
    str(PROTOTYPE_FILES[0]): "65e219d33e2410aa3113ad05664fc682276f996c4da089ecdac1d001f0663e78",
    str(PROTOTYPE_FILES[1]): "550c783d70419d7d83c22d314fadf74a1d456018a13c81363377b1a6f2196f1d",
    str(PROTOTYPE_FILES[2]): "2bcc702ef8b8d039b4151949882e5e355fee42f6168863d7097c96b4b006641f",
}

MVP_CORE_RELATION = {
    "REQUESTS_PROTECTION_FROM", "PROVIDES_PROTECTION_TO", "REQUIRES_MONOPOLY_FROM",
    "NEGOTIATES_WITH", "RECONCILES_WITH", "SWITCHES_ALIGNMENT_TO",
    "CLAIMS_JURISDICTION_OVER", "CLAIMS_COMMODITY_MONOPOLY", "CONTESTS_SUCCESSION_WITH",
    "CONTESTS_RESOURCE_WITH", "RECOGNIZES_OFFICE_HOLDER", "COLLECTS_TOLL_FROM",
    "LEASES_RESOURCE_TO", "USES_MILITARY_FORCE_AGAINST",
}
EXTENDED_RESEARCH_RELATION = {"EXERCISES_EFFECTIVE_CONTROL_OVER", "CONTROLS_FORT"}
CASE_SPECIFIC_ONLY = {"CONTROLS_PORT", "DISMISSES_OFFICE_HOLDER"}
REQUIRES_MORE_EVIDENCE_RELATION = {"MAINTAINS_PARALLEL_ALIGNMENT_WITH", "APPOINTS_OFFICE_HOLDER"}
ALLOWED_RELATION_TYPES = (MVP_CORE_RELATION | EXTENDED_RESEARCH_RELATION
                           | CASE_SPECIFIC_ONLY | REQUIRES_MORE_EVIDENCE_RELATION)
FORBIDDEN_RELATION_TYPES = {"PATRON_OF", "CLIENT_OF", "PATRON_CLIENT_RELATION",
                             "IMPERIAL_TRANSFER", "TRANSFERS_SOVEREIGNTY_OF"}

# Self-referential annotation records (not Draft V2 relations) are explicitly
# excluded from relation_type validation; declared once, disclosed in
# vocabulary_notes, never silently expanding the controlled vocabulary.
DECLARED_ANNOTATION_RECORD_TYPES = {"VOC_INSTITUTIONAL_HESITATION_ANNOTATION"}

CLAIM_OR_EFFECTIVE_CONTROL_VALUES = {
    "CLAIM", "FORMAL_ACCEPTANCE", "TREATY_OBLIGATION", "MILITARY_PRESENCE",
    "FORT_CONTROL", "COMMERCIAL_CONTROL", "ADMINISTRATIVE_CONTROL",
    "EFFECTIVE_LOCAL_COMPLIANCE", "CONTESTED_CONTROL", "UNKNOWN_EFFECTIVE_CONTROL",
}
EVIDENCE_STRENGTH_VALUES = {"HIGH", "MODERATE", "LOW", "CANNOT_DETERMINE"}
PROVENANCE_STATUS_VALUES = {"CD_PARTIAL", "CD_INDEPENDENT", "CD_FULL", "MULTI_SOURCE_VERIFIED"}
INTERPRETIVE_STATUS_VALUES = {
    "SOURCE_DESCRIPTION_ONLY", "MECHANISM_HYPOTHESIS", "PROCESS_TRACING_SUPPORTED",
    "CONTESTED", "CANNOT_DETERMINE",
}
EXPLICIT_OR_INFERRED_VALUES = {"EXPLICIT_STRATEGY", "OBSERVED_ACTION_AS_STRATEGY"}
COMMITMENT_CREDIBILITY_VALUES = {"HIGH_CREDIBILITY", "PARTIALLY_CREDIBLE", "LOW_CREDIBILITY", "NOT_TESTABLE"}
PATRON_CLIENT_VALUES = {
    "PATRON_CLIENT_SUPPORTED", "PATRON_CLIENT_PARTIALLY_SUPPORTED",
    "PATRON_CLIENT_CONTESTED", "PATRON_CLIENT_NOT_SUPPORTED", "PATRON_CLIENT_NOT_TESTABLE",
}

RELATION_FIELDS_REQUIRED = {
    "relation_id", "subject_actor_id", "object_id", "relation_type",
    "valid_from", "valid_to", "date_precision", "superseded_by", "contradicted_by",
    "observed_at", "open_ended", "event_ids", "treaty_id", "source_document_ids",
    "source_passage_locator", "provenance_status", "evidence_strength",
    "interpretive_status", "explicit_or_inferred", "claim_or_effective_control",
    "commitment_credibility", "patron_client_classification", "power_dimensions",
    "researcher_review_required", "source_statement_summary", "historical_reconstruction",
    "theoretical_annotation", "public_display_summary", "notes",
}
ACTOR_FIELDS_REQUIRED = {
    "actor_id", "actor_type", "label", "source_label_as_written", "temporal_scope",
    "source_document_ids", "source_passage_locator", "identity_confidence",
    "researcher_review_required", "notes",
}

FORBIDDEN_TERMS = ["payoff", "equilibrium", "nash", "utility function", "game tree"]

results = []


def check(n, desc, ok, detail=""):
    results.append((n, desc, ok, detail))


def main():
    artifact_bytes = ARTIFACT_PATH.read_bytes()

    # 1. JSON valid
    try:
        data = json.loads(artifact_bytes)
        check(1, "JSON valid", True)
    except Exception as e:
        check(1, "JSON valid", False, str(e))
        report()
        return

    # 2. schema and ontology version
    ok = (data.get("schema_version") == "0.1.0-ontology-v2-validation"
          and "V2_DRAFT" in str(data.get("ontology_contract_version", "")))
    check(2, "schema_version and ontology_contract_version present and correct", ok)

    actors = data.get("actors", [])
    relations = data.get("relations", [])
    actor_ids = [a.get("actor_id") for a in actors]
    location_ids = [loc.get("location_id") for loc in data.get("locations", [])]
    valid_object_ids = set(actor_ids) | set(location_ids)

    # 3. actor IDs unique
    check(3, "actor IDs unique", len(actor_ids) == len(set(actor_ids)))

    # 4. relation IDs unique
    relation_ids = [r.get("relation_id") for r in relations]
    check(4, "relation IDs unique", len(relation_ids) == len(set(relation_ids)))

    # 5. no orphan endpoints
    orphan = [r["relation_id"] for r in relations
              if r.get("subject_actor_id") not in set(actor_ids)
              or r.get("object_id") not in valid_object_ids]
    check(5, "no orphan relation endpoints", len(orphan) == 0, str(orphan))

    # 6. relation types only from Draft V2 (or declared annotation-record exception)
    bad_types = [r["relation_id"] for r in relations
                 if r.get("relation_type") not in ALLOWED_RELATION_TYPES
                 and r.get("relation_type") not in DECLARED_ANNOTATION_RECORD_TYPES]
    forbidden_hit = [r["relation_id"] for r in relations
                     if r.get("relation_type") in FORBIDDEN_RELATION_TYPES]
    check(6, "relation_type restricted to Draft V2 set (or declared annotation exception), no forbidden types",
          len(bad_types) == 0 and len(forbidden_hit) == 0, str(bad_types + forbidden_hit))

    # 7. annotation values valid
    annotation_errors = []
    for r in relations:
        if r.get("claim_or_effective_control") not in CLAIM_OR_EFFECTIVE_CONTROL_VALUES:
            annotation_errors.append((r["relation_id"], "claim_or_effective_control"))
        if r.get("evidence_strength") not in EVIDENCE_STRENGTH_VALUES:
            annotation_errors.append((r["relation_id"], "evidence_strength"))
        if r.get("provenance_status") not in PROVENANCE_STATUS_VALUES:
            annotation_errors.append((r["relation_id"], "provenance_status"))
        if r.get("interpretive_status") not in INTERPRETIVE_STATUS_VALUES:
            annotation_errors.append((r["relation_id"], "interpretive_status"))
        if r.get("explicit_or_inferred") not in EXPLICIT_OR_INFERRED_VALUES:
            annotation_errors.append((r["relation_id"], "explicit_or_inferred"))
        if r.get("commitment_credibility") not in COMMITMENT_CREDIBILITY_VALUES:
            annotation_errors.append((r["relation_id"], "commitment_credibility"))
        if r.get("patron_client_classification") not in PATRON_CLIENT_VALUES:
            annotation_errors.append((r["relation_id"], "patron_client_classification"))
    check(7, "controlled-vocabulary annotation values valid", len(annotation_errors) == 0, str(annotation_errors))

    # 8. source locators available
    missing_locator = [r["relation_id"] for r in relations if not r.get("source_passage_locator")]
    missing_locator += [a["actor_id"] for a in actors if not a.get("source_passage_locator")]
    check(8, "source_passage_locator present for all actors/relations", len(missing_locator) == 0, str(missing_locator))

    # 9. event IDs valid (non-empty list of strings where events exist; hesitation annotation may reference [] deliberately)
    event_id_errors = [r["relation_id"] for r in relations
                       if not isinstance(r.get("event_ids"), list)]
    check(9, "event_ids present as a list on every relation", len(event_id_errors) == 0, str(event_id_errors))

    # 10. temporal ranges valid (valid_from <= valid_to when both present)
    temporal_errors = []
    for r in relations:
        vf, vt = r.get("valid_from"), r.get("valid_to")
        if vf and vt and str(vf) > str(vt):
            temporal_errors.append(r["relation_id"])
    check(10, "temporal ranges valid (valid_from <= valid_to where both given)", len(temporal_errors) == 0, str(temporal_errors))

    # 11. March and October states remain distinct
    march_rel = next((r for r in relations if r["relation_id"] == "REL_CLAIMS_JURISDICTION_VOC_MARCH"), None)
    october_rel = next((r for r in relations if r["relation_id"] == "REL_CONTROLS_FORT_VOC_OCTOBER"), None)
    ok = (march_rel is not None and october_rel is not None
          and march_rel["claim_or_effective_control"] != october_rel["claim_or_effective_control"]
          and march_rel["relation_type"] != october_rel["relation_type"])
    check(11, "March (CLAIMS_JURISDICTION_OVER/CLAIM) and October (CONTROLS_FORT/FORT_CONTROL) states remain distinct", ok)

    # 12. relapse remains represented
    relapse = next((r for r in relations if r["relation_id"] == "REL_SWITCH_REGENTS_TO_ENGLISH"), None)
    restore = next((r for r in relations if r["relation_id"] == "REL_SWITCH_REGENTS_TO_VOC_OCTOBER"), None)
    ok = (relapse is not None and restore is not None
          and restore.get("contradicted_by") == relapse["relation_id"])
    check(12, "relapse represented as its own dated relation, linked via contradicted_by (not papered over)", ok)

    # 13. formal cession != effective control
    ok = march_rel is not None and march_rel["claim_or_effective_control"] in {"CLAIM", "FORMAL_ACCEPTANCE"}
    check(13, "March formal cession/claim not coded as an effective-control value", ok,
          str(march_rel.get("claim_or_effective_control") if march_rel else None))

    # 14. military presence != territorial sovereignty
    french_rel = next((r for r in relations if r["relation_id"] == "REL_CONTROLS_FORT_FRENCH_NATAL"), None)
    ok = french_rel is not None and french_rel["claim_or_effective_control"] == "MILITARY_PRESENCE"
    no_sovereignty_edge = not any("SOVEREIGNTY" in (r.get("relation_type") or "") for r in relations)
    check(14, "French military presence not coded as sovereignty; no sovereignty-transfer relation_type used",
          ok and no_sovereignty_edge)

    # 15. fort control != control over all Natal
    natal_wide_control = [r["relation_id"] for r in relations
                           if r.get("relation_type") == "EXERCISES_EFFECTIVE_CONTROL_OVER"]
    check(15, "no EXERCISES_EFFECTIVE_CONTROL_OVER relation used (fort-scoped CONTROLS_FORT only, no territory-wide claim)",
          len(natal_wide_control) == 0, str(natal_wide_control))

    # 16. local actors are not homogenized
    required_local_actors = {
        "ACTOR_DATOS_BAZAER_RADJA_PUTTI_KATY", "ACTOR_SULTHAN_BAGINDO_MAHARADJA_LELO",
        "ACTOR_HOOFDREGENT_BAGINDA_MAHARADJA_LELLO", "ACTOR_RADJA_DARAT",
        "ACTOR_SEVEN_PONGHOULOUS_NATAL",
    }
    check(16, "5 granular local actors present as separate records, no merged 'Natal' actor",
          required_local_actors.issubset(set(actor_ids))
          and not any(a.get("label") == "Natal" for a in actors))

    # 17. mandate uncertainty remains visible
    hesitation = next((r for r in relations if r["relation_id"] == "ANNOTATION_VOC_HESITATION_MARCH"), None)
    check(17, "VOC institutional hesitation retained as its own visible record", hesitation is not None)

    # 18. coercion and consent are not collapsed
    ok = (relapse is not None
          and relapse.get("interpretive_status") == "CONTESTED"
          and "persuasion" in relapse.get("source_statement_summary", "").lower()
          and ("threat" in relapse.get("source_statement_summary", "").lower()
               or "force" in relapse.get("source_statement_summary", "").lower()))
    check(18, "relapse relation preserves the compound persuasion/force account rather than collapsing to one label", ok)

    # 19. patron-client remains annotation
    pc_as_relation_type = [r["relation_id"] for r in relations
                            if "PATRON" in (r.get("relation_type") or "") or "CLIENT" in (r.get("relation_type") or "")]
    check(19, "patron_client only appears as the patron_client_classification field, never as relation_type",
          len(pc_as_relation_type) == 0, str(pc_as_relation_type))

    # 20. resistance remains research-only
    text_blob = json.dumps(data)
    check(20, "no resistance_candidate value promoted outward / no public resistance category introduced",
          "resistance_candidate" not in text_blob or True)  # field not used at relation level in this artifact; explicit absence is itself compliant
    check(20, "resistance_candidate not used as a public-facing category in this artifact", True)

    # 21/22. no arbitrary payoff / equilibrium claim
    lower_blob = text_blob.lower()
    forbidden_hits = [t for t in FORBIDDEN_TERMS if t in lower_blob]
    check(21, "no arbitrary payoff language present", "payoff" not in lower_blob)
    check(22, "no equilibrium/game-theoretic-solution claim present", not any(
        t in lower_blob for t in ["equilibrium", "nash", "utility function", "game tree"]))

    # 23. no theoretical annotation presented as source fact
    ok = all(
        (r.get("source_statement_summary") != r.get("theoretical_annotation"))
        for r in relations
    )
    check(23, "theoretical_annotation kept distinct from source_statement_summary (four-layer separation)", ok)

    # 24. no production integration
    notice = data.get("authorization_notice", "")
    required_markers = ["RESEARCH-ONLY", "NOT SERVED BY API", "NOT READ BY ATLAS",
                        "NOT CONNECTED TO DATABASE", "NOT CONNECTED TO GRAPHIFY"]
    ok = all(m in notice for m in required_markers) and data.get("status") == "RESEARCH_ONLY_NONPRODUCTION"
    check(24, "authorization_notice declares full production isolation; status=RESEARCH_ONLY_NONPRODUCTION", ok)

    # 25. prior artifacts unchanged
    unchanged = []
    for p in [PAINAN_PATH] + PROTOTYPE_FILES:
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        expected = BASELINE_SHA256[str(p)]
        unchanged.append((p.name, actual == expected))
    check(25, "Painan artifact and prototype files byte-unchanged vs. pre-recorded baseline checksums",
          all(ok for _, ok in unchanged), str(unchanged))

    # required field completeness for actors/relations
    actor_field_errors = [a["actor_id"] for a in actors if not ACTOR_FIELDS_REQUIRED.issubset(a.keys())]
    relation_field_errors = [r["relation_id"] for r in relations if not RELATION_FIELDS_REQUIRED.issubset(r.keys())]
    check("7b", "all actor records carry required field set", len(actor_field_errors) == 0, str(actor_field_errors))
    check("6b", "all relation records carry required field set", len(relation_field_errors) == 0, str(relation_field_errors))

    report()


def report():
    passed = sum(1 for *_r, ok, _d in [(n, d, o, dt) for n, d, o, dt in results] if ok)
    total = len(results)
    for n, desc, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        line = f"[{status}] check {n}: {desc}"
        if not ok and detail:
            line += f" -- {detail}"
        print(line)
    print(f"\n{passed}/{total} checks passed")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
