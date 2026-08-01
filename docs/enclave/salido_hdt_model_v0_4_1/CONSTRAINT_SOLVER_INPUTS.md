# Constraint Solver Inputs v0.2

## Files

- `14_task_requirements.csv`: tasks, required skills, preferred roles, tools, and allowed locations.
- `15_role_location_compatibility.csv`: evidence-weighted compatibility between roles and locations.
- `16_location_adjacency.csv`: spatial or topological relations.

## Semantics

`hard` values are grounded in explicit statements. `soft` values constrain reconstruction but may be violated with a penalty. `interpreted` and `uncertain` records must never be presented as archival facts.

## Initial objective

Minimize contradictions, unsupported assignments, temporal violations, topological violations, and over-assignment. The solver should return multiple equally valid scenarios when evidence is insufficient.

## Important limitation

The files do not assign unnamed enslaved persons to invented individual identities. Aggregate groups remain aggregate groups.
