/*
 * Painan 1663 relational research prototype — NONPRODUCTION.
 *
 * Reads exactly one file, read-only:
 *   ../../data/power_relations/painan_1663_relational_research_artifact.json
 *
 * No API call, no database access, no Graphify access, no production import.
 * Does not mutate the fetched artifact object; renders directly from it.
 * If a required field is missing on a record, that record renders an inline
 * validation error and is skipped from further rendering (per plan §12) —
 * the rest of the view still renders.
 */

const ARTIFACT_PATH = "../../data/power_relations/painan_1663_relational_research_artifact.json";

const AUTHORIZED_RELATION_TYPES = [
  "REQUESTS_PROTECTION_FROM", "PROVIDES_PROTECTION_TO", "REQUIRES_MONOPOLY_FROM",
  "NEGOTIATES_WITH", "RECONCILES_WITH", "MAINTAINS_PARALLEL_ALIGNMENT_WITH",
  "CLAIMS_JURISDICTION_OVER",
];
const FORBIDDEN_RELATION_TYPES = ["PATRON_OF", "CLIENT_OF", "PATRON_CLIENT_RELATION"];

const CLAIM_OR_EFFECTIVE_CONTROL_VOCAB = [
  "CLAIM", "FORMAL_ACCEPTANCE", "TREATY_OBLIGATION", "MILITARY_PRESENCE", "FORT_CONTROL",
  "COMMERCIAL_CONTROL", "ADMINISTRATIVE_CONTROL", "EFFECTIVE_LOCAL_COMPLIANCE",
  "CONTESTED_CONTROL", "UNKNOWN_EFFECTIVE_CONTROL",
];

const RELATION_REQUIRED_FIELDS = [
  "relation_id", "subject_actor_id", "object_actor_id", "relation_type",
  "valid_from", "valid_to", "date_precision", "event_ids", "treaty_id",
  "source_document_ids", "source_passage_locator", "provenance_status",
  "evidence_strength", "interpretive_status", "explicit_or_inferred",
  "claim_or_effective_control", "commitment_credibility", "patron_client_classification",
  "power_dimensions", "researcher_review_required", "source_statement_summary",
  "historical_reconstruction", "theoretical_annotation", "public_display_summary", "notes",
];

let ARTIFACT = null;
let ACTOR_BY_ID = {};
let RENDER_ERRORS = []; // { where, detail } — surfaced in Overview, never silently dropped

function el(tag, attrs, children) {
  const node = document.createElement(tag);
  if (attrs) {
    for (const k in attrs) {
      if (k === "text") { node.textContent = attrs[k]; continue; }
      if (k === "html") { node.innerHTML = attrs[k]; continue; }
      node.setAttribute(k, attrs[k]);
    }
  }
  (children || []).forEach((c) => { if (c) node.appendChild(c); });
  return node;
}

function badge(text, cls) {
  return el("span", { class: "badge " + (cls || ""), text });
}

function setLoadStatus(kind, text) {
  const box = document.getElementById("load-status");
  box.className = kind;
  box.textContent = text;
}

async function loadArtifact() {
  let res;
  try {
    res = await fetch(ARTIFACT_PATH, { cache: "no-store" });
  } catch (e) {
    setLoadStatus("error", "FATAL: could not fetch artifact (" + e.message + "). " +
      "This prototype must be served over http(s) (e.g. `python3 -m http.server` from the " +
      "repository root) — opening index.html directly via file:// blocks fetch() in most browsers.");
    throw e;
  }
  if (!res.ok) {
    setLoadStatus("error", "FATAL: artifact fetch returned HTTP " + res.status + " for " + ARTIFACT_PATH);
    throw new Error("fetch failed");
  }
  let data;
  try {
    data = await res.json();
  } catch (e) {
    setLoadStatus("error", "FATAL: artifact is not valid JSON (" + e.message + ")");
    throw e;
  }

  // Structural validation — required top-level shape. Stop (do not render views) on failure,
  // per plan §12: "If a required field is absent, render an explicit validation error and
  // stop the affected view." At the top level, absence of actors/relations stops the whole app,
  // since no view can meaningfully render without them.
  if (!Array.isArray(data.actors) || !Array.isArray(data.relations)) {
    setLoadStatus("error", "FATAL: artifact missing required top-level 'actors' or 'relations' array.");
    throw new Error("structural validation failed");
  }

  setLoadStatus("ok", "Artifact loaded read-only from " + ARTIFACT_PATH +
    " — status: " + (data.status || "UNKNOWN") + " · schema_version: " + (data.schema_version || "UNKNOWN") +
    " · " + data.actors.length + " actors · " + data.relations.length + " relations.");

  return data;
}

