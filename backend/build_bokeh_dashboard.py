"""
build_bokeh_dashboard.py

Bangun 4 figur Bokeh interaktif dari output Model 2/3/5/6 (data/export/) untuk
halaman /riset/pemodelan/ -- TIDAK menghitung ulang model apa pun, murni
visualisasi lebih kaya dari angka yg sudah ada (bandingkan sparkline SVG kecil
di popup /atlas: buildSparklineSVG() di atlas.js).

Warna & label dominion_status di-REUSE persis dari
frontend/map_app/static/map_app/js/atlas.js (DOMINION_STATUS_COLORS/LABELS)
supaya konsisten lintas peta<->dashboard -- JANGAN drift jadi palet ke-2.

Semua figur statis (bokeh.embed.components(), bukan Bokeh server). Model 5
pakai Tabs/TabPanel (SATU figure per fort, tab native BokehJS) -- BUKAN
Select+CustomJS: CustomJS Bokeh selalu di-compile via `new Function(...)` di
browser (eval), dan CSP proyek ini (nginx/nginx.conf) TIDAK punya
'unsafe-eval' di script-src. CustomJS diam-diam gagal (exception ketelan,
<select> DOM tetap keliatan ganti krn itu reactive binding-nya sendiri, tapi
chart tak pernah update) -- ditemukan via Playwright 2026-07-25 (semua fort
tampil garis rata krn chart macet di data awal). Tabs murni widget bawaan
BokehJS (bukan eval kode Python), jadi aman di CSP saat ini tanpa perlu
longgarkan 'unsafe-eval'.

Jalankan manual: docker compose exec backend python build_bokeh_dashboard.py
(dipanggil ulang otomatis oleh endpoint /api/research/pemodelan-dashboard via
build_dashboard() kalau cache Redis kosong -- lihat routers/research.py).
"""
import csv
import json
from pathlib import Path

import numpy as np
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, TabPanel, Tabs
from bokeh.plotting import figure

_BASE = Path(__file__).parent.parent


def _first_existing(candidates):
    return next((c for c in candidates if c.exists()), None)


MARKOV_MATRIX_FILE = _first_existing([
    Path("/app/data/export/markov_transition_matrix.csv"),
    _BASE / "data" / "export" / "markov_transition_matrix.csv",
])
MARKOV_COUNTS_FILE = _first_existing([
    Path("/app/data/export/markov_counts.csv"),
    _BASE / "data" / "export" / "markov_counts.csv",
])
SYSTEM_DYNAMICS_FILE = _first_existing([
    Path("/app/data/export/system_dynamics_output.json"),
    _BASE / "data" / "export" / "system_dynamics_output.json",
])
H2_REAFFIRMATION_FILE = _first_existing([
    Path("/app/data/export/game_theory_h2_reaffirmation.json"),
    _BASE / "data" / "export" / "game_theory_h2_reaffirmation.json",
])
HAWKES_FILE = _first_existing([
    Path("/app/data/export/hawkes_model_output.json"),
    _BASE / "data" / "export" / "hawkes_model_output.json",
])

# REUSE persis dari atlas.js DOMINION_STATUS_COLORS/LABELS -- lihat komentar modul.
DOMINION_STATUS_COLORS = {
    "aceh_dominion":     "#a02830",
    "relapse_aceh":      "#d26060",
    "voc_alliance":      "#009880",
    "independence":      "#1254ac",
    "foreign_orbit":     "#ab3782",
    "voc_withdrawal":    "#9c640d",
    "internal_conflict": "#569859",
}
DOMINION_STATUS_LABELS = {
    "aceh_dominion":     "Kekuasaan Aceh",
    "relapse_aceh":      "Relaps ke Aceh",
    "voc_alliance":      "Aliansi VOC",
    "independence":      "Merdeka",
    "foreign_orbit":     "Orbit Eropa lain",
    "voc_withdrawal":    "VOC mundur",
    "internal_conflict": "Konflik internal",
}
CLUSTER_COLORS = {
    "Siklus": "#a02830",
    "Stabil": "#009880",
    "Sisa":   "#9c640d",
    "Tipis":  "#7a7368",
}


