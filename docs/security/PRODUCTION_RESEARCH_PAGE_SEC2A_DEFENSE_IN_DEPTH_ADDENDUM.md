# Production Research Page — SEC-2A Defense-in-Depth Addendum

> **Phase:** SEC-2A — Rate-Limit Retest and Same-Host Loopback Defense-in-Depth Prototype
> **Parent security-planning baseline:** `e813192b590917a7f96b9e3ca7da5c8c9a907be8`
> **SEC-2 evidence baseline:** `38120d250a2b629e86a6c66d0d4be7d0851117b5`
> **All tests non-destructive, run only against a new, disposable ephemeral test workspace.**

---

## 1. Scope

This addendum records Phase SEC-2A: (a) a deterministic retest of the SEC-2 rate-limit observability gap (original `SEC2-T-040`, `FAIL` due to a test-sequencing artifact), and (b) a second, independent nonproduction prototype validating a two-layer ("defense-in-depth") Basic Auth boundary intended to mitigate `SEC2-T-030` — same-host loopback access to the inner upstream bypassing authentication entirely. It is strictly additive: it does not delete, renumber, or rewrite any original SEC-2 evidence row or file content.

## 2. Authoritative Baselines

```text
PARENT_SECURITY_PLANNING_BASELINE: e813192b590917a7f96b9e3ca7da5c8c9a907be8
SEC2_EVIDENCE_BASELINE:            38120d250a2b629e86a6c66d0d4be7d0851117b5
```

Both were re-verified at the start of this turn: local HEAD, `origin/main`, `git ls-remote`, and the `westkust-prod` server HEAD/`origin/main` all matched `38120d2...`; local/server checksums of the six original SEC-2 files matched byte-for-byte; the eleven SEC-0/SEC-1 files were unchanged versus `e813192b`; the ontology decision-ledger working diff fingerprint (`d2805d1...`) was unchanged and remained outside this work; all five ontology validators passed (Painan 23/23, Natal 28/28, Koto Tangah 34/34, Tiku 35/35, Sillida 32/32).

## 3. Original SEC-2 Result

```text
43 total tests
40 PASS
1 PASS_WITH_LIMITATION  — SEC2-T-029 (alternate Host header, single-server-block topology limitation)
1 INFORMATIONAL_FINDING — SEC2-T-030 (same-host loopback bypass, architectural, not a defect in the tested design)
1 FAIL                  — SEC2-T-040 (rate-limit observability, test-sequencing artifact)
SECURITY_ACCESS_CONTROL_GATE: NOT_PASSED
```

This distribution is preserved verbatim in `PRODUCTION_RESEARCH_PAGE_SEC2_TEST_RESULTS.csv` rows 1–43. SEC-2A appends 18 new rows (44–61); it does not alter any of rows 1–43 except two `notes`-field annotations (§9 below), and never touches the `status` cell of any original row.

## 4. Researcher Decision on T-030

Per the researcher's instruction for this turn, `SEC2-T-030` is **not** accepted as a permanent production limitation. The transitional (60-day) production design must enforce protected access at two layers — host Nginx (outer) and inner `voc_nginx` (inner) — with the same Basic Auth credential validated at both, subject to: no duplicate interactive prompt in the normal flow; no repeated 401 loop; no credential material in logs or reports; no protected content in unauthorized responses; both layers fail closed; credential stores outside Git. This addendum validates that design in a nonproduction prototype; it does not implement it in production.

## 5. Deterministic Rate-Limit Retest

A fresh, disposable rate-limit zone (`sec2a_outer_zone`, `rate=2r/s burst=3 nodelay`, configured recovery interval ≈1.5s) was deployed on the outer prototype layer, protecting `/api/research/linimasa`.

| Stage | Action | Result |
|---|---|---|
| A | Fresh disposable rate-limit state (container start, zone empty) | t=1787882148.831 |
| B | One authorized baseline request | HTTP 200 (`SEC2A-RL-001`) |
| C | Controlled unauthorized burst — 25 immediate anonymous requests | 401×3, 503×22 |
| D | Threshold + above-threshold observability | 401 present (`SEC2A-RL-002`), 503 present (`SEC2A-RL-003`) — both categories observable in one run, unlike the original T-040 |
| E | Measured cooldown, monotonic timestamps | 5.004s wait (> 1.5s configured recovery) — `SEC2A-RL-004` |
| F | Valid authorized request after cooldown | HTTP 200 (`SEC2A-RL-005`) |
| G | Confirm normal access recovered | second confirming request → HTTP 200 |

