import os
import httpx
from django.shortcuts import render
from django.http import Http404

API_BASE = os.getenv("API_BASE_URL", "http://voc_backend:8000")


def index(request):
    """Main map page — VOC Trade Atlas."""
    return render(request, "map_app/index.html")


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
