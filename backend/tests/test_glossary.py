"""
Unit tests for /api/glossary endpoints.
Fokus: source_citation field (technical debt dari docs/prd-port-tally-aggregate.md
-- commodity_glossary sebelumnya tidak punya cara melacak asal definisi).
Pola mock sama dgn test_voyages.py/test_forts.py.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


def make_glossary_item(**kwargs):
    defaults = {
        "term": "pikol",
        "term_display": "Pikol",
        "variants": ["pikul", "picol"],
        "definition_nl": "Draaglast; meest bepaald op 125 pond.",
        "definition_id": "Satuan berat pikul, sekitar 125 pon Amsterdam.",
        "category": "satuan",
        "source_citation": "VOC-Glossarium (Instituut voor Nederlandse Geschiedenis, 2000)",
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


ITEM_WITH_CITATION = make_glossary_item()
ITEM_NO_CITATION = make_glossary_item(term="peper", term_display="Peper", variants=["lada"], source_citation=None)


def make_scalar_result(items):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    return mock


@pytest.mark.asyncio
async def test_list_glossary_includes_source_citation():
    """GET /api/glossary harus menyertakan field source_citation."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([ITEM_WITH_CITATION])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/glossary")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data[0]["source_citation"] == "VOC-Glossarium (Instituut voor Nederlandse Geschiedenis, 2000)"


@pytest.mark.asyncio
async def test_list_glossary_source_citation_null_not_omitted():
    """Entri lama tanpa citation (asal tak tercatat) harus tampil null, BUKAN ditebak atau field hilang."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([ITEM_NO_CITATION])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/glossary")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "source_citation" in data[0]
    assert data[0]["source_citation"] is None


@pytest.mark.asyncio
async def test_lookup_terms_includes_source_citation():
    """GET /api/glossary/lookup harus menyertakan source_citation per term."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([ITEM_WITH_CITATION])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/glossary/lookup?terms=pikol")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["pikol"]["source_citation"] == "VOC-Glossarium (Instituut voor Nederlandse Geschiedenis, 2000)"
