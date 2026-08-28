# Production Research Page — SEC-3B Audit

> **Phase:** SEC-3B completion record — Deterministic Numeric Rate-Limit Closure attempt for `SEC3A-IP-007`/`SEC3A-IP-008`
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`, SEC-3 `7c0621d512c8574df7b9ca041577a1080ac7e618`, SEC-3A `2864fc28d958194883355e999f111ff7aa4114e8`

---

## 1. Scope

SEC-3B targeted exactly two prior limited results (`SEC3A-IP-007`, `SEC3A-IP-008`) and nothing else. It did not repeat the 20 real-Django tests, duplicated-prefix tests, `APPEND_SLASH` tests, redirect tests, relative-link tests, the credential-store rehearsal, the full SEC-3/SEC-3A matrices, the Option A architecture review, account-provisioning design, or Entra/OIDC design.

## 2. What Happened

Before building the full `CLIENT_A`/`CLIENT_B` topology, this turn ran the required fresh-zone control test (`SEC3B-CTRL-001`) first, per the instruction's own sequencing. A brand-new Docker network and container, never previously used, with an intentionally extreme threshold (`rate=1r/m`, no burst — one request per minute, zero tolerance), was sent 10 rapid sequential requests. **All 10 returned `200`. Zero were rejected.**

This conclusively rules out the prior turn's working hypothesis (that the limitation was specific to that session's accumulated state and would clear with a fresh environment). Full detail and the corrected root-cause classification: `PRODUCTION_RESEARCH_PAGE_SEC3B_RATE_LIMIT_ANALYSIS.md`.

```text
SEC3B-CTRL-001: FAIL
```

Per the instruction's own explicit contingency for this exact outcome — "if the fresh-zone control does not enforce: do not interpret IP-007/IP-008; classify the environment as invalid; stop with SEC3B_REQUIRES_REVIEW" — the twelve dependent `CLIENT_A`/`CLIENT_B` and spoofing-control tests (`SEC3B-IP-007A..D`, `SEC3B-IP-008A..D`, `SEC3B-SPOOF-001..004`) were **not executed** and are recorded `BLOCKED`, not fabricated as `PASS` or silently omitted.

## 3. Result Distribution

```text
Total SEC-3B tests: 16
PASS:    1  (SEC3B-CTRL-004 -- zone freshness itself was genuinely achieved)
FAIL:    3  (SEC3B-CTRL-001, -002, -003 -- enforcement did not occur)
BLOCKED: 12 (all IP-007/IP-008/SPOOF tests -- correctly not run against an invalid environment)
```

## 4. Closure Status

Per the closure rule (all of `SEC3B-IP-007A..D`, `SEC3B-IP-008A..D`, `SEC3B-CTRL-001..004`, `SEC3B-SPOOF-001..004` must `PASS`), this is not met:

```text
SEC3-F-02: OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST (unchanged)
```

Not `TARGETED_NUMERIC_RATE_LIMIT_MITIGATION_VALIDATED`, not `PRODUCTION_CONFIGURED`, not `PRODUCTION_RESOLVED`, not `SECURITY_GATE_PASSED`.

The original `SEC3A-IP-007`/`SEC3A-IP-008` result cells in `PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_IP_TEST_RESULTS.csv` remain `PASS_WITH_LIMITATION`, **unmodified** by this turn. The cross-reference is recorded additively in `PRODUCTION_RESEARCH_PAGE_SEC3A_AUDIT.md` as `SEC3B_ENVIRONMENT_CONTROL_FAILED` / `NO_VALID_SUPERSESSION_PRODUCED` — not by editing those cells, and not as `SUPERSEDED_BY_SEC3B_DETERMINISTIC_RETEST`, since no valid deterministic retest was produced.

## 4.1 SEC-3C Recommendation

Since this sandbox is now confirmed, twice, to have an inert `limit_req` mechanism regardless of session freshness, threshold, or zone novelty, closing `SEC3-F-02` numerically requires moving the retest to a **different** execution environment. A narrow `SEC-3C` turn is recommended, scoped identically to SEC-3B (exactly `IP-007`/`IP-008`, nothing else), on one of:

```text
C1 (preferred): an isolated native Nginx install on a nonproduction Linux
                or WSL host outside this sandbox
C2 (alternative): a disposable staging VPS provisioned specifically for
                   this test, torn down afterward
C3 (alternative): a containerized Nginx on a different host where the
                   fresh-zone control is confirmed to actually pass first
