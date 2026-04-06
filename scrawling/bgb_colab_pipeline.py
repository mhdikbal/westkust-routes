"""
================================================================================
  BGB SUMATRA PIPELINE — GOOGLE COLAB NOTEBOOK
  Jalankan sel-sel ini secara berurutan di Google Colab

  Alur:
    1. Install dependencies
    2. Upload / clone scraper
    3. Jalankan scraping
    4. Lihat preview & statistik
    5. Download hasil JSON
================================================================================
"""

# %% [markdown]
# # 🗺️ BGB Sumatra Scraper — Pipeline ke `Data_BGS_Sumatra_Full.json`
# **Sumber:** https://resources.huygens.knaw.nl/bgb/search
#
# Data yang dikumpulkan:
# - Nama kapal, kapten, tonaj
# - **Tanggal lengkap** (hari, bulan, tahun) keberangkatan & kedatangan
# - **Detail kargo** per item: produk, kuantitas, unit, nilai gulden
# - Semua pos Sumatera: Padang, Pulau Cingkuak, Air Haji, Jambi, Palembang

# %% [markdown]
# ## Sel 1 — Install dependencies

# %%
# !pip install requests beautifulsoup4 pandas lxml -q

# %% [markdown]
# ## Sel 2 — Upload scraper
# Atau clone dari GitHub:

# %%
# Clone dari repo (otomatis terhubung ke branch terbaru)
!git clone --branch scrapping --depth 1 \
    https://github.com/mhdikbal/westkust-routes.git westkust
import sys; sys.path.insert(0, "westkust/scrawling")

# %% [markdown]
# ## Sel 3 — Konfigurasi & Jalankan

# %%
# Sesuaikan konfigurasi di sini sebelum run

CONFIG = {
    # Tempat berangkat yang ingin di-scrape
    # Format: { "ID": ("Nama", lat, lon, "Wilayah", "Keterangan") }
    # ID dari dropdown di https://resources.huygens.knaw.nl/bgb/search
    "TARGET_PORTS": {
        "926": ("Padang",         -0.9655545,  100.353889, "Sumatera Barat", "Fort de Goede Hoop"),
        "858": ("Pulau Cingkuak", -1.352837,   100.559995, "Sumatera Barat", "Pulau Tjinkuk"),
        "854": ("Air Haji",       -1.933939,   100.866982, "Sumatera Barat", "Airhadji"),
        "856": ("Air Bangis",      0.1974875,   99.375555, "Sumatera Barat", "Airbangis"),
        "855": ("Barus",           2.0144566,   98.399319, "Sumatera Utara", "Baros"),
        "850": ("Jambi",          -1.0984482,  104.175717, "Sumatera Tengah", "Jambi"),
        "851": ("Palembang",      -3.0029119,  104.780189, "Sumatera Selatan", "Palembang"),
        "948": ("Lampung",        -5.3578004,  105.280386, "Sumatera Selatan", "Lampong Toulang Bawang"),
        "861": ("Batavia",        -6.133649,   106.816666, "Jawa Barat", "Batavia"),
    },
    # None = ambil semua komoditi, atau: "goud", "peper", "kamfer"
    "PRODUCT_FILTER":     None,
    # Batas halaman per tempat (10 voyage/halaman). 999 = ambil semua
    "MAX_PAGES_PER_PLACE": 200,
    # Jeda antar request (detik) — jangan terlalu cepat!
    "DELAY_DETIK": 1.5,
    "OUTPUT_FILE": "Data_BGS_Sumatra_Full.json",
}

print("Konfigurasi siap.")
print(f"Tempat: {[v[0] for v in CONFIG['TARGET_PORTS'].values()]}")
print(f"Produk filter: {CONFIG['PRODUCT_FILTER'] or 'semua'}")

# %% [markdown]
# ## Sel 4 — Jalankan Scraper

# %%
import sys, importlib

# Patch konfigurasi ke modul scraper
import bgb_sumatra_scraper as scraper

