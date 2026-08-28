/*
 * Multi-case power-relation research prototype — NONPRODUCTION.
 *
 * Reads exactly 5 files, read-only, all under data/power_relations/migrated_v2_1/ (the Draft
 * V2.1 migrated copies produced during the artifact-migration phase; strict supersets of the
 * 5 frozen originals under data/power_relations/, which this page never reads).
 *
 * No API call, no database access, no Graphify access, no production import. Never mutates a
 * fetched artifact object. Never merges actors or relations across cases — the case switcher
 * moves between 5 independently-scoped, independently-authored artifacts; an actor_id that
 * happens to recur (e.g. ACTOR_VOC in more than one case's own file) is reported as a diagnostic
 * fact on the Case Index view, never silently treated as the same in-memory object across cases.
 *
 * Reuses, unmodified in spirit, the rendering/disclosure pattern from
 * research_prototypes/painan_1663_relational/prototype.js: el(), badge(), escapeHtml(),
 * disclosureDrawer(), the render-error-collection pattern (skip an invalid record, surface it,
 * never silently drop it).
 */

const CASES_DEF = [
  { id: "painan", label: "Painan 1663", path: "../../data/power_relations/migrated_v2_1/painan_1663_relational_research_artifact_v2_1_migrated.json" },
  { id: "natal", label: "Natal 1760", path: "../../data/power_relations/migrated_v2_1/natal_1760_relational_validation_artifact_v2_1_migrated.json" },
  { id: "kototangah", label: "Koto Tangah", path: "../../data/power_relations/migrated_v2_1/koto_tangah_destruction_cycle_relational_validation_artifact_v2_1_migrated.json" },
  { id: "tiku", label: "Tiku 1625-1740", path: "../../data/power_relations/migrated_v2_1/tiku_1625_1740_relational_validation_artifact_v2_1_migrated.json" },
  { id: "sillida", label: "Sillida", path: "../../data/power_relations/migrated_v2_1/sillida_resource_governance_relational_validation_artifact_v2_1_migrated.json" },
];

// Mirrors scripts/research_validators/power_relation_ontology_rules.json's own
// closed_relation_vocabulary exactly: 14 MVP_CORE_RELATION + 2 EXTENDED_RESEARCH_RELATION +
// 2 REQUIRES_MORE_EVIDENCE_RELATION (Draft V2 SS2's own third named tier). Do not add a value
// here that is not also in that JSON file's own list.
const AUTHORIZED_RELATION_TYPES = [
  "REQUESTS_PROTECTION_FROM", "PROVIDES_PROTECTION_TO", "REQUIRES_MONOPOLY_FROM", "NEGOTIATES_WITH",
  "RECONCILES_WITH", "SWITCHES_ALIGNMENT_TO", "CLAIMS_JURISDICTION_OVER", "CLAIMS_COMMODITY_MONOPOLY",
  "CONTESTS_SUCCESSION_WITH", "CONTESTS_RESOURCE_WITH", "RECOGNIZES_OFFICE_HOLDER",
  "COLLECTS_TOLL_FROM", "LEASES_RESOURCE_TO", "USES_MILITARY_FORCE_AGAINST",
  "EXERCISES_EFFECTIVE_CONTROL_OVER", "CONTROLS_FORT",
  "MAINTAINS_PARALLEL_ALIGNMENT_WITH", "APPOINTS_OFFICE_HOLDER",
];
const FORBIDDEN_RELATION_TYPES = ["PATRON_OF", "CLIENT_OF", "PATRON_CLIENT_RELATION"];

const CLAIM_OR_EFFECTIVE_CONTROL_VOCAB = [
  "CLAIM", "FORMAL_ACCEPTANCE", "TREATY_OBLIGATION", "MILITARY_PRESENCE", "FORT_CONTROL",
  "COMMERCIAL_CONTROL", "ADMINISTRATIVE_CONTROL", "EFFECTIVE_LOCAL_COMPLIANCE",
  "CONTESTED_CONTROL", "UNKNOWN_EFFECTIVE_CONTROL",
];

// Painan's own relations use object_actor_id; Natal/Koto Tangah/Tiku/Sillida use object_id.
// Read once through this helper everywhere instead of hardcoding either field name.
function objectIdOf(rel) {
  return rel.object_id != null ? rel.object_id : rel.object_actor_id;
}

function labelOf(entity) {
  if (!entity) return undefined;
  return entity.label || entity.normalized_label || entity.source_label;
}

let CASES = {};            // caseId -> { artifact, actorById, validRelations, renderErrors }
let CURRENT_CASE = CASES_DEF[0].id;

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

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s == null ? "" : s;
  return div.innerHTML;
}

function disclosureDrawer(levelClass, summaryText, bodyNode) {
  const details = el("details", { class: "disclosure " + levelClass });
  details.appendChild(el("summary", { text: summaryText }));
  const body = el("div", { class: "disclosure-body" }, [bodyNode]);
  details.appendChild(body);
  return details;
}

function setLoadStatus(kind, text) {
  const box = document.getElementById("load-status");
  box.className = kind;
  box.textContent = text;
}

/* ---------------------------------------------------------------------- */
/* Load + per-case structural validation                                    */
/* ---------------------------------------------------------------------- */

