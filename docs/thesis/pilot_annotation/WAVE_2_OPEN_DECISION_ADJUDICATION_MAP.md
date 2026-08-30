# Wave 2 Open-Decision Adjudication Map

**Status: PREPARATION ONLY. No decision below is adjudicated in this document.**
No threshold, prior, tau, bootstrap count, tolerance, or temperature ladder is
selected here. This document organizes the 16 `OPEN_REQUIRES_ADJUDICATION`
rows of `WAVE_2_OPEN_DECISION_LEDGER.csv` into a proposed batching sequence
for a future, separately authorized adjudication turn.

**Baseline**: repository HEAD at drafting time is `2c90591091a908c9114013b59629387fe14aee7e`
(one commit ahead of the `1a2592c` baseline cited in the governing instruction,
due to an unrelated same-session CSRF-fix commit to `frontend/config/settings.py`
and `frontend/map_app/tests.py` — outside Model 3B scope. All `docs/thesis/pilot_annotation/`
and `docs/thesis/colab/` content is byte-identical between `1a2592c` and `2c90591`,
so this document is drafted against the same frozen Wave 2 corpus the instruction refers to).

Source: `WAVE_2_OPEN_DECISION_LEDGER.csv`, 16 of 18 rows (the other 2:
`OD-016` ROPE = `DEFERRED`, `OD-017` M0/M3-null label ambiguity =
`NONBLOCKING_CLARIFICATION` — neither is in scope here).

---

## 1. Proposed Batch Sequence

Ten batches, ordered so that no batch is adjudicated before a decision it
structurally depends on. Full per-decision rationale is in the companion CSV
(`WAVE_2_OPEN_DECISION_BATCH_MATRIX.csv`); this section gives the ordering
logic only.

| Order | Batch ID | Decisions | Why grouped |
|---|---|---|---|
| 1 | `BATCH-01-M0-TOLERANCES` | OD-001, OD-002 | Both are M0 score/Hessian numerical-tolerance decisions under the same S7.4/S7.6 "no trial-and-error" prohibition; share a synthetic-evidence-generation step. |
| 2 | `BATCH-02-PARAM-NULL-REPRESENTATION` | OD-003, OD-004 | OD-003's own notes require joint resolution with OD-004 — the parameterization choice directly determines whether/how `n=0` is representable (same defect class as `M3-BLOCK-01`). |
| 3 | `BATCH-03-M2-METRICS` | OD-005, OD-006 | Both M2 primary-metric adoption questions the mathematical contract flags as needing a NUM-DEC-01/02 cross-check; feed the same acceptance-criterion registry. |
| 4 | `BATCH-04-M2-PROFILE-LIKELIHOOD` | OD-007 | Package C — one coherent 10-sub-question design bundle; splitting it risks internally contradictory sub-decisions. |
| 5 | `BATCH-05-M2-BOOTSTRAP` | OD-008 | Package D — one coherent 11-sub-question bundle for M2 exact-null bootstrap calibration; distinct procedure from profile likelihood, kept separate. |
| 6 | `BATCH-06-M3-PRIORS` | OD-009 | Package E — must precede bridge sampling, which requires proper versioned priors as an input. |
| 7 | `BATCH-07-M3-EVIDENCE-METHODS` | OD-010, OD-011, OD-012 | Bridge sampling, TI, and their disagreement threshold are inseparable: TI exists to cross-check bridge sampling, and the escalation threshold cannot be designed before both methods' uncertainty characteristics exist. |
| 8 | `BATCH-08-M3-TAU-CALIBRATION` | OD-013 | Package G — depends on the frozen NUM-DEC-05 prior-odds framework and on a validated marginal-likelihood method from Batch 7; explicitly gated to a separately-authorized future calibration turn per NUM-DEC-04. |
| 9 | `BATCH-09-CROSS-SEED-COMPUTE` | OD-014, OD-015 | Cross-cutting execution-infrastructure design; compute/checkpoint planning structurally depends on the seed-hierarchy addressing scheme. |
| 10 | `BATCH-10-AGGREGATE-THRESHOLD-REGISTRY` | OD-018 | Synthesis/registry-completeness check spanning the M0 objects from Batch 1 and the M2 objects from Batch 3 — not an independent decision, sequenced last among M0/M2 batches. |

