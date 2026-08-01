# MLOps and Data Lifecycle

## Data layers

### Bronze

Archive images, DOCX source, raw OCR or HTR, download metadata, checksums.

### Silver

Paragraphs, diplomatic transcription, normalized transcription, translation, marginalia separation, entity annotations.

### Gold

Persons, roles, HRLT assertions, operations, assays, inventory, claims, solver inputs, graph edges.

## Versioning

Use Git for code and documentation. Use DVC or lakeFS for source images and generated datasets.

Suggested releases:

```text
v0.1 seed extraction
v0.2 full inventory and solver inputs
v0.3 complete documentation
v0.4 source-passage linkage
v0.5 constraint solver
v0.6 Petri net simulator
v1.0 reviewed research release
```

## Validation gates

1. schema validation;
2. foreign-key validation;
3. numerical reconciliation;
4. provenance validation;
5. human philological review;
6. release manifest and checksum.

## Reproducibility

Every release must include:

- source-file checksum;
- generation script version;
- output manifest;
- row counts;
- unresolved-reading count;
- anomaly count.

## Model monitoring

Track:

```text
extraction precision
unresolved-term rate
rows without paragraph linkage
rows without folio linkage
solver contradiction count
percentage of reconstructed assignments
```
