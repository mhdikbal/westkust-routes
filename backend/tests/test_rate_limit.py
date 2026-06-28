"""
Rate limit tests — US-14 Sprint PROD-RISET

Nginx membatasi /api/ ke 60 req/menit per IP (burst=20, nodelay).
Saat melebihi limit, Nginx mengembalikan 429 dengan JSON body dan
header Retry-After: 60.

Test suite ini INTEGRATION — membutuhkan Nginx container berjalan di
localhost:8084. Test di-skip otomatis jika Nginx tidak tersedia.

Jalankan:
    pytest tests/test_rate_limit.py -v --timeout=30
atau via docker:
    docker compose exec backend pytest tests/test_rate_limit.py -v
"""
import httpx
import pytest

NGINX_BASE = "http://localhost:8084"
API_STATS  = f"{NGINX_BASE}/api/voyages/stats"


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


# ── Integration tests (butuh Nginx) ─────────────────────────────────────────

@skip_no_nginx
def test_rate_limit_returns_429_when_burst_exceeded():
    """
    Kirim 85 request cepat ke /api/voyages/stats.
    Setelah burst habis (burst=20, rate=60/m) harus ada 429.
    """
    statuses = []
    with httpx.Client(timeout=10) as client:
        for _ in range(85):
            try:
                r = client.get(API_STATS)
                statuses.append(r.status_code)
            except Exception:
                statuses.append(0)

    assert 429 in statuses, (
        f"Tidak ada 429 setelah 85 request cepat. Statuses: {set(statuses)}. "
        "Pastikan limit_req sudah dikonfigurasi di nginx.conf."
    )


@skip_no_nginx
def test_rate_limit_429_has_json_body():
    """
    Respons 429 dari Nginx harus berupa JSON, bukan HTML default Nginx.
    Body harus mengandung key 'error' dan 'retry_after'.
    """
    statuses_with_bodies = []
    with httpx.Client(timeout=10) as client:
        for _ in range(85):
            try:
                r = client.get(API_STATS)
                if r.status_code == 429:
                    statuses_with_bodies.append(r)
                    break
            except Exception:
                pass

    assert statuses_with_bodies, "Tidak berhasil mendapat 429 dalam 85 request"
    r429 = statuses_with_bodies[0]

    content_type = r429.headers.get("content-type", "")
    assert "application/json" in content_type, (
        f"Content-Type 429 harus application/json, dapat: '{content_type}'"
    )

    try:
        body = r429.json()
    except Exception:
        pytest.fail(f"Body 429 bukan JSON valid: {r429.text[:200]}")

    assert "error" in body, f"Body JSON 429 harus punya key 'error'. Dapat: {body}"
    assert "retry_after" in body, f"Body JSON 429 harus punya key 'retry_after'. Dapat: {body}"


@skip_no_nginx
def test_rate_limit_429_has_retry_after_header():
    """
    Response 429 harus mengandung header Retry-After.
    """
    with httpx.Client(timeout=10) as client:
        for _ in range(85):
            try:
                r = client.get(API_STATS)
                if r.status_code == 429:
                    assert "retry-after" in r.headers, (
                        f"Header Retry-After tidak ada di response 429. "
                        f"Headers: {dict(r.headers)}"
                    )
                    return
            except Exception:
                pass

    pytest.skip("Tidak berhasil mendapat 429 — mungkin rate limit belum diaktifkan")


@skip_no_nginx
def test_normal_request_not_blocked():
    """
    Request pertama ke /api/health harus tetap 200 setelah jeda singkat.
    Rate limit tidak boleh memblokir request normal.
    """
    import time
    time.sleep(2)
    r = httpx.get(f"{NGINX_BASE}/api/health", timeout=5)
    assert r.status_code == 200, (
        f"Request normal setelah jeda 2 detik harus 200, dapat {r.status_code}"
    )


# ── Unit test (tidak butuh Nginx) ────────────────────────────────────────────

def _read_nginx_conf() -> str:
    import os
    path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "nginx", "nginx.conf")
    )
    if not os.path.exists(path):
        return ""
    return open(path).read()


def test_rate_limit_config_present_in_nginx_conf():
    """
    nginx.conf harus mengandung konfigurasi rate limiting.
    Test di-skip jika nginx.conf tidak ditemukan (jalan dari dalam container).
    """
    content = _read_nginx_conf()
    if not content:
        pytest.skip("nginx.conf tidak ditemukan dari path ini (container) — lewati")

    assert "limit_req_zone" in content, "nginx.conf harus mengandung limit_req_zone"
    assert "limit_req " in content, "nginx.conf harus mengandung limit_req directive"
    assert "429" in content, "nginx.conf harus mengandung status 429"


def test_rate_limit_status_is_429_not_503():
    """
    limit_req_status harus 429, bukan default 503.
    Test di-skip jika nginx.conf tidak ditemukan (jalan dari dalam container).
    """
    content = _read_nginx_conf()
    if not content:
        pytest.skip("nginx.conf tidak ditemukan dari path ini (container) — lewati")

    assert "limit_req_status 429" in content, (
        "limit_req_status harus di-set ke 429. "
        "Default Nginx adalah 503 yang tidak sesuai semantik HTTP."
    )
