import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Voyage, Fort
from routers.voyages import list_voyages

@pytest.mark.asyncio
async def test_voyage_direction_logic(db_session: AsyncSession):
    # Setup test forts
    padang = Fort(name="Padang", latitude=-0.9, longitude=100.3, port_type="both")
    batavia = Fort(name="Batavia", latitude=-6.1, longitude=106.8, port_type="arrival")
    db_session.add_all([padang, batavia])
    await db_session.commit()
    
    # Test Outbound: Padang -> Batavia
    v1 = Voyage(
        ship_name="Test Ship Out",
        origin_id=padang.id,
        destination_id=batavia.id,
        origin_name_raw="Padang",
        destination_name_raw="Batavia",
        direction="outbound"
    )
    
    # Test Inbound: Batavia -> Padang
    v2 = Voyage(
        ship_name="Test Ship In",
        origin_id=batavia.id,
        destination_id=padang.id,
        origin_name_raw="Batavia",
        destination_name_raw="Padang",
        direction="inbound"
    )
    
    db_session.add_all([v1, v2])
    await db_session.commit()
    
    # Verify via API logic
    outbound = await list_voyages(direction="outbound", db=db_session)
    assert len(outbound) == 1
    assert outbound[0].ship_name == "Test Ship Out"
    
    inbound = await list_voyages(direction="inbound", db=db_session)
    assert len(inbound) == 1
    assert inbound[0].ship_name == "Test Ship In"

@pytest.mark.asyncio
async def test_voyage_year_filtering(db_session: AsyncSession):
    v1 = Voyage(ship_name="Old Ship", year=1720)
    v2 = Voyage(ship_name="New Ship", year=1780)
    db_session.add_all([v1, v2])
    await db_session.commit()
    
    results = await list_voyages(year_from=1750, db=db_session)
    assert len(results) == 1
    assert results[0].ship_name == "New Ship"
