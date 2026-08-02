"""Regression guards for candidate-universe construction: a named person
must not disappear from every output merely because they lack an HRLT
presence row. Verified against the real dataset's actual personnel
register (DOC-PERSONNEL-1682-01-09, dated 1682-01-09) and its actual
41-role-holders-without-HRLT-presence gap (the same population
test_cli_pipeline.py's F2 tests already surface via entity_coverage, now
additionally classified with an explicit, non-pejorative reason).
"""
import csv

from salido_hdt.solver import config
from salido_hdt.solver.candidate_universe import (
    EntityState,
    classify_entities,
    derive_register_presence,
    write_candidate_entities_csv,
    write_entity_presence_csv,
    write_excluded_entities_csv,
)
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.variables import build_variables


def _dataset():
    return load_dataset(config.V0_4_1_ROOT)


# --- derive_register_presence -----------------------------------------------


def test_register_presence_matches_the_real_personnel_register():
    dataset = _dataset()
    register_presence = derive_register_presence(dataset)

    assert "P-HESSE" in register_presence
    rec = register_presence["P-HESSE"][0]
    assert rec.source_document_id == "DOC-PERSONNEL-1682-01-09"
    assert rec.date == "1682-01-09"
    assert rec.presence_scope == "enclave"
    assert rec.location_precision == "enclave_level"
    assert rec.task == "unknown"
    assert rec.evidence_status == "explicit"
    assert rec.derivation_status == "register_presence"


def test_register_presence_count_matches_real_person_role_citations():
    """Every one of the real dataset's 47 04_person_roles.csv rows cites
    DOC-PERSONNEL-1682-01-09 -- so exactly 47 distinct persons must get a
    register presence record."""
    dataset = _dataset()
    register_presence = derive_register_presence(dataset)
    assert len(register_presence) == 47


def test_register_presence_independent_of_role_evidence_status():
    """P-STREIJT's own role claim is evidence_status='interpreted'
    (confidence 0.65, 'Oppersteijger?') -- but their PRESENCE in the
    register is still an explicit claim; role uncertainty must not leak
    into the presence record's own evidence_status."""
    dataset = _dataset()
    assert dataset.person_roles["PR-STREIJT"].evidence_status == "interpreted"
    register_presence = derive_register_presence(dataset)
    assert register_presence["P-STREIJT"][0].evidence_status == "explicit"


def test_register_presence_never_derives_beyond_document_date():
    """No wider interval, no location beyond 'enclave', no task beyond
    'unknown' is ever synthesized."""
    dataset = _dataset()
    for records in derive_register_presence(dataset).values():
        for rec in records:
            assert rec.date == "1682-01-09"
            assert rec.presence_scope == "enclave"
            assert rec.location_precision == "enclave_level"
            assert rec.task == "unknown"


# --- classify_entities -------------------------------------------------------


def test_named_person_without_any_evidence_is_excluded_with_reason():
    """P-CROON has zero 04 rows and zero HRLT rows in the real dataset --
    genuinely no presence evidence of any kind."""
    dataset = _dataset()
    sv = build_variables(dataset)
    classifications = {c.entity_id: c for c in classify_entities(dataset, sv)}

    c = classifications["P-CROON"]
    assert c.has_hrlt_presence is False
    assert c.has_register_presence is False
    assert c.state == EntityState.EXCLUDED_WITH_REASON
    assert c.reason  # non-empty, explicit reason required


def test_named_person_with_register_only_is_documented_present_not_silently_dropped():
    """P-BRETSNIJDER (role R-BERGWERKER via the register, but no HRLT
    presence row -- the exact F2 finding) must be classified
    DOCUMENTED_PRESENT with a reason that does NOT claim absence of
    evidence."""
    dataset = _dataset()
    sv = build_variables(dataset)
    classifications = {c.entity_id: c for c in classify_entities(dataset, sv)}

    c = classifications["P-BRETSNIJDER"]
    assert c.has_hrlt_presence is False
    assert c.has_register_presence is True
    assert c.state == EntityState.DOCUMENTED_PRESENT
    # Must not use the SAME reason text as a genuinely evidence-less
    # exclusion -- the register-only reason is a distinct claim.
    no_evidence_reason = classifications["P-CROON"].reason
    assert c.reason != no_evidence_reason
    assert not c.reason.startswith("no presence evidence")
    assert "register" in c.reason.lower()


def test_named_person_with_hrlt_presence_is_eligible_for_assignment_by_default():
    dataset = _dataset()
    sv = build_variables(dataset)
    classifications = {c.entity_id: c for c in classify_entities(dataset, sv)}

    c = classifications["P-HESSE"]
    assert c.has_hrlt_presence is True
    assert c.state == EntityState.ELIGIBLE_FOR_ASSIGNMENT


