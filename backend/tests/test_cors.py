"""
CORS tests — US-08 Sprint SEC-CONTENT

Verifikasi bahwa CORSMiddleware dikonfigurasi dengan benar:
- Origin yang terdaftar di ALLOWED_ORIGINS mendapat header CORS
- Origin tidak dikenal tidak mendapat header CORS
- Wildcard (*) tidak pernah muncul di Access-Control-Allow-Origin
- Preflight OPTIONS request ditangani dengan benar
- allow_credentials tidak boleh True

Test case name contract (wajib ada, digunakan oleh QA workflow):
  test_cors_allows_nginx_origin
  test_cors_blocks_unknown_origin
  test_cors_preflight_options
  test_cors_wildcard_not_present
"""
import os
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

NGINX_ORIGIN = "http://localhost:8084"
DJANGO_ORIGIN = "http://localhost:8001"
EVIL_ORIGIN  = "http://evil.example.com"


# ─── DB mock helper ──────────────────────────────────────────────────────────

def _empty_db_override():
    """
    Minimal async DB mock that returns an empty forts list.
    CORS middleware runs before the route handler, so response body does not
    affect CORS header assertions. We mock DB to avoid an external dependency
    and keep CORS tests fully unit-level.
    """
    async def mock_get_db():
        session = AsyncMock()
        result_mock = MagicMock()
        result_mock.scalars.return_value.all.return_value = []
        session.execute.return_value = result_mock
        yield session
    return mock_get_db


# ─── Required test cases (exact names mandated by QA workflow) ───────────────

@pytest.mark.asyncio
async def test_cors_allows_nginx_origin():
    """
    GET /api/forts/ dengan Origin: http://localhost:8084 (Nginx reverse proxy)
    harus mendapat Access-Control-Allow-Origin: http://localhost:8084 di response.
    """
    from database import get_db
    app.dependency_overrides[get_db] = _empty_db_override()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/forts/", headers={"Origin": NGINX_ORIGIN})

    app.dependency_overrides.clear()

    assert r.status_code == 200
    acao = r.headers.get("access-control-allow-origin", "")
    assert acao == NGINX_ORIGIN, (
        f"Access-Control-Allow-Origin harus '{NGINX_ORIGIN}', dapat '{acao}'"
    )


@pytest.mark.asyncio
async def test_cors_blocks_unknown_origin():
    """
    GET /api/forts/ dengan Origin: http://evil.example.com TIDAK boleh
    mendapat Access-Control-Allow-Origin yang merefleksikan origin tersebut.
    Header harus absen atau bukan milik evil origin.
    """
    from database import get_db
    app.dependency_overrides[get_db] = _empty_db_override()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/forts/", headers={"Origin": EVIL_ORIGIN})

    app.dependency_overrides.clear()

    acao = r.headers.get("access-control-allow-origin", "")
    assert acao != EVIL_ORIGIN, (
        f"CORS tidak boleh mengizinkan '{EVIL_ORIGIN}' — origin direfleksikan kembali!"
    )
    assert acao != "*", "Wildcard tidak boleh dikembalikan untuk origin yang tidak dikenal"


@pytest.mark.asyncio
async def test_cors_preflight_options():
    """
    OPTIONS /api/forts/ dengan Origin: http://localhost:8084 dan
    Access-Control-Request-Method: GET harus mendapat respons preflight
    yang sukses (200 atau 204) dengan header CORS yang tepat.
    CORS middleware menangani preflight tanpa menyentuh route handler,
    sehingga tidak perlu DB mock.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.options(
            "/api/forts/",
            headers={
                "Origin": NGINX_ORIGIN,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "content-type",
            },
        )

    assert r.status_code in (200, 204), (
        f"Preflight OPTIONS harus return 200 atau 204, dapat {r.status_code}"
    )
    acao = r.headers.get("access-control-allow-origin", "")
    assert acao == NGINX_ORIGIN, (
        f"Preflight harus mengembalikan origin '{NGINX_ORIGIN}', dapat '{acao}'"
    )
    acam = r.headers.get("access-control-allow-methods", "")
    assert "GET" in acam.upper(), (
        f"Access-Control-Allow-Methods harus mengandung GET, dapat '{acam}'"
    )


@pytest.mark.asyncio
async def test_cors_wildcard_not_present():
    """
    Access-Control-Allow-Origin: * TIDAK boleh pernah muncul di response.
    Konfigurasi lama allow_origins=['*'] + allow_credentials=True menyebabkan
    Starlette merefleksikan setiap Origin verbatim — pelanggaran kritis W3C CORS spec.
    Test ini memastikan wildcard sudah dihilangkan untuk semua origin.
    """
    from database import get_db
    app.dependency_overrides[get_db] = _empty_db_override()

    origins_to_check = [NGINX_ORIGIN, DJANGO_ORIGIN, EVIL_ORIGIN]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for origin in origins_to_check:
            r = await ac.get("/api/forts/", headers={"Origin": origin})
            acao = r.headers.get("access-control-allow-origin", "")
            assert acao != "*", (
                f"Access-Control-Allow-Origin tidak boleh '*' untuk origin '{origin}'. "
                "Wildcard CORS adalah security misconfiguration (US-08)."
            )

    app.dependency_overrides.clear()


# ─── Additional coverage ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_cors_credentials_not_allowed():
    """
    allow_credentials harus False — header Access-Control-Allow-Credentials
    tidak boleh bernilai 'true'. Kombinasi credentials=True + wildcard origin
    adalah pelanggaran kritis W3C CORS spec (konfigurasi lama US-08).
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/health", headers={"Origin": NGINX_ORIGIN})
    acac = r.headers.get("access-control-allow-credentials", "false").lower()
    assert acac != "true", "allow_credentials harus False — tidak ada fetch() yang menggunakan credentials:include"


@pytest.mark.asyncio
async def test_cors_no_origin_header_still_works():
    """
    Request tanpa Origin header (same-origin, curl, server-to-server) harus tetap
    return 200 — CORS middleware tidak boleh memblokir non-CORS request.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/health")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_cors_allows_nginx_origin_via_health():
    """
    Konfirmasi tambahan: /api/health (tanpa DB) juga mendapat header CORS
    untuk nginx origin. Memastikan middleware berlaku global, bukan hanya pada
    endpoint tertentu.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/health", headers={"Origin": NGINX_ORIGIN})
    assert r.status_code == 200
    acao = r.headers.get("access-control-allow-origin", "")
    assert acao == NGINX_ORIGIN
