import os
from django.conf import settings
from django.http import HttpResponse

def index(request):
    """Main map page."""
    build_path = os.path.join(settings.BASE_DIR, 'build', 'index.html')
    try:
        with open(build_path, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        return HttpResponse(f"React build not found at {build_path}. Please run npm run build", status=501)
