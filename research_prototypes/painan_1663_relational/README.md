# Painan 1663 Relational Research Prototype — NONPRODUCTION

**Status: RESEARCH PROTOTYPE. NONPRODUCTION. Not connected to the public Atlas, API, database, or Graphify.**

This is a local, self-contained, read-only research page that renders exactly one reviewed
artifact:

```
data/power_relations/painan_1663_relational_research_artifact.json
```

It exists to test whether the Painan 1663 relational MVP artifact can be understood visually
without collapsing overlapping power relations into one territorial color or one sovereign
narrative. See `ATLAS_PAINAN_1663_LOCAL_RELATIONAL_RESEARCH_PROTOTYPE_PLAN.md` (repository root)
for the full governing plan, and
`docs/thesis/pilot_annotation/ATLAS_PAINAN_1663_LOCAL_RELATIONAL_PROTOTYPE_AUDIT.md` for the
construction/validation audit.

## Running it locally

The page fetches the artifact via `fetch()` with a relative path, which most browsers block under
`file://`. Serve it from the repository root with any static file server, for example:

```bash
cd /home/naro/westkust-routes
python3 -m http.server 8899
```

Then open:

```
http://localhost:8899/research_prototypes/painan_1663_relational/index.html
```

## What it does

- Fetches `../../data/power_relations/painan_1663_relational_research_artifact.json` read-only.
  Never writes to it, never mutates the fetched object, never sends data anywhere.
- Renders six views: Overview, Actors, Relation Timeline, Relation Network, Claim vs Effective
  Control, Public-Copy Preview.
- Uses a three-level progressive-disclosure pattern on every relation: Level 1 (actor, relation,
  date, evidence badge) is always visible; Level 2 (source/provenance/claim-control/commitment) and
  Level 3 (power theory, patron-client classification, theoretical annotation) are each behind a
  `<details>` element that starts closed and must be explicitly opened — no Level 3 field is ever
  auto-promoted to Level 1.
- Never renders a `PATRON_OF` / `CLIENT_OF` edge — patron-client status is always a research
  annotation inside a relation's Level 3 drawer, never a network edge type.

## What it does not do

- No API call, no database query, no Graphify call.
- No import of any `backend/` or `frontend/` module.
- No write to the artifact file or any other file (a pure `fetch` + in-memory DOM render).
- No connection to the production Atlas map, `atlas.js`, or any production template.

## Validation

```bash
python3 scripts/research_validators/validate_painan_1663_relational_prototype.py
```

This validator checks the prototype's static source (`index.html`, `prototype.js`,
`prototype.css`) and re-verifies the underlying artifact/base-validator, per the 30-item checklist
in the governing plan §13. It performs no writes and makes no network calls.
