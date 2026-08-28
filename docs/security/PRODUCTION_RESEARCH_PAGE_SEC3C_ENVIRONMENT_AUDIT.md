# Production Research Page — SEC-3C Environment Audit

> **This document records the Phase 1 host preflight and the honest limits of what environment was actually tested.**

---

## 1. Host Identity

```text
hostname:        palito
uname -a:        Linux palito 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC ...
/proc/version:   contains "microsoft" -- confirmed WSL2
/etc/os-release: PRETTY_NAME="Ubuntu 24.04.4 LTS"
uptime:          up 3h40m at the time of this turn
```

**This is the same host SEC-3B ran on.** No SEC-3C tooling in this session has access to a second, genuinely separate WSL/Linux machine, nor to any mechanism for provisioning a disposable staging VPS. The only other SSH-reachable host in this session is `westkust-prod`, which is explicitly and correctly excluded as an experimental test bed.

## 2. Method Selection (C1 vs C3)

| Option | Status | Reason |
|---|---|---|
| C1 — native Nginx on this WSL/Linux host | **`C1_NATIVE_NGINX: NOT_EXECUTED`** — reason: `NATIVE_NGINX_UNAVAILABLE_AND_SUDO_NOT_AUTHORIZED` | `nginx` is not installed (`apt-cache policy nginx` shows candidate `1.24.0-2ubuntu7.17`, installed: none); installing or operating it requires `sudo`, and `sudo apt-get install -y nginx` failed with `sudo: a password is required` — no interactive terminal is available to this session's tools to supply one, and automatic package installation was not separately authorized. **Not executed, not FAIL** — no native-Nginx test outcome exists to report. |
| C3 — disposable Nginx container on this host | **Executed** | Docker `29.4.0` was already available (proven working throughout SEC-2A/SEC-3/SEC-3A/SEC-3B); no new dependency installation was required, consistent with the instruction's "do not modify the base host unnecessarily". Based on `nginx:1.25-alpine`; `limit_req_zone`/`limit_req` directives were accepted by the parser without error; enforcement was not observable. This result is consistent with SEC-3B's finding on the same host and does **not** prove native Nginx would also fail — that remains untested. |

```text
This C3 execution ran on a DIFFERENT EXECUTION INSTANCE ON THE SAME
UNDERLYING WSL2 HOST as SEC-3B (new container, new network, new zone name,
new port) -- not a genuinely different host. This distinction is stated
explicitly rather than left ambiguous.
```

## 3. Module and Build Verification

```text
nginx image:              nginx:1.25-alpine (same image used in every prior SEC-2A/SEC-3/SEC-3A/SEC-3B attempt)
ngx_http_limit_req_module: built into mainline nginx by default -- not an optional compile-time
                            module requiring separate verification via `nginx -V` flags; its
                            presence is implicit in every stock nginx build, and its directives
                            (`limit_req_zone`, `limit_req`) were accepted without a config-parse
                            error in every one of the four attempts across this whole SEC-2A
                            through SEC-3C series
process user:              nginx worker runs as uid 101 inside the container's own namespace
                            (consistent with all prior turns)
existing Nginx processes:  none, before this turn's container was created
existing listening ports:  none in the 39xxx test range before this turn
system clock:              verified sane in SEC-3B's diagnostic (host clock advanced 2.0s in 2s
                            wall-clock); not re-verified this turn since the same host was used
                            and no new clock-related symptom was observed
```

## 4. What Ran

One disposable container (`sec3c_ctrl`), one disposable network (`sec3c_net`), one test port (`127.0.0.1:39200`), one uniquely-named zone (`sec3c_ctrl_zone_v1`, distinct from SEC-3B's `sec3b_ctrl_zone`), one uniquely-marked response body (`SEC3C_UNIQUE_MARKER_LIMITED_LOCATION_v1`, to positively confirm requests reached the intended location rather than a default/fallback route). Full test-by-test evidence: `PRODUCTION_RESEARCH_PAGE_SEC3C_TEST_RESULTS.csv`.

## 5. Result

```text
SEC3C-CTRL-001 (syntax):            PASS
SEC3C-CTRL-002 (reaches location):  PASS
SEC3C-CTRL-003 (first request):     PASS
SEC3C-CTRL-004 (enforcement):       FAIL -- 10/10 requests returned 200
SEC3C-CTRL-005 (error log record):  FAIL -- zero limiting events logged
SEC3C-CTRL-006 (zone freshness):    PASS

Fresh-zone hard gate: 4/6 PASS, 2/6 FAIL -- does not meet the required 6/6
```

Per the plan's own hard-stop rule, testing stopped here. `IP-007`, `IP-008`, and the spoofing/observability tests were not run.

## 6. Cleanup

```text
sec3c_ctrl container removed:  confirmed (docker rm -f)
sec3c_net network removed:     confirmed (docker network rm)
Test port (39200) listening:   none (ss -tln, no match)
Temporary workspace:           deleted (rm -rf /tmp/sec3c-rate-limit-<timestamp>/, confirmed absent)
Production uptime:             unchanged -- westkust-prod voc_nginx still "Up 6 weeks", no restart
Production port 8084:          unchanged, 0.0.0.0:8084 still listening
Production configuration:      unchanged -- no write command issued this turn against any
                                production path
```

## 7. Final Status

```text
PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_INVALID
```

Closing `SEC3-F-02` numerically requires a host this session cannot reach: either a native-Nginx-capable environment with `sudo` access, or a genuinely separate machine (disposable staging VPS) that this session has no provisioning mechanism for. This is disclosed as a tooling limitation of this session, not a security finding and not evidence about production's own rate limiting.
