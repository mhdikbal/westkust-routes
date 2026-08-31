# Session Audit Files — Relocation Manifest

Status: **RELOCATION-ONLY**. This manifest documents a pure file relocation. No document content was changed. No historical reference elsewhere in the repository was rewritten.

---

## 1. Purpose

Repository-root housekeeping: five session/audit `.md` files were scattered at the repository root, cluttering it alongside standard project files (`README.md`, `CLAUDE.md`, `CONTRIBUTING.md`). This relocation moves them into a single, clearly-scoped directory (`session-docs/`) without altering their content.

## 2. Provenance

```text
Relocation date:       2026-08-31
Source baseline commit: e165e6fefae1316794a238589703220a5e1dafca
Current local parent:   91e9740917e318f4ff89fa1784e62330233fda5b
Destination directory:  session-docs/
```

These five files are **not part of** the `91e9740` OP-10 enum-contract commit — they belong to a separate, user-authorized Markdown-housekeeping workstream, unrelated to the Model 3B V2 / OD-005 effort. This relocation changes no Model 3B semantics, no operation registry, no successor specification, and no ART-016 content.

## 3. What this relocation does and does not do

- Moves five files from the repository root into `session-docs/`, byte-for-byte.
- Does **not** modify the content of any of the five files.
- Does **not** rewrite any historical reference to the old root-relative paths found elsewhere in the repository (see §5) — those references remain as point-in-time prose, describing where the file was located at the time they were written.
- Is **not** a deletion — each file is relocated (renamed), never removed.
- Serves as the current-path crosswalk for anyone following an old root-relative citation to one of these five files.

## 4. Relocation crosswalk

| Filename | Old path | New path | Source blob | Destination blob | Content-preservation result |
|---|---|---|---|---|---|
| `BETA_UI_DEPLOYMENT_AUDIT.md` | `./BETA_UI_DEPLOYMENT_AUDIT.md` | `session-docs/BETA_UI_DEPLOYMENT_AUDIT.md` | `a21b35f34969f1738b3793b08d982e047a7a85d7` | `a21b35f34969f1738b3793b08d982e047a7a85d7` | `BYTE_IDENTICAL_RENAME` |
| `COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT.md` | `./COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT.md` | `session-docs/COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT.md` | `2c5454190117acf78a4a90bb69b4596a782da3cd` | `2c5454190117acf78a4a90bb69b4596a782da3cd` | `BYTE_IDENTICAL_RENAME` |
| `CORPUS_DIPLOMATICUM_RECOVERY_PREFLIGHT.md` | `./CORPUS_DIPLOMATICUM_RECOVERY_PREFLIGHT.md` | `session-docs/CORPUS_DIPLOMATICUM_RECOVERY_PREFLIGHT.md` | `8277cea3b42b8f5998e645835ac661be27b08026` | `8277cea3b42b8f5998e645835ac661be27b08026` | `BYTE_IDENTICAL_RENAME` |
| `HAWKES_MODEL_AUDIT.md` | `./HAWKES_MODEL_AUDIT.md` | `session-docs/HAWKES_MODEL_AUDIT.md` | `41d88c1e3b9e1f3a037bee020d4f8ef312bede99` | `41d88c1e3b9e1f3a037bee020d4f8ef312bede99` | `BYTE_IDENTICAL_RENAME` |
| `SOURCE_PROVENANCE_AND_VERSION_CONTROL_AUDIT.md` | `./SOURCE_PROVENANCE_AND_VERSION_CONTROL_AUDIT.md` | `session-docs/SOURCE_PROVENANCE_AND_VERSION_CONTROL_AUDIT.md` | `094ace9b223fa55de5e9aca21c580b1718b122b6` | `094ace9b223fa55de5e9aca21c580b1718b122b6` | `BYTE_IDENTICAL_RENAME` |

5/5 blob hashes match exactly between source and destination. 5/5 classified `BYTE_IDENTICAL_RENAME`.

## 5. Reference-integrity findings (from the prior audit turn, unchanged by this manifest)

```text
Hard functional broken references:    0   (0 Markdown hyperlinks, 0 script path-literal reads found against any of the 5 old paths)
Soft historical location claims:      1   (docs/thesis/pilot_annotation/MODEL_3B_PILOT_RECOVERY_DIAGNOSTIC_AUDIT.md, a point-in-time table entry naming COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT.md's then-current root location)
Historical source artifact modifications: 0
```

The one soft location claim is left untouched deliberately — it is a historical, point-in-time statement, not a live link, and rewriting it would edit an existing Model 3B diagnostic artifact outside this relocation's authorized scope. This manifest is the discoverability mechanism going forward.

## 6. Current-path resolution rule

For any reference found anywhere in this repository (prose, comment, or table entry) of the form:

```text
./<filename>
```

where `<filename>` is one of the five names in §4, the current relocated path is:

```text
session-docs/<filename>
```

This rule applies uniformly to all five files and to any future reference discovered later.

## 7. Non-claims

This manifest does not claim: that any of the five documents' content changed; that any Model 3B artifact changed; that the OP-10 enum contract changed; that a successor reconciliation was created; that any test was executed; that E3 or E4 began.
