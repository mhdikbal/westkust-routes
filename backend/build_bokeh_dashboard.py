"""
build_bokeh_dashboard.py

Bangun 3 figur Bokeh interaktif dari output Model 2/5/6 (data/export/) untuk
halaman /riset/pemodelan/ -- TIDAK menghitung ulang model apa pun, murni
visualisasi lebih kaya dari angka yg sudah ada (bandingkan sparkline SVG kecil
di popup /atlas: buildSparklineSVG() di atlas.js).

Warna & label dominion_status di-REUSE persis dari
frontend/map_app/static/map_app/js/atlas.js (DOMINION_STATUS_COLORS/LABELS)
supaya konsisten lintas peta<->dashboard -- JANGAN drift jadi palet ke-2.

Semua figur statis (bokeh.embed.components(), bukan Bokeh server) -- Model 5
punya Select widget + CustomJS utk ganti fort tanpa round-trip Python, jadi
tak butuh proses Bokeh server yg hidup terus (arsitektur ini deliberately
menghindari proses ke-5 di docker-compose).

Jalankan manual: docker compose exec backend python build_bokeh_dashboard.py
(dipanggil ulang otomatis oleh endpoint /api/research/pemodelan-dashboard via
build_dashboard() kalau cache Redis kosong -- lihat routers/research.py).
"""
import csv
import json
from pathlib import Path

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Select, Column
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


def build_dynamics_selector():
    """Model 5: garis simulasi (sim_I) + titik aktual (actual_I, HANYA di tahun
    event nyata -- tak diinterpolasi, sama aturan buildSparklineSVG() atlas.js)
    per fort, satu chart + dropdown Select+CustomJS gonta-ganti fort tanpa
    round-trip server (components() statis cukup)."""
    with open(SYSTEM_DYNAMICS_FILE, encoding="utf-8") as f:
        sd = json.load(f)

    forts = sorted(sd["forts"].keys())
    if not forts:
        return None

    sources = {}
    for fort in forts:
        d = sd["forts"][fort]
        years = d["sim_years"]
        sim = d["sim_I"]
        actual_by_year = dict(zip(d["actual_years"], d["actual_I"]))
        actual = [actual_by_year.get(y) for y in years]
        sources[fort] = dict(year=years, sim=sim, actual=actual)

    default_fort = forts[0]
    sim_src = ColumnDataSource(dict(year=sources[default_fort]["year"], sim=sources[default_fort]["sim"]))
    actual_src = ColumnDataSource(dict(
        year=[y for y, a in zip(sources[default_fort]["year"], sources[default_fort]["actual"]) if a is not None],
        actual=[a for a in sources[default_fort]["actual"] if a is not None],
    ))
    # Lookup per-fort JAGGED (panjang beda-beda per fort) -- BUKAN tabel
    # rectangular, jadi diteruskan sbg dict Python biasa ke CustomJS (Bokeh
    # serialize otomatis ke JSON), bukan dipaksa jadi ColumnDataSource (itu
    # warn "columns must be of the same length" krn memang bukan pasangannya).

    p = figure(
        title="Model 5 — Simulasi vs Aktual per Fort (skala I: -1 relaps .. +1 aliansi VOC)",
        x_axis_label="Tahun", y_axis_label="I (indeks dominasi)",
        y_range=(-1.1, 1.1), height=420, width=640,
        toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset,save",
    )
    p.line("year", "sim", source=sim_src, line_width=2, color="#31384C", legend_label="Simulasi")
    actual_renderer = p.scatter("year", "actual", source=actual_src, size=8, color="#009880",
                                 marker="circle", legend_label="Aktual (titik event nyata)")
    hover = HoverTool(renderers=[actual_renderer], tooltips=[("Tahun", "@year"), ("I aktual", "@actual{0.00}")])
    p.add_tools(hover)
    p.legend.location = "bottom_right"
    p.legend.label_text_font_size = "9px"

    select = Select(title="Pilih fort:", value=default_fort, options=forts)
    callback = CustomJS(args=dict(sim_src=sim_src, actual_src=actual_src, all_data=sources), code="""
        const fort = cb_obj.value;
        const d = all_data[fort];
        const years = d["year"];
        const sim = d["sim"];
        const actual = d["actual"];
        sim_src.data = {year: years, sim: sim};
        const ay = [], av = [];
        for (let i = 0; i < actual.length; i++) {
            if (actual[i] !== null && actual[i] !== undefined) { ay.push(years[i]); av.push(actual[i]); }
        }
        actual_src.data = {year: ay, actual: av};
        sim_src.change.emit();
        actual_src.change.emit();
    """)
    select.js_on_change("value", callback)
    return Column(select, p)


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
    """Return {'markov': {...}, 'dynamics': {...}, 'game_theory': {...}} tiap
    key {'script':..., 'div':...}, atau None utk key yg sumber datanya belum
    ada (msh 'data belum cukup', bukan error keras -- konsisten pola
    build_metric_row() di seed_fort_model_metrics.py)."""
    result = {}

    if MARKOV_MATRIX_FILE and MARKOV_COUNTS_FILE:
        script, div = components(build_markov_heatmap())
        result["markov"] = {"script": script, "div": div}
    else:
        result["markov"] = None

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