def test_assigned_entity_ids_splits_eligible_into_assigned_and_unassigned():
    dataset = _dataset()
    sv = build_variables(dataset)
    classifications = {
        c.entity_id: c
        for c in classify_entities(dataset, sv, assigned_entity_ids=frozenset({"P-HESSE"}))
    }

    assert classifications["P-HESSE"].state == EntityState.ASSIGNED
    # The other 4 HRLT-presence-eligible individuals must be present but
    # unassigned -- an empty-but-solved scenario is not the same as "no
    # scenario was solved at all" (that distinction is the None sentinel).
    other_eligible = [
        eid for eid in ("P-HOFFMAN", "P-PLEIJTNER", "P-ROELINGH", "P-VOGEL")
        if classifications[eid].has_hrlt_presence
    ]
    assert other_eligible  # sanity: these really are HRLT-eligible in real data
    for eid in other_eligible:
        assert classifications[eid].state == EntityState.PRESENT_BUT_UNASSIGNED


def test_no_scenario_solved_sentinel_differs_from_empty_scenario():
    dataset = _dataset()
    sv = build_variables(dataset)

    none_sentinel = {c.entity_id: c.state for c in classify_entities(dataset, sv, assigned_entity_ids=None)}
    empty_solved = {c.entity_id: c.state for c in classify_entities(dataset, sv, assigned_entity_ids=frozenset())}

    assert none_sentinel["P-HESSE"] == EntityState.ELIGIBLE_FOR_ASSIGNMENT
    assert empty_solved["P-HESSE"] == EntityState.PRESENT_BUT_UNASSIGNED


def test_every_named_person_receives_exactly_one_classification():
    dataset = _dataset()
    sv = build_variables(dataset)
    classifications = classify_entities(dataset, sv)
    assert len(classifications) == len(dataset.persons)
    assert {c.entity_id for c in classifications} == set(dataset.persons)


# --- CSV writers --------------------------------------------------------------


def test_write_entity_presence_csv_covers_both_evidence_tiers(tmp_path):
    dataset = _dataset()
    sv = build_variables(dataset)
    path = tmp_path / "entity_presence.csv"
    write_entity_presence_csv(dataset, sv, path)

    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows  # non-empty
    source_types = {r["source_type"] for r in rows}
    assert source_types == {"hrlt", "register"}

    hesse_rows = [r for r in rows if r["entity_id"] == "P-HESSE"]
    assert any(r["source_type"] == "hrlt" for r in hesse_rows)
    assert any(r["source_type"] == "register" for r in hesse_rows)

    bretsnijder_rows = [r for r in rows if r["entity_id"] == "P-BRETSNIJDER"]
    assert bretsnijder_rows
    assert all(r["source_type"] == "register" for r in bretsnijder_rows)


def test_write_candidate_and_excluded_csvs_partition_all_named_persons(tmp_path):
    """Every named person appears in EXACTLY ONE of candidate_entities.csv
    / excluded_entities.csv -- nobody vanishes, nobody is double-counted."""
    dataset = _dataset()
    sv = build_variables(dataset)
    candidate_path = tmp_path / "candidate_entities.csv"
    excluded_path = tmp_path / "excluded_entities.csv"
    write_candidate_entities_csv(dataset, sv, candidate_path)
    write_excluded_entities_csv(dataset, sv, excluded_path)

    with candidate_path.open(encoding="utf-8") as f:
        candidate_ids = {r["entity_id"] for r in csv.DictReader(f)}
    with excluded_path.open(encoding="utf-8") as f:
        excluded_ids = {r["entity_id"] for r in csv.DictReader(f)}

    assert candidate_ids & excluded_ids == set()
    assert candidate_ids | excluded_ids == set(dataset.persons)
    assert "P-HESSE" in candidate_ids
    assert "P-BRETSNIJDER" in excluded_ids
    assert "P-CROON" in excluded_ids


def test_excluded_entities_csv_distinguishes_register_only_from_no_evidence(tmp_path):
    dataset = _dataset()
    sv = build_variables(dataset)
    path = tmp_path / "excluded_entities.csv"
    write_excluded_entities_csv(dataset, sv, path)

    with path.open(encoding="utf-8") as f:
        rows = {r["entity_id"]: r for r in csv.DictReader(f)}

    assert rows["P-BRETSNIJDER"]["state"] == "documented_present"
    assert rows["P-CROON"]["state"] == "excluded_with_reason"
    assert rows["P-BRETSNIJDER"]["reason"] != rows["P-CROON"]["reason"]
