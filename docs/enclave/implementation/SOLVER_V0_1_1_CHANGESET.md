# SALIDO-HDT Solver v0.1.1 — Changeset

Consolidated record of every fix and extension applied to the solver
(`src/salido_hdt/solver/`) since baseline commit `1cb16df`
("feat(salido-hdt): add validation-first historical reconstruction
solver"). This document exists because `cli.py`, `soft_constraints.py`,
and `scenario_collector.py` accumulated all of the work below as one
continuous, functionally-interdependent diff with no intermediate commit
boundary — F1 through F7 (from
`SOLVER_SCENARIO_INTERPRETATION_AUDIT.md` / `SOLVER_V0_1_1_FIX_PLAN.md`)
plus three further extensions (F8–F10) requested after those two documents
were written. Read alongside, not in place of, those two documents, which
this file does not rewrite or delete.

---

## F1 — Aggregate groups structurally erased via compounding penalty bugs

**Affected modules.** `soft_constraints.py`
(`add_task_continuity_penalty`, and the function originally named
`add_unsupported_role_switching_penalty`, since split — see F1-continuation
below), `cli.py` (wiring).

**Tests.** `tests/salido_hdt/solver/test_continuity_truth_table.py` (7
cases), `test_task_continuity_and_role_bias.py` (10 cases).

**Behaviour before.** `add_task_continuity_penalty` charged an idle↔idle
transition identically to a genuine task switch (no `active` state
existed). Combined with the original `add_unsupported_role_switching_
penalty` penalizing every aggregate-group assignment purely for absence
from `04_person_roles.csv` (a schema fact, not an evidentiary gap), every
one of the 10 real aggregate groups was pushed to zero assignments in
every scenario (objective ≈ 160, ≈ 16 per idle group over a 17-week
window), while 5 named Dutch officials were pushed to 100% occupancy —
verified reproducible via isolated 2-period models.

**Behaviour after.** `add_task_continuity_penalty` rewritten with explicit
`active_t`/`active_t1` reification: idle↔idle, idle↔active, and
active↔idle now cost nothing; only a genuine active→different-active
transition is charged. `test_group_idle_vs_assigned_are_cost_equal_on_
real_presence_window` proves idle and assigned now cost identically for
`G-MS-121`'s real 17-week window — bias removed without introducing the
opposite bias (no test anywhere asserts a group must be assigned).

---

## F1-continuation — `add_unsupported_role_switching_penalty` split into two correctly-named, correctly-scoped functions

**Affected modules.** `soft_constraints.py` (new `add_role_task_support_
penalty`, new `add_role_switch_penalty`, replacing the old single
function), `cli.py` (`_group_declared_roles`, rewired penalty terms).

**Tests.** `tests/salido_hdt/solver/test_role_task_support_and_switch.py`
(23 cases covering all 5 required distinction cases).

**Behaviour before.** One function, despite being named "switching," never
compared time periods at all — it penalized any single-assignment
documentation gap, and blanket-exempted every aggregate group (v0.1.1's
first-pass fix), which was itself an over-correction: a genuinely
undocumented group and a group with its own textually-verified supervisory
function (`G-MANDOOR-8`'s category `'mandoors'` → role `R-MANDOOR`,
verified, not invented) were treated identically.

**Behaviour after.** `add_role_task_support_penalty` (single-assignment,
no time dimension) classifies every role-declaring assignment as
`SUPPORTED` / `undocumented` / `contradicted`, checking two evidence
sources in order: `person_roles` (named individuals) then
`_group_declared_roles` (groups whose own category names a real role — 3
of 17 real groups: `G-MANDOOR-8`, `G-MANDORESS-3`, `G-VOORSLAGER-1`).
`add_role_switch_penalty` (genuinely across-time) penalizes only when an
entity's task assignments at `t`/`t+1` require disjoint roles — it never
consults `person_roles`/group identity, so it cannot reintroduce bias
against groups.

---

## F2 — Entity exclusion from CP-SAT variables was invisible in output

**Affected modules.** `cli.py` (`_entity_coverage`).

**Tests.** `tests/salido_hdt/solver/test_cli_pipeline.py` (3 cases).

**Behaviour before.** 42 of 47 role-documented individuals had zero CP-SAT
variables (no HARD-eligible HRLT presence row) with no trace of this in
any output artifact.

**Behaviour after.** `validation_summary.json`'s `entity_coverage` array
lists every known person/group with `has_hard_role`, `has_hard_presence`,
`included_in_variables` — e.g. `P-BRETSNIJDER` now visibly shows
`has_hard_role=True, has_hard_presence=False`.

---

## F3 — Equipment capacity: declared-not-enforced → enforced

**Affected modules.** `equipment_capacity.py` (new), `cli.py` (wiring,
`add_equipment_capacity` calls).

**Tests.** `tests/salido_hdt/solver/test_equipment_capacity_cli_wiring.py`
(22 cases, including the 4 explicitly mandatory ones: 7-vs-8 simultaneous
teams, unserviceable→zero hard capacity, real parent/child no-double-count
via `INV-0333`, and an identity check that `cli.py` and the unit tests
call the literal same `hard_constraints.add_equipment_capacity` function
object).

**Behaviour before (this changeset's starting point).** The function
existed and was unit-tested but never called from `run()` — declared as a
known, explicit gap (`equipment_capacity_enforced: false`).

**Behaviour after.** `compute_capacity_reports()` matches
`14_task_requirements.csv`'s `required_tool_keywords` against
`10_inventory_items.csv` (category/item_text_id/source_translation_full,
case-insensitive substring), scoped to each task's `allowed_location_ids`,
restricted to `unit_normalized == 'stux'` (piece-count) rows, with
`row_type == 'container_or_parent'` rows always excluded (their children
already itemize the total — verified against `INV-0333` = 6 cannons,
children `INV-0334`(2) + `INV-0335`(4) = 6). Confirmed vs. uncertain
follows the exact rules requested: serviceable/new → confirmed;
empty/compound/other condition → uncertain; unserviceable → zero
(excluded from both pools); `reading_status == 'unresolved'` → always
uncertain regardless of condition. **Verified on the real dataset: 7
equipment-capacity constraints instantiated** (of 45 (task, location)
pairs checked — most are `NO_INVENTORY_MATCH`, a real vocabulary gap
between Dutch tool keywords and Indonesian-translated inventory text, see
"Remaining incomplete" below). The wired HARD bound is
`confirmed + uncertain` (never confirmed alone — real condition data is
unknown for 369 of 403 rows, so confirmed-only would hard-forbid tasks the
archive does not actually forbid). `equipment_capacity.csv` reports
`confirmed_capacity, uncertain_capacity, required_capacity,
capacity_status, source_inventory_item_ids` for every (task, location)
pair, matched or not.

---

## F4 / F9 — Role-task hard gate now respects constraint_strength, parsed atomically (not free-text)

**Affected modules.** `constraint_strength.py` (new),
`cli.py` (`_hard_task_preferred_roles`, `_task_preferred_roles`,
`_blocked_constraint_strength_tasks`).

**Tests.** `tests/salido_hdt/solver/test_constraint_strength.py` (19
cases, all 8 controlled tokens + blocked_unknown + not_applicable
overrides), `test_assignment_schema.py` (4 constraint_strength-wiring
cases).

**Behaviour before (F4, original fix).** `_hard_task_preferred_roles`
called `validation.classify_hard_soft()`, which used a raw
`constraint_strength.startswith("hard")` string comparison.

**Behaviour after (F9, this changeset).** `constraint_strength.py`
implements the authoritative, explicitly-reviewed per-axis table for all 8
controlled tokens (`hard`, `soft`, `hard_role`, `hard_location`,
`hard_for_assay`, `hard_location_soft_staffing`, `hard_role_soft_tools`,
`hard_role_soft_location`), decomposed into four INDEPENDENT atomic axes
(`role_constraint_type`, `location_constraint_type`,
`equipment_constraint_type`, `staffing_constraint_type`) each valued
`hard`/`soft`/`unspecified`/`not_applicable`/`blocked_unknown`. The base
token is never propagated to an axis it does not explicitly name (e.g.
`hard_for_assay` resolves all four axes to `unspecified` plus
`scope="assay", parse_status="legacy_ambiguous"` metadata). Structural
`not_applicable` (task has no `required_tool_keywords`/etc.) overrides the
token table. Any string outside the controlled 8 is `blocked_unknown` on
all four axes and is excluded from both the hard role-task gate and the
soft role-support signal — never silently treated as either.
`_hard_task_preferred_roles` now checks
`role_constraint_type == AxisValue.HARD` directly. **Verified: 0 of the
real dataset's 18 task rows are blocked** (all 7 distinct real
`constraint_strength` values are among the 8 controlled tokens).

---

## F5 / F10 — Evidence citations → full per-assignment provenance schema

**Affected modules.** `cli.py` (`_presence_records_for`, `_citations_for`,
`_assignment_evidence`).

**Tests.** `tests/salido_hdt/solver/test_assignment_schema.py` (11
cases).

**Behaviour before (F5, original fix).** Each `active_assignments` entry
carried `presence_hrlt_ids` only.

**Behaviour after (F10, this changeset).** Every assignment now carries
the full requested schema: `scenario_id, entity_id, entity_type, task_id,
location_id, schicht_id, time_bucket, assignment_state, evidence_status,
source_document_id, source_passage_id, evidence_quote, constraint_ids,
supporting_inventory_item_ids, supporting_role_ids, provenance_precision,
reconstruction_warning`. Since every solver assignment is a combinatorial
reconstruction (no archival record ever states "entity h performed task j
at location l at time t" directly), `assignment_state` is always
`"solver_reconstructed"`, `evidence_status` is always `"reconstructed"`,
and `reconstruction_warning` is always `"not an archival statement"` —
fixed constants, verified by
`test_assignment_evidence_reconstruction_warning_is_always_present_and_
fixed`. `provenance_precision` reuses `domain.ProvenanceLevel`
(`claim_level`/`section_level`/`document_level`/`missing`/`ambiguous`),
computed via `validation.classify_provenance()` on the actual backing
HRLT record. `evidence_quote`/`source_document_id`/`source_passage_id`
trace to that record's own fields (e.g. `HRLT-0003` for `P-HESSE`).

---

## F6 — Run metadata (schicht/time-bucket documentation)

**Affected modules.** `cli.py` (`_RUN_METADATA_NOTE`, `run_metadata` in
`validation_summary.json`).

**Status.** Unchanged since its original implementation in this
changeset's parent turn — `schicht_count`, `time_bucket_width_days`, and
an explanatory note are present in every run's `validation_summary.json`.
Not modified or extended further in this changeset.

---

## F7 — Per-category penalty breakdown

**Affected modules.** `scenario_collector.py` (`Scenario.penalty_
breakdown`, `collect_scenarios(penalty_terms=...)`), `cli.py` (six
objective categories plus diagnostic-only `task_switch`, `location_switch`,
`role_switch`, `role_undocumented`, `role_contradicted` keys).

**Status.** Unchanged in mechanism since its original implementation;
`cli.py`'s `penalty_terms` dict was extended (this changeset) to include
the new `role_switch`/`role_undocumented`/`role_contradicted` diagnostic
keys alongside the original `task_switch`/`location_switch`, but the
`Scenario`/`collect_scenarios` mechanism itself is unmodified.

---

## F8 — Named-person candidate-universe construction (new)

**Affected modules.** `candidate_universe.py` (new), `cli.py` (wiring:
`entity_presence.csv`, `candidate_entities.csv`, `excluded_entities.csv`).

**Tests.** `tests/salido_hdt/solver/test_candidate_universe.py` (13
cases).

**Behaviour before.** A named person lacking an HRLT presence row (42 of
47 role-documented individuals) had no representation distinguishing
"the archive is silent about this person's presence here" from "this
person has other, coarser presence evidence."

**Behaviour after.** Register presence is derived from the real, dated
personnel register (`DOC-PERSONNEL-1682-01-09`, "Lijste van Compagnies
dienaren en lijfeijgenen") via `04_person_roles.csv` rows citing a
`document_type == 'personnel_register'` document — fixed fields
`presence_scope=enclave, location_precision=enclave_level, task=unknown,
evidence_status=explicit, derivation_status=register_presence`, never
widened beyond the document's own date, and independent of the
accompanying role claim's own evidence status (verified: `P-STREIJT`'s
role is `interpreted`/0.65 confidence but their register presence is
still `explicit`). Five states
(`documented_present`/`eligible_for_assignment`/`assigned`/
`present_but_unassigned`/`excluded_with_reason`) classify every one of the
51 named persons exactly once, written to three CSVs. **Explicit scope
decision, unchanged in this changeset: register presence is
reporting-only — it does NOT add CP-SAT x-variables.** Wiring it into
`variables.py`'s variable construction (a new location granularity, a new
HARD-eligibility rule) was explicitly deferred to a future task.

---

## Cross-cutting verification (this changeset)

1. Full test suite: **161/161 passed**.
2. Real `cli.run()` execution in a temporary directory: succeeded,
   produced `entity_presence.csv`, `candidate_entities.csv`,
   `excluded_entities.csv`, `equipment_capacity.csv`, `scenario_00.json`,
   `validation_summary.json`.
3. **Equipment-capacity constraints instantiated: 7** (confirmed via
   `validation_summary.json`'s `equipment_capacity_constraints_
   instantiated` field on a fresh run).
4. **Blocked constraint-strength records: 0** (confirmed via
   `validation_summary.json`'s `blocked_constraint_strength_tasks`, empty
   list, on a fresh run against the real v0.4.1 dataset).
5. Temporary CLI output directory deleted after inspection.
6. SHA-256 / `git status` re-verified: `salido_hdt_model_v0_3/`,
   `salido_hdt_model_v0_4/`, `salido_hdt_model_v0_4_1/` all show zero diff
   against their prior state (`v0_3`/`v0_4` remain untracked-and-untouched
   pre-existing state; `v0_4_1` — the canonical solver input — is
   byte-identical to its last commit).

## Remaining incomplete findings (explicitly not addressed by this changeset)

- **Equipment-capacity vocabulary gap.** Most (task, location) pairs
  (32 of 45) resolve to `NO_INVENTORY_MATCH` because
  `14_task_requirements.csv`'s tool keywords are archaic Dutch
  (`'boor'`) while `10_inventory_items.csv`'s descriptions are
  Indonesian translations (`'bor tambang'`) — a real terminological
  mismatch, not a bug in the matcher. No fuzzy/translation logic was
  added; the gap is reported (`NO_INVENTORY_MATCH`), not papered over.
- **`hard_for_assay`'s `scope`/`parse_status` metadata is captured but not
  acted on** by any downstream constraint — no task in the real dataset
  currently uses this token, so this is untested against live behaviour
  beyond the parser itself.
- **`constraint_ids` in the assignment schema currently only includes
  presence-backing HRLT ids**, not role/location-compatibility rule ids or
  equipment-capacity constraint identifiers, which also bear on an
  assignment's legality. Documented simplification, not implemented this
  changeset.
- **Register presence (F8) is not wired into CP-SAT variable
  construction** — an explicit, previously-confirmed scope decision, not
  an oversight, but still an incomplete extension relative to what a full
  "no person disappears" guarantee would eventually require.
- **`presence_transition` penalty remains implemented but disabled by
  default** (`include_presence_transition_penalty=False` in `cli.run()`'s
  call) — enabling it by default would reintroduce F1-style idle-vs-
  assigned pressure; left as an opt-in mechanism for a future,
  deliberately-scoped use.

## Confirmation: scenario v0.1 outputs remain invalidated

Nothing in this changeset retroactively validates any `scenario_*.json`
produced before these fixes. `SOLVER_SCENARIO_INTERPRETATION_AUDIT.md`'s
verdict stands unchanged: v0.1 output must not be read, quoted, or
presented as an archival reconstruction. Re-running the fixed pipeline
today still produces an all-idle optimum (objective 0) on the real
dataset — nothing in the current wiring rewards any assignment, which is
the correct, bias-free expression of "the archive alone gives the solver
no basis to assert a specific reconstruction," not a new defect.

## Confirmation: canonical datasets unmodified

`docs/enclave/salido_hdt_model_v0_3/`, `salido_hdt_model_v0_4/`, and
`salido_hdt_model_v0_4_1/` were re-verified unchanged immediately before
this document was written (see "Cross-cutting verification" §6 above).
