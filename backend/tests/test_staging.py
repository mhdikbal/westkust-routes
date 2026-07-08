"""
Unit tests for /api/staging/extractions endpoints.
Uses FastAPI dependency override with mock DB session, mirroring test_forts.py conventions.
"""
import hashlib
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db

VALID_KEY = "test-key-daghregister-colab"
VALID_KEY_HASH = hashlib.sha256(VALID_KEY.encode()).hexdigest()

MOCK_API_KEY = SimpleNamespace(id=1, key_hash=VALID_KEY_HASH, label="daghregister_colab", active="true")


def make_scalars_result(items):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    mock.scalar_one_or_none.return_value = items[0] if items else None
    return mock


def make_extraction(id, source="daghregister_batavia", external_ref="volume:1664|page:57",
                     confidence_flag="unverified", text_indonesia="teks contoh"):
    return SimpleNamespace(
        id=id, source=source, external_ref=external_ref, batch_id="batch-1",
        text_indonesia=text_indonesia, text_asli="dutch text", metadata_json={"tanggal_perkiraan": "17 FEBRUARY"},
        confidence_flag=confidence_flag, reviewed_by=None, reviewed_at=None, created_at="2026-07-06T00:00:00+00:00",
    )


def override_db(session):
    async def _get_db():
        yield session
    app.dependency_overrides[get_db] = _get_db


@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()


# ─── API key auth ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_post_extractions_without_api_key_returns_401():
    session = AsyncMock()
    override_db(session)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/staging/extractions", json={
            "source": "daghregister_batavia", "items": []
        })

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_post_extractions_with_wrong_api_key_returns_401():
    session = AsyncMock()
    session.execute.side_effect = [make_scalars_result([])]  # API key lookup: no match
    override_db(session)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/staging/extractions",
            json={"source": "daghregister_batavia", "items": []},
            headers={"X-API-Key": "salah-key"},
        )

    assert response.status_code == 401


# ─── POST batch insert + idempotency ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_post_extractions_inserts_new_items():
    session = AsyncMock()
    session.execute.side_effect = [
        make_scalars_result([MOCK_API_KEY]),  # API key lookup: valid
        make_scalars_result([]),               # existing external_ref lookup: none exist
    ]
    override_db(session)

    payload = {
        "source": "daghregister_batavia",
        "batch_id": "batch-uuid-1",
        "items": [
            {"external_ref": "volume:1664|page:57", "text_indonesia": "teks A", "text_asli": "dutch A",
             "metadata": {"tanggal_perkiraan": "17 FEBRUARY"}},
            {"external_ref": "volume:1664|page:65", "text_indonesia": "teks B"},
        ],
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/staging/extractions", json=payload, headers={"X-API-Key": VALID_KEY}
        )

    assert response.status_code == 201
    data = response.json()
    assert data["inserted"] == 2
    assert data["skipped_duplicate"] == 0
    assert session.add_all.called or session.add.call_count == 2
    session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_post_extractions_created_at_fits_column_length():
    """created_at harus <=30 char -- StagingExtraction.created_at adalah
    String(30). isoformat() dgn microseconds (32 char) overflow di Postgres
    real (StringDataRightTruncationError) meski lolos test lain yg mock DB."""
    session = AsyncMock()
    session.execute.side_effect = [
        make_scalars_result([MOCK_API_KEY]),
        make_scalars_result([]),
    ]
    override_db(session)

    payload = {
        "source": "daghregister_batavia",
        "batch_id": "batch-uuid-len",
        "items": [{"external_ref": "volume:1664|page:99", "text_indonesia": "teks"}],
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/staging/extractions", json=payload, headers={"X-API-Key": VALID_KEY}
        )

    assert response.status_code == 201
    inserted_obj = session.add.call_args_list[0].args[0]
    assert len(inserted_obj.created_at) <= 30, (
        f"created_at panjangnya {len(inserted_obj.created_at)} char, "
        f"melebihi kolom String(30): {inserted_obj.created_at!r}"
    )