Cross-batch note: Batches 4–5 (M2 uncertainty machinery) and 6–8 (M3
Bayesian machinery) are independent of each other and could in principle be
adjudicated in either order or in parallel; Batch 9 (seed/compute
infrastructure) is independent of both model families but is placed after
them because its cost estimates are more informative once the per-batch
implementation shape is clearer. Batch 2 (parameterization/null
representability) is a hard prerequisite for both the M2 and M3 tracks
(it feeds `REQ-M2-001/007` and `REQ-M3-001`) and must be adjudicated before
Batches 4, 5, 7, and 8.

---

## 2. Per-Decision Detail

### OD-001 — M0 score-check tolerance `epsilon_s`
- **Mathematical object**: `epsilon_s`
- **Question**: what tolerance bounds `||s(theta_hat)||_inf <= epsilon_s` for the M0 score check to pass?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S7.4, score `s(theta) = grad_theta ell(theta)`
- **Candidate options** (already in planning, none selected): relative-to-scale tolerance; absolute fixed tolerance; percentile-of-synthetic-null-distribution tolerance
- **Required evidence**: synthetic M0 pilot computational check producing a distribution of `||s(theta_hat)||_inf` under correct specification
- **Upstream dependency**: `REQ-M0-002`, `REQ-M0-003`
- **Downstream impact**: `REQ-M0-008` (M0 gate)
- **Prohibited shortcut**: an arbitrary round number (e.g. `1e-4`) chosen without evidence
- **Batch**: `BATCH-01-M0-TOLERANCES`

### OD-002 — M0 Hessian symmetry/reference tolerances `E_sym`, `E_H`
- **Mathematical object**: `E_sym`, `E_H`
- **Question**: what tolerances bound the Hessian symmetry error and the analytic-vs-numeric-reference comparison error?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S7.6, `E_sym = ||H-H^T||_F / max(1,||H||_F)`, `E_H = ||H_candidate - H_reference||_F / max(1,||H_reference||_F)`
- **Candidate options**: fixed relative-Frobenius-norm tolerance; scale-adaptive tolerance keyed to condition number
- **Required evidence**: synthetic analytic-vs-numeric Hessian comparison across representative parameter regimes
- **Upstream dependency**: `REQ-M0-004`, `REQ-M0-005`
- **Downstream impact**: `REQ-M0-008`
- **Prohibited shortcut**: a tolerance selected post-hoc to make a known result pass
- **Batch**: `BATCH-01-M0-TOLERANCES`

### OD-003 — Parameterization for optimization vs. reporting space (Package A)
- **Mathematical object**: `theta`, `eta`, `n`
- **Question**: which parameterization is used for optimization, which for reporting, and how does `n=0` boundary behavior interact with that choice?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S7.7, three candidate reparameterizations
- **Candidate options**: `(mu,alpha,beta)` direct; `(mu,n,beta)` direct; fully unconstrained transformed `eta` with `n = logit^-1(eta_n)`
- **Required evidence**: identifiability/optimization-stability comparison under synthetic near-critical and near-null regimes
- **Upstream dependency**: `REQ-M0-006`
- **Downstream impact**: `REQ-M2-001`, `REQ-M2-007`, `REQ-M3-001` (n=0 representability)
- **Prohibited shortcut**: none formally rejected yet — this is a brainstorming-stage question, not an adjudication; the shortcut to avoid is adopting the naive logit transform as the sole representation without checking OD-004
- **Batch**: `BATCH-02-PARAM-NULL-REPRESENTATION`

