"""
================================================================================
  BGB SUMATRA COMPREHENSIVE SCRAPER
  Sumber: resources.huygens.knaw.nl/bgb

  CAKUPAN:
    - Semua pos keberangkatan di Sumatera (Padang, Pulau Cingkuak/Tjinkuk,
      Air Haji/Airhadji, Jambi, Palembang, Aceh*)
    - Semua komoditi (goud, peper, kamfer, benzoin, lak, tin, sagu, kopi, dst.)
    - Tanggal LENGKAP: hari, bulan, tahun keberangkatan & kedatangan
    - Detail kargo per voyage: setiap item besok produk, unit, kuantitas, nilai
    - Output JSON siap pipeline → Data_Westkust_Map.json / PostgreSQL / peta

  CARA PAKAI (Google Colab):
    1. Upload file ini ke Colab atau paste kontennya
    2. !pip install requests beautifulsoup4 pandas lxml
    3. Jalankan: python bgb_sumatra_scraper.py
    4. Download hasil: Data_BGS_Sumatra_Full.json

  KONFIGURASI:
    - DEPARTURE_PLACES: tambah/kurangi ID tempat sesuai kebutuhan
    - MAX_PAGES_PER_PLACE: batas halaman per tempat (50 = ~500 voyage)
    - DELAY_DETIK: jeda antar request (hormati server Huygens)
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

# ── Konfigurasi ──────────────────────────────────────────────────────────────

BASE_URL   = "https://resources.huygens.knaw.nl"
SEARCH_URL = f"{BASE_URL}/bgb/voyages_results"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "nl,en;q=0.8",
    "Referer":         f"{BASE_URL}/bgb/search",
}

# ── Pos pelabuhan di Sumatera ────────────────────────────────────────────────
# Format: { "ID": ("Nama tampil", lat, lon, "wilayah", "keterangan") }
# Kita akan scrape kapal yang berangkat DARI atau tiba DI pos-pos berikut.
SUMATRA_PORTS = {
    "926":  ("Padang",         -0.9655545,  100.353889, "Sumatera Barat", "Fort de Goede Hoop"),
    "858":  ("Pulau Cingkuak", -1.352837,   100.559995, "Sumatera Barat", "Pulau Tjinkuk"),
    "854":  ("Air Haji",       -1.933939,   100.866982, "Sumatera Barat", "Airhadji"),
    "856":  ("Air Bangis",      0.1974875,   99.375555, "Sumatera Barat", "Airbangis"),
    "855":  ("Barus",           2.0144566,   98.399319, "Sumatera Utara", "Baros"),
    "850":  ("Jambi",          -1.0984482,  104.175717, "Sumatera Tengah","Jambi"),
    "851":  ("Palembang",      -3.0029119,  104.780189, "Sumatera Selatan","Palembang"),
    "948":  ("Lampung",        -5.3578004,  105.280386, "Sumatera Selatan","Lampong Toulang Bawang"),
    "861":  ("Batavia",        -6.133649,   106.816666, "Jawa Barat", "Batavia"),
}

# Komoditi yang ingin dikumpulkan (None = ambil semua)
PRODUCT_FILTER: Optional[str] = None   # contoh: "peper", "goud", None=semua

# Batas halaman per kombinasi (tiap halaman ~10 voyage)
# Naikkan ke 999 untuk ambil semua (bisa lambat)
MAX_PAGES_PER_PLACE = 200

DELAY_DETIK  = 1.5   # jeda antar request — hormati server Huygens
OUTPUT_FILE  = "Data_BGS_Sumatra_Full.json"
CHECKPOINT   = "bgb_checkpoint.json"   # simpan progress agar bisa resume

# ── Sistem timbang GM4 ───────────────────────────────────────────────────────
GRAM_PER_MARK   = 230.4
LOOD_PER_MARK   = 16
QUENT_PER_MARK  = 64
ENGELS_PER_MARK = 160

# Bulan Belanda (VOC) → nomor
BULAN_NL = {
    "januari":1,"februari":2,"maart":3,"april":4,"mei":5,"juni":6,
    "juli":7,"augustus":8,"september":9,"oktober":10,"november":11,"december":12,
    "jan":1,"feb":2,"mrt":3,"apr":4,"aug":8,"sep":9,"okt":10,"nov":11,"dec":12,
    "january":1,"february":2,"march":3,"may":5,"june":6,"july":7,
    "august":8,"september":9,"october":10,"november":11,"december":12,
}


# ── Helper: Parse tanggal BGB ─────────────────────────────────────────────────
def parse_tanggal(teks: str) -> dict:
    """
    Parse tanggal BGB format: "15 Mei 1724", "3-5-1700", "1724", dll.
    Kembalikan dict: { hari, bulan, tahun, iso } atau None.
    """
    if not teks or not teks.strip() or teks.strip() in ("-", "—", "?"):
        return {"hari": None, "bulan": None, "tahun": None, "iso": None}

    t = teks.strip()

    # Format: DD-MM-YYYY atau DD/MM/YYYY
    m = re.match(r'^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$', t)
    if m:
        d, mo, yr = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return {"hari": d, "bulan": mo, "tahun": yr,
                "iso": f"{yr:04d}-{mo:02d}-{d:02d}"}

    # Format: DD MMMM YYYY (Belanda/Inggris)
    m = re.match(r'^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$', t)
    if m:
        d   = int(m.group(1))
        mn  = m.group(2).lower()
        yr  = int(m.group(3))
        mo  = BULAN_NL.get(mn, 0)
        return {"hari": d, "bulan": mo or None, "tahun": yr,
                "iso": f"{yr:04d}-{mo:02d}-{d:02d}" if mo else f"{yr:04d}"}

    # Format: MMMM YYYY
    m = re.match(r'^([A-Za-z]+)\s+(\d{4})$', t)
    if m:
        mn = m.group(1).lower(); yr = int(m.group(2))
        mo = BULAN_NL.get(mn, 0)
        return {"hari": None, "bulan": mo or None, "tahun": yr,
                "iso": f"{yr:04d}-{mo:02d}" if mo else f"{yr:04d}"}

    # Format: YYYY only
    m = re.match(r'^(\d{4})$', t)
    if m:
        return {"hari": None, "bulan": None, "tahun": int(m.group(1)),
                "iso": m.group(1)}

    # Fallback: cari 4 digit tahun
    m = re.search(r'\b(1[5-9]\d{2}|[12]\d{3})\b', t)
    if m:
        return {"hari": None, "bulan": None, "tahun": int(m.group(1)),
                "iso": m.group(1)}

    return {"hari": None, "bulan": None, "tahun": None, "iso": None, "raw": t}


# ── Helper: Parse nilai gulden ────────────────────────────────────────────────
def parse_gulden(teks: str) -> float:
    """
    "11.142,19"  → 11142.95 (gulden + stuiver/20)
    "21.690,9,8" → 21690 + 9/20 + 8/320
    """
    if not teks or teks.strip() in ("", "-", "—", "nan"):
        return 0.0
    parts = str(teks).strip().replace(".", "").split(",")
    try:
        g  = float(parts[0]) if parts[0] else 0.0
        s  = float(parts[1]) / 20.0  if len(parts) > 1 and parts[1] else 0.0
        p  = float(parts[2]) / 320.0 if len(parts) > 2 and parts[2] else 0.0
        return round(g + s + p, 4)
    except (ValueError, IndexError):
        return 0.0


# ── Helper: Parse kuantitas ───────────────────────────────────────────────────
def parse_kuantitas(qty: str, unit: str) -> dict:
    """
    Kembalikan gram (fisik) jika satuannya mark/lood/quent/engels.
    Untuk satuan lain (lb, pond, koyan, pikul, dst.) kembalikan angka asli.
    """
    unit_l = (unit or "").lower()
    hasil  = {"qty_asli": qty, "unit": unit,
              "nilai_numerik": 0.0, "gram": 0.0, "catatan": ""}
    if not qty or qty.strip() in ("", "-", "—"):
        return hasil
    # Bersihkan angka
    bersih = re.sub(r"[^\d,.]", "", qty).replace(".", "").replace(",", ".")
    try:
        num = float(bersih) if bersih else 0.0
    except ValueError:
        hasil["catatan"] = f"Gagal parse: {qty}"
        return hasil

    hasil["nilai_numerik"] = round(num, 4)

    # Konversi ke gram jika satuan VOC berat
    if "mark" in unit_l:
        # format "A,B mark" = A mark + B lood
        parts = qty.split(",")
        try:
            a = float(re.sub(r"[^\d]", "", parts[0])) if parts[0] else 0
            b = float(parts[1]) / LOOD_PER_MARK if len(parts) > 1 and parts[1] else 0
            hasil["gram"] = round((a + b) * GRAM_PER_MARK, 3)
        except:
            hasil["gram"] = round(num * GRAM_PER_MARK, 3)
    elif "lood" in unit_l:
        hasil["gram"] = round(num * (GRAM_PER_MARK / LOOD_PER_MARK), 3)
    elif "quent" in unit_l:
        hasil["gram"] = round(num * (GRAM_PER_MARK / QUENT_PER_MARK), 3)
    elif "engels" in unit_l:
        hasil["gram"] = round(num * (GRAM_PER_MARK / ENGELS_PER_MARK), 3)

    return hasil


# ── Ekstrak field dari label-value HTML ──────────────────────────────────────
def find_field(soup: BeautifulSoup, *keywords: str) -> str:
    """Cari teks di sebelah elemen label yang mengandung keyword."""
    keywords_l = [k.lower() for k in keywords]
    for el in soup.find_all(["th", "td", "dt", "label", "b", "strong", "h3", "h4"]):
        txt = el.get_text(strip=True).lower()
        if all(k in txt for k in keywords_l):
            # Coba sibling
            sdr = el.find_next_sibling(["td", "dd", "span"])
            if sdr:
                v = sdr.get_text(strip=True)
                if v and v not in ("-", ""):
                    return v
            # Coba cell berikutnya
            parent = el.parent
            if parent:
                cells = parent.find_all(["td", "th"])
                for i, c in enumerate(cells):
                    if c == el and i + 1 < len(cells):
                        v = cells[i + 1].get_text(strip=True)
                        if v and v not in ("-", ""):
                            return v
    return ""


# ── Parse halaman detail voyage ───────────────────────────────────────────────
def parse_voyage_detail(url: str, departure_meta: dict) -> Optional[dict]:
    """
    Fetch & parse halaman detail satu voyage.
    Kembalikan dict lengkap atau None jika gagal.
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=25)
        r.raise_for_status()
    except Exception as e:
        print(f"    [!] Gagal fetch: {url} — {e}")
        return None

    soup  = BeautifulSoup(r.text, "html.parser")
    teks  = soup.get_text(separator=" ")

    # ── Identitas kapal ──────────────────────────────────────────────
    nama_kapal = ""
    for sel in ["h1", "h2", "h3", ".ship-name", "#ship-name"]:
        el = soup.select_one(sel)
        if el:
            nama_kapal = el.get_text(strip=True)
            break
    if not nama_kapal:
        nama_kapal = find_field(soup, "ship", "name") or \
                     find_field(soup, "naam") or \
                     find_field(soup, "vessel")

    # Jika tidak ketemu dari field biasa, cari di judul halaman
    if not nama_kapal:
        title = soup.find("title")
        if title:
            nama_kapal = title.get_text(strip=True).split("|")[0].strip()

    # ── Kapten ───────────────────────────────────────────────────────
    kapten = (find_field(soup, "captain") or
              find_field(soup, "schipper") or
              find_field(soup, "commander") or
              find_field(soup, "gezagvoerder"))

    # ── Ukuran kapal ─────────────────────────────────────────────────
    tonaj = (find_field(soup, "tonnage") or
             find_field(soup, "last") or
             find_field(soup, "grootte"))

    # ── Tanggal keberangkatan ────────────────────────────────────────
    tgl_brgkt_raw = (find_field(soup, "departure", "date") or
                     find_field(soup, "vertrek", "datum") or
                     find_field(soup, "departure") or
                     find_field(soup, "vertrek"))
    tgl_brgkt = parse_tanggal(tgl_brgkt_raw)

    # ── Tanggal kedatangan ───────────────────────────────────────────
    tgl_tiba_raw = (find_field(soup, "arrival", "date") or
                    find_field(soup, "aankomst", "datum") or
                    find_field(soup, "arrival") or
                    find_field(soup, "aankomst"))
    tgl_tiba = parse_tanggal(tgl_tiba_raw)

    # ── Fallback tahun via regex ─────────────────────────────────────
    if not tgl_brgkt["tahun"]:
        tahun_fallback = None
        for pola in [
            r"[Bb]oek(?:ing)?jaar\s*[:\-]?\s*(\d{4})",
            r"[Yy]ear\s*[:\-]?\s*(\d{4})",
            r"(\d{4})",
        ]:
            m = re.search(pola, teks)
            if m:
                tahun_fallback = int(m.group(1))
                # Sanity check: tahun VOC
                if 1595 <= tahun_fallback <= 1800:
                    tgl_brgkt["tahun"] = tahun_fallback
                    break

    # ── Tempat tujuan (arrival place) ───────────────────────────────
    tujuan = (find_field(soup, "arrival", "place") or
              find_field(soup, "aankomst", "plaats") or
              find_field(soup, "destination") or
              find_field(soup, "bestemming"))

    # ── Tahun buku (boekjaar) ────────────────────────────────────────
    tahun_buku_raw = (find_field(soup, "book", "year") or
                      find_field(soup, "boek", "jaar"))
    tahun_buku_info = parse_tanggal(tahun_buku_raw)

    # ── Voyage ID dari URL ───────────────────────────────────────────
    m_id = re.search(r"/voyage/(\d+)", url)
    voyage_id = int(m_id.group(1)) if m_id else None

    # ── Kargo: scan semua tabel ──────────────────────────────────────
    kargo_list = []
    semua_produk = set()
    total_gulden = 0.0
    produk_utama = ""
    max_gulden   = 0.0

    for tabel in soup.find_all("table"):
        baris_semua = tabel.find_all("tr")
        # Cek header tabel -- kita cari tabel yang punya kolom "product"
        header_row = baris_semua[0] if baris_semua else None
        header_txt = header_row.get_text(" ").lower() if header_row else ""
        is_kargo_table = any(k in header_txt for k in
                             ["product", "goods", "cargo", "koopman"])

        for baris in baris_semua[1:] if is_kargo_table else baris_semua:
            sel = baris.find_all(["td", "th"])
            if len(sel) < 3:
                continue
            # Kolom standar BGB: qty | unit | product | spec | nilai_NL | nilai_India
            qty_txt  = sel[0].get_text(strip=True) if len(sel) > 0 else ""
            unit_txt = sel[1].get_text(strip=True) if len(sel) > 1 else ""
            prod_txt = sel[2].get_text(strip=True) if len(sel) > 2 else ""
            spec_txt = sel[3].get_text(strip=True) if len(sel) > 3 else ""
            val_nl   = sel[4].get_text(strip=True) if len(sel) > 4 else ""
            val_in   = sel[5].get_text(strip=True) if len(sel) > 5 else ""

            # Lewati baris kosong / header yang terulang
            if not prod_txt or prod_txt.lower() in ("product", "goods", ""):
                continue

            # Link produk
            prod_link = sel[2].find("a")
            prod_url  = (BASE_URL + prod_link["href"]
                         if prod_link and prod_link.get("href") else "")

            kq   = parse_kuantitas(qty_txt, unit_txt)
            g_nl = parse_gulden(val_nl)
            g_in = parse_gulden(val_in)

            # Gunakan gulden NL jika ada, jika 0 gunakan gulden India
            g_used = g_nl if g_nl > 0 else g_in

            kargo_item = {
                "produk":       prod_txt,
                "produk_url":   prod_url,
                "spesifikasi":  spec_txt,
                "qty_asli":     qty_txt,
                "unit":         unit_txt,
                "nilai_numerik": kq["nilai_numerik"],
                "gram":         kq["gram"],
                "gulden_nl":    g_nl,
                "gulden_india": g_in,
                "gulden_used":  g_used,
                "catatan":      kq["catatan"],
            }
            kargo_list.append(kargo_item)

            produk_bersih = prod_txt.strip().lower()
            if produk_bersih:
                semua_produk.add(produk_bersih)

            total_gulden += g_used
            if g_used > max_gulden:
                max_gulden   = g_used
                produk_utama = prod_txt

    # ── Durasi pelayaran ─────────────────────────────────────────────
    durasi_hari = None
    if (tgl_brgkt.get("iso") and tgl_tiba.get("iso") and
            len(tgl_brgkt["iso"]) == 10 and len(tgl_tiba["iso"]) == 10):
        try:
            db = datetime.fromisoformat(tgl_brgkt["iso"])
            dt = datetime.fromisoformat(tgl_tiba["iso"])
            diff = (dt - db).days
            if 0 < diff < 3000:   # sanity check
                durasi_hari = diff
        except Exception:
            pass

    return {
        # ── Identitas ──────────────────────────────────────────────
        "ID":              voyage_id,
        "URL":             url,
        "Nama_Kapal":      nama_kapal or "Tidak diketahui",
        "Kapten":          kapten or None,
        "Tonaj":           tonaj or None,

        # ── Asal & tujuan ─────────────────────────────────────────
        "Asal":            departure_meta["nama"],
        "Asal_ID":         departure_meta["id"],
        "Asal_Lat":        departure_meta["lat"],
        "Asal_Lon":        departure_meta["lon"],
        "Wilayah":         departure_meta["wilayah"],
        "Tujuan":          tujuan or "",

        # ── Tanggal lengkap ───────────────────────────────────────
        "Tahun_Buku":      tahun_buku_info.get("tahun"),
        "Tahun":           tgl_brgkt.get("tahun") or tgl_tiba.get("tahun") or tahun_buku_info.get("tahun"),
        "Tgl_Berangkat":   tgl_brgkt,   # { hari, bulan, tahun, iso }
        "Tgl_Tiba":        tgl_tiba,
        "Durasi_Hari":     durasi_hari,

        # ── Komoditi (ringkasan) ──────────────────────────────────
        "Produk_Utama":    produk_utama or (list(semua_produk)[0] if semua_produk else ""),
        "Semua_Produk":    " | ".join(sorted(semua_produk)),
        "Total_Gulden_NL": round(total_gulden, 4), # now uses g_used (either NL or India)
        "Jumlah_Item_Kargo": len(kargo_list),

        # ── Detail kargo lengkap ──────────────────────────────────
        "Kargo":           kargo_list,

        # ── Metadata ──────────────────────────────────────────────
        "Scraped_At":      datetime.utcnow().isoformat() + "Z",
    }


