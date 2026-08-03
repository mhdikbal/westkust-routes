"""
SALIDO-HDT enclave data adapter — stdlib-only CSV/JSON reader.

Read-only by construction: every file opened with mode "r" only.
Never modifies canonical dataset. Cache uses SALIDO_HDT_CACHE_DIR.
"""

import csv
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .enclave_config import load_enclave_paths


@dataclass(frozen=True, slots=True)
class EnclaveDatasetSummary:
    """Summary counts for the canonical dataset and scenario snapshot."""

    # Human entity metrics
    named_person_records: int
    aggregate_group_records: int
    independent_aggregate_groups: int
    aggregate_subgroups: int
    primary_entity_count: int
    total_human_related_records: int

    # Other metrics
    role_count: int
    location_count: int

    # Inventory metrics
    inventory_source_rows: int
    inventory_countable_items: int
    inventory_parent_or_container_rows: int

    # Other counts
    weekly_operation_count: int
    assay_count: int
    numeric_anomaly_count: int
    unresolved_reading_count: int

    # Status
    scenario_snapshot_status: str
    canonical_release: str


# Required canonical CSV files (per MANIFEST.csv)
REQUIRED_CSVS = {
    "01_documents.csv": "documents",
    "02_persons.csv": "persons",
    "03_roles.csv": "roles",
    "04_person_roles.csv": "person_roles",
    "05_locations.csv": "locations",
    "06_human_groups.csv": "human_groups",
    "07_human_role_location_time.csv": "human_role_location_time",
    "08_weekly_operations.csv": "weekly_operations",
    "09_assay_results.csv": "assay_results",
    "10_inventory_items.csv": "inventory_items",
    "11_claims.csv": "claims",
    "12_numeric_anomalies.csv": "numeric_anomalies",
    "13_data_dictionary.csv": "data_dictionary",
    "14_task_requirements.csv": "task_requirements",
    "15_role_location_compatibility.csv": "role_location_compatibility",
    "16_location_adjacency.csv": "location_adjacency",
    "MANIFEST.csv": "manifest",
}


def _sha256_file(path: Path) -> str:
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_csv_utf8_sig(path: Path) -> list[dict]:
    """Read CSV with utf-8-sig, preserve empty strings."""
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def _count_inventory_items_by_type(inventory: list[dict], row_type: str) -> int:
    """Count inventory rows by row_type."""
    return sum(1 for r in inventory if r.get("row_type") == row_type)


def _count_unresolved_readings(inventory: list[dict]) -> int:
    """Count unresolved readings from inventory."""
    return sum(1 for r in inventory if r.get("reading_status") == "unresolved")


def _extract_canonical_release(manifest_rows: list[dict]) -> str:
    """Extract canonical release from manifest or README."""
    for row in manifest_rows:
        fname = row.get("file", "")
        if "salido_hdt_model_v" in fname:
            import re
            match = re.search(r"salido_hdt_model_v([\d_]+)", fname)
            if match:
                return match.group(1).replace("_", ".")
    return "v0.4.1"


class EnclaveDataError(Exception):
    """Raised when canonical dataset cannot be loaded."""
    pass


@dataclass(frozen=True, slots=True)
class RestraintEvidenceEntry:
    """One reviewed restraint-device entry, cross-checked against canonical rows."""

    inventory_item_id: str
    source_passage_id: str
    source_paragraph_index: int
    document_section: str
    location_id: str
    object_count: int
    ring_count: int
    key_count: int
    source_translation_full: str
    presence_status: str
    actual_use_status: str
    target_person_status: str
    date_of_use_status: str


@dataclass(frozen=True, slots=True)
class RestraintEvidenceResult:
    """Result of load_restraint_evidence(): resolved entries plus any unresolved-mapping warnings."""

    entries: list[RestraintEvidenceEntry]
    warnings: list[str]


# Controlled visibility vocabulary for the People and Archival Visibility
# Explorer (S4-CRIT-02). A missing relational join is "not_structured",
# never "no_role"/"absent"/"zero" -- the join failing is a data-model fact,
# not an archival claim. Signature events exist in the source corpus but
# are not yet structured per person, so signature_visibility is always
# "not_structured", never "not_recorded" (which would wrongly imply the
# archive has no signatures at all).
VISIBILITY_STATES = frozenset({
    "recorded",
    "not_recorded",
    "not_structured",
    "not_evaluated",
    "not_applicable",
    "uncertain",
})

# Controlled vocabulary for assignment_evidence specifically. Derived
# independently of presence_basis: presence_basis reflects register/HRLT
# *reporting*, assignment_evidence reflects whether an actual role/task
# assignment record (07_human_role_location_time.csv) exists and what its
# own evidence_status says. "not_applicable" is reserved for records where
# an assignment is genuinely out of semantic scope (aggregate groups), not
# merely because assignment evidence happens to be missing for a person.
ASSIGNMENT_EVIDENCE_STATES = frozenset({
    "explicit",
    "interpreted",
    "reconstructed",
    "not_structured",
    "not_applicable",
})

# Maps an HRLT row's own evidence_status to assignment_evidence. Any value
# not in this mapping -- including a blank evidence_status -- falls through
# to "not_structured" and is never silently promoted to "explicit".
_HRLT_EVIDENCE_TO_ASSIGNMENT: dict[str, str] = {
    "explicit": "explicit",
    "interpreted": "interpreted",
    "reconstructed": "reconstructed",
}


@dataclass(frozen=True, slots=True)
class PersonVisibilityEntry:
    """One named-person record's archival-visibility status (S4-CRIT-02)."""

    person_id: str
    name_canonical: str
    role_visibility: str
    role_ids: tuple[str, ...]
    location_visibility: str
    location_ids: tuple[str, ...]
    signature_visibility: str
    assignment_evidence: str
    evidence_status: str
    source_document_id: str
    source_passage_id: str


@dataclass(frozen=True, slots=True)
class GroupVisibilityEntry:
    """One aggregate-group record's archival-visibility status (S4-CRIT-02)."""

    group_id: str
    source_category_original: str
    record_person_count: int
    status_category: str
    growth_category_original: str
    sex_category_original: str
    location_visibility: str
    location_ids: tuple[str, ...]
    assignment_evidence: str  # always "not_applicable" -- groups never receive a synthetic assignment
    evidence_status: str
    source_document_id: str
    source_passage_id: str


@dataclass(frozen=True, slots=True)
class PresenceVisibilityEntry:
    """One offline solver-snapshot presence-reporting row (S4-CRIT-02).

    presence_basis and assignment_evidence are derived independently, from
    different source signals: presence_basis from register/HRLT presence
    reporting (entity_presence.csv / candidate_entities.csv), assignment_evidence
    from the entity's own HRLT row evidence_status, if one exists.
    """

    entity_id: str
    presence_basis: str
    assignment_evidence: str
    derivation_status: str
    note: str


@dataclass(frozen=True, slots=True)
class VisibilityExplorerResult:
    """Result of load_visibility_explorer(): deterministic, read-only."""

    persons: list[PersonVisibilityEntry]
    groups: list[GroupVisibilityEntry]
    presence: list[PresenceVisibilityEntry]
    warnings: list[str]


AGGREGATION_ROLE_STATES = frozenset({"standalone_group", "parent_total", "component_group", "unknown"})
COUNT_SEMANTICS_STATES = frozenset({
    "count_once_as_parent",
    "count_once_as_components",
    "standalone_count",
    "do_not_sum_with_parent",
    "unresolved",
})
CROSS_DOCUMENT_OVERLAP_STATES = frozenset({
    "not_evaluated",
    "no_overlap_supported",
    "possible_overlap",
    "confirmed_overlap",
    "cannot_determine",
})
GROUP_HIERARCHY_DERIVATION_STATES = frozenset({
    "explicit",
    "reviewed_application_mapping",
    "interpreted",
    "unresolved",
})


