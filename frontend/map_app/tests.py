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

    def test_year_defaults_are_1700_and_1789(self):
        """Default year range must be 1700–1789 as defined in the VOC historical period."""
        self.assertIn('value="1700"', self.content)
        self.assertIn('value="1789"', self.content)


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
