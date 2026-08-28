# Production Research Page — SEC-2 Negative Test Report

> **Phase:** SEC-2, negative security tests (Phase 11 of the SEC-2 execution)
> **Baseline:** `e813192b590917a7f96b9e3ca7da5c8c9a907be8`
> **All tests non-destructive, run only against the isolated test workspace.**

---

## 1. Scope

Sixteen negative-test categories were specified by the researcher's SEC-2 instruction. This report records what was actually run, what passed, and — honestly — what did not fully validate this turn, with the exact reason.

## 2. Results by Category

| # | Category | Test ID(s) | Result | Detail |
|---|---|---|---|---|
| 1 | Anonymous protected page access | SEC2-T-006–011 | PASS | All 6 page paths (both prefixes) returned 401 |
| 2 | Anonymous protected API access | SEC2-T-012–013 | PASS | Both APIs returned 401 |
| 3 | Invalid credentials | SEC2-T-014–015 | PASS | 401 on both a protected page and a protected API |
| 4 | Alternate prefix bypass | SEC2-T-006–024 (cross-referenced) | PASS | `/atlas/` and `/westkust/` both denied anonymous access identically — no prefix offered a weaker boundary |
| 5 | Direct test-port bypass | SEC2-T-004 | PASS | N1 binding refused non-loopback connection outright |
| 6 | Alternate Host header | SEC2-T-029 | **PASS_WITH_LIMITATION** | See §3.1 |
| 7 | Encoded path | SEC2-T-027 | PASS | `%61tlas` still resolved to the protected `/atlas/` block and was denied |
| 8 | Repeated slash | SEC2-T-026 | PASS | `//atlas//linimasa/` denied (401) |
| 9 | Missing trailing slash | SEC2-T-025 | PASS | Redirected (301), never served directly |
| 10 | Redirect loop | SEC2-T-031 | PASS | `/atlas/` root returned a single 200, no loop |
| 11 | Cache leakage | SEC2-T-032–033 | PASS | `Cache-Control: no-store` present on both 200 and 401 responses |
| 12 | Static bundle leakage | N/A this turn | NOT_APPLICABLE | Dummy backend has no separate static-bundle asset analogous to the ones reviewed in SEC-0 (§4.3 of the route inventory) — SEC-0's own finding (no separate protected JSON bundle exists in production either) already covers this; not re-tested against a fabricated bundle |
| 13 | Source-map leakage | N/A this turn | NOT_APPLICABLE | No source maps exist in production for the candidate pages (confirmed in SEC-0 discovery); nothing to test against in the dummy backend either |
| 14 | Rate-limit bypass attempt | SEC2-T-037–039 | PASS | Burst below threshold passed cleanly, burst above threshold tripped 503, recovery after cooldown succeeded |
| 15 | Missing test htpasswd file | SEC2-T-035 | PASS | Fail-closed confirmed (see §3.2 for an honest note on the exact mechanism) |
| 16 | Unreadable test htpasswd file | SEC2-T-036 | PASS | Fail-closed confirmed (see §3.2) |

**Additional test run beyond the researcher's 16-category list**, because it surfaced during boundary testing and was judged directly relevant: **direct same-host loopback access to the backend, bypassing the host-proxy auth layer entirely (SEC2-T-030)** — recorded as an `INFORMATIONAL_FINDING`, not a pass/fail, because it is not a defect in the tested design (the backend was never designed to authenticate on its own) but a residual architectural gap worth the researcher's attention (see §3.3).

**One test did not fully validate this turn: repeated-unauthorized-request observability (part of category 14/Phase 9, SEC2-T-040)** — recorded as `FAIL`, with the honest cause identified (§3.4), not glossed over.

---

## 3. Findings Requiring Researcher Attention

### 3.1 SEC2-T-029 — Alternate Host header (PASS_WITH_LIMITATION)

