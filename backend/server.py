from fastapi import FastAPI, APIRouter, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class Voyage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asal: str
    tujuan: str
    nama_kapal: str
    kapten: Optional[str] = ""
    tahun: int
    total_gulden_nl: float
    produk_utama: str
    semua_produk: str
    durasi_hari: Optional[int] = None
    warna_asal: str
    url: str


class VoyageStats(BaseModel):
    total_voyages: int
    total_cargo_value: float
    year_range: dict
    ports: dict
    top_products: List[dict]


# Voyage endpoints
@api_router.get("/")
async def root():
    return {"message": "Westkust Maritime Routes API"}


@api_router.get("/voyages", response_model=List[Voyage])
async def get_voyages(
    year_from: Optional[int] = Query(None),
    year_to: Optional[int] = Query(None),
    port: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    query = {}
    
    if year_from or year_to:
        query["tahun"] = {}
        if year_from:
            query["tahun"]["$gte"] = year_from
        if year_to:
            query["tahun"]["$lte"] = year_to
    
    if port:
        query["asal"] = port
    
    if search:
        query["nama_kapal"] = {"$regex": search, "$options": "i"}
    
    voyages = await db.voyages.find(query, {"_id": 0}).to_list(1000)
    return voyages


@api_router.get("/voyages/stats", response_model=VoyageStats)
async def get_voyage_stats(
    year_from: Optional[int] = Query(None),
    year_to: Optional[int] = Query(None)
):
    query = {}
    if year_from or year_to:
        query["tahun"] = {}
        if year_from:
            query["tahun"]["$gte"] = year_from
        if year_to:
            query["tahun"]["$lte"] = year_to
    
    voyages = await db.voyages.find(query, {"_id": 0}).to_list(10000)
    
    total_voyages = len(voyages)
    total_cargo = sum(v["total_gulden_nl"] for v in voyages)
    
    years = [v["tahun"] for v in voyages]
    year_range = {
        "min": min(years) if years else 0,
        "max": max(years) if years else 0
    }
    
    ports = {}
    for v in voyages:
        port = v["asal"]
        if port not in ports:
            ports[port] = {"count": 0, "value": 0}
        ports[port]["count"] += 1
        ports[port]["value"] += v["total_gulden_nl"]
    
    product_counts = {}
    for v in voyages:
        product = v["produk_utama"]
        if product not in product_counts:
            product_counts[product] = 0
        product_counts[product] += 1
    
    top_products = [
        {"name": k, "count": v}
        for k, v in sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    
    return VoyageStats(
        total_voyages=total_voyages,
        total_cargo_value=total_cargo,
        year_range=year_range,
        ports=ports,
        top_products=top_products
    )


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()