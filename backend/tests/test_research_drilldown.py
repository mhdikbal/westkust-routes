"""
SNK-3 — Unit tests untuk GET /api/research/sankey-tema/rows (drill-down audit).
TDD: ditulis SEBELUM implementasi.

Klik link Sankey -> daftar baris penyusun (teks Indonesia + skor + tanggal +
pelabuhan + sumber corpus + low_confidence). Filter pelabuhan cocok KEANGGOTAAN
pada baris multi-port. Pola: dependency override + mock DB (test_voyages.py).
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db


def make_row(corpus_id, tema, pelabuhan, tahun=1660, **over):
    base = dict(
        corpus_id=corpus_id, corpus_asal="daghregister", source="daghregister_batavia",
        volume="Dagh_register_...-1664", inventaris_ref=None,
        tanggal_perkiraan="14 JANUARY", tahun=tahun, dekade=(tahun // 10 * 10) if tahun else None,
        pelabuhan_disebut=pelabuhan, tema_dominan=tema, skor_dominan=0.87,
        low_confidence=False,
        skor_pdr_drainase=0.1, skor_etr_retensi=0.1, skor_hak_adat=0.1,
        skor_pelayaran=0.1, skor_sengketa=0.1, skor_syahbandar=0.87,
        skor_tidak_relevan=0.02,
        text="Kapal tiba di pelabuhan membawa lada.", text_asli="quam een schip aen.",
    )
    base.update(over)
    return SimpleNamespace(**base)


def db_returning(rows):
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.scalars.return_value.all.return_value = rows
        session.execute.return_value = result
        yield session
    return mock_get_db


async def _get(url):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.get(url)


# ─── Happy path + field audit ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_drilldown_returns_rows_with_audit_fields():
    rows = [make_row(1, "syahbandar", "Padang")]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        resp = await _get("/api/research/sankey-tema/rows?tema=syahbandar&pelabuhan=Padang")
    finally:
        app.dependency_overrides.clear()

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) == 1
    r = data[0]
    for field in ("text", "text_asli", "skor_dominan", "tanggal_perkiraan",
                  "pelabuhan_disebut", "corpus_asal", "source", "tema_dominan",
                  "low_confidence"):
        assert field in r, f"field audit hilang: {field}"
    assert r["text"].startswith("Kapal tiba")
    assert r["skor_dominan"] == 0.87


# ─── Filter pelabuhan cocok keanggotaan di baris multi-port (FIX #2) ─────────

@pytest.mark.asyncio
async def test_drilldown_multiport_membership():
    """pelabuhan='Padang' harus MEMASUKKAN baris 'Barus; Padang', MENGECUALIKAN 'Tiku'."""
    rows = [
        make_row(1, "syahbandar", "Barus; Padang"),
        make_row(2, "syahbandar", "Tiku"),
        make_row(3, "syahbandar", "Padang; Pariaman"),
    ]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        data = (await _get("/api/research/sankey-tema/rows?pelabuhan=Padang")).json()
    finally:
        app.dependency_overrides.clear()

    ids = sorted(r["corpus_id"] for r in data)
    assert ids == [1, 3]  # baris 2 (Tiku) tidak ikut


@pytest.mark.asyncio
async def test_drilldown_no_partial_string_match():
    """Cocok token utuh, bukan substring: 'Painan' != 'Pariaman' dst."""
    rows = [make_row(1, "syahbandar", "Pariaman")]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        data = (await _get("/api/research/sankey-tema/rows?pelabuhan=Painan")).json()
    finally:
        app.dependency_overrides.clear()
    assert data == []


# ─── low_confidence terekspos (juga SNK-4) ───────────────────────────────────

@pytest.mark.asyncio
async def test_drilldown_exposes_low_confidence():
    rows = [
        make_row(1, "sengketa", "Salido", skor_dominan=0.41, low_confidence=True),
        make_row(2, "sengketa", "Salido", skor_dominan=0.90, low_confidence=False),
    ]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        data = (await _get("/api/research/sankey-tema/rows?tema=sengketa")).json()
    finally:
        app.dependency_overrides.clear()
    flags = {r["corpus_id"]: r["low_confidence"] for r in data}
    assert flags == {1: True, 2: False}


# ─── Edge: kosong & validasi limit negatif (SEC) ─────────────────────────────

@pytest.mark.asyncio
async def test_drilldown_empty_is_200():
    app.dependency_overrides[get_db] = db_returning([])
    try:
        resp = await _get("/api/research/sankey-tema/rows?tema=pelayaran")
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_drilldown_negative_limit_is_422():
    """limit negatif -> 422 (pelajaran SEC-2), bukan 500."""
    app.dependency_overrides[get_db] = db_returning([make_row(1, "syahbandar", "Padang")])
    try:
        resp = await _get("/api/research/sankey-tema/rows?limit=-5")
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 422
