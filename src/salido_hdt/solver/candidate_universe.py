"""Named-person candidate-universe construction and reporting.

A named person must never disappear from this solver's output merely
because they lack an HRLT presence row (07_human_role_location_time.csv).
Prior to this module, `cli._entity_coverage()` already flagged such persons
(`has_hard_presence=False`), but a person with genuinely NO other evidence
looked identical, in that report, to a person attested present by a
completely different kind of document. This module tells the two apart.

Two independent presence-evidence tiers exist for named individuals:

  1. HRLT presence (07) -- location + weekly time-bucket window, HARD-
     classified via validation.py. This is what variables.py actually uses
     to build CP-SAT x-variables; UNCHANGED by this module.
  2. Register presence -- a named person cited by a 04_person_roles.csv row
     whose source_document_id points at a 01_documents.csv row with
     document_type == 'personnel_register' (in the real dataset: exactly
     DOC-PERSONNEL-1682-01-09, "Lijste van Compagnies dienaren en
     lijfeijgenen" / "List of Company servants and bondsmen", dated
     1682-01-09). Being NAMED in a dated personnel register is presence
     evidence at the enclave level, independent of whatever role claim
     accompanies it -- even a role documented as 'interpreted'/uncertain
     (e.g. P-STREIJT's 'Oppersteijger?', confidence 0.65) still sits on an
     EXPLICIT presence claim: presence and role are different claims about
     the same row, and role uncertainty does not diminish the certainty of
     "this person was named in this register on this date."

Register presence is deliberately coarse and is never widened into
anything more specific than these fixed fields:

    presence_scope     = enclave
    location_precision = enclave_level
    task                = unknown
    evidence_status     = explicit
    derivation_status   = register_presence

No mine section, task, schicht, or date/interval beyond the register
document's own date_iso is ever derived or inferred here.

Scope decision (explicit, not silent): this module is READ-ONLY reporting.
It does not add x-variables to the solver -- register presence does not
currently grant CP-SAT eligibility. Wiring enclave-level presence into
variables.py's variable construction is a separate, larger change (new
location granularity, new HARD-eligibility rule for the SP-01236-style
"section-level sufficient for presence" precedent) deferred to a future
task once the register-as-evidence-source itself has been reviewed.
"""
from __future__ import annotations

import csv
import enum
from dataclasses import dataclass, field
from pathlib import Path


class EntityState(enum.Enum):
    DOCUMENTED_PRESENT = "documented_present"
    ELIGIBLE_FOR_ASSIGNMENT = "eligible_for_assignment"
    ASSIGNED = "assigned"
    PRESENT_BUT_UNASSIGNED = "present_but_unassigned"
    EXCLUDED_WITH_REASON = "excluded_with_reason"


@dataclass(frozen=True)
class RegisterPresenceRecord:
    person_id: str
    source_document_id: str
    date: str
    presence_scope: str = "enclave"
    location_precision: str = "enclave_level"
    task: str = "unknown"
    evidence_status: str = "explicit"
    derivation_status: str = "register_presence"


@dataclass(frozen=True)
class EntityClassification:
    entity_id: str
    name_canonical: str
    has_hrlt_presence: bool
    has_register_presence: bool
    state: EntityState
    reason: str = ""


_NO_EVIDENCE_REASON = (
    "no presence evidence of any kind: no HRLT (07) presence row, and not "
    "named in any 04_person_roles.csv row citing a personnel_register document"
)
_REGISTER_ONLY_REASON = (
    "register-attested enclave presence only (see entity_presence.csv) -- "
    "no HRLT presence row, so NOT yet a solver-eligible HARD presence this "
    "turn (see candidate_universe.py module docstring for the scope decision); "
    "this is NOT the same as having no evidence"
)


def derive_register_presence(dataset) -> dict[str, list[RegisterPresenceRecord]]:
    """person_id -> register presence record(s), one per distinct
    personnel-register document that names them. Uses only the document's
    own date_iso -- never a derived interval."""
    register_doc_ids = {
        doc.document_id for doc in dataset.documents.values()
        if doc.document_type == "personnel_register"
    }
    out: dict[str, list[RegisterPresenceRecord]] = {}
    seen: set[tuple[str, str]] = set()
    for pr in dataset.person_roles.values():
        if pr.source_document_id not in register_doc_ids:
            continue
        key = (pr.person_id, pr.source_document_id)
        if key in seen:
            continue
        seen.add(key)
        doc = dataset.documents[pr.source_document_id]
        out.setdefault(pr.person_id, []).append(
            RegisterPresenceRecord(
                person_id=pr.person_id,
                source_document_id=doc.document_id,
                date=doc.date_iso,
            )
        )
    return out


