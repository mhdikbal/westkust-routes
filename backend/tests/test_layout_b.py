"""
Layout B — Test Suite
Sprint 1 — Uji Kelayakan | Tim Jangkar QA

Covers the new endpoints and UI features introduced in Layout B:
  - /api/voyages/routes?year_from=X&year_to=Y  (navbar year-range filter → antPath redraw)
  - /api/voyages/?search=X                      (ship search in navbar dropdown)
  - /api/voyages/stats                          (global badge in navbar)
  - /api/voyages/{id}/cargo                     (voyage modal cargo detail)
  - /api/forts/  — outbound_count + inbound_count for welcome port grid

Happy path + edge case + 404 per endpoint, following CLAUDE.md TDD requirements.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


# ─── Shared fixtures ─────────────────────────────────────────────────────────

def make_voyage(**kwargs):
    defaults = dict(
        id=1, voyage_ref=13447,
        origin_id=1, destination_id=6,
        origin_name_raw="Padang", destination_name_raw="Batavia",
        ship_name="Theeboom", captain="Jan de Vries",
        tonnage=None, year=1700,
        departure_date=None, arrival_date="1700-12-08",
        total_gulden=98358.05, main_product="goud",
        all_products="goud | peper | kamfer",
        cargo_count=26, duration_days=44,
        direction="outbound",
        source_url="https://resources.huygens.knaw.nl/bgb/voyage/13447",
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def make_cargo_item(**kwargs):
    defaults = dict(
        id=1, voyage_id=1,
        produk="goud", spesifikasi=None,
        qty_asli="26 mark", unit="mark",
        nilai_numerik=26.0, gram=None,
        gulden_nl=None, gulden_india=80000.0, catatan=None,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def make_scalar_result(items):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    mock.scalar_one_or_none.return_value = items[0] if items else None
    mock.scalar_one.return_value = items[0] if items else None
    return mock


# Route row helper for /api/voyages/routes
def make_route_row(origin_name, destination_name, direction, count, total_value,
                   origin_lat=-0.96, origin_lon=100.35, dest_lat=-6.12, dest_lon=106.82):
    return SimpleNamespace(
        origin_name=origin_name,
        destination_name=destination_name,
        origin_lat=origin_lat,
        origin_lon=origin_lon,
        dest_lat=dest_lat,
        dest_lon=dest_lon,
        direction=direction,
        count=count,
        total_value=total_value,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  1. /api/voyages/routes — year-range filter (Navbar Year Filter → antPath)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_routes_returns_list():
    """GET /api/voyages/routes without filters returns a list of route aggregations."""
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = [
            make_route_row("Padang", "Batavia", "outbound", 45, 1_500_000.0),
            make_route_row("Barus",  "Batavia", "outbound", 12,   400_000.0,
                           origin_lat=2.01, origin_lon=98.40),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_routes_year_from_filter():
    """GET /api/voyages/routes?year_from=1750 passes year_from to query."""
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        # Simulate DB returning only routes within year range
        result.all.return_value = [
            make_route_row("Padang", "Batavia", "outbound", 8, 200_000.0),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?year_from=1750")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["origin_name"] == "Padang"


@pytest.mark.asyncio
async def test_routes_year_to_filter():
    """GET /api/voyages/routes?year_to=1720 passes year_to to query."""
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = [
            make_route_row("Air Bangis", "Batavia", "outbound", 5, 90_000.0,
                           origin_lat=0.20, origin_lon=99.38),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?year_to=1720")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_routes_year_range_combined():
    """GET /api/voyages/routes?year_from=1700&year_to=1750 returns aggregated routes."""
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = [
            make_route_row("Padang",      "Batavia", "outbound", 30, 900_000.0),
            make_route_row("Pulau Cingkuak", "Batavia", "outbound", 10, 300_000.0,
                           origin_lat=-1.35, origin_lon=100.56),
            make_route_row("Batavia",     "Padang",   "inbound",  4,  80_000.0,
                           origin_lat=-6.12, origin_lon=106.82,
                           dest_lat=-0.96, dest_lon=100.35),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?year_from=1700&year_to=1750")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 3
    # Each item must have required fields for front-end antPath rendering
    required_fields = {"origin_name", "destination_name", "count", "total_value"}
    for row in data:
        assert required_fields.issubset(set(row.keys()))


@pytest.mark.asyncio
async def test_routes_returns_count_and_total_value():
    """Route aggregations must expose 'count' and 'total_value' for antPath weight."""
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = [
            make_route_row("Padang", "Batavia", "outbound", 99, 5_000_000.0),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?year_from=1700&year_to=1789")

    app.dependency_overrides.clear()

    data = r.json()
    assert data[0]["count"] == 99
    assert data[0]["total_value"] == pytest.approx(5_000_000.0, rel=1e-3)


@pytest.mark.asyncio
async def test_routes_empty_when_no_voyages_in_range():
    """GET /api/voyages/routes?year_from=1800&year_to=1850 returns empty list (no data)."""
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = []
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?year_from=1800&year_to=1850")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_routes_invalid_year_type_rejected():
    """GET /api/voyages/routes?year_from=notanumber returns 422 Unprocessable Entity."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?year_from=notanumber")

    assert r.status_code == 422


