"""Dedicated, repo-wide guard: nothing in the solver package may ever write
to salido_hdt_model_v0_4_1/ (or v0.3/v0.4). Mirrors the SHA-256 discipline
used throughout every prior task in this session (AUDIT_REPORT.md,
V0_4_MIGRATION_PLAN.md, V0_4_SEMANTIC_QA.md, V0_4_1_VALIDATION_REPORT.md,
SOLVER_INPUT_READINESS.md all re-verified this the same way)."""
import hashlib
from pathlib import Path

from salido_hdt.solver import config


def _hash_tree(root: Path) -> dict[str, str]:
    hashes = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and "Zone.Identifier" not in path.name:
            hashes[str(path.relative_to(root))] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return hashes


def test_data_loader_does_not_mutate_v0_4_1(tmp_path):
    from salido_hdt.solver.data_loader import load_dataset

    before = _hash_tree(config.V0_4_1_ROOT)
    load_dataset(config.V0_4_1_ROOT)
    after = _hash_tree(config.V0_4_1_ROOT)
    assert before == after


def test_full_cli_run_does_not_mutate_v0_4_1(tmp_path):
    from salido_hdt.solver.cli import run

    before_v3 = _hash_tree(config.V0_4_1_ROOT.parent / "salido_hdt_model_v0_3")
    before_v4 = _hash_tree(config.V0_4_1_ROOT.parent / "salido_hdt_model_v0_4")
    before_v41 = _hash_tree(config.V0_4_1_ROOT)

    output_dir = tmp_path / "solver_run"
    run(root=config.V0_4_1_ROOT, output_dir=output_dir, max_scenarios=1)

    after_v3 = _hash_tree(config.V0_4_1_ROOT.parent / "salido_hdt_model_v0_3")
    after_v4 = _hash_tree(config.V0_4_1_ROOT.parent / "salido_hdt_model_v0_4")
    after_v41 = _hash_tree(config.V0_4_1_ROOT)

    assert before_v3 == after_v3
    assert before_v4 == after_v4
    assert before_v41 == after_v41
    # the run must have written its output OUTSIDE the canonical tree
    assert output_dir.exists()
    assert list(output_dir.glob("*.json"))
