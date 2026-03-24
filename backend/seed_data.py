import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_voyages():
    # Load data from JSON file
    json_file = ROOT_DIR / 'voyages_data.json'
    
    with open(json_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # Transform data to match our schema
    voyages_data = []
    for idx, item in enumerate(raw_data):
        voyage = {
            "id": f"voyage-{item.get('Tahun', 0)}-{idx}",
            "asal": item.get("Asal", ""),
            "tujuan": item.get("Tujuan", ""),
            "nama_kapal": item.get("Nama_Kapal", ""),
            "kapten": item.get("Kapten", ""),
            "tahun": item.get("Tahun", 0),
            "total_gulden_nl": item.get("Total_Gulden_NL", 0.0),
            "produk_utama": item.get("Produk_Utama", ""),
            "semua_produk": item.get("Semua_Produk", ""),
            "durasi_hari": item.get("Durasi_Hari"),
            "warna_asal": item.get("Warna_Asal", "#c0392b"),
            "url": item.get("URL", "")
        }
        voyages_data.append(voyage)
    
    # Clear existing data
    await db.voyages.delete_many({})
    
    # Insert new data
    if voyages_data:
        await db.voyages.insert_many(voyages_data)
        print(f"✅ Seeded {len(voyages_data)} voyages successfully!")
        
        # Print summary
        years = [v["tahun"] for v in voyages_data]
        ports = set(v["asal"] for v in voyages_data)
        total_value = sum(v["total_gulden_nl"] for v in voyages_data)
        
        print(f"📊 Summary:")
        print(f"  - Period: {min(years)} - {max(years)}")
        print(f"  - Ports: {', '.join(sorted(ports))}")
        print(f"  - Total Cargo Value: {total_value:,.2f} Gulden")
    else:
        print("⚠️ No voyages data to seed")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_voyages())