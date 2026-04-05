from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routers import forts, voyages


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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forts.router, prefix="/api/forts", tags=["Forts"])
app.include_router(voyages.router, prefix="/api/voyages", tags=["Voyages"])


@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "VOC Westkust API"}
