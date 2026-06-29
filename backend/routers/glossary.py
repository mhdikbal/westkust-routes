from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import CommodityGlossary

router = APIRouter()


@router.get("")
async def list_glossary(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Semua entri glossary, opsional filter per kategori."""
    q = select(CommodityGlossary).order_by(CommodityGlossary.term)
    if category:
        q = q.where(CommodityGlossary.category == category)
    result = await db.execute(q)
    items = result.scalars().all()
    return [_serialize(item) for item in items]


@router.get("/lookup")
async def lookup_terms(
    terms: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Batch lookup definisi untuk satu atau lebih istilah.
    Query param: ?terms=peper,kamfer,goud
    Return: {term: {definition_id, definition_nl, category}}
    """
    raw = [t.strip().lower() for t in terms.split(",") if t.strip()]
    if not raw:
        return {}

    # Match by exact term OR dalam array variants
    q = select(CommodityGlossary).where(
        or_(
            func.lower(CommodityGlossary.term).in_(raw),
            CommodityGlossary.variants.overlap(raw),
        )
    )
    result = await db.execute(q)
    items = result.scalars().all()

    # Build lookup map: setiap queried term → definisi
    lookup: dict[str, dict] = {}
    for item in items:
        data = {
            "term":          item.term,
            "term_display":  item.term_display or item.term,
            "definition_id": item.definition_id,
            "definition_nl": item.definition_nl,
            "category":      item.category,
        }
        # Daftarkan untuk term utama dan semua variannya
        lookup[item.term] = data
        for v in (item.variants or []):
            lookup[v.lower()] = data

    # Return hanya terms yang di-query
    return {t: lookup[t] for t in raw if t in lookup}


def _serialize(item: CommodityGlossary) -> dict:
    return {
        "term":          item.term,
        "term_display":  item.term_display or item.term,
        "variants":      item.variants or [],
        "definition_nl": item.definition_nl,
        "definition_id": item.definition_id,
        "category":      item.category,
    }
