"""Read-only parser for the five Model 3B V2 specification files.

Contract: values, labels, formulas, placeholders, and statuses are returned
exactly as written in the source file. No silent defaults are substituted
for missing fields, and no unrecognized enum value is coerced to a known
one -- both cases raise SpecParseError.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

GATE_SPEC_COLUMNS = [
    "gate_id", "version", "candidate", "model_equation_id", "parameter_space",
    "estimand", "null_definition", "applicability", "mandatory_advisory_status",
    "metric_name", "metric_formula", "denominator", "threshold",
    "threshold_status", "threshold_provenance", "failure_meaning",
    "source_original_gate", "source_amendment", "implementation_status", "notes",
]

APPLICABILITY_MATRIX_COLUMNS = [
    "candidate", "gate_id", "gate_family", "model_equation_id", "parameter_space",
    "estimand", "applicability", "mathematical_reason", "mandatory_advisory_status",
    "source_decision", "implementation_status", "notes",
]

LEDGER_COLUMNS = [
    "decision_id", "topic", "candidate", "mathematical_quantity", "options",
    "recommended_next_evidence", "current_status", "researcher_decision",
    "implementation_blocking", "execution_blocking", "historical_fit_blocking",
    "source_amendment", "notes",
]

LEDGER_STATUS_ENUM = {"APPROVED_WITH_LIMITATIONS", "DEFERRED", "PENDING_RESEARCHER_DECISION"}


class SpecParseError(ValueError):
    """Raised when a source file is missing a required field or contains
    a value outside the recognized contract. Never silently defaulted."""


@dataclass(frozen=True)
class CsvDocument:
    path: Path
    columns: list
    rows: list  # list[dict[str, str]], values verbatim from source


@dataclass(frozen=True)
class MarkdownDocument:
    path: Path
    text: str
    section_headings: list = field(default_factory=list)
    placeholder_tokens: list = field(default_factory=list)


def _read_csv_rows(path: Path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)
    return header, rows


def _require_no_blank_fields(path: Path, rows, required_columns):
    for i, row in enumerate(rows):
        for col in required_columns:
            val = row.get(col)
            if val is None or val.strip() == "":
                raise SpecParseError(
                    f"{path.name}: row {i} missing required field '{col}' "
                    "(blank field is not a valid placeholder -- use an "
                    "explicit decision-linked token instead)"
                )


def parse_gate_spec_v2(path: Path) -> CsvDocument:
    header, rows = _read_csv_rows(path)
    if header != GATE_SPEC_COLUMNS:
        raise SpecParseError(
            f"{path.name}: column set/order does not match the frozen "
            f"20-column gate spec contract.\nexpected={GATE_SPEC_COLUMNS}\n"
            f"found={header}"
        )
    _require_no_blank_fields(path, rows, [c for c in GATE_SPEC_COLUMNS if c != "notes"])
    return CsvDocument(path=path, columns=header, rows=rows)


def parse_applicability_matrix(path: Path) -> CsvDocument:
    header, rows = _read_csv_rows(path)
    if header != APPLICABILITY_MATRIX_COLUMNS:
        raise SpecParseError(
            f"{path.name}: column set/order does not match the frozen "
            f"12-column applicability matrix contract.\nexpected="
            f"{APPLICABILITY_MATRIX_COLUMNS}\nfound={header}"
        )
    # 'notes' is supplementary annotation, legitimately blank on some rows
    # (verified against the frozen 2572c19 baseline: 10/62 rows have no
    # note). Every other column remains required.
    _require_no_blank_fields(path, rows, [c for c in APPLICABILITY_MATRIX_COLUMNS if c != "notes"])
    return CsvDocument(path=path, columns=header, rows=rows)


def parse_ledger(path: Path) -> CsvDocument:
    header, rows = _read_csv_rows(path)
    if header != LEDGER_COLUMNS:
        raise SpecParseError(
            f"{path.name}: column set/order does not match the frozen "
            f"13-column ledger contract.\nexpected={LEDGER_COLUMNS}\n"
            f"found={header}"
        )
    for i, row in enumerate(rows):
        status = row.get("current_status", "")
        if status not in LEDGER_STATUS_ENUM:
            raise SpecParseError(
                f"{path.name}: row {i} (decision_id={row.get('decision_id')!r}) "
                f"has unrecognized current_status {status!r}; expected one of "
                f"{sorted(LEDGER_STATUS_ENUM)}"
            )
    _require_no_blank_fields(path, rows, LEDGER_COLUMNS)
    return CsvDocument(path=path, columns=header, rows=rows)


_PLACEHOLDER_TOKEN_RE = re.compile(
    r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+){2,}\b"
)
_SECTION_HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def parse_markdown_spec(path: Path) -> MarkdownDocument:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise SpecParseError(f"{path.name}: file is empty")
    headings = _SECTION_HEADING_RE.findall(text)
    tokens = sorted(set(_PLACEHOLDER_TOKEN_RE.findall(text)))
    return MarkdownDocument(
        path=path, text=text, section_headings=headings, placeholder_tokens=tokens
    )


@dataclass(frozen=True)
class V2SpecificationSet:
    mathematical_spec: MarkdownDocument
    gate_spec: CsvDocument
    protocol: MarkdownDocument
    applicability_matrix: CsvDocument
    ledger: CsvDocument


def parse_v2_specification_set(pilot_annotation_dir: Path) -> V2SpecificationSet:
    """Parse all five frozen V2 specification files. Raises SpecParseError
    on the first structural or enum violation found -- never proceeds with
    a partially-valid document."""
    d = Path(pilot_annotation_dir)
    return V2SpecificationSet(
        mathematical_spec=parse_markdown_spec(d / "MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md"),
        gate_spec=parse_gate_spec_v2(d / "MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv"),
        protocol=parse_markdown_spec(d / "MODEL_3B_RECOVERY_PROTOCOL_V2.md"),
        applicability_matrix=parse_applicability_matrix(d / "MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv"),
        ledger=parse_ledger(d / "MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv"),
    )
