import os
import httpx
from django.shortcuts import render
from django.http import Http404

API_BASE = os.getenv("API_BASE_URL", "http://voc_backend:8000")


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
    Painan 1663 (thesis-only, top-level /linimasa). Halaman statis: linimasa
    ditarik client-side dari /api/research/linimasa (nginx proxy). noindex +
    tidak di navbar publik (konsisten /riset/tema, /riset/jaringan,
    /riset/atjeh-dagang). Identitas visual salido.my.id (EB Garamond + Space
    Grotesk)."""
    return render(request, "map_app/linimasa.html")


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
