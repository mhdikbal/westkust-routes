"""
Frontend View Tests — Layout B
Sprint 1 — Uji Kelayakan | Tim Jangkar QA

Django TestCase tests for the map_app frontend.
The index view reads the compiled HTML (React build or Leaflet template)
directly via HttpResponse — not through Django's template engine — so
assertTemplateUsed cannot be used here.

Covers:
  - Index view returns HTTP 200
  - Required HTML elements for Layout B are present in the rendered page
  - Security: CSP meta tag, no sensitive data in page source
  - Accessibility markup (aria-* attributes, keyboard handler hooks)

All test classes use SimpleTestCase — no database required since views fetch
from FastAPI backend via httpx (mocked in tests that hit view logic).
"""
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase, Client
from django.urls import reverse

# atlas.js content — read once for tests that verify JS logic extracted from index.html (US-11)
_ATLAS_JS_PATH = Path(__file__).parent / "static" / "map_app" / "js" / "atlas.js"
ATLAS_JS = _ATLAS_JS_PATH.read_text(encoding="utf-8") if _ATLAS_JS_PATH.exists() else ""


class IndexViewStatusTest(SimpleTestCase):
    """Basic smoke tests — the page must load without error."""

    def setUp(self):
        self.client = Client()

    def test_index_returns_200(self):
        """GET / must return HTTP 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_content_type_is_html(self):
        """Response Content-Type should be text/html."""
        response = self.client.get("/")
        self.assertIn("text/html", response["Content-Type"])

    def test_index_not_404(self):
        """GET / must not return 404."""
        response = self.client.get("/")
        self.assertNotEqual(response.status_code, 404)

    def test_index_not_500(self):
        """GET / must not return 500."""
        response = self.client.get("/")
        self.assertNotEqual(response.status_code, 500)


class LayoutBNavbarTest(SimpleTestCase):
    """Verify navbar elements introduced in Layout B are present in the HTML."""

    def setUp(self):
        self.client = Client()
        response = self.client.get("/")
        self.content = response.content.decode("utf-8")

    def test_navbar_element_present(self):
        """#navbar element must be in the page for the 3-column navbar."""
        self.assertIn('id="navbar"', self.content)

    def test_year_from_input_present(self):
        """Year-from input (#year-from) must be present for the navbar year filter."""
        self.assertIn('id="year-from"', self.content)

    def test_year_to_input_present(self):
        """Year-to input (#year-to) must be present for the navbar year filter."""
        self.assertIn('id="year-to"', self.content)

    def test_ship_search_input_present(self):
        """Ship search input (#ship-search) must be present for the navbar search."""
        self.assertIn('id="ship-search"', self.content)

    def test_search_dropdown_present(self):
        """Search results dropdown (#search-dropdown) must exist in DOM."""
        self.assertIn('id="search-dropdown"', self.content)

    def test_stats_badge_present(self):
        """Stats badge (#nav-stats-badge) must be present for voyage count display."""
        self.assertIn('id="nav-stats-badge"', self.content)

    def test_year_defaults_are_1620_and_1790(self):
        """Default year range: 1620 (diperlebar lagi 2026-07-13 utk voyage Wapen van
        Hoorn 1624, volume Dagh-register 1624-1629 -- sebelumnya 1630 via 1660) sampai
        1790 (batas dekade terakhir, step=10)."""
        self.assertIn('value="1620"', self.content)
        self.assertIn('value="1790"', self.content)


class LayoutBWelcomePanelTest(SimpleTestCase):
    """Verify the floating welcome panel with port grid is rendered."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_welcome_panel_present(self):
        """#welcome-panel must exist in the page for the port grid overlay."""
        self.assertIn('id="welcome-panel"', self.content)

    def test_port_grid_present(self):
        """#port-grid must exist — JS will populate it with port cards from /api/forts/."""
        self.assertIn('id="port-grid"', self.content)

    def test_welcome_panel_has_anchor_icon(self):
        """Welcome panel must contain anchor icon (Tabler ti-anchor) per design spec."""
        self.assertIn("ti-anchor", self.content)

    def test_welcome_panel_has_atlas_title(self):
        """Welcome panel must contain the atlas title text."""
        self.assertIn("Atlas Maritim", self.content)


class LayoutBFortPanelTest(SimpleTestCase):
    """Verify the slide-over fort panel structure is in the DOM."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_fort_panel_present(self):
        """#fort-panel must exist — it slides in from the right when a port is selected."""
        self.assertIn('id="fort-panel"', self.content)

    def test_fort_panel_has_dialog_role(self):
        """Fort panel must have role=dialog for accessibility."""
        self.assertIn('role="dialog"', self.content)

    def test_fort_panel_has_aria_modal(self):
        """Fort panel must have aria-modal=true."""
        self.assertIn('aria-modal="true"', self.content)

    def test_fort_backdrop_present(self):
        """#fort-backdrop must exist to close the panel when clicked."""
        self.assertIn('id="fort-backdrop"', self.content)

    def test_close_button_has_accessible_label(self):
        """Close button must have aria-label for keyboard users."""
        self.assertIn("Tutup panel benteng", self.content)

    def test_fort_panel_tabs_present(self):
        """Panel tabs (Keluar / Masuk / Info) must be present."""
        self.assertIn('id="tab-out"', self.content)
        self.assertIn('id="tab-in"', self.content)
        self.assertIn('id="tab-inf"', self.content)

    def test_stats_grid_elements_present(self):
        """Stats grid elements (outbound/inbound counts and values) must be in DOM."""
        self.assertIn('id="st-out-count"', self.content)
        self.assertIn('id="st-in-count"', self.content)
        self.assertIn('id="st-out-val"', self.content)
        self.assertIn('id="st-in-val"', self.content)

    def test_load_more_button_present(self):
        """Load-more button must exist for paginated voyage list."""
        self.assertIn('id="load-more-btn"', self.content)


class LayoutBVoyageModalTest(SimpleTestCase):
    """Verify the voyage detail modal is present in the DOM."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_voyage_modal_present(self):
        """#voyage-modal must exist for voyage detail display."""
        self.assertIn('id="voyage-modal"', self.content)

    def test_voyage_modal_has_aria_modal(self):
        """Voyage modal must have aria-modal=true."""
        self.assertIn('aria-modal="true"', self.content)

    def test_modal_close_button_accessible(self):
        """Modal close button must have aria-label."""
        self.assertIn("Tutup detail pelayaran", self.content)

    def test_modal_ship_name_placeholder_present(self):
        """Modal heading #modal-ship-name must be in DOM."""
        self.assertIn('id="modal-ship-name"', self.content)


class LayoutBMapTest(SimpleTestCase):
    """Verify the full-screen map container is rendered."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_map_container_present(self):
        """#map div must exist — Leaflet initialises to this element."""
        self.assertIn('id="map"', self.content)

    def test_leaflet_js_loaded(self):
        """Leaflet JS CDN script must be referenced."""
        self.assertIn("leaflet", self.content.lower())

    def test_ant_path_js_loaded(self):
        """leaflet-ant-path must be loaded for animated route lines."""
        self.assertIn("ant-path", self.content.lower())

    def test_map_legend_present(self):
        """User 2026-07-13: setelah semua tooltip hover dihapus, tak ada cara lagi
        utk tahu arti warna garis (keluar/masuk/transit/jalur kekuasaan) tanpa
        hover -- legenda statis di peta wajib ada sbg gantinya. Termasuk entri
        jalur kekuasaan Atjeh yg sempat tak masuk legenda lama (yg sebenarnya
        belum pernah dibuat sama sekali)."""
        self.assertIn('id="map-legend"', self.content)
        self.assertIn("Keluar", self.content)
        self.assertIn("Masuk", self.content)
        self.assertIn("Transit", self.content)
        self.assertIn("Jalur kekuasaan", self.content)
        self.assertIn("Atjeh", self.content)