@dataclass(frozen=True, slots=True)
class GroupHierarchyNode:
    """One of the 17 canonical group records, with its hierarchy role and count semantics (S4-CRIT-03)."""

    group_id: str
    source_category_original: str
    recorded_count: int
    aggregation_role: str
    count_semantics: str
    parent_group_id: Optional[str]
    component_group_ids: tuple[str, ...]
    component_count_sum: Optional[int]
    partition_reconciles: Optional[bool]
    cross_document_overlap_status: str
    source_document_id: str
    source_passage_id: str
    evidence_status: str
    review_status: str
    derivation_status: str


@dataclass(frozen=True, slots=True)
class GroupHierarchyRelation:
    """The one reviewed relation type in this ticket: the Madagascar parent/component partition."""

    parent_group_id: str
    component_group_id: str
    component_count: int
    derivation_status: str
    review_status: str
    notes: str


@dataclass(frozen=True, slots=True)
class LegacyGroupRelationCandidate:
    """One of the 3 pre-existing HUMAN_GROUP_HIERARCHY pairs that does not
    reconcile by count and was never reviewed as a parent/component relation.

    Deliberately has no parent_group_id/child_group_id -- direction has not
    been reviewed. group_a_id/group_b_id carry no directional claim. Never
    used for counting or de-duplication (counting_effect is always
    "not_applied").
    """

    group_a_id: str
    group_b_id: str
    relation_status: str
    derivation_status: str
    counting_effect: str
    warning_code: str


@dataclass(frozen=True, slots=True)
class CountSemanticsSummary:
    """Explicit, separated count tiers -- parent and components are never summed together."""

    parent_record_count: int
    component_record_count: int
    other_group_record_count: int
    total_group_record_count: int
    recorded_parent_count: int
    reconciled_component_sum: int
    arithmetic_discrepancy: int
    cross_document_unique_person_total: str


@dataclass(frozen=True, slots=True)
class GroupHierarchyWarning:
    code: str
    message: str
    group_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GroupHierarchyExplorerResult:
    """Result of load_group_hierarchy_explorer(): deterministic, read-only.

    1 (parent) + len(madagascar_components) + len(other_groups) always
    equals the canonical group-record count (17).
    """

    parent: GroupHierarchyNode
    madagascar_components: list[GroupHierarchyNode]
    other_groups: list[GroupHierarchyNode]
    relations: list[GroupHierarchyRelation]
    legacy_relation_candidates: list[LegacyGroupRelationCandidate]
    summary: CountSemanticsSummary
    warnings: list[GroupHierarchyWarning]


# Reviewed Madagascar parent/component partition (application-side,
# derivation_status="reviewed_application_mapping" -- NOT canonical; no
# parent_group_id column exists in 06_human_groups.csv). Component counts
# are the group's own canonical `count` column values; the partition is
# cross-checked against G-MADA-64's own count at load time (see
# load_group_hierarchy_explorer), not hardcoded as always-true.
GROUP_HIERARCHY_RELATIONS: tuple[dict, ...] = (
    {"parent_group_id": "G-MADA-64", "component_group_id": "G-MADA-VJ-10", "component_count": 10},
    {"parent_group_id": "G-MADA-64", "component_group_id": "G-MADA-HJ-8", "component_count": 8},
    {"parent_group_id": "G-MADA-64", "component_group_id": "G-MADA-VM-30", "component_count": 30},
    {"parent_group_id": "G-MADA-64", "component_group_id": "G-MADA-HM-10", "component_count": 10},
    {"parent_group_id": "G-MADA-64", "component_group_id": "G-MADA-K-6", "component_count": 6},
)

# Pre-existing HUMAN_GROUP_HIERARCHY pairs that do not reconcile by count
# (6 vs 4, 68 vs 3, 4 vs 19) and were never reviewed as parent/component
# relations. Listed without directional claim -- neither position implies
# parent or child.
LEGACY_UNREVIEWED_GROUP_PAIRS: tuple[tuple[str, str], ...] = (
    ("G-HWJ-6", "G-KJ-4"),
    ("G-SLAVIN-68", "G-MANDORESS-3"),
    ("G-CHILD-KOST-4", "G-CHILD-NOKOST-19"),
)


# Reviewed restraint-device mapping (application-side, NOT canonical).
# Ring/key counts are the researcher-attested reading recorded in
# A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md (committed f98cfb0, corrected 0361953).
# object_count is cross-checked against 10_inventory_items.csv's own `quantity`
# column at load time (see load_restraint_evidence); this constant does not
# modify or duplicate canonical data, and neither field asserts use or a target person.
RESTRAINT_EVIDENCE_MAPPING: tuple[dict, ...] = (
    {"source_passage_id": "SP-01267", "inventory_item_id": "INV-0343",
     "source_paragraph_index": 1267, "object_count": 1, "ring_count": 5, "key_count": 1},
    {"source_passage_id": "SP-01344", "inventory_item_id": "INV-0401",
     "source_paragraph_index": 1344, "object_count": 1, "ring_count": 3, "key_count": 1},
)


# Application-side human group hierarchy (reviewed grouping config, NOT canonical)
# Groups with a parent are "subgroups"; groups without are "independent aggregate groups".
# This does NOT modify the canonical dataset.
HUMAN_GROUP_HIERARCHY: dict[str, Optional[str]] = {
    "G-MS-121": None,
    "G-HWJ-6": None,
    "G-KJ-4": "G-HWJ-6",
    "G-GRAS-7": None,
    "G-COND-3": None,
    "G-MANDOOR-8": None,
    "G-VOORSLAGER-1": None,
    "G-SLAVIN-68": None,
    "G-MANDORESS-3": "G-SLAVIN-68",
    "G-CHILD-KOST-4": None,
    "G-CHILD-NOKOST-19": "G-CHILD-KOST-4",
    "G-MADA-64": None,
    "G-MADA-VJ-10": "G-MADA-64",
    "G-MADA-HJ-8": "G-MADA-64",
    "G-MADA-VM-30": "G-MADA-64",
    "G-MADA-HM-10": "G-MADA-64",
    "G-MADA-K-6": "G-MADA-64",
}


ROOT_BASIS_STATES = frozenset({
    "containment_root",
    "regional_external_location",
    "no_parent_recorded",
    "disconnected_reference",
    "parent_declared_without_contains_edge",
})
LOCATION_PRESENCE_BASIS_STATES = frozenset({
    "hrlt_record",
    "group_record_location",
    "not_structured",
})
LOCATION_RELATION_LABELS: dict[str, str] = {
    "contains": "Berisi",
    "approaches_or_audibly_connected": "Mendekati atau terhubung secara audibel",
    "topological_relation_unknown": "Relasi topologis belum diketahui",
    "associated_with": "Terkait secara dokumenter",
    "regional_route": "Rute regional",
    "shipping_route": "Rute pengapalan",
    "coerced_mobility_route": "Rute mobilitas paksa",
}
LOCATION_TOPOLOGY_WARNING_CODES = frozenset({
    "PARENT_DECLARED_WITHOUT_CONTAINS_EDGE",
    "UNRESOLVED_RELATION_ENDPOINT",
    "UNRESOLVED_PRESENCE_ENTITY",
    "CYCLIC_CONTAINMENT",
    "MULTIPLE_CONTAINMENT_PARENTS",
    "SELF_RELATION",
    "UNKNOWN_RELATION_TYPE",
})


@dataclass(frozen=True, slots=True)
class LocationTopologyNode:
    """One of the 23 canonical location records (S4-CRIT-04)."""

    location_id: str
    name_source: str
    name_normalized: str
    location_type: str
    parent_location_id: Optional[str]
    appears_as_contains_child: bool
    root_basis: Optional[str]
    evidence_status: str
    source_document_id: str
    source_passage_id: str


@dataclass(frozen=True, slots=True)
class LocationRelation:
    """One row of 16_location_adjacency.csv.

    Never carries source_document_id/source_passage_id -- that table has no
    such columns at all (verified header), and relation-level provenance is
    never copied from a node's own provenance.
    """

    edge_id: str
    from_location_id: str
    to_location_id: str
    relation_type: str
    evidence_status: str
    evidence_basis: str
    notes: str
    directionality: str
    derivation_status: str


