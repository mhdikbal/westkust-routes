# Production Research Page — SEC-3B Numeric Rate-Limit Closure Plan

> **Phase:** SEC-3B — narrow retest of exactly `SEC3A-IP-007` and `SEC3A-IP-008`. Not a repeat of SEC-3/SEC-3A's broader scope.
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`, SEC-3 `7c0621d512c8574df7b9ca041577a1080ac7e618`, SEC-3A `2864fc28d958194883355e999f111ff7aa4114e8`

---

## 1. Scope

Exactly two prior limited results, and nothing else:

```text
SEC3A-IP-007: two distinct restored client IPs should receive distinct rate-limit buckets
SEC3A-IP-008: requests from the same restored client IP should share the intended bucket
```

The 20 real-Django tests, duplicated-prefix tests, `APPEND_SLASH` tests, redirect tests, relative-link tests, the full credential-store rehearsal, the full SEC-3/SEC-3A matrices, the Option A architecture, account-provisioning design, and Entra/OIDC design were **not** repeated — SEC-0 through SEC-3A's frozen results stand as the evidence for all of those.

## 2. Phase 2 Root-Cause Reconfirmation — Result Diverges from the Prior Hypothesis

SEC-3A's audit classified the earlier failure as a sandbox rate-limiter malfunction, implicitly assuming a fresh environment would resolve it. This turn tested that assumption directly, **before** building the full CLIENT_A/CLIENT_B topology, per the instruction's own Phase 2/Phase 8 sequencing:

1. A completely new Docker network and container (`sec3b_ctrl`, never previously used, standard `nginx:1.25-alpine`) was created.
2. A deliberately extreme, minimal threshold was configured: `rate=1r/m` (one request per **minute**), no burst allowance at all — the same class of extreme control case used in SEC-3A's own isolation attempt.
3. Ten rapid sequential requests were sent, all within roughly 100ms of container start.
4. **All ten returned `200`.** Zero were rejected. The access log confirms all ten requests landed within the same second, none delayed, none `429`.

This is the formal `SEC3B-CTRL-001` result, and it fails. Per the instruction's own explicit contingency for this exact outcome:

```text
"If the fresh-zone control does not enforce: do not interpret IP-007/IP-008;
classify the environment as invalid; stop with SEC3B_REQUIRES_REVIEW."
```

**This turn's finding therefore diverges from the prior hypothesis.** The prior SEC-3A classification (`TEST_ENVIRONMENT_LIMITATION_REQUIRES_FRESH_STATE`, implying the problem was specific to *that* session's accumulated state) does not hold — the identical failure reproduces in a container that has never existed before, with a threshold two orders of magnitude more restrictive than anything tested in SEC-3A. The corrected classification is:

```text
NGINX_LIMIT_REQ_MODULE_NOT_ENFORCING_IN_THIS_SANDBOX_PLATFORM
```

This is evidence-bounded to what was observed: `nginx`'s `limit_req` shared-memory rate-limiting mechanism does not enforce thresholds in this specific sandboxed Docker execution environment, regardless of session freshness, threshold strictness, or configuration correctness (syntax validation passed in every attempt; `nginx -t` never flagged an error). The mechanism worked correctly, with real `429` responses, earlier in this same overall multi-day work series (SEC-2A, SEC-3) — so this is not a claim that `limit_req` is broken in general, only that it is not currently enforcing in this particular sandbox instance, for a reason not isolated within this turn's budget (candidate causes not confirmed: a platform-level restriction on the timer/clock or shared-memory primitives `limit_req` depends on; a container-runtime change between sessions; host resource-accounting changes — none of these were confirmed, only the symptom).

## 3. Consequence for This Turn

Per the instruction's own designed off-ramp, IP-007 and IP-008 are **not reinterpreted** using this invalid environment. `PRODUCTION_RESEARCH_PAGE_SEC3B_TEST_RESULTS.csv` records the control-test failure and marks every downstream test `NOT_RUN` (blocked by the control failure), rather than fabricating a pass or silently skipping the record.

```text
SEC3-F-02: OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST (unchanged)
```

The original `SEC3A-IP-007`/`SEC3A-IP-008` result cells in `PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_IP_TEST_RESULTS.csv` are **not modified** by this turn.

## 4. What Would Be Needed to Actually Close This

A working `limit_req` enforcement environment — most plausibly a different sandbox/host, a container runtime without whatever restriction is suppressing the shared-memory zone's timer accounting, or (for the eventual real closure) the actual production-like environment itself in a future `SEC-4`-adjacent test. This plan's design content (deterministic test structure, CLIENT_A/CLIENT_B synthetic identities, trust-boundary sequencing) remains valid and reusable once a working environment is available — it was not executed to completion this turn, not because it was wrong, but because its precondition (a functioning rate limiter to observe) was not met.
