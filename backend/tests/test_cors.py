"""
CORS tests — US-08 Sprint SEC-CONTENT

Verifikasi bahwa CORSMiddleware dikonfigurasi dengan benar:
- Origin yang terdaftar di ALLOWED_ORIGINS mendapat header CORS
- Origin tidak dikenal tidak mendapat header CORS
- Wildcard (*) tidak pernah muncul di Access-Control-Allow-Origin
- Preflight OPTIONS request ditangani dengan benar
"""
import os
import pytest
from httpx import AsyncClient, ASGITransport

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

NGINX_ORIGIN = "http://localhost:8084"
EVIL_ORIGIN  = "http://evil.example.com"


@pytest.mark.asyncio
async def test_cors_allows_nginx_origin():
    """Origin nginx (localhost:8084) harus mendapat Access-Control-Allow-Origin."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/health", headers={"Origin": NGINX_ORIGIN})
    assert r.status_code == 200
    acao = r.headers.get("access-control-allow-origin", "")
    assert acao == NGINX_ORIGIN, f"Expected '{NGINX_ORIGIN}', got '{acao}'"


@pytest.mark.asyncio
async def test_cors_blocks_unknown_origin():
    """Origin tidak dikenal TIDAK boleh mendapat Access-Control-Allow-Origin."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/health", headers={"Origin": EVIL_ORIGIN})
    acao = r.headers.get("access-control-allow-origin", "")
    assert acao != EVIL_ORIGIN, f"Evil origin should not be allowed, got '{acao}'"
    assert acao != "*", "Wildcard should never be returned"


@pytest.mark.asyncio
async def test_cors_wildcard_never_returned():
    """Access-Control-Allow-Origin: * TIDAK boleh pernah muncul."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r1 = await ac.get("/api/health", headers={"Origin": NGINX_ORIGIN})
        r2 = await ac.get("/api/health", headers={"Origin": EVIL_ORIGIN})
    assert r1.headers.get("access-control-allow-origin") != "*"
    assert r2.headers.get("access-control-allow-origin") != "*"


@pytest.mark.asyncio
async def test_cors_preflight_nginx_origin():
    """Preflight OPTIONS dari nginx origin harus return 200 dengan header CORS."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.options(
            "/api/forts/",
            headers={
                "Origin": NGINX_ORIGIN,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "content-type",
            },
        )
    assert r.status_code in (200, 204)
    acao = r.headers.get("access-control-allow-origin", "")
    assert acao == NGINX_ORIGIN


@pytest.mark.asyncio
async def test_cors_credentials_not_allowed():
    """allow_credentials harus False — header Access-Control-Allow-Credentials tidak ada atau 'false'."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/health", headers={"Origin": NGINX_ORIGIN})
    acac = r.headers.get("access-control-allow-credentials", "false").lower()
    assert acac != "true", "allow_credentials must not be true"


@pytest.mark.asyncio
async def test_cors_no_origin_header_still_works():
    """Request tanpa Origin header (same-origin, curl) harus tetap return 200."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/health")
    assert r.status_code == 200