```

Explicitly prohibited for `SEC-3C`, carried forward from this turn's own boundaries:

- using production host Nginx as the experimental test bed;
- changing production rate limits for experimentation;
- testing against real users or real traffic;
- using production credentials.

`SEC-3C` must begin with the identical minimal fresh-zone enforcement control used this turn (`rate=1r/m`, no burst, brand-new zone) **before** attempting `IP-007`/`IP-008`. If that control fails again, on a genuinely different host, `SEC-3C` must stop immediately without running the dependent tests — the same discipline this turn followed.

## 5. Secret and Privacy Scan

```text
NO_SECRET_PATTERN_MATCH
```

No username, password, hash, htpasswd entry, Authorization value, cookie, token, private key, client secret, or `.env` value appears in any of the five new outputs or the SEC-3A audit addition. Only synthetic documentation-range addresses were referenced in the plan (none were actually exercised, since the control test failed before the `CLIENT_A`/`CLIENT_B` topology was built). The known infrastructure peer `10.1.10.126` is referenced only as the already-recorded `PRIVATE_PROVIDER_INTERNAL_ADDRESS` from `SEC3-F-03`, with no new inference added.

## 6. Cleanup Confirmation

```text
sec3b_ctrl container removed:  confirmed (docker rm -f)
sec3b_net network removed:     confirmed (docker network rm)
Test port (39100) listening:   none (ss -tln, no match)
Diagnostic sanity containers
  (quick_sanity, 2, 3, 4)
  removed:                     confirmed (all docker rm -f)
Temporary configs deleted:     confirmed (/tmp/*.conf removed)
Ephemeral workspace:           deleted (rm -rf; confirmed absent)
Production uptime:             unchanged -- westkust-prod voc_nginx still
                                "Up 6 weeks" across this turn, no restart
Production port 8084:          unchanged, 0.0.0.0:8084 still listening
Production configuration:      unchanged -- no write command issued this
                                turn against any production path
```

## 7. Baseline Verification

| Item | Result |
|---|---|
| SEC-0 through SEC-3A committed evidence | unchanged (checksums re-verified against the SEC-3A commit at the start of this turn) |
| Production `docker-compose.yml` / `silida.conf` / `nginx/nginx.conf` | unchanged (not read or written this turn — SEC-3B's diagnostics used only local disposable containers) |
| Backend / Frontend / Database / Migrations | unchanged |
| Five ontology validators | Painan 23/23, Natal 28/28, Koto Tangah 34/34, Tiku 35/35, Sillida 32/32 — all PASS |
| Ontology decision-ledger working diff | unchanged — same fingerprint (`d2805d1...`) carried since an earlier turn |

## 8. Production Isolation Statement

No SSH command was issued against `westkust-prod` to write anything this turn; the two read-only status checks (container status, port 8084 listening state) confirmed no change. The entire control-test attempt and diagnostic sequence ran exclusively against local, disposable Docker containers and networks, all removed before this report was written.

## 9. Output Checksums (this turn)

```text
2b78979c9cef12778ba6fa423889f114add5d6a77ee38ab041ee770385f67b82  PRODUCTION_RESEARCH_PAGE_SEC3B_NUMERIC_RATE_LIMIT_PLAN.md
322617f65d58c5f0707ee06a98cff4c3fbe346eaa5532de993ecf6dfb926701f  PRODUCTION_RESEARCH_PAGE_SEC3B_TEST_MATRIX.csv
6037c3a7c5be101e1fe8ea806d5fdcc6e05e5f7aaea8f0b176d8b8e1eb7b9d53  PRODUCTION_RESEARCH_PAGE_SEC3B_TEST_RESULTS.csv
c9ae541df211de597185a279aa032162a2e05630cd0f20b5c5f3ff2a5796e6a3  PRODUCTION_RESEARCH_PAGE_SEC3B_RATE_LIMIT_ANALYSIS.md
```

---

## 10. Addendum — Phase SEC-3C Different-Host Retest (appended, does not alter §1–9 above or any original test row)

> **SEC-3B result preserved as-is; not rewritten by SEC-3C.**

SEC-3C attempted the recommended different-host retest. No genuinely different host was accessible to the session that ran it — this is disclosed in full in `PRODUCTION_RESEARCH_PAGE_SEC3C_DIFFERENT_HOST_PLAN.md` § 1. Native Nginx (preferred) was unavailable for lack of `sudo`; the container fallback, on the same underlying host as this SEC-3B run, reproduced the identical non-enforcement a third time. Full detail: `PRODUCTION_RESEARCH_PAGE_SEC3C_AUDIT.md`.

```text
SEC3C_ENVIRONMENT_INVALID
NO_VALID_SUPERSESSION_PRODUCED
```

This SEC-3B turn's own `FAIL`/`BLOCKED` rows above remain exactly as recorded — SEC-3C does not supersede or rewrite them, it adds a third, independent, cross-referenced data point.

---

## Final Status

```text
PRODUCTION_RESEARCH_PAGE_SEC3B_REQUIRES_REVIEW
```

`SEC3-F-01` remains closed (untouched this turn). `SEC3-F-02` remains `OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST` — the fresh-zone control test that would have justified proceeding to the numeric `CLIENT_A`/`CLIENT_B` evidence failed, cleanly and reproducibly, ruling out session staleness as the cause. `SEC3-F-03` is unaffected and remains recorded as-is. `SECURITY_ACCESS_CONTROL_GATE` remains `NOT_PASSED`. Production remains `NO_GO`. Production is unchanged. Closing this finding requires a working `limit_req`-enforcing test environment, not available to this session.
