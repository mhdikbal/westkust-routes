import json
import os
import httpx
from django.shortcuts import render
from django.http import Http404

API_BASE = os.getenv("API_BASE_URL", "http://voc_backend:8000")

# Babak naratif /linimasa Fase 1 (docs/prd-linimasa-kronik-pantai-barat.md).
# Copy editorial (label/headline/summary) SENGAJA dipisah dari data event
# bersumber (linimasa_events.era_slug, backend/models.py) -- interpretasi vs
# fakta tersitasi tak boleh campur di satu tempat. Urutan list = urutan babak
# kronologis, dipakai langsung utk grouping di bawah (bukan alfabetis).
LINIMASA_ERAS = [
    {
        "slug": "klaim-awal",
        "label": "Klaim Yurisdiksi & Kekuasaan Iskandar Muda",
        "range": "1625–1637",
        "headline": "Sebelum satu meriam pun ditembakkan, Atjeh sudah mengklaim seluruh pantai Sumatra sebagai wilayahnya.",
        "summary": (
            "Dari risalah VOC sendiri (1625) yang mengakui yurisdiksi Atjeh atas “seluruh pantai "
            "timur dan barat Sumatra”, sampai titah tol Sultan Iskandar Muda (1632) dan wafatnya yang "
            "penuh gejolak (1637) — pondasi kekuasaan yang akan bertahan tiga dekade lebih diletakkan di sini."
        ),
    },
    {
        "slug": "ratu-puncak",
        "label": "Ratu Atjeh & Puncak Kekuasaan",
        "range": "1643–1648",
        "headline": "Seorang perempuan memerintah dari Atjeh, dan VOC mencatatnya dengan hormat yang jarang diberikan pada penguasa lain.",
        "summary": (
            "Ratu Atjeh (konsisten dengan Sultana Safiatuddin) menegaskan kembali klaim atas Perak dan "
            "“segala tanah serta pelabuhan” di bawahnya — bahkan ketika panglima Salida mulai "
            "mengundang VOC berdagang langsung, tanda pertama otonomi lokal yang akan tumbuh."
        ),
    },
    {
        "slug": "perang-damai",
        "label": "Perang & Perdamaian",
        "range": "1656–1659",
        "headline": "Ratu memerintahkan penangkapan setiap orang VOC di pantai barat. Tiga tahun kemudian, ia mengirim surat perdamaian dengan upacara penuh.",
        "summary": (
            "Perang terbuka VOC-Atjeh meninggalkan kerugian terbesar dalam catatan ini — personel Belanda "
            "ditangkap dan disiksa, sebagian tak pernah kembali. Perdamaian 1659 menutup babak ini, tapi "
            "luka yang ditinggalkan tidak."
        ),
    },
    {
        "slug": "retak-painan",
        "label": "Retak & Pemberontakan Painan",
        "range": "1660–1663",
        "headline": "Panglima yang dulu dipaksa menyerang VOC atas nama Atjeh, kini memilih memberontak dari Atjeh sendiri.",
        "summary": (
            "Dalam tiga tahun, kesetiaan pantai barat runtuh: Ticco dan Indrapoura melepaskan diri, dan "
            "pada 1663 konfederasi Songypagouers menandatangani Traktat Painan dengan VOC — titik resmi "
            "berakhirnya kekuasaan Atjeh atas wilayah ini."
        ),
    },
    {
        "slug": "pengusiran-penataan",
        "label": "Pengusiran & Penataan Ulang",
        "range": "1664–1681",
        "headline": "Yang tersisa dari kekuasaan Atjeh di pantai barat akhirnya diusir dengan senjata — digantikan tatanan baru yang bertahan puluhan tahun.",
        "summary": (
            "Kampanye militer menuntaskan apa yang dimulai Traktat Painan. Sillida diserahkan resmi ke VOC "
            "(1667), dan pada 1681 — delapan belas tahun kemudian — bahkan Barus diwajibkan menyerahkan "
            "senjata terakhir bermahkota Atjeh."
        ),
    },
]


def index(request):
    """Main map page — VOC Trade Atlas."""
    return render(request, "map_app/index.html")


