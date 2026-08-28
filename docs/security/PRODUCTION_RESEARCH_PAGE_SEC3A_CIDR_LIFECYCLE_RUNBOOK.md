# Production Research Page — SEC-3A Trusted-Source CIDR Lifecycle Runbook

> **Procedure document. No CIDR list was downloaded or installed into production this turn.**

---

## 1. Scope Correction (important, from this turn's inventory)

The original `SEC3-F-02` framing assumed host Nginx should trust **Cloudflare's** published CIDR ranges directly. This turn's read-only inventory (`PRODUCTION_RESEARCH_PAGE_SEC3A_CLOUDFLARE_REAL_IP_DESIGN.md` § 2) found that `$remote_addr` at host Nginx is **not** Cloudflare's edge IP — it is a fixed hosting-provider internal load-balancer address (`10.1.10.126`, on the `10.1.10.0/24` private VLAN), consistently, across every sampled request. **The thing that must stay current is therefore the provider LB's own address (or narrow subnet), not Cloudflare's CIDR list.** This runbook is written against that corrected scope. If a future architecture change removes the provider LB hop (e.g. Cloudflare connecting directly to `westkust-prod`'s public IP), this runbook's authoritative-source section would need Cloudflare's own published ranges instead — noted here so the correction is traceable, not silently substituted.

## 2. Authoritative Source

- **Primary (current design):** the hosting provider's own network documentation / support channel, confirming the fixed address or subnet their edge/load-balancer layer uses to connect to `westkust-prod`. This is not a URL this document can name with confidence — it depends on the specific hosting provider's own infrastructure documentation, which was not looked up this turn (out of scope for a read-only Nginx-config inventory).
- **Secondary (only if the topology changes to remove the provider LB hop):** Cloudflare's own published IP ranges, at `https://www.cloudflare.com/ips-v4` and `https://www.cloudflare.com/ips-v6` — the standard, Cloudflare-maintained authoritative source, fetched only if and when this design's scope correction (§ 1) is superseded by an actual topology change.

## 3. Fetch Mechanism

```text
NOT_AUTHORIZED_FOR_EXECUTION (production)
1. Fetch the authoritative source's current CIDR list (§ 2) over HTTPS.
2. Save with a retrieval timestamp and the source URL/contact recorded.
3. Diff against the currently-configured set_real_ip_from value(s).
4. Do NOT apply automatically -- present the diff for human review.
```

No automatic execution in production without review, per instruction. This turn, no live fetch against a real Cloudflare or provider endpoint was performed — the disposable test topology used RFC-reserved documentation/test ranges (`198.51.100.0/24` — TEST-NET-2, RFC 5737; `2001:db8::/32` — RFC 3849) as stand-ins for "some trusted CIDR," and a single fixed private IP (`172.40.0.3/32`) as the stand-in for the provider LB, specifically so no real network data needed to be retrieved to exercise the trust-boundary *logic*. This is recorded here for traceability, not omitted.

## 4. Review and Update Process

```text
1. Checksum or diff review: compare the new candidate list against the
   currently-deployed set_real_ip_from value(s) line by line; flag any
   removed entry (could silently stop trusting a legitimate source) and any
   added entry (requires the same scrutiny as the original trust decision).
2. IPv4 and IPv6 coverage: verify both families are present if the
   authoritative source publishes both (Cloudflare does; the provider LB's
   scope should be confirmed for both address families too).
3. Configuration generation: render the new set_real_ip_from block into a
   candidate nginx snippet, syntax-checked with `nginx -t` before any staged
   update (this turn's SEC3A-IP-012 confirms the mechanism works).
4. Staged update: apply to a production-like (not production) environment
   first, re-run PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_IP_TEST_RESULTS.csv's
   test IDs against it, before touching the real silida.conf.
5. Rollback: keep the immediately-prior trusted-source configuration as a
   dated, permissioned-identically backup file, restorable via a single
   `nginx -t && systemctl reload nginx` cycle (config-only, no restart) --
   same low-blast-radius pattern as PRODUCTION_RESEARCH_PAGE_SEC3_ROLLBACK_RUNBOOK.md.
6. Update owner: not assigned by this document -- remaining decision, see
   PRODUCTION_RESEARCH_PAGE_SEC3A_AUDIT.md.
7. Review frequency: recommend confirming the provider LB address has not
   changed at minimum whenever the hosting provider announces infrastructure
   changes, and as a fixed calendar check no less often than quarterly during
   the 60-day Basic Auth transition window itself (i.e. at least once within
   the window, given its short duration) -- final cadence is a remaining
   decision, not fixed by this document.
8. Alert if source unavailable: if the authoritative source (§ 2) cannot be
   reached for a scheduled review, this must NOT silently skip the review --
   it must generate a visible alert to the update owner, since a stale trust
   source is a security-relevant gap, not a routine miss.
9. Behavior if a new/changed range is missing from the deployed config: the
   missing range simply means requests that should have been trusted are
   NOT trusted (fail-safe direction -- SEC3A-IP-011 confirms an untrusted
   source's headers are ignored, never wrongly honored). This degrades to
   "restored IP falls back to the raw peer" for affected traffic, which is
   the same safe behavior as SEC3A-IP-002 (no header, no invented address)
   -- it does not silently start trusting an attacker.
```

## 5. What This Runbook Does Not Do

- It does not fetch, download, or install any real CIDR or LB-address list into `silida.conf` or any production path.
- It does not name a specific update owner or review cadence as final — both are remaining decisions (`PRODUCTION_RESEARCH_PAGE_SEC3A_AUDIT.md`).
- It does not resolve the open question of exactly what the provider LB forwards (`CLOUDFLARE_REAL_IP_DESIGN.md` § 3.1) — that requires an out-of-band conversation with the hosting provider, not something derivable from `westkust-prod`'s own logs.
