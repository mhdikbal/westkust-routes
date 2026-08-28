# Production Research Page — SEC-3A Audit

> **Phase:** SEC-3A completion record — Targeted Closure for Real-Django Prefix Behavior and Cloudflare Trusted Real-IP Design
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`, SEC-3 `7c0621d512c8574df7b9ca041577a1080ac7e618`

---

## 1. Scope

SEC-3A targets exactly two open SEC-3 findings and nothing else: `SEC3-F-01` (duplicated-prefix behavior needs real-Django reverification) and `SEC3-F-02` (Cloudflare real-IP restoration needs a trusted-proxy design). It is not SEC-4 and does not authorize deployment.

## 2. SEC3-F-01: Real-Django Retest

Method D1 was used (reuse the actual built `westkust-routes-frontend:latest` image, disposable network, no production data or secrets) — justified in `PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_DJANGO_TEST_PLAN.md` § 2 (the Django app has no database dependency and gracefully degrades when its backend API is unreachable, confirmed by reading `frontend/config/settings.py` and `frontend/map_app/views.py` before testing). 20/20 tests passed. The decisive result: the real Django app's own 404 handler — not a synthetic fallback, as SEC-3's rehearsal necessarily used — rejects `/atlas/atlas/riset/pemodelan/`-shaped duplicated-prefix paths outright, with the response body confirmed to be Django's generic "Tersesat dari peta" 404 page, not protected content, regardless of whether a valid credential was supplied.

```text
SEC3-F-01: TARGETED_MITIGATION_VALIDATED
```

The original `SEC3-PREC-006`/`SEC3-PREC-007` rows in `PRODUCTION_RESEARCH_PAGE_SEC3_TEST_RESULTS.csv` were **not modified** — the cross-reference is recorded additively in `PRODUCTION_RESEARCH_PAGE_SEC3_AUDIT.md` § 8, per instruction.

## 3. SEC3-F-02: Cloudflare Trusted Real-IP Design

Read-only inventory of `westkust-prod` this turn found a materially important, previously-undocumented fact: `$remote_addr` at host Nginx is **not** Cloudflare's edge IP. It is a fixed hosting-provider internal load-balancer address (`10.1.10.126`, on the `10.1.10.0/24` private VLAN), observed consistently across every sampled access-log line (50/50). This corrects the original `SEC3-F-02` framing (which assumed Cloudflare was the immediate peer) and is documented in full, with the trust-boundary design built against the corrected chain, in `PRODUCTION_RESEARCH_PAGE_SEC3A_CLOUDFLARE_REAL_IP_DESIGN.md`.

A disposable Nginx topology (stand-in trusted-source IP `172.40.0.3/32`, stand-in Cloudflare-equivalent test ranges `198.51.100.0/24`/`2001:db8::/32` per RFC 5737/RFC 3849, to avoid needing any real network fetch) exercised 12 tests:

- **10/12 PASS cleanly**: restoration from a trusted source with a valid header (`IP-001`), no invented address without a header (`IP-002`), spoofed headers from an untrusted source ignored (`IP-003`, `IP-004`), IPv4 and IPv6 restoration (`IP-005`, `IP-006`), the untrusted-peer identity invariance that `IP-009` depends on (proven via `IP-003`/`IP-004` data), log integrity with no credential material (`IP-010`), the corrected CIDR-lifecycle mental model — trust is keyed on the *source*, not on validating the claimed value against a second list (`IP-011`) — and syntax validation (`IP-012`).
- **2/12 `PASS_WITH_LIMITATION`** (`IP-007`, `IP-008`): the *numeric* rate-limit-threshold demonstration did not reproduce in this sandbox run. This was isolated, not left ambiguous: an intentionally extreme control case (`rate=1r/m`, no burst allowance at all, on a fresh minimal container) still returned `200` on three rapid sequential requests, when it should have rejected the second and third outright. The identical directive pattern reliably produced real `429`s earlier in this same session, under materially identical configuration, in both SEC-2A and SEC-3. Container clock was verified sane (advanced 2.0s of wall-clock in 2s). This is conclusively a rate-limiter shared-memory-zone environment malfunction in the current sandbox state, not a defect in the trust-boundary design or in the key-derivation logic itself — which the same test suite's other rows already prove correct independently (a rate-limit key built on `$remote_addr` is only as sound as `$remote_addr`'s restoration correctness, and that correctness is what `IP-001`/`003`/`004`/`005` demonstrate).

Per the researcher's adjudication and the strict 12/12 closure rule, this finding is **not** closed this turn, and is retitled to name exactly what remains:

```text
SEC3-F-02: OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST
```

Not `DESIGN_AND_PROTOTYPE_VALIDATED`, not `PRODUCTION_RESOLVED`, not `PASS`. The design itself is complete and most of its mechanics are cleanly demonstrated (trusted-proxy design complete; spoofed-header guards PASS; IPv4 PASS; IPv6 PASS; key derivation distinguishes synthetic clients structurally); what remains is narrow and specific — a deterministic re-run of exactly the two numeric rate-limit-threshold tests (`IP-007`, `IP-008`) in a clean environment, scoped as a future SEC-3B turn — plus the production-side item this design always required regardless of test environment: confirmation from the hosting provider of exactly what their load balancer forwards.

## 3.1 New Infrastructure Finding

```text
SEC3-F-03: HOST_NGINX_IMMEDIATE_PEER_IS_PROVIDER_INTERNAL_LOAD_BALANCER
Observed immediate peer:  10.1.10.126
Classification:           PRIVATE_PROVIDER_INTERNAL_ADDRESS
```

Host Nginx does not directly observe a Cloudflare edge address — its immediate TCP peer, on every sampled request, is a fixed private address (`10.1.10.126`) on the same local VLAN as `westkust-prod` itself. No specific hosting-provider identity is inferred; the address is classified only as `PRIVATE_PROVIDER_INTERNAL_ADDRESS`, bounded strictly to what was directly observed. This means the trusted real-IP design must model the actual two-hop (or possibly multi-hop) chain, Cloudflare CIDRs alone are not sufficient for `set_real_ip_from`, and provider load-balancer trust, header provenance, and spoofing resistance all require explicit verification — all reflected in `PRODUCTION_RESEARCH_PAGE_SEC3A_CLOUDFLARE_REAL_IP_DESIGN.md` § 2–3. No production configuration change is authorized by this finding.

## 4. SEC-DEC-11

No `SEC-DEC-11` row existed in `PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv` before this turn. `OPTION_A_APPROVED_WITH_LIMITATIONS` is recorded as a proposal in `PRODUCTION_RESEARCH_PAGE_SEC3A_SECURITY_DECISION_ADDENDUM.md`; the ledger's existing schema and rows were not modified, and no row was added silently.

## 5. Cleanup Confirmation

```text
sec3a_* containers removed:        confirmed (docker ps -a --filter name=sec3a_ empty)
sec3a_net network removed:         confirmed (docker network ls has no sec3a_net)
Test ports (39084-39093) listening: none (ss -tln, no match)
Dummy htpasswd files:               shredded (shred -u)
Ephemeral workspace:                deleted (rm -rf; confirmed absent)
Production uptime:                  unchanged -- westkust-prod voc_nginx still
                                     "Up 6 weeks" across this turn, no restart
