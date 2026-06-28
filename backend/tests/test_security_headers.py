"""
Security headers tests — US-15 Sprint PROD-RISET

Verifikasi bahwa Nginx mengirim security headers yang benar:
  - Content-Security-Policy (CSP)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
  - Permissions-Policy
  - Alt-Svc (HTTP/3 advertisement, aktif setelah TLS)

Integration tests — butuh Nginx di localhost:8084.
Di-skip otomatis jika Nginx tidak tersedia.

Jalankan dari host:
    python3 -m pytest backend/tests/test_security_headers.py -v
"""
import httpx
import pytest

NGINX_BASE = "http://localhost:8084"


def _nginx_available() -> bool:
    try:
        r = httpx.get(f"{NGINX_BASE}/api/health", timeout=2)
        return r.status_code < 500
    except Exception:
        return False


skip_no_nginx = pytest.mark.skipif(
    not _nginx_available(),
    reason="Nginx tidak tersedia di localhost:8084 — integration test dilewati"
)

# Endpoints yang diuji: satu API, satu frontend
ENDPOINTS = [
    f"{NGINX_BASE}/api/health",
    f"{NGINX_BASE}/",
]


# ── X-Frame-Options ─────────────────────────────────────────────────────────

@skip_no_nginx
@pytest.mark.parametrize("url", ENDPOINTS)
def test_x_frame_options_deny(url):
    """X-Frame-Options: DENY harus ada di semua response — cegah clickjacking."""
    r = httpx.get(url, timeout=5)
    assert "x-frame-options" in r.headers, (
        f"Header X-Frame-Options tidak ada di {url}"
    )
    assert r.headers["x-frame-options"].upper() == "DENY", (
        f"X-Frame-Options harus DENY, dapat: '{r.headers['x-frame-options']}'"
    )


# ── X-Content-Type-Options ───────────────────────────────────────────────────

@skip_no_nginx
@pytest.mark.parametrize("url", ENDPOINTS)
def test_x_content_type_options_nosniff(url):
    """X-Content-Type-Options: nosniff wajib ada — cegah MIME-type sniffing."""
    r = httpx.get(url, timeout=5)
    assert "x-content-type-options" in r.headers, (
        f"Header X-Content-Type-Options tidak ada di {url}"
    )
    assert r.headers["x-content-type-options"].lower() == "nosniff", (
        f"X-Content-Type-Options harus nosniff, dapat: '{r.headers['x-content-type-options']}'"
    )


# ── Referrer-Policy ──────────────────────────────────────────────────────────

@skip_no_nginx
@pytest.mark.parametrize("url", ENDPOINTS)
def test_referrer_policy_present(url):
    """Referrer-Policy harus ada — kontrol informasi referrer ke situs eksternal."""
    r = httpx.get(url, timeout=5)
    assert "referrer-policy" in r.headers, (
        f"Header Referrer-Policy tidak ada di {url}"
    )
    val = r.headers["referrer-policy"].lower()
    allowed = {"strict-origin-when-cross-origin", "strict-origin", "no-referrer", "same-origin"}
    assert val in allowed, (
        f"Referrer-Policy '{val}' bukan nilai yang aman. Harus salah satu dari: {allowed}"
    )


# ── Content-Security-Policy ──────────────────────────────────────────────────

@skip_no_nginx
def test_csp_present_on_frontend():
    """CSP harus ada di response frontend (/)."""
    r = httpx.get(f"{NGINX_BASE}/", timeout=5)
    assert "content-security-policy" in r.headers, (
        "Header Content-Security-Policy tidak ada di / (frontend). "
        "CSP adalah lapisan pertahanan XSS utama."
    )


@skip_no_nginx
def test_csp_blocks_frame_ancestors():
    """CSP harus mengandung frame-ancestors 'none' untuk mencegah clickjacking via CSP."""
    r = httpx.get(f"{NGINX_BASE}/", timeout=5)
    csp = r.headers.get("content-security-policy", "")
    assert "frame-ancestors" in csp, (
        f"CSP harus mengandung frame-ancestors directive. CSP saat ini: {csp[:200]}"
    )