class LayoutBSecurityTest(SimpleTestCase):
    """Security checks for Layout B template."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_csp_not_in_meta_tag(self):
        """CSP dipindah ke Nginx header, tidak boleh ada di meta tag (penyebab tile blocking)."""
        self.assertNotIn('<meta http-equiv="Content-Security-Policy"', self.content)

    def test_no_hardcoded_api_keys_in_page(self):
        """Page source must not contain any hardcoded API keys or secrets."""
        suspicious_patterns = ["sk-", "apikey=", "api_key=", "secret="]
        for pattern in suspicious_patterns:
            self.assertNotIn(pattern.lower(), self.content.lower(),
                             msg=f"Suspicious pattern '{pattern}' found in page source")

    def test_esc_function_defined(self):
        """esc() XSS-escaping helper must be defined in atlas.js (extracted in US-11)."""
        self.assertIn("function esc(", ATLAS_JS)

    def test_no_inline_user_data_in_html(self):
        """Initial HTML must not embed raw user data — data loaded via fetch."""
        # The page should not have voyage data baked into the HTML
        self.assertNotIn('"ship_name":', self.content)
        self.assertNotIn('"total_gulden":', self.content)


class LayoutBAccessibilityTest(SimpleTestCase):
    """Basic accessibility checks for Layout B markup."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_html_lang_attribute_set(self):
        """html element must have lang='id' for Indonesian language."""
        self.assertIn('lang="id"', self.content)

    def test_meta_viewport_present(self):
        """Viewport meta tag must be present for mobile support."""
        self.assertIn('name="viewport"', self.content)

    def test_aria_live_on_stats_badge(self):
        """Stats badge must have aria-live for dynamic updates."""
        self.assertIn("aria-live", self.content)

    def test_search_has_aria_expanded(self):
        """Ship search input must have aria-expanded for dropdown state."""
        self.assertIn("aria-expanded", self.content)

    def test_escape_key_handler_defined(self):
        """Keyboard Escape handler must be defined in atlas.js (extracted in US-11)."""
        self.assertIn('"Escape"', ATLAS_JS)

    def test_port_card_keyboard_handler_defined(self):
        """Port card keyboard handler must exist in atlas.js (extracted in US-11)."""
        self.assertIn("onkeydown", ATLAS_JS)


# ---------------------------------------------------------------------------
# US-05 — Direction Toggle
# ---------------------------------------------------------------------------