# ── Crawl daftar voyage untuk satu tempat ────────────────────────────────────
def crawl_voyage_urls(place_id: str, place_name: str, 
                      arah: str = "departure_place_id",
                      product: Optional[str] = None) -> list[str]:
    """
    Ambil semua URL voyage dari halaman daftar BGB.
    Mendukung arah: departure_place_id atau arrival_place_id.
    """
    urls    = []
    seen    = set()
    page    = 0
    params  = {
        arah:           place_id,
        "group_by_all": "on",
    }
    if product:
        params["product_name"] = product

    dir_label = "Keberangkatan" if arah == "departure_place_id" else "Kedatangan"
    print(f"  Crawling URL ({dir_label}): {place_name} (id={place_id})"
          + (f" produk={product}" if product else " semua produk"))

    while page < MAX_PAGES_PER_PLACE:
        params["start"] = page * 10
        try:
            r = requests.get(SEARCH_URL, params=params,
                             headers=HEADERS, timeout=25)
            r.raise_for_status()
        except Exception as e:
            print(f"    [!] Gagal page {page}: {e}")
            break

        soup = BeautifulSoup(r.text, "html.parser")
        baru = 0
        for a in soup.find_all("a", href=True):
            if re.search(r"/bgb/voyage/\d+", a["href"]):
                u = (a["href"] if a["href"].startswith("http")
                     else BASE_URL + a["href"])
                if u not in seen:
                    seen.add(u)
                    urls.append(u)
                    baru += 1

        print(f"    page={page} | +{baru} baru | total: {len(urls)}")

        # Cek "next" link
        nxt = soup.find("a", string=re.compile(r"^\s*next\s*$", re.I))
        if not nxt:
            break
        page += 1
        time.sleep(DELAY_DETIK)

    return urls


