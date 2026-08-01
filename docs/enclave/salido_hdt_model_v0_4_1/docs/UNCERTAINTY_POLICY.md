# Uncertainty Policy

## Separate uncertainties

```text
reading_confidence
identity_confidence
relation_confidence
temporal_confidence
spatial_confidence
interpretation_confidence
```

## Evidence statuses

```text
explicit
normalized
interpreted
reconstructed
parallel_reading
uncertain
needs_image_review
rejected
```

## Evidence-status extensions in use (added v0.4, MIG-005)

The following compound values are already present in the v0.3/v0.4 data (`06_human_groups.csv`, `08_weekly_operations.csv`, `11_claims.csv`, `16_location_adjacency.csv`) but were not previously registered in the list above. They are refinements of the base vocabulary, not replacements — no existing CSV value was changed to add this section; it only documents usage that already existed.

```text
explicit_route             an explicitly stated route or movement between locations
                            (e.g. a documented voyage), as distinct from a static
                            containment/adjacency relationship.
explicit_or_structural      either explicitly stated in the source, or necessarily
                            entailed by the documented location hierarchy (e.g. a
                            facility's containment within its parent complex).
explicit_or_translated      explicitly stated in the source, accessed through the
                            translated text at this stage rather than independently
                            re-verified against the original-language wording.
interpreted_from_explicit_report
                            derived by interpretation from an explicitly stated
                            narrative report, rather than from a direct spatial or
                            relational statement.
strong_interpretation       a strong interpretive inference that goes beyond what is
                            directly stated, but stops short of a full model
                            reconstruction.
```

Do not normalize these to their nearest base-vocabulary term (e.g. collapsing `explicit_or_structural` to plain `explicit`) without an editorial record — doing so silently would discard a real distinction the original extraction made, which is exactly the kind of silent correction this policy prohibits below.

## Prohibited practice

- using absence of evidence as evidence of absence;
- silently correcting totals;
- assigning exact ages to historical growth categories;
- converting historical distance units without verified standards;
- merging marginalia into the main body without an editorial record;
- presenting the solver's best scenario as fact.

## Composite confidence

A conservative composite score may use:

```text
C = C_reading * C_identity * C_relation * C_temporal
```

The component scores must remain visible because a single scalar can hide the source of uncertainty.