class DirectionToggleTest(SimpleTestCase):
    """US-05 — 3 toggle buttons untuk filter arah pelayaran di navbar."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_direction_toggle_group_present(self):
        """Group tombol arah (dir-toggle-group) harus ada di navbar."""
        self.assertIn("dir-toggle-group", self.content)

    def test_dir_all_button_present(self):
        """Tombol 'Semua' (#dir-all) harus ada dan default active."""
        self.assertIn('id="dir-all"', self.content)

    def test_dir_outbound_button_present(self):
        """Tombol 'Keluar' (#dir-out) untuk filter outbound harus ada."""
        self.assertIn('id="dir-out"', self.content)

    def test_dir_inbound_button_present(self):
        """Tombol 'Masuk' (#dir-in) untuk filter inbound harus ada."""
        self.assertIn('id="dir-in"', self.content)

    def test_set_direction_function_defined(self):
        """Fungsi setDirection() harus terdefinisi di atlas.js (extracted in US-11)."""
        self.assertIn("function setDirection(", ATLAS_JS)

    def test_active_direction_state_variable(self):
        """State variable activeDirection harus ada di atlas.js (extracted in US-11)."""
        self.assertIn("activeDirection", ATLAS_JS)

    def test_direction_filter_passed_to_api(self):
        """drawRoutes harus kirim direction ke API — check atlas.js (extracted in US-11)."""
        self.assertIn('params.set("direction", activeDirection)', ATLAS_JS)

    def test_direction_buttons_have_aria_pressed(self):
        """Tombol toggle harus punya aria-pressed untuk aksesibilitas."""
        self.assertIn('aria-pressed', self.content)


# ---------------------------------------------------------------------------
# P0.3b — Source/Provenance Toggle (docs/prd-cleaning-daghregister-1660-1669.md)
# ---------------------------------------------------------------------------

class SourceToggleTest(SimpleTestCase):
    """P0.3b — filter provenance data pelayaran di navbar.
    Diubah dari 3 tombol pill jadi <select> dropdown (2026-07-07) supaya gampang
    diperluas kalau sumber baru muncul (mis. GLOBALISE OBP) tanpa navbar penuh tombol."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_source_select_present(self):
        """Dropdown filter sumber (#source-select) harus ada di navbar."""
        self.assertIn('id="source-select"', self.content)

    def test_source_select_has_all_option(self):
        """Opsi 'Semua Sumber' harus ada dan default selected."""
        self.assertIn('value="all" selected', self.content)

    def test_source_select_has_bgb_option(self):
        """Opsi filter BGB Huygens harus ada."""
        self.assertIn('value="bgb_huygens"', self.content)

    def test_source_select_has_daghregister_option(self):
        """Opsi filter Dagh-register harus ada."""
        self.assertIn('value="daghregister_batavia"', self.content)

    def test_set_source_function_defined(self):
        """Fungsi setSource() harus terdefinisi di atlas.js."""
        self.assertIn("function setSource(", ATLAS_JS)

    def test_active_source_state_variable(self):
        """State variable activeSource harus ada di atlas.js."""
        self.assertIn("activeSource", ATLAS_JS)

    def test_source_filter_passed_to_api(self):
        """drawRoutes harus kirim source ke API kalau bukan 'all'."""
        self.assertIn('params.set("source", activeSource)', ATLAS_JS)

    def test_source_select_wired_to_onchange(self):
        """Dropdown harus panggil setSource(this.value) saat berubah."""
        self.assertIn("onchange=\"setSource(this.value)\"", self.content)

    def test_modal_shows_source_label(self):
        """Modal voyage harus menampilkan baris 'Sumber Data' (P0.3b)."""
        self.assertIn("MODAL_SOURCE_LABELS", ATLAS_JS)

    def test_fort_coords_populated_dynamically_from_api(self):
        """Regresi bug 2026-07-07: FORT_COORDS hardcode cuma 9 pelabuhan awal — fort
        baru (Tiku dll, node regional) garis+markernya diam-diam tidak tergambar.
        loadForts() harus mengisi FORT_COORDS dari API utk fort yg belum ada."""
        self.assertIn("if (!FORT_COORDS[f.name]", ATLAS_JS)

    def test_aceh_routes_have_explicit_sea_waypoints(self):
        """Bug 2026-07-13: rute Aceh (Aceh<->Batavia, Aceh->Tiku) tak punya entri di
        SEA_WAYPOINTS, jadi jatuh ke fallback getBezierCurve() -- lengkung bezier generik
        yg arah bengkoknya tergantung tanda vektor origin->destination, BUKAN geografi
        nyata. Efeknya salah satu arah pasangan (mis. Batavia->Aceh) melengkung ke sisi
        yg salah (memotong lewat utara/Selat Malaka) alih-alih menyusuri pantai barat
        Sumatra spt rute pelabuhan westkust lain. Harus ada waypoint eksplisit spy
        konsisten & presisi (garis penuh, bukan dashed 'perkiraan')."""
        for key in ("Aceh→Batavia", "Batavia→Aceh", "Aceh→Tiku"):
            self.assertIn(f'"{key}"', ATLAS_JS, f"SEA_WAYPOINTS harus punya entri {key}")

    def test_inderapura_routes_have_explicit_sea_waypoints(self):
        """Pola bug sama dgn Aceh (test di atas) -- Inderapura<->Batavia & Padang<->
        Inderapura tak punya waypoint eksplisit, jatuh ke fallback bezier. Ketahuan
        2026-07-13 saat cek rute jacht Sardam (voyage 1636)."""
        for key in ("Inderapura→Batavia", "Batavia→Inderapura", "Padang→Inderapura", "Inderapura→Padang"):
            self.assertIn(f'"{key}"', ATLAS_JS, f"SEA_WAYPOINTS harus punya entri {key}")

    def test_no_hover_tooltips_on_map_layers(self):
        """User 2026-07-13: hapus SEMUA tooltip hover (pelabuhan, catatan politik,
        rute) -- info politik & rincian kapal cukup ada di /riset/atjeh-dagang,
        peta sendiri tak perlu tooltip. Regresi kalau ada yg nambah bindTooltip()
        balik ke marker/garis tanpa sepengetahuan user."""
        self.assertNotIn("marker.bindTooltip(", ATLAS_JS)
        self.assertNotIn("ant.bindTooltip(", ATLAS_JS)
        self.assertNotIn("line.bindTooltip(", ATLAS_JS)
        self.assertNotIn("function fortTooltipHtml(", ATLAS_JS)

    def test_political_data_still_loaded_for_power_routes(self):
        """Tooltip dihapus, tapi loadPoliticalNotes()/politicalNotesForFort() tetap
        wajib ada -- itu yg menentukan kapal jalur kekuasaan mana yg digambar,
        bukan cuma buat isi tooltip yg sekarang sudah tak ada."""
        self.assertIn("function loadPoliticalNotes(", ATLAS_JS)
        self.assertIn("function politicalNotesForFort(", ATLAS_JS)
        self.assertIn("PORT_TEXT_ALIASES", ATLAS_JS)
        self.assertIn("direction=politik", ATLAS_JS)

    def test_power_routes_drawn_for_political_evidence_without_voyage(self):
        """User: hubungan Aceh<->Pariaman/Inderapura (cuma bukti politik, tak ada
        voyage tercatat) harus tetap kelihatan sbg GARIS di peta. Garis ini "jalur
        kekuasaan", HARUS beda gaya dari garis pelayaran asli (bukan antPath
        animasi, warna beda) supaya tak menyesatkan pembaca peta."""
        self.assertIn("function drawPowerRoutes(", ATLAS_JS)
        self.assertIn("drawPowerRoutes(politicalRows, forts)", ATLAS_JS)
        self.assertIn("POWER_ROUTE_COLOR", ATLAS_JS)
        self.assertIn("jalur kekuasaan", ATLAS_JS)

    def test_power_routes_drawn_on_top_and_stay_visible(self):
        """Bug 2026-07-13: jalur kekuasaan Aceh->Tiku ketutup garis pelayaran
        Aceh->Tiku yg jalurnya nyaris sama, krn drawPowerRoutes() dipanggil SEBELUM
        drawRoutes() (Leaflet render layer belakangan di atas) -- diam-diam tak
        kelihatan walau datanya benar. Fix: drawPowerRoutes() dipanggil SETELAH
        drawRoutes(), plus bringToFront() dipanggil ULANG tiap drawRoutes() jalan
        (dipicu geser slider tahun) supaya tak ketutup lagi stlh redraw."""
        self.assertIn("l.bringToFront()", ATLAS_JS)
        idx_draw = ATLAS_JS.find("await drawRoutes(yearFrom, yearTo);")
        idx_power = ATLAS_JS.find("drawPowerRoutes(politicalRows, forts);")
        self.assertNotEqual(idx_draw, -1, "await drawRoutes(...) di loadFortsAndRoutes tidak ditemukan")
        self.assertLess(idx_draw, idx_power,
            "drawPowerRoutes() harus dipanggil SETELAH drawRoutes() di loadFortsAndRoutes")

    def test_power_routes_visually_prominent(self):
        """Weight/opacity/dash jalur kekuasaan dinaikkan 2026-07-13 -- versi awal
        (weight 1.5, opacity .55, dash [2,8]) terlalu tipis, hampir tak kelihatan
        di peta walau sudah di atas & datanya benar. Regresi kalau nilainya
        diturunkan lagi tanpa sengaja."""
        self.assertIn("weight: 3.5,", ATLAS_JS)
        self.assertIn("opacity: 0.9,", ATLAS_JS)

    def test_power_routes_skip_batavia_false_positive(self):
        """Batavia (VOC HQ, tempat semua laporan politik dicatat) trivial cocok di
        hampir semua baris politik lewat PORT_TEXT_ALIASES fallback -- HARUS
        dilewati eksplisit, bukan digambar sbg 'jalur kekuasaan Aceh->Batavia'
        yg tak berarti. Ketahuan via verifikasi Playwright 2026-07-13."""
        self.assertIn('f.name === "Aceh" || f.name === "Batavia"', ATLAS_JS)

    def test_power_routes_have_waypoints_for_pariaman_and_inderapura(self):
        """Aceh->Pariaman & Aceh->Inderapura butuh waypoint eksplisit spt Aceh->Tiku
        sebelumnya -- tanpa ini jatuh ke fallback bezier yg bisa salah arah (pola
        bug berulang, lihat feedback_sisir_semua_titik_pemakaian)."""
        for key in ("Aceh→Pariaman", "Aceh→Inderapura"):
            self.assertIn(f'"{key}"', ATLAS_JS, f"SEA_WAYPOINTS harus punya entri {key}")

    def test_map_fits_bounds_to_all_forts(self):
        """Bug besar 2026-07-13: center/zoom awal peta di-hardcode ke [-2.5,103.0]/7,
        yg TIDAK mencakup Aceh (lat 5.56) sama sekali -- semua kerja marker/garis/
        tooltip Aceh sesi2 sebelumnya sia-sia krn selalu di luar layar default.
        map.fitBounds() dari koordinat SEMUA fort (dipanggil setelah forts dimuat)
        menimpa hardcode awal itu, supaya pelabuhan manapun yg ada datanya otomatis
        kelihatan tanpa perlu geser manual -- termasuk kalau nanti ada fort baru
        lebih jauh lagi. Hardcode awal boleh tetap ada sbg state sblm data dimuat."""
        self.assertIn("map.fitBounds(fortLatLngs", ATLAS_JS)

    def test_waypoint_routes_use_smooth_curve_not_straight_segments(self):
        """User: rute yg pakai SEA_WAYPOINTS kelihatan "kaku, garis lurus tegas"
        krn cuma disambung garis lurus antar titik -- beda dgn rute fallback yg
        bezier halus. smoothPath() (Catmull-Rom spline) HARUS dipakai di kedua
        drawRoutes() & drawPowerRoutes(), bukan array waypoint mentah langsung,
        supaya seluruh peta konsisten melengkung."""
        self.assertIn("function smoothPath(", ATLAS_JS)
        self.assertIn("smoothPath([s, ...vias, e])", ATLAS_JS)
        self.assertIn("smoothPath([acehCoords, ...vias, coords])", ATLAS_JS)

    def test_modal_shows_full_dates_when_present(self):
        """Penanggalan (rev.10): modal harus menampilkan departure/arrival date penuh,
        bukan cuma tahun — data kargo ikut tanggal voyage."""
        self.assertIn("function voyageDateText(", ATLAS_JS)
        self.assertIn("Berangkat", ATLAS_JS)
        self.assertIn("Tiba", ATLAS_JS)
        # Daftar sidebar & dropdown pencarian juga harus pakai helper (bukan v.year mentah)
        self.assertGreaterEqual(ATLAS_JS.count("voyageDateText("), 4)

    def test_regional_node_has_sea_waypoints(self):
        """Node regional 'Pantai Barat Sumatra' (voyage Dagh-register terverifikasi
        tanpa pelabuhan spesifik) harus punya jalur laut, bukan bezier lintas darat."""
        self.assertIn("Pantai Barat Sumatra→Batavia", ATLAS_JS)
        self.assertIn("Batavia→Pantai Barat Sumatra", ATLAS_JS)


# ---------------------------------------------------------------------------
# US-02 & US-03 — Port Detail Page
# ---------------------------------------------------------------------------

MOCK_FORT_PADANG_ENRICHED = {
    "id": 3,
    "name": "Padang",
    "latitude": -0.966,
    "longitude": 100.354,
    "color": "#c0392b",
    "description": "Pusat perdagangan VOC di Pantai Barat Sumatra",
    "port_type": "both",
    "nama_historis": "Padangh",
    "designasi_voc": "Sumatras Westcust (VOC-gebied)",
    "fungsi_historis": "Markas komandan perdagangan Pantai Barat Sumatra",
    "periode_aktif": None,
    "amh_url": "https://www.atlasofmutualheritage.nl/page/5751/padang",
    "outbound_voyages": [],
    "inbound_voyages": [],
    "outbound_count": 0,
    "inbound_count": 0,
    "total_value_out": 0.0,
    "total_value_in": 0.0,
    "year_min": None,
    "year_max": None,
    "tally_ship_count": 6,
    "tally_person_count": 39,
}

MOCK_FORT_AIRBANGIS_NO_AMH = {
    "id": 2,
    "name": "Air Bangis",
    "latitude": 0.197,
    "longitude": 99.375,
    "color": "#2980b9",
    "description": "Pelabuhan dagang Air Bangis",
    "port_type": "departure",
    "nama_historis": "Air Bangis",
    "designasi_voc": "Handelshaven",
    "fungsi_historis": "Pos perdagangan lada dan kamfer",
    "periode_aktif": None,
    "amh_url": None,
    "outbound_voyages": [],
    "inbound_voyages": [],
    "outbound_count": 0,
    "inbound_count": 0,
    "total_value_out": 0.0,
    "total_value_in": 0.0,
    "year_min": None,
    "year_max": None,
}

# Slug → fort-id mapping mirroring what the view will implement
_SLUG_TO_ID = {
    "padang": 3,
    "air-bangis": 2,
    "barus": 1,
    "pulau-cingkuak": 4,
}
_ID_TO_MOCK = {
    3: MOCK_FORT_PADANG_ENRICHED,
    2: MOCK_FORT_AIRBANGIS_NO_AMH,
}


def _make_httpx_response(data, status_code=200):
    """Build a minimal mock that mimics httpx.Response."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = data
    mock_resp.raise_for_status = MagicMock()
    return mock_resp


class PortDetailPageTest(SimpleTestCase):
    """
    US-02 & US-03 — /ports/<slug>/ halaman detail pelabuhan historis.

    View membuat 2 httpx.get calls:
      1. GET /api/forts/ → list of forts (untuk lookup by name)
      2. GET /api/forts/{id}/enrichment → dict enrichment data
    Mock menggunakan side_effect=[list_resp, enrichment_resp] per test.
    """

    def setUp(self):
        self.client = Client()

    # ------------------------------------------------------------------
    # US-02 — Halaman detail bisa diakses dan menampilkan field enrichment
    # ------------------------------------------------------------------

    @patch("map_app.views.httpx.get")
    def test_port_detail_padang_returns_200(self, mock_get):
        """GET /ports/padang/ harus return HTTP 200."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_ENRICHED]),
            _make_httpx_response(MOCK_FORT_PADANG_ENRICHED),
        ]
        response = self.client.get("/ports/padang/")
        self.assertEqual(response.status_code, 200)

    @patch("map_app.views.httpx.get")
    def test_port_detail_unknown_returns_404(self, mock_get):
        """GET /ports/tidak-ada/ harus return HTTP 404."""
        mock_get.return_value = _make_httpx_response([])
        response = self.client.get("/ports/tidak-ada/")
        self.assertEqual(response.status_code, 404)

    @patch("map_app.views.httpx.get")
    def test_port_detail_shows_nama_historis(self, mock_get):
        """Halaman detail harus menampilkan nama_historis dari data enrichment."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_ENRICHED]),
            _make_httpx_response(MOCK_FORT_PADANG_ENRICHED),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertIn("Padangh", content)

    @patch("map_app.views.httpx.get")
    def test_port_detail_shows_designasi_voc(self, mock_get):
        """Halaman detail harus menampilkan designasi_voc."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_ENRICHED]),
            _make_httpx_response(MOCK_FORT_PADANG_ENRICHED),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertIn("Sumatras Westcust", content)

    @patch("map_app.views.httpx.get")
    def test_port_detail_shows_fungsi_historis(self, mock_get):
        """Halaman detail harus menampilkan fungsi_historis."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_ENRICHED]),
            _make_httpx_response(MOCK_FORT_PADANG_ENRICHED),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertIn("Markas komandan", content)

    # ------------------------------------------------------------------
    # US-03 — Tombol "Lihat di AMH" dan fallback teks jika null
    # ------------------------------------------------------------------

    @patch("map_app.views.httpx.get")
    def test_port_detail_shows_amh_link(self, mock_get):
        """Jika amh_url tidak null, link atlasofmutualheritage.nl harus tampil."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_ENRICHED]),
            _make_httpx_response(MOCK_FORT_PADANG_ENRICHED),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertIn("atlasofmutualheritage.nl", content)

    @patch("map_app.views.httpx.get")
    def test_port_detail_amh_link_has_target_blank(self, mock_get):
        """Link AMH harus punya target=_blank dan rel=noopener noreferrer (US-03)."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_ENRICHED]),
            _make_httpx_response(MOCK_FORT_PADANG_ENRICHED),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertIn('target="_blank"', content)
        self.assertIn("noopener", content)
        self.assertIn("noreferrer", content)

    @patch("map_app.views.httpx.get")
    def test_port_detail_shows_fallback_no_amh(self, mock_get):
        """Jika amh_url null → tampilkan teks 'Data AMH belum tersedia'."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_AIRBANGIS_NO_AMH]),
            _make_httpx_response(MOCK_FORT_AIRBANGIS_NO_AMH),
        ]
        response = self.client.get("/ports/air-bangis/")
        content = response.content.decode("utf-8")
        self.assertIn("Data AMH belum tersedia", content)
        self.assertNotIn("atlasofmutualheritage.nl", content)

    # ------------------------------------------------------------------
    # P1.2 — Stat kedatangan Dagh-register (docs/prd-port-tally-aggregate.md)
    # ------------------------------------------------------------------

    @patch("map_app.views.httpx.get")
    def test_port_detail_shows_tally_stats_when_present(self, mock_get):
        """Fort dgn tally_ship_count > 0 harus tampilkan angka kedatangan Dagh-register."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_ENRICHED]),
            _make_httpx_response(MOCK_FORT_PADANG_ENRICHED),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertIn("Kedatangan Tercatat", content)
        # rev.11: frasa "belum diverifikasi" DIHAPUS — verifikasi sudah dilakukan tim
        self.assertNotIn("belum diverifikasi", content)

    @patch("map_app.views.httpx.get")
    def test_port_detail_hides_tally_section_when_absent(self, mock_get):
        """Fort tanpa data tally sama sekali tidak boleh tampilkan section-nya."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_AIRBANGIS_NO_AMH]),
            _make_httpx_response(MOCK_FORT_AIRBANGIS_NO_AMH),
        ]
        response = self.client.get("/ports/air-bangis/")
        content = response.content.decode("utf-8")
        self.assertNotIn("Kedatangan Tercatat", content)