Credential/Authorization scan of the redacted access log (`log_format` records only `auth_present=0/1` and `status`, never the header value) across the full retest: zero matches for `Basic `, `Authorization`, or the dummy username — `SEC2A-RL-006` PASS.

```text
SEC2A-RL-001..006: 6/6 PASS
```

## 6. Inner Authentication Boundary

Two disposable `nginx:1.25-alpine` containers on an isolated Docker network (`sec2a_net`, no relation to any production or prior-turn network):

- **`sec2a_inner`** (`127.0.0.1:28085`) — models `voc_nginx`. Protects `/riset/pemodelan/`, `/riset/pemodelan/panduan/`, `/linimasa/`, `/api/research/linimasa`, `/api/research/pemodelan-dashboard` with `auth_basic`; serves `/public/` unauthenticated as the explicit public control route; carries the rate-limit zone from §5 on the API path.
- **`sec2a_outer`** (`127.0.0.1:28084`) — models the host Nginx public reverse proxy. Maps and protects `/atlas/riset/pemodelan/`, `/atlas/riset/pemodelan/panduan/`, `/atlas/linimasa/`, `/westkust/riset/pemodelan/`, `/westkust/riset/pemodelan/panduan/`, `/westkust/linimasa/`, and both research APIs, proxying to `sec2a_inner` over the Docker network; serves `/atlas/public/` unauthenticated.

Both use the same dummy credential (`DUMMY_CREDENTIAL_CREATED_IN_EPHEMERAL_TEST_WORKSPACE`), each layer with its own independently-mounted `htpasswd` copy (Option B in §9).

## 7. Same-Host Negative Tests

| Test | Description | Result |
|---|---|---|
| `SEC2A-INNER-001` | Anonymous direct-loopback page request denied | 401 |
| `SEC2A-INNER-002` | Anonymous direct-loopback API request denied | 401 |
| `SEC2A-INNER-003` | Valid direct-loopback page request succeeds | 200 |
| `SEC2A-INNER-004` | Valid direct-loopback API request succeeds | 200 |
| `SEC2A-INNER-005` | Valid outer-to-inner page request succeeds | 200 |
| `SEC2A-INNER-006` | Anonymous outer-to-inner request denied | 401 |
| `SEC2A-INNER-007` | Alternate/unmapped public prefix cannot bypass | 404 (anon and valid credential alike — no route exists) |
| `SEC2A-INNER-008` | Inner route path variation cannot bypass | no-trailing-slash=404, repeated-slash=401, query-string=401, encoded-path=401, alt-Host-header=401 |
| `SEC2A-INNER-009` | Missing credential store fails closed | anon=401, valid-cred-attempt=403 (no content) |
| `SEC2A-INNER-010` | Unreadable credential store fails closed | anon=401, valid-cred-attempt=500 (no content) |
| `SEC2A-INNER-011` | Unauthorized responses contain no protected body | confirmed — generic nginx error pages only |
| `SEC2A-INNER-012` | Credential/Authorization absent from logs | confirmed — zero matches across both access logs |

```text
SEC2A-INNER-001..012: 12/12 PASS
```

`SEC2A-INNER-009`/`010` were tested via disposable variant containers (a nonexistent-path config, and a `chmod 000` htpasswd copy respectively), since the primary containers' configs and credential store are read-only bind mounts and cannot be mutated in place — this mirrors how a real deployment would also refuse to silently degrade a read-only-mounted secret.

## 8. Double-Challenge Assessment

Normal valid flow: `anonymous → 401 at outer (WWW-Authenticate: Basic) → credential supplied once → 200`. Verified:

- Exactly one interactive-equivalent challenge (the outer 401) — confirmed by inspecting response headers at each hop.
- No second `401`/`WWW-Authenticate` appears anywhere in the successful chain (`num_redirects=0`, `final_status=200`).
- The outer proxy forwards the client's actual `Authorization` header value to the inner layer (standard `proxy_pass` header forwarding — not a synthetic, unvalidated trust header).
- The inner layer **independently re-validates** that header against its own credential store — proven by pointing the outer proxy at an inner instance provisioned with a different password: the outer-valid request still received `401` from that inner instance. This rules out "outer trusts inner is fine because outer said so" and confirms genuine two-layer validation.

No duplicate prompt, no 401 loop, no redirect loop, no credential disclosure, no protected content released before successful authorization. **No design limitation to report here** — the shared-credential, header-forwarding approach achieved single-prompt UX with genuine dual enforcement in this prototype.

## 9. Credential-Store Alternatives