# ── Checkpoint: simpan & muat progress ───────────────────────────────────────
def simpan_checkpoint(data: list, done_urls: set):
    with open(CHECKPOINT, "w", encoding="utf-8") as f:
        json.dump({"data": data, "done_urls": list(done_urls)},
                  f, ensure_ascii=False)

def muat_checkpoint() -> tuple[list, set]:
    if os.path.exists(CHECKPOINT):
        with open(CHECKPOINT, encoding="utf-8") as f:
            d = json.load(f)
        print(f"[RESUME] {len(d['data'])} voyage dari checkpoint.")
        return d["data"], set(d["done_urls"])
    return [], set()


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 72)
    print("  BGB SUMATRA COMPREHENSIVE SCRAPER")
    print(f"  Lokasi: {', '.join(v[0] for v in SUMATRA_PORTS.values())}")
    print(f"  Output: {OUTPUT_FILE}")
    print(f"  Filter produk: {PRODUCT_FILTER or 'semua'}")
    print("=" * 72)

    # Resume dari checkpoint jika ada
    semua_data, done_urls = muat_checkpoint()

    for place_id, meta in SUMATRA_PORTS.items():
        place_name, lat, lon, wilayah, keterangan = meta
        port_meta = {
            "id": place_id, "nama": place_name,
            "lat": lat, "lon": lon,
            "wilayah": wilayah, "keterangan": keterangan,
        }

        print(f"\n{'─'*72}")
        print(f"[TEMPAT] {place_name} (id={place_id}) — {wilayah}")
        print(f"{'─'*72}")

        # Kumpulkan URL sebagai Departure
        urls_dep = crawl_voyage_urls(place_id, place_name, "departure_place_id", PRODUCT_FILTER)
        urls_arr = crawl_voyage_urls(place_id, place_name, "arrival_place_id", PRODUCT_FILTER)
        
        # Gabung dan hapus duplikat
        semua_url_port = list(set(urls_dep + urls_arr))
        
        url_untuk_discrape = [u for u in semua_url_port if u not in done_urls]
        print(f"  → Ditemukan {len(urls_dep)} depart, {len(urls_arr)} arrive.")
        print(f"  → Total {len(url_untuk_discrape)} voyage baru yang akan di-scrape.")

        for i, url in enumerate(url_untuk_discrape):
            if url in done_urls:
                continue

            detail = parse_voyage_detail(url, port_meta)
            if detail:
                semua_data.append(detail)
                done_urls.add(url)

            # Progress
            if (i + 1) % 10 == 0 or (i + 1) == len(url_untuk_discrape):
                print(f"  [{i+1}/{len(url_untuk_discrape)}] "
                      f"total terkumpul: {len(semua_data)} voyage")
                # Simpan checkpoint setiap 10 voyage
                simpan_checkpoint(semua_data, done_urls)

            time.sleep(DELAY_DETIK)

    # ── Tulis output final ────────────────────────────────────────────────
    print(f"\n{'='*72}")
    print(f"[SELESAI] Total: {len(semua_data)} voyage dari {len(done_urls)} URL")

    # Urutkan berdasarkan tahun
    semua_data.sort(key=lambda x: (x.get("Tahun") or 9999, x.get("ID") or 0))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(semua_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Disimpan: {OUTPUT_FILE}")

    # ── Ringkasan statistik ───────────────────────────────────────────────
    print(f"\n{'─'*72}")
    print("RINGKASAN")
    print(f"{'─'*72}")

    from collections import Counter
    per_asal = Counter(d["Asal"] for d in semua_data)
    for nama, jml in per_asal.most_common():
        print(f"  {nama:25s}: {jml:4d} voyage")

    tahun_list = [d["Tahun"] for d in semua_data if d.get("Tahun")]
    if tahun_list:
        print(f"\n  Rentang tahun : {min(tahun_list)} – {max(tahun_list)}")

    produk_all = []
    for d in semua_data:
        produk_all.extend([p.strip() for p in d.get("Semua_Produk","").split("|") if p.strip()])
    if produk_all:
        print("\n  Komoditi teratas:")
        for prod, ct in Counter(produk_all).most_common(10):
            print(f"    {prod:25s}: {ct:4d}×")

    total_gulden = sum(d.get("Total_Gulden_NL", 0) for d in semua_data)
    print(f"\n  Total nilai (gulden): ƒ{total_gulden:,.0f}")

    # Hapus checkpoint setelah selesai
    if os.path.exists(CHECKPOINT):
        os.remove(CHECKPOINT)
    print("\n[DONE] Scraping selesai.")


if __name__ == "__main__":
    main()
