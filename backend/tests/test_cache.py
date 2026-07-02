"""
DBA-1 (Sprint SALIDO-LIVE) — Kontrak cache-aside Redis untuk backend/cache.py.

Ditulis SEBELUM implementasi (TDD RED). Kontrak yang diuji:
- make_key(namespace, params)  → key deterministik "voc:<ns>:<params terurut>"
- cache_get(key)               → nilai (deserialized) atau None (miss / Redis down)
- cache_set(key, value, ttl)   → simpan JSON dengan TTL (default 24 jam); no-op saat down
- invalidate_prefix(prefix)    → hapus semua key berprefix; dipakai seed_data.py
- Endpoint GET /api/voyages/   → header X-Cache: MISS lalu HIT; DB hanya di-query sekali
- Endpoint /api/voyages/export → TIDAK di-cache (StreamingResponse)

Redis dipalsukan (FakeRedis) — tidak butuh server Redis untuk unit test.
"""
import asyncio
import fnmatch
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cache
from main import app


# ─── Fake Redis ──────────────────────────────────────────────────────────────

class FakeRedis:
    """Redis asyncio palsu: get/set(ex=)/scan_iter(match=)/delete."""

    def __init__(self):
        self.store = {}   # key -> value (str)
        self.ttls = {}    # key -> ttl detik

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ex=None):
        self.store[key] = value
        if ex is not None:
            self.ttls[key] = ex

    async def scan_iter(self, match="*"):
        for key in list(self.store.keys()):
            if fnmatch.fnmatch(key, match):
                yield key

    async def delete(self, *keys):
        n = 0
        for k in keys:
            if k in self.store:
                del self.store[k]
                self.ttls.pop(k, None)
                n += 1
        return n


class DownRedis:
    """Semua operasi melempar ConnectionError — simulasi Redis mati."""

    def _boom(self, *a, **kw):
        raise ConnectionError("redis down")

    async def get(self, *a, **kw): self._boom()
    async def set(self, *a, **kw): self._boom()
    async def delete(self, *a, **kw): self._boom()

    def scan_iter(self, *a, **kw):
        async def gen():
            self._boom()
            yield  # pragma: no cover
        return gen()


@pytest.fixture
def fake_redis(monkeypatch):
    r = FakeRedis()
    monkeypatch.setattr(cache, "_client", r)
    return r


@pytest.fixture
def down_redis(monkeypatch):
    monkeypatch.setattr(cache, "_client", DownRedis())


# ─── make_key ────────────────────────────────────────────────────────────────

def test_make_key_deterministic_terhadap_urutan_param():
    """Urutan dict param tidak boleh mengubah key."""
    k1 = cache.make_key("voyages", {"year_from": 1700, "direction": "outbound"})
    k2 = cache.make_key("voyages", {"direction": "outbound", "year_from": 1700})
    assert k1 == k2


def test_make_key_pakai_prefix_voc_dan_namespace():
    k = cache.make_key("voyages", {"year_from": 1700})
    assert k.startswith("voc:voyages:")
    assert "year_from=1700" in k


def test_make_key_beda_param_beda_key():
    k1 = cache.make_key("voyages", {"year_from": 1700})
    k2 = cache.make_key("voyages", {"year_from": 1750})
    assert k1 != k2


def test_make_key_tanpa_param():
    assert cache.make_key("glossary", None) == cache.make_key("glossary", {})


# ─── cache_get / cache_set ───────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_roundtrip_set_lalu_get(fake_redis):
    data = [{"id": 1, "ship_name": "Theeboom", "total_gulden": 98358.05}]
    await cache.cache_set("voc:test:a", data)
    assert await cache.cache_get("voc:test:a") == data


@pytest.mark.asyncio
async def test_get_miss_mengembalikan_none(fake_redis):
    assert await cache.cache_get("voc:test:tidak-ada") is None


@pytest.mark.asyncio
async def test_set_memakai_ttl_default_24_jam(fake_redis):
    await cache.cache_set("voc:test:ttl", {"x": 1})
    assert fake_redis.ttls["voc:test:ttl"] == 86400


@pytest.mark.asyncio
async def test_set_ttl_kustom(fake_redis):
    await cache.cache_set("voc:test:ttl2", {"x": 1}, ttl=60)
    assert fake_redis.ttls["voc:test:ttl2"] == 60


