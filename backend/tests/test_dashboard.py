"""
Unit tests untuk GET /api/research/pemodelan-dashboard.

TDD: ditulis SEBELUM endpoint ditambahkan ke routers/research.py. Endpoint ini
TIDAK butuh DB session -- murni baca data/export/*.csv+json via
build_bokeh_dashboard.build_dashboard() lalu cache-aside Redis (pola sama
sankey-tema/power-status). conftest.py autouse _cache_off fixture bikin
cache_get selalu None di test, jadi tiap test exercise compute path (build_dashboard
DI-MOCK di sini, bukan bokeh sungguhan -- itu domain test build_bokeh_dashboard
sendiri, bukan endpoint ini).
"""
import sys
import os
from unittest.mock import patch

import pytest
from httpx import AsyncClient, ASGITransport

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


FAKE_DASHBOARD = {
    "markov": {"script": "<script>markov</script>", "div": "<div>markov</div>"},
    "dynamics": {"script": "<script>dynamics</script>", "div": "<div>dynamics</div>"},
    "game_theory": {"script": "<script>gt</script>", "div": "<div>gt</div>"},
}


@pytest.mark.asyncio
async def test_pemodelan_dashboard_happy_path():
    with patch("routers.research.build_dashboard", return_value=FAKE_DASHBOARD):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.get("/api/research/pemodelan-dashboard")
    assert res.status_code == 200
    body = res.json()
    assert set(body.keys()) == {"markov", "dynamics", "game_theory"}
    for key in ("markov", "dynamics", "game_theory"):
        assert body[key]["script"]
        assert body[key]["div"]


@pytest.mark.asyncio
async def test_pemodelan_dashboard_graceful_when_source_missing():
    """Kalau salah satu sumber data/export/* belum ada (mis. blm pernah
    dijalankan Model 5), key-nya None -- BUKAN 500 traceback (security
    checklist CLAUDE.md: jangan expose stack trace ke client)."""
    partial = {**FAKE_DASHBOARD, "dynamics": None}
    with patch("routers.research.build_dashboard", return_value=partial):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.get("/api/research/pemodelan-dashboard")
    assert res.status_code == 200
    assert res.json()["dynamics"] is None


@pytest.mark.asyncio
async def test_pemodelan_dashboard_no_stack_trace_on_build_error():
    """build_dashboard() melempar exception (mis. file CSV korup) -> 503
    dgn pesan jujur, bukan 500 raw traceback."""
    with patch("routers.research.build_dashboard", side_effect=RuntimeError("boom")):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.get("/api/research/pemodelan-dashboard")
    assert res.status_code == 503
    assert "boom" not in res.text
