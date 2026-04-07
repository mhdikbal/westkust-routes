from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel, ConfigDict

from database import get_db
from models import Voyage

router = APIRouter()


# ---------- Schemas ----------

class VoyageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    origin_id: Optional[int]
    destination_id: Optional[int]
    origin_name_raw: Optional[str]
    destination_name_raw: Optional[str]
    ship_name: str
    captain: Optional[str]
    year: Optional[int]
    total_gulden: Optional[float]
    main_product: Optional[str]
    all_products: Optional[str]
    duration_days: Optional[int]
    direction: Optional[str]
    source_url: Optional[str]



# ---------- Endpoints ----------

@router.get("/", response_model=List[VoyageSchema])
async def list_voyages(
    origin_id: Optional[int] = None,
    destination_id: Optional[int] = None,
    direction: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    product: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """List all voyages with optional filters."""
    query = select(Voyage)
    if origin_id is not None:
        query = query.where(Voyage.origin_id == origin_id)
    if destination_id is not None:
        query = query.where(Voyage.destination_id == destination_id)
    if direction:
        query = query.where(Voyage.direction == direction)
    if year_from:
        query = query.where(Voyage.year >= year_from)
    if year_to:
        query = query.where(Voyage.year <= year_to)
    if product:
        query = query.where(Voyage.all_products.ilike(f"%{product}%"))

    # Default sort by year descending
    query = query.order_by(desc(Voyage.year)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{voyage_id}", response_model=VoyageSchema)
async def get_voyage(voyage_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single voyage by ID."""
    result = await db.execute(select(Voyage).where(Voyage.id == voyage_id))
    voyage = result.scalar_one_or_none()
    if not voyage:
        raise HTTPException(status_code=404, detail=f"Voyage with id={voyage_id} not found")
    return voyage