# ---------------------------------------------------------------------------
# US-09 — source_url BGB Link di Voyage Modal
# ---------------------------------------------------------------------------

class SourceUrlVoyageModalTest(SimpleTestCase):
    """US-09 — Link sumber BGB harus muncul di voyage modal saat source_url tersedia."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_voyage_modal_has_bgb_link_element(self):
        """Elemen #modal-bgb-link harus ada di DOM sebagai anchor link sumber BGB."""
        self.assertIn('id="modal-bgb-link"', self.content)

    def test_voyage_modal_has_bgb_source_link(self):
        """atlas.js harus mengandung logic untuk render link BGB dari source_url."""
        self.assertIn("source_url", ATLAS_JS)

    def test_bgb_link_has_target_blank(self):
        """Link BGB harus membuka di tab baru (target=_blank)."""
        self.assertIn('target="_blank"', self.content)

    def test_bgb_link_has_noopener(self):
        """Link BGB harus punya rel=noopener noreferrer untuk keamanan."""
        self.assertIn("noopener noreferrer", self.content)

    def test_bgb_link_text_present(self):
        """Teks link BGB harus ada di template sebagai label link."""
        self.assertIn("Lihat sumber di BGB", self.content)

    def test_bgb_link_icon_present(self):
        """Icon ti-external-link harus ada di template untuk visual link eksternal."""
        self.assertIn("ti-external-link", self.content)

    def test_bgb_link_null_fallback(self):
        """Saat source_url null, bgbLink.style.display none — check atlas.js."""
        self.assertIn("bgbLink", ATLAS_JS)


