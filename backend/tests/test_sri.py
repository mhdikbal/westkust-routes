"""
SRI (Subresource Integrity) tests — US-16 Sprint PROD-RISET

Verifikasi bahwa semua CDN asset di index.html dan port_detail.html
menggunakan integrity= + crossorigin=anonymous attribute.

SRI mencegah CDN compromise attack: jika CDN menyajikan file yang dimodifikasi,
browser akan memblokir eksekusinya karena hash tidak cocok.

Catatan:
- Google Fonts (fonts.googleapis.com): CSS dinamis per user-agent, SRI tidak bisa
  digunakan. Didokumentasikan sebagai accepted limitation.
- Tabler Icons @latest: harus dipinned ke versi spesifik sebelum SRI bisa ditambahkan.
  Dipinned ke @3.44.0.
"""
import os
import pytest
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parents[2] / "frontend" / "map_app" / "templates" / "map_app"
INDEX_HTML    = TEMPLATES_DIR / "index.html"
PORT_DETAIL   = TEMPLATES_DIR / "port_detail.html"


def _read(path: Path) -> str:
    if not path.exists():
        pytest.skip(f"File tidak ditemukan: {path}")
    return path.read_text(encoding="utf-8")


# ── Tabler Icons — versi harus di-pin, bukan @latest ────────────────────────

def test_tabler_icons_not_using_latest_tag_in_index():
    """Tabler Icons harus menggunakan versi spesifik, bukan @latest — SRI tidak kompatibel dengan @latest."""
    content = _read(INDEX_HTML)
    assert "@latest" not in content or "tabler" not in content.split("@latest")[0].split("\n")[-1], (
        "Tabler Icons masih menggunakan @latest — pin ke versi spesifik (misal @3.44.0) "
        "sebelum bisa menambahkan SRI hash."
    )


def test_tabler_icons_not_using_latest_tag_in_port_detail():
    """port_detail.html: Tabler Icons harus pin ke versi spesifik."""
    content = _read(PORT_DETAIL)
    # Cek tidak ada @latest pada line yang mengandung tabler
    for line in content.splitlines():
        if "tabler" in line and "@latest" in line:
            pytest.fail(
                f"port_detail.html baris dengan Tabler Icons masih @latest: {line.strip()}"
            )


# ── integrity= attribute wajib ada ──────────────────────────────────────────

CDN_ASSETS_INDEX = [
    ("Leaflet CSS",         "leaflet@1.9.4/dist/leaflet.css"),
    ("Leaflet JS",          "leaflet@1.9.4/dist/leaflet.js"),
    ("leaflet-ant-path JS", "leaflet-ant-path@1.3.0"),
    ("Chart.js",            "chart.js@4.4.0"),
    ("Tabler Icons CSS",    "tabler/icons-webfont@3.44.0"),
]

CDN_ASSETS_PORT_DETAIL = [
    ("Tabler Icons CSS",    "tabler/icons-webfont@3.44.0"),
]


def _tag_block_containing(content: str, url_fragment: str) -> list[str]:
    """
    Kembalikan daftar 'blok tag' (5 baris di sekitar kemunculan url_fragment)
    sebagai string. HTML tag multi-line membutuhkan window pencarian.
    """
    lines = content.splitlines()
    blocks = []
    for i, line in enumerate(lines):
        if url_fragment in line:
            start = max(0, i - 1)
            end = min(len(lines), i + 4)
            blocks.append("\n".join(lines[start:end]))
    return blocks


@pytest.mark.parametrize("name,url_fragment", CDN_ASSETS_INDEX)
def test_index_html_cdn_has_integrity(name, url_fragment):
    """index.html: setiap CDN asset harus punya integrity= attribute (multi-line tag)."""
    content = _read(INDEX_HTML)
    blocks = _tag_block_containing(content, url_fragment)
    assert blocks, f"URL fragment '{url_fragment}' tidak ditemukan di index.html"
    for block in blocks:
        assert "integrity=" in block, (
            f"{name}: tag CDN tidak punya integrity= attribute.\n"
            f"Block: {block.strip()}"
        )


