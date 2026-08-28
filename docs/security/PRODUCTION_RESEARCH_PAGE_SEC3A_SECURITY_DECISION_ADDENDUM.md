# Production Research Page — SEC-3A Security Decision Addendum

> **This addendum does not modify `PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv`'s schema or rows. It records a decision proposal for the researcher, separately.**

---

## 1. Ledger Check (this turn)

```text
grep -c "SEC-DEC-11" PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv
```

No existing `SEC-DEC-11` row was found in the ledger at the start of this turn (consistent with the same check performed in SEC-3's `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md` § 1). Per instruction, this addendum does **not** add a row silently. It records the decision here.

## 2. Decision

```text
SEC-DEC-11: OPTION_A_APPROVED_WITH_LIMITATIONS
```

**Decision scope:** design approval for the 60-day transitional Basic Auth architecture (Option A — one host-managed credential source, dual-read by host Nginx directly and by the inner `voc_nginx` container via a read-only mount). This is a **design-level** approval only.

## 3. What This Decision Means

- One host-managed credential source, outside Git and outside the project checkout.
- Host Nginx reads the source directly (no mount needed at that layer — it is a native process on the same filesystem).
- Inner `voc_nginx` receives a **read-only** mount of the same source.
- `0640` with an approved matching group is the **preferred target** permission model.
- `0644` remains a **non-preferred fallback only** — acceptable if the container-UID-matching mechanics described in `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md` § 3 cannot be resolved for the stock `nginx:1.25-alpine` image without a custom image build, but never the default choice.
- `0777` is prohibited, with no exception.
- Named individual accounts only (`SEC-DEC-08`, already `APPROVED`) — no shared account.
- Atomic rotation is required (`mv`-based replacement, never in-place edit).

## 4. Limitations

- No production credential store has been created.
- The exact server-local path remains pending (deliberately not finalized in this broadly-visible document, per the same convention used in `PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md` § D).
- The actual UID/GID permission mapping for `0640` + matching group remains pending verification against a real (or custom-built) `voc_nginx` image — see the credential-store design's own honest limitation on this point.
- The pilot-user list remains pending.
- The credential-delivery channel remains pending.
- Production deployment remains pending — this decision does **not** authorize implementation.
- A read-only mount is required wherever the credential source reaches a container.
- Atomic rotation is required for every future update to the source, not only the initial provisioning.
- A rollback procedure is required and must be validated against the real production host before this design is implemented (SEC-3's rollback rehearsal covered only the disposable environment).

## 5. Production Implementation Status

```text
NOT_AUTHORIZED
```

This addendum approves the *design*. It does not authorize, create, or provision any of the following:

- a production credential path;
- production htpasswd creation;
- username provisioning;
- password provisioning;
- Nginx modification;
- Compose modification;
- deployment.

It does not authorize `SEC-4` or any production change.