function validateRelation(rel) {
  const missing = RELATION_REQUIRED_FIELDS.filter((f) => !(f in rel));
  if (missing.length > 0) {
    RENDER_ERRORS.push({
      where: "relation " + (rel.relation_id || "(no id)"),
      detail: "missing required field(s): " + missing.join(", "),
    });
    return false;
  }
  if (FORBIDDEN_RELATION_TYPES.includes(rel.relation_type)) {
    RENDER_ERRORS.push({
      where: "relation " + rel.relation_id,
      detail: "forbidden relation_type '" + rel.relation_type + "' — patron-client must never be an edge",
    });
    return false;
  }
  if (!AUTHORIZED_RELATION_TYPES.includes(rel.relation_type)) {
    RENDER_ERRORS.push({
      where: "relation " + rel.relation_id,
      detail: "unauthorized relation_type '" + rel.relation_type + "' — not one of the seven approved types",
    });
    return false;
  }
  if (!ACTOR_BY_ID[rel.subject_actor_id] || !ACTOR_BY_ID[rel.object_actor_id]) {
    RENDER_ERRORS.push({
      where: "relation " + rel.relation_id,
      detail: "unresolved endpoint (subject=" + rel.subject_actor_id + ", object=" + rel.object_actor_id + ")",
    });
    return false;
  }
  return true;
}

/* ---------------------------------------------------------------------- */
/* View: Overview                                                          */
/* ---------------------------------------------------------------------- */

function renderOverview(root, validRelations) {
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "overview-heading", text: "Overview" }));
  root.appendChild(el("div", { class: "warning-box", text:
    "RESEARCH-ONLY WARNING: This page renders one reviewed, nonproduction JSON artifact for a " +
    "single 1663 case. It is not the public Atlas, does not represent Atlas coverage generally, " +
    "and every relation below is bounded, source-linked, and marked with its own evidence status — " +
    "nothing here should be read as a settled historical verdict." }));

  const stats = el("div", { class: "stat-grid" });
  const tile = (n, label) => el("div", { class: "stat-tile" }, [
    el("div", { class: "n", text: String(n) }),
    el("div", { class: "label", text: label }),
  ]);
  stats.appendChild(tile(ARTIFACT.actors.length, "Actors"));
  stats.appendChild(tile(validRelations.length, "Relations (valid)"));

  const dates = validRelations.map((r) => r.valid_from).filter(Boolean).sort();
  const dateRange = dates.length ? (dates[0] + " → " + (dates[dates.length - 1] || "open")) : "n/a";
  stats.appendChild(tile(dateRange, "Date range (valid_from span)"));

  root.appendChild(el("div", { class: "card" }, [stats]));

  // relation-type distribution
  const typeDist = {};
  validRelations.forEach((r) => { typeDist[r.relation_type] = (typeDist[r.relation_type] || 0) + 1; });
  root.appendChild(el("h2", { text: "Relation-type distribution" }));
  root.appendChild(distTable(typeDist));

  // explicit vs inferred
  const eoiDist = {};
  validRelations.forEach((r) => { eoiDist[r.explicit_or_inferred] = (eoiDist[r.explicit_or_inferred] || 0) + 1; });
  root.appendChild(el("h2", { text: "Explicit versus inferred distribution" }));
  root.appendChild(distTable(eoiDist));

  // claim vs effective control
  const cecDist = {};
  validRelations.forEach((r) => { cecDist[r.claim_or_effective_control] = (cecDist[r.claim_or_effective_control] || 0) + 1; });
  root.appendChild(el("h2", { text: "Claim versus effective-control distribution" }));
  root.appendChild(distTable(cecDist));

  // unresolved actors / mandates (declared on actor records themselves)
  root.appendChild(el("h2", { text: "Unresolved actors and mandates (researcher_review_required)" }));
  const reviewActors = ARTIFACT.actors.filter((a) => a.researcher_review_required);
  if (reviewActors.length === 0) {
    root.appendChild(el("p", { text: "None flagged on actor records." }));
  } else {
    const ul = el("ul", { class: "rel-list" });
    reviewActors.forEach((a) => ul.appendChild(el("li", { text: a.label + " — " + (a.notes || a.identity_caveat || "flagged for review") })));
    root.appendChild(ul);
  }

  root.appendChild(el("h2", { text: "Source gaps" }));
  root.appendChild(el("p", { text:
    "De Leeuw 1926 full text; Kroeskamp 1931; Painan/Padang/Tiku's own 1663 internal circumstances; " +
    "an Aceh-side independent account of the pre-1660 tributary relationship; a written VOC mandate " +
    "document for Groenewegen's 1662-63 negotiation. Carried forward unchanged from the recovered " +
    "deep-dive and audit; not re-derived by this prototype." }));

  if (RENDER_ERRORS.length > 0) {
    root.appendChild(el("h2", { text: "Render-time validation errors (record-level, not fatal)" }));
    const ul = el("ul", { class: "rel-list" });
    RENDER_ERRORS.forEach((e) => ul.appendChild(el("li", { text: e.where + ": " + e.detail })));
    root.appendChild(el("div", { class: "warning-box" }, [ul]));
  }
}