# ---------------------------------------------------------------------------
# US-10 — AMH Gallery (Sumber Kartografi)
# ---------------------------------------------------------------------------

_AMH_IMAGE_ITEM = {
    "title": "Kaart Westkust",
    "creator": "VOC",
    "year": "1780",
    "thumbnail_url": None,
    "page_url": "https://www.atlasofmutualheritage.nl/page/5751/padang",
}

MOCK_FORT_PADANG_WITH_GALLERY = {
    **MOCK_FORT_PADANG_ENRICHED,
    "amh_images": [_AMH_IMAGE_ITEM],
}

MOCK_FORT_PADANG_EMPTY_GALLERY = {
    **MOCK_FORT_PADANG_ENRICHED,
    "amh_images": [],
}


class AmhGalleryTemplateTest(SimpleTestCase):
    """
    US-10 — Gallery kartografi AMH di halaman detail pelabuhan.

    Verifikasi:
      1. Saat amh_images berisi item → seksi "Sumber Kartografi" muncul.
      2. Saat amh_images kosong ([]) → seksi tidak dirender.
      3. page_url dari item gallery muncul sebagai link di halaman.
    """

    def setUp(self):
        self.client = Client()

    @patch("map_app.views.httpx.get")
    def test_gallery_renders_when_amh_images_present(self, mock_get):
        """Jika amh_images berisi ≥1 item, 'Sumber Kartografi' harus muncul di halaman."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_WITH_GALLERY]),
            _make_httpx_response(MOCK_FORT_PADANG_WITH_GALLERY),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertIn("Sumber Kartografi", content)

    @patch("map_app.views.httpx.get")
    def test_gallery_hidden_when_amh_images_empty(self, mock_get):
        """Jika amh_images = [] (kosong), 'Sumber Kartografi' TIDAK boleh muncul di halaman."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_EMPTY_GALLERY]),
            _make_httpx_response(MOCK_FORT_PADANG_EMPTY_GALLERY),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertNotIn("Sumber Kartografi", content)

    @patch("map_app.views.httpx.get")
    def test_gallery_card_has_external_link(self, mock_get):
        """page_url dari item gallery harus muncul sebagai href di halaman."""
        mock_get.side_effect = [
            _make_httpx_response([MOCK_FORT_PADANG_WITH_GALLERY]),
            _make_httpx_response(MOCK_FORT_PADANG_WITH_GALLERY),
        ]
        response = self.client.get("/ports/padang/")
        content = response.content.decode("utf-8")
        self.assertIn(_AMH_IMAGE_ITEM["page_url"], content)


# ─── US-19: CSV Export Button ────────────────────────────────────────────────

class CsvExportButtonTest(SimpleTestCase):
    """Verifikasi tombol Unduh CSV dan fungsi downloadCSV di atlas.js (US-19)."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_csv_export_button_exists(self):
        """#btn-export-csv harus ada di navbar sebagai tombol download."""
        self.assertIn('id="btn-export-csv"', self.content)

    def test_atlas_js_has_download_csv_function(self):
        """atlas.js harus mengandung fungsi downloadCSV untuk trigger browser download."""
        self.assertIn("function downloadCSV(", ATLAS_JS)

    def test_csv_export_button_uses_download_csv(self):
        """Tombol Unduh CSV harus memanggil downloadCSV() via onclick."""
        idx = self.content.find('id="btn-export-csv"')
        self.assertNotEqual(idx, -1, "#btn-export-csv tidak ditemukan di HTML")
        block = self.content[max(0, idx - 20): idx + 200]
        self.assertIn("downloadCSV", block)

    def test_atlas_js_download_uses_api_export_endpoint(self):
        """downloadCSV di atlas.js harus menggunakan /voyages/export sebagai URL endpoint."""
        self.assertIn("voyages/export", ATLAS_JS)


# ─── US-17: Commodity Timeline Slider ────────────────────────────────────────

class TimelineSliderTest(SimpleTestCase):
    """Verifikasi decade range slider (US-17) ada di index.html dan atlas.js."""

    def setUp(self):
        self.client = Client()
        self.content = self.client.get("/").content.decode("utf-8")

    def test_year_from_input_is_range_slider(self):
        """#year-from harus type='range' dengan step='10' — bukan type='number'."""
        self.assertIn('id="year-from"', self.content)
        self.assertIn('type="range"', self.content)
        # Pastikan step=10 ada dalam proximity year-from
        idx = self.content.find('id="year-from"')
        block = self.content[max(0, idx - 50): idx + 200]
        self.assertIn('step="10"', block)

    def test_year_to_input_is_range_slider(self):
        """#year-to harus type='range' dengan step='10' — bukan type='number'."""
        self.assertIn('id="year-to"', self.content)
        idx = self.content.find('id="year-to"')
        block = self.content[max(0, idx - 50): idx + 200]
        self.assertIn('step="10"', block)

    def test_slider_min_covers_aceh_voyages_1620s(self):
        """min='1620' (diperlebar lagi 2026-07-13) -- voyage schip Wapen van Hoorn
        1624 (volume Dagh-register 1624-1629, paling awal disisir sejauh ini) MUSTAHIL
        dijangkau slider kalau min masih 1630. Default value juga ikut ke 1620 (lihat
        test_year_defaults_are_1620_and_1790) -- pola sama spt fix min=1630
        sebelumnya: batas BAWAH & DEFAULT adalah dua hal terpisah, keduanya harus
        ikut melebar bareng."""
        for field_id in ('id="year-from"', 'id="year-to"'):
            idx = self.content.find(field_id)
            self.assertNotEqual(idx, -1, f"{field_id} tidak ditemukan")
            block = self.content[max(0, idx - 50): idx + 200]
            self.assertIn('min="1620"', block)

    def test_slider_value_display_elements_exist(self):
        """#year-from-display dan #year-to-display harus ada sebagai label nilai slider."""
        self.assertIn('id="year-from-display"', self.content)
        self.assertIn('id="year-to-display"', self.content)

    def test_atlas_js_updates_grafik_on_year_change(self):
        """setupYearFilter di atlas.js harus memanggil loadGrafikData() agar KPI update realtime."""
        self.assertIn("loadGrafikData()", ATLAS_JS)
        # Verifikasi loadGrafikData dipanggil dalam konteks setupYearFilter
        idx = ATLAS_JS.find("function setupYearFilter")
        self.assertNotEqual(idx, -1, "setupYearFilter tidak ditemukan di atlas.js")
        func_body = ATLAS_JS[idx: idx + 1000]
        self.assertIn("loadGrafikData", func_body)


