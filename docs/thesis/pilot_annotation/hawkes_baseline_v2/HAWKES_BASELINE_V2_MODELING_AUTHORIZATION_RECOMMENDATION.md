# Hawkes Baseline V2 — Modeling Authorization Recommendation

```text
G_V2_preauth = 0
```

Per instruction §17, an `AUTHORIZE_V2_MODELING_WITH_LIMITATIONS` recommendation may be issued only if `G_V2_preauth=1`. It is 0. The recommendation below is one of the other five allowed values.

## Recommendation

```text
DEFER_PENDING_G7_GATES
```

## Why this recommendation, not a different one

`G_G7=0` is the single factor that, by itself, zeroes `G_V2_preauth` regardless of every other factor's value. The two failing H-gates (H-05, H-08) both require actions **entirely outside this operation's scope**:

- **H-05** requires the newly-specified, Phase-D-distinct recovery design (`D_distinct=1`, see `HAWKES_BASELINE_V2_RECOVERY_DISTINCTION_MATRIX.csv`) to actually be **executed** and pass the ≥0.80 threshold. This operation was explicitly prohibited from running any simulation recovery.
- **H-08** requires a **separate, explicit researcher decision** authorizing historical inference from a Hawkes fit — a decision distinct from, and not satisfied by, V2 modeling authorization itself.

By contrast, the other two blocking factors are now narrow and well-characterized, not structural:

- **P_141** fails only because 2 of the original 6 dedup cases remain `REQUIRES_FOLIO_OR_SOURCE_CHECK` (down from a 6-unresolved + 32-ambiguous entry state). Both have a named, specific next step (a CD6 folio search for Koto Tangah 1755; a CD3 cross-check against an RGP-cited "Corpus III, nr. D" for the Bayang 1687 event).
- **F_SLR** fails only because 1 of 14 formulas (the time-rescaling theorem) has its correct source identified (Ogata 1988) but not yet confirmed against full text.

`DEFER_PENDING_RESIDUAL_PROVENANCE` and `DEFER_PENDING_POINT_PROCESS_METHOD_SUPPORT` were considered and rejected as the *primary* recommendation because P_141 and F_SLR are no longer the dominant blockers — they are narrow, nearly-resolved residuals that could plausibly close within the same future operation that addresses H-05/H-08. `REJECT_CURRENT_V2_DESIGN` was rejected because the V2 design itself (Work Package G) is sound and demonstrably distinct from Phase D — there is no defect in the design to reject. `REQUIRES_RESEARCHER_REVIEW` was rejected because every blocker has a specific, actionable, already-identified corrective path (see `HAWKES_BASELINE_V2_RESIDUAL_BLOCKER_MATRIX.csv`) — this is not an impasse requiring open-ended researcher judgment, it is a known punch list.

## What must happen, in one future standalone operation, before `A_V2` can be considered

1. Execute the specified V2 recovery design (not Phase D) and confirm it passes the ≥0.80 recovery-accuracy gate → resolves H-05.
2. Obtain a separate, explicit researcher decision on historical-inference authorization → resolves H-08.
3. Locate the CD6 folio for Koto Tangah (DEDUP-05) and cross-check the RGP "Corpus III, nr. D" reference (DEDUP-06) → resolves P_141.
4. Obtain full text of Ogata (1988), JASA 83(401), and confirm the exact time-rescaling theorem section → resolves F_SLR.

Only after all four are resolved does `G_G7=1` become possible, and only then can `G_V2_preauth` be recomputed toward 1.

## Final gate state

```text
A_V2 is NOT created this operation (G_V2_preauth != 1, per instruction §18)
G_V2_model = G_V2_preauth x A_V2 = 0
```

## Final status

```text
MODELING_REMAINS_BLOCKED
```
