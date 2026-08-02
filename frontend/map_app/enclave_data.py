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