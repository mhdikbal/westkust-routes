#!/usr/bin/env python3
"""Validator for data/power_relations/tiku_1625_1740_relational_validation_artifact.json.

RESEARCH-ONLY NONPRODUCTION. Not served by API, not read by Atlas, not
connected to database or Graphify. Validates the Tiku V3 artifact against
the frozen ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md (unmodified
by this script), per the V3 ontology stress-test instructions.

Dependency policy mirrors the corrected Koto Tangah V2 validator's
environment contract: SYNCED_FROZEN_DEPENDENCIES (committed, must exist and
checksum-match everywhere) are kept separate from LOCAL_ONLY_FROZEN_DEPENDENCIES
(the interpretive ledger -- gitignored, nonproduction, not expected on a
server checkout; its absence there is NOT_APPLICABLE_ON_SERVER, never a
silent content PASS).
"""
import json
import sys
import csv
import io
import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO / "data/power_relations/tiku_1625_1740_relational_validation_artifact.json"

SYNCED_FROZEN_DEPENDENCIES = [
    REPO / "data/power_relations/painan_1663_relational_research_artifact.json",
    REPO / "data/power_relations/natal_1760_relational_validation_artifact.json",
    REPO / "data/power_relations/koto_tangah_destruction_cycle_relational_validation_artifact.json",
    REPO / "docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md",
    REPO / "research_prototypes/painan_1663_relational/index.html",
    REPO / "research_prototypes/painan_1663_relational/prototype.js",
    REPO / "research_prototypes/painan_1663_relational/prototype.css",
    REPO / "docs/thesis/pilot_annotation/CROSS_CASE_POWER_ONTOLOGY_REVIEW.md",
    REPO / "docs/thesis/pilot_annotation/CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md",
    REPO / "docs/thesis/colab/CROSS_CASE_ENTITY_DECISION_LEDGER.csv",
    REPO / "docs/thesis/colab/CROSS_CASE_RELATION_DECISION_LEDGER.csv",
    REPO / "docs/thesis/colab/CROSS_CASE_ANNOTATION_DECISION_LEDGER.csv",
    REPO / "scripts/research_validators/validate_painan_1663_relational_artifact.py",
    REPO / "scripts/research_validators/validate_natal_1760_relational_artifact.py",
]

SYNCED_BASELINE_SHA256 = {
    str(REPO / "data/power_relations/painan_1663_relational_research_artifact.json"): "eeeeda8b368e255303c46dc245beb3c1179815d9f960cdff20b1ea59518b4bd7",
    str(REPO / "data/power_relations/natal_1760_relational_validation_artifact.json"): "afafe9f2985ef5e326514fcb8634d304f39a59c6f729abf1582d5221638ab07a",
    str(REPO / "data/power_relations/koto_tangah_destruction_cycle_relational_validation_artifact.json"): "2cb6e44cb8fd9eb7b4160cb2efd7d5f244d3547a1becc09919eaab7d4faae1aa",
    str(REPO / "docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md"): "f43b1f9fcee75e7a7271994905b676616470271f89dd99d62a6758f1c4b3cd37",
    str(REPO / "research_prototypes/painan_1663_relational/index.html"): "65e219d33e2410aa3113ad05664fc682276f996c4da089ecdac1d001f0663e78",
    str(REPO / "research_prototypes/painan_1663_relational/prototype.js"): "550c783d70419d7d83c22d314fadf74a1d456018a13c81363377b1a6f2196f1d",
    str(REPO / "research_prototypes/painan_1663_relational/prototype.css"): "2bcc702ef8b8d039b4151949882e5e355fee42f6168863d7097c96b4b006641f",
    str(REPO / "docs/thesis/pilot_annotation/CROSS_CASE_POWER_ONTOLOGY_REVIEW.md"): "c7d40cc93dbbb7246177d508dff04421039526a170ed8750cc98f97a73bdf8e9",
    str(REPO / "docs/thesis/pilot_annotation/CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md"): "707d2d0045c4b43a1c354eb5d79db59e6554ccbe39e2a2fa3396862e828b1bf5",
    str(REPO / "docs/thesis/colab/CROSS_CASE_ENTITY_DECISION_LEDGER.csv"): "b833b1b30c5eeed6a173ee7433a015d727e55d3c3234293b1201bd3700c2b310",
    str(REPO / "docs/thesis/colab/CROSS_CASE_RELATION_DECISION_LEDGER.csv"): "e14a55d85b3ebbc1279e9b4fe8be2769040fd543cef219f05d233b5b51b8b55a",
    str(REPO / "docs/thesis/colab/CROSS_CASE_ANNOTATION_DECISION_LEDGER.csv"): "b2fcf29724fa8be28efb366b6d7c634a2beca84d27b51ca9727c3924d89b8e8b",
    str(REPO / "scripts/research_validators/validate_painan_1663_relational_artifact.py"): "eca88fd8eb434f83b9506a7f9ebf732ee5f37de52acfffe4aa9ce878d945d625",
    str(REPO / "scripts/research_validators/validate_natal_1760_relational_artifact.py"): "a7ed12baf1069e33f9c3cbd3bc6c68e15150f1f1f6866fd84eb05147b658d805",
}
# The Koto Tangah validator itself was updated by the scoped fix; its own
# checksum is intentionally NOT pinned here (it is allowed to evolve via its
# own researcher-gated commits) -- presence is checked, not byte-equality,
# to avoid this validator becoming stale the moment that one is corrected
# again. This is disclosed, not silent: see check 33 detail.
KOTO_TANGAH_VALIDATOR_PATH = REPO / "scripts/research_validators/validate_koto_tangah_relational_artifact.py"