# ═══════════════════════════════════════════════════════════════════════════════
#  2. /api/voyages/?search=X — Ship Search (Navbar Search Dropdown)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_search_returns_matching_ships():
    """GET /api/voyages/?search=Theeboom returns voyages where ship_name contains 'Theeboom'."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([
            make_voyage(id=1, ship_name="Theeboom", year=1700),
        ])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/?search=Theeboom")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["ship_name"] == "Theeboom"


@pytest.mark.asyncio
async def test_search_case_insensitive_returns_results():
    """GET /api/voyages/?search=theeboom (lowercase) should still match — ilike in router."""
    async def mock_get_db():
        session = AsyncMock()
        # ilike in SQL means DB does the case-insensitive match; mock returns result
        session.execute.return_value = make_scalar_result([
            make_voyage(id=1, ship_name="Theeboom"),
        ])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/?search=theeboom")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.asyncio
async def test_search_no_match_returns_empty_list():
    """GET /api/voyages/?search=VesselThatDoesNotExist returns empty list, not 404."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/?search=VesselThatDoesNotExist")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_search_with_limit_respected():
    """GET /api/voyages/?search=Wind&limit=20 returns at most 20 results."""
    items = [make_voyage(id=i, ship_name=f"Wind_{i}", year=1700 + i) for i in range(20)]

    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result(items)
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/?search=Wind&limit=20")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    assert len(r.json()) == 20


@pytest.mark.asyncio
async def test_search_result_has_required_dropdown_fields():
    """Search result items must expose ship_name, year, origin_name_raw, destination_name_raw for dropdown UI."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([
            make_voyage(id=5, ship_name="Nieuw Amsterdam",
                        origin_name_raw="Barus", destination_name_raw="Batavia", year=1712),
        ])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/?search=Nieuw")

    app.dependency_overrides.clear()

    data = r.json()
    assert len(data) == 1
    v = data[0]
    assert v["ship_name"] == "Nieuw Amsterdam"
    assert v["origin_name_raw"] == "Barus"
    assert v["destination_name_raw"] == "Batavia"
    assert v["year"] == 1712


@pytest.mark.asyncio
async def test_search_with_special_characters_does_not_error():
    """GET /api/voyages/?search=O%27Brien (URL-encoded apostrophe) must not raise 500."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/?search=O%27Brien")

    app.dependency_overrides.clear()

    # Should not be a server error
    assert r.status_code in (200, 422)
    if r.status_code == 200:
        assert isinstance(r.json(), list)