def _read_csv_matrix(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header = rows[0][1:]
    data = {r[0]: [float(v) if v not in ("", None) else None for v in r[1:]] for r in rows[1:]}
    return header, data


def build_markov_heatmap():
    """Heatmap states x states -- P(transisi), hover tampilkan probabilitas + n.
    Sel kosong (mis. relapse_aceh: n=0 observasi keluar) DIBIARKAN kosong,
    BUKAN 0 -- 0 berarti 'diamati tak pernah pindah', kosong berarti 'tak ada
    observasi', beda makna (lihat GOTCHA di model2_markov_dominion_status.py)."""
    states, probs = _read_csv_matrix(MARKOV_MATRIX_FILE)
    _, counts = _read_csv_matrix(MARKOV_COUNTS_FILE)

    xs, ys, alphas, colors, labels, prob_txt, n_txt = [], [], [], [], [], [], []
    for from_s in states:
        for j, to_s in enumerate(states):
            p = probs[from_s][j]
            n = counts[from_s][j] if from_s in counts else None
            xs.append(DOMINION_STATUS_LABELS.get(to_s, to_s))
            ys.append(DOMINION_STATUS_LABELS.get(from_s, from_s))
            if p is None:
                alphas.append(0.0)
                prob_txt.append("tak ada observasi")
                n_txt.append("n=0")
            else:
                alphas.append(0.15 + p * 0.85)
                prob_txt.append(f"{p:.1%}")
                n_txt.append(f"n={int(n) if n is not None else '?'}")
            colors.append(DOMINION_STATUS_COLORS.get(from_s, "#888"))
            labels.append(from_s)

    src = ColumnDataSource(dict(x=xs, y=ys, alpha=alphas, color=colors, prob=prob_txt, n=n_txt))
    display_states = [DOMINION_STATUS_LABELS.get(s, s) for s in states]

    p = figure(
        x_range=display_states, y_range=list(reversed(display_states)),
        title="Model 2 — Matriks Transisi Markov (dominion_status)",
        toolbar_location="above", tools="hover,pan,wheel_zoom,reset,save",
        height=420, width=560,
    )
    p.rect(x="x", y="y", width=1, height=1, source=src,
           fill_color="color", fill_alpha="alpha", line_color="#1e1e1e", line_width=0.5)
    p.xaxis.major_label_orientation = 0.9
    p.grid.visible = False
    hover = p.select_one(HoverTool)
    hover.tooltips = [("Dari", "@y"), ("Ke", "@x"), ("P(transisi)", "@prob"), ("Observasi", "@n")]
    return p


def build_hawkes_intensity():
    """Model 3: kurva intensitas kondisional lambda(t) proses Hawkes (kernel
    eksponensial) yg dicocokkan ke 141 event linimasa, dgn 141 event asli
    ditumpangkan sbg titik di sepanjang kurva (y diinterpolasi dari grid
    intensitas via np.interp -- pola sama Model 5: titik aktual HANYA di tahun
    event nyata, bukan garis simulasi yg diinterpolasi terus-menerus).
    Judul menyertakan statistik kunci LANGSUNG dari file (alpha, beta, LR,
    p-value, n) -- JANGAN hardcode angka dari memori sesi lama, itu sudah
    berubah (mis. hasil stratifikasi per klaster beda dari hasil pooled di
    file ini) [[project_markov_hawkes_models]]. p_value dibulatkan ke 0.0 di
    file -> ditampilkan sbg 'p<0.0001', bukan literal 'p=0.0'."""
    with open(HAWKES_FILE, encoding="utf-8") as f:
        hk = json.load(f)

    params = hk["params"]
    years = [pt[0] for pt in hk["intensity"]]
    lam = [pt[1] for pt in hk["intensity"]]
    events = hk["events"]
    event_lam = list(np.interp(events, years, lam))

    curve_src = ColumnDataSource(dict(year=years, lam=lam))
    event_src = ColumnDataSource(dict(year=events, lam=event_lam))

    p_str = "p<0.0001" if params["p_value"] < 0.0001 else f"p={params['p_value']:.4f}"
    p = figure(
        title=(
            f"Model 3 — Baseline Hawkes Eksploratif "
            f"(α={params['alpha']:.3f}, β={params['beta']:.3f}/thn, "
            f"LR={params['LR']:.1f}, {p_str}, n={params['n']})"
        ),
        x_axis_label="Tahun", y_axis_label="λ(t) — intensitas kondisional",
        height=420, width=780,
        toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset,save",
    )
    line_renderer = p.line(
        "year", "lam", source=curve_src, line_width=2, color=CLUSTER_COLORS["Siklus"],
        legend_label="λ(t) tercocokkan",
    )
    event_renderer = p.scatter(
        "year", "lam", source=event_src, size=6, color="#31384C", marker="circle",
        legend_label="Event nyata (linimasa)",
    )
    hover_curve = HoverTool(renderers=[line_renderer], tooltips=[("Tahun", "@year{0.0}"), ("λ(t)", "@lam{0.000}")])
    hover_event = HoverTool(renderers=[event_renderer], tooltips=[("Tahun event", "@year{0.0}")])
    p.add_tools(hover_curve, hover_event)
    p.legend.location = "top_right"
    p.legend.label_text_font_size = "9px"

    # Ringkasan statistik presentasi utk panel "Batas Interpretasi" /riset/pemodelan --
    # SEMUA nilai dibaca langsung dari HAWKES_FILE (params di atas), TIDAK ada fitting
    # ulang. branching_ratio = alpha/beta adalah pembagian deterministik murni,
    # BUKAN parameter baru yg dicocokkan (lihat BETA_UI_DEPLOYMENT_AUDIT.md #4).
    branching_ratio = params["alpha"] / params["beta"]
    hawkes_stats = {
        "n_events": params["n"],
        # Diformat sbg string desimal-koma (id-ID) SEKALI di sini -- satu-satunya
        # sumber format angka utk panel "Ringkasan Statistik", supaya tak ada
        # pembulatan berbeda antar komponen UI (lihat BETA_UI_DEPLOYMENT_AUDIT.md #4).
        "mu": f"{params['mu']:.3f}".replace(".", ","),
        "alpha": f"{params['alpha']:.3f}".replace(".", ","),
        "beta": f"{params['beta']:.3f}".replace(".", ","),
        "branching_ratio": f"{branching_ratio:.3f}".replace(".", ","),
        "kernel": "eksponensial",
    }
    return p, hawkes_stats


def build_dynamics_selector():
    """Model 5: garis simulasi (sim_I) + titik aktual (actual_I, HANYA di tahun
    event nyata -- tak diinterpolasi, sama aturan buildSparklineSVG() atlas.js)
    per fort, SATU tab per fort (Tabs/TabPanel -- lihat catatan modul kenapa
    BUKAN Select+CustomJS)."""
    with open(SYSTEM_DYNAMICS_FILE, encoding="utf-8") as f:
        sd = json.load(f)

    forts = sorted(sd["forts"].keys())
    if not forts:
        return None

    panels = []
    for fort in forts:
        d = sd["forts"][fort]
        years = d["sim_years"]
        sim = d["sim_I"]
        actual_by_year = dict(zip(d["actual_years"], d["actual_I"]))

        sim_src = ColumnDataSource(dict(year=years, sim=sim))
        actual_years = [y for y in years if y in actual_by_year]
        actual_src = ColumnDataSource(dict(
            year=actual_years,
            actual=[actual_by_year[y] for y in actual_years],
        ))

        p = figure(
            title=f"Model 5 — {fort}: Simulasi vs Aktual (skala I: -1 relaps .. +1 aliansi VOC)",
            x_axis_label="Tahun", y_axis_label="I (indeks dominasi)",
            y_range=(-1.1, 1.1), height=380, width=620,
            toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset,save",
        )
        p.line("year", "sim", source=sim_src, line_width=2, color="#31384C", legend_label="Simulasi")
        actual_renderer = p.scatter("year", "actual", source=actual_src, size=8, color="#009880",
                                     marker="circle", legend_label="Aktual (titik event nyata)")
        hover = HoverTool(renderers=[actual_renderer], tooltips=[("Tahun", "@year"), ("I aktual", "@actual{0.00}")])
        p.add_tools(hover)
        p.legend.location = "bottom_right"
        p.legend.label_text_font_size = "9px"

        panels.append(TabPanel(child=p, title=fort))

    return Tabs(tabs=panels)


def build_reaffirmation_bars():
    """Model 6 H2: rate re-afirmasi voc_alliance/tahun per klaster arketipe,
    hover breakdown per fort (data/export/game_theory_h2_reaffirmation.json --
    sblmnya cuma print stdout di model6_game_theory.py, skrg jg disimpan)."""
    with open(H2_REAFFIRMATION_FILE, encoding="utf-8") as f:
        h2 = json.load(f)

    clusters = list(h2.keys())
    rates = [h2[c]["rate_rata2"] for c in clusters]
    colors = [CLUSTER_COLORS.get(c, "#888") for c in clusters]
    breakdown = [
        "; ".join(f"{pf['fort']} ({pf['rate']}/thn)" for pf in h2[c]["per_fort"])
        for c in clusters
    ]

    src = ColumnDataSource(dict(cluster=clusters, rate=rates, color=colors, breakdown=breakdown))
    p = figure(
        x_range=clusters, title="Model 6 — Tingkat Re-afirmasi voc_alliance per Klaster Arketipe",
        y_axis_label="re-afirmasi / tahun", height=380, width=480,
        toolbar_location="above", tools="hover,pan,reset,save",
    )
    p.vbar(x="cluster", top="rate", width=0.6, source=src, fill_color="color", line_color=None)
    hover = p.select_one(HoverTool)
    hover.tooltips = [("Klaster", "@cluster"), ("Rate rata2", "@rate{0.000}/thn"), ("Per fort", "@breakdown")]
    p.xgrid.visible = False
    return p


def build_dashboard():
    """Return {'markov': {...}, 'hawkes': {...}, 'dynamics': {...}, 'game_theory': {...}}
    tiap key {'script':..., 'div':...}, atau None utk key yg sumber datanya
    belum ada (msh 'data belum cukup', bukan error keras -- konsisten pola
    build_metric_row() di seed_fort_model_metrics.py)."""
    result = {}

    if MARKOV_MATRIX_FILE and MARKOV_COUNTS_FILE:
        script, div = components(build_markov_heatmap())
        result["markov"] = {"script": script, "div": div}
    else:
        result["markov"] = None

    if HAWKES_FILE:
        fig, hawkes_stats = build_hawkes_intensity()
        script, div = components(fig)
        result["hawkes"] = {"script": script, "div": div, "params": hawkes_stats}
    else:
        result["hawkes"] = None

    if SYSTEM_DYNAMICS_FILE:
        fig = build_dynamics_selector()
        result["dynamics"] = None if fig is None else dict(zip(("script", "div"), components(fig)))
    else:
        result["dynamics"] = None

    if H2_REAFFIRMATION_FILE:
        script, div = components(build_reaffirmation_bars())
        result["game_theory"] = {"script": script, "div": div}
    else:
        result["game_theory"] = None

    return result


if __name__ == "__main__":
    out = build_dashboard()
    for k, v in out.items():
        status = "OK" if v else "KOSONG (sumber data tak ditemukan)"
        print(f"{k}: {status}")
