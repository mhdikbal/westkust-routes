# Constraint Solver for Historical Reconstruction

## Objective

The solver seeks assignments that minimize contradiction with archival evidence. It does not optimize the extraction of labour.

## Recommended engine

Use CP-SAT for Boolean assignments and logical rules. Use MILP only where a linear continuous score is needed.

## Decision variable

```text
x[h,j,l,s,t] = 1
```

when human or group `h` performs task `j` at location `l`, in schicht `s`, during time `t`.

## Supporting variables

```text
y[e,j,l,t] equipment use
m[h,l1,l2,t] movement
q[h,t] health state
z[j,l,t] task activation
```

## Hard constraints

### Temporal presence

No assignment before arrival or after documented departure.

### Role compatibility

An assignment to assay requires an `Assaijeur` role unless the scenario explicitly tests a counterfactual.

### One location per schicht

```text
sum_l x[h,j,l,s,t] <= 1
```

### Equipment capacity

Simultaneous drilling teams cannot exceed available serviceable borers.

### Topological feasibility

Movement is allowed only through an adjacency or a deliberately marked unknown connection.

### Health exclusion

A person documented as released because of illness cannot be assigned afterwards without evidence of return.

## Soft constraints

- role-location compatibility;
- task continuity;
- preference for explicit over interpreted locations;
- avoidance of unsupported role switching;
- preference for serviceable equipment;
- minimum movement between periods.

## Objective function

```text
minimize:
  lambda1 * archival_contradictions
+ lambda2 * unsupported_assignments
+ lambda3 * temporal_violations
+ lambda4 * topological_violations
+ lambda5 * role_location_penalties
+ lambda6 * over_assignment
```

`lambda1` must dominate all other penalties.

## Multiple scenarios

Return all optimal or near-optimal scenarios within a declared tolerance. Do not collapse equally plausible histories into one answer.

## Input files

- `14_task_requirements.csv`
- `15_role_location_compatibility.csv`
- `16_location_adjacency.csv`
- `07_human_role_location_time.csv`
- `10_inventory_items.csv`
