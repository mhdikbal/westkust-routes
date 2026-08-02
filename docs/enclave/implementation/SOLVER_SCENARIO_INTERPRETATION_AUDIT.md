# SALIDO-HDT Solver — Scenario Interpretation Audit

Status: read-only audit. No canonical dataset file and no solver source file
was modified to produce this report. All findings below were reproduced
against the real `docs/enclave/salido_hdt_model_v0_4_1/` dataset via a fresh
`python -m salido_hdt.solver.cli --scenarios 3 --output <scratch dir>` run
(commit `1cb16df`) plus targeted, isolated reproductions of the CP-SAT
sub-models responsible for each finding. Scratch output was deleted after
inspection; nothing under `docs/enclave/` was written to.

## 1. Purpose

The solver committed in `1cb16df` passes all 51 tests and its own
`test_no_source_mutation.py` guard. Passing tests establish that the code
does what its authors intended it to do; they do not establish that a
downstream reader can safely interpret what it *produces*. This audit asks
the second question: if someone opens `scenario_00.json` today, what could
they wrongly conclude, and why?

## 2. What a scenario is, and is not

A `scenario_NN.json` emitted by `cli.run()` is: one feasible assignment of
`x[h,j,l,s,t]` variables that (a) satisfies every HARD constraint built from
`validation.py`'s re-derived provenance classification, and (b) minimizes
(or comes within `SCENARIO_OBJECTIVE_TOLERANCE` of minimizing) a
`lambda`-weighted sum of six penalty terms whose mapping to
`CONSTRAINT_SOLVER.md`'s named categories is itself an **interpretive
choice made in this implementation** (documented in `objective.py`'s
docstring), not a literal transcription of the source document's objective.

It is **not**: a historical claim, a probability-weighted reconstruction, or
evidence that an entity did or did not do something. `active_assignments`
entries carry no citation back to the record that licensed them (§4, F5) —
an entry's presence in a scenario means only "this combination survived the
solver's HARD filter and happened to be cheap under this run's soft-penalty
arithmetic," nothing more.

## 3. Real output examined

Three scenarios generated (`--scenarios 3`, defaults otherwise):

| scenario | status | objective | entities with any assignment | assignments |
|---|---|---|---|---|
| 0 | OPTIMAL | 160 | 5 | 90 |
| 1 | OPTIMAL | 161 | 5 | 89 |
| 2 | OPTIMAL | 161 | 5 | 89 |

`validation_summary.json`: 536 records validated, 498 hard-eligible, 57
entities have at least one CP-SAT variable, 4,680 `x` variables total, 18
weekly time buckets.

The same 5 entities appear in **all three** scenarios, every time:
`P-HESSE`, `P-HOFFMAN`, `P-PLEIJTNER`, `P-ROELINGH`, `P-VOGEL` — each
assigned to exactly one task, held constant across all 18 time buckets
(18 assignments × 5 = 90). The other 52 entities, including **all 10
aggregate labor groups**, receive zero assignments in every scenario.

## 4. Findings

### F1 — CRITICAL: aggregate coerced-labor groups are structurally erased from every optimal scenario, and it is a formulation bug, not an evidentiary finding

The 10 aggregate groups in `07_human_role_location_time.csv`
(`G-MS-121` = 121 mine-slaves, `G-SLAVIN-68` = 68 enslaved women,
`G-MANDOOR-8`, `G-CHILD-KOST-4`, `G-CHILD-NOKOST-19`, etc. — collectively
well over 200 people) all have HARD-eligible presence (verified: all 10 pass
`hard_eligible_presence()`, each getting 306 `x`-variables spanning weeks
1–17 at `L-BENEDEN-PAGGER`). Verified directly, ignoring the objective, that
a group **can** legally hold one consistent task across the full 17-week
window (`Maximize(sum(G-MS-121 vars))` returns 17/17 feasible). Yet in the
actual minimization every group is assigned **zero** tasks, in all three
scenarios, while the objective is dominated by exactly this: 160 ≈
10 groups × 16 (see below).

Two formulation choices compound to cause this:

1. **`soft_constraints.add_task_continuity_penalty` treats "idle at both t
   and t+1" as a task switch.** The function builds a `switch` BoolVar for
   every consecutive `(h, t), (h, t+1)` pair *for which any x-variable
   exists*, regardless of whether any of those variables are true. Isolated
   reproduction (2 periods, `add_one_location_per_schicht` + continuity
   penalty only): forcing an entity fully idle across both periods costs
   **1**; assigning the same task in both periods costs **0**. Over a
   16-consecutive-pair window (17 buckets), full idleness costs **16** —
   which is exactly the per-group cost that sums to the observed
   objective of 160/161. Idleness is not a "switch"; the function has no
   idle/idle case, so CP-SAT is forced to pay a penalty for doing nothing.