def classify_entities(
    dataset, sv, assigned_entity_ids: frozenset[str] | None = None
) -> list[EntityClassification]:
    """Exactly one classification per named person in 02_persons.csv --
    nobody is ever omitted. `assigned_entity_ids`: pass the set of entity
    ids with at least one active assignment in a specific scenario to split
    ELIGIBLE_FOR_ASSIGNMENT into ASSIGNED/PRESENT_BUT_UNASSIGNED; pass None
    (the default) when no scenario has been solved yet, distinct from
    passing an empty frozenset (a scenario WAS solved and assigned nobody,
    per add_task_continuity_penalty's/add_role_task_support_penalty's
    current formulation -- see SOLVER_SCENARIO_INTERPRETATION_AUDIT.md)."""
    register_presence = derive_register_presence(dataset)
    results: list[EntityClassification] = []
    for person_id, person in sorted(dataset.persons.items()):
        has_hrlt = person_id in sv.presence
        has_register = person_id in register_presence
        if has_hrlt:
            if assigned_entity_ids is None:
                state = EntityState.ELIGIBLE_FOR_ASSIGNMENT
            elif person_id in assigned_entity_ids:
                state = EntityState.ASSIGNED
            else:
                state = EntityState.PRESENT_BUT_UNASSIGNED
            reason = ""
        elif has_register:
            state = EntityState.DOCUMENTED_PRESENT
            reason = _REGISTER_ONLY_REASON
        else:
            state = EntityState.EXCLUDED_WITH_REASON
            reason = _NO_EVIDENCE_REASON
        results.append(EntityClassification(
            entity_id=person_id,
            name_canonical=person.name_canonical,
            has_hrlt_presence=has_hrlt,
            has_register_presence=has_register,
            state=state,
            reason=reason,
        ))
    return results


def write_entity_presence_csv(dataset, sv, path: Path) -> None:
    """One row per presence-evidence CLAIM (a person may have several) --
    both HRLT-sourced and register-sourced, clearly tagged by source_type
    so the two evidentiary tiers are never conflated."""
    register_presence = derive_register_presence(dataset)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "entity_id", "source_type", "source_id", "location_id",
            "presence_scope", "location_precision", "task",
            "valid_from", "valid_to", "evidence_status", "derivation_status",
        ])
        for person_id in sorted(dataset.persons):
            for (location_id, t_from, t_to) in sorted(sv.presence.get(person_id, ())):
                writer.writerow([
                    person_id, "hrlt", "", location_id,
                    "location", "location_level", "",
                    t_from, t_to, "explicit", "hrlt_presence",
                ])
            for rec in register_presence.get(person_id, ()):
                writer.writerow([
                    person_id, "register", rec.source_document_id, "",
                    rec.presence_scope, rec.location_precision, rec.task,
                    rec.date, rec.date, rec.evidence_status, rec.derivation_status,
                ])


def write_candidate_entities_csv(
    dataset, sv, path: Path, assigned_entity_ids: frozenset[str] | None = None
) -> None:
    """One row per person in ELIGIBLE_FOR_ASSIGNMENT / ASSIGNED /
    PRESENT_BUT_UNASSIGNED -- the current, HRLT-driven CP-SAT candidate
    pool (register presence does not add rows here this turn)."""
    eligible_states = {
        EntityState.ELIGIBLE_FOR_ASSIGNMENT, EntityState.ASSIGNED, EntityState.PRESENT_BUT_UNASSIGNED,
    }
    classifications = classify_entities(dataset, sv, assigned_entity_ids)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "entity_id", "name_canonical", "state", "has_hrlt_presence", "has_register_presence",
        ])
        for c in classifications:
            if c.state in eligible_states:
                writer.writerow([
                    c.entity_id, c.name_canonical, c.state.value,
                    c.has_hrlt_presence, c.has_register_presence,
                ])


def write_excluded_entities_csv(
    dataset, sv, path: Path, assigned_entity_ids: frozenset[str] | None = None
) -> None:
    """One row per person in DOCUMENTED_PRESENT (register-only, not solver-
    eligible this turn) or EXCLUDED_WITH_REASON (no evidence at all) -- the
    two are always distinguishable via `state` and `reason`, so a
    register-attested person is never conflated with a person the archive
    is silent about entirely."""
    excluded_states = {EntityState.DOCUMENTED_PRESENT, EntityState.EXCLUDED_WITH_REASON}
    classifications = classify_entities(dataset, sv, assigned_entity_ids)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["entity_id", "name_canonical", "state", "reason", "has_register_presence"])
        for c in classifications:
            if c.state in excluded_states:
                writer.writerow([c.entity_id, c.name_canonical, c.state.value, c.reason, c.has_register_presence])
