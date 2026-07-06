from datetime import datetime, timezone
from typing import Optional, List
import hashlib

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, ConfigDict, field_validator

from database import get_db
from models import StagingExtraction, ApiKey

router = APIRouter()

VALID_CONFIDENCE_FLAGS = {"unverified", "reviewed", "promoted", "rejected"}


async def verify_api_key(
    x_api_key: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
) -> str:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
    result = await db.execute(
        select(ApiKey).where(ApiKey.key_hash == key_hash, ApiKey.active == "true")
    )
    api_key = result.scalars().all()
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key[0].label


# ---------- Schemas ----------

class ExtractionItem(BaseModel):
    external_ref: str
    text_indonesia: str
    text_asli: Optional[str] = None
    metadata: Optional[dict] = None


class ExtractionBatch(BaseModel):
    source: str
    batch_id: Optional[str] = None
    items: List[ExtractionItem]


class BatchResult(BaseModel):
    inserted: int
    skipped_duplicate: int


class StagingExtractionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    source: str
    external_ref: str
    batch_id: Optional[str] = None
    text_indonesia: str
    text_asli: Optional[str] = None
    metadata_json: Optional[dict] = None
    confidence_flag: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    created_at: str


class PatchConfidence(BaseModel):
    confidence_flag: str
    reviewed_by: Optional[str] = None

    @field_validator("confidence_flag")
    @classmethod
    def validate_flag(cls, v):
        if v not in VALID_CONFIDENCE_FLAGS:
            raise ValueError(f"confidence_flag harus salah satu dari {sorted(VALID_CONFIDENCE_FLAGS)}")
        return v


# ---------- Endpoints ----------

@router.post("/extractions", status_code=201, response_model=BatchResult)
async def create_extractions(
    batch: ExtractionBatch,
    db: AsyncSession = Depends(get_db),
    _label: str = Depends(verify_api_key),
):
    if not batch.items:
        return BatchResult(inserted=0, skipped_duplicate=0)

    refs = [item.external_ref for item in batch.items]
    result = await db.execute(
        select(StagingExtraction.external_ref).where(
            StagingExtraction.source == batch.source,
            StagingExtraction.external_ref.in_(refs),
        )
    )
    existing_refs = set(result.scalars().all())

    now = datetime.now(timezone.utc).isoformat()
    new_items = [item for item in batch.items if item.external_ref not in existing_refs]
    for item in new_items:
        db.add(StagingExtraction(
            source=batch.source,
            external_ref=item.external_ref,
            batch_id=batch.batch_id,
            text_indonesia=item.text_indonesia,
            text_asli=item.text_asli,
            metadata_json=item.metadata,
            created_at=now,
        ))
    await db.commit()

    return BatchResult(
        inserted=len(new_items),
        skipped_duplicate=len(batch.items) - len(new_items),
    )


@router.get("/extractions", response_model=List[StagingExtractionSchema])
async def list_extractions(
    source: Optional[str] = None,
    confidence_flag: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    _label: str = Depends(verify_api_key),
):
    stmt = select(StagingExtraction)
    if source:
        stmt = stmt.where(StagingExtraction.source == source)
    if confidence_flag:
        stmt = stmt.where(StagingExtraction.confidence_flag == confidence_flag)
    stmt = stmt.order_by(StagingExtraction.id).limit(limit).offset(offset)

    result = await db.execute(stmt)
    return result.scalars().all()


@router.patch("/extractions/{extraction_id}", response_model=StagingExtractionSchema)
async def update_confidence(
    extraction_id: int,
    patch: PatchConfidence,
    db: AsyncSession = Depends(get_db),
    _label: str = Depends(verify_api_key),
):
    result = await db.execute(
        select(StagingExtraction).where(StagingExtraction.id == extraction_id)
    )
    rows = result.scalars().all()
    if not rows:
        raise HTTPException(status_code=404, detail="Extraction not found")

    extraction = rows[0]
    extraction.confidence_flag = patch.confidence_flag
    if patch.reviewed_by:
        extraction.reviewed_by = patch.reviewed_by
        extraction.reviewed_at = datetime.now(timezone.utc).isoformat()
    await db.commit()
    return extraction
