from django.shortcuts import render
from django.conf import settings


def index(request):
    """Main map page."""
    return render(request, "map_app/index.html", {
        "api_base_url": "/api",  # Via nginx proxy
    })