function validateRelation(rel, actorById, renderErrors) {
  const objId = objectIdOf(rel);
  if (!rel.relation_id || !rel.subject_actor_id || objId == null || !rel.relation_type) {
    renderErrors.push({ where: "relation " + (rel.relation_id || "(no id)"),
      detail: "missing required field(s) among relation_id/subject_actor_id/object_id(_actor_id)/relation_type" });
    return false;
  }
  if (FORBIDDEN_RELATION_TYPES.includes(rel.relation_type)) {
    renderErrors.push({ where: "relation " + rel.relation_id,
      detail: "forbidden relation_type '" + rel.relation_type + "' — patron-client must never be an edge" });
    return false;
  }
  if (!AUTHORIZED_RELATION_TYPES.includes(rel.relation_type)) {
    renderErrors.push({ where: "relation " + rel.relation_id,
      detail: "unapproved relation_type '" + rel.relation_type + "' — outside the closed 18-value V2/V2.1 " +
        "vocabulary (this is a known, disclosed, expected finding for some cases — see the migration audit)" });
    return false;
  }
  if (!actorById[rel.subject_actor_id] || !actorById[objId]) {
    renderErrors.push({ where: "relation " + rel.relation_id,
      detail: "unresolved endpoint (subject=" + rel.subject_actor_id + ", object=" + objId + ") — " +
        "known, disclosed for cases using a Commodity id as object_id (see the migration audit)" });
    return false;
  }
  return true;
}

async function loadOneCase(def) {
  let res;
  try {
    res = await fetch(def.path, { cache: "no-store" });
  } catch (e) {
    return { error: "FATAL fetch error for " + def.label + ": " + e.message };
  }
  if (!res.ok) {
    return { error: "FATAL: " + def.label + " fetch returned HTTP " + res.status };
  }
  let data;
  try {
    data = await res.json();
  } catch (e) {
    return { error: "FATAL: " + def.label + " artifact is not valid JSON (" + e.message + ")" };
  }
  if (!Array.isArray(data.actors) || !Array.isArray(data.relations)) {
    return { error: "FATAL: " + def.label + " artifact missing required top-level 'actors' or 'relations' array." };
  }

  // Endpoint resolution includes locations, mirroring the Python generalized validator's own
  // `known = _actor_ids(artifact) | _location_ids(artifact)` (relations may target a Location,
  // e.g. USES_MILITARY_FORCE_AGAINST a fort/nagari, or CLAIMS_COMMODITY_MONOPOLY over a
  // salt-refinery location). The Actors view below iterates data.actors directly, so merging
  // locations into this lookup map does not make a location render as an actor card.
  const actorById = {};
  data.actors.forEach((a) => { actorById[a.actor_id] = a; });
  (data.locations || []).forEach((loc) => { actorById[loc.location_id] = loc; });
  const renderErrors = [];
  const validRelations = data.relations.filter((r) => validateRelation(r, actorById, renderErrors));

  return { artifact: data, actorById, validRelations, renderErrors };
}

async function loadAllCases() {
  const results = await Promise.all(CASES_DEF.map(loadOneCase));
  const loadErrors = [];
  CASES_DEF.forEach((def, i) => {
    const r = results[i];
    if (r.error) {
      loadErrors.push(r.error);
      CASES[def.id] = { artifact: null, actorById: {}, validRelations: [], renderErrors: [] };
    } else {
      CASES[def.id] = r;
    }
  });

  const okCount = CASES_DEF.filter((d) => CASES[d.id].artifact).length;
  if (loadErrors.length > 0) {
    setLoadStatus("error", loadErrors.length + " of " + CASES_DEF.length + " cases failed to load. " +
      loadErrors.join(" | ") +
      ". This prototype must be served over http(s) (e.g. `python3 -m http.server` from the repository " +
      "root) — opening index.html directly via file:// blocks fetch() in most browsers.");
  } else {
    setLoadStatus("ok", okCount + "/" + CASES_DEF.length + " cases loaded read-only.");
  }
}

/* ---------------------------------------------------------------------- */
/* View: Case Index                                                         */
/* ---------------------------------------------------------------------- */

function computeNamespaceDiagnostic() {
  const seenIn = {}; // actor_id -> [case labels]
  CASES_DEF.forEach((def) => {
    const c = CASES[def.id];
    if (!c.artifact) return;
    Object.keys(c.actorById).forEach((aid) => {
      seenIn[aid] = seenIn[aid] || [];
      seenIn[aid].push(def.label);
    });
  });
  return Object.entries(seenIn).filter(([, labels]) => labels.length > 1);
}

