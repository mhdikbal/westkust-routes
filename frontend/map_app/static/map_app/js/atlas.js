"use strict";

/* ─────────────────────────────────────────────────────────────────────────────
   Constants
   ───────────────────────────────────────────────────────────────────────────── */
const API = "/api";

const FORT_COORDS = {
  "Barus":          [2.0144566, 98.3993198],
  "Air Bangis":     [0.1974875, 99.3755554],
  "Padang":         [-0.9655545, 100.3538894],
  "Pulau Cingkuak": [-1.3531125710383205, 100.55921198502948],
  "Air Haji":       [-1.9339388, 100.8669821],
  "Batavia":        [-6.1165019, 106.8165121],
};

// Waypoints along actual sea lanes — prevents routes from cutting through Sumatra.
// Format: [lat, lng]. Western ports → Batavia route: Indian Ocean → Sunda Strait.
// Eastern ports → Batavia route: south through Java Sea.
const SEA_WAYPOINTS = {
  "Barus→Batavia":          [[-1.0, 96.5], [-5.2, 100.8], [-5.9, 105.4]],
  "Air Bangis→Batavia":     [[-2.0, 97.8], [-5.2, 101.0], [-5.9, 105.4]],
  "Padang→Batavia":         [[-3.2, 99.0], [-5.4, 101.5], [-5.9, 105.4]],
  "Pulau Cingkuak→Batavia": [[-3.2, 99.2], [-5.4, 101.5], [-5.9, 105.4]],
  "Air Haji→Batavia":       [[-3.5, 99.5], [-5.5, 101.8], [-5.9, 105.4]],
  "Batavia→Barus":          [[-5.9, 105.4], [-5.2, 100.8], [-1.0, 96.5]],
  "Batavia→Air Bangis":     [[-5.9, 105.4], [-5.2, 101.0], [-2.0, 97.8]],
  "Batavia→Padang":         [[-5.9, 105.4], [-5.4, 101.5], [-3.2, 99.0]],
  "Batavia→Pulau Cingkuak": [[-5.9, 105.4], [-5.4, 101.5], [-3.2, 99.2]],
  "Batavia→Air Haji":       [[-5.9, 105.4], [-5.5, 101.8], [-3.5, 99.5]],
  // Pelabuhan pantai-barat yg ditambah belakangan + node regional Dagh-register —
  // jalur laut sama dgn koridor Padang/Cingkuak (Samudra Hindia → Selat Sunda).
  "Tiku→Batavia":                 [[-3.0, 98.8], [-5.4, 101.5], [-5.9, 105.4]],
  "Batavia→Tiku":                 [[-5.9, 105.4], [-5.4, 101.5], [-3.0, 98.8]],
  "Pariaman→Batavia":             [[-3.1, 98.9], [-5.4, 101.5], [-5.9, 105.4]],
  "Batavia→Pariaman":             [[-5.9, 105.4], [-5.4, 101.5], [-3.1, 98.9]],
  "Salido→Batavia":               [[-3.2, 99.2], [-5.4, 101.5], [-5.9, 105.4]],
  "Batavia→Salido":               [[-5.9, 105.4], [-5.4, 101.5], [-3.2, 99.2]],
  "Bayang→Batavia":               [[-3.2, 99.2], [-5.4, 101.5], [-5.9, 105.4]],
  "Batavia→Bayang":               [[-5.9, 105.4], [-5.4, 101.5], [-3.2, 99.2]],
  "Painan→Batavia":               [[-3.2, 99.2], [-5.4, 101.5], [-5.9, 105.4]],
  "Batavia→Painan":               [[-5.9, 105.4], [-5.4, 101.5], [-3.2, 99.2]],
  "Pantai Barat Sumatra→Batavia": [[-3.2, 99.0], [-5.4, 101.5], [-5.9, 105.4]],
  "Batavia→Pantai Barat Sumatra": [[-5.9, 105.4], [-5.4, 101.5], [-3.2, 99.0]],
  // Pelayaran PESISIR antar-pelabuhan pantai barat (lapisan surat Dagh-register) —
  // titik tunggal sedikit lepas pantai supaya garis pendek tidak memotong daratan.
  "Padang→Salido":                   [[-1.18, 100.32]],
  "Salido→Padang":                   [[-1.18, 100.32]],
  "Salido→Tiku":                     [[-1.20, 100.15], [-0.62, 99.78]],
  "Padang→Tiku":                     [[-0.68, 99.95]],
  "Tiku→Pulau Cingkuak":             [[-0.70, 99.88], [-1.25, 100.30]],
  "Padang→Pariaman":                 [[-0.83, 100.12]],
  "Pantai Barat Sumatra→Tiku":       [[-0.72, 99.72]],
  "Pantai Barat Sumatra→Padang":     [[-1.05, 100.05]],
  "Pantai Barat Sumatra→Inderapura": [[-1.75, 100.45]],
  // Aceh -- lanjutan koridor Barus ke utara (Samudra Hindia, bukan Selat Malaka).
  // Tanpa waypoint eksplisit, rute jatuh ke fallback bezier yg arah lengkungnya
  // tergantung tanda vektor origin->destination -- bikin Aceh->Batavia & Batavia->Aceh
  // melengkung ke sisi BERLAWANAN (satu lewat pantai barat spt seharusnya, satu lewat
  // utara/Selat Malaka spt kapal yg salah jalan). Lihat feedback_sisir_semua_titik_pemakaian.
  "Aceh→Batavia":  [[3.5, 95.0], [-1.0, 96.5], [-5.2, 100.8], [-5.9, 105.4]],
  "Batavia→Aceh":  [[-5.9, 105.4], [-5.2, 100.8], [-1.0, 96.5], [3.5, 95.0]],
  "Aceh→Tiku":     [[3.5, 95.0], [-1.0, 96.5], [-0.72, 99.72]],
  "Tiku→Aceh":     [[-0.72, 99.72], [-1.0, 96.5], [3.5, 95.0]],
  // Inderapura -- sama koridor Air Haji (garis lintang berdekatan), jatuh ke fallback
  // bezier tanpa ini (pola bug yg sama, lihat komentar Aceh di atas).
  "Inderapura→Batavia": [[-3.7, 99.6], [-5.6, 101.9], [-5.9, 105.4]],
  "Batavia→Inderapura": [[-5.9, 105.4], [-5.6, 101.9], [-3.7, 99.6]],
  "Padang→Inderapura":  [[-1.5, 100.5]],
  "Inderapura→Padang":  [[-1.5, 100.5]],
};

// Icon class per port type for welcome grid
const PORT_ICONS = {
  "Barus": "ti-anchor",
  "Air Bangis": "ti-ship",
  "Padang": "ti-building-fortress",
  "Pulau Cingkuak": "ti-island",
  "Air Haji": "ti-anchor",
  "Jambi": "ti-ship",
  "Palembang": "ti-building-fortress",
  "Lampung": "ti-anchor",
  "Batavia": "ti-building-fortress",
};

const PAGE_SIZE = 20;

/* ─────────────────────────────────────────────────────────────────────────────
   State
   ───────────────────────────────────────────────────────────────────────────── */