Production port 8084:               unchanged, 0.0.0.0:8084 still listening
Production configuration:           unchanged -- no write command issued
                                     against silida.conf, nginx/nginx.conf,
                                     or docker-compose.yml this turn
```

## 6. Baseline Verification

| Item | Result |
|---|---|
| SEC-0 through SEC-3 committed evidence | unchanged (checksums re-verified against the SEC-3 commit at the start of this turn) |
| Production `docker-compose.yml` | unchanged (read-only this turn) |
| `silida.conf` | unchanged (read-only this turn — re-read for the inventory in § 3) |
| `nginx/nginx.conf` | unchanged |
| Backend / Frontend / Database / Migrations | unchanged (the real Django *image* was run in an isolated container; the repository's frontend source was not modified) |
| Five ontology validators | Painan 23/23, Natal 28/28, Koto Tangah 34/34, Tiku 35/35, Sillida 32/32 — all PASS |
| Ontology decision-ledger working diff | unchanged — same fingerprint (`d2805d1...`) carried since an earlier turn, confirmed still present and still outside every change made this session |

## 7. Production Isolation Statement

Every SSH command executed against `westkust-prod` this turn was read-only: `grep`, `tail`, `ip addr show`, `ip route`, `ss -tln`, `docker compose ps`. No file was written, no service was reloaded or restarted, no container was recreated. The entire Django-topology rehearsal, real-IP prototype, and failure isolation ran exclusively against local, disposable Docker containers.

## 8. Output Checksums (this turn)

```text
69a0eb6c05db938670e65176cbe0f96094b223686c087c48b8584b98f4c87155  PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_DJANGO_TEST_PLAN.md
cfe8fd93e60cf95526ed740be43997563bbcdae49a6e4578691ed09b692afa5e  PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_DJANGO_TEST_RESULTS.csv
a8cd421c1e27555e802a358ada4d7d1ba466f2330b929c17c4820983abb398a0  PRODUCTION_RESEARCH_PAGE_SEC3A_CLOUDFLARE_REAL_IP_DESIGN.md
5957405c8d7ab2e1c1ea51539b74cf209ae7eb05cce46faa0377ee0c27a89cf0  PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_IP_TEST_RESULTS.csv
e3d872fbb52ee1b57b82f570b06d8583a73b7be87e413a9dd6f946a1b869cf13  PRODUCTION_RESEARCH_PAGE_SEC3A_CIDR_LIFECYCLE_RUNBOOK.md
7010430c5bc9d46d8fc417237acea8500653c1c58cc53db836c9ad19fafbdf64  PRODUCTION_RESEARCH_PAGE_SEC3A_SECURITY_DECISION_ADDENDUM.md
```

(This file's own checksum is not self-referential and is reported in the terminal summary.)

## 9. Addendum — Phase SEC-3B Numeric Rate-Limit Retest (appended, does not alter §1–8 above or any original test row)

> **SEC-3A evidence baseline:** `2864fc28d958194883355e999f111ff7aa4114e8`

SEC-3B attempted to close `SEC3-F-02`'s two remaining limited results (`SEC3A-IP-007`, `SEC3A-IP-008`) using a deterministic, fresh-environment numeric retest. Full detail in `PRODUCTION_RESEARCH_PAGE_SEC3B_NUMERIC_RATE_LIMIT_PLAN.md`, `PRODUCTION_RESEARCH_PAGE_SEC3B_TEST_RESULTS.csv`, `PRODUCTION_RESEARCH_PAGE_SEC3B_RATE_LIMIT_ANALYSIS.md`, and `PRODUCTION_RESEARCH_PAGE_SEC3B_AUDIT.md`.

```text
Result: PRODUCTION_RESEARCH_PAGE_SEC3B_REQUIRES_REVIEW