@dataclass(frozen=True, slots=True)
class LocationHumanPresence:
    location_id: str
    entity_id: str
    entity_type: str
    presence_basis: str
    role_id: str
    evidence_status: str
    review_status: str
    assignment_evidence: str
    source_document_id: str
    source_passage_id: str


@dataclass(frozen=True, slots=True)
class LocationPresenceReconciliation:
    """Record counts and distinct-entity counts, always reported separately -- never a population figure."""

    hrlt_record_count: int
    hrlt_distinct_entity_count: int
    group_record_location_count: int
    group_only_distinct_count: int
    overlap_distinct_count: int
    total_presence_record_count: int
    total_distinct_entity_count: int


@dataclass(frozen=True, slots=True)
class LocationInventorySummary:
    location_id: str
    inventory_source_row_count: int
    inventory_non_parent_item_count: int
    inventory_parent_or_container_count: int


@dataclass(frozen=True, slots=True)
class LocationOperationSummary:
    """Record counts and evidence status only -- never a production or labour figure."""

    location_id: str
    weekly_operation_record_count: int
    period_start_earliest: str
    period_end_latest: str
    evidence_status_breakdown: tuple[str, ...]
    review_status_breakdown: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LocationTopologySummary:
    location_id: str
    named_person_record_count: int
    aggregate_group_record_count: int
    inventory_source_row_count: int
    inventory_non_parent_item_count: int
    weekly_operation_record_count: int
    role_compatibility_count: int
    location_relation_row_count: int


@dataclass(frozen=True, slots=True)
class RelationTypeCount:
    relation_type: str
    row_count: int


@dataclass(frozen=True, slots=True)
class LocationTopologyWarning:
    code: str
    message: str
    location_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LocationTopologyExplorerResult:
    """Result of load_location_topology_explorer(): deterministic, read-only.

    containment_roots (edge-graph derived, 7) and declared_parent_top_level_nodes
    (parent_location_id derived, 5) are kept as two separate lists, never merged --
    their difference is exactly parent_edge_inconsistencies (2).
    """

    nodes: list[LocationTopologyNode]
    relations: list[LocationRelation]
    containment_roots: list[LocationTopologyNode]
    declared_parent_top_level_nodes: list[LocationTopologyNode]
    parent_edge_inconsistencies: list[LocationTopologyWarning]
    presence: list[LocationHumanPresence]
    presence_reconciliation: LocationPresenceReconciliation
    inventory_summaries: list[LocationInventorySummary]
    operation_summaries: list[LocationOperationSummary]
    summaries: list[LocationTopologySummary]
    relation_type_counts: tuple[RelationTypeCount, ...]
    total_weekly_operation_record_count: int
    warnings: list[LocationTopologyWarning]


