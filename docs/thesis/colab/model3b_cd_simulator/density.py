"""Spec A CD annual document density: read-only loader + log1p transform.

Source of truth: docs/thesis/colab/CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv
(Spec A column `cd_documents_all_accepted`, plan §0/§3/§7). This module
NEVER writes to that file — it is read-only, exactly like every other
consumer of the working annual density series.

The CSV also carries an appended out-of-window summary block (years
outside [1600, 1784], marked with `#` comment lines and a differently
shaped table). Rows that are not parseable as `(year, spec_a_count)`
are skipped rather than raising, since they are structurally outside
the window this simulator ever needs.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np

SPEC_A_COLUMN = "cd_documents_all_accepted"
DEFAULT_WINDOW = (1600, 1784)
DEFAULT_CSV_PATH = Path(__file__).resolve().parents[1] / "CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv"


@dataclass(frozen=True)
class CdDensitySeries:
    years: np.ndarray
    counts: np.ndarray
    source_path: Path

    def as_dict(self) -> dict[int, int]:
        return dict(zip(self.years.tolist(), self.counts.tolist()))


def load_spec_a_density(
    csv_path: Path | str = DEFAULT_CSV_PATH,
    window: tuple[int, int] = DEFAULT_WINDOW,
) -> CdDensitySeries:
    """Read Spec A (`cd_documents_all_accepted`) annual counts, read-only.

    Rows outside [window[0], window[1]] are dropped. Rows that cannot be
    parsed as an integer year (e.g. the out-of-window summary's comment
    lines) are skipped, not treated as errors.
    """
    path = Path(csv_path)
    years: list[int] = []
    counts: list[int] = []
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if SPEC_A_COLUMN not in (reader.fieldnames or []):
            raise ValueError(f"{SPEC_A_COLUMN} column not found in {path}")
        for row in reader:
            raw_year = (row.get("year") or "").strip()
            try:
                year = int(raw_year)
            except ValueError:
                continue
            if window[0] <= year <= window[1]:
                raw_count = row.get(SPEC_A_COLUMN)
                if raw_count is None or raw_count == "":
                    raise ValueError(f"missing {SPEC_A_COLUMN} for year {year} in {path}")
                years.append(year)
                counts.append(int(raw_count))
    if not years:
        raise ValueError(f"no rows found in window {window} for {path}")
    order = np.argsort(years)
    years_arr = np.array(years)[order]
    expected = np.arange(window[0], window[1] + 1)
    if years_arr.tolist() != expected.tolist():
        missing = sorted(set(expected.tolist()) - set(years_arr.tolist()))
        raise ValueError(f"gap(s) in Spec A density within window {window}: missing years {missing}")
    return CdDensitySeries(years=years_arr, counts=np.array(counts)[order], source_path=path)


def log1p_transform(counts: np.ndarray) -> np.ndarray:
    """x_CD(t) = log(1 + CD_t) — plan §1.3 working transformation."""
    counts = np.asarray(counts, dtype=float)
    if np.any(counts < 0):
        raise ValueError("negative document counts are not valid")
    return np.log1p(counts)


def build_year_covariates(series: CdDensitySeries) -> dict[int, float]:
    """year -> x_CD(year) = log1p(CD_year), for exact per-year likelihood terms."""
    return dict(zip(series.years.tolist(), log1p_transform(series.counts).tolist()))


def build_x_cd_lookup(series: CdDensitySeries) -> Callable[[float], float]:
    """Piecewise-constant x_CD(t) = log1p(CD_year) for t in [year, year+1)."""
    year_covariates = build_year_covariates(series)
    year_min, year_max = int(series.years.min()), int(series.years.max())

    def x_cd(t: float) -> float:
        year = int(np.floor(t))
        year = min(max(year, year_min), year_max)
        return year_covariates[year]

    return x_cd
