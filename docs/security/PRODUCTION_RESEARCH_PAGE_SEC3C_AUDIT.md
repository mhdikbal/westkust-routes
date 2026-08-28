# Production Research Page — SEC-3C Audit

> **Phase:** SEC-3C completion record — Different-Host Deterministic Rate-Limit Closure attempt
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`, SEC-3 `7c0621d512c8574df7b9ca041577a1080ac7e618`, SEC-3A `2864fc28d958194883355e999f111ff7aa4114e8`, SEC-3B `92b10685e32318a262a3c64762993482d77947a6`

---

## 1. Scope

SEC-3C targeted exactly the same two prior limited results (`SEC3A-IP-007`, `SEC3A-IP-008`) as SEC-3B, this time attempting a genuinely different execution host per the researcher's instruction. It did not repeat the 20 real-Django tests, `APPEND_SLASH` tests, redirect tests, protected-page tests, Basic Auth dual-layer tests, credential-store tests, the Option A architecture review, account-provisioning review, or the full SEC-3/SEC-3A matrices.

## 2. Disclosure — No Different Host Was Actually Available

This is the central, load-bearing fact of this turn and is stated plainly rather than buried: **this session had no access to a host different from the one SEC-3B used.** The tool environment is a single WSL2 sandbox; the only other reachable host is `westkust-prod`, correctly excluded as a test bed. Full detail: `PRODUCTION_RESEARCH_PAGE_SEC3C_DIFFERENT_HOST_PLAN.md` § 1, `PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_AUDIT.md`.

Given that constraint, this turn attempted the closest available approximation to "different": native (non-Docker) Nginx, per the plan's own preferred `C1` option — which would have removed the Docker/cgroup layer as a variable even on the same host. This was **not possible**: no native `nginx` package is installed, and installing it requires `sudo` with an interactive password this session's tools cannot supply. The plan's own explicit fallback (`C3`, disposable container) was used instead.

## 3. What Happened

A fresh disposable container, network, uniquely-named zone (`sec3c_ctrl_zone_v1`), and uniquely-marked response body were built, distinct in every identifying detail from SEC-3B's `sec3b_ctrl_zone`. `SEC3C-CTRL-001` (syntax), `-002` (correct location reached), `-003` (first request succeeds), and `-006` (zone freshness) all `PASS`ed. `SEC3C-CTRL-004` (enforcement) and `SEC3C-CTRL-005` (error-log record of enforcement) both **`FAIL`**ed: 10/10 rapid requests against a `rate=1r/m`, no-burst policy all returned `200`, and the error log recorded zero limiting events — not merely a missing `429`, but no enforcement activity of any kind.

```text
Fresh-zone hard gate: 4/6 PASS -- does not meet the required 6/6
```

Per the plan's own hard-stop rule, `IP-007`, `IP-008`, and the spoofing/observability tests (20 tests total) were **not executed** and are recorded `BLOCKED`, not fabricated.

## 4. Result Distribution

```text
Total SEC-3C tests: 26
PASS:    4  (SEC3C-CTRL-001, -002, -003, -006)
FAIL:    2  (SEC3C-CTRL-004, -005)
BLOCKED: 20 (all IP-007/IP-008/SPOOF tests)
```

## 5. Closure Status

Per the closure rule (fresh-zone gate must be 6/6, plus IP-007 7/7, IP-008 7/7, spoofing 6/6, total 26/26), this is not met:

```text
SEC3C_ENVIRONMENT_HARD_GATE_FAILED
NO_VALID_NUMERIC_SUPERSESSION_PRODUCED

SEC3-F-02: OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST (unchanged, third consecutive attempt)
```

The original `SEC3A-IP-007`/`SEC3A-IP-008` result cells remain `PASS_WITH_LIMITATION`, **unmodified** by this turn. No supersession is claimed — recorded additively in `PRODUCTION_RESEARCH_PAGE_SEC3A_AUDIT.md`. SEC-3B's own `FAIL`/`BLOCKED` rows are likewise unmodified — SEC-3C does not rewrite SEC-3B's historical result, it adds a third independent data point via cross-reference in `PRODUCTION_RESEARCH_PAGE_SEC3B_AUDIT.md`.

### 5.1 Next-Environment Requirement

A future numeric closure requires one of:

```text
C1: native Nginx on a WSL/Linux host with authorized package installation
    and process control
C2: disposable staging VPS that is not westkust-prod
C3: containerized Nginx on a genuinely different host where the fresh-zone
    hard gate passes