function distTable(distObj) {
  const wrap = el("div", { class: "vocab-list" });
  Object.keys(distObj).sort().forEach((k) => {
    wrap.appendChild(el("div", { class: "vocab-item active" }, [
      el("span", { class: "count", text: String(distObj[k]) }),
      document.createTextNode(" " + k),
    ]));
  });
  return wrap;
}

/* ---------------------------------------------------------------------- */
/* View: Actors                                                            */
/* ---------------------------------------------------------------------- */

function renderActors(root, validRelations) {
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "actors-heading", text: "Actors" }));
  root.appendChild(el("p", { class: "level3-notice", text:
    "Actors are individually named factions, institutions, or broker individuals — never a " +
    "territorial population or a merged regional label. See the notice on each card." }));

  ARTIFACT.actors.forEach((actor) => {
    const incoming = validRelations.filter((r) => r.object_actor_id === actor.actor_id);
    const outgoing = validRelations.filter((r) => r.subject_actor_id === actor.actor_id);

    const card = el("div", { class: "card actor-card" });
    card.appendChild(el("h3", { text: actor.label + "  " + (actor.researcher_review_required ? "⚠" : "") }));
    card.appendChild(el("div", { class: "actor-type", text: actor.actor_type + " · actor_id: " + actor.actor_id }));
    if (actor.named_individuals && actor.named_individuals.length) {
      card.appendChild(el("p", { text: "Named individuals: " + actor.named_individuals.join(", ") }));
    }
    card.appendChild(el("p", { text: actor.description || "" }));

    card.appendChild(el("p", { class: "level3-notice", text:
      "Non-homogenization notice: this actor is kept distinct from any other faction, negeri, or " +
      "aggregate label (e.g. never merged into a generic \"Songypagouers\" or territorial identity)." }));

    card.appendChild(el("h4", { text: "Outgoing relations (" + outgoing.length + ")" }));
    card.appendChild(relList(outgoing, "object_actor_id"));
    card.appendChild(el("h4", { text: "Incoming relations (" + incoming.length + ")" }));
    card.appendChild(relList(incoming, "subject_actor_id"));

    if (actor.identity_caveat) {
      const d = disclosureDrawer("level2", "Show source basis / identity caveat (Level 2)",
        el("p", { text: actor.identity_caveat }));
      card.appendChild(d);
    }
    root.appendChild(card);
  });
}

function relList(relations, otherEndpointField) {
  const ul = el("ul", { class: "rel-list" });
  if (relations.length === 0) {
    ul.appendChild(el("li", { text: "(none)" }));
    return ul;
  }
  relations.forEach((r) => {
    const otherId = r[otherEndpointField];
    const other = ACTOR_BY_ID[otherId];
    const li = el("li", {});
    li.appendChild(document.createTextNode(r.relation_type + " — " + (other ? other.label : otherId) +
      " (" + r.valid_from + (r.valid_to ? " → " + r.valid_to : " → open") + ") "));
    li.appendChild(badge(r.explicit_or_inferred === "EXPLICIT_STRATEGY" ? "explicit" : "inferred",
      r.explicit_or_inferred === "EXPLICIT_STRATEGY" ? "badge-explicit" : "badge-inferred"));
    ul.appendChild(li);
  });
  return ul;
}