let map, routeLines = [], powerStatusLayers = [];
let powerStatusEnabled = false;  // layer status kekuasaan -- opt-in, default OFF
let activeMarker = null, allFortsData = [];
let activeTab = "outbound";
let currentData = { outbound: [], inbound: [], info: "" };
let pageIndex = 0;
let yearFrom = 1620, yearTo = 1790;
let activeDirection = "all";
let activeSource = "all";  // P0.3b — filter provenance (bgb_huygens | daghregister_batavia | globalise_obp)
const MODAL_SOURCE_LABELS = {
  // Modal voyage SELALU tampilkan baris sumber (beda dgn tooltip rute yg cuma tandai non-default)
  bgb_huygens: "BGB Huygens (data terstruktur, terverifikasi)",
  daghregister_batavia: "Dagh-register Batavia",
  globalise_obp: "GLOBALISE OBP (belum diverifikasi penuh)",
};
let glossaryCache = {};   // term (lowercase) → {definition_id, definition_nl, category}
let yearDebounce = null;
let searchDebounce = null;

/* ─────────────────────────────────────────────────────────────────────────────
   Commodity Glossary — lookup dan tooltip
   ───────────────────────────────────────────────────────────────────────────── */
async function fetchGlossaryForTerms(terms) {
  const uncached = terms.filter(t => !(t in glossaryCache));
  if (!uncached.length) return;
  try {
    const res = await fetch(`${API}/glossary/lookup?terms=${encodeURIComponent(uncached.join(","))}`);
    if (!res.ok) return;
    const data = await res.json();
    Object.assign(glossaryCache, data);
    // Tandai yang tidak ada di glossary agar tidak re-fetch
    uncached.forEach(t => { if (!(t in glossaryCache)) glossaryCache[t] = null; });
  } catch (_) { /* silent — tooltip opsional */ }
}

function applyGlossaryTooltips(container) {
  container.querySelectorAll("[data-term]").forEach(el => {
    const term = el.dataset.term;
    const entry = glossaryCache[term];
    if (!entry) return;
    const tip = entry.definition_id || entry.definition_nl || "";
    if (!tip) return;
    el.setAttribute("data-gtip", tip);
    el.classList.add("has-gtip");
  });
}

/* ─────────────────────────────────────────────────────────────────────────────
   Security helpers
   ───────────────────────────────────────────────────────────────────────────── */
function esc(s) {
  if (!s) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function voyageDateText(v, short) {
  // Penanggalan berjenjang: ISO dep/arr -> label tanggal sumber (source_url) -> tahun.
  // Voyage Dagh-register tanpa tahun pasti tetap menampilkan label hari-bulan sumber + jilid.
  if (v.departure_date && v.arrival_date) return `${v.departure_date} → ${v.arrival_date}`;
  if (v.arrival_date)   return short ? v.arrival_date   : `Tiba ${v.arrival_date}`;
  if (v.departure_date) return short ? v.departure_date : `Berangkat ${v.departure_date}`;
  const m = /[?&#]tanggal=([^&]+)/.exec(v.source_url || "");
  if (m) {
    const label = m[1].trim();
    if (v.year) return `${label} ${v.year}`;
    const j = /Batavia-([0-9-]+)/.exec(v.source_url || "");
    return j ? `${label} · jilid ${j[1]}` : label;
  }
  return v.year || "?";
}

function fmt(n) {
  if (!n && n !== 0) return "0";
  if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
  if (n >= 1e3) return (n / 1e3).toFixed(0) + "K";
  return Math.round(n).toLocaleString("nl-NL");
}

/* ─────────────────────────────────────────────────────────────────────────────
   Map SVG icons
   ───────────────────────────────────────────────────────────────────────────── */
function createFortSVG(color, isActive) {
  const glow = isActive ? `filter:drop-shadow(0 0 8px ${color});` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="36" viewBox="0 0 46 56" style="${glow}" aria-hidden="true">
    <path d="M23 54 L10 42 Q2 32 2 18 A18 18 0 1 1 44 18 Q44 32 36 42 Z" fill="white" stroke="${color}" stroke-width="2.5"/>
    <rect x="16" y="12" width="14" height="12" rx="1" fill="${color}"/>
    <path d="M14 24 L32 24 M18 12 L18 10 M28 12 L28 10" stroke="${color}" stroke-width="2" stroke-linecap="round"/>
    <circle cx="23" cy="30" r="3" fill="${color}"/>
  </svg>`;
}

function createAnchorSVG(color, isActive) {
  const glow = isActive ? `filter:drop-shadow(0 0 8px ${color});` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 40 48" style="${glow}" aria-hidden="true">
    <circle cx="20" cy="20" r="18" fill="white" stroke="${color}" stroke-width="2"/>
    <path d="M20 10 L20 32 M13 15 L27 15 M12 28 Q20 38 28 28" fill="none" stroke="${color}" stroke-width="3" stroke-linecap="round"/>
    <circle cx="12" cy="28" r="2" fill="${color}"/>
    <circle cx="28" cy="28" r="2" fill="${color}"/>
  </svg>`;
}

function fortIcon(f, active) {
  const isArrival = f.port_type === "arrival";
  return L.divIcon({
    html: isArrival ? createAnchorSVG(f.color, active) : createFortSVG(f.color, active),
    className: "fort-marker-icon",
    iconSize: isArrival ? [26, 26] : [28, 36],
    iconAnchor: isArrival ? [13, 24] : [14, 34],
  });
}

/* ─────────────────────────────────────────────────────────────────────────────
   Map initialisation
   ───────────────────────────────────────────────────────────────────────────── */
function init() {
  map = L.map("map", { center: [-2.5, 103.0], zoom: 7, zoomControl: true });
  L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
    attribution: "&copy; <a href='https://carto.com/'>CARTO</a> &copy; OpenStreetMap contributors",
    subdomains: "abcd", maxZoom: 19,
  }).addTo(map);
  setTimeout(() => map.invalidateSize(), 100);

  loadGlobalStats();
  loadFortsAndRoutes();
  setupYearFilter();
  setupShipSearch();

  // Close search dropdown on map click
  map.on("click", () => closeSearchDropdown());
}

/* ─────────────────────────────────────────────────────────────────────────────
   Bezier curve helper
   ───────────────────────────────────────────────────────────────────────────── */
function getBezierCurve(start, end, bend) {
  const [lat1, lng1] = start, [lat2, lng2] = end;
  const mlat = (lat1 + lat2) / 2, mlng = (lng1 + lng2) / 2;
  const dlat = lat2 - lat1, dlng = lng2 - lng1;
  const clat = mlat - dlng * bend, clng = mlng + dlat * bend;
  const pts = [];
  for (let t = 0; t <= 1.01; t += 0.05) {
    const u = 1 - t;
    pts.push([u*u*lat1 + 2*u*t*clat + t*t*lat2, u*u*lng1 + 2*u*t*clng + t*t*lng2]);
  }
  return pts;
}

/* ─────────────────────────────────────────────────────────────────────────────
   Catmull-Rom spline -- rute berbasis SEA_WAYPOINTS sebelumnya digambar sbg
   segmen garis LURUS antar titik (kaku, kelihatan patah-patah di tiap waypoint),
   beda dgn rute fallback yg pakai bezier halus. Fungsi ini melewatkan kurva
   mulus MELALUI semua titik asli (bukan bezier yg cuma "ditarik" ke arah titik
   kontrol) -- dipakai baik utk rute pelayaran maupun jalur kekuasaan supaya
   seluruh peta konsisten melengkung, bukan cuma sebagian.
   ───────────────────────────────────────────────────────────────────────────── */