LOCAL_ONLY_LEDGER_PATH = REPO / "docs/thesis/colab/MODEL_3B_COLONIAL_CATEGORY_AND_RESISTANCE_INTERPRETIVE_WORKING.csv"
LOCAL_ONLY_LEDGER_SHA256 = "57ae2e16bd88eeaff3f055d3b0a188dbcea7ed51eb629fea2b7f03b1927469b8"
LOCAL_ONLY_LEDGER_EXPECTED_ROWS = 79
LOCAL_ONLY_LEDGER_VOCAB_CHECKS = {
    "source_asymmetry": {"VOC_ONLY", "VOC_DOMINANT", "MIXED", "LOCAL_VOICE_PRESENT", "CANNOT_DETERMINE"},
    "resistance_candidate": {"SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED", "NOT_TESTABLE"},
    "interpretive_status": {"SOURCE_DESCRIPTION_ONLY", "MECHANISM_HYPOTHESIS", "PROCESS_TRACING_SUPPORTED", "CONTESTED", "CANNOT_DETERMINE"},
    "evidence_strength": {"HIGH", "MODERATE", "LOW", "CANNOT_DETERMINE"},
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
FORBIDDEN_RELATION_TYPES = {
    "PATRON_OF", "CLIENT_OF", "PATRON_CLIENT_RELATION", "SECEDES_FROM", "REBELS_AGAINST",
    "SUBDUES", "KILLS", "RESISTS", "CONTINUES_AS_SAME_ACTOR", "GRANTS_TRADE_ACCESS_TO",
    "IMPOSES_PUNITIVE_CLASSIFICATION_ON", "MAINTAINS_PARALLEL_ALIGNMENT_WITH",
}

CLAIM_OR_EFFECTIVE_CONTROL_VALUES = {
    "CLAIM", "FORMAL_ACCEPTANCE", "TREATY_OBLIGATION", "MILITARY_PRESENCE",
    "FORT_CONTROL", "COMMERCIAL_CONTROL", "ADMINISTRATIVE_CONTROL",
    "EFFECTIVE_LOCAL_COMPLIANCE", "CONTESTED_CONTROL", "UNKNOWN_EFFECTIVE_CONTROL",
}
EVIDENCE_STRENGTH_VALUES = {"HIGH", "MODERATE", "LOW", "CANNOT_DETERMINE"}
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
FORBIDDEN_TERMS = ["payoff", "equilibrium", "nash", "utility function", "game tree",
                    "best move", "winner", "loser", "perfect rationality", "inevitab"]

results = []


def check(n, desc, ok, detail=""):
    results.append((n, desc, ok, detail))


def main():
    artifact_bytes = ARTIFACT_PATH.read_bytes()

    try:
        data = json.loads(artifact_bytes)
        check(1, "valid JSON", True)
    except Exception as e:
        check(1, "valid JSON", False, str(e))
        report()
        return

    check(2, "schema_version and ontology_contract_version present and correct",
          data.get("schema_version") == "0.1.0-ontology-v2-validation"
          and "V2_DRAFT" in str(data.get("ontology_contract_version", "")))

    notice = data.get("authorization_notice", "")
    required_markers = ["RESEARCH-ONLY", "NOT SERVED BY API", "NOT READ BY ATLAS",
                        "NOT CONNECTED TO DATABASE", "NOT CONNECTED TO GRAPHIFY"]
    check(3, "status=RESEARCH_ONLY_NONPRODUCTION and full production-isolation notice",
          all(m in notice for m in required_markers) and data.get("status") == "RESEARCH_ONLY_NONPRODUCTION")

    actors = data.get("actors", [])
    locations = data.get("locations", [])
    commodities = data.get("commodities", [])
    instruments = data.get("instruments", [])
    observations = data.get("observations", [])
    relations = data.get("relations", [])

    actor_ids = [a.get("actor_id") for a in actors]
    location_ids = [l.get("location_id") for l in locations]
    commodity_ids = [c.get("commodity_id") for c in commodities]
    instrument_ids = [i.get("instrument_id") for i in instruments]
    relation_ids = [r.get("relation_id") for r in relations]
    observation_ids = [o.get("observation_id") for o in observations]
    valid_object_ids = set(actor_ids) | set(location_ids) | set(commodity_ids) | {"UNIDENTIFIED"}

    check(4, "actor IDs unique", len(actor_ids) == len(set(actor_ids)))
    check(5, "location IDs unique", len(location_ids) == len(set(location_ids)))
    check(6, "commodity IDs unique", len(commodity_ids) == len(set(commodity_ids)))
    check(7, "instrument IDs unique", len(instrument_ids) == len(set(instrument_ids)))
    check(8, "relation IDs unique", len(relation_ids) == len(set(relation_ids)))
    check(9, "observation IDs unique", len(observation_ids) == len(set(observation_ids)))

    orphan = [r["relation_id"] for r in relations
              if r.get("subject_actor_id") not in set(actor_ids)
              or r.get("object_id") not in valid_object_ids]
    check(10, "no orphan endpoints", len(orphan) == 0, str(orphan))

    bad_types = [r["relation_id"] for r in relations if r.get("relation_type") not in ALLOWED_RELATION_TYPES]
    forbidden_hit = [r["relation_id"] for r in relations if r.get("relation_type") in FORBIDDEN_RELATION_TYPES]
    check(11, "relation_type restricted to Draft V2 set, no forbidden types",
          len(bad_types) == 0 and len(forbidden_hit) == 0, str(bad_types + forbidden_hit))

    annotation_errors = []
    for r in relations:
        if r.get("claim_or_effective_control") not in CLAIM_OR_EFFECTIVE_CONTROL_VALUES:
            annotation_errors.append((r["relation_id"], "claim_or_effective_control"))
        if r.get("evidence_strength") not in EVIDENCE_STRENGTH_VALUES:
            annotation_errors.append((r["relation_id"], "evidence_strength"))
        if r.get("interpretive_status") not in INTERPRETIVE_STATUS_VALUES:
            annotation_errors.append((r["relation_id"], "interpretive_status"))
        if r.get("explicit_or_inferred") not in EXPLICIT_OR_INFERRED_VALUES:
            annotation_errors.append((r["relation_id"], "explicit_or_inferred"))
        if r.get("commitment_credibility") not in COMMITMENT_CREDIBILITY_VALUES:
            annotation_errors.append((r["relation_id"], "commitment_credibility"))
        if r.get("patron_client_classification") not in PATRON_CLIENT_VALUES:
            annotation_errors.append((r["relation_id"], "patron_client_classification"))
    check(12, "controlled-vocabulary annotation values valid", len(annotation_errors) == 0, str(annotation_errors))

    event_id_errors = [r["relation_id"] for r in relations
                       if not isinstance(r.get("event_ids"), list) or not all(str(e).startswith("EVT-") for e in r["event_ids"])]
    check(13, "event_ids present, list-typed, EVT- prefixed on every relation", len(event_id_errors) == 0, str(event_id_errors))

    missing_locator = [r["relation_id"] for r in relations if not r.get("source_passage_locator")]
    missing_locator += [a["actor_id"] for a in actors if not a.get("source_passage_locator")]
    check(14, "source_passage_locator present for all actors/relations", len(missing_locator) == 0, str(missing_locator))

    check(15, "actor and location kept as separate entity sets",
          len(set(actor_ids) & set(location_ids)) == 0)

    office_office_holder_ok = "ACTOR_ACEH_COURT" in actor_ids and "ACTOR_PANGLIMA_SOURERADJA" in actor_ids
    check(16, "office (Aceh court / panglima office) kept separate from office-holder records", office_office_holder_ok)

    check(17, "commodity IDs kept separate from location IDs", len(set(commodity_ids) & set(location_ids)) == 0)

    soureradja_actor = next((a for a in actors if a["actor_id"] == "ACTOR_PONGELOUS_12_DESA_TICCO_1662"), None)
    ok18 = (soureradja_actor is not None
            and "not confirmed to bind" in soureradja_actor.get("mandate_status", "").lower()
            and soureradja_actor.get("researcher_review_required") is True)
    check(18, "Soureradja/pongelous mandate explicitly bounded, not asserted to bind all Tiku", ok18)

    pro_aceh = next((a for a in actors if a["actor_id"] == "ACTOR_PRO_ACEH_FACTION_1684"), None)
    tiku_regents_1684 = next((a for a in actors if a["actor_id"] == "ACTOR_TIKU_REGENTS_1684"), None)
    check(19, "pro-Aceh faction (1684) kept as a separate actor from the wider Tiku regents/inhabitants collective",
          pro_aceh is not None and tiku_regents_1684 is not None and pro_aceh["actor_id"] != tiku_regents_1684["actor_id"])

    rel_1740 = next((r for r in relations if r["relation_id"] == "REL_1740_CONTESTS_SUCCESSION"), None)
    check(20, "1740 Raja Ibrahim/Kinali conflict represented as a local relation, not attributed to Aceh or VOC",
          rel_1740 is not None and rel_1740["subject_actor_id"] == "ACTOR_RAJA_KINALI" and rel_1740["object_id"] == "ACTOR_RAJA_IBRAHIM")

    check(21, "no MAINTAINS_PARALLEL_ALIGNMENT_WITH relation used",
          not any(r.get("relation_type") == "MAINTAINS_PARALLEL_ALIGNMENT_WITH" for r in relations))

    pc_as_type = [r["relation_id"] for r in relations if "PATRON" in (r.get("relation_type") or "") or "CLIENT" in (r.get("relation_type") or "")]
    check(22, "no patron-client edge (patron_client_classification field only)", len(pc_as_type) == 0, str(pc_as_type))

    resistance_as_type = [r["relation_id"] for r in relations if "RESIST" in (r.get("relation_type") or "").upper()]
    check(23, "no resistance edge (relation_type never encodes resistance)", len(resistance_as_type) == 0, str(resistance_as_type))

    rel_1641 = next((r for r in relations if r["relation_id"] == "REL_1641_CLAIMS_JURISDICTION"), None)
    check(24, "1641 claim not treated as effective-control proof",
          rel_1641 is not None and rel_1641["claim_or_effective_control"] == "CLAIM")

    rel_1649 = next((r for r in relations if r["relation_id"] == "REL_1649_CLAIMS_COMMODITY_MONOPOLY"), None)
    check(25, "1649 treaty not treated as sovereignty (COMMERCIAL_CONTROL only)",
          rel_1649 is not None and rel_1649["claim_or_effective_control"] not in {"ADMINISTRATIVE_CONTROL", "FORT_CONTROL"})

    rel_1662a = next((r for r in relations if r["relation_id"] == "REL_1662_SWITCHES_SOURERADJA"), None)
    rel_1662b = next((r for r in relations if r["relation_id"] == "REL_1662_SWITCHES_PONGELOUS"), None)
    check(26, "1662 secession represented as two actor-specific relations, not one whole-Tiku-community relation",
          rel_1662a is not None and rel_1662b is not None and rel_1662a["subject_actor_id"] != rel_1662b["subject_actor_id"])

    rel_1684_mil = next((r for r in relations if r["relation_id"] == "REL_1684_MILITARY_FORCE"), None)
    check(27, "1684 subduing not treated as durable-control proof (MILITARY_PRESENCE only)",
          rel_1684_mil is not None and rel_1684_mil["claim_or_effective_control"] == "MILITARY_PRESENCE")

    sas_obs = next((o for o in observations if o["observation_id"] == "OBS_1693_1695_SAS_KILLING"), None)
    check(28, "Sas episode (1693-95) remains uncertainty-marked (perpetrator UNIDENTIFIED, no relation forced)",
          sas_obs is not None and sas_obs["perpetrator_status"].startswith("UNIDENTIFIED")
          and not any(r.get("object_id") == "ACTOR_VAANDRIG_SAS" for r in relations))

    long_span_bad = []
    for r in relations:
        vf, vt = r.get("valid_from"), r.get("valid_to")
        if vf and vt and str(vf)[:4].isdigit() and str(vt)[:4].isdigit():
            if int(str(vt)[:4]) - int(str(vf)[:4]) > 25:
                long_span_bad.append(r["relation_id"])
    check(29, "no actor continuity invented across the full 1625-1740 span (no relation spans the whole period)",
          len(long_span_bad) == 0, str(long_span_bad))

    check(30, "temporal gaps remain gaps (no single relation bridges 1625-1740 continuously)",
          len(relations) > 1 and not any(
              r.get("valid_from") and str(r["valid_from"])[:4] in {"1625"} and r.get("valid_to") and str(r["valid_to"])[:4] in {"1740"}
              for r in relations))

    text_blob = json.dumps(data)
    lower_blob = text_blob.lower()
    check(31, "no arbitrary payoff language present", "payoff" not in lower_blob)
    check(32, "no equilibrium/game-theoretic-solution claim present",
          not any(t in lower_blob for t in ["equilibrium", "nash", "utility function", "game tree", "best move", "perfect rationality"]))

    # 33. SYNCED_FROZEN_DEPENDENCIES present and checksum-matched (Koto Tangah
    # validator checked for presence only, per the note above).
    missing_synced, mismatched_synced = [], []
    for p in SYNCED_FROZEN_DEPENDENCIES:
        if not p.exists():
            missing_synced.append(p.name)
            continue
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != SYNCED_BASELINE_SHA256[str(p)]:
            mismatched_synced.append(p.name)
    kt_validator_present = KOTO_TANGAH_VALIDATOR_PATH.exists()
    ok_33 = not missing_synced and not mismatched_synced and kt_validator_present
    check(33, "prior artifacts (Painan/Natal/Koto Tangah) and other synced frozen dependencies unchanged",
          ok_33, f"missing={missing_synced} mismatched={mismatched_synced} kt_validator_present={kt_validator_present}")

    # 34. local-only dependency policy matches the corrected Koto Tangah
    # validator's environment contract (34A/34B split).
    if not LOCAL_ONLY_LEDGER_PATH.exists():
        status_34b, ok_34b = "NOT_APPLICABLE_ON_SERVER", True
        detail_34b = ("interpretive ledger is an explicitly documented local-only, gitignored, "
                      "nonproduction artifact; content was validated in the research environment "
                      "before the milestone commit; this check does not read ledger content on a "
                      "checkout where the file is absent")
    else:
        raw = LOCAL_ONLY_LEDGER_PATH.read_bytes()
        hash_ok = hashlib.sha256(raw).hexdigest() == LOCAL_ONLY_LEDGER_SHA256
        text_lines = [l for l in raw.decode("utf-8").splitlines(keepends=True) if not l.startswith("#")]
        ledger_rows = list(csv.reader(io.StringIO("".join(text_lines))))
        ledger_header, ledger_data = ledger_rows[0], ledger_rows[1:]
        row_count_ok = len(ledger_data) == LOCAL_ONLY_LEDGER_EXPECTED_ROWS
        col_idx = {name: i for i, name in enumerate(ledger_header)}
        vocab_violations = []
        for row_i, row in enumerate(ledger_data, 2):
            for field, allowed in LOCAL_ONLY_LEDGER_VOCAB_CHECKS.items():
                if field in col_idx and row[col_idx[field]] not in allowed:
                    vocab_violations.append((row_i, field))
        ok_34b = hash_ok and row_count_ok and len(vocab_violations) == 0
        status_34b = "PASS_LOCAL" if ok_34b else "FAIL_LOCAL"
        detail_34b = (f"rows={len(ledger_data)} (expected {LOCAL_ONLY_LEDGER_EXPECTED_ROWS}), "
                      f"vocabulary_violations={len(vocab_violations)}, checksum_match={hash_ok}")
    detail_34 = f"Check 34B (local-only ledger, mirrors Koto Tangah's environment contract): {status_34b} -- {detail_34b}"
    check(34, "local-only dependency policy matches the corrected Koto Tangah validator environment contract",
          ok_34b, detail_34)

    check(35, "no production integration (status/notice confirm nonproduction)",
          data.get("status") == "RESEARCH_ONLY_NONPRODUCTION")

    report()


def report():
    passed = sum(1 for *_r, ok, _d in [(n, d, o, dt) for n, d, o, dt in results] if ok)
    total = len(results)
    for n, desc, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        line = f"[{status}] check {n}: {desc}"
        if detail and (not ok or n == 34 or n == 33):
            line += f" -- {detail}"
        print(line)
    print(f"\n{passed}/{total} checks passed")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