# ─── Sea Lane Routing ─────────────────────────────────────────────────────────

class SeaLaneRoutingTest(SimpleTestCase):
    """Verifikasi SEA_WAYPOINTS ada di atlas.js dan mencakup rute utama."""

    def test_sea_waypoints_constant_exists(self):
        """SEA_WAYPOINTS harus ada di atlas.js menggantikan SEA_BENDS."""
        self.assertIn("SEA_WAYPOINTS", ATLAS_JS)

    def test_sea_bends_replaced_by_waypoints(self):
        """SEA_BENDS tidak boleh lagi digunakan sebagai mekanisme routing utama."""
        self.assertNotIn("SEA_BENDS", ATLAS_JS)

    def test_western_ports_to_batavia_have_waypoints(self):
        """Semua pelabuhan westkust utama harus punya waypoint ke Batavia."""
        for port in ["Padang", "Barus", "Air Bangis", "Pulau Cingkuak", "Air Haji"]:
            self.assertIn(f'"{port}→Batavia"', ATLAS_JS,
                          f'Waypoint untuk {port}→Batavia tidak ditemukan di SEA_WAYPOINTS')

    def test_batavia_to_western_ports_have_waypoints(self):
        """Rute inbound Batavia → westkust harus punya waypoint balik."""
        for port in ["Padang", "Barus", "Air Bangis", "Pulau Cingkuak", "Air Haji"]:
            self.assertIn(f'"Batavia→{port}"', ATLAS_JS,
                          f'Waypoint untuk Batavia→{port} tidak ditemukan di SEA_WAYPOINTS')

    def test_drawroutes_uses_sea_waypoints_lookup(self):
        """drawRoutes harus pakai SEA_WAYPOINTS, bukan SEA_BENDS langsung."""
        idx = ATLAS_JS.find("async function drawRoutes")
        self.assertNotEqual(idx, -1, "drawRoutes tidak ditemukan di atlas.js")
        func_body = ATLAS_JS[idx: idx + 2200]
        self.assertIn("SEA_WAYPOINTS", func_body)
        self.assertIn("routeKey", func_body)


# ─── SNK-5: halaman Sankey tema-korpus (/riset/tema, thesis-only) ─────────────
class RisetTemaViewTest(SimpleTestCase):
    """Halaman /riset/tema render statis; data ditarik client-side dari /api/research."""

    def test_returns_200(self):
        resp = self.client.get(reverse("riset_tema"))
        self.assertEqual(resp.status_code, 200)

    def test_noindex_present(self):
        """Thesis-only: WAJIB noindex (SEC-SNK-2) — tidak boleh ter-index Google."""
        html = self.client.get(reverse("riset_tema")).content.decode()
        self.assertIn("noindex", html)
        self.assertIn('name="robots"', html)

    def test_uses_research_endpoint_not_hardcoded_data(self):
        """Diagram ditarik dari endpoint triples; drill dari /rows (bukan data embed)."""
        html = self.client.get(reverse("riset_tema")).content.decode()
        self.assertIn("/api/research/sankey-tema", html)
        self.assertIn("/triples", html)

    def test_uses_salido_fonts(self):
        """Identitas visual salido.my.id: EB Garamond + Space Grotesk."""
        html = self.client.get(reverse("riset_tema")).content.decode()
        self.assertIn("EB Garamond", html)
        self.assertIn("Space Grotesk", html)

    def test_filters_to_daghregister_only(self):
        """SPLIT-1: halaman ini HARUS memisahkan ke corpus_asal=daghregister,
        bukan lagi menggabung GLOBALISE (diganti /riset/petunjuk-arsip)."""
        html = self.client.get(reverse("riset_tema")).content.decode()
        self.assertIn("corpus_asal=daghregister", html)

    def test_links_to_petunjuk_arsip(self):
        """Nav resiprokal ke halaman GLOBALISE baru (sibling relatif di bawah /riset/)."""
        html = self.client.get(reverse("riset_tema")).content.decode()
        self.assertIn("../petunjuk-arsip/", html)


# ─── SPLIT-1: halaman Petunjuk Arsip GLOBALISE (/riset/petunjuk-arsip) ────────
class RisetPetunjukArsipViewTest(SimpleTestCase):
    """Halaman /riset/petunjuk-arsip render statis; data ditarik client-side dari
    /api/research?corpus_asal=globalise. Dipisah dari /riset/tema karena GLOBALISE
    adalah metadata katalog/finding-aid arsip, bukan narasi peristiwa -- lihat
    docs/prd-split-tema-globalise-daghregister.md."""

    def test_returns_200(self):
        resp = self.client.get(reverse("riset_petunjuk_arsip"))
        self.assertEqual(resp.status_code, 200)

    def test_noindex_present(self):
        html = self.client.get(reverse("riset_petunjuk_arsip")).content.decode()
        self.assertIn("noindex", html)
        self.assertIn('name="robots"', html)

    def test_uses_research_endpoint_not_hardcoded_data(self):
        html = self.client.get(reverse("riset_petunjuk_arsip")).content.decode()
        self.assertIn("/api/research/sankey-tema", html)
        self.assertIn("/triples", html)

    def test_filters_to_globalise_only(self):
        html = self.client.get(reverse("riset_petunjuk_arsip")).content.decode()
        self.assertIn("corpus_asal=globalise", html)

    def test_uses_salido_fonts(self):
        html = self.client.get(reverse("riset_petunjuk_arsip")).content.decode()
        self.assertIn("EB Garamond", html)
        self.assertIn("Space Grotesk", html)

    def test_does_not_claim_ocr_narrative(self):
        """Framing HARUS jujur: ini indeks katalog, bukan kutipan narasi mata-saksi
        seperti Dagh-register -- inti keputusan strategis pemisahan ini."""
        html = self.client.get(reverse("riset_petunjuk_arsip")).content.decode()
        self.assertIn("bukan narasi peristiwa", html)

    def test_links_back_to_riset_tema(self):
        """Nav resiprokal ke halaman Dagh-register (sibling relatif di bawah /riset/)."""
        html = self.client.get(reverse("riset_petunjuk_arsip")).content.decode()
        self.assertIn("../tema/", html)


