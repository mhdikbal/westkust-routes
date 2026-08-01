# Human Classification Model

## Scope

The human model includes named individuals and aggregate groups. It does not invent individual identities for unnamed persons.

## Entity levels

### Named individual

A person explicitly named in the document, such as Benjamin Olitsch, Johan Pleijtner, Johan Hoffman, Johan Willem Vogel, or Elias Hesse.

### Aggregate group

A historically recorded group such as:

- `volwassen mansslaven`;
- `halfwasse cleene jongens`;
- `grasjongens`;
- `volwassen slavinnen`;
- children with or without `kostgelt`;
- the sixty-four enslaved persons recorded as arriving with the ship *Sillida* from Madagascar.

## Human state vector

For person or group `h` at time `t`:

```text
H_h(t) = [status, role, skill, growth_category, sex_category,
          health, location, schicht, task, supervision,
          mobility_constraint, evidence_confidence]
```

## Status categories

```text
VOC_employee
enslaved
convicted_coerced
local_worker
local_authority
dependent_child
unknown
```

These categories are analytical mappings. The original colonial category is always retained in `source_category_original`.

## Growth categories

```text
volwassen
volle
halfwasse
cleene_kinders
kinder_jongetjes
unknown
```

No numeric modern age is inferred from `halfwasse` or `volle` without external evidence.

## Food allowance

`kostgelt` is modelled as a historically recorded allowance attribute:

```text
receives_kostgelt
without_kostgelt
not_stated
```

It is not automatically interpreted as proof of total food provision.

## Aggregate integrity checks

Current reconciled groups include:

- male-group total: 150;
- female-and-children-group total: 94;
- combined total: 244;
- arrival classification total: 64.

## Required ethical metadata

Every coerced-labour record must include:

```text
source_category_original
status_category
evidence_status
ethical_note
individual_or_aggregate
```
