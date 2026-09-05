# SLR-DEC-08 — Researcher Adjudication Decision (Seed-Study Set)

**Status:** SUBSTANTIVE ADJUDICATION. Adjudicates SLR-DEC-08 only.

**Baseline:** commit `79a6a614cee74df85a27c37e0c0792501825199b`.

---

## 1. Authoritative Definition (quoted verbatim from the ledger)

```text
decision_topic: seed-study set (K = {k_1,...,k_m})
candidate_options: not populated; m has not been invented and no seed study has been drawn
  from memory
auditor_note_consequences: a preregistered seed-study set must be nominated by the researcher
  (e.g. known foundational hermeneutics/DH/archival-criticism/Hawkes papers already known to
  the project) before pilot sensitivity P_hat_seed can be computed; seed studies are diagnostic
  only and are not automatically included in final synthesis
```

This matches "seed-study governance" exactly. No mismatch found.

Critically, the authoritative definition requires the seed set to be **nominated by the researcher** — not discovered or invented by Claude. No such nomination has been made in this conversation or any prior frozen artifact.

---

## 2. Seed Candidate Universe

```math
Z^* = \{z_1,\ldots,z_M\}.
```

Every SLR artifact under `docs/thesis/pilot_annotation/systematic_literature_review/` and the computational-hermeneutics protocol were searched for any already-cited, exact bibliographic record (title + author + year/identifier) suitable as a seed study for the review's substantive topic domain. **None was found.** The protocol references concepts and scholars by name in passing (e.g. Gadamer/Heidegger hermeneutic lineage, Moretti-style distant reading, Trouillot-style archival-silence theory) but never cites an exact, verifiable bibliographic record for any of them. No researcher-provided reference was supplied in this conversation.

```math
M = 0,\qquad A_m^{\mathrm{seed}} \text{ is vacuously satisfied for the empty set},\qquad Z=\varnothing,\qquad M_Z=0.
```

No title was invented or classified as a seed merely because it seemed relevant. `SLR_DEC_07_08_SEED_STUDY_REGISTRY.csv` is created with the authoritative header and zero data rows.

---

## 3. DEC-08 Readiness Gate

```text
D_8,dep=1: SLR-DEC-05/06/07 all adjudicated
D_8,set=1: seed universe and admitted set are finite (M=0, M_Z=0 — zero is a finite number)
D_8,id=1: every admitted seed identity is verified (vacuously true — zero admitted seeds)
D_8,prov=1: every admitted seed has exact provenance (vacuously true)
D_8,bound=1: seed use is diagnostic, not a total-recall claim (stated explicitly, Sec.4)
D_8,0=1: no seed result is fabricated or assumed
```

```math
G_8^{\mathrm{decision\_ready}} = 1.
```

The gate does not require `M_Z>0` — it requires the finite set and its handling to be honestly and completely characterized, which a correctly-reported empty set satisfies.

---

## 4. Researcher Decision

```text
SLR-DEC-08:
APPROVE_WITH_LIMITATIONS
```

This approves the seed-study **governance framework** — the admissibility rule (`A_m^seed = 1[I_m=R_m=P_m=B_m=1]`), the required per-seed provenance fields, the independence-disclosure requirement, and the diagnostic-only (never total-recall) usage boundary — not any specific seed study, since none is currently admitted.

Per instruction §5: **DEC-08 is not approved merely to enable the pilot.** The pilot proceeded under the explicit zero-seed diagnostic design the authoritative definition itself anticipates ("before pilot sensitivity P_hat_seed can be computed" implies the estimand is simply not computed, not that the pilot cannot occur). `SLR_PILOT_SEED_RETRIEVAL_MATRIX.csv` records the diagnostic as `NOT_ESTIMABLE_NO_ADMISSIBLE_SEEDS`, not a fabricated value.

---

## 5. Explicit Limitations

1. Zero admissible seed studies exist as of this decision (`M_Z=0`).
2. The seed-retrieval diagnostic (`P̂_seed`) is `NOT_ESTIMABLE_NO_ADMISSIBLE_SEEDS` for this pilot — it is not zero, not skipped silently, and not a recall claim of any kind.
3. This decision does not claim discipline-general search methods (per SLR-DEC-06) substitute for seed validation.
4. Future seed nomination remains explicitly open: the researcher may nominate specific foundational papers (hermeneutics/DH/archival-criticism/Hawkes-process literature already known to the project) in a later, separate turn, at which point this governance framework already approved here would apply to admit them.
5. No statistical independence is claimed among any future seeds merely because none exist to claim it about yet.

---

## 6. Ledger Amendment Contract

`SLR-DEC-08` row: `status=ADJUDICATED_APPROVED_WITH_LIMITATIONS`, `adjudicated_decision` referencing this artifact and the seed study registry/retrieval matrix, explicitly recording `M_Z=0` and the `NOT_ESTIMABLE` diagnostic status.

---

## 7. Final Status

```text
SLR-DEC-08 adjudicated: APPROVE_WITH_LIMITATIONS (governance framework only, M_Z=0)
```