### OD-004 — Exact-null representability under unconstrained transform
- **Mathematical object**: `n`, `eta_n`
- **Question**: what representation makes `n=0` exactly reachable in at least one code path, given that a naive logit transform structurally excludes it?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` §7.7 item 3–4; directly parallels `M3-BLOCK-01`
- **Candidate options**: explicit nested null submodel with a separate parameter space (no `eta_n` at all under H0); piecewise transform with a hard `n=0` branch; hurdle/mixture representation
- **Required evidence**: design review confirming the chosen representation reaches `n=0` exactly, with a passing unit test
- **Upstream dependency**: `REQ-M0-006`, `REQ-M2-010`, `REQ-M3-001`
- **Downstream impact**: `REQ-M2-011`, `REQ-M3-009`
- **Prohibited shortcut**: `logit^-1(eta_n)` alone as the sole representation (structurally excludes `n=0` for any finite `eta_n` — the confirmed defect class); must not be closed by planning-only design review alone
- **Batch**: `BATCH-02-PARAM-NULL-REPRESENTATION`

### OD-005 — AbsBias as adopted exact-null acceptance metric
- **Mathematical object**: `AbsBias_c`
- **Question**: is `AbsBias_c` the adopted M2 exact-null bias metric, given `RelBias` is undefined at `n_c=0`?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S8.4, `AbsBias_c = (1/R_valid,c) * sum |n_hat_cr - n_c|`
- **Candidate options**: `AbsBias_c` as proposed; a different exact-null-specific metric
- **Required evidence**: explicit researcher review confirming `AbsBias_c` against frozen NUM-DEC-01/02 documents
- **Upstream dependency**: `REQ-M2-005`
- **Downstream impact**: `REQ-M2-008` (acceptance-criterion registry)
- **Prohibited shortcut**: `RelBias` at the exact null (`n_c=0`) — mathematically undefined (division by zero)
- **Batch**: `BATCH-03-M2-METRICS`

### OD-006 — Primary M2 coverage metric: `Coverage_c` vs `CoverAndValid_c`
- **Mathematical object**: `Coverage_c`, `CoverAndValid_c`
- **Question**: is the primary M2 coverage metric conditional-on-valid-interval (`Coverage_c`) or unconditional/attempted-denominator (`CoverAndValid_c`)?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S8.7
- **Candidate options**: `Coverage_c` (conditional, always reported with failure rate); `CoverAndValid_c` (unconditional, attempted-denominator)
- **Required evidence**: cross-check against NUM-DEC-01/02's own metric-denominator language
- **Upstream dependency**: `REQ-M2-008`
- **Downstream impact**: `REQ-M2-009` (MCSE target), acceptance-criterion registry
- **Prohibited shortcut**: adopting a new primary metric without the NUM-DEC cross-check
- **Batch**: `BATCH-03-M2-METRICS`

### OD-007 — Profile-likelihood design (Package C)
- **Mathematical object**: `ell_p(n)`, `D(n)`, `C_{1-gamma}`
- **Question**: 10 coupled sub-questions — initial grid, adaptive refinement, nuisance optimization, warm-start policy, endpoint search, disconnected-confidence-set handling, boundary (`n=0`, `n->1^-`) handling, profile-failure classification, interpolation method, permitted monotonicity assumptions.
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S8.6, `D(n) = 2[ell_p(n_hat) - ell_p(n)]`, `C_{1-gamma} = {n : D(n) <= c_{1-gamma}}`
- **Candidate options**: fixed uniform grid then local refinement near `D(n)=c`; fully adaptive bisection/golden-section endpoint search; hybrid
- **Required evidence**: future implementation-design review; synthetic profile-shape stress tests (unimodal, ridge, boundary-touching)
- **Upstream dependency**: `REQ-M2-007`
- **Downstream impact**: `REQ-M2-008`, `REQ-M2-011`, `REQ-M2-012`
- **Prohibited shortcut**: assuming monotonicity of the profile log-likelihood without stress-testing ridge-shaped and boundary-touching synthetic profiles
- **Batch**: `BATCH-04-M2-PROFILE-LIKELIHOOD`

### OD-008 — M2 exact-null bootstrap design (Package D)
- **Mathematical object**: `B`, `Lambda(Y)`, `Y*(b)`
- **Question**: 11 coupled sub-questions — replication count `B`, seed hierarchy, failed-fit policy, denominator policy, adaptive extension, critical-value estimation, exact-null generation contract, nonfinite/negative-LR treatment, calibration-validity acceptance criteria.
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S9.4, bootstrap LR statistic `Lambda*(b) = 2[ell(theta_hat_1*(b)) - ell(theta_hat_0*(b))]`, bootstrap p-value formula
- **Candidate options**: fixed `B` (illustrative examples such as 999/1999 appear in the contract but are **not adopted**); sequential/adaptive `B` with a stopping rule keyed to target MCSE
- **Required evidence**: future implementation-design review; MCSE-target-driven `B` selection once a target MCSE is itself adjudicated
- **Upstream dependency**: `REQ-M2-011`, `REQ-M2-010`
- **Downstream impact**: `REQ-M2-012`; the same bootstrap-machinery pattern is reused in principle for the M3 tau-calibration track
- **Prohibited shortcut**: picking `B` before a target MCSE exists; silently dropping failed bootstrap fits from the denominator
- **Batch**: `BATCH-05-M2-BOOTSTRAP`

### OD-009 — M3 within-model priors for `mu`, `beta`, `n` (Package E)
- **Mathematical object**: `p(mu|M_k)`, `p(beta|M1)`, `p(n|M1)`
- **Question**: what proper, versioned priors govern the excitation model's parameters?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S10.5
- **Candidate options**: weakly informative conjugate-adjacent priors (Normal on `log mu`, Gamma on `beta`, Beta on `n`); reference/objective priors; empirical-Bayes-informed priors (**rejected** — would require historical data)
- **Required evidence**: prior-predictive check results under synthetic generating processes; properness verification; bridge-sampling compatibility check
- **Upstream dependency**: `REQ-M3-002`, `REQ-M3-006`
- **Downstream impact**: `REQ-M3-003`, `REQ-M3-004`, `REQ-M3-005`, `REQ-M3-009` — all downstream of a proper prior
- **Prohibited shortcut**: deriving priors empirical-Bayes-style from the historical data being analyzed; selecting a prior purely for computational convenience without a documented prior-predictive check
- **Batch**: `BATCH-06-M3-PRIORS` — directly linked to `M3-BLOCK-06`

### OD-010 — Bridge sampling design (Package F)
- **Mathematical object**: `Z`, `g(theta)`, `h(theta)`
- **Question**: 15 coupled sub-questions — sampling space, constrained-to-unconstrained transform + Jacobian, proposal `g`, bridge function `h`, draw-count requirements, chain inclusion rules, convergence diagnostics, ESS requirements, repeated-run stability, overflow/underflow safeguards, log-scale computation, bridge failure taxonomy, uncertainty estimate, reproducibility.
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S11, `Z = E_g[h(theta)q(theta)] / E_p[h(theta)g(theta)]`
- **Candidate options**: optimal bridge function (Meng & Wong); geometric bridge; warp-II bridge sampling variants
- **Required evidence**: future implementation-design review; toy-model validation against a known-closed-form `Z` before any real use
- **Upstream dependency**: `REQ-M3-003`, `REQ-M3-006`, `REQ-M0-006`
- **Downstream impact**: `REQ-M3-004`, `REQ-M3-011`
- **Prohibited shortcut**: running bridge sampling in this or any planning turn; directly linked to `M3-BLOCK-02/03/04`
- **Batch**: `BATCH-07-M3-EVIDENCE-METHODS`

### OD-011 — Thermodynamic-integration temperature ladder and discretization design
- **Mathematical object**: `p_t(theta|Y)`
- **Question**: what temperature ladder (spacing, count, integration rule) is used for TI?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S12, `p_t(theta|Y) propto p(Y|theta)^t p(theta)`, `log p(Y) = integral_0^1 E_t[log p(Y|theta)] dt`
- **Candidate options**: geometric ladder with denser spacing near `t=0`; fixed-count linear ladder (flagged as likely insufficient, not formally rejected); adaptive ladder refinement
- **Required evidence**: synthetic TI discretization-error study on the validation subset defined in NUM-DEC-06
- **Upstream dependency**: `REQ-M3-009`, `REQ-M3-010`
- **Downstream impact**: `REQ-M3-011`
- **Prohibited shortcut**: adopting naive uniform spacing as a default without a synthetic discretization-error study; directly linked to `M3-BLOCK-05`
- **Batch**: `BATCH-07-M3-EVIDENCE-METHODS`

### OD-012 — Bridge-vs-TI escalation threshold `Delta_BTI`
- **Mathematical object**: `Delta_BTI`
- **Question**: what threshold on `|log Z_bridge - log Z_TI|` triggers `MODEL_COMPARISON_NUMERICALLY_UNRESOLVED`?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md` S12, `Delta_BTI = |log Z_bridge_hat - log Z_TI_hat|`
- **Candidate options**: fixed log-scale absolute threshold; threshold scaled to each method's own estimated MC uncertainty
- **Required evidence**: synthetic dual-method (bridge+TI) runs on the same toy posteriors to characterize typical disagreement under correct implementation
- **Upstream dependency**: `REQ-M3-009`, `REQ-M3-010`, `REQ-M3-011`
- **Downstream impact**: `REQ-M3-004` (BF validity gate)
- **Prohibited shortcut**: choosing an arbitrary fixed number without characterizing typical disagreement first; matches NUM-DEC-06's own unresolved `BRIDGE_TI_AGREEMENT_TOLERANCE` item
- **Batch**: `BATCH-07-M3-EVIDENCE-METHODS`

