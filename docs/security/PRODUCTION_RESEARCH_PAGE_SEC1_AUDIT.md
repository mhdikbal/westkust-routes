# Production Research Page — SEC-1 Architecture Design Audit

> **Phase:** SEC-1 completion record
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`

---

## 1. Scope

Confirms Phase SEC-1 (network containment and authentication architecture design) was performed as specified, with no implementation, credential creation, or configuration change.

## 2. Inputs Used

Authoritative discovery findings F-01 through F-05 (from Phase SEC-0), the four SEC-0 discovery documents, and this turn's additional read-only verification: production network path trace (`systemctl is-active nginx`, `ps aux`, `docker compose config`, `docker network ls`), and a full-repository shared-consumer grep for the two candidate research APIs.

## 3. Phase 1 — Network Containment Design

Complete. Two alternatives (N1, N2) documented in `PRODUCTION_RESEARCH_PAGE_NETWORK_CONTAINMENT_PLAN.md`. **N2 was traced, not assumed, and found infeasible without a separately scoped re-architecture** (host nginx is a native systemd process, not a Docker network member — confirmed via live process inspection). N1 is documented as the only alternative achievable within current architecture, matching the researcher's own stated preference.

## 4. Phase 2 — Dual-Prefix Policy

Complete. P1 (protect both identically) adopted as the design policy, per researcher direction. Exact location-block shape, precedence/regex risk, trailing-slash behavior, `proxy_redirect` repetition requirement, and unaffected public routes all documented in `PRODUCTION_RESEARCH_PAGE_DUAL_PREFIX_AND_API_POLICY.md` §Phase 2.

## 5. Phase 3 — API Protection Policy

Complete. Shared-consumer audit performed this turn (full-repository grep) — **result: no public or shared consumer exists for either `/api/research/linimasa` or `/api/research/pemodelan-dashboard`.** Both classified `AUTHENTICATED_RESEARCH_API` without needing a public/private response split. Documented in the same policy document, §Phase 3.

## 6. Phase 4 — Option C Transitional Design

Complete. All 14 design requirements from the plan addressed in `PRODUCTION_RESEARCH_PAGE_BASIC_AUTH_TRANSITION_PLAN.md`, including a location-block design sketch (not applied), rollback procedure, and explicit confirmation that no credential value appears anywhere in the document.

## 7. Phase 5 — Option B Target Design

Complete. All 13 design areas from the plan addressed in `PRODUCTION_RESEARCH_PAGE_ENTRA_OIDC_TARGET_PLAN.md`, including the dual-callback-URI requirement (§2, a direct consequence of the dual-prefix policy), the new `X-Forwarded-Prefix` requirement not present in any existing config, and an explicit restatement of the direct-port containment prerequisite (§13).

## 8. Phase 6 — Security Decisions

Complete. `PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv` created with exactly 10 rows (SEC-DEC-01 through SEC-DEC-10). Every row's `researcher_decision` column is `PENDING` — verified programmatically (`set(...) == {'PENDING'}`). The researcher's own draft recommendations from this turn's instruction are captured verbatim in a separate `researcher_draft_recommendation` column, distinct from the decision column itself, mirroring the established pattern from the ontology adjudication ledger (recommend now, decide/record later) — **no decision was filled.**

## 9. Phase 7 — Outputs

All six required files created, exactly as named:

```text
docs/security/PRODUCTION_RESEARCH_PAGE_NETWORK_CONTAINMENT_PLAN.md
docs/security/PRODUCTION_RESEARCH_PAGE_DUAL_PREFIX_AND_API_POLICY.md
docs/security/PRODUCTION_RESEARCH_PAGE_BASIC_AUTH_TRANSITION_PLAN.md
docs/security/PRODUCTION_RESEARCH_PAGE_ENTRA_OIDC_TARGET_PLAN.md
docs/security/PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv
docs/security/PRODUCTION_RESEARCH_PAGE_SEC1_AUDIT.md   (this file)
```

No file outside `docs/security/` was created or modified by this turn, except as already noted in §11 (unrelated pre-existing state).

## 10. Phase 8 — Validation

| # | Check | Result |
|---|---|---|
| 1 | No route protected under only one prefix | PASS — every design in the dual-prefix policy document applies to `/atlas/` and `/westkust/` identically (P1) |
| 2 | APIs not omitted | PASS — both candidate APIs explicitly designed into the same boundary as the HTML pages |
| 3 | Direct port bypass addressed by both supported architectures | PASS — N1 (network containment) is a prerequisite (SEC-DEC-01/02) for both Option B and Option C designs; both target-design documents restate this dependency explicitly |
| 4 | All password material stays outside Git | PASS by design — htpasswd path design explicitly specifies a location outside the repository tree; Entra design references no secret value |
| 5 | No username or password generated | PASS — confirmed, none created this turn |
| 6 | No htpasswd file created | PASS — confirmed, none created this turn |
| 7 | No Nginx edit | PASS — `silida.conf` and `nginx/nginx.conf` both read-only this turn |
| 8 | No Compose edit | PASS — `docker-compose.yml` read-only this turn |
| 9 | No firewall edit | PASS — `ufw` not touched this turn (status checked in SEC-0, not re-checked or modified this turn) |
| 10 | No application edit | PASS — no `.py`/`.html` file modified |
| 11 | No migration created | PASS |
| 12 | No service restarted | PASS |
| 13 | No container recreated | PASS |
| 14 | No server state changes | PASS — all SSH commands this turn were read-only (`systemctl is-active`, `ps aux`, `which`, `docker compose config`, `docker network ls`) |
| 15 | Draft V2 and research artifacts unchanged | PASS — unrelated to this turn's file set; not touched |
| 16 | Production gates stay 0/8 | PASS — unaffected by this turn, unrelated subsystem |
| 17 | `SECURITY_ACCESS_CONTROL_GATE` remains `NOT_PASSED` | PASS — no implementation occurred that could pass it |

## 11. Git Status Note

`docs/security/` now contains 10 files total (4 from Phase SEC-0, 6 from this turn) — see terminal summary for the full `git status --short` output. The pre-existing, unrelated modified file (`docs/thesis/colab/POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv`, from an earlier ontology-adjudication turn) remains untouched by this turn, as does every other pre-existing untracked file in the working tree.

---

## 12. Current Risk Disclosure (unchanged by this milestone's freeze)

As of the SEC-0/SEC-1 discovery date, and **still true at the time this milestone is frozen**: `voc_nginx` remains published on `0.0.0.0:8084`, the production host firewall remains inactive, `/atlas/` and `/westkust/` remain identical proxies to the same upstream, and both `/api/research/linimasa` and `/api/research/pemodelan-dashboard` remain reachable without authentication. **None of SEC-DEC-01 through SEC-DEC-10 has been implemented.** Recording researcher decisions and freezing this planning milestone documents the *approved direction*, not a remediation — the underlying exposure is unchanged and remains live until a separately authorized implementation turn closes it.

---

## Final Status

```text
PRODUCTION_RESEARCH_PAGE_AUTH_ARCHITECTURE_READY_FOR_RESEARCHER_DECISION
```