/* ---------------------------------------------------------------------- */
/* View: Relation Timeline                                                  */
/* ---------------------------------------------------------------------- */

function parseDateForAxis(s, fallbackEnd) {
  if (!s) return fallbackEnd ? 9999 : 1600; // open-ended sorts to the far right
  const parts = s.split("-").map(Number);
  return parts[0] + (parts[1] ? parts[1] / 12 : 0);
}

function renderTimeline(root, validRelations) {
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "timeline-heading", text: "Relation Timeline" }));
  root.appendChild(el("p", { text:
    "Overlapping validity ranges are shown as separate, non-overwriting bars — including the " +
    "simultaneous VOC protection tie and the Aceh reconciliation in Oct 1663. Open-ended ranges " +
    "(valid_to = null) are marked with →." }));

  const controls = el("div", { id: "timeline-controls" });
  const actorLabel = el("label", { text: "Filter by actor: " });
  const actorSelect = el("select", { id: "tl-actor-filter" });
  actorSelect.appendChild(el("option", { value: "", text: "All actors" }));
  ARTIFACT.actors.forEach((a) => actorSelect.appendChild(el("option", { value: a.actor_id, text: a.label })));
  actorLabel.appendChild(actorSelect);

  const typeLabel = el("label", { text: "Filter by relation type: " });
  const typeSelect = el("select", { id: "tl-type-filter" });
  typeSelect.appendChild(el("option", { value: "", text: "All types" }));
  AUTHORIZED_RELATION_TYPES.forEach((t) => typeSelect.appendChild(el("option", { value: t, text: t })));
  typeLabel.appendChild(typeSelect);

  controls.appendChild(actorLabel);
  controls.appendChild(typeLabel);
  root.appendChild(controls);

  const listWrap = el("div", { id: "tl-list" });
  root.appendChild(listWrap);

  const minYear = 1662, maxYear = 1666.5; // this case's own window; each bar scaled within it

  function draw() {
    listWrap.innerHTML = "";
    const actorFilter = actorSelect.value;
    const typeFilter = typeSelect.value;
    const rows = validRelations.filter((r) =>
      (!actorFilter || r.subject_actor_id === actorFilter || r.object_actor_id === actorFilter) &&
      (!typeFilter || r.relation_type === typeFilter)
    ).sort((a, b) => parseDateForAxis(a.valid_from) - parseDateForAxis(b.valid_from));

    if (rows.length === 0) {
      listWrap.appendChild(el("p", { text: "No relations match this filter." }));
      return;
    }

    rows.forEach((r) => {
      const row = el("div", { class: "timeline-row" });
      const subj = ACTOR_BY_ID[r.subject_actor_id], obj = ACTOR_BY_ID[r.object_actor_id];
      row.appendChild(el("div", { class: "tl-label" }, [
        document.createTextNode(r.relation_type),
        el("br", {}),
        document.createTextNode((subj ? subj.label : r.subject_actor_id) + " → " + (obj ? obj.label : r.object_actor_id)),
      ]));

      const track = el("div", { class: "timeline-track" });
      const startY = parseDateForAxis(r.valid_from);
      const endY = r.valid_to ? parseDateForAxis(r.valid_to) : maxYear;
      const leftPct = Math.max(0, Math.min(100, ((startY - minYear) / (maxYear - minYear)) * 100));
      const widthPct = Math.max(3, Math.min(100 - leftPct, ((endY - startY) / (maxYear - minYear)) * 100));
      const isExplicit = r.explicit_or_inferred === "EXPLICIT_STRATEGY";
      const bar = el("div", {
        class: "timeline-bar " + (isExplicit ? "explicit" : "inferred") + (r.valid_to ? "" : " open-end"),
        style: "left:" + leftPct + "%; width:" + widthPct + "%;",
        title: r.relation_id + " (" + r.date_precision + " precision)",
        tabindex: "0",
        "aria-label": r.relation_type + " from " + (subj ? subj.label : r.subject_actor_id) + " to " +
          (obj ? obj.label : r.object_actor_id) + ", " + r.valid_from + (r.valid_to ? " to " + r.valid_to : ", open end"),
      }, [document.createTextNode(r.valid_from)]);
      track.appendChild(bar);
      row.appendChild(track);
      listWrap.appendChild(row);
    });
  }

  actorSelect.addEventListener("change", draw);
  typeSelect.addEventListener("change", draw);
  draw();
}