| Option | Description | Least privilege | Rotation consistency | Drift risk | Container-mount risk | Secret exposure | Rollback | Operational burden | Entra/OIDC compatibility | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** — one host-managed htpasswd, mounted read-only into the inner container | Single file, single source of truth | High — one file, one owner | Best — one rotation updates both layers atomically | Low — physically impossible for the two layers to diverge | Cross-boundary mount from host into a container that otherwise has no reason to read host-managed secrets | Single file to protect; if leaked, compromises both layers at once | Simple — one file to restore | Lowest | Neutral — file-based approach is superseded wholesale by OIDC, not partially | Both layers fail closed together if the file is missing/unreadable (validated in §7) |
| **B** — two separately provisioned, identically generated htpasswd stores (used in this prototype) | Two files, must be kept in sync manually or by a provisioning script | Medium — each layer owns its own file | Weakest — two independent files can silently drift if rotation touches only one | None — no cross-container mount needed | No mount coupling between layers | Two files to protect; smaller blast radius if only one is compromised, but harder to guarantee both were rotated together | Requires restoring/regenerating two files in the correct order | Higher — provisioning script must run twice, verify parity | Neutral | Each layer fails closed independently (validated in §7); a silent drift (only one rotated) produces user-visible mixed success/failure rather than a clean fail-closed state |
| **C** — outer Basic Auth plus service-aware/application authorization at the inner layer (e.g. a signed internal token, mTLS, or an application-level check) | No shared secret file at all between layers | Highest — inner trusts a purpose-built mechanism, not a copy of the outer credential | Best in the long run — inner rotation is independent of end-user credential rotation | Lowest | None | Smallest — end-user credential never needs to exist inside the inner container at all | Most complex to roll back cleanly (two different mechanisms) | Highest for a 60-day transition — requires new tooling, not just two htpasswd files | **Best** — this is structurally closest to how an Entra/OIDC-fronted inner service would eventually work (inner validates a token, not a shared password) | Depends entirely on the chosen mechanism's own fail-closed guarantees — not validated by this prototype |

### Recommendation for the 60-day transition

```text
OPTION_A_RECOMMENDED_WITH_LIMITATIONS
PENDING_RESEARCHER_DECISION
```

**Option A** (one host-managed htpasswd source) is recommended for the temporary transition, with the following conditions attached:

