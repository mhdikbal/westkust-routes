# Production Research Page — SEC-3A Cloudflare Trusted Real-IP Design

> **Phase:** SEC-3A closure item 2 of 2 — targeted design for `SEC3-F-02` only.
> **Design document. Nothing in this document was applied to production.**

---

## 1. Finding Under Design

```text
SEC3-F-02: OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST
```

## 2. Read-Only Inventory (this turn, `westkust-prod`)

| Item | Finding |
|---|---|
| `real_ip_header` / `set_real_ip_from` in `silida.conf` | absent |
| `X-Forwarded-For` handling | set via `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` on the three proxy blocks (`/api/`, `/westkust/`, `/atlas/`) — appended, not trusted/restored |
| `CF-Connecting-IP` handling | not referenced anywhere in `silida.conf` |
| Current access-log source address (`$remote_addr`) | **`10.1.10.126`, consistently, across every sampled request** (50/50 recent log lines) |
| IPv6 `listen` directives | none found in `silida.conf` |
| Direct-IP reachability of port 8084 | confirmed still reachable externally (N1 not yet applied — see SEC-3 candidate diff §A) |

### 2.1 Critical finding: an undocumented intermediate hop

```text
FINDING SEC3-F-03: HOST_NGINX_IMMEDIATE_PEER_IS_PROVIDER_INTERNAL_LOAD_BALANCER
Observed immediate peer:  10.1.10.126
Classification:           PRIVATE_PROVIDER_INTERNAL_ADDRESS
```

