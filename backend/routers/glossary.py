from typing import Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from cache import make_key, cache_get, cache_set
from database import get_db
from models import CommodityGlossary

router = APIRouter()


@router.get("")
async def list_glossary(
    response: Response,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Semua entri glossary, opsional filter per kategori. Cache-aside Redis."""
    cache_key = make_key("glossary", {"category": category})
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    q = select(CommodityGlossary).order_by(CommodityGlossary.term)
    if category:
        q = q.where(CommodityGlossary.category == category)
    result = await db.execute(q)
    items = result.scalars().all()
    payload = [_serialize(item) for item in items]
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


@router.get("/lookup")
async def lookup_terms(
    response: Response,
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

    cache_key = make_key("glossary-lookup", {"terms": ",".join(sorted(raw))})
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

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
            "term":            item.term,
            "term_display":    item.term_display or item.term,
            "definition_id":   item.definition_id,
            "definition_nl":   item.definition_nl,
            "category":        item.category,
            "source_citation": item.source_citation,
        }
        # Daftarkan untuk term utama dan semua variannya
        lookup[item.term] = data
        for v in (item.variants or []):
            lookup[v.lower()] = data

    # Return hanya terms yang di-query
    payload = {t: lookup[t] for t in raw if t in lookup}
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


def _serialize(item: CommodityGlossary) -> dict:
    return {
        "term":            item.term,
        "term_display":    item.term_display or item.term,
        "variants":        item.variants or [],
        "definition_nl":   item.definition_nl,
        "definition_id":   item.definition_id,
        "category":        item.category,
        "source_citation": item.source_citation,
    }
