"""Structured failure logging.

Plan §6 poin 5 / §5 poin 6: convergence and identification failures must
be reported explicitly, never hidden by only reporting replicates that
happened to converge. Every optimizer failure or invalid estimate
produced by `estimate.py` is appended here as a structured record rather
than silently dropped or overwritten.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class FailureRecord:
    scenario_id: str
    grid_point_id: str
    replicate_id: int
    reason: str
    detail: str = ""
    timestamp: float = field(default_factory=time.time)


class FailureLog:
    def __init__(self) -> None:
        self._records: list[FailureRecord] = []

    def log(self, scenario_id: str, grid_point_id: str, replicate_id: int, reason: str, detail: str = "") -> FailureRecord:
        record = FailureRecord(scenario_id, grid_point_id, replicate_id, reason, detail)
        self._records.append(record)
        return record

    @property
    def records(self) -> list[FailureRecord]:
        return list(self._records)

    def __len__(self) -> int:
        return len(self._records)

    def to_jsonl(self, path: Path | str) -> None:
        with Path(path).open("w", encoding="utf-8") as fh:
            for record in self._records:
                fh.write(json.dumps(asdict(record)) + "\n")
