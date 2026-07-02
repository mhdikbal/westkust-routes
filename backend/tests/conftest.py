"""
Shared test configuration and fixtures.
"""
import sys
import os

# Ensure backend module is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import cache


@pytest.fixture(autouse=True)
def _cache_off(monkeypatch):
    """Matikan Redis di semua test — cache nyata membuat test saling bocor
    (data mock test A ter-cache lalu di-HIT test B dengan param sama).
    Test cache sendiri meng-inject FakeRedis lewat monkeypatch _client."""
    monkeypatch.setattr(cache, "_client", None)
    monkeypatch.setattr(cache, "REDIS_URL", "")
