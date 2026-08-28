# Production Research Page — SEC-3C Different-Host Rate-Limit Closure Plan

> **Phase:** SEC-3C — attempted different-host retest of `SEC3-F-02`'s numeric evidence gap.
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`, SEC-3 `7c0621d512c8574df7b9ca041577a1080ac7e618`, SEC-3A `2864fc28d958194883355e999f111ff7aa4114e8`, SEC-3B `92b10685e32318a262a3c64762993482d77947a6`

---

## 1. Honest Disclosure Before Anything Else

**This turn did not have access to a genuinely different physical or virtual host.** The tool environment available to this session is a single WSL2 sandbox (hostname `palito`, kernel `6.18.33.2-microsoft-standard-WSL2`, Ubuntu 24.04.4). This is the **same host** SEC-3B ran on — there is no mechanism available to this session to provision a separate VPS or reach a different WSL/Linux machine. `westkust-prod` was correctly not used (explicitly prohibited). This is disclosed here, first, rather than silently proceeding and letting the reader infer a different host was used.

Given that constraint, this turn attempted the next-most-different thing actually available: **native (non-Docker) Nginx**, per the plan's own preferred `C1` option, since removing the Docker container/cgroup layer at least changes one variable versus SEC-3B's fully-containerized approach.

## 2. Host Preflight (Phase 1)

| Item | Value |
|---|---|
| Host type | WSL2 (confirmed via `/proc/version` containing `microsoft`) |
| OS | Ubuntu 24.04.4 LTS (Noble Numbat) |
| Kernel | `6.18.33.2-microsoft-standard-WSL2` |
| Native Nginx | **not installed** (`apt-cache policy nginx` shows candidate `1.24.0-2ubuntu7.17`, installed: none) |
| `sudo` | **not available without an interactive password** (`sudo: a password is required`) — `apt-get install nginx` could not be run |
| Docker | available, `29.4.0` |
| `ngx_http_limit_req_module` | built into mainline `nginx` (not an optional module needing separate compilation) — present in the `nginx:1.25-alpine` image already used throughout SEC-2A/SEC-3/SEC-3A/SEC-3B |

**Consequence:** `C1` (native Nginx) is unavailable — genuinely, not by choice, per the same "do not install a package automatically" instruction that governed this decision. Per the instruction's own fallback path, `C3` (disposable container) was used instead, since Docker was already available and no new dependency installation was required.

## 3. What This Means for the Result

Because `C3` on this host uses the identical container runtime, kernel, and cgroup configuration that SEC-3B's `C3` attempt used, **a failure here does not add new evidence that the underlying cause is container-specific** (SEC-3B already suspected this was not purely a Docker artifact, since the failure persisted across multiple different container/network combinations). What this turn *can* still validate is whether the specific `SEC3C-CTRL-*` methodology (a differently-named zone, a uniquely-marked location, explicit error-log-level enforcement) changes the observed outcome on this same host — it does not, as recorded in `PRODUCTION_RESEARCH_PAGE_SEC3C_TEST_RESULTS.csv`.

## 4. Result

```text
SEC3C-CTRL-004: FAIL (10/10 requests returned 200 against rate=1r/m, no burst)
SEC3C-CTRL-005: FAIL (error log recorded zero limiting events)
```

Per the plan's own explicit hard-stop rule, `IP-007`, `IP-008`, and the spoofing/observability tests were **not run**. Full detail: `PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_AUDIT.md` and `PRODUCTION_RESEARCH_PAGE_SEC3C_RATE_LIMIT_ANALYSIS.md`.

```text
PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_INVALID
```

`SEC3-F-02` remains open.
