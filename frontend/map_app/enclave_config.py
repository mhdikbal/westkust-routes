"""
SALIDO-HDT enclave configuration — read-only data access paths.

This module provides path resolution for the canonical dataset and solver
snapshot directories, with safe local-development defaults derived from the
repository structure and Docker container paths from environment variables.

Environment variables (container):
  SALIDO_HDT_DATA_DIR     -> /app/data/salido_hdt_model_v0_4_1
  SALIDO_HDT_SCENARIO_DIR -> /app/data/salido_solver_snapshot
  SALIDO_HDT_CACHE_DIR    -> /tmp/salido-hdt-cache

Local development (no env vars set):
  Resolves relative to this file's location:
  - DATA_DIR: ../../../../docs/enclave/salido_hdt_model_v0_4_1
  - SCENARIO_DIR: ./data/enclave_1682_solver_run (committed snapshot)
  - CACHE_DIR: /tmp/salido-hdt-cache (system temp, never in repo)

The canonical dataset directories (v0_3, v0_4, v0_4_1) are IMMUTABLE.
This module NEVER writes to them. Any cache or derived output uses
SALIDO_HDT_CACHE_DIR.
"""

import os
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class EnclavePaths:
    """Resolved paths for the enclave application."""
    data_dir: Path
    scenario_dir: Path
    cache_dir: Path
    data_dir_exists: bool
    scenario_dir_exists: bool
    cache_dir_writable: bool
    scenario_snapshot_status: str  # "available" | "unavailable" | "error"


def _repo_root() -> Path:
    """Return the repository root (three levels up from frontend/map_app/)."""
    return Path(__file__).resolve().parents[3]


def _resolve_local_data_dir() -> Path:
    """Local development default for canonical dataset."""
    return _repo_root() / "docs" / "enclave" / "salido_hdt_model_v0_4_1"


def _resolve_local_scenario_dir() -> Path:
    """Local development default for committed solver snapshot."""
    return Path(__file__).resolve().parent / "data" / "enclave_1682_solver_run"


def _resolve_cache_dir() -> Path:
    """Cache directory — always system temp, never in repo."""
    return Path("/tmp/salido-hdt-cache")


def _check_writable(path: Path) -> bool:
    """Check if a directory exists and is writable."""
    try:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        test_file = path / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        return True
    except Exception:
        return False


def _check_readable(path: Path) -> bool:
    """Check if a directory exists and is readable."""
    try:
        if not path.exists() or not path.is_dir():
            return False
        # Try to list directory
        next(path.iterdir(), None)
        return True
    except Exception:
        return False


def _find_canonical_data_dir() -> Path | None:
    """
    Find the canonical dataset directory by checking known locations.

    Checks in order:
    1. Environment variable SALIDO_HDT_DATA_DIR (if absolute and exists)
    2. Container mount point /app/data/salido_hdt_model_v0_4_1
    3. Local development path relative to this file
    """
    # 1. Check env var first
    env_data = os.getenv("SALIDO_HDT_DATA_DIR")
    if env_data:
        p = Path(env_data)
        if p.is_absolute():
            # If env var is set, use it (even if doesn't exist - caller handles missing)
            return p
        # Non-absolute or empty, fall through

    # 2. Check container mount point
    container_path = Path("/app/data/salido_hdt_model_v0_4_1")
    if _check_readable(container_path):
        return container_path

    # 3. Check local development path
    local_path = _resolve_local_data_dir()
    if _check_readable(local_path):
        return local_path

    return None


def _find_scenario_dir() -> Path | None:
    """
    Find the solver snapshot directory by checking known locations.

    Checks in order:
    1. Environment variable SALIDO_HDT_SCENARIO_DIR (if absolute)
    2. Container mount point /app/data/salido_solver_snapshot
    3. Local development path relative to this file
    """
    # 1. Check env var first
    env_scenario = os.getenv("SALIDO_HDT_SCENARIO_DIR")
    if env_scenario:
        p = Path(env_scenario)
        if p.is_absolute():
            # If env var is set, use it (even if doesn't exist)
            return p

    # 2. Check container mount point
    container_path = Path("/app/data/salido_solver_snapshot")
    if _check_readable(container_path):
        return container_path

    # 3. Check local development path
    local_path = _resolve_local_scenario_dir()
    if _check_readable(local_path):
        return local_path

    return None