function smoothPath(points, segmentsPerSpan = 12) {
  if (points.length < 3) return points;
  const pts = points;
  const n = pts.length;
  const result = [pts[0]];
  for (let i = 0; i < n - 1; i++) {
    const p0 = pts[i === 0 ? 0 : i - 1];
    const p1 = pts[i];
    const p2 = pts[i + 1];
    const p3 = pts[i + 2 < n ? i + 2 : n - 1];
    for (let t = 1; t <= segmentsPerSpan; t++) {
      const s = t / segmentsPerSpan, s2 = s * s, s3 = s2 * s;
      const lat = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * s
        + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * s2
        + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * s3);
      const lng = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * s
        + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * s2
        + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * s3);
      result.push([lat, lng]);
    }
  }
  return result;
}

/* ─────────────────────────────────────────────────────────────────────────────
   Route drawing (supports year filter via /api/voyages/routes)
   ───────────────────────────────────────────────────────────────────────────── */
async function drawRoutes(yFrom, yTo) {
  routeLines.forEach(l => map.removeLayer(l));
  routeLines = [];

  // Use /api/voyages/routes which supports year filter, direction, and limit
  let url = `${API}/voyages/routes`;
  const params = new URLSearchParams();
  if (yFrom) params.set("year_from", yFrom);
  if (yTo)   params.set("year_to",   yTo);
  if (activeDirection !== "all") params.set("direction", activeDirection);
  if (activeSource !== "all") params.set("source", activeSource);
  params.set("limit", "50");
  const qs = params.toString();
  if (qs) url += "?" + qs;

  let routesData;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("routes fetch failed");
    routesData = await res.json();
  } catch (e) {
    console.warn("drawRoutes error:", e);
    return;
  }

  // Update stats badge with active route count
  const badge = document.getElementById("nav-stats-badge");
  if (badge) {
    const routeCountEl = badge.querySelector("#stats-route-count");
    if (routeCountEl) {
      routeCountEl.textContent = routesData.length;
    } else {
      const div = document.createElement("div");
      div.style.cssText = "font-size:.7rem;opacity:.8;margin-top:2px;";
      div.innerHTML = `<span id="stats-route-count">${routesData.length}</span> rute aktif`;
      badge.appendChild(div);
    }
  }

  routesData.forEach(r => {
    const s = FORT_COORDS[r.origin_name], e = FORT_COORDS[r.destination_name];
    if (!s || !e) return;
    // Color by direction field (US-05) — palet Atlas of Mutual Heritage:
    // navy=outbound, teal=inbound, abu=transit
    const dir = r.direction || "transit";
    const color   = dir === "outbound" ? "#31384C" : dir === "inbound" ? "#027B8C" : "#8B9E97";
    const delay   = dir === "outbound" ? 2800 : dir === "inbound" ? 2200 : 3500;
    const routeKey = `${r.origin_name}→${r.destination_name}`;
    const vias = SEA_WAYPOINTS[routeKey];
    // Rute dengan waypoint jalur laut nyata = presisi (garis penuh).
    // Tanpa waypoint = fallback lengkung → tandai "perkiraan" (dashed, jujur soal presisi).
    const approx = !vias;
    const pts = vias ? smoothPath([s, ...vias, e]) : getBezierCurve(s, e, 0.25);
    const weight = Math.min(1 + (r.count || 1) / 80, 2.5);

    const ant = L.polyline.antPath(pts, {
      delay: delay,
      color: color,
      weight: weight,
      opacity: approx ? 0.38 : 0.55,
      dashArray: approx ? [4, 16] : [10, 20],
      pulseColor: "#FFFFFF",
    }).addTo(map);

    routeLines.push(ant);
  });

  // Layer status kekuasaan pakai L.marker (markerPane) bukan L.circleMarker
  // (overlayPane, sama pane dgn antPath rute) -- markerPane defaultnya SUDAH
  // di atas overlayPane di urutan pane Leaflet, jadi tak perlu bringToFront()
  // manual lagi spt versi circleMarker sebelumnya (L.Marker tak punya method
  // itu, motongnya bakal error).
}

// DOMINION_STATUS_COLORS -- palet dua-sumbu Aceh-tone/VOC-tone/Eropa-lain-tone
// (docs/prd/prd-atlas-power-model.md §7.1), BUKAN 7 warna lepas tak berkaitan.
// Sengaja REUSE token warna existing biar tak nabrak: voc_alliance = SAMA dgn
// .legend-swatch.in (teal, keluarga warna VOC/dagang); internal_conflict =
// SAMA dgn .legend-swatch.transit (abu netral, bukan transisi kekuasaan luar);
// independence = --ocean (CSS token, biru "merdeka" tenang). foreign_orbit
// SENGAJA beda dari POWER_ROUTE_COLOR lama (#6B4C8A) -- status ini bukan
// kelanjutan konsep garis lama yg dihapus, jangan sampai warnanya menyiratkan
// itu masih hal yang sama.
// Palet 2026-07-20 divalidasi lulus skill dataviz (node scripts/validate_palette.js)
// -- palet lama (#A6303B dst, reuse token CSS existing) GAGAL: beberapa warna
// di bawah chroma floor (kebauran, kebaca abu-abu), independence vs voc_alliance
// ΔE cuma 12.3 utk mata normal (di bawah batas keras 15 -- nyaris tak terbedakan
// bahkan tanpa buta warna). Nilai baru dibangun langsung di OKLCH (bukan tebak
// hex) supaya lulus enam cek: lightness band, chroma floor, pemisahan CVD,
// normal-vision floor, kontras. 1 WARN (foreign_orbit<->independence, ΔE 7.4
// protanopia, dlm pita 6-8) sah krn sudah ada label teks di popup/legend
// (secondary encoding), bukan identitas warna semata.
const DOMINION_STATUS_COLORS = {
  aceh_dominion:     "#a02830", // merah-Aceh gelap -- kekuasaan penuh
  relapse_aceh:      "#d26060", // merah-Aceh pudar -- siklus kembali, bukan awal
  voc_alliance:      "#009880",
  independence:      "#1254ac",
  foreign_orbit:     "#ab3782",
  voc_withdrawal:    "#9c640d",
  internal_conflict: "#569859",
};

// Label manusiawi utk tooltip/legend -- JANGAN tampilkan dominion_status
// mentah (snake_case) ke pembaca, itu nama kolom database bukan bahasa peta.
const DOMINION_STATUS_LABELS = {
  aceh_dominion:     "Kekuasaan Aceh",
  relapse_aceh:      "Relaps ke Aceh",
  voc_alliance:      "Aliansi VOC",
  independence:      "Merdeka",
  foreign_orbit:     "Orbit Eropa lain",
  voc_withdrawal:    "VOC mundur",
  internal_conflict: "Konflik internal",
};

// Klaster arketipe (taksonomi CLD, data/export/fort_archetype_clusters.json)
// -- INDEPENDEN dari kanal warna dominion_status di atas, jangan tabrakan.
// Siklus/Stabil ambil dari token app existing (--gold/--ocean di index.html,
// diperdalam dikit spy beda kanal), Sisa reuse --sunset yg sebelumnya tak
// dipakai di peta, Tipis abu netral -- jujur bilang "data <5 event, blm bisa
// dipastikan", bukan warna yg menyaru seolah terklasifikasi.
const CLUSTER_COLORS = {
  Siklus: "#B8901E",
  Stabil: "#2C5364",
  Sisa:   "#D48166",
  Tipis:  "#9AA39E",
};
const CLUSTER_LABELS = {
  Siklus: "Klaster Siklus",
  Stabil: "Klaster Stabil",
  Sisa:   "Klaster Sisa",
  Tipis:  "Data belum cukup",
};

