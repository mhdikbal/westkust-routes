FROM python:3.11-slim

WORKDIR /app

# Semua dependency (asyncpg, psycopg2-binary, geoalchemy2, uvicorn[standard])
# punya wheel manylinux / pure-Python → tak butuh gcc/libpq-dev. GDAL tak pernah
# di-import kode (geoalchemy2 pure-Python; kerja spasial di container postgis),
# jadi apt-get gdal/build-tools (dulu ~1.12GB) DIHAPUS. psycopg2-binary sudah
# membundel libpq. Image turun 1.78GB → ~270MB.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
