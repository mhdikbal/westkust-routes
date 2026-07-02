"""
Cache-aside Redis untuk endpoint read-heavy (ADR-001).

Data VOC praktis immutable (berubah hanya saat re-seed), maka TTL panjang
(24 jam) + invalidasi eksplisit prefix "voc:" dari seed_data.py.

Degradasi anggun: semua operasi menelan error koneksi — Redis mati berarti
cache miss, endpoint tetap dilayani langsung dari PostgreSQL.
"""
import json
import os
from typing import Any, Optional

try:
    import redis.asyncio as aioredis
    import redis as redis_sync
except ImportError:  # lingkungan tanpa paket redis (mis. unit test host)
    aioredis = None
    redis_sync = None

REDIS_URL = os.getenv("REDIS_URL", "")
DEFAULT_TTL = 86400  # 24 jam
PREFIX = "voc"

_client = None  # di-monkeypatch oleh test; lazy-init di get_client()


def get_client():
    """Klien redis.asyncio singleton; None bila Redis tidak dikonfigurasi."""
    global _client
    if _client is None and aioredis is not None and REDIS_URL:
        _client = aioredis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
    return _client


def make_key(namespace: str, params: Optional[dict] = None) -> str:
    """Key deterministik: voc:<namespace>:<param terurut>. None di-skip."""
    if not params:
        return f"{PREFIX}:{namespace}:"
    parts = "&".join(
        f"{k}={params[k]}" for k in sorted(params) if params[k] is not None
    )
    return f"{PREFIX}:{namespace}:{parts}"


async def cache_get(key: str) -> Optional[Any]:
    client = get_client()
    if client is None:
        return None
    try:
        raw = await client.get(key)
    except Exception:
        return None
    return json.loads(raw) if raw is not None else None


async def cache_set(key: str, value: Any, ttl: int = DEFAULT_TTL) -> None:
    client = get_client()
    if client is None:
        return
    try:
        await client.set(key, json.dumps(value, default=str), ex=ttl)
    except Exception:
        pass


async def invalidate_prefix(prefix: str = f"{PREFIX}:") -> int:
    """Hapus semua key berprefix. Return jumlah terhapus (0 bila Redis down)."""
    client = get_client()
    if client is None:
        return 0
    deleted = 0
    try:
        async for key in client.scan_iter(match=f"{prefix}*"):
            deleted += await client.delete(key)
    except Exception:
        return 0
    return deleted


# ── Sinkron — dipakai seed_data.py (jalan di luar event loop uvicorn) ────────

_sync_client = None


def get_sync_client():
    global _sync_client
    if _sync_client is None and redis_sync is not None and REDIS_URL:
        _sync_client = redis_sync.from_url(
            REDIS_URL, decode_responses=True, socket_connect_timeout=2
        )
    return _sync_client


def invalidate_prefix_sync(prefix: str = f"{PREFIX}:") -> int:
    client = get_sync_client()
    if client is None:
        return 0
    deleted = 0
    try:
        for key in client.scan_iter(match=f"{prefix}*"):
            deleted += client.delete(key)
    except Exception:
        return 0
    return deleted
