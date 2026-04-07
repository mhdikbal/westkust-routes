import sys
from scrawling.bgb_sumatra_scraper import parse_voyage_detail
dummy_meta = {'id': '854', 'nama': 'Airhadji', 'lat': 0, 'lon': 0, 'wilayah': 'Sumatra'}
url = 'https://resources.huygens.knaw.nl/bgb/voyage/5406'
res = parse_voyage_detail(url, dummy_meta)
print('Tahun:', res.get('Tahun'))
print('Tgl_Tiba:', res.get('Tgl_Tiba'))
print('Tgl_Berangkat:', res.get('Tgl_Berangkat'))
print('Total_Gulden:', res.get('Total_Gulden_NL'))
print('Produk_Utama:', res.get('Produk_Utama'))