function renderCaseIndex(root) {
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "caseindex-heading", text: "Case Index" }));
  root.appendChild(el("div", { class: "warning-box", text:
    "RESEARCH-ONLY WARNING: This page renders 5 reviewed, nonproduction Draft V2.1 artifacts, one " +
    "case at a time. It is not the public Atlas and does not represent Atlas coverage generally. " +
    "Cases are never merged — switching cases fully replaces the actor/relation set in every other " +
    "view; nothing here builds one shared cross-case graph." }));

  const table = el("table", { class: "case-index-table" });
  const thead = el("thead", {}, [el("tr", {}, [
    el("th", { text: "Case" }), el("th", { text: "Actors" }), el("th", { text: "Valid relations" }),
    el("th", { text: "V2.1 entities" }), el("th", { text: "Generalized validator (informational)" }),
  ])]);
  table.appendChild(thead);
  const tbody = el("tbody");
  CASES_DEF.forEach((def) => {
    const c = CASES[def.id];
    if (!c.artifact) {
      tbody.appendChild(el("tr", {}, [el("td", { text: def.label }), el("td", { text: "—", colspan: "4" })]));
      return;
    }
    const v21Count = (c.artifact.commercial_rights || []).length + (c.artifact.right_modifications || []).length +
      (c.artifact.command_observations || []).length + (c.artifact.operation_participations || []).length;
    const statusOk = c.renderErrors.length === 0;
    const row = el("tr", {}, [
      el("td", {}, [el("button", { type: "button", class: "case-btn", "data-case": def.id, text: def.label })]),
      el("td", { text: String(c.artifact.actors.length) }),
      el("td", { text: c.validRelations.length + " / " + c.artifact.relations.length }),
      el("td", { text: String(v21Count) }),
      el("td", { class: statusOk ? "status-pass" : "status-fail",
        text: statusOk ? "0 flagged relations" : c.renderErrors.length + " flagged (see that case's Overview)" }),
    ]);
    tbody.appendChild(row);
  });
  table.appendChild(tbody);
  root.appendChild(table);

  root.appendChild(el("p", { text: "Click a case name above, or use the case switcher bar, to view it in the " +
    "other 7 tabs." }));

  const nsPairs = computeNamespaceDiagnostic();
  root.appendChild(el("h2", { text: "Cross-case actor_id diagnostic (informational, not an error)" }));
  const nsPanel = el("div", { class: "namespace-panel" });
  if (nsPairs.length === 0) {
    nsPanel.appendChild(el("p", { text: "No actor_id string is reused across more than one case's own file." }));
  } else {
    nsPanel.appendChild(el("p", { text:
      "Per CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md SS5, the check below is a namespace-recurrence " +
      "report, not a merge: each occurrence below is a SEPARATE, independently-authored actor object in " +
      "its own case file (e.g. the VOC institution recurring is expected and correct — Draft V2's own " +
      "Institution entity is meant to recur across cases). This page never treats two occurrences as the " +
      "same in-memory object; DEC-01's own safeguard (no automatic actor merge) applies fully here." }));
    nsPairs.forEach(([aid, labels]) => {
      nsPanel.appendChild(el("div", { class: "shared-id-row" }, [
        el("strong", { text: aid }), document.createTextNode(" — appears independently in: " + labels.join(", ")),
      ]));
    });
  }
  root.appendChild(nsPanel);

  // wire the case-name buttons in the table
  root.querySelectorAll("button[data-case]").forEach((btn) => {
    btn.addEventListener("click", () => switchCase(btn.dataset.case));
  });
}

/* ---------------------------------------------------------------------- */
/* View: Overview                                                           */
/* ---------------------------------------------------------------------- */

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

function renderOverview(root, caseId) {
  const c = CASES[caseId];
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "overview-heading", text: "Overview — " + caseLabel(caseId) }));
  if (!c.artifact) { root.appendChild(el("p", { text: "This case failed to load." })); return; }
  const validRelations = c.validRelations;

  root.appendChild(el("div", { class: "warning-box", text:
    "RESEARCH-ONLY WARNING: nonproduction artifact for one case; every relation below is bounded, " +
    "source-linked, and marked with its own evidence status — nothing here is a settled verdict." }));

  const stats = el("div", { class: "stat-grid" });
  const tile = (n, label) => el("div", { class: "stat-tile" }, [
    el("div", { class: "n", text: String(n) }), el("div", { class: "label", text: label }),
  ]);
  stats.appendChild(tile(c.artifact.actors.length, "Actors"));
  stats.appendChild(tile(validRelations.length, "Relations (valid)"));
  const dates = validRelations.map((r) => r.valid_from).filter(Boolean).sort();
  stats.appendChild(tile(dates.length ? (dates[0] + " → " + dates[dates.length - 1]) : "n/a", "Date range"));
  root.appendChild(el("div", { class: "card" }, [stats]));

  const typeDist = {};
  validRelations.forEach((r) => { typeDist[r.relation_type] = (typeDist[r.relation_type] || 0) + 1; });
  root.appendChild(el("h2", { text: "Relation-type distribution" }));
  root.appendChild(distTable(typeDist));

  const cecDist = {};
  validRelations.forEach((r) => { cecDist[r.claim_or_effective_control] = (cecDist[r.claim_or_effective_control] || 0) + 1; });
  root.appendChild(el("h2", { text: "Claim versus effective-control distribution" }));
  root.appendChild(distTable(cecDist));

  if (c.renderErrors.length > 0) {
    root.appendChild(el("h2", { text: "Render-time validation errors (record-level, not fatal)" }));
    const ul = el("ul", { class: "rel-list" });
    c.renderErrors.forEach((e) => ul.appendChild(el("li", { text: e.where + ": " + e.detail })));
    root.appendChild(el("div", { class: "warning-box" }, [ul]));
  }
}

/* ---------------------------------------------------------------------- */
/* View: Actors                                                             */
/* ---------------------------------------------------------------------- */

