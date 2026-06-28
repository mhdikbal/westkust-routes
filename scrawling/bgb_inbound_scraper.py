"""
================================================================================
  BGB INBOUND SCRAPER — Batavia → Sumatera Westkust
  Sumber: resources.huygens.knaw.nl/bgb

  GAP yang diisi:
    Dataset existing (Data_BGS_Sumatra_Full.json) hanya punya voyage OUTBOUND
    (berangkat DARI Sumatera ke Batavia). Script ini mengambil voyage INBOUND
    (berangkat DARI Batavia ke port-port Sumatera).

  TOTAL TARGET: ~375 voyage (berdasarkan recon 24 Jun 2026)
    Batavia → Padang         139
    Batavia → Palembang      154
    Batavia → Jambi           42
    Batavia → Pulau Cingkuak  21
    Batavia → Air Haji        11
    Batavia → Barus            4
    Batavia → Air Bangis       2
    Batavia → Lampung          2

  OUTPUT: scrawling/Data_BGS_Inbound_Full.json
    Format identik dengan Data_BGS_Sumatra_Full.json (kompatibel seed_data.py)

  CARA PAKAI:
    python3 scrawling/bgb_inbound_scraper.py
    # atau dari root project:
    python3 -m scrawling.bgb_inbound_scraper

  Setelah selesai, merge ke dataset utama:
    python3 scrawling/merge_inbound.py
================================================================================
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from datetime import datetime
from typing import Optional

# ── Konfigurasi ───────────────────────────────────────────────────────────────
BASE_URL   = "https://resources.huygens.knaw.nl"
SEARCH_URL = f"{BASE_URL}/bgb/voyages_results"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept":          "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "nl,en;q=0.8",
    "Referer":         f"{BASE_URL}/bgb/search",
}

PAGE_SIZE   = 40      # BGB menampilkan 40 hasil per halaman
DELAY_DETIK = 2.0     # jeda antar request
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "Data_BGS_Inbound_Full.json")
CHECKPOINT  = os.path.join(os.path.dirname(__file__), "bgb_inbound_checkpoint.json")

# ── Matrix rute inbound yang akan di-scrape ───────────────────────────────────
# dep = Batavia (861), arr = masing-masing port Sumatera
ROUTE_MATRIX = [
    {
        "dep_id": "861", "dep_name": "Batavia",
        "dep_lat": -6.1165019, "dep_lon": 106.8165121, "dep_wilayah": "Jawa Barat",
        "arr_id": "851", "arr_name": "Palembang", "expected": 154,
    },
    {
        "dep_id": "861", "dep_name": "Batavia",
        "dep_lat": -6.1165019, "dep_lon": 106.8165121, "dep_wilayah": "Jawa Barat",
        "arr_id": "926", "arr_name": "Padang", "expected": 139,
    },
    {
        "dep_id": "861", "dep_name": "Batavia",
        "dep_lat": -6.1165019, "dep_lon": 106.8165121, "dep_wilayah": "Jawa Barat",
        "arr_id": "850", "arr_name": "Jambi", "expected": 42,
    },
    {
        "dep_id": "861", "dep_name": "Batavia",
        "dep_lat": -6.1165019, "dep_lon": 106.8165121, "dep_wilayah": "Jawa Barat",
        "arr_id": "858", "arr_name": "Pulau Cingkuak", "expected": 21,
    },
    {
        "dep_id": "861", "dep_name": "Batavia",
        "dep_lat": -6.1165019, "dep_lon": 106.8165121, "dep_wilayah": "Jawa Barat",
        "arr_id": "854", "arr_name": "Air Haji", "expected": 11,
    },
    {
        "dep_id": "861", "dep_name": "Batavia",
        "dep_lat": -6.1165019, "dep_lon": 106.8165121, "dep_wilayah": "Jawa Barat",
        "arr_id": "855", "arr_name": "Barus", "expected": 4,
    },
    {
        "dep_id": "861", "dep_name": "Batavia",
        "dep_lat": -6.1165019, "dep_lon": 106.8165121, "dep_wilayah": "Jawa Barat",
        "arr_id": "856", "arr_name": "Air Bangis", "expected": 2,
    },
    {
        "dep_id": "861", "dep_name": "Batavia",
        "dep_lat": -6.1165019, "dep_lon": 106.8165121, "dep_wilayah": "Jawa Barat",
        "arr_id": "948", "arr_name": "Lampung", "expected": 2,
    },
]

# ── Sistem timbang VOC ────────────────────────────────────────────────────────
GRAM_PER_MARK  = 230.4
LOOD_PER_MARK  = 16
QUENT_PER_MARK = 64

BULAN_NL = {
    "januari":1,"februari":2,"maart":3,"april":4,"mei":5,"juni":6,
    "juli":7,"augustus":8,"september":9,"oktober":10,"november":11,"december":12,
    "jan":1,"feb":2,"mrt":3,"apr":4,"aug":8,"sep":9,"okt":10,"nov":11,"dec":12,
    "january":1,"february":2,"march":3,"may":5,"june":6,"july":7,
    "august":8,"october":10,
}


# ── Helpers: identik dengan bgb_sumatra_scraper.py ───────────────────────────

def parse_tanggal(teks: str) -> dict:
    if not teks or teks.strip() in ("-", "—", "?", ""):
        return {"hari": None, "bulan": None, "tahun": None, "iso": None}
    t = teks.strip()
    m = re.match(r'^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$', t)
    if m:
        d, mo, yr = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return {"hari": d, "bulan": mo, "tahun": yr, "iso": f"{yr:04d}-{mo:02d}-{d:02d}"}
    m = re.match(r'^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$', t)
    if m:
        d = int(m.group(1)); mn = m.group(2).lower(); yr = int(m.group(3))
        mo = BULAN_NL.get(mn, 0)
        return {"hari": d, "bulan": mo or None, "tahun": yr,
                "iso": f"{yr:04d}-{mo:02d}-{d:02d}" if mo else f"{yr:04d}"}
    m = re.match(r'^([A-Za-z]+)\s+(\d{4})$', t)
    if m:
        mn = m.group(1).lower(); yr = int(m.group(2)); mo = BULAN_NL.get(mn, 0)
        return {"hari": None, "bulan": mo or None, "tahun": yr,
                "iso": f"{yr:04d}-{mo:02d}" if mo else f"{yr:04d}"}
    m = re.match(r'^(\d{4})$', t)
    if m:
        return {"hari": None, "bulan": None, "tahun": int(m.group(1)), "iso": m.group(1)}
    m = re.search(r'\b(1[5-9]\d{2}|[12]\d{3})\b', t)
    if m:
        return {"hari": None, "bulan": None, "tahun": int(m.group(1)), "iso": m.group(1)}
    return {"hari": None, "bulan": None, "tahun": None, "iso": None, "raw": t}


def parse_gulden(teks: str) -> float:
    if not teks or str(teks).strip() in ("", "-", "—", "nan"):
        return 0.0
    parts = str(teks).strip().replace(".", "").split(",")
    try:
        g = float(parts[0]) if parts[0] else 0.0
        s = float(parts[1]) / 20.0  if len(parts) > 1 and parts[1] else 0.0
        p = float(parts[2]) / 320.0 if len(parts) > 2 and parts[2] else 0.0
        return round(g + s + p, 4)
    except (ValueError, IndexError):
        return 0.0


def find_field(soup: BeautifulSoup, *keywords: str) -> str:
    keywords_l = [k.lower() for k in keywords]
    for el in soup.find_all(["th", "td", "dt", "label", "b", "strong", "h3", "h4"]):
        txt = el.get_text(strip=True).lower()
        if all(k in txt for k in keywords_l):
            sdr = el.find_next_sibling(["td", "dd", "span"])
            if sdr:
                v = sdr.get_text(strip=True)
                if v and v not in ("-", ""):
                    return v
            parent = el.parent
            if parent:
                cells = parent.find_all(["td", "th"])
                for i, c in enumerate(cells):
                    if c == el and i + 1 < len(cells):
                        v = cells[i + 1].get_text(strip=True)
                        if v and v not in ("-", ""):
                            return v
    return ""


def parse_voyage_detail(url: str, route: dict) -> Optional[dict]:
    """Fetch & parse satu halaman detail voyage dari BGB."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=25)
        r.raise_for_status()
    except Exception as e:
        print(f"    [!] Gagal fetch: {url} — {e}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    teks = soup.get_text(separator=" ")

    # Ship name
    nama_kapal = ""
    for sel in ["h1", "h2", "h3"]:
        el = soup.select_one(sel)
        if el:
            nama_kapal = el.get_text(strip=True)
            break
    if not nama_kapal:
        nama_kapal = (find_field(soup, "ship", "name") or
                      find_field(soup, "naam") or "")

    # Captain, tonnage
    kapten = (find_field(soup, "captain") or find_field(soup, "schipper") or
              find_field(soup, "gezagvoerder"))
    tonaj  = (find_field(soup, "tonnage") or find_field(soup, "last") or
              find_field(soup, "grootte"))

    # Dates
    tgl_brgkt_raw = (find_field(soup, "departure", "date") or
                     find_field(soup, "vertrek", "datum") or
                     find_field(soup, "vertrek"))
    tgl_tiba_raw  = (find_field(soup, "arrival", "date") or
                     find_field(soup, "aankomst", "datum") or
                     find_field(soup, "aankomst"))
    tgl_brgkt = parse_tanggal(tgl_brgkt_raw)
    tgl_tiba  = parse_tanggal(tgl_tiba_raw)

    # Book year fallback
    tahun_buku_raw  = (find_field(soup, "book", "year") or find_field(soup, "boek", "jaar"))
    tahun_buku_info = parse_tanggal(tahun_buku_raw)

    if not tgl_brgkt["tahun"]:
        for pola in [r"[Bb]oekjaar\s*[:\-]?\s*(\d{4})", r"(\d{4})"]:
            m = re.search(pola, teks)
            if m:
                yr = int(m.group(1))
                if 1595 <= yr <= 1800:
                    tgl_brgkt["tahun"] = yr
                    break

    # Arrival place from detail page (validate it matches expected destination)
    tujuan_raw = (find_field(soup, "arrival", "place") or
                  find_field(soup, "aankomst", "plaats") or
                  find_field(soup, "destination") or
                  route["arr_name"])

    # Voyage ID
    m_id = re.search(r"/voyage/(\d+)", url)
    voyage_id = int(m_id.group(1)) if m_id else None

    # Cargo
    kargo_list   = []
    semua_produk = set()
    total_gulden = 0.0
    produk_utama = ""
    max_gulden   = 0.0

    for tabel in soup.find_all("table"):
        baris_semua = tabel.find_all("tr")
        header_row  = baris_semua[0] if baris_semua else None
        header_txt  = header_row.get_text(" ").lower() if header_row else ""
        is_kargo    = any(k in header_txt for k in ["product", "goods", "cargo", "koopman"])

        for baris in (baris_semua[1:] if is_kargo else baris_semua):
            sel = baris.find_all(["td", "th"])
            if len(sel) < 3:
                continue
            qty_txt  = sel[0].get_text(strip=True) if len(sel) > 0 else ""
            unit_txt = sel[1].get_text(strip=True) if len(sel) > 1 else ""
            prod_txt = sel[2].get_text(strip=True) if len(sel) > 2 else ""
            spec_txt = sel[3].get_text(strip=True) if len(sel) > 3 else ""
            val_nl   = sel[4].get_text(strip=True) if len(sel) > 4 else ""
            val_in   = sel[5].get_text(strip=True) if len(sel) > 5 else ""

            if not prod_txt or prod_txt.lower() in ("product", "goods", ""):
                continue

            g_nl = parse_gulden(val_nl)
            g_in = parse_gulden(val_in)
            g_used = g_nl if g_nl > 0 else g_in
            total_gulden += g_used

            # Quantity (simplified — no gram conversion needed for inbound)
            try:
                qty_num = float(re.sub(r"[^\d.]", "", qty_txt.replace(",", "."))) if qty_txt else 0.0
            except ValueError:
                qty_num = 0.0

            kargo_list.append({
                "produk":        prod_txt,
                "spesifikasi":   spec_txt,
                "qty_asli":      qty_txt,
                "unit":          unit_txt,
                "nilai_numerik": round(qty_num, 4),
                "gram":          0.0,
                "gulden_nl":     g_nl,
                "gulden_india":  g_in,
                "gulden_used":   g_used,
                "catatan":       "",
            })

            produk_bersih = prod_txt.strip().lower()
            if produk_bersih:
                semua_produk.add(produk_bersih)
            if g_used > max_gulden:
                max_gulden   = g_used
                produk_utama = prod_txt

    # Duration
    durasi_hari = None
    if (tgl_brgkt.get("iso") and tgl_tiba.get("iso") and
            len(tgl_brgkt["iso"]) == 10 and len(tgl_tiba["iso"]) == 10):
        try:
            db   = datetime.fromisoformat(tgl_brgkt["iso"])
            dt   = datetime.fromisoformat(tgl_tiba["iso"])
            diff = (dt - db).days
            if 0 < diff < 3000:
                durasi_hari = diff
        except Exception:
            pass

    return {
        "ID":              voyage_id,
        "URL":             url,
        "Nama_Kapal":      nama_kapal or "Tidak diketahui",
        "Kapten":          kapten or None,
        "Tonaj":           tonaj or None,

        # Asal = Batavia (departure), Tujuan = port Sumatera (arrival)
        "Asal":            route["dep_name"],
        "Asal_ID":         route["dep_id"],
        "Asal_Lat":        route["dep_lat"],
        "Asal_Lon":        route["dep_lon"],
        "Wilayah":         route["dep_wilayah"],
        "Tujuan":          tujuan_raw,

        "Tahun_Buku":      tahun_buku_info.get("tahun"),
        "Tahun":           tgl_brgkt.get("tahun") or tgl_tiba.get("tahun") or tahun_buku_info.get("tahun"),
        "Tgl_Berangkat":   tgl_brgkt,
        "Tgl_Tiba":        tgl_tiba,
        "Durasi_Hari":     durasi_hari,

        "Produk_Utama":    produk_utama or (list(semua_produk)[0] if semua_produk else ""),
        "Semua_Produk":    " | ".join(sorted(semua_produk)),
        "Total_Gulden_NL": round(total_gulden, 4),
        "Jumlah_Item_Kargo": len(kargo_list),
        "Kargo":           kargo_list,

        "Direction":       "inbound",
        "Scraped_At":      datetime.utcnow().isoformat() + "Z",
    }


def crawl_route_urls(route: dict) -> list:
    """Ambil semua voyage URL untuk satu pasangan (dep_id, arr_id)."""
    urls = []
    seen = set()
    start = 0
    label = f"{route['dep_name']} → {route['arr_name']}"

    print(f"\n  Crawling: {label} (ekspektasi ~{route['expected']} voyage)")

    while True:
        params = {
            "group_by_all":       "on",
            "departure_place_id": route["dep_id"],
            "arrival_place_id":   route["arr_id"],
            "booking_year_from":  "1700",
            "booking_year_to":    "1789",
            "start":              start,
        }
        try:
            r = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=25)
            r.raise_for_status()
        except Exception as e:
            print(f"    [!] Gagal page start={start}: {e}")
            break

        soup = BeautifulSoup(r.text, "html.parser")

        # Count total from header (only first page)
        if start == 0:
            m = re.search(r'Total results:\s*<b>(\d+)</b>', r.text)
            total_count = int(m.group(1)) if m else "?"
            print(f"    Total di BGB: {total_count}")

        # Collect voyage URLs from this page
        baru = 0
        for a in soup.find_all("a", href=True):
            if re.search(r"/bgb/voyage/\d+$", a["href"]):
                u = a["href"] if a["href"].startswith("http") else BASE_URL + a["href"]
                if u not in seen:
                    seen.add(u)
                    urls.append(u)
                    baru += 1

        print(f"    start={start} | +{baru} baru | total: {len(urls)}")

        # Check for "next" link
        nxt = soup.find("a", string=re.compile(r"next", re.I))
        if not nxt:
            break

        start += PAGE_SIZE
        time.sleep(DELAY_DETIK)

    return urls


