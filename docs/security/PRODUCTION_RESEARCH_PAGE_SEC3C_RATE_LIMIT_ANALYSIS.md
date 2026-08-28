# Production Research Page — SEC-3C Rate-Limit Analysis

> **Analysis of a second, different-methodology environment failure on the same host. No production rate-limit conclusion is drawn.**

---

## 1. What Was Observed

| Turn | Host | Execution model | Zone | Threshold | Result |
|---|---|---|---|---|---|
| SEC-2A | this WSL2 host | Docker container | ad hoc | `2r/s burst=3 nodelay` | **Enforced correctly** |
| SEC-3 | this WSL2 host | Docker container | production `api_limit` zone reused | `60r/m burst=20 nodelay` | **Enforced correctly** |
| SEC-3A | this WSL2 host | Docker container | ad hoc, then extreme control | `1r/s` → `1r/m`, no burst | **Did not enforce** |
| SEC-3B | this WSL2 host | Docker container, brand-new network/container | `sec3b_ctrl_zone` | `1r/m`, no burst | **Did not enforce** |
| SEC-3C (this turn) | **the same WSL2 host** (no different host was accessible) | Docker container (native Nginx unavailable — no `sudo`) | `sec3c_ctrl_zone_v1` | `1r/m`, no burst | **Did not enforce** |

## 2. Root-Cause Status — Unchanged, With One New Constraint Identified

SEC-3B corrected the classification from "stale session state" to `NGINX_LIMIT_REQ_MODULE_NOT_ENFORCING_IN_THIS_SANDBOX_PLATFORM`, evidence-bounded to the sandbox tested. This turn attempted to test whether that classification was specific to *containerized* Nginx specifically (as opposed to something host-wide), by trying `C1` (native, non-Docker Nginx) first. **That attempt could not be completed**: this WSL2 host has no native `nginx` installed, and installing it requires `sudo`, which requires an interactive password not available to this session's tools. This is a genuine tooling constraint, not a design choice.

Falling back to `C3` (disposable container, per the plan's own explicit fallback path) reproduced the identical failure a third time, with a uniquely-named zone, a uniquely-marked response body (to rule out any possibility of hitting the wrong location), and explicit error-log-level enforcement checking (to rule out "429 wasn't returned but limiting still happened silently" — it did not; the error log recorded zero limiting events of any kind).

```text
Classification (SEC-3C, bounded to this turn's exact tested scope):
CONTAINERIZED_NGINX_LIMIT_REQ_ENFORCEMENT_NOT_OBSERVABLE_ON_CURRENT_WSL2_HOST
```

This classification is deliberately narrower than SEC-3B's own `NGINX_LIMIT_REQ_MODULE_NOT_ENFORCING_IN_THIS_SANDBOX_PLATFORM` — it is bounded to exactly what SEC-3C tested: the `nginx:1.25-alpine` container image, the current WSL2 host, and this turn's specific disposable topology. It does **not** claim:

- native Nginx on WSL2 would also fail (never tested — `sudo` was unavailable);
- Nginx `limit_req` is universally defective (it worked correctly earlier in this series, in SEC-2A and SEC-3);
- production Nginx rate limiting cannot work;
- trusted real-IP restoration is defective (independently proven correct by SEC-3A's `IP-001`/`003`/`004`/`005`);
- `$binary_remote_addr` is an invalid rate-limit key.

This is **not** upgraded to a host-wide or kernel-wide claim, because the native-Nginx variant that would have tested that specifically could not be run. What SEC-3C adds is: the failure is not an artifact of any single container, network, zone name, or response mechanism tried so far — three independent container instances, three different zone names, and one intentionally unique response marker have all shown the same non-enforcement.

## 3. Why a Genuinely Different Host Was Not Used

Disclosed in full in `PRODUCTION_RESEARCH_PAGE_SEC3C_DIFFERENT_HOST_PLAN.md` § 1 and `PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_AUDIT.md`: this session's tool access is confined to one WSL2 sandbox and (via SSH, explicitly prohibited as an experimental test bed) `westkust-prod`. No mechanism to provision a disposable staging VPS is available to this session. Reaching a genuinely different host requires either the user provisioning one and granting access, or a future session with different tooling.

## 4. Consequence

Per the plan's own hard-stop rule, `IP-007`, `IP-008`, and the spoofing/observability tests were not run, and are recorded `BLOCKED`, not fabricated. `SEC3-F-02` remains open.

```text
PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_INVALID
```

## 5. Rate-Limit Key Recommendation (unaffected)

Unchanged from SEC-3A/SEC-3B:

```text
$binary_remote_addr, after validated trusted real-IP restoration
Recommendation status: RECOMMENDED_WITH_LIMITATIONS
```

Required limitations (restated for SEC-3C traceability, unchanged from prior turns):

- trust only explicit immediate proxy addresses;
- production provider-load-balancer trust identity must be verified (`SEC3-F-03`: immediate peer `10.1.10.126`, classified only as `PRIVATE_PROVIDER_INTERNAL_ADDRESS`);
- direct client headers must be ignored;
- IPv4 and IPv6 design required;
- N1 containment required;
- production threshold separately approved;
- numeric bucket behavior still requires a working test environment — not yet obtained across three attempts (SEC-3A, SEC-3B, SEC-3C);
- production logs should retain both immediate and restored identity fields;
- privacy review applies to retained client-IP data;
- provider/CIDR lifecycle maintained (`PRODUCTION_RESEARCH_PAGE_SEC3A_CIDR_LIFECYCLE_RUNBOOK.md`).

This recommendation is **not implemented in production** and remains numerically unverified.