# ─── Network Graph Fase 1: halaman jaringan pelabuhan (/riset/jaringan) ────────
class RisetJaringanViewTest(SimpleTestCase):
    """Halaman /riset/jaringan render statis; graf ditarik client-side dari
    /api/research/network-pelabuhan, drill dari /sankey-tema/rows. thesis-only."""

    def test_returns_200(self):
        resp = self.client.get(reverse("riset_jaringan"))
        self.assertEqual(resp.status_code, 200)

    def test_noindex_present(self):
        """Thesis-only: WAJIB noindex (konsisten /riset/tema) — tak boleh ter-index."""
        html = self.client.get(reverse("riset_jaringan")).content.decode()
        self.assertIn("noindex", html)
        self.assertIn('name="robots"', html)

    def test_uses_network_endpoint_not_hardcoded_data(self):
        """Graf ditarik dari endpoint network-pelabuhan; drill dari /rows (bukan embed)."""
        html = self.client.get(reverse("riset_jaringan")).content.decode()
        self.assertIn("/api/research/network-pelabuhan", html)
        self.assertIn("/sankey-tema/rows", html)

    def test_uses_salido_fonts(self):
        """Identitas visual salido.my.id: EB Garamond + Space Grotesk."""
        html = self.client.get(reverse("riset_jaringan")).content.decode()
        self.assertIn("EB Garamond", html)
        self.assertIn("Space Grotesk", html)

    def test_links_to_petunjuk_arsip(self):
        """SPLIT-1: nav harus menautkan ke halaman GLOBALISE baru juga (sibling relatif)."""
        html = self.client.get(reverse("riset_jaringan")).content.decode()
        self.assertIn("../petunjuk-arsip/", html)


# ─── Dagang Atjeh 1643-1644 + 1631-1634: laporan dagang (/riset/atjeh-dagang) ──
class RisetAtjehViewTest(SimpleTestCase):
    """Halaman /riset/atjeh-dagang render statis; tabel ditarik client-side dari
    /api/research/atjeh-trade. thesis-only, bukti HARUS tampil jujur per pelabuhan
    -- lihat konteks percakapan: Barus tetap nihil bukti di 2 volume; Tiku/Pariaman/
    Indrapura sekarang punya bukti kuat (titah pembatasan dagang 1633, volume
    1631-1634) -- caveat lama yg bilang 'Pariaman nihil' sudah usang & diperbaiki."""

    def test_returns_200(self):
        resp = self.client.get(reverse("riset_atjeh"))
        self.assertEqual(resp.status_code, 200)

    def test_noindex_present(self):
        """Thesis-only: WAJIB noindex (konsisten /riset/tema & /riset/jaringan)."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn("noindex", html)
        self.assertIn('name="robots"', html)

    def test_uses_atjeh_trade_endpoint_not_hardcoded_data(self):
        """Tabel ditarik dari endpoint atjeh-trade (bukan data embed statis)."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn("/api/research/atjeh-trade", html)

    def test_uses_salido_fonts(self):
        """Identitas visual salido.my.id: EB Garamond + Space Grotesk."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn("EB Garamond", html)
        self.assertIn("Space Grotesk", html)

    def test_surfaces_unverified_caveat(self):
        """Data blm dicocokkan ke scan asli -- caveat 'unverified'/'belum diverifikasi'
        wajib terlihat di halaman, bukan cuma di field JSON tersembunyi."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertTrue(
            "belum diverifikasi" in html.lower() or "unverified" in html.lower()
        )

    def test_surfaces_barus_still_absent(self):
        """Kejujuran evidentiary: Barus TETAP tak punya bukti eksplisit di 2 volume
        yg sudah disisir -- halaman harus bilang ini, bukan diam."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn("Barus", html)

    def test_surfaces_1633_licensing_edict(self):
        """Temuan utama volume 1631-1634: titah Raja Atjeh membatasi dagang VOC/
        Inggris HANYA di Tiku, Pariaman, Indrapura (1633) -- harus tampil eksplisit,
        bukan cuma ada di data JSON."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn("Tiku", html)
        self.assertIn("Pariaman", html)
        self.assertIn("Indrapura", html)
        self.assertIn("1633", html)

    def test_five_volumes_mentioned(self):
        """Lima volume PDF sumber (1643-1644, 1631-1634, 1637, 1636, 1624-1629) harus disebut eksplisit."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn("1643-1644", html)
        self.assertIn("1631-1634", html)
        self.assertIn("1637", html)
        self.assertIn("1636", html)
        self.assertIn("1624-1629", html)

    def test_1637_volume_option_in_filter(self):
        """Dropdown filter volume harus punya opsi 1637 (regresi 2026-07-13)."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn('value="1637"', html)

    def test_1636_volume_option_in_filter(self):
        """Dropdown filter volume harus punya opsi 1636 (regresi 2026-07-13)."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn('value="1636"', html)

    def test_1624_1629_volume_option_in_filter(self):
        """Dropdown filter volume harus punya opsi 1624-1629 (regresi 2026-07-13)."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn('value="1624-1629"', html)

    def test_politik_direction_option_in_filter(self):
        """Dropdown filter arah harus punya opsi 'politik' (kategori ke-4, dipisah
        dari 'in_atjeh' 2026-07-13 atas permintaan user -- fakta politik/administratif
        Atjeh bukan lagi bercampur dgn transaksi dagang di dalam Atjeh)."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn('value="politik"', html)

    def test_links_to_petunjuk_arsip(self):
        """SPLIT-1: nav harus menautkan ke halaman GLOBALISE baru juga (sibling relatif)."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn("../petunjuk-arsip/", html)


# ─── Linimasa Suksesi Atjeh (top-level /linimasa) ────────────────────────────
class LinimasaViewTest(SimpleTestCase):
    """Halaman /linimasa render statis; linimasa ditarik client-side dari
    /api/research/linimasa. thesis-only, top-level route (BUKAN di bawah
    /riset/*) atas permintaan eksplisit user."""

    def test_returns_200(self):
        resp = self.client.get(reverse("linimasa"))
        self.assertEqual(resp.status_code, 200)

    def test_url_is_top_level_not_under_riset(self):
        """User eksplisit minta /linimasa top-level, bukan /riset/linimasa."""
        resp = self.client.get("/linimasa/")
        self.assertEqual(resp.status_code, 200)

    def test_noindex_present(self):
        html = self.client.get(reverse("linimasa")).content.decode()
        self.assertIn("noindex", html)
        self.assertIn('name="robots"', html)

    @patch("map_app.views.httpx.get")
    def test_fetches_from_linimasa_endpoint_not_hardcoded_data(self, mock_get):
        """View harus tarik data lewat httpx.get ke /api/research/linimasa (SSR
        sinkron, Fase 1) -- bukan data hardcode. String endpoint sendiri sudah
        tak lagi bocor ke HTML sejak fetch() client-side dihapus (lihat
        LinimasaSsrTest di bawah utk bukti SSR-nya)."""
        mock_get.return_value = _make_httpx_response({"items": [], "meta": {}})
        self.client.get(reverse("linimasa"))
        mock_get.assert_called_once()
        called_url = mock_get.call_args[0][0]
        self.assertIn("/api/research/linimasa", called_url)

    def test_uses_salido_fonts(self):
        html = self.client.get(reverse("linimasa")).content.decode()
        self.assertIn("EB Garamond", html)
        self.assertIn("Space Grotesk", html)

    def test_surfaces_unverified_caveat(self):
        html = self.client.get(reverse("linimasa")).content.decode()
        self.assertTrue(
            "belum diverifikasi" in html.lower() or "unverified" in html.lower()
        )

    def test_mentions_iskandar_muda_and_painan(self):
        """Arc utama linimasa (Iskandar Muda -> Traktat Painan) harus tampil
        eksplisit di halaman, bukan cuma ada di data JSON."""
        html = self.client.get(reverse("linimasa")).content.decode()
        self.assertIn("Iskandar Muda", html)
        self.assertIn("Painan", html)

    def test_flags_dual_pipeline_provenance(self):
        """Baris 1663 sumbernya beda pipeline (korpus_tema_slim.csv, terjemahan)
        dari baris lain (OCR docs/ kita) -- caveat wajib eksplisit."""
        html = self.client.get(reverse("linimasa")).content.decode()
        self.assertIn("korpus_tema_slim.csv", html)

    def test_event_type_filter_options_present(self):
        html = self.client.get(reverse("linimasa")).content.decode()
        self.assertIn('value="suksesi"', html)
        self.assertIn('value="perjanjian"', html)

    def test_reciprocal_link_from_riset_atjeh(self):
        """Konvensi proyek: halaman riset baru ditautkan resiprokal dari
        halaman riset lain, dan sebaliknya."""
        html = self.client.get(reverse("riset_atjeh")).content.decode()
        self.assertIn("/linimasa/", html)