def _resolve_cache_dir_from_env() -> Path:
    """Resolve cache directory from env or default."""
    env_cache = os.getenv("SALIDO_HDT_CACHE_DIR")
    if env_cache:
        p = Path(env_cache)
        if p.is_absolute():
            return p
    return _resolve_cache_dir()


def load_enclave_paths() -> EnclavePaths:
    """
    Load and validate enclave paths from environment or discovered locations.

    Returns EnclavePaths with existence/writability checks performed.
    Does not raise — missing paths are reported via boolean flags and
    scenario_snapshot_status.
    """
    # Try to find canonical data directory
    data_dir = _find_canonical_data_dir()
    if data_dir is None:
        # Fall back to env var or local path (may not exist)
        env_data = os.getenv("SALIDO_HDT_DATA_DIR")
        if env_data and Path(env_data).is_absolute():
            data_dir = Path(env_data)
        else:
            data_dir = _resolve_local_data_dir()

    # Try to find scenario directory
    scenario_dir = _find_scenario_dir()
    if scenario_dir is None:
        # Fall back to env var or local path (may not exist)
        env_scenario = os.getenv("SALIDO_HDT_SCENARIO_DIR")
        if env_scenario and Path(env_scenario).is_absolute():
            scenario_dir = Path(env_scenario)
        else:
            scenario_dir = _resolve_local_scenario_dir()

    # Cache directory
    cache_dir = _resolve_cache_dir_from_env()

    # Perform checks
    data_dir_exists = _check_readable(data_dir)
    scenario_dir_exists = _check_readable(scenario_dir)
    cache_dir_writable = _check_writable(cache_dir)

    # Determine scenario snapshot status
    if scenario_dir_exists:
        # Check for expected solver output files
        expected_files = [
            "scenario_00.json",
            "scenario_01.json",
            "scenario_02.json",
            "scenario_03.json",
            "scenario_04.json",
            "validation_summary.json",
        ]
        if all((scenario_dir / f).exists() for f in expected_files):
            scenario_snapshot_status = "available"
        else:
            # Directory exists but incomplete/empty -> unavailable (not error)
            # Per plan: "Jika snapshot solver belum disiapkan... scenario_snapshot_status = unavailable"
            scenario_snapshot_status = "unavailable"
    else:
        scenario_snapshot_status = "unavailable"

    return EnclavePaths(
        data_dir=data_dir,
        scenario_dir=scenario_dir,
        cache_dir=cache_dir,
        data_dir_exists=data_dir_exists,
        scenario_dir_exists=scenario_dir_exists,
        cache_dir_writable=cache_dir_writable,
        scenario_snapshot_status=scenario_snapshot_status,
    )


def validate_enclave_config() -> list[str]:
    """
    Validate enclave configuration at startup.

    Returns a list of warning/error messages. Empty list = all good.
    Does not raise — callers decide how to handle.
    """
    paths = load_enclave_paths()
    issues = []

    if not paths.data_dir_exists:
        issues.append(
            f"Canonical dataset not found at {paths.data_dir}. "
            f"Set SALIDO_HDT_DATA_DIR or ensure docs/enclave/salido_hdt_model_v0_4_1 exists."
        )

    if not paths.cache_dir_writable:
        issues.append(
            f"Cache directory {paths.cache_dir} is not writable. "
            f"Set SALIDO_HDT_CACHE_DIR to a writable location."
        )

    if paths.scenario_snapshot_status == "unavailable":
        issues.append(
            f"Solver snapshot not found at {paths.scenario_dir}. "
            f"Expected scenario_00.json .. scenario_04.json + validation_summary.json. "
            f"Application will run with scenario_snapshot_status=unavailable."
        )
    elif paths.scenario_snapshot_status == "error":
        issues.append(
            f"Solver snapshot directory exists at {paths.scenario_dir} but "
            f"is missing expected files (scenario_00.json .. scenario_04.json, "
            f"validation_summary.json)."
        )

    return issues