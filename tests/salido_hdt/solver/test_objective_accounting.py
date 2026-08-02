"""Regression guards for v0.1.2 Item 2 (SOLVER_V0_1_2_FIX_PLAN.md):
structural-zero objective categories must be explicitly disclosed in
output, not just documented in a docstring nobody reading the JSON sees.
"""
import json

from salido_hdt.solver import config
from salido_hdt.solver.cli import run
from salido_hdt.solver.objective import STRUCTURAL_ZERO_CATEGORIES


def test_structural_zero_categories_constant_is_the_two_hard_enforced_ones():
    assert STRUCTURAL_ZERO_CATEGORIES == frozenset({
        "temporal_violations", "topological_violations",
    })


def test_structural_zero_categories_reported_in_validation_summary(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    summary = json.loads((output_dir / "validation_summary.json").read_text(encoding="utf-8"))
    assert summary["structural_zero_categories"] == sorted(STRUCTURAL_ZERO_CATEGORIES)


def test_structural_zero_categories_reported_in_scenario_json(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    payload = json.loads((output_dir / "scenario_00.json").read_text(encoding="utf-8"))
    assert payload["structural_zero_categories"] == sorted(STRUCTURAL_ZERO_CATEGORIES)


def test_structural_zero_categories_are_actually_always_zero_in_practice(tmp_path):
    """Live check that the documentation constant hasn't drifted out of
    sync with the actual wiring -- a plain docstring claim cannot
    self-verify this."""
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    payload = json.loads((output_dir / "scenario_00.json").read_text(encoding="utf-8"))
    for category in payload["structural_zero_categories"]:
        assert payload["penalty_breakdown"][category] == 0
