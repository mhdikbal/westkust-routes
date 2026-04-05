"""
========================================================================
  BGB GOUD SCRAPER — VERSI FINAL
  Lacak pengiriman emas (goud) dari Padang ke Batavia
  Sumber: resources.huygens.knaw.nl/bgb

  Koreksi sistem timbang (GM4):
    - 1 mark (berat) = 230,4 gram  [bukan 246,084]
    - 1 mark = 16 lood = 64 quent = 160 engels = 5.120 ase
    - mark fijns = kadar kemurnian, BUKAN massa fisik
========================================================================
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

# =====================================================================
# BAGIAN 1 — KONFIGURASI
# =====================================================================
BASE_DOMAIN = "https://resources.huygens.knaw.nl"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept':     'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

# Dua URL — goud + goudt (ejaan lama VOC)
LIST_URLS = [
    ("https://resources.huygens.knaw.nl/bgb/voyages_results"
     "?start={start}&departure_place_id=926"
     "&product_name=goud&departure_region_id=3120&group_by_all=on"),
    ("https://resources.huygens.knaw.nl/bgb/voyages_results"
     "?start={start}&departure_place_id=926"
     "&product_name=goudt&departure_region_id=3120&group_by_all=on"),
]

KEYWORDS_GOUD   = ['goud', 'goudt', 'gold', 'gout']
DELAY_DETIK     = 1.2

# =====================================================================
# BAGIAN 2 — SISTEM TIMBANG GM4 (KOREKSI)
# =====================================================================
# Referensi: GM4 — BGB Glossary / Woordenboek der Nederlandsche Taal
#
# DUA SISTEM MARK YANG BERBEDA:
#
# [A] mark fijns  → KADAR kemurnian emas (fineness scale)
#     1 mark fijns = 12 penningen = 24 karaat = 288 grein = 4.920 mg
#     "29,17,1" di unit 'mark fijns' = kadar, bukan massa fisik
#     → tidak dikonversi langsung ke gram
#
# [B] mark berat  → MASSA FISIK (mark-troys)
#     1 mark = 230,4 gram
#     1 mark = 16 lood = 64 quent = 160 engels = 5.120 ase = 288 grein
#     Turunan:
#       1 lood   = 230,4 / 16  = 14,40  gram
#       1 quent  = 230,4 / 64  =  3,60  gram
#       1 engels = 230,4 / 160 =  1,44  gram
#       1 ase    = 230,4 / 5120=  0,045 gram
# =====================================================================
GRAM_PER_MARK   = 230.4
LOOD_PER_MARK   = 16
QUENT_PER_MARK  = 64
ENGELS_PER_MARK = 160
ASE_PER_MARK    = 5120
GREIN_PER_MARK  = 288         # untuk mark fijns
PENNING_PER_MARK_FIJNS = 12  # untuk mark fijns

GRAM_PER_LOOD   = GRAM_PER_MARK / LOOD_PER_MARK    # 14,40 g
GRAM_PER_QUENT  = GRAM_PER_MARK / QUENT_PER_MARK   #  3,60 g
GRAM_PER_ENGELS = GRAM_PER_MARK / ENGELS_PER_MARK  #  1,44 g
GRAM_PER_ASE    = GRAM_PER_MARK / ASE_PER_MARK     #  0,045 g

# Harga referensi hari ini (update manual jika perlu)
GOLD_USD_PER_GRAM = 143.75   # spot Mar 2026 (~$4.478/troy oz)
USD_TO_IDR        = 16_350

print("=" * 65)
print("  BGB GOUD SCRAPER — FINAL (GM4 MARK SYSTEM)")
print("=" * 65)
print(f"  1 mark (berat) = {GRAM_PER_MARK} g | 1 lood = {GRAM_PER_LOOD} g")
print(f"  1 quent = {GRAM_PER_QUENT} g | 1 engels = {GRAM_PER_ENGELS} g")
print(f"  Harga emas: ${GOLD_USD_PER_GRAM}/g = Rp{GOLD_USD_PER_GRAM*USD_TO_IDR:,.0f}/g")


# =====================================================================
# BAGIAN 3 — FUNGSI HELPER
# =====================================================================

def parse_mark(qty_teks: str, unit_teks: str) -> dict:
    """
    Parse quantity emas BGB dengan sistem GM4.

    Mode A (unit mengandung 'fijn'):
      Kadar kemurnian — format "A,B,C" = mark,penning,grein fijns
      1 mark fijns = 12 penning = 288 grein
      Output: mark_desimal = rasio kadar; gram = 0 (bukan massa)

    Mode B (unit = mark/lood/quent/engels/ase):
      Massa fisik — format "A,B" = satuan-utama, sub-satuan
      Contoh "4,8 mark" = 4 mark + 8 lood = 4 + 8/16 = 4,5 mark
      Output: gram = mark_desimal × 230,4
    """
    hasil = {
        'qty_asli':     str(qty_teks).strip() if qty_teks else '',
        'unit':         str(unit_teks).strip() if unit_teks else '',
        'is_fijns':     False,
        'mark_desimal': 0.0,
        'lood':         0.0,
        'quent':        0.0,
        'engels':       0.0,
        'gram':         0.0,
        'catatan':      '',
    }

    teks = hasil['qty_asli']
    if not teks or teks in ('-', 'nan', 'None', ''):
        return hasil

    unit_l = hasil['unit'].lower()

    # ── MODE A: mark fijns (kadar) ──────────────────────────────────
    if 'fijn' in unit_l:
        hasil['is_fijns'] = True
        hasil['catatan']  = 'Kadar kemurnian — bukan massa fisik'
        parts = teks.split(',')
        try:
            m_val = float(parts[0].replace('.', '')) if parts[0] else 0.0
            p_val = float(parts[1]) if len(parts) > 1 and parts[1] else 0.0
            g_val = float(parts[2]) if len(parts) > 2 and parts[2] else 0.0
            hasil['mark_desimal'] = round(
                m_val + p_val / PENNING_PER_MARK_FIJNS + g_val / GREIN_PER_MARK, 6
            )
        except (ValueError, IndexError):
            hasil['catatan'] = f'Gagal parse fijns: {teks}'
        return hasil

    # ── MODE B: massa fisik ─────────────────────────────────────────
    # Faktor konversi ke mark
    if   'lood'   in unit_l: faktor = 1.0 / LOOD_PER_MARK
    elif 'quent'  in unit_l: faktor = 1.0 / QUENT_PER_MARK
    elif 'engels' in unit_l: faktor = 1.0 / ENGELS_PER_MARK
    elif 'ase'    in unit_l: faktor = 1.0 / ASE_PER_MARK
    else:                     faktor = 1.0   # sudah dalam mark

    parts = teks.split(',')
    try:
        if len(parts) >= 2:
            a = float(parts[0].replace('.', ''))
            b = float(parts[1]) if parts[1] else 0.0
            # Ambiguitas: "4,8" = 4 mark 8 lood ATAU 4,8 mark desimal?
            # Jika b < maks sub-unit, anggap sub-unit
            if faktor == 1.0 and b < LOOD_PER_MARK:
                # "A,B mark" = A mark + B lood
                desimal = a + b / LOOD_PER_MARK
                hasil['lood'] = b
            elif faktor == 1.0 and len(parts[1]) == 3:
                # "1.234" → ribuan, bukan sub-unit
                desimal = float(teks.replace('.', '').replace(',', '.'))
            else:
                desimal = a * faktor  # hanya pakai bagian pertama jika unit sudah bukan mark
        else:
            bersih  = teks.replace('.', '').replace(',', '.')
            desimal = float(bersih) * faktor if bersih else 0.0
    except ValueError:
        hasil['catatan'] = f'Gagal parse berat: {teks}'
        return hasil

    hasil['mark_desimal'] = round(desimal, 6)
    hasil['gram']         = round(desimal * GRAM_PER_MARK, 3)
    return hasil


def parse_guilder(teks: str) -> float:
    """
    Nilai guilder VOC → float desimal gulden.
    Format: "11.142,19"  → 11142 gulden 19 stuiver
            "21.690,9,8" → 21690 gulden 9 stuiver 8 penning
    1 gulden = 20 stuiver = 320 penning
    """
    if not teks or str(teks).strip() in ('', '-', 'nan', 'None', '—'):
        return 0.0
    parts = str(teks).strip().replace('.', '').split(',')
    try:
        gulden  = float(parts[0]) if parts[0] else 0.0
        stuiver = float(parts[1]) / 20.0   if len(parts) > 1 and parts[1] else 0.0
        penning = float(parts[2]) / 320.0  if len(parts) > 2 and parts[2] else 0.0
        return round(gulden + stuiver + penning, 4)
    except (ValueError, IndexError):
        return 0.0


def ekstrak_tahun(soup, teks_halaman: str, label_kunci: list) -> int:
    """Cari tahun di halaman berdasarkan label. Fallback ke regex."""
    for el in soup.find_all(['th', 'td', 'dt', 'label', 'b', 'strong']):
        t = el.get_text(strip=True).lower()
        if all(k in t for k in label_kunci):
            sdr = el.find_next_sibling(['td', 'dd'])
            if sdr:
                m = re.search(r'\b(1[5-9]\d{2}|[12]\d{3})\b', sdr.get_text())
                if m:
                    return int(m.group(1))
    pola_fallback = {
        ('book',):   r'[Bb]ook(?:ing)?\s*[Yy]ear\s*[:\-]?\s*(\d{4})',
        ('depart',): r'[Dd]epart(?:ure)?\s*[:\-]?\s*(\d{4})',
        ('arriv',):  r'[Aa]rriv(?:al|ed)?\s*[:\-]?\s*(\d{4})',
    }
    for keys, pola in pola_fallback.items():
        if any(k in ' '.join(label_kunci) for k in keys):
            m = re.search(pola, teks_halaman)
            if m:
                return int(m.group(1))
    return 0


def ekstrak_tujuan(soup, teks_halaman: str) -> str:
    """Cari tujuan (arrival place) di halaman."""
    for el in soup.find_all(['th', 'td', 'dt', 'label', 'b', 'strong']):
        lbl = el.get_text(strip=True).lower()
        if ('arrival' in lbl and 'place' in lbl) \
                or 'destination' in lbl or 'bestemming' in lbl:
            sdr = el.find_next_sibling(['td', 'dd'])
            if sdr:
                return sdr.get_text(strip=True)
    m = re.search(r'[Aa]rrival\s+[Pp]lace\s*[:\-]?\s*([A-Za-z ,]+)', teks_halaman)
    return m.group(1).strip() if m else 'Tidak diketahui'


def crawl_list(template: str) -> set:
    """Crawl satu URL template (dengan pagination) → set URL detail voyage."""
    urls   = set()
    nama   = re.search(r'product_name=([^&]+)', template).group(1)
    start  = 0
    print(f"\n  >> product_name={nama}")
    while True:
        url_list = template.format(start=start)
        try:
            res = requests.get(url_list, headers=HEADERS, timeout=20)
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"    [!] Gagal (start={start}): {e}")
            break
        soup = BeautifulSoup(res.text, 'html.parser')
        baru = 0
        for a in soup.find_all('a', href=True):
            if re.search(r'/bgb/voyage/\d+', a['href']):
                u = a['href'] if a['href'].startswith('http') else BASE_DOMAIN + a['href']
                if u not in urls:
                    urls.add(u)
                    baru += 1
        print(f"    start={start:>4} | +{baru} baru | total: {len(urls)}")
        nxt = soup.find('a', string=re.compile(r'^\s*next\s*$', re.IGNORECASE))
        if nxt and nxt.get('href'):
            m = re.search(r'start=(\d+)', nxt['href'])
            if m:
                start = int(m.group(1))
            else:
                break
        else:
            break
        time.sleep(DELAY_DETIK)
    return urls


# =====================================================================
# BAGIAN 4 — FASE 1: CRAWL URL
# =====================================================================
print("\n" + "─" * 65)
print("[FASE 1] Kumpulkan URL detail voyage...")
print("─" * 65)

semua_url = set()
for tmpl in LIST_URLS:
    semua_url |= crawl_list(tmpl)

semua_url = sorted(semua_url)
print(f"\n[+] Total URL voyage unik: {len(semua_url)}")


# =====================================================================
# BAGIAN 5 — FASE 2: EKSTRAKSI DETAIL
# =====================================================================
# Struktur tabel kargo BGB (dari HTML aktual):
#   <td col-0> Quantity     </td>  ← angka
#   <td col-1> Unit         </td>  ← mark fijns / lood / lb / dst
#   <td col-2> Product link </td>  ← goud / peper / dst
#   <td col-3> Specification</td>  ← bij gewicht / fijns / ruw / dst
#   <td col-4> Value Dutch  </td>  ← guilder Belanda
#   <td col-5> Value Indian </td>  ← guilder India
# =====================================================================
print("\n" + "─" * 65)
print("[FASE 2] Ekstraksi data dari setiap voyage...")
print("─" * 65)

data_valid = []

for idx, url_kapal in enumerate(semua_url):
    try:
        res  = requests.get(url_kapal, headers=HEADERS, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        teks = soup.get_text(separator=' ')

        # Tahun
        thn_buku  = ekstrak_tahun(soup, teks, ['book', 'year'])
        thn_brgkt = ekstrak_tahun(soup, teks, ['depart'])
        thn_tiba  = ekstrak_tahun(soup, teks, ['arriv'])
        thn_final = thn_buku or thn_brgkt or thn_tiba

        # Tujuan
        tujuan = ekstrak_tujuan(soup, teks)

        # Scan tabel kargo
        for tabel in soup.find_all('table'):
            for baris in tabel.find_all('tr'):
                sel = baris.find_all(['td', 'th'])
                if len(sel) < 3:
                    continue

                qty_teks  = sel[0].get_text(strip=True) if len(sel) > 0 else ''
                unit_teks = sel[1].get_text(strip=True) if len(sel) > 1 else ''
                prod_teks = sel[2].get_text(strip=True) if len(sel) > 2 else ''
                spec_teks = sel[3].get_text(strip=True) if len(sel) > 3 else ''
                val_dutch = sel[4].get_text(strip=True) if len(sel) > 4 else ''
                val_india = sel[5].get_text(strip=True) if len(sel) > 5 else ''

                # Filter produk emas
                if not any(kw in prod_teks.lower() for kw in KEYWORDS_GOUD):
                    continue

                # Parse quantity dengan GM4
                unit_l = unit_teks.lower()
                if any(k in unit_l for k in ['mark', 'lood', 'quent', 'engels', 'ase']):
                    p = parse_mark(qty_teks, unit_teks)
                else:
                    # Unit lain (lb, pond, tail, dll)
                    bersih = re.sub(r'[^\d.,]', '', qty_teks)
                    bersih = bersih.replace('.', '').replace(',', '.') if ',' in bersih else bersih
                    try:
                        qty_num = float(bersih) if bersih else 0.0
                    except ValueError:
                        qty_num = 0.0
                    p = {
                        'qty_asli': qty_teks, 'unit': unit_teks,
                        'is_fijns': False, 'mark_desimal': 0.0,
                        'lood': 0.0, 'quent': 0.0, 'engels': 0.0,
                        'gram': 0.0, 'catatan': f'Unit lain: {unit_teks}',
                    }

                # Parse nilai guilder
                nilai_nl = parse_guilder(val_dutch)
                nilai_in = parse_guilder(val_india)

                data_valid.append({
                    'Tahun':           thn_final  if thn_final  > 0 else None,
                    'Tahun_Buku':      thn_buku   if thn_buku   > 0 else None,
                    'Tahun_Berangkat': thn_brgkt  if thn_brgkt  > 0 else None,
                    'Tahun_Tiba':      thn_tiba   if thn_tiba   > 0 else None,
                    'Tujuan':          tujuan,
                    'Produk':          prod_teks,
                    'Spesifikasi':     spec_teks,
                    'Qty_Asli':        p['qty_asli'],
                    'Unit':            unit_teks,
                    'Is_Fijns':        p['is_fijns'],
                    'Mark_Desimal':    p['mark_desimal'],
                    'Lood':            p.get('lood', 0.0),
                    'Gram':            p['gram'],          # 0 jika is_fijns
                    'Nilai_Gulden_NL': nilai_nl,
                    'Nilai_Gulden_IN': nilai_in,
                    'Catatan':         p.get('catatan', ''),
                    'URL':             url_kapal,
                })

    except requests.RequestException as e:
        print(f"  [!] Network: {url_kapal} — {e}")
    except Exception as e:
        print(f"  [!] Parse:   {url_kapal} — {e}")

    if (idx + 1) % 10 == 0 or (idx + 1) == len(semua_url):
        fijns_ct = sum(1 for d in data_valid if d['Is_Fijns'])
        print(f"  -> {idx+1}/{len(semua_url)} | baris={len(data_valid)} "
              f"(massa={len(data_valid)-fijns_ct}, fijns={fijns_ct})")

    time.sleep(DELAY_DETIK)


# =====================================================================
# BAGIAN 6 — FASE 3: BERSIHKAN & SIMPAN
# =====================================================================
print("\n" + "─" * 65)
print("[FASE 3] Membersihkan dan menyimpan data...")
print("─" * 65)

if not data_valid:
    print("[GAGAL] Tidak ada data emas ditemukan.")
    raise SystemExit

df_raw   = pd.DataFrame(data_valid)
df_bersih = df_raw.dropna(subset=['Tahun']).copy()
df_bersih['Tahun'] = df_bersih['Tahun'].astype(int)
df_bersih = df_bersih[
    (df_bersih['Tahun'] >= 1550) & (df_bersih['Tahun'] <= 1850)
].sort_values('Tahun')
df_bersih = df_bersih.drop_duplicates(subset=['URL', 'Qty_Asli', 'Nilai_Gulden_NL'])

# Pisahkan baris massa fisik vs kadar
df_massa  = df_bersih[~df_bersih['Is_Fijns']].copy()
df_fijns  = df_bersih[ df_bersih['Is_Fijns']].copy()

print(f"[SUKSES] {len(df_bersih)} baris dari {df_bersih['URL'].nunique()} voyage unik")
print(f"  Massa fisik : {len(df_massa)} baris")
print(f"  Mark fijns  : {len(df_fijns)} baris (kadar — tidak dikonversi ke gram)")
print(f"  Rentang     : {df_bersih['Tahun'].min()} – {df_bersih['Tahun'].max()}")

print("\n  Unit timbang:")
print(df_bersih['Unit'].value_counts().to_string())
print("\n  Spesifikasi:")
print(df_bersih['Spesifikasi'].value_counts().to_string())
print("\n  Tujuan teratas:")
print(df_bersih['Tujuan'].value_counts().head(8).to_string())

tot_gram   = df_massa['Gram'].sum()
tot_gulden = df_bersih['Nilai_Gulden_NL'].sum()
print(f"\n  Total massa emas : {tot_gram:,.1f} g = {tot_gram/1000:,.3f} kg")
print(f"  Total Dutch gulden: ƒ{tot_gulden:,.2f}")
print(f"  Nilai kini (~spot): Rp{tot_gram*GOLD_USD_PER_GRAM*USD_TO_IDR/1e12:.3f} triliun")

# Simpan
df_bersih.to_csv('Data_Goud_Padang_Final.csv',
                 index=False, sep=';', encoding='utf-8-sig')
print("\n[+] Disimpan: Data_Goud_Padang_Final.csv")


# =====================================================================
# BAGIAN 7 — FASE 4: VISUALISASI LENGKAP (6 PANEL)
# =====================================================================
print("\n" + "─" * 65)
print("[FASE 4] Visualisasi...")
print("─" * 65)

plt.rcParams.update({
    'figure.facecolor':   '#fafafa',
    'axes.facecolor':     'white',
    'axes.grid':          True,
    'grid.color':         '#e8e8e8',
    'grid.linewidth':     0.6,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.spines.left':   True,
    'axes.spines.bottom': True,
    'axes.edgecolor':     '#cccccc',
    'font.family':        'DejaVu Sans',
})

C_G  = '#854f0b'    # amber gelap (emas)
C_GA = '#fac77530'
C_V  = '#185fa5'    # biru (gulden)
C_VA = '#378add25'
C_N  = '#3b6d11'    # hijau (nilai kini)
C_GR = '#5f5e5a'    # abu (voyage count)

# ── Agregasi per tahun ────────────────────────────────────────────
df_gram  = df_massa[df_massa['Gram'] > 0].groupby('Tahun')['Gram'].sum().reset_index()
df_gulden= df_bersih[df_bersih['Nilai_Gulden_NL']>0]\
           .groupby('Tahun')['Nilai_Gulden_NL'].sum().reset_index()
df_voy   = df_bersih.groupby('Tahun')['URL'].nunique().reset_index()
df_spec  = df_bersih['Spesifikasi'].value_counts().head(8)
df_tujuan= df_bersih['Tujuan'].value_counts().head(8)

# Nilai hari ini per tahun
df_gram['Nilai_IDR_M'] = df_gram['Gram'] * GOLD_USD_PER_GRAM * USD_TO_IDR / 1e9

# ── Figure ────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 16))
fig.suptitle(
    'Pengiriman Emas (Goud) dari Padang  ·  BGB Huygens\n'
    'Sistem timbang GM4: 1 mark = 230,4 gram  ·  '
    f'Harga emas ${GOLD_USD_PER_GRAM}/g (Mar 2026)',
    fontsize=13, fontweight='bold', y=0.995, color='#2c2c2a'
)

gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.52, wspace=0.32,
                       top=0.95, bottom=0.06, left=0.07, right=0.97)


def annotate_top(ax, x, y, fmt, color, threshold_pct=0.70):
    """Anotasi titik di atas threshold persentil."""
    if len(y) == 0:
        return
    thr = np.quantile(y, threshold_pct)
    for xi, yi in zip(x, y):
        if yi >= thr:
            ax.annotate(fmt(yi), (xi, yi),
                        textcoords='offset points', xytext=(0, 7),
                        ha='center', fontsize=8, color=color, fontweight='500')


def stat_box(ax, txt, color):
    ax.text(0.98, 0.96, txt, transform=ax.transAxes,
            ha='right', va='top', fontsize=8.5, color=color,
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                      edgecolor=color, linewidth=0.7, alpha=0.9))


# ── Panel 1: Kuantitas gram per tahun ────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
if not df_gram.empty:
    ax1.bar(df_gram['Tahun'], df_gram['Gram'],
            color=C_GA, width=1.0, zorder=2, edgecolor=C_G, linewidth=0.3)
    ax1.plot(df_gram['Tahun'], df_gram['Gram'],
             color=C_G, lw=2.2, marker='o', ms=5.5, zorder=3)
    annotate_top(ax1, df_gram['Tahun'], df_gram['Gram'],
                 lambda v: f'{v/1000:.1f}kg', C_G)
    tot_g = df_gram['Gram'].sum()
    pk    = df_gram.loc[df_gram['Gram'].idxmax()]
    stat_box(ax1,
             f"Total: {tot_g/1000:,.2f} kg\nPuncak: {int(pk['Tahun'])} "
             f"({pk['Gram']/1000:.2f} kg)", C_G)

ax1.set_title('Massa emas per tahun (gram → kg)', fontsize=11,
              color=C_G, fontweight='bold', loc='left', pad=6)
ax1.set_ylabel('Gram', fontsize=10, color='#444')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'{v/1000:.1f}k'))
ax1.xaxis.set_major_locator(ticker.MaxNLocator(9, integer=True))
ax1.tick_params(axis='x', rotation=45, labelsize=8.5)
ax1.tick_params(axis='y', labelsize=8.5)


# ── Panel 2: Nilai Dutch guilders per tahun ───────────────────────
ax2 = fig.add_subplot(gs[0, 1])
if not df_gulden.empty:
    ax2.bar(df_gulden['Tahun'], df_gulden['Nilai_Gulden_NL'],
            color=C_VA, width=1.0, zorder=2, edgecolor=C_V, linewidth=0.3)
    ax2.plot(df_gulden['Tahun'], df_gulden['Nilai_Gulden_NL'],
             color=C_V, lw=2.2, marker='s', ms=5, zorder=3)
    annotate_top(ax2, df_gulden['Tahun'], df_gulden['Nilai_Gulden_NL'],
                 lambda v: f'ƒ{v/1000:.0f}k', C_V)
    tot_v = df_gulden['Nilai_Gulden_NL'].sum()
    pk2   = df_gulden.loc[df_gulden['Nilai_Gulden_NL'].idxmax()]
    stat_box(ax2,
             f"Total: ƒ{tot_v:,.0f}\nPuncak: {int(pk2['Tahun'])} "
             f"(ƒ{pk2['Nilai_Gulden_NL']:,.0f})", C_V)

ax2.set_title('Nilai emas dalam Dutch guilders per tahun', fontsize=11,
              color=C_V, fontweight='bold', loc='left', pad=6)
ax2.set_ylabel('Guilden (ƒ)', fontsize=10, color='#444')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'ƒ{v:,.0f}'))
ax2.xaxis.set_major_locator(ticker.MaxNLocator(9, integer=True))
ax2.tick_params(axis='x', rotation=45, labelsize=8.5)
ax2.tick_params(axis='y', labelsize=8.5)


# ── Panel 3: Nilai kini (IDR miliar) per tahun ────────────────────
ax3 = fig.add_subplot(gs[1, 0])
if not df_gram.empty:
    ax3.bar(df_gram['Tahun'], df_gram['Nilai_IDR_M'],
            color='#eaf3de', width=1.0, zorder=2, edgecolor=C_N, linewidth=0.3)
    ax3.plot(df_gram['Tahun'], df_gram['Nilai_IDR_M'],
             color=C_N, lw=2.2, marker='^', ms=5.5, zorder=3)
    annotate_top(ax3, df_gram['Tahun'], df_gram['Nilai_IDR_M'],
                 lambda v: f'Rp{v:.0f}M', C_N)
    tot_idr = df_gram['Nilai_IDR_M'].sum()
    stat_box(ax3,
             f"Total: Rp{tot_idr:.1f} miliar\n= Rp{tot_idr/1000:.3f} triliun\n"
             f"(spot emas ${GOLD_USD_PER_GRAM}/g)", C_N)

ax3.set_title('Nilai emas kini (Rp miliar, harga spot Mar 2026)', fontsize=11,
              color=C_N, fontweight='bold', loc='left', pad=6)
ax3.set_ylabel('Rp (miliar)', fontsize=10, color='#444')
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'Rp{v:,.0f}M'))
ax3.xaxis.set_major_locator(ticker.MaxNLocator(9, integer=True))
ax3.tick_params(axis='x', rotation=45, labelsize=8.5)
ax3.tick_params(axis='y', labelsize=8.5)


# ── Panel 4: Jumlah voyage per tahun ─────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.bar(df_voy['Tahun'], df_voy['URL'],
        color='#f1efe860', width=1.0, zorder=2, edgecolor=C_GR, linewidth=0.5)
ax4.plot(df_voy['Tahun'], df_voy['URL'],
         color=C_GR, lw=2.0, marker='D', ms=4.5, zorder=3)
for _, r in df_voy.iterrows():
    ax4.annotate(str(int(r['URL'])), (r['Tahun'], r['URL']),
                 textcoords='offset points', xytext=(0, 6),
                 ha='center', fontsize=8, color=C_GR)
stat_box(ax4,
         f"Total voyage: {int(df_voy['URL'].sum())}\n"
         f"Rata-rata: {df_voy['URL'].mean():.1f}/tahun", C_GR)

ax4.set_title('Jumlah voyage membawa emas per tahun', fontsize=11,
              color=C_GR, fontweight='bold', loc='left', pad=6)
ax4.set_ylabel('Jumlah voyage', fontsize=10, color='#444')
ax4.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax4.xaxis.set_major_locator(ticker.MaxNLocator(9, integer=True))
ax4.tick_params(axis='x', rotation=45, labelsize=8.5)
ax4.tick_params(axis='y', labelsize=8.5)


# ── Panel 5: Spesifikasi emas (horizontal bar) ────────────────────
ax5 = fig.add_subplot(gs[2, 0])
if not df_spec.empty:
    cols_spec = ['#ef9f27','#fac775','#ba7517','#854f0b',
                 '#633806','#412402','#d3d1c7','#888780']
    bars5 = ax5.barh(range(len(df_spec)), df_spec.values,
                     color=cols_spec[:len(df_spec)], height=0.6, zorder=2)
    ax5.set_yticks(range(len(df_spec)))
    ax5.set_yticklabels(df_spec.index, fontsize=9)
    for i, (bar, val) in enumerate(zip(bars5, df_spec.values)):
        ax5.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                 f'{int(val)}×', va='center', fontsize=9, color='#444')
ax5.set_title('Spesifikasi emas (jumlah entri)', fontsize=11,
              fontweight='bold', loc='left', pad=6, color='#444')
ax5.set_xlabel('Jumlah entri', fontsize=10)
ax5.spines['left'].set_visible(False)
ax5.tick_params(axis='y', length=0)
ax5.invert_yaxis()


# ── Panel 6: Tujuan pengiriman (horizontal bar) ───────────────────
ax6 = fig.add_subplot(gs[2, 1])
if not df_tujuan.empty:
    cols_tuj = ['#185fa5','#378add','#85b7eb','#b5d4f4',
                '#0c447c','#042c53','#d3d1c7','#888780']
    bars6 = ax6.barh(range(len(df_tujuan)), df_tujuan.values,
                     color=cols_tuj[:len(df_tujuan)], height=0.6, zorder=2)
    ax6.set_yticks(range(len(df_tujuan)))
    ax6.set_yticklabels(df_tujuan.index, fontsize=9)
    for bar, val in zip(bars6, df_tujuan.values):
        ax6.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                 f'{int(val)}×', va='center', fontsize=9, color='#444')
ax6.set_title('Tujuan pengiriman emas (jumlah voyage)', fontsize=11,
              fontweight='bold', loc='left', pad=6, color='#444')
ax6.set_xlabel('Jumlah voyage', fontsize=10)
ax6.spines['left'].set_visible(False)
ax6.tick_params(axis='y', length=0)
ax6.invert_yaxis()


# ── Simpan ────────────────────────────────────────────────────────
plt.savefig('Grafik_Goud_Padang_Final.png', dpi=150, bbox_inches='tight',
            facecolor='#fafafa')
plt.show()
print("[+] Grafik disimpan: Grafik_Goud_Padang_Final.png")


# =====================================================================
# BAGIAN 8 — TABEL RINGKASAN & JSON EXPORT
# =====================================================================
print("\n" + "=" * 65)
print("TABEL RINGKASAN PER TAHUN")
print("=" * 65)

df_ring = df_massa[df_massa['Gram'] > 0].groupby('Tahun').agg(
    Voyage       = ('URL',            'nunique'),
    Mark_Total   = ('Mark_Desimal',   'sum'),
    Gram_Total   = ('Gram',           'sum'),
    Gulden_NL    = ('Nilai_Gulden_NL','sum'),
    Gulden_IN    = ('Nilai_Gulden_IN','sum'),
).round(2)
df_ring['Kg']          = (df_ring['Gram_Total'] / 1000).round(3)
df_ring['Nilai_IDR_M'] = (df_ring['Gram_Total'] * GOLD_USD_PER_GRAM
                           * USD_TO_IDR / 1e9).round(2)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width',    200)
print(df_ring.to_string())

print("\n" + "-" * 65)
print("RINGKASAN PER SPESIFIKASI")
print("-" * 65)
print(df_bersih.groupby('Spesifikasi').agg(
    Entri       = ('Qty_Asli',        'count'),
    Gram_Total  = ('Gram',            'sum'),
    Gulden_Total= ('Nilai_Gulden_NL', 'sum'),
).round(1).sort_values('Gulden_Total', ascending=False).to_string())

print("\n" + "-" * 65)
print("RINGKASAN PER TUJUAN")
print("-" * 65)
print(df_bersih.groupby('Tujuan').agg(
    Voyage      = ('URL',             'nunique'),
    Gram_Total  = ('Gram',            'sum'),
    Gulden_Total= ('Nilai_Gulden_NL', 'sum'),
).round(1).sort_values('Gram_Total', ascending=False).to_string())

# JSON untuk grafik interaktif
df_json = df_ring.reset_index()[['Tahun','Mark_Total','Gram_Total','Kg',
                                  'Gulden_NL','Nilai_IDR_M','Voyage']]
df_json.columns = ['t','mark','gram','kg','gulden','idr_m','voyage']
print("\n[JSON untuk grafik interaktif Claude]")
print("const RAW =", df_json.to_json(orient='records', double_precision=3))