- one host-managed htpasswd source — not two independently provisioned copies;
- stored outside Git (as already required by every prior SEC-0/SEC-1/SEC-2 output);
- mounted read-only into the inner `voc_nginx` container;
- the outer host Nginx reads the same host-managed source directly (no container mount needed at that layer);
- named individual accounts only, per `SEC-DEC-08` — no shared account;
- atomic rotation — one file, one edit, both layers see the update simultaneously with no window where the layers hold different credentials;
- least-privilege file permissions (readable only by the Nginx worker user/group, not world-readable, unlike the dummy 644 permission used in this ephemeral prototype purely to work around this sandbox's UID mismatch — see `PRODUCTION_RESEARCH_PAGE_SEC2A_DEFENSE_IN_DEPTH_ADDENDUM.md` §7 and the negative-test-report §3.2 mechanism note);
- no credential value, hash, or file content printed into any report this turn or in the future;
- production provisioning of this option remains **unauthorized** by this addendum — recommendation only.

**Rationale:** Option A has the lowest operational burden and the lowest drift risk of the two Basic-Auth-based options, which matters most for a mechanism explicitly scoped to 60 days. Option B (used in *this* prototype instead, specifically to prove each layer validates independently rather than one blindly trusting the other — see §8) is a reasonable fallback if the cross-boundary mount in Option A is judged an unacceptable container-isolation trade-off, but it carries a real risk of silent rotation drift that would need a provisioning script to guard against. Option C is the right target shape for the eventual inner-layer mechanism but is disproportionate engineering for a 60-day bridge and should instead inform the Entra/OIDC target design directly.

**Decision-ledger status:** no existing row in `PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv` covers credential-store topology selection specifically (`SEC-DEC-05` covers *whether* to run an Option C Basic Auth prototype at all; `SEC-DEC-08` covers *who* gets an account — neither decides *how many htpasswd files* or *which mount topology*). This recommendation is therefore recorded here only, as `PENDING_RESEARCHER_DECISION`. No new decision row is added to the ledger by this freeze; that remains a separate, explicitly-authorized researcher action.

## 10. Recommended Transitional Approach

Adopt Option A for the 60-day Basic Auth transition at the inner layer, contingent on all Phase 7 conditions being met in a production-like environment (SEC-3, not this turn): single interactive prompt confirmed against production's actual multi-server-block `silida.conf` topology (extending the SEC2-T-029 limitation note), fail-closed confirmed against a real filesystem path (extending the SEC2-T-035/036 mechanism note), and the credential-store file provisioned outside Git with least-privilege container-mount permissions.

## 11. Production Design Consequences

- Production's `voc_nginx` container will need an `auth_basic` block added for the six protected routes and two APIs listed in §6, plus a read-only-mounted `auth_basic_user_file`.
- Production's host Nginx (public reverse proxy) already carries the dual-prefix Basic Auth design from SEC-2; it now additionally needs to forward the client's `Authorization` header to `voc_nginx` unmodified (standard proxy behavior, no code change expected, but must be explicitly verified against production's actual proxy directives — this was not re-verified against production's real config in this turn).
- Neither change was made to any production file in this turn. Port 8084 remains exposed and unauthenticated at both layers in production.

## 12. Remaining Limitations

- This prototype used a single-server-block outer topology (like the original SEC-2 run); production's multi-server-block `silida.conf` was not re-tested here — the SEC2-T-029 recommendation to verify against a multi-server-block topology before production implementation still stands and now additionally applies to the inner-layer Host-header behavior.
- `SEC2A-INNER-009`/`010` (missing/unreadable store) were validated via disposable variant containers, not by mutating the primary running containers, because their configs are read-only bind mounts — production's real failure mode (a real filesystem path, not a container bind-mount) should be verified directly in SEC-3, per the existing SEC2-T-035/036 note this addendum does not override.
- The double-challenge assessment (§8) validated header-forwarding within this prototype's Docker network only; production's actual outer→inner network path (and any intermediate component that might strip or rewrite the `Authorization` header) was not exercised.
- No production-like environment was used this turn (Phase SEC-3 remains a distinct, not-yet-authorized step).

## 13. Rollback Rehearsal

Recorded in full in `PRODUCTION_RESEARCH_PAGE_SEC2_ROLLBACK_REHEARSAL.md` §6 (appended). Summary: a disposable no-auth inner variant reproduced the exact T-030 condition (direct-loopback anonymous → 200); the authenticated `sec2a_inner` container, unchanged throughout, denied the same request (401). This isolates inner `auth_basic` as the specific control that mitigates T-030. Public control routes (`/atlas/public/`, `/public/`) remained accessible throughout. All dummy credential material was shredded and the ephemeral workspace deleted.

## 14. Cleanup

```text
sec2a_* containers removed:        confirmed (docker ps -a --filter name=sec2a_ empty)
sec2a_net network removed:         confirmed (docker network ls has no sec2a_net)
Test ports (28084-28089) listening: none (ss -tln, no match)
Dummy htpasswd files:               shredded (shred -u), directory permission mistake corrected and re-verified, workspace confirmed deleted
Ephemeral workspace:                deleted (rm -rf; ls afterward: "No such file or directory")
Production uptime:                  unchanged — local dev voc_nginx unaffected by this turn's containers/network; remote westkust-prod voc_nginx still "Up 5 weeks", db "Up 8 weeks", redis "Up 7 weeks" — no restart
Production files:                   unchanged — no SSH write command issued this turn beyond read-only git/docker/ss checks
```

## 15. Security Gate Status

```text
SECURITY_ACCESS_CONTROL_GATE: NOT_PASSED
```

Unchanged. This phase validates a nonproduction mitigation prototype for a documented limitation; it does not implement Basic Auth in production, does not create any real account, and does not authorize deployment.

## 16. Final Decision

```text
RATE-LIMIT RETEST:  6/6 PASS   (SEC2A-RL-001..006)
INNER BOUNDARY:     12/12 PASS (SEC2A-INNER-001..012)
DOUBLE CHALLENGE:   single effective prompt, genuine dual validation, no defect found
ROLLBACK REHEARSAL: PASS
CLEANUP:            PASS
T-040:              SUPERSEDED_BY_SEC2A_RETEST (original FAIL cell preserved verbatim)
T-030:              MITIGATION_PROTOTYPE_VALIDATED (NOT PRODUCTION_RESOLVED)
CREDENTIAL STORE:   OPTION_A_RECOMMENDED_WITH_LIMITATIONS (PENDING_RESEARCHER_DECISION)
PRODUCTION:         UNCHANGED
SECURITY GATE:      NOT_PASSED

FINAL STATUS: PRODUCTION_RESEARCH_PAGE_SEC2A_PASS
```