function relList(relations, otherEndpointField, actorById) {
  const ul = el("ul", { class: "rel-list" });
  if (relations.length === 0) { ul.appendChild(el("li", { text: "(none)" })); return ul; }
  relations.forEach((r) => {
    const otherId = otherEndpointField === "object" ? objectIdOf(r) : r[otherEndpointField];
    const other = actorById[otherId];
    const li = el("li", {});
    li.appendChild(document.createTextNode(r.relation_type + " — " + (other ? labelOf(other) : otherId) +
      " (" + r.valid_from + (r.valid_to ? " → " + r.valid_to : " → open") + ") "));
    li.appendChild(badge(r.explicit_or_inferred === "EXPLICIT_STRATEGY" ? "explicit" : "inferred",
      r.explicit_or_inferred === "EXPLICIT_STRATEGY" ? "badge-explicit" : "badge-inferred"));
    ul.appendChild(li);
  });
  return ul;
}

function renderActors(root, caseId) {
  const c = CASES[caseId];
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "actors-heading", text: "Actors — " + caseLabel(caseId) }));
  if (!c.artifact) { root.appendChild(el("p", { text: "This case failed to load." })); return; }
  root.appendChild(el("p", { class: "level3-notice", text:
    "Actors are individually named factions, institutions, or broker individuals — never a " +
    "territorial population or a merged regional label." }));

  c.artifact.actors.forEach((actor) => {
    const incoming = c.validRelations.filter((r) => objectIdOf(r) === actor.actor_id);
    const outgoing = c.validRelations.filter((r) => r.subject_actor_id === actor.actor_id);
    const label = labelOf(actor) || actor.actor_id;

    const card = el("div", { class: "card actor-card" });
    card.appendChild(el("h3", { text: label + "  " + (actor.researcher_review_required ? "⚠" : "") }));
    card.appendChild(el("div", { class: "actor-type", text: (actor.actor_type || "Actor") + " · actor_id: " + actor.actor_id }));
    if (actor.notes) card.appendChild(el("p", { text: actor.notes }));

    card.appendChild(el("h4", { text: "Outgoing relations (" + outgoing.length + ")" }));
    card.appendChild(relList(outgoing, "object", c.actorById));
    card.appendChild(el("h4", { text: "Incoming relations (" + incoming.length + ")" }));
    card.appendChild(relList(incoming, "subject_actor_id", c.actorById));

    // Draft V2.1 SS4a identity-continuity fields — Research-Only, closed by default
    const hasV21Identity = actor.mandate_status || actor.mandate_scope ||
      actor.identity_continuity_status || (actor.explicit_non_identity_with && actor.explicit_non_identity_with.length);
    if (hasV21Identity) {
      const body = el("div", {});
      if (actor.mandate_status) body.appendChild(el("p", { html: "<strong>mandate_status:</strong> " + escapeHtml(actor.mandate_status) }));
      if (actor.mandate_scope) body.appendChild(el("p", { html: "<strong>mandate_scope:</strong> " + escapeHtml(actor.mandate_scope) }));
      if (actor.identity_continuity_status) body.appendChild(el("p", { html: "<strong>identity_continuity_status:</strong> " + escapeHtml(actor.identity_continuity_status) }));
      (actor.explicit_non_identity_with || []).forEach((n) => {
        body.appendChild(el("p", { html: "<strong>explicitly NOT identical to:</strong> " + escapeHtml(n.actor_id) +
          " — " + escapeHtml(n.rationale) }));
      });
      card.appendChild(disclosureDrawer("level2", "Show Draft V2.1 identity-continuity fields (Research-Only)", body));
    }

    root.appendChild(card);
  });
}

/* ---------------------------------------------------------------------- */
/* View: Relation Timeline                                                  */
/* ---------------------------------------------------------------------- */

function parseDateForAxis(s, fallbackEnd) {
  if (!s) return fallbackEnd ? 9999 : 1600;
  const parts = String(s).split("-").map(Number);
  return parts[0] + (parts[1] ? parts[1] / 12 : 0);
}