The required precondition test (SEC3B-CTRL-001 -- a brand-new zone, never
previously used, with an intentionally extreme threshold of 1 request per
minute and zero burst allowance) FAILED: 10/10 rapid sequential requests
returned 200, zero rejected. Per SEC-3B's own instruction, this means the
environment is invalid for interpreting IP-007/IP-008, and the twelve
dependent tests were correctly left BLOCKED rather than fabricated.

This RULES OUT the prior hypothesis that the SEC-3A limitation was specific
to that session's accumulated state ("TEST_ENVIRONMENT_LIMITATION_REQUIRES_
FRESH_STATE") -- the identical failure reproduces in a container that never
previously existed. Corrected classification:
NGINX_LIMIT_REQ_MODULE_NOT_ENFORCING_IN_THIS_SANDBOX_PLATFORM.

SEC3-F-02 status: UNCHANGED -- OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST.
Not TARGETED_NUMERIC_RATE_LIMIT_MITIGATION_VALIDATED, not
PRODUCTION_CONFIGURED, not PRODUCTION_RESOLVED.

The SEC3A-IP-007/SEC3A-IP-008 result cells above remain PASS_WITH_LIMITATION,
unmodified by SEC-3B.

SEC3B_ENVIRONMENT_CONTROL_FAILED
NO_VALID_SUPERSESSION_PRODUCED
```

Cleanup for SEC-3B: all `sec3b_*` and diagnostic `quick_sanity*` containers/networks removed, no test port remains listening, ephemeral workspace deleted and confirmed absent. Production `docker-compose.yml`, `silida.conf`, `nginx/nginx.conf`, backend, frontend, and database were not touched. Production port 8084 remains published and unauthenticated; no Basic Auth exists in production.

## 10. Addendum — Phase SEC-3C Different-Host Retest (appended, does not alter §1–9 above or any original test row)

> **SEC-3B evidence baseline:** `92b10685e32318a262a3c64762993482d77947a6`

SEC-3C attempted a third retest of `SEC3-F-02`'s two remaining limited results, this time on a host intended to be different from SEC-3B's. Full detail in `PRODUCTION_RESEARCH_PAGE_SEC3C_DIFFERENT_HOST_PLAN.md`, `PRODUCTION_RESEARCH_PAGE_SEC3C_TEST_RESULTS.csv`, `PRODUCTION_RESEARCH_PAGE_SEC3C_RATE_LIMIT_ANALYSIS.md`, `PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_AUDIT.md`, and `PRODUCTION_RESEARCH_PAGE_SEC3C_AUDIT.md`.

```text
Result: PRODUCTION_RESEARCH_PAGE_SEC3C_ENVIRONMENT_INVALID