/* ---------------------------------------------------------------------- */
/* View: Relation Network (hand-rolled SVG, no external library)            */
/* ---------------------------------------------------------------------- */

function renderNetwork(root, validRelations) {
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "network-heading", text: "Relation Network" }));
  root.appendChild(el("p", { text:
    "Directed research diagram. No territorial shapes. Multiple edges between the same pair of " +
    "actors are drawn as separate curves. No edge is ever labeled PATRON_OF or CLIENT_OF — " +
    "patron-client status is a Level 3 annotation available in each relation's detail panel below, " +
    "never an edge type." }));

  const svgNS = "http://www.w3.org/2000/svg";
  const width = 900, height = 560;
  const cx = width / 2, cy = height / 2, radius = 210;
  const actors = ARTIFACT.actors;
  const pos = {};
  actors.forEach((a, i) => {
    const angle = (i / actors.length) * 2 * Math.PI - Math.PI / 2;
    pos[a.actor_id] = { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) };
  });

  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("viewBox", "0 0 " + width + " " + height);
  svg.setAttribute("width", "100%");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Directed diagram of six Painan 1663 actors and their relations");

  const defs = document.createElementNS(svgNS, "defs");
  const marker = document.createElementNS(svgNS, "marker");
  marker.setAttribute("id", "arrowhead");
  marker.setAttribute("markerWidth", "8");
  marker.setAttribute("markerHeight", "8");
  marker.setAttribute("refX", "7");
  marker.setAttribute("refY", "3");
  marker.setAttribute("orient", "auto");
  const arrowPath = document.createElementNS(svgNS, "path");
  arrowPath.setAttribute("d", "M0,0 L0,6 L7,3 z");
  arrowPath.setAttribute("fill", "#a6acb8");
  marker.appendChild(arrowPath);
  defs.appendChild(marker);
  svg.appendChild(defs);

  // group edges between the same unordered pair to offset multiple edges as separate curves
  const pairCounts = {};
  validRelations.forEach((r) => {
    const key = [r.subject_actor_id, r.object_actor_id].sort().join("|");
    pairCounts[key] = pairCounts[key] || [];
    pairCounts[key].push(r);
  });

  Object.values(pairCounts).forEach((group) => {
    group.forEach((r, idx) => {
      const p1 = pos[r.subject_actor_id], p2 = pos[r.object_actor_id];
      if (!p1 || !p2) return;
      const mx = (p1.x + p2.x) / 2, my = (p1.y + p2.y) / 2;
      const offset = (idx - (group.length - 1) / 2) * 60;
      const dx = p2.y - p1.y, dy = p1.x - p2.x;
      const len = Math.hypot(dx, dy) || 1;
      const ctrlX = mx + (dx / len) * offset, ctrlY = my + (dy / len) * offset;
      // stagger label position further along the same normal so overlapping edges don't collide
      const labelOffset = offset * 1.35;
      const labelX = mx + (dx / len) * labelOffset;
      const labelY = my + (dy / len) * labelOffset;

      const isExplicit = r.explicit_or_inferred === "EXPLICIT_STRATEGY";
      const isContested = r.claim_or_effective_control === "CONTESTED_CONTROL";
      const isUnknown = r.claim_or_effective_control === "UNKNOWN_EFFECTIVE_CONTROL";

      const path = document.createElementNS(svgNS, "path");
      path.setAttribute("d", "M " + p1.x + " " + p1.y + " Q " + ctrlX + " " + ctrlY + " " + p2.x + " " + p2.y);
      path.setAttribute("fill", "none");
      path.setAttribute("stroke", isContested ? "#ff6b6b" : "#6fb3ff");
      path.setAttribute("stroke-width", "2");
      if (!isExplicit) path.setAttribute("stroke-dasharray", "7,5");
      else if (isUnknown) path.setAttribute("stroke-dasharray", "2,3");
      path.setAttribute("marker-end", "url(#arrowhead)");
      path.setAttribute("tabindex", "0");
      path.setAttribute("role", "img");
      path.setAttribute("aria-label", r.relation_type + ": " + (ACTOR_BY_ID[r.subject_actor_id] || {}).label +
        " to " + (ACTOR_BY_ID[r.object_actor_id] || {}).label + ". " + r.explicit_or_inferred +
        ". claim or effective control: " + r.claim_or_effective_control + ".");
      const titleEl = document.createElementNS(svgNS, "title");
      titleEl.textContent = r.relation_type + " (" + r.relation_id + ")";
      path.appendChild(titleEl);
      svg.appendChild(path);

      const labelText = r.relation_type.replace(/_/g, " ");
      const approxWidth = labelText.length * 5.2;
      const bg = document.createElementNS(svgNS, "rect");
      bg.setAttribute("x", String(labelX - approxWidth / 2 - 3));
      bg.setAttribute("y", String(labelY - 11));
      bg.setAttribute("width", String(approxWidth + 6));
      bg.setAttribute("height", "13");
      bg.setAttribute("fill", "#171a21");
      bg.setAttribute("opacity", "0.85");
      svg.appendChild(bg);

      const label = document.createElementNS(svgNS, "text");
      label.setAttribute("x", String(labelX));
      label.setAttribute("y", String(labelY - 2));
      label.setAttribute("font-size", "9");
      label.setAttribute("fill", "#c7ccd6");
      label.setAttribute("text-anchor", "middle");
      label.textContent = labelText;
      svg.appendChild(label);
    });
  });

  actors.forEach((a) => {
    const p = pos[a.actor_id];
    const g = document.createElementNS(svgNS, "g");
    const circle = document.createElementNS(svgNS, "circle");
    circle.setAttribute("cx", String(p.x));
    circle.setAttribute("cy", String(p.y));
    circle.setAttribute("r", "26");
    circle.setAttribute("fill", "#171a21");
    circle.setAttribute("stroke", a.researcher_review_required ? "#ff6b6b" : "#f2c14e");
    circle.setAttribute("stroke-width", "2");
    g.appendChild(circle);
    const text = document.createElementNS(svgNS, "text");
    text.setAttribute("x", String(p.x));
    text.setAttribute("y", String(p.y + 40));
    text.setAttribute("font-size", "11");
    text.setAttribute("fill", "#e8e8ec");
    text.setAttribute("text-anchor", "middle");
    text.textContent = a.label;
    g.appendChild(text);
    svg.appendChild(g);
  });

  const wrap = el("div", { id: "network-svg-wrap" }, [svg]);
  root.appendChild(wrap);

  const legend = el("div", { id: "network-legend" }, [
    el("span", {}, [el("span", { class: "legend-swatch" }), document.createTextNode("explicit relation")]),
    el("span", {}, [el("span", { class: "legend-swatch inferred" }), document.createTextNode("observed action as strategy (inferred)")]),
    el("span", {}, [el("span", { class: "legend-swatch contested" }), document.createTextNode("contested control")]),
    el("span", {}, [document.createTextNode("gold node border = actor OK; red node border = researcher_review_required")]),
  ]);
  root.appendChild(legend);

  root.appendChild(el("h2", { text: "Relation detail (progressive disclosure)" }));
  validRelations.forEach((r) => root.appendChild(relationDetailPanel(r)));
}