function renderTimeline(root, caseId) {
  const c = CASES[caseId];
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "timeline-heading", text: "Relation Timeline — " + caseLabel(caseId) }));
  if (!c.artifact) { root.appendChild(el("p", { text: "This case failed to load." })); return; }
  const validRelations = c.validRelations;
  root.appendChild(el("p", { text: "Overlapping validity ranges are shown as separate, non-overwriting bars." }));

  const controls = el("div", { id: "timeline-controls" });
  const actorLabel = el("label", { text: "Filter by actor: " });
  const actorSelect = el("select", { id: "tl-actor-filter" });
  actorSelect.appendChild(el("option", { value: "", text: "All actors" }));
  c.artifact.actors.forEach((a) => actorSelect.appendChild(el("option", { value: a.actor_id, text: labelOf(a) || a.actor_id })));
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

  const starts = validRelations.map((r) => parseDateForAxis(r.valid_from)).filter((n) => n > 1000);
  const ends = validRelations.map((r) => r.valid_to ? parseDateForAxis(r.valid_to, true) : null).filter((n) => n && n < 9999);
  const minYear = starts.length ? Math.min(...starts) - 1 : 1600;
  const maxYear = ends.length ? Math.max(...ends, ...starts) + 1 : (starts.length ? Math.max(...starts) + 5 : 1800);

  function draw() {
    listWrap.innerHTML = "";
    const actorFilter = actorSelect.value;
    const typeFilter = typeSelect.value;
    const rows = validRelations.filter((r) =>
      (!actorFilter || r.subject_actor_id === actorFilter || objectIdOf(r) === actorFilter) &&
      (!typeFilter || r.relation_type === typeFilter)
    ).sort((a, b) => parseDateForAxis(a.valid_from) - parseDateForAxis(b.valid_from));

    if (rows.length === 0) { listWrap.appendChild(el("p", { text: "No relations match this filter." })); return; }

    rows.forEach((r) => {
      const row = el("div", { class: "timeline-row" });
      const subj = c.actorById[r.subject_actor_id], obj = c.actorById[objectIdOf(r)];
      const subjLabel = subj ? (labelOf(subj)) : r.subject_actor_id;
      const objLabel = obj ? (labelOf(obj)) : objectIdOf(r);
      row.appendChild(el("div", { class: "tl-label" }, [
        document.createTextNode(r.relation_type), el("br", {}),
        document.createTextNode(subjLabel + " → " + objLabel),
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
        title: r.relation_id + " (" + (r.date_precision || "precision unknown") + ")",
        tabindex: "0",
        "aria-label": r.relation_type + " from " + subjLabel + " to " + objLabel + ", " + r.valid_from +
          (r.valid_to ? " to " + r.valid_to : ", open end"),
      }, [document.createTextNode(String(r.valid_from))]);
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

function renderNetwork(root, caseId) {
  const c = CASES[caseId];
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "network-heading", text: "Relation Network — " + caseLabel(caseId) }));
  if (!c.artifact) { root.appendChild(el("p", { text: "This case failed to load." })); return; }
  const validRelations = c.validRelations;
  root.appendChild(el("p", { text:
    "Directed research diagram, this case only. No territorial shapes. No PATRON_OF/CLIENT_OF edge " +
    "ever. CommandObservation and CommercialRight (Draft V2.1 Research-Only entities) are NEVER drawn " +
    "as an edge here — see the V2.1 Additions tab for those, listed only, never graphed." }));

  const svgNS = "http://www.w3.org/2000/svg";
  const width = 900, height = 560, cx = width / 2, cy = height / 2, radius = 210;
  const actors = c.artifact.actors;
  const pos = {};
  actors.forEach((a, i) => {
    const angle = (i / actors.length) * 2 * Math.PI - Math.PI / 2;
    pos[a.actor_id] = { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) };
  });

  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("viewBox", "0 0 " + width + " " + height);
  svg.setAttribute("width", "100%");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Directed diagram of " + caseLabel(caseId) + " actors and relations");

  const defs = document.createElementNS(svgNS, "defs");
  const marker = document.createElementNS(svgNS, "marker");
  marker.setAttribute("id", "arrowhead");
  marker.setAttribute("markerWidth", "8"); marker.setAttribute("markerHeight", "8");
  marker.setAttribute("refX", "7"); marker.setAttribute("refY", "3"); marker.setAttribute("orient", "auto");
  const arrowPath = document.createElementNS(svgNS, "path");
  arrowPath.setAttribute("d", "M0,0 L0,6 L7,3 z"); arrowPath.setAttribute("fill", "#a6acb8");
  marker.appendChild(arrowPath); defs.appendChild(marker); svg.appendChild(defs);

  const pairCounts = {};
  validRelations.forEach((r) => {
    const key = [r.subject_actor_id, objectIdOf(r)].sort().join("|");
    pairCounts[key] = pairCounts[key] || [];
    pairCounts[key].push(r);
  });

  Object.values(pairCounts).forEach((group) => {
    group.forEach((r, idx) => {
      const p1 = pos[r.subject_actor_id], p2 = pos[objectIdOf(r)];
      if (!p1 || !p2) return;
      const mx = (p1.x + p2.x) / 2, my = (p1.y + p2.y) / 2;
      const offset = (idx - (group.length - 1) / 2) * 60;
      const dx = p2.y - p1.y, dy = p1.x - p2.x;
      const len = Math.hypot(dx, dy) || 1;
      const ctrlX = mx + (dx / len) * offset, ctrlY = my + (dy / len) * offset;
      const labelOffset = offset * 1.35;
      const labelX = mx + (dx / len) * labelOffset, labelY = my + (dy / len) * labelOffset;
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
      const subjA = c.actorById[r.subject_actor_id], objA = c.actorById[objectIdOf(r)];
      path.setAttribute("aria-label", r.relation_type + ": " + (subjA ? (labelOf(subjA)) : r.subject_actor_id) +
        " to " + (objA ? (labelOf(objA)) : objectIdOf(r)));
      const titleEl = document.createElementNS(svgNS, "title");
      titleEl.textContent = r.relation_type + " (" + r.relation_id + ")";
      path.appendChild(titleEl);
      svg.appendChild(path);

      const labelText = r.relation_type.replace(/_/g, " ");
      const approxWidth = labelText.length * 5.2;
      const bg = document.createElementNS(svgNS, "rect");
      bg.setAttribute("x", String(labelX - approxWidth / 2 - 3));
      bg.setAttribute("y", String(labelY - 11));
      bg.setAttribute("width", String(approxWidth + 6)); bg.setAttribute("height", "13");
      bg.setAttribute("fill", "#171a21"); bg.setAttribute("opacity", "0.85");
      svg.appendChild(bg);

      const labelEl = document.createElementNS(svgNS, "text");
      labelEl.setAttribute("x", String(labelX)); labelEl.setAttribute("y", String(labelY - 2));
      labelEl.setAttribute("font-size", "9"); labelEl.setAttribute("fill", "#c7ccd6");
      labelEl.setAttribute("text-anchor", "middle"); labelEl.textContent = labelText;
      svg.appendChild(labelEl);
    });
  });

  actors.forEach((a) => {
    const p = pos[a.actor_id];
    const g = document.createElementNS(svgNS, "g");
    const circle = document.createElementNS(svgNS, "circle");
    circle.setAttribute("cx", String(p.x)); circle.setAttribute("cy", String(p.y)); circle.setAttribute("r", "26");
    circle.setAttribute("fill", "#171a21");
    circle.setAttribute("stroke", a.researcher_review_required ? "#ff6b6b" : "#f2c14e");
    circle.setAttribute("stroke-width", "2");
    g.appendChild(circle);
    const text = document.createElementNS(svgNS, "text");
    text.setAttribute("x", String(p.x)); text.setAttribute("y", String(p.y + 40));
    text.setAttribute("font-size", "11"); text.setAttribute("fill", "#e8e8ec"); text.setAttribute("text-anchor", "middle");
    text.textContent = labelOf(a) || a.actor_id;
    g.appendChild(text);
    svg.appendChild(g);
  });

  root.appendChild(el("div", { id: "network-svg-wrap" }, [svg]));

  root.appendChild(el("div", { id: "network-legend" }, [
    el("span", {}, [el("span", { class: "legend-swatch" }), document.createTextNode("explicit relation")]),
    el("span", {}, [el("span", { class: "legend-swatch inferred" }), document.createTextNode("inferred")]),
    el("span", {}, [el("span", { class: "legend-swatch contested" }), document.createTextNode("contested control")]),
    el("span", {}, [document.createTextNode("gold border = OK; red border = researcher_review_required")]),
  ]));

  root.appendChild(el("h2", { text: "Relation detail (progressive disclosure)" }));
  validRelations.forEach((r) => root.appendChild(relationDetailPanel(r, c.actorById)));
}