class EnclaveDataAdapter:
    """
    Read-only data adapter for SALIDO-HDT canonical dataset.

    All methods open files in "r" mode only. Never writes to canonical paths.
    """

    def __init__(self, paths=None):
        """Initialize adapter. paths is EnclavePaths from load_enclave_paths()."""
        if paths is None:
            paths = load_enclave_paths()
        self.paths = paths
        self._cache: dict[str, list[dict]] = {}
        self._hierarchy: dict[str, Optional[str]] = {}

    def _load_hierarchy(self) -> dict[str, Optional[str]]:
        """Load human group hierarchy from embedded application-side config."""
        if self._hierarchy:
            return self._hierarchy

        # Use embedded hierarchy as primary source
        self._hierarchy = dict(HUMAN_GROUP_HIERARCHY)

        # Optionally override from file if it exists (for local dev)
        hierarchy_path = self.paths.cache_dir / "human_group_hierarchy.csv"
        if not hierarchy_path.exists():
            local_path = Path(__file__).resolve().parent / "data" / "human_group_hierarchy.csv"
            if local_path.exists():
                hierarchy_path = local_path
            else:
                hierarchy_path = None

        if hierarchy_path and hierarchy_path.exists():
            rows = _read_csv_utf8_sig(hierarchy_path)
            for row in rows:
                gid = row.get("group_id", "").strip()
                parent = row.get("parent_group_id", "").strip()
                if gid and not gid.startswith("#"):
                    self._hierarchy[gid] = parent if parent else None

        return self._hierarchy

    def _compute_human_entity_metrics(self) -> tuple[int, int, int, int, int, int]:
        """
        Compute human entity metrics using hierarchy.

        Returns:
            (named_person_records, aggregate_group_records, independent_aggregate_groups,
             aggregate_subgroups, primary_entity_count, total_human_related_records)
        """
        persons = self.load_persons()
        human_groups = self.load_human_groups()
        hierarchy = self._load_hierarchy()

        named_person_records = len(persons)
        aggregate_group_records = len(human_groups)

        # Count independent vs subgroups using hierarchy
        independent = 0
        for g in human_groups:
            gid = g["group_id"]
            parent = hierarchy.get(gid)
            if parent is None:
                independent += 1

        independent_aggregate_groups = independent
        aggregate_subgroups = aggregate_group_records - independent_aggregate_groups
        primary_entity_count = named_person_records + independent_aggregate_groups
        total_human_related_records = named_person_records + aggregate_group_records

        return (
            named_person_records,
            aggregate_group_records,
            independent_aggregate_groups,
            aggregate_subgroups,
            primary_entity_count,
            total_human_related_records,
        )

    def validate_dataset(self) -> tuple[bool, list[str]]:
        """
        Validate that canonical dataset directory exists and has required files.

        Returns (is_valid, list_of_issues).
        """
        issues = []

        if not self.paths.data_dir_exists:
            issues.append(f"Canonical dataset directory not readable: {self.paths.data_dir}")
            return False, issues

        for filename in REQUIRED_CSVS:
            file_path = self.paths.data_dir / filename
            if not file_path.exists():
                issues.append(f"Required file missing: {filename}")

        return len(issues) == 0, issues

    def load_manifest(self) -> list[dict]:
        """Load MANIFEST.csv with file hashes."""
        if "manifest" not in self._cache:
            manifest_path = self.paths.data_dir / "MANIFEST.csv"
            self._cache["manifest"] = _read_csv_utf8_sig(manifest_path)
        return self._cache["manifest"]

    def verify_hashes(self) -> tuple[bool, list[str]]:
        """
        Verify file hashes against MANIFEST.csv for required CSV files only.

        Returns (all_match, list_of_mismatches).
        """
        manifest = self.load_manifest()
        mismatches = []

        required_files = set(REQUIRED_CSVS.keys())

        for row in manifest:
            fname = row.get("file", "")
            expected_hash = row.get("sha256", "")
            if not fname or not expected_hash:
                continue

            if "/" in fname:
                fname = fname.split("/")[-1]

            if fname not in required_files:
                continue

            file_path = self.paths.data_dir / fname
            if not file_path.exists():
                mismatches.append(f"File not found: {fname}")
                continue

            actual_hash = _sha256_file(file_path)
            if actual_hash != expected_hash:
                mismatches.append(f"Hash mismatch: {fname} (expected {expected_hash[:8]}..., got {actual_hash[:8]}...)")

        return len(mismatches) == 0, mismatches

    def load_documents(self) -> list[dict]:
        if "documents" not in self._cache:
            self._cache["documents"] = _read_csv_utf8_sig(self.paths.data_dir / "01_documents.csv")
        return self._cache["documents"]

    def load_persons(self) -> list[dict]:
        if "persons" not in self._cache:
            self._cache["persons"] = _read_csv_utf8_sig(self.paths.data_dir / "02_persons.csv")
        return self._cache["persons"]

    def load_roles(self) -> list[dict]:
        if "roles" not in self._cache:
            self._cache["roles"] = _read_csv_utf8_sig(self.paths.data_dir / "03_roles.csv")
        return self._cache["roles"]

    def load_person_roles(self) -> list[dict]:
        if "person_roles" not in self._cache:
            self._cache["person_roles"] = _read_csv_utf8_sig(self.paths.data_dir / "04_person_roles.csv")
        return self._cache["person_roles"]

    def load_locations(self) -> list[dict]:
        if "locations" not in self._cache:
            self._cache["locations"] = _read_csv_utf8_sig(self.paths.data_dir / "05_locations.csv")
        return self._cache["locations"]

    def load_human_groups(self) -> list[dict]:
        if "human_groups" not in self._cache:
            self._cache["human_groups"] = _read_csv_utf8_sig(self.paths.data_dir / "06_human_groups.csv")
        return self._cache["human_groups"]

    def load_human_role_location_time(self) -> list[dict]:
        if "human_role_location_time" not in self._cache:
            self._cache["human_role_location_time"] = _read_csv_utf8_sig(
                self.paths.data_dir / "07_human_role_location_time.csv"
            )
        return self._cache["human_role_location_time"]

    def load_weekly_operations(self) -> list[dict]:
        if "weekly_operations" not in self._cache:
            self._cache["weekly_operations"] = _read_csv_utf8_sig(
                self.paths.data_dir / "08_weekly_operations.csv"
            )
        return self._cache["weekly_operations"]

    def load_assay_results(self) -> list[dict]:
        if "assay_results" not in self._cache:
            self._cache["assay_results"] = _read_csv_utf8_sig(self.paths.data_dir / "09_assay_results.csv")
        return self._cache["assay_results"]

    def load_inventory_items(self) -> list[dict]:
        if "inventory_items" not in self._cache:
            self._cache["inventory_items"] = _read_csv_utf8_sig(self.paths.data_dir / "10_inventory_items.csv")
        return self._cache["inventory_items"]

    def load_claims(self) -> list[dict]:
        if "claims" not in self._cache:
            self._cache["claims"] = _read_csv_utf8_sig(self.paths.data_dir / "11_claims.csv")
        return self._cache["claims"]

    def load_numeric_anomalies(self) -> list[dict]:
        if "numeric_anomalies" not in self._cache:
            self._cache["numeric_anomalies"] = _read_csv_utf8_sig(self.paths.data_dir / "12_numeric_anomalies.csv")
        return self._cache["numeric_anomalies"]

    def load_data_dictionary(self) -> list[dict]:
        if "data_dictionary" not in self._cache:
            self._cache["data_dictionary"] = _read_csv_utf8_sig(self.paths.data_dir / "13_data_dictionary.csv")
        return self._cache["data_dictionary"]

    def load_task_requirements(self) -> list[dict]:
        if "task_requirements" not in self._cache:
            self._cache["task_requirements"] = _read_csv_utf8_sig(self.paths.data_dir / "14_task_requirements.csv")
        return self._cache["task_requirements"]

    def load_role_location_compatibility(self) -> list[dict]:
        if "role_location_compatibility" not in self._cache:
            self._cache["role_location_compatibility"] = _read_csv_utf8_sig(
                self.paths.data_dir / "15_role_location_compatibility.csv"
            )
        return self._cache["role_location_compatibility"]

    def load_location_adjacency(self) -> list[dict]:
        if "location_adjacency" not in self._cache:
            self._cache["location_adjacency"] = _read_csv_utf8_sig(self.paths.data_dir / "16_location_adjacency.csv")
        return self._cache["location_adjacency"]

    def load_source_passages(self) -> list[dict]:
        if "source_passages" not in self._cache:
            self._cache["source_passages"] = _read_csv_utf8_sig(self.paths.data_dir / "00_source_passages.csv")
        return self._cache["source_passages"]

    def load_restraint_evidence(self) -> RestraintEvidenceResult:
        """
        Read-only lookup of the two reviewed restraint-device entries (A0-5 finding).

        Never writes. Never substitutes a different row if a mapping is unresolved —
        emits a controlled warning instead of guessing. Never infers use or a target person.
        """
        inventory_by_id = {r["inventory_item_id"]: r for r in self.load_inventory_items()}
        passages_by_id = {r["source_passage_id"]: r for r in self.load_source_passages()}

        entries: list[RestraintEvidenceEntry] = []
        warnings: list[str] = []
        for m in RESTRAINT_EVIDENCE_MAPPING:
            inv_row = inventory_by_id.get(m["inventory_item_id"])
            sp_row = passages_by_id.get(m["source_passage_id"])
            if inv_row is None or sp_row is None:
                warnings.append(
                    f"Restraint evidence mapping unresolved: {m['source_passage_id']} -> "
                    f"{m['inventory_item_id']} (inventory_row_found={inv_row is not None}, "
                    f"passage_found={sp_row is not None})"
                )
                continue
            actual_paragraph = int(inv_row.get("source_paragraph_index") or 0)
            if actual_paragraph != m["source_paragraph_index"]:
                warnings.append(
                    f"Restraint evidence paragraph mismatch for {m['inventory_item_id']}: "
                    f"expected {m['source_paragraph_index']}, found {actual_paragraph}"
                )
                continue
            entries.append(RestraintEvidenceEntry(
                inventory_item_id=inv_row["inventory_item_id"],
                source_passage_id=sp_row["source_passage_id"],
                source_paragraph_index=actual_paragraph,
                document_section=inv_row.get("inventory_section", ""),
                location_id=inv_row.get("location_id", ""),
                object_count=m["object_count"],
                ring_count=m["ring_count"],
                key_count=m["key_count"],
                source_translation_full=inv_row.get("source_translation_full", ""),
                presence_status="explicit",
                actual_use_status="not_recorded",
                target_person_status="not_recorded",
                date_of_use_status="not_recorded",
            ))

        return RestraintEvidenceResult(entries=entries, warnings=warnings)

    def load_visibility_explorer(self) -> VisibilityExplorerResult:
        """
        Read-only People and Archival Visibility Explorer (S4-CRIT-02).

        Every dimension uses the controlled vocabulary in VISIBILITY_STATES /
        ASSIGNMENT_EVIDENCE_STATES. A missing role or location join is
        reported as "not_structured" (the relational join found no row),
        never "no_role", "absent", or "zero". signature_visibility is always
        "not_structured", never "not_recorded". assignment_evidence is
        derived independently of presence_basis, from each entity's own HRLT
        row evidence_status (never hardcoded, never promoted from a blank
        value to "explicit"); absence of an HRLT row is "not_structured",
        not "no historical assignment". Aggregate groups always get
        assignment_evidence="not_applicable" -- assignment is genuinely out
        of scope for a group record, and groups never receive a synthetic
        per-entity assignment. Never expands a group's count into synthetic
        per-person entries, and never sums group counts into a total.
        """
        persons = self.load_persons()
        groups = self.load_human_groups()
        hrlt = self.load_human_role_location_time()
        person_roles = self.load_person_roles()

        warnings: list[str] = []

        roles_by_person: dict[str, list[str]] = {}
        for pr in person_roles:
            pid = pr.get("person_id", "")
            if pid:
                roles_by_person.setdefault(pid, []).append(pr.get("role_id", ""))

        known_person_ids = {p["person_id"] for p in persons}
        known_group_ids = {g["group_id"] for g in groups}

        locations_by_entity: dict[str, list[str]] = {}
        assignment_by_person: dict[str, str] = {}
        for row in sorted(hrlt, key=lambda r: r.get("hrlt_id", "")):
            entity_id = row.get("human_or_group_id", "")
            entity_type = row.get("entity_type", "")
            location_id = row.get("location_id", "")
            if not entity_id:
                continue
            if entity_type == "individual" and entity_id not in known_person_ids:
                warnings.append(
                    f"Unresolved HRLT individual identifier: {entity_id} "
                    f"(row {row.get('hrlt_id', '?')})"
                )
                continue
            if entity_type == "aggregate_group" and entity_id not in known_group_ids:
                warnings.append(
                    f"Unresolved HRLT group identifier: {entity_id} "
                    f"(row {row.get('hrlt_id', '?')})"
                )
                continue
            if location_id:
                locations_by_entity.setdefault(entity_id, []).append(location_id)
            if entity_type == "individual" and entity_id not in assignment_by_person:
                assignment_by_person[entity_id] = _HRLT_EVIDENCE_TO_ASSIGNMENT.get(
                    row.get("evidence_status", ""), "not_structured"
                )

        person_entries: list[PersonVisibilityEntry] = []
        for p in sorted(persons, key=lambda r: r["person_id"]):
            pid = p["person_id"]
            role_ids = tuple(roles_by_person.get(pid, ()))
            location_ids = tuple(locations_by_entity.get(pid, ()))
            person_entries.append(PersonVisibilityEntry(
                person_id=pid,
                name_canonical=p.get("name_canonical", ""),
                role_visibility="recorded" if role_ids else "not_structured",
                role_ids=role_ids,
                location_visibility="recorded" if location_ids else "not_structured",
                location_ids=location_ids,
                signature_visibility="not_structured",
                assignment_evidence=assignment_by_person.get(pid, "not_structured"),
                evidence_status=p.get("evidence_status") or "not_recorded",
                source_document_id=p.get("source_document_id") or "not_recorded",
                source_passage_id=p.get("source_passage_id") or "not_recorded",
            ))

        group_entries: list[GroupVisibilityEntry] = []
        for g in sorted(groups, key=lambda r: r["group_id"]):
            gid = g["group_id"]
            own_location = g.get("location_id", "")
            location_ids = list(locations_by_entity.get(gid, ()))
            if own_location and own_location not in location_ids:
                location_ids.insert(0, own_location)
            group_entries.append(GroupVisibilityEntry(
                group_id=gid,
                source_category_original=g.get("source_category_original", ""),
                record_person_count=int(g.get("count") or 0),
                status_category=g.get("status_category", ""),
                growth_category_original=g.get("growth_category_original", ""),
                sex_category_original=g.get("sex_category_original", ""),
                location_visibility="recorded" if location_ids else "not_structured",
                location_ids=tuple(location_ids),
                assignment_evidence="not_applicable",
                evidence_status=g.get("evidence_status") or "not_recorded",
                source_document_id=g.get("source_document_id") or "not_recorded",
                source_passage_id=g.get("source_passage_id") or "not_recorded",
            ))

        presence_entries: list[PresenceVisibilityEntry] = []
        snapshot = self.load_scenario_snapshot()
        if snapshot is None:
            warnings.append(
                "Presence data not available offline (solver snapshot not mounted)."
            )
        else:
            hrlt_backed_ids = {
                r.get("entity_id", "")
                for r in snapshot.get("candidate_entities", [])
                if r.get("has_hrlt_presence") == "True"
            }
            note_by_id = {
                r.get("entity_id", ""): r.get("reason", "")
                for r in snapshot.get("excluded_entities", [])
            }
            for row in sorted(
                snapshot.get("entity_presence", []),
                key=lambda r: r.get("entity_id", ""),
            ):
                eid = row.get("entity_id", "")
                presence_entries.append(PresenceVisibilityEntry(
                    entity_id=eid,
                    presence_basis=(
                        "register_and_hrlt" if eid in hrlt_backed_ids
                        else "register_reporting_only"
                    ),
                    assignment_evidence=assignment_by_person.get(eid, "not_structured"),
                    derivation_status=row.get("derivation_status") or "not_recorded",
                    note=note_by_id.get(eid) or "not_recorded",
                ))

        return VisibilityExplorerResult(
            persons=person_entries,
            groups=group_entries,
            presence=presence_entries,
            warnings=warnings,
        )

    def load_group_hierarchy_explorer(self) -> GroupHierarchyExplorerResult:
        """
        Read-only Group Hierarchy and Count Semantics Explorer (S4-CRIT-03).

        The Madagascar parent/component relation is the only reviewed
        hierarchy in this ticket (derivation_status="reviewed_application_mapping"
        -- no canonical parent_group_id column exists, so this is never
        "explicit"). Parent and components are never summed together;
        component_count_sum is checked against the parent's own canonical
        count at load time, not hardcoded. 17 canonical group records
        partition exactly into 1 parent + 5 components + 11 other records --
        never rendered as "other 16". cross_document_overlap_status and
        cross_document_unique_person_total are both "not_evaluated": the
        cross-document overlap review has not been performed at the level
        exposed here -- distinct from "cannot_determine", which would mean a
        review was performed but evidence was insufficient. That is not the
        case here. The 3 legacy HUMAN_GROUP_HIERARCHY pairs that don't
        reconcile by count are surfaced as unresolved candidates only
        (group_a_id/group_b_id, no direction, counting_effect="not_applied")
        -- never folded into the reviewed relation set, never used for any
        count adjustment.
        """
        groups = self.load_human_groups()
        by_id = {g["group_id"]: g for g in groups}
        warnings: list[GroupHierarchyWarning] = []

        component_ids = tuple(r["component_group_id"] for r in GROUP_HIERARCHY_RELATIONS)
        component_count_sum = sum(r["component_count"] for r in GROUP_HIERARCHY_RELATIONS)
        parent_row = by_id.get("G-MADA-64")
        recorded_parent_count = int(parent_row.get("count") or 0) if parent_row else 0
        partition_reconciles = parent_row is not None and recorded_parent_count == component_count_sum
        if not partition_reconciles:
            warnings.append(GroupHierarchyWarning(
                code="madagascar_partition_mismatch",
                message=(
                    f"G-MADA-64 recorded count ({recorded_parent_count}) does not equal "
                    f"the reviewed component sum ({component_count_sum})."
                ),
                group_ids=("G-MADA-64",) + component_ids,
            ))

        parent = GroupHierarchyNode(
            group_id="G-MADA-64",
            source_category_original=(parent_row or {}).get("source_category_original", ""),
            recorded_count=recorded_parent_count,
            aggregation_role="parent_total",
            count_semantics="count_once_as_parent",
            parent_group_id=None,
            component_group_ids=component_ids,
            component_count_sum=component_count_sum,
            partition_reconciles=partition_reconciles,
            cross_document_overlap_status="not_evaluated",
            source_document_id=(parent_row or {}).get("source_document_id") or "not_recorded",
            source_passage_id=(parent_row or {}).get("source_passage_id") or "not_recorded",
            evidence_status=(parent_row or {}).get("evidence_status") or "not_recorded",
            review_status=(parent_row or {}).get("review_status") or "not_recorded",
            derivation_status="reviewed_application_mapping",
        )

        relations: list[GroupHierarchyRelation] = []
        madagascar_components: list[GroupHierarchyNode] = []
        for r in GROUP_HIERARCHY_RELATIONS:
            cid = r["component_group_id"]
            crow = by_id.get(cid)
            if crow is None:
                warnings.append(GroupHierarchyWarning(
                    code="madagascar_component_missing",
                    message=f"Reviewed component {cid} not found in canonical 06_human_groups.csv.",
                    group_ids=(cid,),
                ))
                continue
            relations.append(GroupHierarchyRelation(
                parent_group_id="G-MADA-64",
                component_group_id=cid,
                component_count=r["component_count"],
                derivation_status="reviewed_application_mapping",
                review_status=crow.get("review_status") or "not_recorded",
                notes="Reviewed application-side partition; no canonical parent_group_id column exists.",
            ))
            madagascar_components.append(GroupHierarchyNode(
                group_id=cid,
                source_category_original=crow.get("source_category_original", ""),
                recorded_count=int(crow.get("count") or 0),
                aggregation_role="component_group",
                count_semantics="do_not_sum_with_parent",
                parent_group_id="G-MADA-64",
                component_group_ids=(),
                component_count_sum=None,
                partition_reconciles=None,
                cross_document_overlap_status="not_evaluated",
                source_document_id=crow.get("source_document_id") or "not_recorded",
                source_passage_id=crow.get("source_passage_id") or "not_recorded",
                evidence_status=crow.get("evidence_status") or "not_recorded",
                review_status=crow.get("review_status") or "not_recorded",
                derivation_status="reviewed_application_mapping",
            ))

        madagascar_ids = {"G-MADA-64"} | set(component_ids)
        other_groups: list[GroupHierarchyNode] = []
        for g in sorted(groups, key=lambda r: r["group_id"]):
            gid = g["group_id"]
            if gid in madagascar_ids:
                continue
            other_groups.append(GroupHierarchyNode(
                group_id=gid,
                source_category_original=g.get("source_category_original", ""),
                recorded_count=int(g.get("count") or 0),
                aggregation_role="standalone_group",
                count_semantics="standalone_count",
                parent_group_id=None,
                component_group_ids=(),
                component_count_sum=None,
                partition_reconciles=None,
                cross_document_overlap_status="not_evaluated",
                source_document_id=g.get("source_document_id") or "not_recorded",
                source_passage_id=g.get("source_passage_id") or "not_recorded",
                evidence_status=g.get("evidence_status") or "not_recorded",
                review_status=g.get("review_status") or "not_recorded",
                derivation_status="explicit",
            ))

        legacy_relation_candidates: list[LegacyGroupRelationCandidate] = []
        for a, b in LEGACY_UNREVIEWED_GROUP_PAIRS:
            if a not in by_id or b not in by_id:
                warnings.append(GroupHierarchyWarning(
                    code="legacy_pair_group_missing",
                    message=f"Legacy pair references a group not found in canonical data: {a} / {b}.",
                    group_ids=(a, b),
                ))
                continue
            legacy_relation_candidates.append(LegacyGroupRelationCandidate(
                group_a_id=a,
                group_b_id=b,
                relation_status="unresolved",
                derivation_status="not_reviewed",
                counting_effect="not_applied",
                warning_code="UNREVIEWED_LEGACY_GROUP_RELATION",
            ))

        summary = CountSemanticsSummary(
            parent_record_count=1,
            component_record_count=len(madagascar_components),
            other_group_record_count=len(other_groups),
            total_group_record_count=1 + len(madagascar_components) + len(other_groups),
            recorded_parent_count=recorded_parent_count,
            reconciled_component_sum=component_count_sum,
            arithmetic_discrepancy=recorded_parent_count - component_count_sum,
            cross_document_unique_person_total="not_evaluated",
        )

        return GroupHierarchyExplorerResult(
            parent=parent,
            madagascar_components=madagascar_components,
            other_groups=other_groups,
            relations=relations,
            legacy_relation_candidates=legacy_relation_candidates,
            summary=summary,
            warnings=warnings,
        )

    def load_location_topology_explorer(self) -> LocationTopologyExplorerResult:
        """
        Read-only Topologi Lokasi dan Infrastruktur Sosial-Teknis explorer (S4-CRIT-04).

        Two distinct topology representations are kept separate and never merged:
        containment_roots is derived purely from 16_location_adjacency.csv's
        `contains` edges (23 nodes minus the 16 distinct contains-edge children =
        7 roots); declared_parent_top_level_nodes is derived purely from
        05_locations.csv's own `parent_location_id` field (5 roots). Their
        difference (2 nodes -- L-ZZW-DAGGANG, L-MALEIJTS-ORT -- each with a
        stated parent but no confirming contains edge) is never resolved by
        synthesizing a missing edge or by hiding either fact; both nodes remain
        visible in every relevant list and are reported via
        parent_edge_inconsistencies (code=PARENT_DECLARED_WITHOUT_CONTAINS_EDGE).

        Presence is built from two independent sources and never deduplicated:
        07_human_role_location_time.csv rows (presence_basis="hrlt_record") and
        06_human_groups.csv rows (presence_basis="group_record_location"). The
        10 groups attested by both sources keep both records -- 32 presence
        records total, 22 distinct entities, reported as separate numbers,
        never as one population count. Role-location compatibility
        (15_role_location_compatibility.csv) is a model-input rule, counted
        only in role_compatibility_count, never added to `presence`. A location
        stated on an aggregate-group record is never expanded into individual
        presence for unnamed members.

        16_location_adjacency.csv carries no source_document_id/source_passage_id
        columns -- LocationRelation never fabricates them, and relation-level
        provenance is never copied from a node's own provenance.

        No labour/productivity figure is ever computed: weekly-operation and
        inventory summaries expose only record counts and evidence/review
        status, never schoten or ore_weight_lb divided by any person or group
        count.
        """
        locations = self.load_locations()
        adjacency = self.load_location_adjacency()
        groups = self.load_human_groups()
        hrlt = self.load_human_role_location_time()
        operations = self.load_weekly_operations()
        inventory = self.load_inventory_items()
        role_compat = self.load_role_location_compatibility()
        persons = self.load_persons()

        loc_ids = {l["location_id"] for l in locations}
        person_ids = {p["person_id"] for p in persons}
        group_ids = {g["group_id"] for g in groups}

        warnings: list[LocationTopologyWarning] = []

        # --- Relations -------------------------------------------------------
        relations: list[LocationRelation] = []
        relation_type_counter: dict[str, int] = {}
        contains_children: dict[str, list[str]] = {}
        for row in sorted(adjacency, key=lambda r: r["edge_id"]):
            rel_type = row.get("relation_type", "")
            relation_type_counter[rel_type] = relation_type_counter.get(rel_type, 0) + 1

            from_id = row.get("from_location_id", "")
            to_id = row.get("to_location_id", "")

            if from_id not in loc_ids or to_id not in loc_ids:
                warnings.append(LocationTopologyWarning(
                    code="UNRESOLVED_RELATION_ENDPOINT",
                    message=(
                        f"Relation {row.get('edge_id', '?')} references an unknown "
                        f"location ({from_id} -> {to_id})."
                    ),
                    location_ids=(from_id, to_id),
                ))
                continue

            if from_id == to_id:
                warnings.append(LocationTopologyWarning(
                    code="SELF_RELATION",
                    message=f"Relation {row.get('edge_id', '?')} has identical from/to location ({from_id}).",
                    location_ids=(from_id,),
                ))

            if rel_type not in LOCATION_RELATION_LABELS:
                warnings.append(LocationTopologyWarning(
                    code="UNKNOWN_RELATION_TYPE",
                    message=(
                        f"Relation {row.get('edge_id', '?')} uses an unrecognized "
                        f"relation_type: {rel_type}."
                    ),
                    location_ids=(from_id, to_id),
                ))

            bidirectional_raw = (row.get("bidirectional") or "").strip().lower()
            directionality = "bidirectional" if bidirectional_raw == "true" else "unidirectional"

            relations.append(LocationRelation(
                edge_id=row.get("edge_id", ""),
                from_location_id=from_id,
                to_location_id=to_id,
                relation_type=rel_type,
                evidence_status=row.get("evidence_status") or "not_recorded",
                evidence_basis=row.get("evidence_basis") or "not_recorded",
                notes=row.get("notes") or "not_recorded",
                directionality=directionality,
                derivation_status="canonical_row",
            ))

            if rel_type == "contains":
                contains_children.setdefault(to_id, []).append(from_id)

        for child, parents in contains_children.items():
            if len(set(parents)) > 1:
                warnings.append(LocationTopologyWarning(
                    code="MULTIPLE_CONTAINMENT_PARENTS",
                    message=(
                        f"{child} is listed as a contains-child of more than one "
                        f"location: {sorted(set(parents))}."
                    ),
                    location_ids=(child,) + tuple(sorted(set(parents))),
                ))

        contains_child_ids = set(contains_children.keys())

        # --- Cycle check (parent_location_id walk) ----------------------------
        parent_map = {l["location_id"]: (l.get("parent_location_id") or None) for l in locations}

        def _walk_has_cycle(start: str) -> bool:
            seen: set[str] = set()
            cur: Optional[str] = start
            while cur:
                if cur in seen:
                    return True
                seen.add(cur)
                cur = parent_map.get(cur)
            return False

        cyclic_nodes = tuple(sorted(lid for lid in loc_ids if _walk_has_cycle(lid)))
        if cyclic_nodes:
            warnings.append(LocationTopologyWarning(
                code="CYCLIC_CONTAINMENT",
                message=f"Containment cycle detected involving: {cyclic_nodes}.",
                location_ids=cyclic_nodes,
            ))

        # --- Nodes and root classification -------------------------------------
        declared_parent_ids = {l["location_id"] for l in locations if not l.get("parent_location_id")}
        containment_root_ids = loc_ids - contains_child_ids
        parent_edge_inconsistency_ids = containment_root_ids - declared_parent_ids
        contains_from_ids = {r["from_location_id"] for r in adjacency if r["relation_type"] == "contains"}

        def _root_basis(lid: str, parent_blank: bool) -> Optional[str]:
            if lid in parent_edge_inconsistency_ids:
                return "parent_declared_without_contains_edge"
            if not parent_blank:
                return None
            if lid in contains_from_ids:
                return "containment_root"
            referenced_elsewhere = (
                any(r["from_location_id"] == lid or r["to_location_id"] == lid for r in adjacency)
                or any(g["location_id"] == lid for g in groups)
                or any(h["location_id"] == lid for h in hrlt)
                or any(o["location_id"] == lid for o in operations)
                or any(i["location_id"] == lid for i in inventory)
                or any(rc["location_id"] == lid for rc in role_compat)
            )
            return "regional_external_location" if referenced_elsewhere else "disconnected_reference"

        nodes: list[LocationTopologyNode] = []
        for l in sorted(locations, key=lambda r: r["location_id"]):
            lid = l["location_id"]
            parent_blank = not l.get("parent_location_id")
            nodes.append(LocationTopologyNode(
                location_id=lid,
                name_source=l.get("name_original", ""),
                name_normalized=l.get("name_normalized_id", ""),
                location_type=l.get("location_type", ""),
                parent_location_id=l.get("parent_location_id") or None,
                appears_as_contains_child=lid in contains_child_ids,
                root_basis=_root_basis(lid, parent_blank),
                evidence_status=l.get("evidence_status") or "not_recorded",
                source_document_id=l.get("source_document_id") or "not_recorded",
                source_passage_id=l.get("source_passage_id") or "not_recorded",
            ))

        nodes_by_id = {n.location_id: n for n in nodes}
        containment_roots = [nodes_by_id[lid] for lid in sorted(containment_root_ids)]
        declared_parent_top_level_nodes = [nodes_by_id[lid] for lid in sorted(declared_parent_ids)]

        parent_edge_inconsistencies: list[LocationTopologyWarning] = []
        for lid in sorted(parent_edge_inconsistency_ids):
            stated_parent = nodes_by_id[lid].parent_location_id
            parent_edge_inconsistencies.append(LocationTopologyWarning(
                code="PARENT_DECLARED_WITHOUT_CONTAINS_EDGE",
                message=(
                    f"{lid} states parent_location_id={stated_parent}, but no contains "
                    f"edge {stated_parent} -> {lid} exists in 16_location_adjacency.csv."
                ),
                location_ids=(lid,),
            ))
        warnings.extend(parent_edge_inconsistencies)

        # --- Presence ------------------------------------------------------------
        presence: list[LocationHumanPresence] = []
        for row in sorted(hrlt, key=lambda r: r["hrlt_id"]):
            entity_id = row.get("human_or_group_id", "")
            entity_type = row.get("entity_type", "")
            loc_id = row.get("location_id", "")
            if loc_id not in loc_ids:
                warnings.append(LocationTopologyWarning(
                    code="UNRESOLVED_RELATION_ENDPOINT",
                    message=f"HRLT row {row.get('hrlt_id', '?')} references an unknown location: {loc_id}.",
                    location_ids=(loc_id,),
                ))
                continue
            if entity_type == "individual" and entity_id not in person_ids:
                warnings.append(LocationTopologyWarning(
                    code="UNRESOLVED_PRESENCE_ENTITY",
                    message=f"HRLT row {row.get('hrlt_id', '?')} references an unknown person: {entity_id}.",
                    location_ids=(loc_id,),
                ))
                continue
            if entity_type == "aggregate_group" and entity_id not in group_ids:
                warnings.append(LocationTopologyWarning(
                    code="UNRESOLVED_PRESENCE_ENTITY",
                    message=f"HRLT row {row.get('hrlt_id', '?')} references an unknown group: {entity_id}.",
                    location_ids=(loc_id,),
                ))
                continue
            presence_basis = "hrlt_record" if entity_type in ("individual", "aggregate_group") else "not_structured"
            presence.append(LocationHumanPresence(
                location_id=loc_id,
                entity_id=entity_id,
                entity_type=entity_type or "not_structured",
                presence_basis=presence_basis,
                role_id=row.get("role_id") or "not_applicable",
                evidence_status=row.get("evidence_status") or "not_recorded",
                review_status=row.get("review_status") or "not_recorded",
                assignment_evidence=_HRLT_EVIDENCE_TO_ASSIGNMENT.get(
                    row.get("evidence_status", ""), "not_structured"
                ),
                source_document_id=row.get("source_document_id") or "not_recorded",
                source_passage_id=row.get("source_passage_id") or "not_recorded",
            ))

        hrlt_record_count = sum(1 for p in presence if p.presence_basis == "hrlt_record")
        hrlt_distinct_entity_count = len(
            {p.entity_id for p in presence if p.presence_basis == "hrlt_record"}
        )

        for g in sorted(groups, key=lambda r: r["group_id"]):
            loc_id = g.get("location_id", "")
            if loc_id not in loc_ids:
                warnings.append(LocationTopologyWarning(
                    code="UNRESOLVED_RELATION_ENDPOINT",
                    message=f"Group {g.get('group_id', '?')} references an unknown location: {loc_id}.",
                    location_ids=(loc_id,),
                ))
                continue
            presence.append(LocationHumanPresence(
                location_id=loc_id,
                entity_id=g["group_id"],
                entity_type="aggregate_group",
                presence_basis="group_record_location",
                role_id="not_applicable",
                evidence_status=g.get("evidence_status") or "not_recorded",
                review_status=g.get("review_status") or "not_recorded",
                assignment_evidence="not_applicable",
                source_document_id=g.get("source_document_id") or "not_recorded",
                source_passage_id=g.get("source_passage_id") or "not_recorded",
            ))

        group_record_location_count = sum(
            1 for p in presence if p.presence_basis == "group_record_location"
        )
        hrlt_group_ids = {
            p.entity_id for p in presence
            if p.presence_basis == "hrlt_record" and p.entity_type == "aggregate_group"
        }
        group_only_ids = group_ids - hrlt_group_ids
        overlap_ids = group_ids & hrlt_group_ids

        presence_reconciliation = LocationPresenceReconciliation(
            hrlt_record_count=hrlt_record_count,
            hrlt_distinct_entity_count=hrlt_distinct_entity_count,
            group_record_location_count=group_record_location_count,
            group_only_distinct_count=len(group_only_ids),
            overlap_distinct_count=len(overlap_ids),
            total_presence_record_count=len(presence),
            total_distinct_entity_count=len({p.entity_id for p in presence}),
        )

        # --- Inventory summaries -----------------------------------------------
        inventory_summaries: list[LocationInventorySummary] = []
        for lid in sorted(loc_ids):
            rows_here = [r for r in inventory if r.get("location_id") == lid]
            non_parent = sum(1 for r in rows_here if r.get("row_type") != "container_or_parent")
            parent_or_container = sum(1 for r in rows_here if r.get("row_type") == "container_or_parent")
            inventory_summaries.append(LocationInventorySummary(
                location_id=lid,
                inventory_source_row_count=len(rows_here),
                inventory_non_parent_item_count=non_parent,
                inventory_parent_or_container_count=parent_or_container,
            ))

        # --- Operation summaries ------------------------------------------------
        operation_summaries: list[LocationOperationSummary] = []
        for lid in sorted(loc_ids):
            rows_here = [r for r in operations if r.get("location_id") == lid]
            starts = sorted(r["period_start"] for r in rows_here if r.get("period_start"))
            ends = sorted(r["period_end"] for r in rows_here if r.get("period_end"))
            operation_summaries.append(LocationOperationSummary(
                location_id=lid,
                weekly_operation_record_count=len(rows_here),
                period_start_earliest=starts[0] if starts else "not_recorded",
                period_end_latest=ends[-1] if ends else "not_recorded",
                evidence_status_breakdown=tuple(
                    sorted({r.get("evidence_status") or "not_recorded" for r in rows_here})
                ),
                review_status_breakdown=tuple(
                    sorted({r.get("review_status") or "not_recorded" for r in rows_here})
                ),
            ))

        # --- Per-location rollup -------------------------------------------------
        named_person_counts: dict[str, int] = {}
        aggregate_group_counts: dict[str, int] = {}
        for p in presence:
            if p.entity_type == "individual":
                named_person_counts[p.location_id] = named_person_counts.get(p.location_id, 0) + 1
            elif p.entity_type == "aggregate_group" and p.presence_basis == "group_record_location":
                aggregate_group_counts[p.location_id] = aggregate_group_counts.get(p.location_id, 0) + 1

        role_compat_counts: dict[str, int] = {}
        for r in role_compat:
            lid = r.get("location_id", "")
            role_compat_counts[lid] = role_compat_counts.get(lid, 0) + 1

        relation_row_counts: dict[str, int] = {}
        for r in relations:
            relation_row_counts[r.from_location_id] = relation_row_counts.get(r.from_location_id, 0) + 1
            if r.to_location_id != r.from_location_id:
                relation_row_counts[r.to_location_id] = relation_row_counts.get(r.to_location_id, 0) + 1

        inv_by_id = {s.location_id: s for s in inventory_summaries}
        op_by_id = {s.location_id: s for s in operation_summaries}

        summaries: list[LocationTopologySummary] = []
        for lid in sorted(loc_ids):
            summaries.append(LocationTopologySummary(
                location_id=lid,
                named_person_record_count=named_person_counts.get(lid, 0),
                aggregate_group_record_count=aggregate_group_counts.get(lid, 0),
                inventory_source_row_count=inv_by_id[lid].inventory_source_row_count,
                inventory_non_parent_item_count=inv_by_id[lid].inventory_non_parent_item_count,
                weekly_operation_record_count=op_by_id[lid].weekly_operation_record_count,
                role_compatibility_count=role_compat_counts.get(lid, 0),
                location_relation_row_count=relation_row_counts.get(lid, 0),
            ))

        relation_type_counts = tuple(
            RelationTypeCount(relation_type=rt, row_count=cnt)
            for rt, cnt in sorted(relation_type_counter.items())
        )

        return LocationTopologyExplorerResult(
            nodes=nodes,
            relations=relations,
            containment_roots=containment_roots,
            declared_parent_top_level_nodes=declared_parent_top_level_nodes,
            parent_edge_inconsistencies=parent_edge_inconsistencies,
            presence=presence,
            presence_reconciliation=presence_reconciliation,
            inventory_summaries=inventory_summaries,
            operation_summaries=operation_summaries,
            summaries=summaries,
            relation_type_counts=relation_type_counts,
            total_weekly_operation_record_count=len(operations),
            warnings=warnings,
        )

    def get_summary(self) -> EnclaveDatasetSummary:
        """Compute summary counts for the canonical dataset."""
        persons = self.load_persons()
        human_groups = self.load_human_groups()
        inventory = self.load_inventory_items()

        (
            named_person_records,
            aggregate_group_records,
            independent_aggregate_groups,
            aggregate_subgroups,
            primary_entity_count,
            total_human_related_records,
        ) = self._compute_human_entity_metrics()

        return EnclaveDatasetSummary(
            # Human entities
            named_person_records=named_person_records,
            aggregate_group_records=aggregate_group_records,
            independent_aggregate_groups=independent_aggregate_groups,
            aggregate_subgroups=aggregate_subgroups,
            primary_entity_count=primary_entity_count,
            total_human_related_records=total_human_related_records,
            # Other
            role_count=len(self.load_roles()),
            location_count=len(self.load_locations()),
            # Inventory
            inventory_source_rows=len(inventory),
            inventory_countable_items=_count_inventory_items_by_type(inventory, "inventory_item"),
            inventory_parent_or_container_rows=_count_inventory_items_by_type(inventory, "container_or_parent"),
            # Other counts
            weekly_operation_count=len(self.load_weekly_operations()),
            assay_count=len(self.load_assay_results()),
            numeric_anomaly_count=len(self.load_numeric_anomalies()),
            unresolved_reading_count=_count_unresolved_readings(inventory),
            # Status
            scenario_snapshot_status=self.paths.scenario_snapshot_status,
            canonical_release=_extract_canonical_release(self.load_manifest()),
        )

    def load_scenario_snapshot(self) -> Optional[dict]:
        """
        Load solver scenario snapshot if available.

        Returns dict with scenarios, validation_summary, etc. or None if unavailable.
        """
        if self.paths.scenario_snapshot_status != "available":
            return None

        snapshot = {}
        scenario_dir = self.paths.scenario_dir

        scenarios = []
        for i in range(5):
            scenario_path = scenario_dir / f"scenario_{i:02d}.json"
            if scenario_path.exists():
                with scenario_path.open("r", encoding="utf-8") as f:
                    scenarios.append(json.load(f))
        snapshot["scenarios"] = scenarios

        validation_path = scenario_dir / "validation_summary.json"
        if validation_path.exists():
            with validation_path.open("r", encoding="utf-8") as f:
                snapshot["validation_summary"] = json.load(f)

        csv_files = {
            "equipment_capacity": "equipment_capacity.csv",
            "entity_presence": "entity_presence.csv",
            "candidate_entities": "candidate_entities.csv",
            "excluded_entities": "excluded_entities.csv",
        }
        for key, fname in csv_files.items():
            fpath = scenario_dir / fname
            if fpath.exists():
                snapshot[key] = _read_csv_utf8_sig(fpath)

        return snapshot