2. **`soft_constraints.add_unsupported_role_switching_penalty` fires for
   every assignment of a role-undocumented entity to a role-declaring
   task.** All 18 rows of `14_task_requirements.csv` declare at least one
   `preferred_role_ids` entry — there is no role-free task to fall back on.
   Aggregate groups never appear in `04_person_roles.csv` (that table only
   covers named individuals by schema), so `person_roles.get(group_id)` is
   always `None`: any task assignment for a group costs 1 penalty point per
   period, for the group's entire presence window. 17 periods of
   role-unsupported penalty (≈17) is *worse* than 16 periods of the
   idle-miscount bug — so the minimizer picks idleness, by a margin of
   exactly one arithmetic unit.

The five entities that *do* get assigned are precisely the five named
individuals who both (a) have a HARD-eligible presence window and (b) hold
a matching HARD-documented role in `04_person_roles.csv` for the task they
end up on (`P-HESSE`→`R-BERGHSCHRIJVER`/`T-RECORD`,
`P-HOFFMAN`/`P-ROELINGH`/`P-VOGEL`→`R-ASSAIJEUR`/`T-ASSAY`,
`P-PLEIJTNER`→`R-MARKSCHEIDER`/`T-INSPECT-MINE`) — all European mine
officials (assayers, surveyor, clerk). For them, assignment costs 0 (no
role penalty, since they hold the role) and idleness would cost 16 — so the
same arithmetic pushes them the *opposite* direction.

