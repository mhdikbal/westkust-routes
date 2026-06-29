"""
Unit tests untuk AMH enrichment data di seed_data.py — US-18.

Test ini verifikasi bahwa FORTS_META sudah berisi amh_url dan amh_images
untuk fort-fort yang terkonfirmasi memiliki halaman AMH.

Tidak butuh database — hanya membaca struktur data Python.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Patch env var agar seed_data.py bisa diimpor tanpa DATABASE_SYNC_URL
os.environ.setdefault("DATABASE_SYNC_URL", "postgresql://dummy/dummy")

from seed_data import FORTS_META

# Lookup helper
_META_BY_NAME = {m["name"]: m for m in FORTS_META}

AMH_IMAGE_KEYS = {"title", "creator", "year", "thumbnail_url", "page_url"}


# ── Padang ────────────────────────────────────────────────────────────────────

def test_padang_meta_has_amh_url():
    """FORTS_META Padang harus punya amh_url non-null ke halaman AMH yang benar."""
    meta = _META_BY_NAME.get("Padang")
    assert meta is not None, "Entry 'Padang' tidak ada di FORTS_META"
    assert meta.get("amh_url"), "Padang belum punya amh_url"
    assert "atlasofmutualheritage.nl" in meta["amh_url"], (
        f"amh_url harus mengarah ke atlasofmutualheritage.nl, dapat: {meta['amh_url']}"
    )


def test_padang_meta_has_amh_images():
    """FORTS_META Padang harus punya amh_images list ≥1 item dengan keys yang benar."""
    meta = _META_BY_NAME.get("Padang")
    assert meta is not None
    images = meta.get("amh_images")
    assert images and isinstance(images, list) and len(images) >= 1, (
        f"Padang amh_images harus list ≥1 item, dapat: {images!r}"
    )
    for item in images:
        missing = AMH_IMAGE_KEYS - set(item.keys())
        assert not missing, (
            f"Item AMH Padang kehilangan keys: {missing}. Keys ada: {set(item.keys())}"
        )
        assert item.get("title"), f"title tidak boleh kosong: {item}"
        assert item.get("creator"), f"creator tidak boleh kosong: {item}"
        assert item.get("year"), f"year tidak boleh kosong: {item}"
        assert item.get("page_url"), f"page_url tidak boleh kosong: {item}"


def test_padang_amh_images_have_correct_page_url():
    """Setiap item amh_images Padang harus punya page_url mengarah ke AMH."""
    meta = _META_BY_NAME.get("Padang")
    assert meta is not None
    for item in meta.get("amh_images", []):
        assert "atlasofmutualheritage.nl" in item.get("page_url", ""), (
            f"page_url harus ke atlasofmutualheritage.nl: {item['page_url']}"
        )


# ── Pulau Cingkuak ────────────────────────────────────────────────────────────

def test_pulau_cingkuak_meta_has_amh_url():
    """FORTS_META Pulau Cingkuak harus punya amh_url non-null."""
    meta = _META_BY_NAME.get("Pulau Cingkuak")
    assert meta is not None, "Entry 'Pulau Cingkuak' tidak ada di FORTS_META"
    assert meta.get("amh_url"), "Pulau Cingkuak belum punya amh_url"
    assert "atlasofmutualheritage.nl" in meta["amh_url"]


def test_pulau_cingkuak_meta_has_amh_images():
    """FORTS_META Pulau Cingkuak harus punya amh_images list ≥1 item."""
    meta = _META_BY_NAME.get("Pulau Cingkuak")
    assert meta is not None
    images = meta.get("amh_images")
    assert images and isinstance(images, list) and len(images) >= 1, (
        f"Pulau Cingkuak amh_images harus list ≥1 item, dapat: {images!r}"
    )
    for item in images:
        missing = AMH_IMAGE_KEYS - set(item.keys())
        assert not missing, f"Item AMH Pulau Cingkuak kehilangan keys: {missing}"


# ── Invariant: semua fort dengan amh_url harus punya amh_images ───────────────

def test_all_forts_with_amh_url_have_amh_images():
    """Setiap fort yang punya amh_url harus punya amh_images ≥1 item."""
    for meta in FORTS_META:
        if meta.get("amh_url"):
            images = meta.get("amh_images")
            assert images and len(images) >= 1, (
                f"Fort '{meta['name']}' punya amh_url tapi amh_images kosong/null"
            )


def test_forts_without_amh_url_have_no_amh_images():
    """Fort yang tidak punya amh_url sebaiknya juga tidak punya amh_images — konsistensi data."""
    for meta in FORTS_META:
        if not meta.get("amh_url"):
            images = meta.get("amh_images")
            assert not images, (
                f"Fort '{meta['name']}' tidak punya amh_url tapi punya amh_images: {images!r}\n"
                f"Jika ingin menambah amh_images, tambah juga amh_url-nya."
            )