/* ---------------------------------------------------------------------- */
/* Shared: relation detail panel with Level 1 / 2 / 3 disclosure            */
/* ---------------------------------------------------------------------- */

function relationDetailPanel(r, actorById) {
  const subj = actorById[r.subject_actor_id], obj = actorById[objectIdOf(r)];
  const subjLabel = subj ? (labelOf(subj)) : r.subject_actor_id;
  const objLabel = obj ? (labelOf(obj)) : objectIdOf(r);
  const card = el("div", { class: "card" });

  const l1 = el("div", {});
  l1.appendChild(el("h3", { text: subjLabel + " — " + r.relation_type.replace(/_/g, " ") + " — " + objLabel }));
  l1.appendChild(el("p", { text: r.valid_from + (r.valid_to ? " → " + r.valid_to : " → open") +
    "  (" + (r.date_precision || "precision unknown") + ")" }));
  if (r.evidence_strength) l1.appendChild(badge(r.evidence_strength, "badge-" + (r.evidence_strength === "HIGH" ? "explicit" : "inferred")));
  if (r.explicit_or_inferred) l1.appendChild(badge(r.explicit_or_inferred, r.explicit_or_inferred === "EXPLICIT_STRATEGY" ? "badge-explicit" : "badge-inferred"));
  card.appendChild(l1);

  const l2body = el("div", {});
  if (r.source_statement_summary) l2body.appendChild(el("p", { html: "<strong>Source statement:</strong> " + escapeHtml(r.source_statement_summary) }));
  if (r.historical_reconstruction) l2body.appendChild(el("p", { html: "<strong>Historical reconstruction:</strong> " + escapeHtml(r.historical_reconstruction) }));
  if (r.source_document_ids) l2body.appendChild(el("p", { html: "<strong>Source document IDs:</strong> " + r.source_document_ids.join(", ") }));
  if (r.source_passage_locator) l2body.appendChild(el("p", { html: "<strong>Passage locator:</strong> " + escapeHtml(r.source_passage_locator) }));
  if (r.provenance_status) l2body.appendChild(el("p", { html: "<strong>Provenance status:</strong> " + r.provenance_status }));
  if (r.claim_or_effective_control) l2body.appendChild(el("p", { html: "<strong>Claim vs effective control:</strong> " + r.claim_or_effective_control }));
  if (r.interpretive_status) l2body.appendChild(el("p", { html: "<strong>Interpretive status:</strong> " + r.interpretive_status }));
  l2body.appendChild(el("p", { html: "<strong>Researcher review required:</strong> " + (r.researcher_review_required ? "YES" : "no") }));
  if (r.resistance_target_actor_id) {
    const t = actorById[r.resistance_target_actor_id];
    l2body.appendChild(el("p", { html: "<strong>resistance_target_actor_id (Draft V2.1):</strong> " +
      escapeHtml(t ? (labelOf(t)) : r.resistance_target_actor_id) +
      " — differs from this relation's own object, per CH-06/DEC-08" }));
  }
  card.appendChild(disclosureDrawer("level2", "Show source & provenance (Level 2)", l2body));

  const l3body = el("div", {});
  l3body.appendChild(el("p", { class: "level3-notice", text:
    "Level 3 research annotation — NOT a confirmed historical fact." }));
  if (r.patron_client_classification) l3body.appendChild(el("p", { html: "<strong>Patron-client classification:</strong> " + escapeHtml(r.patron_client_classification) }));
  if (r.theoretical_annotation) l3body.appendChild(el("p", { html: "<strong>Theoretical annotation:</strong> " + escapeHtml(r.theoretical_annotation) }));
  if (r.resistance_candidate) l3body.appendChild(el("p", { html: "<strong>resistance_candidate:</strong> " + escapeHtml(String(r.resistance_candidate)) }));
  if (r.notes) l3body.appendChild(el("p", { html: "<strong>Notes / limitations:</strong> " + escapeHtml(r.notes) }));
  card.appendChild(disclosureDrawer("level3", "Show theory & interpretation (Level 3 — research annotation only)", l3body));

  if (r.public_display_summary) {
    card.appendChild(disclosureDrawer("level1", "Show proposed public-copy summary",
      el("p", { text: r.public_display_summary })));
  }
  return card;
}