@pytest.mark.asyncio
async def test_post_extractions_retry_skips_existing_duplicates():
    """Re-sending the same batch (retry after disconnect) must not duplicate rows."""
    session = AsyncMock()
    session.execute.side_effect = [
        make_scalars_result([MOCK_API_KEY]),
        make_scalars_result(["volume:1664|page:57", "volume:1664|page:65"]),  # both already exist
    ]
    override_db(session)

    payload = {
        "source": "daghregister_batavia",
        "items": [
            {"external_ref": "volume:1664|page:57", "text_indonesia": "teks A"},
            {"external_ref": "volume:1664|page:65", "text_indonesia": "teks B"},
        ],
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/staging/extractions", json=payload, headers={"X-API-Key": VALID_KEY}
        )

    assert response.status_code == 201
    data = response.json()
    assert data["inserted"] == 0
    assert data["skipped_duplicate"] == 2


@pytest.mark.asyncio
async def test_post_extractions_partial_duplicate():
    session = AsyncMock()
    session.execute.side_effect = [
        make_scalars_result([MOCK_API_KEY]),
        make_scalars_result(["volume:1664|page:57"]),  # only first item already exists
    ]
    override_db(session)

    payload = {
        "source": "daghregister_batavia",
        "items": [
            {"external_ref": "volume:1664|page:57", "text_indonesia": "teks A"},
            {"external_ref": "volume:1664|page:65", "text_indonesia": "teks B"},
        ],
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/staging/extractions", json=payload, headers={"X-API-Key": VALID_KEY}
        )

    data = response.json()
    assert data["inserted"] == 1
    assert data["skipped_duplicate"] == 1


# ─── GET listing + pagination ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_extractions_filters_by_source_and_confidence_flag():
    session = AsyncMock()
    matching = make_extraction(1, source="daghregister_batavia", confidence_flag="unverified")
    session.execute.side_effect = [
        make_scalars_result([MOCK_API_KEY]),
        make_scalars_result([matching]),
    ]
    override_db(session)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/api/staging/extractions?source=daghregister_batavia&confidence_flag=unverified",
            headers={"X-API-Key": VALID_KEY},
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["source"] == "daghregister_batavia"
    assert data[0]["confidence_flag"] == "unverified"


@pytest.mark.asyncio
async def test_get_extractions_default_pagination_is_50():
    session = AsyncMock()
    session.execute.side_effect = [
        make_scalars_result([MOCK_API_KEY]),
        make_scalars_result([]),
    ]
    override_db(session)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/staging/extractions", headers={"X-API-Key": VALID_KEY})

    assert response.status_code == 200
    # Cek statement yang benar-benar dikirim ke DB memuat LIMIT 50 (default), bukan tanpa batas
    endpoint_call = session.execute.call_args_list[-1]
    stmt = endpoint_call[0][0]
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    assert "LIMIT 50" in compiled


@pytest.mark.asyncio
async def test_get_extractions_limit_over_200_rejected():
    session = AsyncMock()
    session.execute.side_effect = [make_scalars_result([MOCK_API_KEY])]
    override_db(session)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/api/staging/extractions?limit=500", headers={"X-API-Key": VALID_KEY}
        )

    assert response.status_code == 422


# ─── PATCH confidence_flag ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_patch_confidence_flag_valid_value():
    session = AsyncMock()
    extraction = make_extraction(1, confidence_flag="unverified")
    session.execute.side_effect = [
        make_scalars_result([MOCK_API_KEY]),
        make_scalars_result([extraction]),
    ]
    override_db(session)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            "/api/staging/extractions/1",
            json={"confidence_flag": "reviewed", "reviewed_by": "muhammad.ikbal"},
            headers={"X-API-Key": VALID_KEY},
        )

    assert response.status_code == 200
    assert extraction.confidence_flag == "reviewed"
    assert extraction.reviewed_by == "muhammad.ikbal"
    session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_patch_confidence_flag_invalid_value_returns_422():
    session = AsyncMock()
    session.execute.side_effect = [make_scalars_result([MOCK_API_KEY])]
    override_db(session)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            "/api/staging/extractions/1",
            json={"confidence_flag": "not-a-real-status"},
            headers={"X-API-Key": VALID_KEY},
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_patch_confidence_flag_not_found_returns_404():
    session = AsyncMock()
    session.execute.side_effect = [
        make_scalars_result([MOCK_API_KEY]),
        make_scalars_result([]),  # extraction id not found
    ]
    override_db(session)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            "/api/staging/extractions/999",
            json={"confidence_flag": "reviewed"},
            headers={"X-API-Key": VALID_KEY},
        )

    assert response.status_code == 404