### OD-013 — Tau calibration design (Package G)
- **Mathematical object**: `tau`, `alpha_target`, `tau_star`
- **Question**: 11 coupled sub-questions — `alpha_target`, candidate tau grid, alternative grid, prior-odds sensitivity grid, MC precision target, replication count, failure handling, objective function, tie-breaking rule, stability criterion, independent confirmation method.
- **Formula**: `WAVE_2_TAU_CALIBRATION_PREREGISTRATION.md`, `FSR_0_hat(tau)`, `DP_j_hat(tau)`, candidate rule `tau_star = inf{tau : FSR_0_hat(tau) <= alpha_target}`
- **Candidate options**: the illustrative grid `{0.50,0.75,0.90,0.95,0.975,0.99}` referenced elsewhere in the frozen corpus (NUM-DEC-04) as a comparison grid — **not adopted here as final**; `alpha_target` such as 0.05 — **not selected**
- **Required evidence**: future prospective synthetic calibration per NUM-DEC-04's approved procedure
- **Upstream dependency**: `REQ-M3-007`, `REQ-M3-013`, `REQ-M3-014`
- **Downstream impact**: the final NUM-DEC-04 value adjudication — a separately authorized future decision, explicitly not part of Wave 2 or this batch
- **Prohibited shortcut**: selecting tau in this or any planning-only turn; selecting tau from the FSR-only rule without a joint FNR/power check; reusing the illustrative 0.90/0.95 example or the illustrative grid as adopted values
- **Batch**: `BATCH-08-M3-TAU-CALIBRATION`