# ═══════════════════════════════════════════════════════════════════════════════
#  3. /api/voyages/stats — Global Stats Badge (Navbar)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_stats_returns_total_voyages():
    """GET /api/voyages/stats must include total_voyages for the navbar badge."""
    async def mock_get_db():
        session = AsyncMock()

        # Main totals query
        totals_result = MagicMock()
        totals_result.one.return_value = (4700, 250_000_000.0, 1700, 1789)

        # Direction counts
        dir_result = MagicMock()
        dir_result.all.return_value = [
            ("outbound", 3200), ("inbound", 1200), ("transit", 300),
        ]

        # Top products
        prod_result = MagicMock()
        prod_result.all.return_value = [
            ("goud", 800), ("peper", 600), ("kamfer", 400),
        ]

        # Ports
        port_result = MagicMock()
        port_result.all.return_value = [
            ("Padang", "both", 1500, 80_000_000.0),
            ("Batavia", "arrival", 900, 50_000_000.0),
        ]

        session.execute.side_effect = [
            totals_result, dir_result, prod_result, port_result,
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/stats")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert "total_voyages" in data
    assert data["total_voyages"] == 4700


@pytest.mark.asyncio
async def test_stats_response_schema_complete():
    """GET /api/voyages/stats response must have all required schema fields."""
    async def mock_get_db():
        session = AsyncMock()

        totals_result = MagicMock()
        totals_result.one.return_value = (100, 5_000_000.0, 1705, 1780)

        dir_result = MagicMock()
        dir_result.all.return_value = [("outbound", 70), ("inbound", 30)]

        prod_result = MagicMock()
        prod_result.all.return_value = [("peper", 40)]

        port_result = MagicMock()
        port_result.all.return_value = [("Padang", "both", 60, 3_000_000.0)]

        session.execute.side_effect = [
            totals_result, dir_result, prod_result, port_result,
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/stats")

    app.dependency_overrides.clear()

    data = r.json()
    required = {
        "total_voyages", "total_cargo_value",
        "outbound_count", "inbound_count", "transit_count",
        "year_min", "year_max", "top_products", "ports",
    }
    assert required.issubset(set(data.keys()))
    assert data["year_min"] == 1705
    assert data["year_max"] == 1780


# ═══════════════════════════════════════════════════════════════════════════════
#  4. /api/voyages/{id}/cargo — Voyage Modal Cargo Detail
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_cargo_returns_list_for_valid_voyage():
    """GET /api/voyages/1/cargo returns cargo items for voyage 1."""
    async def mock_get_db():
        session = AsyncMock()

        # First call: verify voyage exists
        voyage_check = MagicMock()
        voyage_check.scalar_one_or_none.return_value = 1  # id exists

        # Second call: cargo items
        cargo_result = make_scalar_result([
            make_cargo_item(id=1, produk="goud",  gulden_india=80_000.0),
            make_cargo_item(id=2, produk="peper", gulden_india=10_000.0),
        ])

        session.execute.side_effect = [voyage_check, cargo_result]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/1/cargo")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["produk"] == "goud"
    assert data[0]["gulden_india"] == pytest.approx(80_000.0)


@pytest.mark.asyncio
async def test_cargo_returns_empty_list_when_no_cargo():
    """GET /api/voyages/2/cargo returns [] when no cargo items exist for voyage."""
    async def mock_get_db():
        session = AsyncMock()

        voyage_check = MagicMock()
        voyage_check.scalar_one_or_none.return_value = 2

        cargo_result = make_scalar_result([])

        session.execute.side_effect = [voyage_check, cargo_result]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/2/cargo")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_cargo_404_for_nonexistent_voyage():
    """GET /api/voyages/9999/cargo returns 404 when voyage does not exist."""
    async def mock_get_db():
        session = AsyncMock()
        voyage_check = MagicMock()
        voyage_check.scalar_one_or_none.return_value = None
        session.execute.return_value = voyage_check
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/9999/cargo")

    app.dependency_overrides.clear()

    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_cargo_item_schema_fields():
    """Cargo items must expose produk, gulden_india, gulden_nl for modal display."""
    async def mock_get_db():
        session = AsyncMock()

        voyage_check = MagicMock()
        voyage_check.scalar_one_or_none.return_value = 1

        cargo_result = make_scalar_result([
            make_cargo_item(
                id=1, voyage_id=1,
                produk="kamfer",
                spesifikasi="kristal",
                qty_asli="10 bahar",
                unit="bahar",
                gulden_nl=5_000.0,
                gulden_india=None,
            ),
        ])

        session.execute.side_effect = [voyage_check, cargo_result]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/1/cargo")

    app.dependency_overrides.clear()

    data = r.json()
    item = data[0]
    required_keys = {"id", "voyage_id", "produk", "gulden_nl", "gulden_india"}
    assert required_keys.issubset(set(item.keys()))
    assert item["produk"] == "kamfer"
    assert item["gulden_nl"] == pytest.approx(5_000.0)
    assert item["gulden_india"] is None


# ═══════════════════════════════════════════════════════════════════════════════
#  5. /api/forts/ — Welcome Panel Port Grid (outbound_count + inbound_count)
# ═══════════════════════════════════════════════════════════════════════════════

def make_fort(id, name, latitude, longitude, color, description, port_type="departure",
              designasi_voc=None):
    return SimpleNamespace(
        id=id, name=name, latitude=latitude, longitude=longitude,
        color=color, description=description, port_type=port_type,
        designasi_voc=designasi_voc,
    )


NINE_FORTS = [
    make_fort(1,  "Padang",           -0.966,  100.354, "#c0392b", "Fort Padang",      "both"),
    make_fort(2,  "Pulau Cingkuak",   -1.353,  100.560, "#e67e22", "Fort Cingkuak",    "departure"),
    make_fort(3,  "Air Haji",         -1.934,  100.867, "#27ae60", "Fort Air Haji",    "departure"),
    make_fort(4,  "Air Bangis",        0.197,   99.376, "#2980b9", "Air Bangis",       "departure"),
    make_fort(5,  "Barus",             2.014,   98.399, "#16a085", "Barus",            "departure"),
    make_fort(6,  "Batavia",          -6.117,  106.817, "#2c3e50", "Fort Batavia",     "arrival"),
    make_fort(7,  "Jambi",            -1.098,  104.176, "#d35400", "Jambi",            "arrival"),
    make_fort(8,  "Lampung",          -5.358,  105.280, "#7f8c8d", "Lampung",          "arrival"),
    make_fort(9,  "Palembang",        -3.003,  104.780, "#8e44ad", "Palembang",        "arrival"),
]


@pytest.mark.asyncio
async def test_forts_list_returns_nine_ports_for_welcome_grid():
    """GET /api/forts/ returns 9 ports matching the welcome panel port grid."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.side_effect = [
            # Fort list
            MagicMock(**{"scalars.return_value.all.return_value": NINE_FORTS}),
            # Stats (outbound + inbound) for each of 9 forts = 18 calls
            *[MagicMock(one=MagicMock(return_value=(10, 500_000.0)))
              for _ in range(len(NINE_FORTS) * 2)],
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/forts/")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 9


@pytest.mark.asyncio
async def test_forts_list_exposes_outbound_inbound_counts():
    """Each fort in /api/forts/ must expose outbound_count and inbound_count for port grid cards."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.side_effect = [
            MagicMock(**{"scalars.return_value.all.return_value": [
                make_fort(1, "Padang", -0.966, 100.354, "#c0392b", "desc", "both"),
            ]}),
            MagicMock(one=MagicMock(return_value=(42, 1_200_000.0))),  # outbound stats
            MagicMock(one=MagicMock(return_value=(7,    150_000.0))),  # inbound stats
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/forts/")

    app.dependency_overrides.clear()

    data = r.json()
    assert len(data) == 1
    fort = data[0]
    assert "outbound_count" in fort
    assert "inbound_count"  in fort
    assert fort["outbound_count"] == 42
    assert fort["inbound_count"]  == 7


@pytest.mark.asyncio
async def test_forts_list_contains_all_nine_expected_ports():
    """Welcome panel expects: Padang, Pulau Cingkuak, Air Haji, Air Bangis, Barus,
    Batavia, Jambi, Lampung, Palembang — all must be present."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.side_effect = [
            MagicMock(**{"scalars.return_value.all.return_value": NINE_FORTS}),
            *[MagicMock(one=MagicMock(return_value=(0, 0.0)))
              for _ in range(len(NINE_FORTS) * 2)],
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/forts/")

    app.dependency_overrides.clear()

    names = {d["name"] for d in r.json()}
    expected = {
        "Padang", "Pulau Cingkuak", "Air Haji", "Air Bangis",
        "Barus", "Batavia", "Jambi", "Lampung", "Palembang",
    }
    assert expected == names


# ═══════════════════════════════════════════════════════════════════════════════
#  6. /api/forts/{id} — Fort Panel: outbound/inbound voyages + stats
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_fort_detail_has_inbound_voyages_field():
    """GET /api/forts/6 (Batavia) should expose inbound_voyages list for Fort Panel tab."""
    batavia = make_fort(6, "Batavia", -6.117, 106.817, "#2c3e50", "Batavia desc", "arrival")
    inbound_voyage = SimpleNamespace(
        id=10, fort_id=6, ship_name="Batavia Retour", captain="P. Verhoef",
        year=1710, total_gulden=22_000.0, main_product="peper",
        all_products="peper | bijenwas", destination="Padang", duration_days=40,
        source_url="https://resources.huygens.knaw.nl/bgb/voyage/20001",
        direction="inbound", departure_date=None, arrival_date=None, cargo_count=None,
        origin_id=1, destination_id=6,
        origin_name_raw="Padang", destination_name_raw="Batavia",
    )

    async def mock_get_db():
        session = AsyncMock()
        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = batavia

        outbound_result = MagicMock()
        outbound_result.scalars.return_value.all.return_value = []

        inbound_result = MagicMock()
        inbound_result.scalars.return_value.all.return_value = [inbound_voyage]

        out_stats = MagicMock()
        out_stats.one.return_value = (0, 0.0, None, None)

        in_stats = MagicMock()
        in_stats.one.return_value = (1, 22_000.0, 1710, 1710)

        session.execute.side_effect = [
            fort_result, outbound_result, inbound_result, out_stats, in_stats,
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/forts/6")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert "inbound_voyages" in data
    assert len(data["inbound_voyages"]) == 1
    assert data["inbound_voyages"][0]["ship_name"] == "Batavia Retour"


@pytest.mark.asyncio
async def test_fort_detail_stats_exposed_for_panel():
    """Fort panel stats grid needs outbound_count, inbound_count, total_value_out, total_value_in."""
    padang = make_fort(1, "Padang", -0.966, 100.354, "#c0392b", "desc", "both")

    async def mock_get_db():
        session = AsyncMock()
        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = padang

        out_voyages = MagicMock()
        out_voyages.scalars.return_value.all.return_value = []

        in_voyages = MagicMock()
        in_voyages.scalars.return_value.all.return_value = []

        out_stats = MagicMock()
        out_stats.one.return_value = (350, 12_000_000.0, 1700, 1789)

        in_stats = MagicMock()
        in_stats.one.return_value = (80, 3_000_000.0, 1710, 1785)

        session.execute.side_effect = [
            fort_result, out_voyages, in_voyages, out_stats, in_stats,
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/forts/1")

    app.dependency_overrides.clear()

    data = r.json()
    assert data["outbound_count"] == 350
    assert data["inbound_count"]  == 80
    assert data["total_value_out"] == pytest.approx(12_000_000.0, rel=1e-3)
    assert data["total_value_in"]  == pytest.approx(3_000_000.0,  rel=1e-3)
    assert data["year_min"] == 1700
    assert data["year_max"] == 1789
