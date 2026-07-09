import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routers import forts, voyages, glossary, staging, research

# Baca ALLOWED_ORIGINS dari env var, parse sebagai comma-separated list.
# Default: hanya Nginx entry point. Tambahkan origin lain via env var di .env.
_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:8084")
ALLOWED_ORIGINS = [o.strip() for o in _origins_raw.split(",") if o.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="VOC Sumatera Westkust API",
    description="API untuk data jalur perdagangan VOC di Sumatera Barat",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,   # tidak ada cookie/session — sesuai temuan audit
    allow_methods=["GET", "OPTIONS"],  # API read-only; OPTIONS wajib untuk preflight
    allow_headers=["*"],
)

app.include_router(forts.router, prefix="/api/forts", tags=["Forts"])
app.include_router(voyages.router, prefix="/api/voyages", tags=["Voyages"])
app.include_router(glossary.router, prefix="/api/glossary", tags=["Glossary"])
app.include_router(staging.router, prefix="/api/staging", tags=["Staging (internal)"])
app.include_router(research.router, prefix="/api/research", tags=["Research (thesis-only)"])


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "VOC Westkust API"}
