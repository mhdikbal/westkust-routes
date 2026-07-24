"""
seed_fort_model_metrics.py

Muat data/export/system_dynamics_output.json (Model 5 -- System Dynamics) +
data/export/fort_archetype_clusters.json (klaster arketipe, sumber kebenaran
tunggal per arahan MLOPS 2026-07-24) ke tabel fort_model_metrics. Idempotent
-- truncate & reload tiap run, sama pola seed_linimasa_events.py.

Beda dari fort SIMULASI (n>=2 event, ada di system_dynamics_output.json
"forts") vs fort TIPIS (n<2, mis. Pauh/Sorkam -- di-SKIP model5, tak pernah
masuk JSON): keduanya TETAP dapat 1 baris fort_model_metrics (cluster diisi
dari fort_archetype_clusters.json, metrik lain None) -- supaya frontend bisa
tampilkan "data belum cukup" eksplisit, bukan diam-diam menghilangkan fort
dari tampilan.

Jalankan: docker compose exec backend python seed_fort_model_metrics.py
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

_BASE = Path(__file__).parent.parent


def _first_existing(candidates):
    return next((c for c in candidates if c.exists()), None)


SYSTEM_DYNAMICS_FILE = _first_existing([
    Path("/app/data/export/system_dynamics_output.json"),
    _BASE / "data" / "export" / "system_dynamics_output.json",
])
CLUSTERS_FILE = _first_existing([
    Path("/app/data/export/fort_archetype_clusters.json"),
    _BASE / "data" / "export" / "fort_archetype_clusters.json",
])


def build_metric_row(fort_name, cluster, current_status, model5_forts):
    """Bangun 1 baris fort_model_metrics dari output Model 5 (kalau ada) +
    klaster arketipe. Fort tak lolos simulate_fort (n<2, tak ada di
    model5_forts) tetap dapat baris -- cluster terisi, sisanya None (jujur
    soal "data belum cukup", bukan dihilangkan)."""
    result = model5_forts.get(fort_name)
    if result is None:
        return {
            "cluster": cluster,
            "p_self_current_status": None,
            "dynamics_series": None,
            "rmse": None,
        }

    beta_by_status = {b["status"]: b["beta"] for b in result.get("beta_log", [])}
    beta_current = beta_by_status.get(current_status)
    p_self_current_status = (1 - beta_current) if beta_current is not None else None

    actual_by_year = dict(zip(result["actual_years"], result["actual_I"]))
    dynamics_series = [
        {"year": y, "sim_I": round(i, 4), "actual_I": actual_by_year.get(y)}
        for y, i in zip(result["sim_years"], result["sim_I"])
    ]

    return {
        "cluster": cluster,
        "p_self_current_status": p_self_current_status,
        "dynamics_series": dynamics_series,
        "rmse": result.get("rmse"),
    }


def main():
    if SYSTEM_DYNAMICS_FILE is None:
        raise RuntimeError("system_dynamics_output.json tidak ditemukan -- jalankan model5_system_dynamics_1d.py dulu")
    if CLUSTERS_FILE is None:
        raise RuntimeError("fort_archetype_clusters.json tidak ditemukan")

    with open(SYSTEM_DYNAMICS_FILE) as f:
        sd = json.load(f)
    with open(CLUSTERS_FILE) as f:
        clusters = json.load(f)["clusters"]

    engine = create_engine(DATABASE_SYNC_URL, future=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    with Session(engine) as session:
        fort_name_to_id = dict(session.execute(text("SELECT name, id FROM forts")).all())

        # current_status per fort: dominion_status TERBARU (year DESC) --
        # sama query yg dipakai /power-status, tapi lintas SEMUA tahun (bukan
        # dibatasi year<=X) krn ini utk klasifikasi model, bukan tampilan
        # per-tahun.
        current_status_rows = session.execute(text("""
            SELECT DISTINCT ON (fort_id) fort_id, dominion_status
            FROM linimasa_events
            WHERE fort_id IS NOT NULL AND dominion_status IS NOT NULL AND year IS NOT NULL
            ORDER BY fort_id, year DESC, id DESC
        """)).all()
        current_status_by_fort_id = {r.fort_id: r.dominion_status for r in current_status_rows}

        records = []
        skipped_no_fort_row = []
        for fort_name, cluster in clusters.items():
            fort_id = fort_name_to_id.get(fort_name)
            if fort_id is None:
                skipped_no_fort_row.append(fort_name)
                continue
            current_status = current_status_by_fort_id.get(fort_id)
            row = build_metric_row(fort_name, cluster, current_status, sd["forts"])
            row["fort_id"] = fort_id
            row["computed_at"] = now
            records.append(row)

        session.execute(text("TRUNCATE TABLE fort_model_metrics RESTART IDENTITY"))
        if records:
            from models import FortModelMetric
            session.execute(FortModelMetric.__table__.insert(), records)
        session.commit()
        after = session.execute(text("SELECT COUNT(*) FROM fort_model_metrics")).scalar()

    print(f"fort_model_metrics: {after} baris ({len(records)} dari {len(clusters)} fort di fort_archetype_clusters.json)")
    if skipped_no_fort_row:
        print(f"dilewati (fort_name tak ada di tabel forts): {skipped_no_fort_row}")
    by_cluster = {}
    for r in records:
        by_cluster.setdefault(r["cluster"], 0)
        by_cluster[r["cluster"]] += 1
    print(f"per klaster: {by_cluster}")
    n_with_series = sum(1 for r in records if r["dynamics_series"] is not None)
    print(f"dynamics_series terisi: {n_with_series}/{len(records)} (sisanya fort n<2 event, model5 skip)")

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:forts-power-status")
        print(f"cache power-status di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