/* ---------------------------------------------------------------------- */
/* Shared: relation detail panel with Level 1 / 2 / 3 disclosure            */
/* ---------------------------------------------------------------------- */

function disclosureDrawer(levelClass, summaryText, bodyNode) {
  const details = el("details", { class: "disclosure " + levelClass });
  details.appendChild(el("summary", { text: summaryText }));
  const body = el("div", { class: "disclosure-body" }, [bodyNode]);
  details.appendChild(body);
  return details;
}

function relationDetailPanel(r) {
  const subj = ACTOR_BY_ID[r.subject_actor_id], obj = ACTOR_BY_ID[r.object_actor_id];
  const card = el("div", { class: "card" });

  // Level 1 — always visible, never more than this by default
  const l1 = el("div", {});
  l1.appendChild(el("h3", { text: (subj ? subj.label : r.subject_actor_id) + " — " + r.relation_type.replace(/_/g, " ") +
    " — " + (obj ? obj.label : r.object_actor_id) }));
  l1.appendChild(el("p", { text: r.valid_from + (r.valid_to ? " → " + r.valid_to : " → open") + "  (" + r.date_precision + ")" }));
  l1.appendChild(badge(r.evidence_strength, "badge-" + (r.evidence_strength === "HIGH" ? "explicit" : "inferred")));
  l1.appendChild(badge(r.explicit_or_inferred, r.explicit_or_inferred === "EXPLICIT_STRATEGY" ? "badge-explicit" : "badge-inferred"));
  card.appendChild(l1);

  // Level 2 — source, provenance, claim/control, commitment credibility, limitation
  const l2body = el("div", {});
  l2body.appendChild(el("p", { html: "<strong>Source statement:</strong> " + escapeHtml(r.source_statement_summary) }));
  l2body.appendChild(el("p", { html: "<strong>Historical reconstruction:</strong> " + escapeHtml(r.historical_reconstruction) }));
  l2body.appendChild(el("p", { html: "<strong>Source document IDs:</strong> " + r.source_document_ids.join(", ") }));
  l2body.appendChild(el("p", { html: "<strong>Passage locator:</strong> " + escapeHtml(r.source_passage_locator) }));
  l2body.appendChild(el("p", { html: "<strong>Event IDs:</strong> " + (r.event_ids.length ? r.event_ids.join(", ") : "(none — secondary-source-only relation)") }));
  l2body.appendChild(el("p", { html: "<strong>Provenance status:</strong> " + r.provenance_status }));
  l2body.appendChild(el("p", { html: "<strong>Claim vs effective control:</strong> " + r.claim_or_effective_control }));
  l2body.appendChild(el("p", { html: "<strong>Commitment credibility:</strong> " + r.commitment_credibility }));
  l2body.appendChild(el("p", { html: "<strong>Interpretive status:</strong> " + r.interpretive_status }));
  l2body.appendChild(el("p", { html: "<strong>Researcher review required:</strong> " + (r.researcher_review_required ? "YES" : "no") }));
  card.appendChild(disclosureDrawer("level2", "Show source & provenance (Level 2)", l2body));

  // Level 3 — theory, patron-client, power dimensions, counterevidence, limitation. Never auto-open.
  const l3body = el("div", {});
  l3body.appendChild(el("p", { class: "level3-notice", text:
    "Level 3 research annotation — NOT a confirmed historical fact. Reused verbatim from the reviewed " +
    "artifact's own research findings; provided for research-detail review only." }));
  l3body.appendChild(el("p", { html: "<strong>Power dimensions:</strong> " + r.power_dimensions.join(", ") }));
  l3body.appendChild(el("p", { html: "<strong>Patron-client classification:</strong> " + badgeText(r.patron_client_classification) }));
  l3body.appendChild(el("p", { html: "<strong>Theoretical annotation:</strong> " + escapeHtml(r.theoretical_annotation) }));
  l3body.appendChild(el("p", { html: "<strong>Notes / counterevidence / limitations:</strong> " + escapeHtml(r.notes) }));
  card.appendChild(disclosureDrawer("level3", "Show theory & interpretation (Level 3 — research annotation only)", l3body));

  // Public-copy preview, shown as its own separate layer, never merged with the above
  const pubBody = el("div", {}, [el("p", { text: r.public_display_summary })]);
  card.appendChild(disclosureDrawer("level1", "Show proposed public-copy summary", pubBody));

  return card;
}