# ─── invalidate_prefix ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_invalidate_hanya_hapus_prefix_cocok(fake_redis):
    await cache.cache_set("voc:voyages:a", 1)
    await cache.cache_set("voc:forts:b", 2)
    await cache.cache_set("lain:c", 3)

    deleted = await cache.invalidate_prefix("voc:")

    assert deleted == 2
    assert await cache.cache_get("voc:voyages:a") is None
    assert await cache.cache_get("voc:forts:b") is None
    assert fake_redis.store.get("lain:c") is not None


# ─── Degradasi anggun saat Redis mati ────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_saat_redis_down_kembalikan_none(down_redis):
    assert await cache.cache_get("voc:apapun") is None


@pytest.mark.asyncio
async def test_set_saat_redis_down_tidak_meledak(down_redis):
    await cache.cache_set("voc:apapun", {"x": 1})  # tidak boleh raise


@pytest.mark.asyncio
async def test_invalidate_saat_redis_down_kembalikan_nol(down_redis):
    assert await cache.invalidate_prefix("voc:") == 0


# ─── Sinkron — jalur seed_data.py (DBA-3) ────────────────────────────────────

class FakeSyncRedis:
    def __init__(self, keys):
        self.store = dict.fromkeys(keys, "1")

    def scan_iter(self, match="*"):
        yield from [k for k in list(self.store) if fnmatch.fnmatch(k, match)]

    def delete(self, *keys):
        n = 0
        for k in keys:
            n += 1 if self.store.pop(k, None) else 0
        return n


def test_invalidate_sync_hapus_prefix(monkeypatch):
    fake = FakeSyncRedis(["voc:voyages:a", "voc:forts:b", "lain:c"])
    monkeypatch.setattr(cache, "_sync_client", fake)
    assert cache.invalidate_prefix_sync() == 2
    assert list(fake.store) == ["lain:c"]


def test_invalidate_sync_tanpa_redis_kembalikan_nol(monkeypatch):
    monkeypatch.setattr(cache, "_sync_client", None)
    monkeypatch.setattr(cache, "REDIS_URL", "")
    assert cache.invalidate_prefix_sync() == 0


# ─── Integrasi endpoint /api/voyages/ ────────────────────────────────────────

def make_voyage(**kwargs):
    defaults = {
        "id": 1, "voyage_ref": 13447, "origin_id": 1, "destination_id": 6,
        "origin_name_raw": "Padang", "destination_name_raw": "Batavia",
        "ship_name": "Theeboom", "captain": None, "tonnage": None, "year": 1700,
        "departure_date": None, "arrival_date": None, "total_gulden": 98358.05,
        "main_product": "goud", "all_products": None, "cargo_count": 26,
        "duration_days": 44, "direction": "outbound", "source_url": None,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def override_db_counting(voyages):
    """Dependency override DB yang menghitung berapa kali di-query."""
    from database import get_db
    counter = {"execute": 0}

    async def mock_get_db():
        session = AsyncMock()

        async def counting_execute(*a, **kw):
            counter["execute"] += 1
            mock = MagicMock()
            mock.scalars.return_value.all.return_value = voyages
            return mock

        session.execute = counting_execute
        yield session

    app.dependency_overrides[get_db] = mock_get_db
    return counter


@pytest.mark.asyncio
async def test_voyages_list_miss_lalu_hit_db_sekali(fake_redis):
    """Request pertama MISS (query DB), kedua HIT (tanpa query DB)."""
    counter = override_db_counting([make_voyage()])
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            r1 = await client.get("/api/voyages/?year_from=1700&year_to=1710")
            r2 = await client.get("/api/voyages/?year_from=1700&year_to=1710")

        assert r1.status_code == 200 and r2.status_code == 200
        assert r1.headers.get("x-cache") == "MISS"
        assert r2.headers.get("x-cache") == "HIT"
        assert r1.json() == r2.json()
        assert counter["execute"] == 1
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_voyages_param_beda_tidak_pakai_cache_yang_sama(fake_redis):
    counter = override_db_counting([make_voyage()])
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            r1 = await client.get("/api/voyages/?year_from=1700")
            r2 = await client.get("/api/voyages/?year_from=1750")

        assert r1.headers.get("x-cache") == "MISS"
        assert r2.headers.get("x-cache") == "MISS"
        assert counter["execute"] == 2
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_export_csv_tidak_dicache(fake_redis):
    """StreamingResponse /export dikecualikan dari cache (PRD/ADR-001)."""
    counter = override_db_counting([make_voyage()])
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            r = await client.get("/api/voyages/export?year_from=1700")

        assert r.status_code == 200
        assert "x-cache" not in r.headers
        assert not any(k.startswith("voc:") and "export" in k for k in fake_redis.store)
    finally:
        app.dependency_overrides.clear()