# Module-level convenience functions
_default_adapter: Optional[EnclaveDataAdapter] = None


def get_adapter() -> EnclaveDataAdapter:
    """Get module-level singleton adapter."""
    global _default_adapter
    if _default_adapter is None:
        _default_adapter = EnclaveDataAdapter()
    return _default_adapter


def get_dataset_summary() -> EnclaveDatasetSummary:
    """Get canonical dataset summary."""
    return get_adapter().get_summary()


def load_canonical_csv(csv_name: str) -> list[dict]:
    """Load a canonical CSV by logical name."""
    adapter = get_adapter()
    method_map = {
        "documents": adapter.load_documents,
        "persons": adapter.load_persons,
        "roles": adapter.load_roles,
        "person_roles": adapter.load_person_roles,
        "locations": adapter.load_locations,
        "human_groups": adapter.load_human_groups,
        "human_role_location_time": adapter.load_human_role_location_time,
        "weekly_operations": adapter.load_weekly_operations,
        "assay_results": adapter.load_assay_results,
        "inventory_items": adapter.load_inventory_items,
        "claims": adapter.load_claims,
        "numeric_anomalies": adapter.load_numeric_anomalies,
        "data_dictionary": adapter.load_data_dictionary,
        "task_requirements": adapter.load_task_requirements,
        "role_location_compatibility": adapter.load_role_location_compatibility,
        "location_adjacency": adapter.load_location_adjacency,
    }
    if csv_name not in method_map:
        raise ValueError(f"Unknown CSV: {csv_name}")
    return method_map[csv_name]()