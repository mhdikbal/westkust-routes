"""
QA-SNK-1 — Regression guard granular untuk tabel research_theme_rows (Sankey tema-korpus).

SIFAT TEST INI (jujur): data korpus tema sudah live & ter-seed, jadi ini BUKAN
TDD RED-first murni — ini test KARAKTERISASI / regression guard. Fungsinya sebagai
GATE ANTI-DROP-DIAM-DIAM: mengunci angka granular per-korpus supaya bila re-seed atau
migration di masa depan menggeser data, kegagalan langsung terlihat di CI, bukan
menyelinap sebagai baris yang hilang senyap dari Sankey.

Kenapa granular (bukan cuma total)? Pelajaran [[feedback_sisir_semua_titik_pemakaian]]:
total 1005 bisa tetap "benar" sementara komposisi 470/535 bergeser diam-diam. Endpoint
/api/research/sankey-tema query-nya TIDAK menyertakan corpus_asal, jadi cakupan
470/470 daghregister MUSTAHIL dibuktikan lewat unit-test mock atau response HTTP —
harus query tabel research_theme_rows langsung. Karena itu file ini INTEGRATION
(real DB), terpisah dari test_research_sankey.py yang unit/mock. Test ini ADITIF —
tidak menghapus/mengubah test unit yang sudah hijau.

Pola sync_engine diadopsi dari test_atm_p0_us06.py.

Jalankan:
    docker compose exec -T backend pytest tests/test_research_qa_granular.py -v

BASELINE DIPERBARUI (2026-07-17, docs/prd/prd-pembersihan-korpus-daghregister.md):
angka lama (1005/470/535/27/481) adalah sblm pembersihan kebocoran scan
(nomor halaman/header tanggal/entri katalog arsip yg bocor ke kolom `text`,
sempat tampil di /riset/tema). 101+2 baris `non_narrative` (bukan narasi
peristiwa) dikeluarkan scr sengaja dari research_theme_rows -- baseline di
bawah SUDAH mencerminkan state pasca-cleaning yg benar, bukan regresi.
"""
import os
import sys

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routers.research import _split_ports  # noqa: E402  (endpoint logic under test)

SYNC_DB_URL = os.getenv(
    "SYNC_DATABASE_URL",
    "postgresql://vocuser:vocpassword@voc_db:5432/vocdb",
)


@pytest.fixture(scope="module")
def sync_engine():
    engine = create_engine(SYNC_DB_URL)
    # skip anggun bila DB tak tersedia (mis. jalan di luar docker network)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError as exc:
        engine.dispose()
        pytest.skip(f"DB research_theme_rows tak tersedia untuk integration test: {exc}")
    yield engine
    engine.dispose()


def _scalar(sync_engine, sql, **params):
    with sync_engine.connect() as conn:
        return conn.execute(text(sql), params).scalar()


# ─── 1. total ────────────────────────────────────────────────────────────────
def test_total_research_theme_rows(sync_engine):
    """Total baris korpus tema = 902 (baseline pasca-pembersihan kebocoran scan,
    2026-07-17 — sebelumnya 1005, 103 baris non_narrative dikeluarkan sengaja)."""
    total = _scalar(sync_engine, "SELECT count(*) FROM research_theme_rows")
    assert total == 902, f"total research_theme_rows = {total}, harusnya 902 (re-seed menggeser volume?)"


# ─── 2. count daghregister == 437 (baseline diperbarui pasca-cleaning) ───────
def test_count_daghregister_437(sync_engine):
    """DoD QA-SNK-1: baris corpus_asal='daghregister' TEPAT 437 (sebelumnya 470 —
    33 baris non_narrative/indeks-nama dikeluarkan saat pembersihan kebocoran scan)."""
    dagh = _scalar(
        sync_engine,
        "SELECT count(*) FROM research_theme_rows WHERE corpus_asal='daghregister'",
    )
    assert dagh == 437, f"daghregister = {dagh}, harusnya 437 (komposisi per-korpus bergeser diam-diam?)"


# ─── 3. count globalise == 465 ───────────────────────────────────────────────
def test_count_globalise_465(sync_engine):
    """Baris corpus_asal='globalise' TEPAT 465 (437 + 465 = 902, konsisten).
    Sebelumnya 535 -- 70 baris katalog/inventaris arsip (non_narrative)
    dikeluarkan saat pembersihan kebocoran scan."""
    glob = _scalar(
        sync_engine,
        "SELECT count(*) FROM research_theme_rows WHERE corpus_asal='globalise'",
    )
    assert glob == 465, f"globalise = {glob}, harusnya 465"


