#!/usr/bin/env python3
"""Validator for data/power_relations/sillida_resource_governance_relational_validation_artifact.json.

RESEARCH-ONLY NONPRODUCTION. Not served by API, not read by Atlas, not
connected to database or Graphify. Validates the Sillida V4 artifact against
the frozen ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md (unmodified by
this script), per the V4 ontology stress-test instructions.

Dependency policy mirrors the corrected Koto Tangah V2 / Tiku V3 validator's
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
ARTIFACT_PATH = REPO / "data/power_relations/sillida_resource_governance_relational_validation_artifact.json"

SYNCED_FROZEN_DEPENDENCIES = [
    REPO / "data/power_relations/painan_1663_relational_research_artifact.json",
    REPO / "data/power_relations/natal_1760_relational_validation_artifact.json",
    REPO / "data/power_relations/koto_tangah_destruction_cycle_relational_validation_artifact.json",
    REPO / "data/power_relations/tiku_1625_1740_relational_validation_artifact.json",
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
    str(REPO / "data/power_relations/tiku_1625_1740_relational_validation_artifact.json"): "b9abf275f0dbcb4e82370f88bbf37ac845f3eaf35aaab16330376c688891923c",
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
# Koto Tangah and Tiku validators are checked for presence only (not
# checksum-pinned), same rationale as Tiku's own validator: they are allowed
# to evolve via their own researcher-gated commits without making this
# validator stale.
KOTO_TANGAH_VALIDATOR_PATH = REPO / "scripts/research_validators/validate_koto_tangah_relational_artifact.py"
TIKU_VALIDATOR_PATH = REPO / "scripts/research_validators/validate_tiku_relational_artifact.py"

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
    "ENSLAVES", "COMMANDS_SLAVE_COMPANY", "ALLY_OF", "VOLUNTARILY_SUPPORTS",
    "REBELS_AGAINST", "RESISTS", "OWNS_TERRITORY", "TRANSFERS_SOVEREIGNTY",
    "PATRON_OF", "CLIENT_OF", "PATRON_CLIENT_RELATION", "GRANTS_TRADE_ACCESS_TO",
    "MAINTAINS_PARALLEL_ALIGNMENT_WITH", "IMPOSES_PUNITIVE_CLASSIFICATION_ON",
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
    valid_object_ids = set(actor_ids) | set(location_ids) | set(commodity_ids)

    check(4, "actor IDs unique", len(actor_ids) == len(set(actor_ids)))
    check(5, "location IDs unique", len(location_ids) == len(set(location_ids)))
    check(6, "commodity IDs unique", len(commodity_ids) == len(set(commodity_ids)))
    check(7, "instrument IDs unique", len(instrument_ids) == len(set(instrument_ids)))
    check(8, "relation IDs unique", len(relation_ids) == len(set(relation_ids)))
    check(9, "observation IDs unique", len(observation_ids) == len(set(observation_ids)))

    orphan = [r["relation_id"] for r in relations
              if r.get("subject_actor_id") not in set(actor_ids)
              or r.get("object_id") not in valid_object_ids]
    check(10, "no orphan endpoints (actor/location/resource separation preserved)", len(orphan) == 0, str(orphan))

    bad_types = [r["relation_id"] for r in relations if r.get("relation_type") not in ALLOWED_RELATION_TYPES]
    forbidden_hit = [r["relation_id"] for r in relations if r.get("relation_type") in FORBIDDEN_RELATION_TYPES]
    check(11, "relation_type restricted to Draft V2 set, no forbidden types (ENSLAVES/COMMANDS_SLAVE_COMPANY/etc never used)",
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

    # 13. native Sillida ruler not invented (only appears where the source itself supports it)
    fabricated_ruler = any("NATIVE_RULER" in a["actor_id"].upper() and "REGENT" not in a["actor_id"].upper() for a in actors)
    check(13, "no fabricated Sillida-native-ruler actor invented to fill the 1667/1681 cession-mandate gap", not fabricated_ruler)

    # 14. three neighboring rulers not merged
    three_rulers = {"ACTOR_SULTHAN_ACHMET_CHIA_BAJANG", "ACTOR_SULTHAN_MAMET_CHIA_INDRAPURA", "ACTOR_SULTHAN_BESAAR_TROSANG"}
    check(14, "the three neighboring ceding rulers (Bajang, Indrapura, Trosang) kept as three separate actors",
          three_rulers.issubset(set(actor_ids)))

    # 15. mandate uncertainty retained
    sillida_regents = next((a for a in actors if a["actor_id"] == "ACTOR_SILLIDA_REGENTS"), None)
    check(15, "Sillida regents' own mandate/absence-of-voice for the 1667/1681 cessions explicitly documented",
          sillida_regents is not None and sillida_regents.get("researcher_review_required") is True
          and "ABSENT" in sillida_regents.get("notes", "").upper())

    # 16. territorial cession not sovereignty (FORMAL_ACCEPTANCE, not ADMINISTRATIVE_CONTROL)
    cession_rels = [r for r in relations if r["relation_id"].startswith("REL_1667_RECOGNIZES") or r["relation_id"].startswith("REL_1681_RECOGNIZES")]
    bad_cession = [r["relation_id"] for r in cession_rels if r["claim_or_effective_control"] == "ADMINISTRATIVE_CONTROL"]
    check(16, "territorial cession relations carry FORMAL_ACCEPTANCE, not a durable ADMINISTRATIVE_CONTROL sovereignty value",
          len(bad_cession) == 0 and len(cession_rels) > 0, str(bad_cession))

    # 17. resource conflict separate from commercial strategy (two CONTESTS_RESOURCE_WITH relations exist, distinct object pairs)
    cr_rels = [r for r in relations if r.get("relation_type") == "CONTESTS_RESOURCE_WITH"]
    check(17, "resource conflict (CONTESTS_RESOURCE_WITH) modeled as its own relation, distinct from commercial-strategy relations",
          len(cr_rels) >= 2)

    # 18. mine lease separate from territorial control
    lease_rel = next((r for r in relations if r["relation_id"] == "REL_1737_LEASES_MINE"), None)
    jurisdiction_rel = next((r for r in relations if r["relation_id"] == "REL_1737_CLAIMS_JURISDICTION_MINE"), None)
    check(18, "1737 mine lease (LEASES_RESOURCE_TO) and mine jurisdiction claim (CLAIMS_JURISDICTION_OVER) modeled as two separate relations",
          lease_rel is not None and jurisdiction_rel is not None
          and lease_rel["claim_or_effective_control"] != jurisdiction_rel["claim_or_effective_control"])

    # 19. toll release represented without reversing relation direction
    toll_rel = next((r for r in relations if r["relation_id"] == "REL_1698_COLLECTS_TOLL_SALIMOET"), None)
    check(19, "1698 salimoet toll relation direction matches the source (regents as beneficiary, subject=regents, object=VOC), not reversed",
          toll_rel is not None and toll_rel["subject_actor_id"] == "ACTOR_SILLIDA_REGENTS" and toll_rel["object_id"] == "ACTOR_VOC")

    # 20. coerced company not modeled as voluntary ally
    enslaved_actor_in_relations = any(r.get("subject_actor_id") == "ACTOR_ARMED_ENSLAVED_COMPANY_SILLIDA_MINE"
                                       or r.get("object_id") == "ACTOR_ARMED_ENSLAVED_COMPANY_SILLIDA_MINE" for r in relations)
    check(20, "armed enslaved company never appears as subject/object of any relation (no voluntary-ally mischaracterization possible)",
          not enslaved_actor_in_relations)

    # 21. constrained agency visible (observation exists, explicitly flagged)
    obs_ca = next((o for o in observations if o["observation_id"] == "OBS_CONSTRAINED_AGENCY_ARMED_ENSLAVED_COMPANY"), None)
    check(21, "constrained agency represented as a standalone observation with explicit uncertainty_note",
          obs_ca is not None and len(obs_ca.get("uncertainty_note", "")) > 0)

    # 22. political intent CANNOT_DETERMINE for the enslaved company
    check(22, "armed enslaved company's political intent recorded as CANNOT_DETERMINE",
          obs_ca is not None and obs_ca.get("interpretive_status") == "CANNOT_DETERMINE")

    # 23. colonial punitive classification annotation-only ("rebellie" framing never a relation_type)
    check(23, "VOC's 'rebellie'/punitive classification language never used as a relation_type",
          not any("REBEL" in (r.get("relation_type") or "").upper() for r in relations))

    # 24. no resistance edge
    check(24, "no resistance edge (relation_type never encodes resistance)",
          not any("RESIST" in (r.get("relation_type") or "").upper() for r in relations))

    # 25. no patron-client edge
    pc_as_type = [r["relation_id"] for r in relations if "PATRON" in (r.get("relation_type") or "") or "CLIENT" in (r.get("relation_type") or "")]
    check(25, "no patron-client edge (patron_client_classification field only)", len(pc_as_type) == 0, str(pc_as_type))

    # 26. claim and effective control distinct (1737 pair uses two different values)
    check(26, "claim (CLAIM) and effective/commercial control (COMMERCIAL_CONTROL) kept distinct in the 1737 lease pair",
          lease_rel is not None and jurisdiction_rel is not None
          and jurisdiction_rel["claim_or_effective_control"] == "CLAIM"
          and lease_rel["claim_or_effective_control"] == "COMMERCIAL_CONTROL")

    # 27. no actor continuity invented (Bajang office-holder succession kept separate)
    check(27, "Bajang's 1667/1681 ruler and 1679 ruler (different named individuals) kept as separate actors, no invented succession chain",
          "ACTOR_SULTHAN_ACHMET_CHIA_BAJANG" in actor_ids and "ACTOR_SULTHAN_NIAMOELIA_BAJANG" in actor_ids
          and "ACTOR_SULTHAN_ACHMET_CHIA_BAJANG" != "ACTOR_SULTHAN_NIAMOELIA_BAJANG")

    # 28/29. no arbitrary payoff / equilibrium
    text_blob = json.dumps(data)
    lower_blob = text_blob.lower()
    check(28, "no arbitrary payoff language present", "payoff" not in lower_blob)
    check(29, "no equilibrium/game-theoretic-solution claim present",
          not any(t in lower_blob for t in ["equilibrium", "nash", "utility function", "game tree", "best move", "perfect rationality"]))

    # 30. all frozen dependencies unchanged (SYNCED)
    missing_synced, mismatched_synced = [], []
    for p in SYNCED_FROZEN_DEPENDENCIES:
        if not p.exists():
            missing_synced.append(p.name)
            continue
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != SYNCED_BASELINE_SHA256[str(p)]:
            mismatched_synced.append(p.name)
    kt_present = KOTO_TANGAH_VALIDATOR_PATH.exists()
    tiku_present = TIKU_VALIDATOR_PATH.exists()
    ok_30 = not missing_synced and not mismatched_synced and kt_present and tiku_present
    check(30, "all prior artifacts (Painan/Natal/Koto Tangah/Tiku) and other synced frozen dependencies unchanged",
          ok_30, f"missing={missing_synced} mismatched={mismatched_synced} kt_validator_present={kt_present} tiku_validator_present={tiku_present}")

    # 31. local-only ledger policy handled correctly (34A/34B-equivalent split)
    if not LOCAL_ONLY_LEDGER_PATH.exists():
        status_ledger, ok_ledger = "NOT_APPLICABLE_ON_SERVER", True
        detail_ledger = ("interpretive ledger is an explicitly documented local-only, gitignored, "
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
        ok_ledger = hash_ok and row_count_ok and len(vocab_violations) == 0
        status_ledger = "PASS_LOCAL" if ok_ledger else "FAIL_LOCAL"
        detail_ledger = (f"rows={len(ledger_data)} (expected {LOCAL_ONLY_LEDGER_EXPECTED_ROWS}), "
                         f"vocabulary_violations={len(vocab_violations)}, checksum_match={hash_ok}")
    check(31, "local-only interpretive-ledger dependency policy matches the corrected V2/V3 environment contract",
          ok_ledger, f"{status_ledger} -- {detail_ledger}")

    # 32. no production integration
    check(32, "no production integration (status/notice confirm nonproduction)",
          data.get("status") == "RESEARCH_ONLY_NONPRODUCTION")

    report()


def report():
    passed = sum(1 for *_r, ok, _d in [(n, d, o, dt) for n, d, o, dt in results] if ok)
    total = len(results)
    for n, desc, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        line = f"[{status}] check {n}: {desc}"
        if detail and (not ok or n in (30, 31)):
            line += f" -- {detail}"
        print(line)
    print(f"\n{passed}/{total} checks passed")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