// Ikon bendera-di-tiang -- motif kartografi VOC-era sesungguhnya (menancapkan
// bendera = klaim wilayah), BUKAN circleMarker polos. Selaras dgn createFortSVG/
// createAnchorSVG yg sudah dipakai fort roster (SVG custom, bukan Leaflet
// default), supaya layer ini kelihatan dirancang, bukan ditempel belakangan.
// clusterColor/pSelf OPSIONAL -- fort blm py fort_model_metrics (atau blm
// di-seed_fort_model_metrics.py sama sekali) tetap dapat bendera dominion_status
// polos spt sebelumnya, 2 layer tambahan ini cuma nempel kalau datanya ada.
function createFlagSVG(color, clusterColor, pSelf) {
  const ringRadius = 9;
  const ringCx = 10, ringCy = 41;
  const circumference = 2 * Math.PI * ringRadius;
  const subPennant = clusterColor
    ? `<path d="M22 16 L34 20 L22 24 Z" fill="${clusterColor}" stroke="#FFFFFF" stroke-width="1" stroke-linejoin="round"/>`
    : "";
  // Cincin kestabilan (Model 2 Markov, P(self) status terkini) -- busur
  // penuh = status ini "lengket" (jarang berpindah), busur tipis = fort
  // secara statistik "jatuh tempo" utk berubah. p_self null (fort n<2 event
  // atau status terkini tanpa transisi keluar teramati) -> ring TAK digambar
  // sama sekali, bukan digambar kosong/nol (beda dari "P(self)=0 teramati").
  const dwellRing = (clusterColor && typeof pSelf === "number")
    ? `<circle cx="${ringCx}" cy="${ringCy}" r="${ringRadius}" fill="none" stroke="#E6E2D6" stroke-width="2.4"/>
       <circle cx="${ringCx}" cy="${ringCy}" r="${ringRadius}" fill="none" stroke="${clusterColor}" stroke-width="2.4"
               stroke-linecap="round" stroke-dasharray="${circumference}"
               stroke-dashoffset="${circumference * (1 - pSelf)}"
               transform="rotate(-90 ${ringCx} ${ringCy})"/>`
    : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" width="44" height="50" viewBox="0 0 44 50" aria-hidden="true">
    <line x1="22" y1="41" x2="22" y2="8" stroke="#5C4A32" stroke-width="2" stroke-linecap="round"/>
    <path d="M22 8 L40 13.5 L22 19 Z" fill="${color}" stroke="#FFFFFF" stroke-width="1.2" stroke-linejoin="round"/>
    ${subPennant}
    ${dwellRing}
    <circle cx="22" cy="41" r="2.4" fill="${color}" stroke="#FFFFFF" stroke-width="1"/>
  </svg>`;
}

function dominionFlagIcon(color, clusterColor, pSelf) {
  return L.divIcon({
    html: createFlagSVG(color, clusterColor, pSelf),
    className: "dominion-flag-icon",
    iconSize: [44, 50],
    // Pole base lokal (22,41) digeser -10 di x supaya tetap +10px di kanan
    // titik geografis fort (perilaku sama persis versi lama, cuma kanvas
    // lebih lebar sekarang utk muat pennant klaster + cincin kestabilan).
    iconAnchor: [12, 41],
  });
}

/* ─────────────────────────────────────────────────────────────────────────────
   Layer status kekuasaan (dominion_status) -- GANTI drawPowerRoutes lama.
   Beda dari garis Aceh->fort statis sebelumnya: status baru (voc_withdrawal,
   foreign_orbit, dst) tak selalu melibatkan Aceh sbg "titik asal", jadi
   direpresentasikan sbg lingkaran warna di titik fort itu sendiri, bukan
   garis. Fetch fresh dari /api/forts/power-status tiap dipanggil (pola sama
   drawRoutes, BUKAN fetch-sekali spt loadPoliticalNotes lama) supaya ikut
   berubah tiap slider tahun digeser. Opt-in -- cuma gambar kalau
   powerStatusEnabled true (docs/prd/prd-atlas-power-model.md §7.1: data jauh
   lebih padat drpd sebelumnya, default ON berisiko peta ramai).
   ───────────────────────────────────────────────────────────────────────────── */
// Sparkline simulasi-vs-aktual (Model 5 System Dynamics) di dalam popup --
// dynamics_series: [{year, sim_I, actual_I|null}], actual_I cuma terisi
// PERSIS di titik event asli (lihat seed_fort_model_metrics.py), None di
// titik sim antara -- garis aktual digambar putus-putus dari titik terisi
// ke titik terisi berikutnya, BUKAN interpolasi diam-diam yg menyaru presisi
// yg tak ada.
function buildSparklineSVG(series, currentYear) {
  if (!series || series.length < 2) return "";
  const W = 220, H = 40, PAD = 3;
  const years = series.map(p => p.year);
  const yMin = Math.min(...years), yMax = Math.max(...years);
  const xScale = y => yMin === yMax ? PAD : PAD + ((y - yMin) / (yMax - yMin)) * (W - 2 * PAD);
  // skala I tetap -1..+1 (docs/prd/prd-pemodelan-system-dynamics-game-theory.md §2.2 TARGET),
  // bukan auto-fit ke data -- supaya "seberapa dekat ke +1/-1" tetap bisa dibandingkan antar-fort.
  const yScale = i => H - PAD - ((i + 1) / 2) * (H - 2 * PAD);

  const simPts = series.map(p => `${xScale(p.year).toFixed(1)},${yScale(p.sim_I).toFixed(1)}`).join(" ");
  const actualPts = series.filter(p => p.actual_I !== null && p.actual_I !== undefined);
  const actualPolyline = actualPts.length >= 2
    ? `<polyline points="${actualPts.map(p => `${xScale(p.year).toFixed(1)},${yScale(p.actual_I).toFixed(1)}`).join(" ")}"
                 fill="none" stroke="#009880" stroke-width="1.4" opacity=".55" stroke-dasharray="3,2"/>`
    : "";
  const lastPt = series[series.length - 1];
  // titik "sekarang" (tahun slider aktif) ditebalkan -- bukan cuma titik terakhir data
  const nearestToCurrent = series.reduce((best, p) =>
    Math.abs(p.year - currentYear) < Math.abs(best.year - currentYear) ? p : best, series[0]);

  return `
    <div class="dwell-spark-label">
      <span>Simulasi vs aktual (Model 5)</span><span>${yMin}&ndash;${yMax}</span>
    </div>
    <svg class="dwell-spark" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img"
         aria-label="Kurva simulasi pengaruh VOC dibanding data aktual, ${yMin} sampai ${yMax}">
      ${actualPolyline}
      <polyline points="${simPts}" fill="none" stroke="#B8901E" stroke-width="1.8"/>
      <circle cx="${xScale(nearestToCurrent.year).toFixed(1)}" cy="${yScale(nearestToCurrent.sim_I).toFixed(1)}" r="2.6" fill="#B8901E"/>
    </svg>`;
}

async function drawPowerStatus(year) {
  powerStatusLayers.forEach(l => map.removeLayer(l));
  powerStatusLayers = [];
  if (!powerStatusEnabled) return;

  let data;
  try {
    const res = await fetch(`${API}/forts/power-status?year=${year}`);
    if (!res.ok) throw new Error("power-status fetch failed");
    data = await res.json();
  } catch (e) {
    console.warn("drawPowerStatus error:", e);
    return;
  }

  data.forEach(item => {
    const coords = FORT_COORDS[item.fort_name];
    if (!coords) return;
    const color = DOMINION_STATUS_COLORS[item.dominion_status] || "#999999";
    const label = DOMINION_STATUS_LABELS[item.dominion_status] || item.dominion_status;
    // 3 sinyal Model 2/5/6 -- SEMUA opsional (item.cluster null kalau fort
    // blm py baris fort_model_metrics sama sekali, mis. blm di-seed ulang
    // pasca roster baru). null berarti "belum digambar", bukan "Tipis" --
    // Tipis sendiri adalah nilai cluster yg VALID (data <5 event, taksonomi
    // CLD), beda dari null (tak ada baris metrik sama sekali).
    const clusterColor = item.cluster ? (CLUSTER_COLORS[item.cluster] || null) : null;
    const clusterLabel = item.cluster ? (CLUSTER_LABELS[item.cluster] || item.cluster) : null;

    const marker = L.marker(coords, {
      icon: dominionFlagIcon(color, clusterColor, item.p_self_current_status),
      zIndexOffset: 500,
    }).addTo(map);

    const clusterChip = clusterColor
      ? `<div class="cluster-chip" style="--cluster-color:${clusterColor}">
           <span class="cluster-chip-dot"></span>${esc(clusterLabel)}
         </div>`
      : "";
    const sparkline = clusterColor ? buildSparklineSVG(item.dynamics_series, year) : "";

    // bindPopup (klik), BUKAN bindTooltip (hover) -- proyek ini sengaja hapus
    // semua tooltip hover di layer peta (test_no_hover_tooltips_on_map_layers,
    // keputusan user 2026-07-13). Popup klik konsisten dgn cara marker fort
    // lain sudah bekerja (klik -> panel), bukan pola baru.
    marker.bindPopup(
      `<div class="dominion-popup-card" style="--dominion-color:${color}">
         <div class="dominion-popup-fort">${esc(item.fort_name)}</div>
         <div class="dominion-popup-status">${esc(label)}</div>
         ${clusterChip}
         <div class="dominion-popup-event">${esc(item.as_of_event.title)}</div>
         <div class="dominion-popup-meta">${item.as_of_event.year ?? "?"} &middot; ${esc(item.as_of_event.source_document)}</div>
         ${sparkline ? `<div class="dwell-spark-wrap">${sparkline}</div>` : ""}
       </div>`,
      { className: "dominion-popup", closeButton: true, minWidth: 200, maxWidth: 280 }
    );

    powerStatusLayers.push(marker);
  });
}

function togglePowerStatus() {
  powerStatusEnabled = !powerStatusEnabled;
  const btn = document.getElementById("btn-power-status");
  if (btn) {
    btn.classList.toggle("active", powerStatusEnabled);
    btn.setAttribute("aria-pressed", powerStatusEnabled ? "true" : "false");
  }
  const legend = document.getElementById("dominion-legend-group");
  if (legend) legend.style.display = powerStatusEnabled ? "block" : "none";
  drawPowerStatus(yearTo);
}

/* ─────────────────────────────────────────────────────────────────────────────
   Direction toggle (US-05)
   ───────────────────────────────────────────────────────────────────────────── */
function setDirection(dir) {
  activeDirection = dir;

  // Update button active state
  const btnMap = { all: "dir-all", outbound: "dir-out", inbound: "dir-in" };
  Object.entries(btnMap).forEach(([key, id]) => {
    const btn = document.getElementById(id);
    if (!btn) return;
    const isActive = key === dir;
    btn.classList.toggle("active", isActive);
    btn.setAttribute("aria-pressed", isActive ? "true" : "false");
  });

  drawRoutes(yearFrom, yearTo);
}

/* ─────────────────────────────────────────────────────────────────────────────
   Source/provenance toggle (P0.3b)
   ───────────────────────────────────────────────────────────────────────────── */
function setSource(src) {
  activeSource = src;

  const select = document.getElementById("source-select");
  if (select && select.value !== src) select.value = src;

  drawRoutes(yearFrom, yearTo);
}

/* ─────────────────────────────────────────────────────────────────────────────
   Fakta politik/administratif Atjeh (atjeh_trade_records, direction=politik --
   kategori terpisah dari in_atjeh sejak 2026-07-13, lihat feedback_sisir_semua_
   titik_pemakaian) -- kini digantikan layer status kekuasaan (drawPowerStatus,
   dominion_status per fort/tahun) yg jauh lebih presisi, lihat PRD terkait.
   ───────────────────────────────────────────────────────────────────────────── */

/* ─────────────────────────────────────────────────────────────────────────────
   Load forts + routes, populate welcome grid
   ───────────────────────────────────────────────────────────────────────────── */
async function loadFortsAndRoutes() {
  let forts;
  try {
    forts = await fetch(`${API}/forts/`).then(r => r.json());
  } catch (e) {
    console.warn("loadForts error:", e);
    return;
  }

  allFortsData = forts;

  // FORT_COORDS hardcode hanya mencakup 9 pelabuhan awal — fort yg ditambah belakangan
  // (Tiku, Pariaman, Salido, Bayang, Painan, node regional Pantai Barat Sumatra) diisi
  // dinamis dari API di sini, kalau tidak marker & garis rutenya diam-diam tidak tergambar.
  forts.forEach(f => {
    if (!FORT_COORDS[f.name] && f.latitude != null && f.longitude != null) {
      FORT_COORDS[f.name] = [f.latitude, f.longitude];
    }
  });

  // Sesuaikan viewport ke SEMUA pelabuhan yg ada data-nya -- jangan hardcode
  // center/zoom, krn itu bikin pelabuhan yg lokasinya jauh dari cluster utama
  // (mis. Aceh, jauh di utara) permanen di luar layar meski markernya SUDAH
  // digambar dgn benar. Regresi 2026-07-13: user berulang kali lapor "rute Aceh
  // tak ada" padahal datanya benar -- ternyata cuma di luar viewport default.
  //
  // Batavia (Jawa, -6.1/106.8) DIKECUALIKAN dari perhitungan bounds ini --
  // itu cuma hub administratif VOC yg jauh di luar "Pesisir Barat Sumatera"
  // (subjek atlas ini), bukan pelabuhan westkust. Ikut dihitung bikin default
  // view zoom keluar sampai mencakup seluruh Selat Malaka+daratan Asia
  // Tenggara (Thailand/Kamboja/Vietnam ikut kelihatan) -- regresi ditemukan
  // 2026-07-17 lewat audit mobile. Marker/rute Batavia TETAP digambar &
  // klik-able, cuma tak ikut menentukan default zoom.
  const fortLatLngs = forts
    .filter(f => f.name !== "Batavia")
    .map(f => FORT_COORDS[f.name]).filter(Boolean);
  if (fortLatLngs.length) {
    map.fitBounds(fortLatLngs, { padding: [40, 40] });
  }

  // Welcome port grid
  const grid = document.getElementById("port-grid");
  if (forts.length === 0) {
    grid.innerHTML = `<div class="port-card" style="grid-column:span 3; color:var(--text-muted); font-size:.75rem;">Tidak ada data port.</div>`;
  } else {
    grid.innerHTML = forts.map(f => {
      const icon = PORT_ICONS[f.name] || "ti-anchor";
      return `<div class="port-card" role="listitem" tabindex="0"
               aria-label="Pelabuhan ${esc(f.name)}, ${f.outbound_count} keluar, ${f.inbound_count} masuk"
               onclick="openFortById(${f.id})"
               onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();openFortById(${f.id})}">
        <i class="ti ${esc(icon)} port-card-icon" aria-hidden="true"></i>
        <div class="port-card-name">${esc(f.name)}</div>
        <div class="port-card-counts">
          <span class="port-count-tag port-count-out" title="Keluar">${f.outbound_count}</span>
          <span class="port-count-tag port-count-in"  title="Masuk">${f.inbound_count}</span>
        </div>
      </div>`;
    }).join("");
  }

  // Place markers on map
  forts.forEach(f => {
    const coords = FORT_COORDS[f.name];
    if (!coords) return;
    const marker = L.marker(coords, { icon: fortIcon(f, false) }).addTo(map);
    marker.on("click", () => openFort(f, marker));
    marker._fortData = f;
    f._marker = marker;
  });

  // Draw routes for default year range
  await drawRoutes(yearFrom, yearTo);

  // Layer status kekuasaan -- digambar SETELAH drawRoutes supaya selalu di
  // ATAS garis pelayaran (Leaflet: layer belakangan render di atas). Opt-in
  // (powerStatusEnabled default false), jadi no-op di load awal kecuali user
  // sudah aktifkan toggle sebelumnya di sesi ini.
  await drawPowerStatus(yearTo);
}

/* ─────────────────────────────────────────────────────────────────────────────
   Open fort by ID (called from welcome grid)
   ───────────────────────────────────────────────────────────────────────────── */
function openFortById(id) {
  const f = allFortsData.find(x => x.id === id);
  if (!f || !f._marker) return;
  openFort(f, f._marker);
}

/* ─────────────────────────────────────────────────────────────────────────────
   Open fort panel
   ───────────────────────────────────────────────────────────────────────────── */
async function openFort(f, marker) {
  // Swap marker icon
  if (activeMarker && activeMarker !== marker) {
    activeMarker.setIcon(fortIcon(activeMarker._fortData, false));
  }
  activeMarker = marker;
  marker.setIcon(fortIcon(f, true));

  // Hide welcome, show fort panel
  document.getElementById("welcome-panel").classList.add("hidden");
  const panel = document.getElementById("fort-panel");
  const backdrop = document.getElementById("fort-backdrop");
  panel.classList.add("open");
  panel.setAttribute("aria-hidden", "false");
  backdrop.classList.add("open");

  // Set heading
  document.getElementById("ft-name").textContent = f.name;
  document.getElementById("ft-years").textContent = "—";

  // Reset stats
  ["st-out-count","st-in-count","st-out-val","st-in-val"].forEach(id =>
    document.getElementById(id).textContent = "—");

  toggleLoader(true);

  let d;
  try {
    const res = await fetch(`${API}/forts/${f.id}`);
    if (!res.ok) throw new Error("fort fetch failed");
    d = await res.json();
  } catch (e) {
    console.warn("openFort error:", e);
    toggleLoader(false);
    return;
  }

  currentData.outbound = d.outbound_voyages || [];
  currentData.inbound  = d.inbound_voyages  || [];
  currentData.info     = d.description || "";

  document.getElementById("st-out-count").textContent = d.outbound_count || 0;
  document.getElementById("st-in-count").textContent  = d.inbound_count  || 0;
  document.getElementById("st-out-val").textContent   = "ƒ " + fmt(d.total_value_out);
  document.getElementById("st-in-val").textContent    = "ƒ " + fmt(d.total_value_in);

  if (d.year_min && d.year_max) {
    document.getElementById("ft-years").textContent = `${d.year_min} – ${d.year_max}`;
  }

  toggleLoader(false);
  setTab("outbound");

  if (FORT_COORDS[f.name]) map.flyTo(FORT_COORDS[f.name], 9);
}

/* ─────────────────────────────────────────────────────────────────────────────
   Close fort panel
   ───────────────────────────────────────────────────────────────────────────── */
function closeFortPanel() {
  const panel = document.getElementById("fort-panel");
  const backdrop = document.getElementById("fort-backdrop");
  panel.classList.remove("open");
  panel.setAttribute("aria-hidden", "true");
  backdrop.classList.remove("open");
  document.getElementById("welcome-panel").classList.remove("hidden");

  if (activeMarker) {
    activeMarker.setIcon(fortIcon(activeMarker._fortData, false));
    activeMarker = null;
  }
}

/* ─────────────────────────────────────────────────────────────────────────────
   Tabs
   ───────────────────────────────────────────────────────────────────────────── */
function setTab(t) {
  activeTab = t;
  pageIndex = 0;

  document.querySelectorAll(".panel-tab").forEach(el => {
    el.classList.remove("active");
    el.setAttribute("aria-selected", "false");
  });

  const tabMap = { outbound: "tab-out", inbound: "tab-in", info: "tab-inf" };
  const activeEl = document.getElementById(tabMap[t]);
  if (activeEl) {
    activeEl.classList.add("active");
    activeEl.setAttribute("aria-selected", "true");
  }

  const vCont = document.getElementById("list-voyages");
  const iCont = document.getElementById("fort-info");
  const lmBtn = document.getElementById("load-more-btn");

  if (t === "info") {
    vCont.style.display = "none";
    iCont.style.display = "block";
    lmBtn.style.display = "none";
    iCont.textContent = currentData.info || "Informasi sejarah belum tersedia untuk pelabuhan ini.";
  } else {
    vCont.style.display = "block";
    iCont.style.display = "none";
    renderPage(currentData[t], 0);
  }
}

/* ─────────────────────────────────────────────────────────────────────────────
   Voyage list rendering with pagination
   ───────────────────────────────────────────────────────────────────────────── */
function renderPage(data, startIndex) {
  const el = document.getElementById("list-voyages");
  const lmBtn = document.getElementById("load-more-btn");
  const countEl = document.getElementById("load-more-count");

  if (!data || data.length === 0) {
    el.innerHTML = `<div class="empty-state">
      <i class="ti ti-ship" aria-hidden="true"></i>
      Tidak ada catatan pelayaran.
    </div>`;
    lmBtn.style.display = "none";
    return;
  }

  const slice = data.slice(startIndex, startIndex + PAGE_SIZE);

  if (startIndex === 0) {
    el.innerHTML = "";
  }

  const frag = document.createDocumentFragment();
  slice.forEach(v => {
    const item = document.createElement("div");
    item.className = "voyage-item";
    item.setAttribute("tabindex", "0");
    item.setAttribute("role", "button");
    item.setAttribute("aria-label", `Kapal ${esc(v.ship_name)}, ${voyageDateText(v, true)}`);
    item.dataset.voyageId = v.id;

    const yearTag = `<span class="tag tag-year"><i class="ti ti-calendar-event" aria-hidden="true"></i> ${esc(voyageDateText(v, true))}</span>`;
    const valTag  = v.total_gulden ? `<span class="tag tag-val"><i class="ti ti-coin" aria-hidden="true"></i> ƒ ${fmt(v.total_gulden)}</span>` : "";

    item.innerHTML = `
      <div class="voyage-ship">${esc(v.ship_name)}</div>
      <div class="voyage-route-line">
        <i class="ti ti-route-2" aria-hidden="true"></i>
        ${esc(v.origin_name_raw || "")} &rarr; ${esc(v.destination_name_raw || "")}
      </div>
      <div class="voyage-meta">${yearTag}${valTag}</div>`;

    item.onclick = () => openVoyageModal(v.id);
    item.onkeydown = (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openVoyageModal(v.id); }
    };
    frag.appendChild(item);
  });

  el.appendChild(frag);
  pageIndex = startIndex + slice.length;

  const remaining = data.length - pageIndex;
  if (remaining > 0) {
    lmBtn.style.display = "block";
    countEl.textContent = remaining;
  } else {
    lmBtn.style.display = "none";
  }
}

function loadMore() {
  renderPage(currentData[activeTab], pageIndex);
}

/* ─────────────────────────────────────────────────────────────────────────────
   Voyage modal — fetches data on demand (security: no inline JSON)
   ───────────────────────────────────────────────────────────────────────────── */
async function openVoyageModal(voyageId) {
  const modal = document.getElementById("voyage-modal");
  const body = document.getElementById("modal-body-content");

  // Reset header and BGB link
  document.getElementById("modal-ship-name").textContent = "Memuat...";
  document.getElementById("modal-ship-meta").textContent = "";
  body.innerHTML = `<div class="modal-loading"><i class="ti ti-loader-2"></i><span>Memuat detail pelayaran...</span></div>`;
  document.getElementById("modal-bgb-link").style.display = "none";
  modal.classList.add("active");

  let voyage, cargo;
  try {
    const [vRes, cRes] = await Promise.all([
      fetch(`${API}/voyages/${voyageId}`),
      fetch(`${API}/voyages/${voyageId}/cargo`),
    ]);
    if (!vRes.ok) throw new Error("voyage not found");
    voyage = await vRes.json();
    cargo  = cRes.ok ? await cRes.json() : [];
  } catch (e) {
    console.warn("openVoyageModal error:", e);
    body.innerHTML = `<div class="empty-state"><i class="ti ti-alert-circle"></i>Gagal memuat data pelayaran.</div>`;
    return;
  }

  // Header
  document.getElementById("modal-ship-name").textContent = voyage.ship_name || "Unknown Ship";
  const capt = voyage.captain ? ` &bull; Capt. ${esc(voyage.captain)}` : "";
  // Tanggal penuh (penanggalan kargo ikut voyage): tampilkan berangkat/tiba bila ada, fallback tahun
  const dateText = voyageDateText(voyage, false);
  document.getElementById("modal-ship-meta").innerHTML = `${esc(dateText)}${capt}`;

  // Build body HTML
  const durText  = voyage.duration_days ? `${voyage.duration_days} hari` : "—";
  const valText  = voyage.total_gulden  ? `ƒ ${fmt(voyage.total_gulden)}`  : "—";
  const destText = esc(voyage.destination || voyage.destination_name_raw || "Batavia");
  const prodText = voyage.main_product
    ? `<span class="cargo-name" data-term="${esc((voyage.main_product).trim().toLowerCase())}">${esc(voyage.main_product)}</span>`
    : "—";

  // Kumpulkan semua terms untuk glossary lookup
  const allTerms = [];
  let cargoHtml = "";
  if (cargo && cargo.length > 0) {
    cargoHtml = cargo.map(c => {
      const val = c.gulden_india ? `ƒ ${fmt(c.gulden_india)}` : (c.gulden_nl ? `ƒ ${fmt(c.gulden_nl)}` : "");
      const termKey = (c.produk || "").trim().toLowerCase();
      if (termKey) allTerms.push(termKey);
      return `<div class="cargo-item">
        <span class="cargo-name" data-term="${esc(termKey)}">${esc(c.produk)}</span>
        ${val ? `<span class="cargo-val">${val}</span>` : ""}
      </div>`;
    }).join("");
  } else if (voyage.all_products) {
    cargoHtml = voyage.all_products.split("|").map(p => {
      const clean = p.trim();
      const termKey = clean.toLowerCase();
      if (termKey) allTerms.push(termKey);
      return `<div class="cargo-item"><span class="cargo-name" data-term="${esc(termKey)}">${esc(clean)}</span></div>`;
    }).join("");
  } else {
    cargoHtml = `<div class="empty-state" style="padding:1rem 0;"><i class="ti ti-package"></i>Data kargo detail tidak tersedia.</div>`;
  }

  // Main product juga perlu tooltip
  const mainTermKey = (voyage.main_product || "").trim().toLowerCase();
  if (mainTermKey) allTerms.push(mainTermKey);

  body.innerHTML = `
    <div class="modal-data-grid">
      <div class="modal-data-item">
        <div class="lbl"><i class="ti ti-map-pin" aria-hidden="true"></i> Tujuan</div>
        <div class="val">${destText}</div>
      </div>
      <div class="modal-data-item">
        <div class="lbl"><i class="ti ti-calendar-event" aria-hidden="true"></i> Durasi</div>
        <div class="val">${durText}</div>
      </div>
      <div class="modal-data-item">
        <div class="lbl"><i class="ti ti-coin" aria-hidden="true"></i> Total Nilai Kargo</div>
        <div class="val" style="color:var(--accent);font-weight:700;">${valText}</div>
      </div>
      <div class="modal-data-item">
        <div class="lbl"><i class="ti ti-package" aria-hidden="true"></i> Komoditi Utama</div>
        <div class="val">${prodText}</div>
      </div>
      <div class="modal-data-item">
        <div class="lbl"><i class="ti ti-database" aria-hidden="true"></i> Sumber Data</div>
        <div class="val">${esc(MODAL_SOURCE_LABELS[voyage.source] || MODAL_SOURCE_LABELS.bgb_huygens)}</div>
      </div>
    </div>
    <div class="cargo-list">
      <div class="cargo-list-label"><i class="ti ti-package" aria-hidden="true"></i> Detail Kargo</div>
      ${cargoHtml}
    </div>`;

  // BGB source link — show only when source_url is present
  const bgbLink = document.getElementById("modal-bgb-link");
  if (voyage.source_url) {
    bgbLink.href = voyage.source_url;
    bgbLink.style.display = "";
  } else {
    bgbLink.style.display = "none";
  }

  // Glossary tooltips — fetch definisi dan terapkan ke elemen [data-term]
  if (allTerms.length) {
    fetchGlossaryForTerms(allTerms).then(() => applyGlossaryTooltips(body));
  }
}

function closeModal() {
  document.getElementById("voyage-modal").classList.remove("active");
}

/* ─────────────────────────────────────────────────────────────────────────────
   Global stats badge
   ───────────────────────────────────────────────────────────────────────────── */
async function loadGlobalStats() {
  try {
    const res = await fetch(`${API}/voyages/stats`);
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById("stats-total").textContent =
      (data.total_voyages || 0).toLocaleString("nl-NL");
  } catch (e) {
    console.warn("stats error:", e);
  }
}

/* ─────────────────────────────────────────────────────────────────────────────
   Year range filter with debounce
   ───────────────────────────────────────────────────────────────────────────── */
function downloadCSV() {
    const params = new URLSearchParams();
    params.set("year_from", yearFrom);
    params.set("year_to",   yearTo);
    if (activeDirection && activeDirection !== "all") {
        params.set("direction", activeDirection);
    }
    const url = `${API}/voyages/export?${params.toString()}`;
    const a = document.createElement("a");
    a.href = url;
    a.download = "voyages_westkust.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function setupYearFilter() {
  const fromEl    = document.getElementById("year-from");
  const toEl      = document.getElementById("year-to");
  const fromDisp  = document.getElementById("year-from-display");
  const toDisp    = document.getElementById("year-to-display");

  function updateDisplays() {
    if (fromDisp) fromDisp.textContent = fromEl.value;
    if (toDisp)   toDisp.textContent   = toEl.value;
  }

  function onYearChange() {
    updateDisplays();
    clearTimeout(yearDebounce);
    yearDebounce = setTimeout(async () => {
      const yf = parseInt(fromEl.value, 10) || 1620;
      const yt = parseInt(toEl.value, 10)   || 1790;
      if (yf > yt) return;
      yearFrom = yf;
      yearTo   = yt;
      await drawRoutes(yearFrom, yearTo);
      await drawPowerStatus(yearTo);
      loadGrafikData();
    }, 500);
  }

  fromEl.addEventListener("input", onYearChange);
  toEl.addEventListener("input", onYearChange);
  updateDisplays();
}

/* ─────────────────────────────────────────────────────────────────────────────
   Ship search with debounce
   ───────────────────────────────────────────────────────────────────────────── */
function setupShipSearch() {
  const input = document.getElementById("ship-search");
  const dropdown = document.getElementById("search-dropdown");

  input.addEventListener("input", () => {
    clearTimeout(searchDebounce);
    const q = input.value.trim();
    if (q.length < 2) {
      closeSearchDropdown();
      return;
    }
    searchDebounce = setTimeout(() => fetchShipSearch(q), 350);
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeSearchDropdown(); input.value = ""; }
  });

  document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      closeSearchDropdown();
    }
  });
}

async function fetchShipSearch(q) {
  const dropdown = document.getElementById("search-dropdown");
  const input = document.getElementById("ship-search");

  try {
    const res = await fetch(`${API}/voyages/?search=${encodeURIComponent(q)}&limit=20`);
    if (!res.ok) throw new Error("search failed");
    const voyages = await res.json();

    if (voyages.length === 0) {
      dropdown.innerHTML = `<div class="search-result-item" style="color:var(--text-muted);cursor:default;">Tidak ada hasil untuk "${esc(q)}"</div>`;
    } else {
      dropdown.innerHTML = voyages.map(v =>
        `<div class="search-result-item" role="option" tabindex="0"
              aria-label="Kapal ${esc(v.ship_name)}"
              onclick="openVoyageModal(${v.id})"
              onkeydown="if(event.key==='Enter'){openVoyageModal(${v.id})}">
           <div class="search-result-ship">${esc(v.ship_name)}</div>
           <div class="search-result-meta">
             ${esc(voyageDateText(v, true))} &bull; ${esc(v.origin_name_raw || "")} &rarr; ${esc(v.destination_name_raw || "")}
           </div>
         </div>`
      ).join("");
    }

    dropdown.classList.add("open");
    input.setAttribute("aria-expanded", "true");
  } catch (e) {
    console.warn("ship search error:", e);
  }
}

function closeSearchDropdown() {
  const dropdown = document.getElementById("search-dropdown");
  const input = document.getElementById("ship-search");
  dropdown.classList.remove("open");
  dropdown.innerHTML = "";
  input.setAttribute("aria-expanded", "false");
}

/* ─────────────────────────────────────────────────────────────────────────────
   Loader toggle
   ───────────────────────────────────────────────────────────────────────────── */
function toggleLoader(show) {
  document.getElementById("loader").classList.toggle("active", show);
}

/* ─────────────────────────────────────────────────────────────────────────────
   Welcome panel ciutkan/buka -- diminta krn di mobile panel menutupi peta;
   dgn ini pengguna bisa ciutkan jadi cuma header (lihat #welcome-panel.collapsed
   di CSS) tanpa kehilangan akses ke peta di baliknya.
   ───────────────────────────────────────────────────────────────────────────── */
function toggleWelcomePanel() {
  const panel = document.getElementById("welcome-panel");
  const btn = document.getElementById("welcome-toggle");
  const collapsed = panel.classList.toggle("collapsed");
  btn.setAttribute("aria-expanded", String(!collapsed));
  btn.setAttribute("aria-label", collapsed ? "Buka panel" : "Ciutkan panel");
}

/* ─────────────────────────────────────────────────────────────────────────────
   Reset view
   ───────────────────────────────────────────────────────────────────────────── */
function resetView() {
  map.flyTo([-2.5, 103.0], 7);
  closeFortPanel();
  closeSearchDropdown();
}

/* ─────────────────────────────────────────────────────────────────────────────
   Keyboard accessibility — Escape closes panels/modal
   ───────────────────────────────────────────────────────────────────────────── */
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const modal = document.getElementById("voyage-modal");
    if (modal.classList.contains("active")) { closeModal(); return; }
    const panel = document.getElementById("fort-panel");
    if (panel.classList.contains("open")) { closeFortPanel(); return; }
  }
});

/* ─────────────────────────────────────────────────────────────────────────────
   Grafik / Analytics Panel
   ───────────────────────────────────────────────────────────────────────────── */
let grafikOpen = false;
let chartProducts = null, chartPorts = null;

function toggleGrafikPanel() {
  grafikOpen = !grafikOpen;
  const panel = document.getElementById("grafik-panel");
  const btn   = document.getElementById("btn-grafik");
  panel.classList.toggle("open", grafikOpen);
  panel.setAttribute("aria-hidden", String(!grafikOpen));
  btn.setAttribute("aria-expanded", String(grafikOpen));
  btn.classList.toggle("active", grafikOpen);
  if (grafikOpen) loadGrafikData();
}

async function loadGrafikData() {
  try {
    const res = await fetch(`${API}/voyages/stats?year_from=${yearFrom}&year_to=${yearTo}`);
    if (!res.ok) return;
    const d = await res.json();

    document.getElementById("gk-total").textContent  = (d.total_voyages || 0).toLocaleString("nl-NL");
    document.getElementById("gk-value").textContent  = "ƒ" + fmt(d.total_cargo_value || 0);
    document.getElementById("gk-out").textContent    = (d.outbound_count || 0).toLocaleString("nl-NL");
    document.getElementById("gk-in").textContent     = (d.inbound_count || 0).toLocaleString("nl-NL");

    const CHART_FONT = "'IBM Plex Sans', sans-serif";
    const GRID_COLOR = "rgba(26,36,33,0.07)";
    const sharedScales = {
      x: { beginAtZero: true, grid: { color: GRID_COLOR },
           ticks: { font: { family: CHART_FONT, size: 11 }, color: "#5C6A66" } },
      y: { grid: { display: false },
           ticks: { font: { family: CHART_FONT, size: 11 }, color: "#1A2421" } }
    };

    // Chart 1 — Top Products (horizontal bar)
    const prods = (d.top_products || []).slice(0, 8);
    if (chartProducts) chartProducts.destroy();
    chartProducts = new Chart(document.getElementById("chart-products"), {
      type: "bar",
      data: {
        labels: prods.map(p => esc(p.name || "—")),
        datasets: [{ data: prods.map(p => p.count),
          backgroundColor: "#D8B13Bcc", borderRadius: 4, borderSkipped: false }]
      },
      options: {
        indexAxis: "y", responsive: true,
        plugins: { legend: { display: false },
          tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.x} voyage` } } },
        scales: sharedScales
      }
    });

    // Chart 2 — Port Value (horizontal bar)
    const ports = (d.ports || []).filter(p => (p.value || 0) > 0).slice(0, 8);
    if (chartPorts) chartPorts.destroy();
    chartPorts = new Chart(document.getElementById("chart-ports"), {
      type: "bar",
      data: {
        labels: ports.map(p => esc(p.name)),
        datasets: [{ data: ports.map(p => Math.round(p.value)),
          backgroundColor: "#31384Cbb", borderRadius: 4, borderSkipped: false }]
      },
      options: {
        indexAxis: "y", responsive: true,
        plugins: { legend: { display: false },
          tooltip: { callbacks: { label: ctx => ` ƒ${ctx.parsed.x.toLocaleString("nl-NL")}` } } },
        scales: sharedScales
      }
    });

  } catch (e) {
    console.error("Grafik data error:", e);
  }
}

/* ─────────────────────────────────────────────────────────────────────────────
   Boot
   ───────────────────────────────────────────────────────────────────────────── */
init();