### OD-014 — Seed-hierarchy derivation function `f(s_master,c,r,m)`
- **Mathematical object**: `s_{c,r,m}`
- **Question**: what deterministic function derives per-(cell, replication, method) seeds from a master seed with adequate collision resistance and independence?
- **Formula**: `WAVE_2_MATHEMATICAL_CONTRACT.md`/`WAVE_2_SIMULATION_AND_COVERAGE_PLAN.md` §13.4, `s_{c,r,m} = f(s_master, c, r, m)`
- **Candidate options**: cryptographic hash-based derivation (hash of tuple, truncated to seed range); counter-based RNG (Philox/Threefry) keyed by `(c,r,m)`; splittable-RNG derivation
- **Required evidence**: collision-resistance test on a large synthetic `(c,r,m)` grid; independence test (e.g. RNG test suite) on derived streams
- **Upstream dependency**: `REQ-M3-015`
- **Downstream impact**: `REQ-M2-002`, `REQ-M3-009`, `REQ-M3-010` execution manifests
- **Prohibited shortcut**: naive linear combination of indices — flagged as collision-prone and lacking independence guarantees, not adopted
- **Batch**: `BATCH-09-CROSS-SEED-COMPUTE`

### OD-015 — Compute planning: storage, checkpoint, restart, provenance (Package H)
- **Mathematical object**: n/a (infrastructure design)
- **Question**: what symbolic/structural cost model governs storage estimate, checkpoint design, restart determinism, and provenance manifest content?
- **Formula**: `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md`, resource formulas from NUM-DEC-08 (`T_serial_hat`, `S_total_hat`, `M_peak_hat`)
- **Candidate options**: symbolic/structural estimate scaled from Wave-1-era pilot logs (per-cell time × replication count × method-cost multiplier); no benchmark executed
- **Required evidence**: the structural estimate document itself (already drafted in `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md`), reviewed against NUM-DEC-08's resource-envelope framework
- **Upstream dependency**: `REQ-CROSS-001`
- **Downstream impact**: NUM-DEC-08 resource-envelope framework (still `PENDING_MEASUREMENT` for all 8 ceiling dimensions)
- **Prohibited shortcut**: running an actual compute-cost benchmark in a planning turn — explicitly prohibited by the governing instruction (§18 Package H)
- **Batch**: `BATCH-09-CROSS-SEED-COMPUTE`