def riset_tema(request):
    """SNK-5 — Sankey tema-korpus (thesis-only, /riset/tema).
    Halaman statis: diagram & drill-down ditarik client-side dari /api/research
    (nginx proxy). noindex + tidak di navbar publik (SEC-SNK-2). Identitas visual
    salido.my.id (EB Garamond + Space Grotesk)."""
    return render(request, "map_app/riset_tema.html")


def riset_jaringan(request):
    """Network Graph Fase 1 — graf co-occurrence pelabuhan (thesis-only, /riset/jaringan).
    Halaman statis: graf force-directed & drill-down ditarik client-side dari
    /api/research/network-pelabuhan + /sankey-tema/rows (nginx proxy). noindex +
    tidak di navbar publik (konsisten /riset/tema). Identitas visual salido.my.id."""
    return render(request, "map_app/riset_jaringan.html")


def riset_atjeh(request):
    """Dagang Atjeh 1643-1644 — laporan dagang dari/ke Atjeh (thesis-only, /riset/atjeh-dagang).
    Halaman statis: tabel ditarik client-side dari /api/research/atjeh-trade (nginx
    proxy). noindex + tidak di navbar publik (konsisten /riset/tema, /riset/jaringan).
    Identitas visual salido.my.id (EB Garamond + Space Grotesk)."""
    return render(request, "map_app/riset_atjeh.html")


def linimasa(request):
    """Linimasa suksesi kekuasaan Atjeh, Iskandar Muda -> Ratu -> Traktat
    Painan 1663 (thesis-only, top-level /linimasa). Fase 1 (docs/prd-linimasa-
    kronik-pantai-barat.md): SSR penuh -- event di-render server-side dari
    httpx.get() sinkron ke /api/research/linimasa (pola sama port_detail di
    bawah), BUKAN client-side fetch() spt riset_tema/riset_jaringan/riset_atjeh.
    Konten utama (judul, kutipan, sumber) harus terbaca tanpa JavaScript;
    JS cuma progressive enhancement (filter jenis, SVG timeline). noindex +
    tidak di navbar publik. Identitas visual salido.my.id, palet arsip
    tersendiri (beda dari 3 halaman riset lain yg putih-polos)."""
    items = []
    meta = {}
    backend_error = False
    try:
        r = httpx.get(f"{API_BASE}/api/research/linimasa", timeout=8.0)
        r.raise_for_status()
        payload = r.json()
        items = payload.get("items", [])
        meta = payload.get("meta", {})
    except Exception:
        backend_error = True

    eras_with_events = []
    for era in LINIMASA_ERAS:
        era_events = [it for it in items if it.get("era_slug") == era["slug"]]
        if not era_events:
            continue
        eras_with_events.append({**era, "events": era_events})

    context = {
        "eras": eras_with_events,
        "meta": meta,
        "n_items": len(items),
        "backend_error": backend_error,
        "items_json": json.dumps(items),
    }
    return render(request, "map_app/linimasa.html", context)


def port_detail(request, slug):
    """Detail page for a single VOC port/fort."""
    # Convert slug to title-cased name (e.g. "pulau-cingkuak" → "Pulau Cingkuak")
    name = slug.replace("-", " ").title()

    try:
        r = httpx.get(f"{API_BASE}/api/forts/", timeout=8.0)
        r.raise_for_status()
        forts = r.json()
    except Exception:
        raise Http404("Backend tidak dapat dihubungi")

    fort_summary = next((f for f in forts if f["name"].lower() == name.lower()), None)
    if not fort_summary:
        raise Http404(f"Pelabuhan '{name}' tidak ditemukan")

    # Fetch enrichment detail (US-02 / US-03 fields)
    fort_id = fort_summary["id"]
    try:
        enr = httpx.get(f"{API_BASE}/api/forts/{fort_id}/enrichment", timeout=8.0)
        enr.raise_for_status()
        enrichment = enr.json()
    except Exception:
        enrichment = {}

    # Merge summary + enrichment; enrichment keys win on conflict
    fort = {**fort_summary, **enrichment}
    return render(request, "map_app/port_detail.html", {"fort": fort})