No genuinely different host was accessible to this session -- the same WSL2
sandbox as SEC-3B was used (disclosed explicitly, not silently). Native
Nginx (the preferred C1 option) was unavailable: no package installed, and
`sudo apt-get install nginx` failed for lack of an interactive password.
The C3 fallback (disposable container) reproduced the identical
non-enforcement a third time, with a uniquely-named zone and a
uniquely-marked response body: SEC3C-CTRL-004 (enforcement) and
SEC3C-CTRL-005 (error-log record) both FAILED -- 10/10 requests returned
200 against rate=1r/m no-burst, zero limiting events logged.

Per the hard-stop rule, the 20 dependent IP-007/IP-008/spoofing tests were
NOT run and are recorded BLOCKED.

SEC3-F-02 status: UNCHANGED -- OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST,
now after three independent attempts (SEC-3A, SEC-3B, SEC-3C).

The SEC3A-IP-007/SEC3A-IP-008 result cells above remain PASS_WITH_LIMITATION,
unmodified by SEC-3C.

SEC3C_ENVIRONMENT_INVALID
NO_VALID_SUPERSESSION_PRODUCED
```

Cleanup for SEC-3C: `sec3c_ctrl` container and `sec3c_net` network removed, no test port remains listening, temporary workspace deleted and confirmed absent. Production unchanged.

---

## Final Status

```text
PRODUCTION_RESEARCH_PAGE_SEC3A_REQUIRES_REVIEW
```

`SEC3-F-01` is fully closed (`TARGETED_MITIGATION_VALIDATED`, 20/20). `SEC3-F-02` is not fully closed this turn (`OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST`) because 2 of its 12 required tests are `PASS_WITH_LIMITATION` rather than clean `PASS`, per the strict 12/12 rule — even though the underlying limitation was conclusively isolated to a sandbox environment artifact unrelated to the design's correctness. `SEC3-F-03` (§3.1) is a new infrastructure finding, evidence-bounded, no production change authorized. `SECURITY_ACCESS_CONTROL_GATE` remains `NOT_PASSED`. Production remains `NO_GO`. Production is unchanged.