/* ---------------------------------------------------------------------- */
/* View: Claim vs Effective Control                                        */
/* ---------------------------------------------------------------------- */

function renderClaimControl(root, caseId) {
  const c = CASES[caseId];
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "claimcontrol-heading", text: "Claim versus Effective Control — " + caseLabel(caseId) }));
  if (!c.artifact) { root.appendChild(el("p", { text: "This case failed to load." })); return; }
  root.appendChild(el("p", { text: "A claim or formal agreement does not by itself demonstrate effective control." }));

  const counts = {};
  c.validRelations.forEach((r) => { counts[r.claim_or_effective_control] = (counts[r.claim_or_effective_control] || 0) + 1; });

  const list = el("div", { class: "vocab-list" });
  CLAIM_OR_EFFECTIVE_CONTROL_VOCAB.forEach((v) => {
    const active = !!counts[v];
    const item = el("div", { class: "vocab-item" + (active ? " active" : "") });
    item.appendChild(el("div", { text: v }));
    item.appendChild(el("div", { class: "count", text: active ? String(counts[v]) + " relation(s)" : "not present in this case" }));
    list.appendChild(item);
  });
  root.appendChild(list);

  root.appendChild(el("h2", { text: "Relations by claim/control category" }));
  CLAIM_OR_EFFECTIVE_CONTROL_VOCAB.filter((v) => counts[v]).forEach((v) => {
    root.appendChild(el("h3", { text: v }));
    c.validRelations.filter((r) => r.claim_or_effective_control === v).forEach((r) => root.appendChild(relationDetailPanel(r, c.actorById)));
  });
}

/* ---------------------------------------------------------------------- */
/* View: V2.1 Additions (new — research-only, never rendered as an edge)    */
/* ---------------------------------------------------------------------- */

function v21EntityCard(title, fields, entry) {
  const card = el("div", { class: "card v21-entity-card" });
  card.appendChild(el("h4", { text: title }));
  const body = el("div", {});
  fields.forEach((f) => {
    if (entry[f] === undefined) return;
    let v = entry[f];
    if (Array.isArray(v)) v = v.join(", ");
    body.appendChild(el("p", { html: "<strong>" + f + ":</strong> " + escapeHtml(String(v)) }));
  });
  card.appendChild(disclosureDrawer("level2", "Show " + title + " fields (RESEARCH-ONLY)", body));
  return card;
}

function renderV21Additions(root, caseId) {
  const c = CASES[caseId];
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "v21additions-heading", text: "V2.1 Additions — " + caseLabel(caseId) }));
  if (!c.artifact) { root.appendChild(el("p", { text: "This case failed to load." })); return; }
  root.appendChild(el("div", { class: "warning-box", text:
    "RESEARCH-ONLY. Every entity below is a Draft V2.1 addition (DEC-04/DEC-08/DEC-09/DEC-10), bound " +
    "by DEC-16's research-only boundary. None is rendered as a graph edge anywhere on this page — " +
    "CommercialRight/RightModification/CommandObservation/OperationParticipation are deliberately kept " +
    "off the Relation Network view (see Draft V2.1 SS2/SS4c's own non-negotiable safety rule)." }));

  const rights = c.artifact.commercial_rights || [];
  const mods = c.artifact.right_modifications || [];
  const cmds = c.artifact.command_observations || [];
  const ops = c.artifact.operation_participations || [];

  root.appendChild(el("h2", { text: "CommercialRight (" + rights.length + ")" }));
  if (rights.length === 0) root.appendChild(el("p", { class: "v21-empty-state", text: "None in this case." }));
  rights.forEach((r) => root.appendChild(v21EntityCard(r.right_id || "CommercialRight",
    ["right_id", "holder_actor_id", "granting_actor_id", "concerns_relation_type", "commodity",
     "provenance_status", "evidence_strength", "valid_from", "valid_to"], r)));

  root.appendChild(el("h2", { text: "RightModification (" + mods.length + ")" }));
  if (mods.length === 0) root.appendChild(el("p", { class: "v21-empty-state", text: "None in this case." }));
  mods.forEach((m) => root.appendChild(v21EntityCard(m.modification_id || "RightModification",
    ["modification_id", "right_id", "action", "acting_actor_id", "affected_actor_id", "modification_date"], m)));

  root.appendChild(el("h2", { text: "CommandObservation (" + cmds.length + ")" }));
  if (cmds.length === 0) root.appendChild(el("p", { class: "v21-empty-state", text: "None in this case." }));
  cmds.forEach((o) => root.appendChild(v21EntityCard(o.observation_id || "CommandObservation",
    ["observation_id", "commanding_actor_id", "commanded_actor_id", "coercion_status", "ability_to_refuse",
     "dependency_status", "voice_availability", "constrained_agency", "political_intent"], o)));

  root.appendChild(el("h2", { text: "OperationParticipation (" + ops.length + ")" }));
  if (ops.length === 0) root.appendChild(el("p", { class: "v21-empty-state", text: "None in this case." }));
  ops.forEach((p) => root.appendChild(v21EntityCard(p.participation_id || "OperationParticipation",
    ["participation_id", "command_observation_id", "participant_actor_id", "event_id", "role_as_written"], p)));
}