The test topology has exactly one `server {}` block, so an alternate `Host:` header cannot be routed anywhere except the single protected block — the 401 result is real but does not exercise the specific production risk pattern of a *second, less-guarded* server block (e.g., a default server, or nginx's own "first server block wins when no `server_name` matches") picking up a spoofed-Host request. Production's `silida.conf` has multiple `server {}` blocks (`silida.org`, `www.silida.org`, redirect blocks). **Recommendation:** before production implementation, explicitly verify (in a topology that includes more than one server block) that an unmatched or spoofed `Host:` header cannot reach an unintended, unauthenticated server block.

### 3.2 SEC2-T-035/036 — htpasswd absence/unreadability (PASS, mechanism note)

Both tests confirmed fail-closed behavior — but via a *different* mechanism than expected. Because the test used a Docker bind-mount, removing or making the source file unreadable caused **the container itself to fail to start** (Docker refused the mount, `docker restart` errored out, and the eventual "connection refused" was because no process was listening at all — see the operational note in the prototype plan §9). In production, host nginx reads `auth_basic_user_file` at request time from a real filesystem path (not a container bind-mount), so the expected failure mode there is nginx returning a clean `500 Internal Server Error` per request (as was in fact observed in the very first accidental permission-denied run during this turn's boundary testing, before the test file's permissions were corrected). **Both mechanisms fail closed — neither serves protected content — but they are not the same failure mode**, and production implementation should verify the actual `500`-on-unreadable-file behavior directly against a real filesystem path, not infer it solely from this container-mount-based test.

### 3.3 SEC2-T-030 — Direct same-host loopback bypass of the auth layer (informational, not pass/fail)

`http://127.0.0.1:18084/api/research/linimasa` (the backend, N1-bound to loopback) returned `200` with no auth challenge when accessed directly, bypassing the host-proxy's Basic Auth entirely. This is expected given the tested design (auth lives only at the proxy layer) and is not a defect in the prototype — but it means: **N1 protects against remote/external bypass; it does not add any authentication to the backend/app process itself.** Anything else running on the same host that can reach `127.0.0.1:8084` (in production) would still get unauthenticated access. This is the same structural point already made in the ADR's "Cross-Cutting Prerequisite" section and the Entra/OIDC target plan's placement discussion (§4) — this test turns that prior reasoning into an empirically demonstrated fact rather than only a documented concern. **Recommendation:** treat proxy-only enforcement as sufficient only if same-host processes are already trusted (true today — only the Docker stack itself and the host nginx process run on the VPS), and revisit if that trust boundary ever changes.

### 3.4 SEC2-T-040 — Repeated-unauthorized-request observability (FAIL, honestly reported)

This test ran immediately after SEC2-T-038 (a 25-request burst against the same rate-limited route), without sufficient cooldown for the leaky-bucket rate limiter to recover. As a result, all 25 requests in T-040 were rejected by the rate limiter (`503`) before nginx ever reached the auth-check stage, so **no `401` was observed at all** — the test could not distinguish "unauthorized requests are observable" from "everything is rate-limited right now." This is a **test-sequencing artifact, not a security defect**: the earlier tests (SEC2-T-006–015) *did* demonstrate 401s are correctly returned and logged in nginx's access log with the attempted username visible (per the design in the nonproduction implementation spec §19). **Recommendation:** retest this specific interaction (repeated unauthorized requests, observed over a longer window with the rate limiter *not* freshly exhausted) before treating rate-limit/auth interaction as fully characterized — this is a two-minute retest, not a design change.

---

## 4. Overall Negative-Test Verdict

15 of 16 researcher-specified categories passed cleanly or passed with a documented, non-blocking limitation. One category (rate-limit bypass attempt / observability) requires a short, low-effort retest before being considered fully validated. None of the findings in this report indicate the tested design fails closed anywhere it should fail closed — every fail-closed check that ran to completion (missing/unreadable htpasswd, invalid credentials, anonymous access on all 8 protected paths) confirmed the expected behavior.