@pytest.mark.parametrize("name,url_fragment", CDN_ASSETS_PORT_DETAIL)
def test_port_detail_html_cdn_has_integrity(name, url_fragment):
    """port_detail.html: setiap CDN asset harus punya integrity= attribute."""
    content = _read(PORT_DETAIL)
    blocks = _tag_block_containing(content, url_fragment)
    assert blocks, f"URL fragment '{url_fragment}' tidak ditemukan di port_detail.html"
    for block in blocks:
        assert "integrity=" in block, (
            f"port_detail.html — {name}: tag CDN tidak punya integrity= attribute.\n"
            f"Block: {block.strip()}"
        )


# ── crossorigin=anonymous wajib ada bersama integrity= ───────────────────────

@pytest.mark.parametrize("name,url_fragment", CDN_ASSETS_INDEX)
def test_index_html_cdn_has_crossorigin(name, url_fragment):
    """Setiap tag dengan integrity= harus juga punya crossorigin=anonymous."""
    content = _read(INDEX_HTML)
    blocks = _tag_block_containing(content, url_fragment)
    assert blocks, f"URL fragment '{url_fragment}' tidak ditemukan di index.html"
    for block in blocks:
        if "integrity=" in block:
            assert "crossorigin=" in block, (
                f"{name}: tag punya integrity= tapi tidak punya crossorigin=.\n"
                f"Tanpa crossorigin=anonymous, browser tidak menerapkan SRI check.\n"
                f"Block: {block.strip()}"
            )


# ── Hash yang benar (sha384) ──────────────────────────────────────────────────

EXPECTED_HASHES = {
    "leaflet@1.9.4/dist/leaflet.css":                  "sha384-sHL9NAb7lN7rfvG5lfHpm643Xkcjzp4jFvuavGOndn6pjVqS6ny56CAt3nsEVT4H",
    "leaflet@1.9.4/dist/leaflet.js":                   "sha384-cxOPjt7s7Iz04uaHJceBmS+qpjv2JkIHNVcuOrM+YHwZOmJGBXI00mdUXEq65HTH",
    "leaflet-ant-path@1.3.0":                          "sha384-bosmXRid5U6b12gQd1FDXneHPric1YAG2B1QuQgLvaYGhqAVo8V4iG36a5zL5g4f",
    "chart.js@4.4.0":                                  "sha384-e6nUZLBkQ86NJ6TVVKAeSaK8jWa3NhkYWZFomE39AvDbQWeie9PlQqM3pmYW5d1g",
    "tabler/icons-webfont@3.44.0":                     "sha384-ccZHbezhtZWmNy0cg8odL0D/jFU5k5HIls9y78Qd6lWor7rpvFIZtK0fTFG4z456",
}


@pytest.mark.parametrize("url_fragment,expected_hash", EXPECTED_HASHES.items())
def test_sri_hash_value_correct(url_fragment, expected_hash):
    """Hash sha384 di index.html harus cocok dengan hash yang sudah diverifikasi."""
    content = _read(INDEX_HTML)
    blocks = _tag_block_containing(content, url_fragment)
    if not blocks:
        content2 = _read(PORT_DETAIL)
        blocks = _tag_block_containing(content2, url_fragment)
    assert blocks, f"URL fragment '{url_fragment}' tidak ditemukan di template manapun"

    for block in blocks:
        assert expected_hash in block, (
            f"Hash SRI untuk '{url_fragment}' tidak cocok atau tidak ada.\n"
            f"Expected: {expected_hash}\n"
            f"Block: {block.strip()}"
        )


# ── Google Fonts — documented exception ──────────────────────────────────────

def test_google_fonts_sri_exception_documented():
    """
    Google Fonts tidak support SRI (CSS dinamis per user-agent).
    Test ini memverifikasi bahwa kita TIDAK salah menambahkan integrity=
    ke Google Fonts tag (karena hash akan selalu berbeda, memblokir fonts).
    """
    content = _read(INDEX_HTML)
    for line in content.splitlines():
        if "fonts.googleapis.com" in line:
            assert "integrity=" not in line, (
                "Google Fonts tidak bisa menggunakan SRI — CSS-nya dinamis.\n"
                "Jangan tambahkan integrity= ke tag Google Fonts.\n"
                f"Baris: {line.strip()}"
            )
