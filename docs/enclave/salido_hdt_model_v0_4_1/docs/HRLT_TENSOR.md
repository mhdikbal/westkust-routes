# Human–Role–Location–Time Tensor

## Definition

The conceptual tensor is:

```text
X in [0,1]^(N_H x N_R x N_L x N_T)
```

`X[h,r,l,t]` represents evidential support that human entity `h` carried role `r` at location `l` during time `t`.

## Sparse implementation

The tensor is stored as `07_human_role_location_time.csv` rather than as a dense array.

Required coordinates:

```text
human_or_group_id
role_id
location_id
valid_from
valid_to
```

Required epistemic fields:

```text
assignment_value
evidence_status
confidence
source_quote
source_document_id
review_status
```

## Interpretation of values

```text
1.00 explicit statement
0.80–0.99 strong normalization or identification
0.60–0.79 strong interpretation
0.40–0.59 plausible reconstruction
0.01–0.39 weak hypothesis
0.00 contradicted or explicitly unavailable
NULL unknown
```

`0` and `NULL` are not interchangeable.

## Group tensor

Aggregate groups occupy a tensor coordinate without being expanded into fictional people. A count is stored separately.

## Time intervals

Use event-indexed intervals rather than creating one row per day. Open-ended intervals remain empty in `valid_to`.

## Companion tensors

```text
Skill[h,k,t]
Activity[h,j,l,t]
Health[h,t]
Equipment[e,l,t]
Material[m,l,t]
Supervision[h1,h2,t]
```
