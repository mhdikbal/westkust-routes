# Audit & Perbaikan: `dutch_ships_asian_waters` (dataverse.nl)

**Status:** Eksekusi selesai (2026-07-26).
**Sumber:** [Dutch-Asiatic Shipping / Bruijn-Gaastra-Schöffer](https://dataverse.nl/dataset.xhtml?persistentId=doi:10.34894/5HGTCD), dataverse.nl/DANS.
**Konteks:** 889 baris voyage (1600-1692) sudah di-insert ke tabel `voyages` production lokal (`source='dutch_ships_asian_waters'`) di sesi lain, TANPA script yang di-commit ke git -- tidak ada PRD, tidak ada entry di `seed_data.py`. Sesi ini mengaudit kualitas data lalu memperbaiki lewat script reproducible.

## Temuan Audit

| # | Temuan | Skala |
|---|---|---|
| 1 | Nama kapal "Unknown" | 667/889 (75%) sebelum fix -- **tidak diperbaiki**, memang tak ada di sumber utk baris ini |
| 2 | Kargo tidak ada di `cargo_items` (padahal teks ADA di `all_products`) | 0/889 |
| 3 | Nilai (`total_gulden`) kosong | 744/889 (84%) -- **tidak diperbaiki**, memang tak ada di sumber |
| 4 | **Baris duplikat murni** (kapal+asal+tujuan+tanggal identik, terulang 2-7x) | 194/889 -- kemungkinan bug proses import ad-hoc lama (re-run tanpa dedup) |
| 5 | **False-positive mapping fort**: "tuticorin"/"tuticoryn" (Tuticorin, pantai Coromandel India -- rute Tafelbaai/Caap→Tuticorin→Colombo/Trincomalee/Paliacatte) ke-mapping keliru ke fort **Tiku** (Sumatra) | 21 baris |
| 6 | Varian ejaan fort existing belum ter-mapping (kotatengah, paddangh, tijcouw, silleda) | 4 baris |
| 7 | Baris self-loop origin=destination (mis. "tico"→"tico") | 108 baris (sebelum dedup; sebagian adalah duplikat di temuan #4, sisanya representasi sah "singgah 1 pelabuhan" -- **TIDAK diubah**, lihat Keputusan di bawah |
| 8 | Tidak ada script/PRD tercatat di git | Risiko: data hilang total kalau DB di-reseed |
| 9 | **`source` tak ada di whitelist API/dropdown** — `SourceParam` (Pydantic `Literal`, `backend/routers/voyages.py`) dan dropdown navbar (`index.html`) cuma tahu `bgb_huygens`/`daghregister_batavia`/`globalise_obp`. Data tetap muncul di "Semua Sumber" (filter default None = semua), tapi TAK BISA di-toggle sendiri/dibedakan di peta | 695 voyage |

## Keputusan

1. **Dedup**: 194 baris duplikat dihapus (sisakan id terkecil per grup). Backup `pg_dump` dibuat dulu ke scratchpad sebelum eksekusi. 889 → 695 baris.
2. **Unmap Tuticorin**: `origin_id`/`destination_id` untuk baris berejaan "tuticorin"/"tuticoryn" di-set NULL kembali -- bukan Sumatra, tidak boleh muncul di bawah fort Tiku. `origin_name_raw`/`destination_name_raw` (teks asli) TIDAK diubah, tetap jujur thd sumber.
3. **Mapping baru** (hanya varian tak-ambigu dari fort yang sudah ada): kotatengah→Koto Tangah, paddangh→Padang, tijcouw→Tiku, silleda→Salido. Varian yang mirip "Sillebar" (cillebaer/celebar/silebar/chillebaer/dst) **SENGAJA TIDAK dipetakan** -- kemungkinan pelabuhan berbeda dari Salido (lihat kutipan VOC di `prd-daghregister-voyage-data.md`: "Sillida, Indrapoura ende Sillebar" disebut sebagai 3 tempat terpisah), belum ada fort untuk itu, dan menambah fort baru butuh konfirmasi koordinat dari user (di luar scope audit ini).
4. **Self-loop origin=destination**: setelah dedup, sisa baris self-loop yang BUKAN duplikat dibiarkan apa adanya -- ini representasi sah "kapal singgah di 1 pelabuhan" (tanggal datang & berangkat beda, tapi pelabuhan sama), bukan bug. Tidak digabung/dihapus.
5. **Parse kargo**: `all_products` (teks bebas Belanda arkais) dipecah ke `cargo_items` per segmen koma, dengan ekstraksi qty+unit kalau match vocab VOC yang dikenal (bhar, teyl, catty, pond, last, dll). Segmen yang tak match pola tetap disimpan **verbatim** sebagai `produk`, dengan `catatan` berisi teks asli lengkap -- tidak ada yang dibuang atau ditebak. Hasil: 222 voyage → 850 cargo_items baru.
6. **Tambah `dutch_ships_asian_waters` ke whitelist**: `SourceParam` di `backend/routers/voyages.py` + opsi dropdown "Dutch-Asiatic Shipping" di `index.html`. Test baru: `test_filter_by_source_dutch_ships_asian_waters` (backend), `test_source_select_has_dutch_ships_asian_waters_option` (Django). Backend 502 pass, Django 164 pass. Verifikasi live: `/api/voyages/routes?source=dutch_ships_asian_waters` → 50 grup rute.
7. **Ship name "Unknown" dan nilai gulden kosong TIDAK dipaksa diisi** -- konsisten dengan kebijakan project ("jangan mengarang data", lihat rollback §7.1 `prd-daghregister-voyage-data.md`). Kalau perlu diisi, butuh ekstraksi tambahan dari sumber DAS asli (kolom lain di dataset dataverse.nl yang belum di-scrape), bukan tebakan.

## Script

`docs/thesis/dr/enrich_dutch_ships_asian_waters.py` -- idempotent (aman dijalankan ulang), verifikasi: rerun kedua menghasilkan 0 perubahan di semua langkah. Menggantikan proses ad-hoc lama yang tidak tercatat.

## Hasil Akhir

| Metrik | Sebelum | Sesudah |
|---|---|---|
| Total baris | 889 | 695 |
| Ship name "Unknown" | 667 (75%) | 473 (68%) -- turun murni krn dedup, bukan diisi |
| `origin_id` NULL | 115 | 96 |
| `destination_id` NULL | 56 | 54 |
| `total_gulden` NULL | 744 | 550 -- turun murni krn dedup |
| `cargo_items` terhubung | 0 | 850 (222 voyage) |
| Baris salah-geo (Tuticorin di bawah Tiku) | 21 | 0 |

## Belum Terselesaikan (dicatat, bukan diabaikan)

- **473 voyage masih tanpa nama kapal** -- perlu cek apakah dataset DAS asli (dataverse.nl) punya kolom nama kapal yang belum ter-scrape untuk baris ini, atau memang tidak tercatat di sumber.
- **550 voyage masih tanpa nilai gulden** -- sama, kemungkinan kolom lain di dataset asli belum diambil.
- **Parser kargo tidak sempurna** untuk segmen yang menggabungkan >1 fakta tanpa koma pemisah (mis. "54811 guldens aen ongesmolten gout. 173456 # swarte peper" ikut ke-1 baris) -- tidak ada data hilang (verbatim tetap di `catatan`), tapi butuh pembacaan manual kalau ingin dipecah lebih presisi, mengikuti pola `promote_*.py` lain di folder ini.
- **~80 raw name yang genuinely di luar Sumatra Westkust** (Tafelbaai, Bengale, Colombo, Malacca, Ceylon, dll) tetap NULL -- ini BENAR, bukan gap, karena dataset DAS mencakup seluruh pelayaran VOC Asia bukan cuma Westkust.
