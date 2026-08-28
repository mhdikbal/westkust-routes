# ATLAS Canonical Route Redirect Plan

> **Design document. No redirect has been implemented. No Nginx file was edited or reloaded. No production change.**

---

## 1. Candidate Redirect Design

```text
/westkust/                    -> /atlas/                    (301/308, no path segment)
/westkust/<child-path>        -> /atlas/<child-path>         (path preserved exactly once)
/westkust/<child-path>?<qs>   -> /atlas/<child-path>?<qs>    (query string preserved)
```

Candidate Nginx block (illustrative only — **not applied**, would replace the current `location /westkust/ { proxy_pass ...; proxy_redirect ...; sub_filter ...; }` block in `silida.conf`):

```nginx
# CANDIDATE ONLY -- NOT APPLIED
location /westkust/ {
    return 301 /atlas/$1$is_args$args;   # exact regex capture group syntax to be
                                           # finalized against nginx's location
                                           # matching semantics before real drafting;
                                           # illustrative form only
}
```

The precise directive form (`rewrite` vs `return` with a captured regex location, vs a `location ~ ^/westkust/(.*)$` block) needs to be worked out carefully against Nginx's own semantics — this is a **design sketch**, not implementation-ready syntax, and is explicitly not meant to be copy-pasted into production.

## 2. Requirements Checklist

| Requirement | How the design satisfies it |
|---|---|
| Path preserved exactly once | Single-segment substitution (`/westkust/` → `/atlas/`), no double-application |
| Query string preserved | `$is_args$args` (or equivalent) appended, not dropped |
| No `/atlas/atlas/` duplication | The redirect target is always `/atlas/<captured-path>`, never re-prefixes an already-`/atlas/`-prefixed path — since the redirect only fires from the `/westkust/` location, an already-`/atlas/`-prefixed request never reaches this rule |
| No `/westkust/westkust/` duplication | Same reasoning — the rule only ever *emits* `/atlas/...`, it never re-enters itself |
| No redirect loop | The target prefix (`/atlas/`) has no rule redirecting back to `/westkust/`; a loop would require two opposing rules, which this design does not create |
| No open redirect | The target host is never taken from user input (`Host` header, query parameter, or any client-controlled value) — only the path segment is substituted, the domain is always implicitly `silida.org` via a relative redirect (`/atlas/...`, not `https://.../atlas/...`) |
| Encoded paths handled safely | Nginx decodes `%XX` sequences before location matching by default (already confirmed in SEC-2/SEC-3A's own encoded-path tests); the redirect rule inherits this behavior without needing special handling |
| Repeated slashes normalized/rejected consistently | Needs explicit verification against the actual `merge_slashes` directive state in `silida.conf` (default `on` in Nginx, which already collapses `//` sequences before location matching) — to be confirmed in the smoke-test phase (§ `ATLAS_WESTKUST_ROUTE_RETIREMENT_TEST_MATRIX.csv`), not assumed here |
| `GET`/`HEAD` verified | Both already confirmed working identically on both prefixes today (`ATLAS_WESTKUST_ROUTE_RETIREMENT_DISCOVERY.md` § 2); a redirect preserves method semantics for `GET`/`HEAD` under both `301` and `308` |
| Non-`GET` behavior explicitly reviewed | See § 3 below — this is the deciding factor between `301` and `308` |
| Static/media paths reviewed separately | Static assets (`/static/...`) currently resolve correctly under both prefixes via `sub_filter` URL rewriting in the response body, not via the redirect mechanism — retiring `/westkust/` as an *application* route does not necessarily mean static assets must also redirect; this needs an explicit scope decision (does "retire /westkust/" include its static assets, or only its page routes?) not resolved by this plan |

## 3. 301 vs 308 — Recommendation

| | `301 Moved Permanently` | `308 Permanent Redirect` |
|---|---|---|
| Method preservation | Browsers/clients are permitted (and in practice, virtually all do) to change `POST`→`GET` on redirect follow | Strictly preserves the original method — a `POST` stays a `POST` |
| Caching | Both are cacheable long-term by browsers and CDNs (Cloudflare included) | Same |
| SEO signal | Well-understood, universally supported "permanent move" signal for search engines | Equivalent signal, less universally implemented in older crawlers, but Google/Bing both support it |
| Relevance here | The known routes under `/westkust/` (`/`, `/linimasa/`, `/riset/pemodelan/`, `/riset/pemodelan/panduan/`) are all read-only `GET` pages — no non-`GET` form submission or API call currently targets `/westkust/<path>` directly (the two research APIs are separately, directly protected, not proxied through the page-prefix redirect) | — |

**Recommendation: `301`.** Every known route under `/westkust/` is `GET`/`HEAD` only; there is no evidence of any `POST`/`PUT`/`DELETE` request ever targeting a `/westkust/`-prefixed path (confirmed by the repository dependency search finding zero application-level references to the prefix — nothing in Django code constructs or expects a `/westkust/`-prefixed request). `308`'s stricter method preservation would add no protection against a scenario that doesn't exist here, while `301` is the more universally-recognized "permanent move" signal for the SEO canonicalization goal (§ Phase 5). This is a recommendation only — **not implemented**.

## 4. What This Plan Does Not Decide

- The exact Nginx directive syntax (§ 1's caveat).
- Whether static assets under `/westkust/` should also redirect, or remain dual-served indefinitely (§ 2's static-path caveat).
- The observation period before actually retiring `/westkust/`'s application content entirely (see `ATLAS_WESTKUST_ROUTE_RETIREMENT_AUDIT.md` § "Remaining Decisions").
