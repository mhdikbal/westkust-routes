"""Unit tests for seed_fort_model_metrics.py logic.

Pure function tests (no DB) -- mirrors backend/tests/test_seed_logic.py pattern.
Sumber: data/export/system_dynamics_output.json (Model 5) + fort_archetype_clusters.json.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed_fort_model_metrics import build_metric_row


class TestBuildMetricRow:
    def test_fort_with_simulation(self):
        """Fort yg lolos simulate_fort (n>=2) -- cluster, rmse, dynamics_series,
        dan p_self_current_status semua terisi."""
        model5_forts = {
            "Barus": {
                "sim_years": [1668, 1669, 1670],
                "sim_I": [0.3, 0.35, 0.4],
                "actual_years": [1668, 1670],
                "actual_I": [0.3, 0.0],
                "rmse": 0.562,
                "cluster": "Siklus",
                "beta_log": [{"status": "independence", "beta": 1.0, "source": "cluster-shrunk(n=1)"}],
            }
        }
        row = build_metric_row("Barus", "Siklus", "internal_conflict", model5_forts)
        assert row["cluster"] == "Siklus"
        assert row["rmse"] == 0.562
        assert row["dynamics_series"] is not None
        assert len(row["dynamics_series"]) == 3
        assert row["dynamics_series"][0] == {"year": 1668, "sim_I": 0.3, "actual_I": 0.3}
        assert row["dynamics_series"][1] == {"year": 1669, "sim_I": 0.35, "actual_I": None}

    def test_fort_below_simulation_threshold(self):
        """Fort n<2 (mis. Pauh, Sorkam) -- tak ada di model5_forts sama sekali
        (simulate_fort return None, di-skip Model 5). Tetap dapat baris
        fort_model_metrics dgn cluster='Tipis', metrik lain None -- BUKAN
        dihilangkan dari tabel sama sekali."""
        row = build_metric_row("Pauh", "Tipis", "internal_conflict", {})
        assert row["cluster"] == "Tipis"
        assert row["rmse"] is None
        assert row["dynamics_series"] is None
        assert row["p_self_current_status"] is None

    def test_p_self_current_status_from_beta_log(self):
        """P(self) status TERKINI diturunkan dari beta_log entry yg cocok
        current_status (bukan status pertama dlm sekuens) -- beta_for
        mengembalikan 1-P(self), jadi p_self = 1-beta."""
        model5_forts = {
            "Koto Tangah": {
                "sim_years": [1660, 1670], "sim_I": [1.0, 0.5],
                "actual_years": [1660, 1670], "actual_I": [1.0, 0.0],
                "rmse": 0.634, "cluster": "Siklus",
                "beta_log": [
                    {"status": "voc_alliance", "beta": 0.223, "source": "cluster-shrunk(n=20)"},
                    {"status": "internal_conflict", "beta": 1.0, "source": "cluster-shrunk(n=6)"},
                ],
            }
        }
        row = build_metric_row("Koto Tangah", "Siklus", "voc_alliance", model5_forts)
        assert row["p_self_current_status"] == 1 - 0.223

    def test_dynamics_series_actual_i_none_between_events(self):
        """Titik sim yg BUKAN persis di tahun actual_years -- actual_I None,
        bukan 0 atau diinterpolasi diam-diam (jujur soal apa yg diobservasi
        vs disimulasikan)."""
        model5_forts = {
            "X": {
                "sim_years": [1700, 1701, 1702, 1705],
                "sim_I": [0.1, 0.2, 0.3, 0.4],
                "actual_years": [1700, 1705],
                "actual_I": [0.1, 0.4],
                "rmse": 0.1, "cluster": "Sisa", "beta_log": [],
            }
        }
        row = build_metric_row("X", "Sisa", "voc_alliance", model5_forts)
        actual_vals = [pt["actual_I"] for pt in row["dynamics_series"]]
        assert actual_vals == [0.1, None, None, 0.4]