**Risk.** A reader of `scenario_00.json` alone, without this audit, could
conclude "the archival reconstruction shows the enslaved/coerced labor
groups performing no work while the Dutch specialists did the mine labor" —
a direct inversion of both the historical reality the dataset describes and
the intent of `ETHICAL_MODELING.md` and the aggregate-group modeling
apparatus this whole solver was built to support without erasing. The
erasure is 100% attributable to the two penalty-formulation choices above,
not to any absence or weakness of archival evidence about the groups
themselves (their presence evidence is exactly as strong, HARD-classified,
as the officials').

**Recommendation.** Before any scenario output is read, quoted, or
presented as illustrative of the archive: fix `add_task_continuity_penalty`
so an idle→idle transition is not counted as a switch (e.g., only build the
`switch` var when at least one of the two periods has a legal non-idle
option that was structurally intended to be compared, or explicitly zero
the term when both periods' variable sets are all-idle-eligible). Separately,
decide and document explicitly whether `add_unsupported_role_switching_penalty`
should apply to aggregate groups at all, given their absence from `04` is a
*schema* fact (groups are never rows in that table), not an *evidentiary*
one — the current code treats structural absence as if it were an
evidentiary gap, which is exactly the conflation `UNCERTAIN_POLICY.md`
prohibits for the CSVs themselves and should not be reintroduced silently
in the objective.

### F2 — HIGH: 42 of 47 role-documented individuals cannot appear in any scenario, for reasons invisible from the JSON output

`hard_eligible_person_roles()` finds 47 person IDs with a HARD-classified
role in `04_person_roles.csv`. `hard_eligible_presence()` finds only 15
entities total with a HARD-eligible presence window (10 groups + 5
individuals — precisely the five from F1). `variables.build_variables()`
only constructs `x`-variables for an entity if it has an attested presence
window (`if not attested: continue`); an entity with a documented role but
no HARD-eligible presence gets **no CP-SAT variables at all**. Its absence
from every scenario is therefore not a solver "decision" and carries no
evidentiary weight either way — it is a scope boundary of this run, silent
in the output.

**Risk.** A reader must not treat an entity's absence from `scenario_NN.json`
as "no evidence this person worked at this site" — 89% of role-documented
individuals are excluded purely because their location/time evidence didn't
clear the HARD provenance bar, independent of how strong their role
evidence is.

**Recommendation.** `validation_summary.json` should enumerate excluded
entities and the specific reason (`no_hard_presence`, `no_hard_role`, etc.),
not just aggregate counts, so this boundary is visible without reading
`variables.py`.

### F3 — MEDIUM: equipment_capacity is implemented and tested but never wired into `cli.run()`

`hard_constraints.add_equipment_capacity()` (the `INV-0232` / borer-capacity
mechanism documented in `SOLVER_INPUT_READINESS.md` §8–9, with its
widened-bound rule for `reading_status=unresolved`) is exercised only by
`test_equipment_capacity.py`'s synthetic fixtures. `cli.py`'s `run()` never
calls it — wiring it requires resolving which specific inventory rows cap
which specific `(task_id, location_id)` pairs, a mapping this codebase does
not currently derive automatically (deliberately, to avoid inventing a
linkage the CSVs don't state). Currently moot in practice (F1 means no
drilling task is ever chosen), but it means nothing in the live pipeline
would catch a future scenario proposing more simultaneous drilling
assignments than the archive's own equipment count supports.

**Recommendation.** Either derive the task/location/inventory linkage
explicitly (documented, not inferred) and wire it in, or record this gap in
`README.md`/`cli.py`'s own docstring as a known non-enforced hard
constraint, so a future scenario reader isn't relying on a capacity check
that silently isn't running.

### F4 — MEDIUM: role-task compatibility ignores `TaskRequirement.constraint_strength`

`cli._task_preferred_roles()` builds `{task_id: set(preferred_role_ids)}`
from every row of `14_task_requirements.csv` unconditionally, and
`add_role_task_compatibility` then enforces it as a HARD exclusion. This
happens regardless of whether that specific task-requirement row itself
classifies as HARD or SOFT under `validation.classify_hard_soft()` (which
does inspect `TaskRequirement.constraint_strength` when called on `14`
rows directly, but `cli.py` never routes task-requirement rows through that
classifier before using `preferred_role_ids`). A task whose own evidentiary
basis is `constraint_strength="soft"`/interpreted still hard-forbids every
role-undocumented entity from it.

**Recommendation.** Either gate `_task_preferred_roles()` by
`classify_hard_soft(task_requirement, ...)` the same way locations and
adjacency edges already are, or add an explicit code comment stating why
task-role preference is treated as always-authoritative regardless of the
row's own strength label — right now it is an undocumented omission, not a
recorded decision like the other five interpretive choices in
`objective.py`.

### F5 — MEDIUM: scenario JSON carries no evidence citation per assignment

Each `active_assignments` entry is
`{human_or_group_id, task_id, location_id, schicht, time_bucket}` — no
`hrlt_id`, `person_role_id`, `evidence_status`, or `source_passage_id`. This
breaks the citation-traceability discipline the v0.3→v0.4→v0.4.1 lineage
was built around the moment output leaves the pipeline: a reader cannot
tell, from the JSON alone, which archival record licensed a given
assignment's presence window without re-running `validation.py` by hand.

**Recommendation.** Attach the `hrlt_id` (and, where applicable,
`person_role_id`) that supplied the presence window backing each assignment
to its JSON entry.

### F6 — LOW: `schicht` is always 0; scenario diversity is task-choice-only

`DEFAULT_SCHICHT_COUNT=1` (documented, `config.py`). Every emitted
assignment has `schicht: 0`. The three scenarios examined never differ in
location or time window for a given entity — only in which task an already
HARD-attested (entity, location, time) combination is assigned to. A reader
comparing scenarios should not expect them to represent alternate
presence/location histories; presence and location are resolved before
variable construction (`variables.py`'s pruning design) and are identical
across every scenario by construction.

### F7 — LOW / documentation: no per-category penalty breakdown in output

`objective.py`'s own docstring states `temporal_violations` and
`topological_violations` are structurally always zero in this
implementation (enforced as HARD exclusions, never soft penalties) —
confirmed true in the real run. But `scenario_NN.json`/
`validation_summary.json` expose only the single scalar `objective_value`;
a reader cannot see the six-term breakdown (which, per F1, would have
immediately surfaced the idle-penalty dominance) without reading
`cli.py`'s source and re-deriving it themselves.

**Recommendation.** Have `run()` capture and emit the six penalty-term
subtotals (`sum(archival_contradictions)`, etc.) alongside
`objective_value` in `validation_summary.json`. Cheap, non-invasive, and
would have made F1 visible from the output alone.

## 5. Overall verdict

The pipeline mechanics audited previously (immutability, provenance
re-derivation, ethical structural guard on variable construction,
read-only I/O) all hold and are correctly enforced — this audit found no
issue with those. But **the specific content of every scenario JSON
produced by the current `cli.run()` must not be read, quoted, or presented
as an archival reconstruction.** The near-total absence of aggregate labor
groups from every scenario (F1) is a solver-formulation artifact traceable
to two specific, fixable penalty-function bugs, not a reflection of the
underlying evidence, and reads in a direction that is the exact opposite of
what `ETHICAL_MODELING.md` and this project's aggregate-group discipline
were built to prevent. F1 should be treated as a blocking issue for any use
of solver output beyond further internal testing.

No code was changed as part of this audit. Recommend a follow-up
implementation task, scoped narrowly to F1 (at minimum), before generating
any scenario output intended for review outside this pipeline's own test
suite.
