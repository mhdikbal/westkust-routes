FROM python:3.11-slim

WORKDIR /app

# deps (django, requests, whitenoise, gunicorn, httpx) semua pure-Python/wheel
# → gcc tak perlu, dihapus.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8001