### OD-018 — M2/M3 acceptance-criterion thresholds not yet set (aggregate)
- **Mathematical object**: various (see registry)
- **Question**: aggregate entry tracking every M0/M2 acceptance-criterion threshold not yet set — resolves only as each itemized row below is separately adjudicated.
- **Formula**: full itemized registry in `WAVE_2_MATHEMATICAL_CONTRACT.md` §6 (per-criterion candidate/rejected/evidence breakdown)
- **Candidate options**: see the S6 registry — every row currently `threshold_status=OPEN_REQUIRES_ADJUDICATION`, `threshold_value=NULL`
- **Required evidence**: per-criterion synthetic evidence as itemized in the acceptance-criterion registry
- **Upstream dependency**: `REQ-M0-003`, `REQ-M0-005`, `REQ-M2-005`, `REQ-M2-006`, `REQ-M2-008`
- **Downstream impact**: every downstream gate decision for M0/M2
- **Prohibited shortcut**: filling any threshold via guessing or common practice without a sourced decision (§21 of the governing instruction)
- **Batch**: `BATCH-10-AGGREGATE-THRESHOLD-REGISTRY`

---

## 3. Decidable-from-Frozen-Sources vs. Blocked-on-Future-Evidence

**Decidable from frozen sources + general methodological literature alone,
no benchmark or calibration required** (3 of 16):

- **OD-005** (AbsBias adoption) — resolves via a documented NUM-DEC-01/02 cross-check, a review action, not a computational one.
- **OD-006** (Coverage_c vs CoverAndValid_c) — same: resolves via cross-checking NUM-DEC-01/02's own denominator language.
- **OD-015** (compute-planning structural estimate) — the ledger and the governing instruction (§18 Package H) explicitly restrict this to a symbolic/structural estimate; no benchmark is permitted or needed to answer the design question itself (the estimate's *numerical accuracy* is separately gated by NUM-DEC-08's `PENDING_MEASUREMENT` framework, which is out of scope for this decision).

**Blocked on future calibration and/or implementation evidence before final
adjudication** (13 of 16): OD-001, OD-002, OD-003, OD-004, OD-007, OD-008,
OD-009, OD-010, OD-011, OD-012, OD-013, OD-014, OD-018.

Within this blocked set, two sub-patterns are worth distinguishing (see the
`requires_implementation_evidence` vs `requires_calibration_evidence` columns
in the companion CSV for the exact split per decision):

- **OD-004** requires no calibration evidence, but does require a passing
  implementation unit test before closure — its underlying design *choice*
  could in principle be argued from mathematical structure and literature
  alone, but the governing instruction is explicit that it "must not be
  closed by planning alone."
- **OD-018** requires no fresh implementation evidence of its own (it is an
  aggregate/registry-completeness entry) but cannot resolve until its
  constituent per-criterion decisions (which do require calibration
  evidence) are each separately adjudicated.

All other 11 decisions in the blocked set require genuine future synthetic
calibration, prior-predictive checking, toy-model validation, or
implementation-design review before a defensible value can be adopted — none
of that evidence exists yet, and none of it is generated in this or any
planning-only turn.

---

## 4. Explicit Non-Actions This Turn

- No literature search was performed.
- No decision above was adjudicated; every `current_status` in
  `WAVE_2_OPEN_DECISION_LEDGER.csv` remains exactly as frozen.
- No threshold, prior, tau, bootstrap count, tolerance, or temperature
  ladder was selected.
- No code was written or modified.
- No statistical procedure was run.
- Nothing was staged, committed, pushed, synced, or deployed.
