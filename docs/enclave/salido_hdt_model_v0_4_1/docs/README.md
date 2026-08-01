# SALIDO-HDT Model Documentation v0.3

## Purpose

This documentation defines the evidence-centred data and mathematical model for reconstructing the Salido or Sillida mining enclave in 1681–1682. The working source is `enklave-salido.docx`, associated in the research file with Nationaal Archief, Den Haag, access `1.04.02`, inventory `7964`.

The package currently contains:

- 50 named persons;
- 22 role definitions;
- 23 locations and facilities;
- 17 aggregate human groups;
- 15 seed Human–Role–Location–Time records;
- 42 weekly operation-location records;
- 19 assay observations;
- 403 line-level inventory records;
- 18 solver task definitions;
- 31 role-location compatibility rules;
- 22 location relations.

## Modelling principle

The system separates:

1. archival statement;
2. diplomatic or source-preserving reading;
3. normalized reading;
4. Indonesian translation;
5. technical interpretation;
6. mathematical reconstruction.

A reconstruction must never overwrite the archival statement.

## Documentation map

- `DATA_DICTIONARY.md`
- `HUMAN_CLASSIFICATION.md`
- `ROLE_TAXONOMY.md`
- `LOCATION_ONTOLOGY.md`
- `HRLT_TENSOR.md`
- `CONSTRAINT_SOLVER.md`
- `PETRI_NET_MODEL.md`
- `ASSAY_MODEL.md`
- `MLOPS.md`
- `SOURCE_PROVENANCE.md`
- `UNCERTAINTY_POLICY.md`
- `ETHICAL_MODELING.md`
- `NUMERIC_ANOMALIES.md`
- `UNRESOLVED_READINGS.md`
- `HOW_TO_ADD_A_DOCUMENT.md`
- `RESEARCH_ROADMAP.md`

## Status vocabulary

- `explicit`: directly stated in the working source.
- `normalized`: a source form has been standardized without changing identity.
- `interpreted`: a domain interpretation has been added.
- `reconstructed`: inferred by a formal model.
- `uncertain`: evidence is insufficient.
- `needs_image_review`: comparison with the archival scan is required.