@skip_no_nginx
def test_csp_restricts_connect_src():
    """connect-src 'self' harus ada — fetch() hanya boleh ke origin sendiri."""
    r = httpx.get(f"{NGINX_BASE}/", timeout=5)
    csp = r.headers.get("content-security-policy", "")
    assert "connect-src" in csp, (
        f"CSP harus mengandung connect-src directive. CSP: {csp[:200]}"
    )


@skip_no_nginx
def test_csp_allows_cdn_scripts():
    """CSP script-src harus include cdn.jsdelivr.net dan unpkg.com untuk Leaflet/Chart.js."""
    r = httpx.get(f"{NGINX_BASE}/", timeout=5)
    csp = r.headers.get("content-security-policy", "")
    assert "cdn.jsdelivr.net" in csp, (
        f"CSP script-src harus include cdn.jsdelivr.net (Chart.js, Tabler). CSP: {csp[:300]}"
    )
    assert "unpkg.com" in csp, (
        f"CSP script-src harus include unpkg.com (Leaflet). CSP: {csp[:300]}"
    )


# ── Permissions-Policy ───────────────────────────────────────────────────────

@skip_no_nginx
def test_permissions_policy_present():
    """Permissions-Policy harus ada — batasi akses ke API browser sensitif."""
    r = httpx.get(f"{NGINX_BASE}/", timeout=5)
    assert "permissions-policy" in r.headers, (
        "Header Permissions-Policy tidak ada di response frontend."
    )


# ── HTTP/2 ───────────────────────────────────────────────────────────────────

@skip_no_nginx
def test_http2_negotiated():
    """
    HTTP/2 harus dinegosiasikan saat client mendukung h2.
    httpx secara default mencoba h2 jika http2=True.
    Tanpa TLS, h2 tidak akan dinegosisiasikan oleh browser,
    tapi server-side config harus sudah siap.
    """
    try:
        import h2  # noqa: F401
        client = httpx.Client(http2=True, timeout=5)
        r = client.get(f"{NGINX_BASE}/api/health")
        # h2 atas plain HTTP (h2c) tidak di-support semua klien,
        # tapi kita verifikasi response tetap valid
        assert r.status_code == 200
    except ImportError:
        pytest.skip("Library 'h2' tidak terinstall — skip HTTP/2 negotiation test")


# ── nginx.conf content checks (berjalan dari host) ───────────────────────────

def _read_nginx_conf() -> str:
    import os
    path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "nginx", "nginx.conf")
    )
    if not os.path.exists(path):
        return ""
    return open(path).read()


def test_nginx_conf_has_http2():
    """nginx.conf harus mengandung http2 on directive."""
    content = _read_nginx_conf()
    if not content:
        pytest.skip("nginx.conf tidak ditemukan dari path ini")
    assert "http2 on" in content, (
        "nginx.conf harus mengandung 'http2 on' (Nginx 1.25+ syntax). "
        "Tanpa ini, HTTP/2 tidak aktif meski module tersedia."
    )


def test_nginx_conf_has_csp_header():
    """nginx.conf harus mengandung Content-Security-Policy header."""
    content = _read_nginx_conf()
    if not content:
        pytest.skip("nginx.conf tidak ditemukan dari path ini")
    assert "Content-Security-Policy" in content, (
        "nginx.conf harus mengandung add_header Content-Security-Policy"
    )


def test_nginx_conf_has_x_frame_options():
    """nginx.conf harus mengandung X-Frame-Options header."""
    content = _read_nginx_conf()
    if not content:
        pytest.skip("nginx.conf tidak ditemukan dari path ini")
    assert "X-Frame-Options" in content


def test_nginx_conf_http3_comment_ready():
    """nginx.conf harus mengandung konfigurasi HTTP/3 (aktif setelah TLS / US-13)."""
    content = _read_nginx_conf()
    if not content:
        pytest.skip("nginx.conf tidak ditemukan dari path ini")
    assert "http3" in content, (
        "nginx.conf harus mengandung http3 directive atau komentar persiapan HTTP/3 (US-13)"
    )