/* ---------------------------------------------------------------------- */
/* View: Public-Copy Preview                                                */
/* ---------------------------------------------------------------------- */

function renderPublicCopy(root, caseId) {
  const c = CASES[caseId];
  root.innerHTML = "";
  root.appendChild(el("h1", { id: "publiccopy-heading", text: "Public-Copy Preview — " + caseLabel(caseId) }));
  if (!c.artifact) { root.appendChild(el("p", { text: "This case failed to load." })); return; }
  root.appendChild(el("p", { text:
    "Each relation's interpretive layers, shown side by side. Only the public-display summary layer " +
    "is suitable for a Level-1 map label; the others are research content." }));

  c.validRelations.forEach((r) => {
    const subj = c.actorById[r.subject_actor_id], obj = c.actorById[objectIdOf(r)];
    const subjLabel = subj ? (labelOf(subj)) : r.subject_actor_id;
    const objLabel = obj ? (labelOf(obj)) : objectIdOf(r);
    root.appendChild(el("h3", { text: subjLabel + " → " + objLabel + " (" + r.relation_type + ")" }));
    const grid = el("div", { class: "layer-compare" });
    grid.appendChild(el("div", { class: "layer-card source" }, [el("h4", { text: "Source statement" }), el("p", { text: r.source_statement_summary || "(n/a)" })]));
    grid.appendChild(el("div", { class: "layer-card reconstruction" }, [el("h4", { text: "Historical reconstruction" }), el("p", { text: r.historical_reconstruction || "(n/a)" })]));
    grid.appendChild(el("div", { class: "layer-card theory" }, [el("h4", { text: "Theoretical annotation (Level 3)" }), el("p", { text: r.theoretical_annotation || "(n/a)" })]));
    grid.appendChild(el("div", { class: "layer-card public" }, [el("h4", { text: "Public-display summary" }), el("p", { text: r.public_display_summary || "(n/a)" })]));
    root.appendChild(el("div", { class: "card" }, [grid]));
  });
}

/* ---------------------------------------------------------------------- */
/* Case switcher + navigation + bootstrap                                   */
/* ---------------------------------------------------------------------- */

function caseLabel(caseId) {
  const def = CASES_DEF.find((d) => d.id === caseId);
  return def ? def.label : caseId;
}

const VIEW_RENDERERS = {
  caseindex: (root) => renderCaseIndex(root),
  overview: (root, caseId) => renderOverview(root, caseId),
  actors: (root, caseId) => renderActors(root, caseId),
  timeline: (root, caseId) => renderTimeline(root, caseId),
  network: (root, caseId) => renderNetwork(root, caseId),
  claimcontrol: (root, caseId) => renderClaimControl(root, caseId),
  v21additions: (root, caseId) => renderV21Additions(root, caseId),
  publiccopy: (root, caseId) => renderPublicCopy(root, caseId),
};

function currentViewName() {
  const active = document.querySelector(".nav-btn[aria-current='page']");
  return active ? active.dataset.view : "caseindex";
}

function renderCurrentView() {
  const view = currentViewName();
  const root = document.getElementById("view-" + view);
  VIEW_RENDERERS[view](root, CURRENT_CASE);
}

function switchCase(caseId) {
  CURRENT_CASE = caseId;
  document.querySelectorAll("#case-switcher .case-btn").forEach((b) => {
    b.setAttribute("aria-current", b.dataset.case === caseId ? "true" : "false");
  });
  renderCurrentView();
}

function setupCaseSwitcher() {
  const box = document.getElementById("case-switcher");
  box.innerHTML = "";
  CASES_DEF.forEach((def) => {
    const btn = el("button", { type: "button", class: "case-btn", "data-case": def.id,
      "aria-current": def.id === CURRENT_CASE ? "true" : "false", text: def.label });
    btn.addEventListener("click", () => switchCase(def.id));
    box.appendChild(btn);
  });
}

function setupNav() {
  const buttons = Array.from(document.querySelectorAll(".nav-btn"));
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.removeAttribute("aria-current"));
      btn.setAttribute("aria-current", "page");
      document.querySelectorAll(".view").forEach((v) => { v.hidden = true; });
      const section = document.getElementById("view-" + btn.dataset.view);
      section.hidden = false;
      VIEW_RENDERERS[btn.dataset.view](section, CURRENT_CASE);
      section.focus?.();
    });
  });
}

(async function main() {
  setupNav();
  await loadAllCases();
  setupCaseSwitcher();
  renderCurrentView();
})();