# ─── 4. count dekade IS NULL == 26 ───────────────────────────────────────────
def test_count_dekade_null_26(sync_engine):
    """26 baris tanpa dekade -> jatuh ke bucket 'Tak bertahun' (sebelumnya 27 --
    satu baris null-dekade termasuk yg dikeluarkan saat pembersihan). Angka
    dikunci agar pergeseran bucket null (mis. gagal parse tanggal) ketahuan."""
    null_dek = _scalar(
        sync_engine,
        "SELECT count(*) FROM research_theme_rows WHERE dekade IS NULL",
    )
    assert null_dek == 26, f"dekade IS NULL = {null_dek}, harusnya 26"


# ─── 5. daghregister 437/437 punya dekade (fix#1 backfill tuntas) ────────────
def test_daghregister_437_all_have_dekade(sync_engine):
    """INTI QA-SNK-1: seluruh 437 DR punya dekade NOT NULL (fix#1 backfill terbukti
    tuntas). Jika ada DR ber-dekade NULL, ia jatuh senyap ke bucket 'Tak bertahun'
    dan hilang dari alur dekade nyata di Sankey — regresi yang harus gagal keras."""
    dagh_with_dek = _scalar(
        sync_engine,
        "SELECT count(*) FROM research_theme_rows "
        "WHERE corpus_asal='daghregister' AND dekade IS NOT NULL",
    )
    dagh_null_dek = _scalar(
        sync_engine,
        "SELECT count(*) FROM research_theme_rows "
        "WHERE corpus_asal='daghregister' AND dekade IS NULL",
    )
    assert dagh_with_dek == 437, (
        f"{437 - dagh_with_dek}/437 DR tidak punya dekade -> jatuh ke bucket "
        f"'Tak bertahun', drop senyap dari Sankey (dagh_with_dekade={dagh_with_dek})"
    )
    assert dagh_null_dek == 0, (
        f"{dagh_null_dek} DR ber-dekade NULL — 26 bucket null harusnya MURNI globalise"
    )


# ─── 6. sanity multi-port: minimal 1 baris mengandung ';' ────────────────────
def test_multiport_rows_present(sync_engine):
    """Sanity FIX #2 (explode multi-port): ada baris pelabuhan_disebut multi-nilai.
    Bila 0, logika explode tema->pelabuhan tak teruji oleh data nyata."""
    multiport = _scalar(
        sync_engine,
        "SELECT count(*) FROM research_theme_rows WHERE pelabuhan_disebut LIKE '%;%'",
    )
    assert multiport >= 1, (
        f"tidak ada baris multi-port (LIKE '%;%') = {multiport}; explode tak teruji data nyata"
    )
    assert multiport == 436, (
        f"baris multi-port = {multiport}, baseline 436 (dagh=135 + glob=301, "
        f"sebelumnya 481 sblm pembersihan kebocoran scan) bergeser?"
    )


# ─── 7. _split_ports endpoint <-> data nyata (membership, bukan substring) ────
def test_split_ports_membership_real_row(sync_engine):
    """Menyambungkan logika endpoint (_split_ports) ke baris DB nyata (corpus_id=538):
    'Bayang; Inderapura; Pariaman; Salido' -> 4 token bersih. Membuktikan filter
    pelabuhan endpoint pakai KEANGGOTAAN token, bukan substring (Painan bukan Pariaman)."""
    raw = _scalar(
        sync_engine,
        "SELECT pelabuhan_disebut FROM research_theme_rows "
        "WHERE corpus_id=538 AND corpus_asal='daghregister'",
    )
    assert raw is not None, "baris DR corpus_id=538 (spot-check multi-port) hilang dari DB"
    ports = _split_ports(raw)
    assert ports == ["Bayang", "Inderapura", "Pariaman", "Salido"], (
        f"_split_ports({raw!r}) = {ports}, split multi-port meleset"
    )
    assert "Pariaman" in ports, "membership token Pariaman gagal (harusnya TRUE)"
    assert "Painan" not in ports, "false-match: 'Painan' tak boleh cocok (bukan substring)"


# ─── 8. corpus_id unik dalam DR (tak ada duplikat menggelembungkan 437) ───────
def test_daghregister_corpus_id_unique(sync_engine):
    """count(DISTINCT corpus_id) DR == 437 == jumlah baris DR: corpus_id unik, tak ada
    duplikat yang diam-diam menggelembungkan hitungan 437."""
    distinct_id = _scalar(
        sync_engine,
        "SELECT count(DISTINCT corpus_id) FROM research_theme_rows "
        "WHERE corpus_asal='daghregister'",
    )
    assert distinct_id == 437, (
        f"distinct corpus_id DR = {distinct_id}, harusnya 437 (duplikat corpus_id?)"
    )
