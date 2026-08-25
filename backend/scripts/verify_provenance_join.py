#!/usr/bin/env python3
"""Verify the read-only join between Phase B's provenance audit and the
production `linimasa_events` table (Postgres), without ever touching
`linimasa_events.csv` or the database schema.

Join key: sha1(source_document|source_page|book_page|event_date_raw|title)[:4]
-- the same deterministic key used throughout Phase B (see
docs/thesis/pilot_annotation/MODEL_3B_EVENT_SOURCE_PROVENANCE_AUDIT.md).

Usage (must run inside the backend container, where /app == backend/ and
/app/data == the repo-root data/ bind mount):

    docker compose exec -e PYTHONPATH=/app backend python scripts/verify_provenance_join.py

Exits non-zero and prints unmatched rows if the join is not exactly 141/141.
This script performs no writes anywhere -- it is a read-only diagnostic.
"""
import asyncio
import hashlib
import json
import sys

from sqlalchemy import select

from database import AsyncSessionLocal
from models import LinimasaEvent

ARTIFACT_PATH = "/app/data/provenance/provenance_artifact.json"


def join_hash(source_document: str, source_page, book_page, event_date_raw: str, title: str) -> str:
    """Reconstruct Phase B's join key from live DB column values.

    NOTE: `book_page` is nullable on LinimasaEvent (Postgres NULL for an
    empty CSV field); Phase B's original hash was computed from
    csv.DictReader, where an empty field is an empty string, not None.
    NULL must be normalized to "" here to match -- this is exactly the kind
    of mismatch this script exists to catch if it were ever done wrong.
    """
    sp = str(source_page)
    bp = book_page or ""
    return hashlib.sha1(f"{source_document}|{sp}|{bp}|{event_date_raw}|{title}".encode("utf-8")).hexdigest()[:4]


async def main():
    with open(ARTIFACT_PATH, encoding="utf-8") as f:
        artifact = json.load(f)["events"]

    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                select(
                    LinimasaEvent.id,
                    LinimasaEvent.source_document,
                    LinimasaEvent.source_page,
                    LinimasaEvent.book_page,
                    LinimasaEvent.event_date_raw,
                    LinimasaEvent.title,
                )
            )
        ).all()

    total = len(rows)
    matched = 0
    unmatched = []
    seen_hashes = set()
    for r in rows:
        h = join_hash(r.source_document, r.source_page, r.book_page, r.event_date_raw, r.title)
        if h in seen_hashes:
            unmatched.append((r.id, "DUPLICATE_JOIN_HASH", h))
            continue
        seen_hashes.add(h)
        if h in artifact:
            matched += 1
        else:
            unmatched.append((r.id, "NO_ARTIFACT_MATCH", h, r.title))

    print(f"production rows: {total}")
    print(f"matched to provenance artifact: {matched}")
    print(f"unmatched: {len(unmatched)}")
    for u in unmatched[:20]:
        print("  ", u)

    if total != 141 or matched != 141 or unmatched:
        print("JOIN_INTEGRITY: FAIL -- not exactly 141/141")
        sys.exit(1)
    print("JOIN_INTEGRITY: PASS -- 141/141")


if __name__ == "__main__":
    asyncio.run(main())