function badgeText(v) {
  return v; // plain text render inside an html-built <p>; classification kept as literal controlled-vocab string
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s == null ? "" : s;
  return div.innerHTML;
}

/* ---------------------------------------------------------------------- */
/* View: Claim vs Effective Control                                        */
/* ---------------------------------------------------------------------- */

function renderClaimControl(root, validRelations) {
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "claimcontrol-heading", text: "Claim versus Effective Control" }));
  root.appendChild(el("p", { text: "A claim or formal agreement does not by itself demonstrate effective control." }));

  const counts = {};
  validRelations.forEach((r) => { counts[r.claim_or_effective_control] = (counts[r.claim_or_effective_control] || 0) + 1; });

  const list = el("div", { class: "vocab-list" });
  CLAIM_OR_EFFECTIVE_CONTROL_VOCAB.forEach((v) => {
    const active = !!counts[v];
    const item = el("div", { class: "vocab-item" + (active ? " active" : "") });
    item.appendChild(el("div", { text: v }));
    item.appendChild(el("div", { class: "count", text: active ? String(counts[v]) + " relation(s)" : "not present in this artifact" }));
    list.appendChild(item);
  });
  root.appendChild(list);

  root.appendChild(el("h2", { text: "Relations by claim/control category" }));
  CLAIM_OR_EFFECTIVE_CONTROL_VOCAB.filter((v) => counts[v]).forEach((v) => {
    root.appendChild(el("h3", { text: v }));
    validRelations.filter((r) => r.claim_or_effective_control === v).forEach((r) => root.appendChild(relationDetailPanel(r)));
  });
}