def simpan_checkpoint(data: list, done_urls: set, route_idx: int):
    with open(CHECKPOINT, "w", encoding="utf-8") as f:
        json.dump({
            "data":      data,
            "done_urls": list(done_urls),
            "route_idx": route_idx,
        }, f, ensure_ascii=False)


def muat_checkpoint():
    if os.path.exists(CHECKPOINT):
        with open(CHECKPOINT, encoding="utf-8") as f:
            d = json.load(f)
        print(f"[RESUME] {len(d['data'])} voyage dari checkpoint, rute ke-{d['route_idx']}.")
        return d["data"], set(d["done_urls"]), d["route_idx"]
    return [], set(), 0


def main():
    print("=" * 72)
    print("  BGB INBOUND SCRAPER — Batavia → Sumatera Westkust")
    print(f"  Output: {OUTPUT_FILE}")
    print(f"  Delay: {DELAY_DETIK}s per request")
    print("=" * 72)

    semua_data, done_urls, start_route_idx = muat_checkpoint()

    for i, route in enumerate(ROUTE_MATRIX):
        if i < start_route_idx:
            print(f"  [SKIP] Rute {i}: {route['dep_name']} → {route['arr_name']} (sudah di-scrape)")
            continue

        label = f"{route['dep_name']} → {route['arr_name']}"
        print(f"\n{'─'*72}")
        print(f"[RUTE {i+1}/{len(ROUTE_MATRIX)}] {label}")
        print(f"{'─'*72}")

        urls = crawl_route_urls(route)
        urls_baru = [u for u in urls if u not in done_urls]
        print(f"  → {len(urls_baru)} voyage baru (skip {len(urls)-len(urls_baru)} duplikat)")

        for j, url in enumerate(urls_baru):
            detail = parse_voyage_detail(url, route)
            if detail:
                semua_data.append(detail)
                done_urls.add(url)

            if (j + 1) % 5 == 0 or (j + 1) == len(urls_baru):
                print(f"  [{j+1}/{len(urls_baru)}] total: {len(semua_data)} voyage")
                simpan_checkpoint(semua_data, done_urls, i)

            time.sleep(DELAY_DETIK)

        simpan_checkpoint(semua_data, done_urls, i + 1)

    # ── Output final ──────────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    semua_data.sort(key=lambda x: (x.get("Tahun") or 9999, x.get("ID") or 0))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(semua_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Disimpan: {OUTPUT_FILE}")
    print(f"[+] Total: {len(semua_data)} voyage inbound")

    if os.path.exists(CHECKPOINT):
        os.remove(CHECKPOINT)

    # Ringkasan per rute
    from collections import Counter
    per_tujuan = Counter(d["Tujuan"] for d in semua_data)
    print(f"\n{'─'*72}\nRINGKASAN PER TUJUAN")
    for nama, jml in per_tujuan.most_common():
        print(f"  {nama:25s}: {jml:4d} voyage")

    total_gulden = sum(d.get("Total_Gulden_NL", 0) for d in semua_data)
    print(f"\n  Total nilai (gulden): ƒ{total_gulden:,.0f}")
    print("\n[DONE] Scraping inbound selesai.")


if __name__ == "__main__":
    main()