# ─── Linimasa Fase 1: SSR fallback + narasi berbab (docs/prd-linimasa-kronik-pantai-barat.md) ──

MOCK_LINIMASA_ITEMS = [
    {
        "id": 1, "source_document": "1624-1629", "source_page": 12, "book_page": "9",
        "event_date_raw": "29 Sep 1625", "year": 1625, "event_type": "administratif",
        "ruler_actor": "Coninck van Atchijn", "title": "Klaim yurisdiksi Atjeh atas seluruh pantai Sumatra",
        "era_slug": "klaim-awal",
        "text_asli": "dat den geheelen zeecant van Sumatra onder het gebiedt van Atchijn behoort",
        "confidence_flag": "unverified", "notes": None,
    },
    {
        "id": 2, "source_document": "1647-1648", "source_page": 94, "book_page": "80",
        "event_date_raw": "Mei 1648", "year": 1648, "event_type": "diplomasi",
        "ruler_actor": "Ratu van Atchijn", "title": "Ratu Atjeh menegaskan yurisdiksi atas Perak",
        "era_slug": "ratu-puncak",
        "text_asli": "de Con.ne van Atchijn... alle landen ende havens",
        "confidence_flag": "unverified", "notes": None,
    },
    {
        "id": 3, "source_document": "1656-1657", "source_page": 51, "book_page": "44",
        "event_date_raw": "Feb 1657", "year": 1657, "event_type": "konflik",
        "ruler_actor": "panglima van Sillida", "title": "Ekspedisi hukuman VOC bebaskan tawanan Sillida",
        "era_slug": "perang-damai",
        "text_asli": "200 soldaten... de gevangenen tot Sillida verlost",
        "confidence_flag": "unverified", "notes": None,
    },
    {
        "id": 4, "source_document": "1663", "source_page": 86, "book_page": "70",
        "event_date_raw": "27 Maret 1663", "year": 1663, "event_type": "perjanjian",
        "ruler_actor": "Songypagouers", "title": "Traktat Painan ditandatangani",
        "era_slug": "retak-painan",
        "text_asli": "1º diluaskan pertjajaan antara VOC ende de confederatie Songypagouers",
        "confidence_flag": "unverified", "notes": "SUMBER BEDA PIPELINE: korpus_tema_slim.csv",
    },
    {
        "id": 5, "source_document": "1681", "source_page": 12, "book_page": "8",
        "event_date_raw": "1681", "year": 1681, "event_type": "perjanjian",
        "ruler_actor": "radja hulu/hilir Barus", "title": "Traktat Barus: penyerahan mahkota Atjeh",
        "era_slug": "pengusiran-penataan",
        "text_asli": "de overgebleven wapenen van de croon van Atchijn",
        "confidence_flag": "unverified", "notes": "SUMBER BEDA PIPELINE: korpus_tema_slim.csv",
    },
]

MOCK_LINIMASA_META = {
    "n_items": 5,
    "by_event_type": {"administratif": 1, "diplomasi": 1, "konflik": 1, "perjanjian": 2},
    "year_min": 1625, "year_max": 1681,
}


class LinimasaSsrTest(SimpleTestCase):
    """Fase 1 (docs/prd-linimasa-kronik-pantai-barat.md): konten utama harus
    terbaca tanpa JavaScript -- view SSR penuh dari httpx.get() sinkron
    (bukan fetch() client-side seperti riset_tema/riset_jaringan/riset_atjeh)."""

    def setUp(self):
        self.client = Client()

    @patch("map_app.views.httpx.get")
    def test_content_rendered_server_side(self, mock_get):
        """Judul & kutipan event spesifik harus muncul LANGSUNG di response.content
        tanpa eksekusi JS -- bukti SSR nyata."""
        mock_get.return_value = _make_httpx_response({"items": MOCK_LINIMASA_ITEMS, "meta": MOCK_LINIMASA_META})
        response = self.client.get(reverse("linimasa"))
        content = response.content.decode("utf-8")
        self.assertIn("Klaim yurisdiksi Atjeh atas seluruh pantai Sumatra", content)
        self.assertIn("Traktat Painan ditandatangani", content)
        self.assertIn("dat den geheelen zeecant van Sumatra", content)
        self.assertIn("de overgebleven wapenen van de croon van Atchijn", content)

    @patch("map_app.views.httpx.get")
    def test_era_headers_present(self, mock_get):
        """Label babak (era) harus muncul di HTML, dikelompokkan per event yang
        ada -- narasi berbab, bukan list kronologis datar."""
        mock_get.return_value = _make_httpx_response({"items": MOCK_LINIMASA_ITEMS, "meta": MOCK_LINIMASA_META})
        response = self.client.get(reverse("linimasa"))
        content = response.content.decode("utf-8")
        self.assertIn("Kontrak Pertama", content)
        self.assertIn("Ratu Atjeh", content)
        self.assertIn("Perang", content)
        self.assertIn("Pemberontakan Painan", content)
        self.assertIn("Penataan Ulang", content)

    @patch("map_app.views.httpx.get")
    def test_cards_use_native_details_disclosure(self, mock_get):
        """Card harus <details class="card"> -- disclosure native HTML5, bisa
        dibuka tanpa JS (progressive enhancement, bukan div+class toggle JS)."""
        mock_get.return_value = _make_httpx_response({"items": MOCK_LINIMASA_ITEMS, "meta": MOCK_LINIMASA_META})
        response = self.client.get(reverse("linimasa"))
        content = response.content.decode("utf-8")
        self.assertIn('<details class="card"', content)
        self.assertIn("<summary>", content)

    @patch("map_app.views.httpx.get")
    def test_no_client_side_fetch_of_linimasa_api(self, mock_get):
        """JS tak lagi fetch() ke /api/research/linimasa saat load -- data sudah
        inline via items_json, cuma dipakai timeline SVG & filter (non-destruktif)."""
        mock_get.return_value = _make_httpx_response({"items": MOCK_LINIMASA_ITEMS, "meta": MOCK_LINIMASA_META})
        response = self.client.get(reverse("linimasa"))
        content = response.content.decode("utf-8")
        self.assertNotIn("fetch(API)", content)
        self.assertIn('id="linimasa-data"', content)

    @patch("map_app.views.httpx.get")
    def test_backend_error_still_renders_page_structure(self, mock_get):
        """Kalau backend gagal, halaman TETAP render strukturnya (bukan 500/Http404)
        -- beda dari port_detail yg memang 404 kalau target tak ada."""
        mock_get.side_effect = Exception("connection refused")
        response = self.client.get(reverse("linimasa"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Backend tidak terjangkau", content)