scraper.SUMATRA_PORTS      = CONFIG["TARGET_PORTS"]
scraper.PRODUCT_FILTER     = CONFIG["PRODUCT_FILTER"]
scraper.MAX_PAGES_PER_PLACE= CONFIG["MAX_PAGES_PER_PLACE"]
scraper.DELAY_DETIK        = CONFIG["DELAY_DETIK"]
scraper.OUTPUT_FILE        = CONFIG["OUTPUT_FILE"]

scraper.main()

# %% [markdown]
# ## Sel 5 — Preview & Statistik

# %%
import json, pandas as pd

with open(CONFIG["OUTPUT_FILE"], encoding="utf-8") as f:
    data = json.load(f)

print(f"Total voyage: {len(data)}")

# Flatten ke DataFrame (ringkasan tanpa kargo detail)
rows = []
for d in data:
    rows.append({
        "ID":            d.get("ID"),
        "Nama_Kapal":    d.get("Nama_Kapal"),
        "Kapten":        d.get("Kapten"),
        "Asal":          d.get("Asal"),
        "Wilayah":       d.get("Wilayah"),
        "Tujuan":        d.get("Tujuan"),
        "Tahun":         d.get("Tahun"),
        "Bulan":         d["Tgl_Berangkat"].get("bulan") if d.get("Tgl_Berangkat") else None,
        "Hari":          d["Tgl_Berangkat"].get("hari")  if d.get("Tgl_Berangkat") else None,
        "Tgl_Iso_Brgkt": d["Tgl_Berangkat"].get("iso")  if d.get("Tgl_Berangkat") else None,
        "Tgl_Iso_Tiba":  d["Tgl_Tiba"].get("iso")       if d.get("Tgl_Tiba")      else None,
        "Durasi_Hari":   d.get("Durasi_Hari"),
        "Produk_Utama":  d.get("Produk_Utama"),
        "Semua_Produk":  d.get("Semua_Produk"),
        "Total_Gulden":  d.get("Total_Gulden_NL"),
        "Jml_Item_Kargo":d.get("Jumlah_Item_Kargo"),
        "URL":           d.get("URL"),
    })

df = pd.DataFrame(rows)
print(df.dtypes)
print(df.head(5))

# %% [markdown]
# ### Statistik per Asal

# %%
print(df.groupby("Asal").agg(
    Voyage      = ("ID",           "count"),
    Tahun_Min   = ("Tahun",        "min"),
    Tahun_Max   = ("Tahun",        "max"),
    Gulden_Total= ("Total_Gulden", "sum"),
    Gulden_Rata = ("Total_Gulden", "mean"),
).round(0))

# %% [markdown]
# ### Top Komoditi

# %%
from collections import Counter
produk_all = []
for d in data:
    produk_all += [p.strip() for p in d.get("Semua_Produk","").split("|") if p.strip()]
for p, c in Counter(produk_all).most_common(15):
    print(f"  {p:30s}: {c:5d}×")

# %% [markdown]
# ### Timeline: Voyage per Tahun

# %%
import matplotlib.pyplot as plt
df_year = df.groupby("Tahun").size().reset_index(name="count")
fig, ax = plt.subplots(figsize=(14, 4))
ax.bar(df_year["Tahun"], df_year["count"], color="#B85D19", alpha=.8, width=.9)
ax.set_xlabel("Tahun"); ax.set_ylabel("Jumlah Voyage")
ax.set_title("Voyage dari Sumatera (semua pos) per Tahun — BGB Huygens")
plt.tight_layout(); plt.show()

# %% [markdown]
# ### Kelengkapan Tanggal

# %%
print("Kelengkapan data tanggal:")
print(f"  Punya tahun : {df['Tahun'].notna().sum():5d} / {len(df)}")
print(f"  Punya bulan : {df['Bulan'].notna().sum():5d} / {len(df)}")
print(f"  Punya hari  : {df['Hari'].notna().sum():5d} / {len(df)}")
print(f"  Punya durasi: {df['Durasi_Hari'].notna().sum():5d} / {len(df)}")

# %% [markdown]
# ## Sel 6 — Download file hasil

# %%
from google.colab import files
files.download(CONFIG["OUTPUT_FILE"])
files.download("bgb_checkpoint.json")  # jika ada (proses belum selesai)