```

Repeating the same containerized test on this present WSL2 host is **not** recommended — it has now been tried three times (SEC-3A, SEC-3B, SEC-3C) with the identical outcome. `westkust-prod` must not be used as an experimental rate-limit test bed under any of these options.

**Researcher's stated preference (this turn):** Option `C2` — a disposable staging VPS — is preferred over `C1`/further `C3` attempts, because it is a genuinely separate host, requires no production experimentation, can run native Nginx, is destroyable after evidence is obtained, and is closest to production's real Linux behavior. This preference is recorded here as guidance for the next environment decision; provisioning such a VPS is outside this session's own tooling and requires the researcher's separate action.

## 6. Secret and Privacy Scan

```text
NO_SECRET_PATTERN_MATCH
```

No username, password, hash, htpasswd entry, Authorization value, cookie, token, private key, client secret, or `.env` value appears in any of the six new outputs or the two audit additions. No `CLIENT_A`/`CLIENT_B` synthetic identities were exercised (the topology was never built, since the control gate failed first). The known infrastructure peer `10.1.10.126` is not newly referenced this turn beyond what SEC-3A already recorded.

## 7. Cleanup Confirmation

```text
sec3c_ctrl container removed:   confirmed
sec3c_net network removed:      confirmed
Test port (39200) listening:    none
Temporary workspace deleted:    confirmed (rm -rf, confirmed absent)
Production uptime:              unchanged -- voc_nginx "Up 6 weeks" across this turn
Production port 8084:           unchanged, 0.0.0.0:8084 still listening
Production configuration:       unchanged -- no write command issued this turn
```

## 8. Baseline Verification

| Item | Result |
|---|---|
| SEC-0 through SEC-3B committed evidence | unchanged (checksums re-verified against the SEC-3B commit at the start of this turn) |
| Production `docker-compose.yml` / `silida.conf` / `nginx/nginx.conf` | unchanged (not touched this turn) |
| Backend / Frontend / Database / Migrations | unchanged |
| Five ontology validators | Painan 23/23, Natal 28/28, Koto Tangah 34/34, Tiku 35/35, Sillida 32/32 — all PASS |
| Ontology decision-ledger working diff | unchanged — same fingerprint (`d2805d1...`) carried since an earlier turn |

## 9. Output Checksums (this turn)

```text
9332c568d78e15ebb1b633133441898997063e2dde37734f98c7e34fa629d73b  PRODUCTION_RESEARCH_PAGE_SEC3C_DIFFERENT_HOST_PLAN.md
9b5f4177bc745e7da08a5b24c213d0af2fa646d5d24f93da572ab4d639bcad2d  PRODUCTION_RESEARCH_PAGE_SEC3C_TEST_MATRIX.csv
52a53c5378200b7ec537e4874529c141cef3d87610b33064f2508f22ecc04acc  PRODUCTION_RESEARCH_PAGE_SEC3C_TEST_RESULTS.csv
204da70719e90099bf9435a4d66d02e85748352dba42870cb927f9b7850a8380  PRODUCTION_RESEARCH_PAGE_SEC3C_RATE_LIMIT_ANALYSIS.md
170d4ffd49e7d901a60cab1dc010248527042e5ecadcf8b7d3915ad2f2ec8c97  PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_AUDIT.md
```

---

## Final Status

```text
PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_INVALID
```

`SEC3-F-01` remains closed (untouched this turn). `SEC3-F-02` remains `OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST` after three independent attempts across SEC-3A, SEC-3B, and SEC-3C, all on the same host (no genuinely different host was ever accessible to this session). `SEC3-F-03` is unaffected. `SECURITY_ACCESS_CONTROL_GATE` remains `NOT_PASSED`. Production remains `NO_GO`, unchanged, and its production access page remains publicly reachable exactly as before — Basic Auth was never implemented, port 8084 was never touched. Closing `SEC3-F-02` numerically requires a host this session genuinely cannot reach, most plausibly a disposable staging VPS provisioned by the researcher outside this session's tooling.

### Note on an unrelated observation (not investigated, not in scope)

```text
Observed production presentation issue: recurring "API KEY REQUIRED"
watermark on the basemap, visible in a screenshot of the live /atlas/ page
referenced in the researcher's own message this turn.
Classification: OUT_OF_SCOPE_UI_CONFIGURATION_BACKLOG
```

This was observed visually only, from the researcher's own description — it was not investigated during SEC-3C, no map or tile-provider configuration was read or modified, and no map API key of any kind is recorded anywhere in this document set. No specific provider or missing credential is attributed to this observation without a separate, dedicated investigation — that attribution was not performed here. It has no relationship to `SEC3-F-02`'s closure and was not allowed to influence this turn's rate-limit scope. It is recorded here only so the observation is not lost, per the researcher's own instruction, and requires a separate scoped discovery turn if pursued.