`$remote_addr` at host Nginx is **not** Cloudflare's edge IP — it is `10.1.10.126`, a fixed address inside a private subnet (`westkust-prod`'s own interface is `10.1.10.142/24` on the same `ens18` VLAN; `10.1.10.126` is a different host on that same private segment, not the public internet). This address is classified only as `PRIVATE_PROVIDER_INTERNAL_ADDRESS` — evidence-bounded to what was directly observed (a private RFC 1918 address on the host's own local VLAN, distinct from the host itself, sending every sampled request). **No specific hosting-provider identity is inferred or named** — none was documented in any approved infrastructure evidence available to this turn, and none is needed to state the finding correctly. The actual chain, discovered this turn and not documented anywhere prior to this addendum, is:

```text
client -> Cloudflare edge -> [hosting-provider internal load balancer, 10.1.10.0/24]
       -> westkust-prod host Nginx (silida.conf) -> voc_nginx (:8084) -> backend/frontend
```

This means a design that only trusts Cloudflare's published CIDR ranges via `set_real_ip_from` on the **immediate** peer address would never activate — the immediate peer is always the provider's internal LB, never a Cloudflare IP directly. Every prior mention of "Cloudflare real-IP restoration" in the SEC-3 audit (correctly) flagged the absence of any restoration, but did not yet know about this second hop; this document corrects and completes that picture.

The corresponding sample log line captured (redacted of nothing sensitive — this is a public-facing access log with no credentials, since Basic Auth is not active):

```text
10.1.10.126 - - [.. GET /atlas/linimasa/ ..] 200 169887 ".." "Mozilla/5.0 .." "103.91.87.10, 104.23.175.61"
```

The final quoted field (a custom log-format addition already present in `silida.conf`'s access logging — not modified by this document) shows a two-value chain: a plausible genuine client IP followed by a plausible Cloudflare edge IP. This is consistent with the two-hop model above and gives independent, real evidence supporting it, without this document needing to enumerate or trust any specific IP as "the" client from log inspection alone.

## 3. Trust Boundary Design

### 3.1 Principle

Trust the **immediate, single, fixed** internal-LB address (or its narrow subnet) as the only nginx `set_real_ip_from` source at the host-Nginx layer — **not** Cloudflare's ranges directly, since Cloudflare is never the immediate peer in this topology. The value nginx should then restore `$remote_addr` from is whatever the trusted LB hop forwarded — which, depending on what the provider's LB itself does, is either (a) the LB's own restored/passed-through `CF-Connecting-IP` value, or (b) a chained `X-Forwarded-For` whose second-to-last hop is Cloudflare's own edge IP and whose first hop is the genuine client. **This requires confirming, out of band with the hosting provider, exactly what the LB forwards** — this design cannot determine that from `westkust-prod`'s own logs alone, and does not claim to.

### 3.2 Required directives (candidate, not applied)

```nginx
# candidate only -- NOT applied to silida.conf this turn
set_real_ip_from <PROVIDER_LB_ADDRESS_OR_SUBNET>;   # e.g. 10.1.10.126/32 or 10.1.10.0/24 -- confirm exact scope with the provider before finalizing
real_ip_header X-Forwarded-For;                      # or CF-Connecting-IP, pending provider confirmation (see 3.1)
real_ip_recursive off;                                # start conservative: trust only the one confirmed hop; revisit only if the provider confirms a second forwarded value needs recursion
```

`real_ip_recursive` is deliberately proposed **off** as the conservative starting point, in contrast to this turn's disposable *test* topology (which used `on` to exercise the two-value-chain code path safely against synthetic ranges). Turning it on in production without first confirming exactly what the LB forwards risks trusting a value an untrusted upstream party (anything able to reach the LB, if the LB itself doesn't strip inbound `X-Forwarded-For`) could inject. This is a specific, deliberate divergence between the test topology and the production recommendation, called out explicitly rather than left implicit.

### 3.3 Defined behavior by scenario

| Scenario | Expected `$remote_addr` after restoration |
|---|---|
| Request through Cloudflare → provider LB → host Nginx | restored to the genuine client IP, once the LB-forwarded value is confirmed and trusted |
| Direct request to an allowed host endpoint (bypassing Cloudflare, hitting host Nginx's public IP:443 directly) | **not** trusted — the immediate peer is the direct client, not the provider LB, so `set_real_ip_from` does not match and `$remote_addr` remains the raw direct-connect IP (correct: this is already the true client) |
| Direct request to port 8084 before N1 containment | irrelevant to this design — port 8084 bypasses host Nginx entirely; N1 (SEC-3 candidate diff §A) is the control for this, not real-IP restoration |
| Direct request to port 8084 after N1 | same as above — N1 makes this scenario unreachable from outside the host regardless of real-IP configuration |
| Stale Cloudflare CIDR list | not directly applicable to the recommended design, since Cloudflare's ranges are not what host Nginx trusts directly (the provider LB is) — see § `PRODUCTION_RESEARCH_PAGE_SEC3A_CIDR_LIFECYCLE_RUNBOOK.md` for why the LB address itself is the thing that must stay current, and why a stale/incorrect LB address fails closed (§ 3.4) |
| Missing `CF-Connecting-IP` / missing forwarded value | falls back to the immediate peer address (the LB), never invents an address — verified in the disposable test (`SEC3A-IP-002`) |
| Spoofed header from an untrusted source | ignored — verified in the disposable test (`SEC3A-IP-003`, `SEC3A-IP-004`); only requests whose *immediate* peer matches `set_real_ip_from` are eligible for restoration at all |

### 3.4 Interpretation of key variables

- `$remote_addr` — after `ngx_http_realip_module` processing, this becomes the **restored** (believed-genuine) client address when the immediate peer is trusted and a forwarded value is present; otherwise it remains the raw peer address. This is the variable to use in `add_header`, application-facing client-IP logic, and (per § `PRODUCTION_RESEARCH_PAGE_SEC3A_RATE_LIMIT_KEY` recommendation below) the rate-limit key.
- `$realip_remote_addr` — always the **original, raw** socket peer address, regardless of restoration. Use this for infrastructure-level debugging ("which upstream hop actually connected to us"), never as a security-relevant client identity.
- Access logs — should log **both** `$remote_addr` (restored) and `$realip_remote_addr` (raw peer) so that infrastructure issues (e.g. the LB address changing) remain diagnosable without losing per-client observability. Verified structurally in the disposable test's `sec3a_ip` log format.
- `limit_req_zone` keys — must key on `$remote_addr` (post-restoration), never on the raw peer, or every client behind the shared LB/Cloudflare hop collapses into one bucket (this was the exact SEC3-F-02 concern). See § Rate-Limit Key Decision below.

### 3.5 Explicit anti-goals (from Phase 7)

- **Not all users may appear as one Cloudflare IP** — resolved by restoring to the genuine client value once the trust chain is correctly established, not by trusting Cloudflare's IP as the identity.
- **A direct client must not be able to select its own rate-limit identity** — resolved by scoping trust to the single confirmed immediate-peer address/subnet; an attacker connecting directly to host Nginx's public IP is never the trusted peer, so any header they send is ignored and they are keyed on their own real, unspoofable TCP peer address.

## 4. Rate-Limit Key Decision

| Option | Description | Verdict |
|---|---|---|
| **RK-1** — `$binary_remote_addr` (equivalently `$remote_addr`) after trusted real-IP restoration | Keys on the restored, believed-genuine client address once the trust chain in § 3 is correctly configured | **Recommended** |
| RK-2 | A derived key using a validated Cloudflare client address parsed independently of the realip module (e.g. custom `map` on `$http_cf_connecting_ip` with manual validation) | Rejected as unnecessary complexity — duplicates what `ngx_http_realip_module` already does correctly once configured per § 3, with a higher risk of an inconsistent, hand-rolled validation bug |
| RK-3 | The existing un-restored source address (today's actual behavior — always `10.1.10.126`) | **Rejected** — collapses every client into one shared bucket, exactly the concern that opened `SEC3-F-02`; confirmed structurally unsound by this turn's inventory (§ 2.1) |

**Recommendation: RK-1**, contingent on the provider confirming the exact forwarded-value mechanism (§ 3.1) before implementation. This accounts for: Cloudflare trust validation (indirect, via the confirmed LB hop, not direct Cloudflare CIDR trust — a deliberate correction from the original SEC3-F-02 framing, which assumed Cloudflare was the immediate peer); direct-access behavior (unaffected — direct clients are never trusted, correctly keyed on their own peer address); N1 containment (orthogonal — N1 closes the port-8084 bypass, real-IP design addresses per-client fairness for traffic that does go through host Nginx); IPv4 and IPv6 (both exercised in the disposable test, § `PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_IP_TEST_RESULTS.csv`); spoofing resistance (verified — untrusted direct sources cannot inject a trusted-looking header); log observability (both restored and raw addresses retained, § 3.4); privacy (no new data is retained beyond what already exists — IP addresses were already being logged); operational simplicity (lower than RK-2, since it reuses the stock module rather than hand-rolled validation).

## 5. Closure Rule

Per the required rule, `DESIGN_AND_PROTOTYPE_VALIDATED` requires **12/12** spoofing and real-IP tests to `PASS`. This turn achieved **10/12 clean PASS** plus **2/12 `PASS_WITH_LIMITATION`** (`SEC3A-IP-007`, `SEC3A-IP-008` — see `PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_IP_TEST_RESULTS.csv`). The two limited results are not a design defect: the trust-boundary logic they depend on (restored-address correctness and distinctness) was independently and structurally proven by other tests in the same suite (`SEC3A-IP-001`, `-003`, `-004`, `-005`) that passed cleanly. What did not reproduce was the **numeric** rate-limit-threshold demonstration itself — isolated this turn to a rate-limiter shared-memory-zone malfunction specific to the current sandbox's Docker runtime state (confirmed with an intentionally extreme control case: `rate=1r/m`, no burst allowance, still returned `200` on every request), not a flaw in the trust/design logic. The identical directive pattern reliably produced real `429`s earlier in this same session under SEC-2A and SEC-3.

Per the researcher's adjudication of this evidence, the closure status — retitled to name exactly what remains, rather than the broader "trusted-proxy design" framing this finding originally carried (the design itself is now complete) — is:

```text
SEC3-F-02: OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST
```

**not** `DESIGN_AND_PROTOTYPE_VALIDATED`, **not** `PRODUCTION_RESOLVED`, and **not** `PASS`. The design itself (§ 3–4) is complete, and the trust-boundary mechanics that matter most (restoration correctness, spoofing resistance, IPv4/IPv6, log integrity, the CIDR-source mental-model correction in `SEC3A-IP-011`) are fully and cleanly demonstrated. What remains before this finding can close is narrow and specific: (a) a deterministic, clean-environment re-run of exactly the two rate-limit-threshold tests (`SEC3A-IP-007`/`008`) to rule out any doubt about the sandbox anomaly — scoped as SEC-3B, not a repeat of this document's design or the 20 Django tests — and (b) the production-specific items already listed above — provider confirmation of the LB's forwarded-value mechanism, the actual `silida.conf` edit, and verification against the real chain.