/* ---------------------------------------------------------------------- */
/* View: Public-Copy Preview                                                */
/* ---------------------------------------------------------------------- */

function renderPublicCopy(root, validRelations) {
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "publiccopy-heading", text: "Public-Copy Preview" }));
  root.appendChild(el("p", { text:
    "Each relation's four interpretive layers, shown side by side so they cannot be mistaken for " +
    "one another. The public-copy summary is the only layer suitable for a Level-1 map label; the " +
    "other three are research content." }));

  validRelations.forEach((r) => {
    const subj = ACTOR_BY_ID[r.subject_actor_id], obj = ACTOR_BY_ID[r.object_actor_id];
    root.appendChild(el("h3", { text: (subj ? subj.label : r.subject_actor_id) + " → " + (obj ? obj.label : r.object_actor_id) + " (" + r.relation_type + ")" }));
    const grid = el("div", { class: "layer-compare" });
    grid.appendChild(el("div", { class: "layer-card source" }, [el("h4", { text: "Source statement" }), el("p", { text: r.source_statement_summary })]));
    grid.appendChild(el("div", { class: "layer-card reconstruction" }, [el("h4", { text: "Historical reconstruction" }), el("p", { text: r.historical_reconstruction })]));
    grid.appendChild(el("div", { class: "layer-card theory" }, [el("h4", { text: "Theoretical annotation (Level 3)" }), el("p", { text: r.theoretical_annotation })]));
    grid.appendChild(el("div", { class: "layer-card public" }, [el("h4", { text: "Public-display summary" }), el("p", { text: r.public_display_summary })]));
    root.appendChild(el("div", { class: "card" }, [grid]));
  });
}

/* ---------------------------------------------------------------------- */
/* Navigation                                                                */
/* ---------------------------------------------------------------------- */

function setupNav() {
  const buttons = Array.from(document.querySelectorAll(".nav-btn"));
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => { b.removeAttribute("aria-current"); });
      btn.setAttribute("aria-current", "page");
      document.querySelectorAll(".view").forEach((v) => { v.hidden = true; });
      document.getElementById("view-" + btn.dataset.view).hidden = false;
      document.getElementById("view-" + btn.dataset.view).focus?.();
    });
  });
}

/* ---------------------------------------------------------------------- */
/* Bootstrap                                                                */
/* ---------------------------------------------------------------------- */

(async function main() {
  setupNav();
  try {
    ARTIFACT = await loadArtifact();
  } catch (e) {
    console.error("Prototype halted: artifact could not be loaded.", e);
    return; // stop — do not render any view without a valid artifact
  }

  ACTOR_BY_ID = {};
  ARTIFACT.actors.forEach((a) => { ACTOR_BY_ID[a.actor_id] = a; });

  RENDER_ERRORS = [];
  const validRelations = ARTIFACT.relations.filter(validateRelation);

  renderOverview(document.getElementById("view-overview"), validRelations);
  renderActors(document.getElementById("view-actors"), validRelations);
  renderTimeline(document.getElementById("view-timeline"), validRelations);
  renderNetwork(document.getElementById("view-network"), validRelations);
  renderClaimControl(document.getElementById("view-claimcontrol"), validRelations);
  renderPublicCopy(document.getElementById("view-publiccopy"), validRelations);
})();
