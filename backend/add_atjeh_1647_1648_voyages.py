"""
add_atjeh_1647_1648_voyages.py

7 voyage ditemukan saat sisir volume docs/"Dagh-register gehouden int casteel
Batavia ... 1647-1648" (218 hlm.). Volume ini punya BANYAK surat langsung dari
ratu Atjeh, koning Indrapoera, panglima Bhandar Galiffa (Tikoe), panglima
Priaman, dan panglima Sileda/Cillida (Salido modern) -- lihat
data/research/atjeh_trade.csv baris source_document='1647-1648' utk 8 fakta
politik/dagang terkait, termasuk temuan kunci: panglima Sileda MENGUNDANG
LANGSUNG VOC berdagang thn 1648, mengonfirmasi Salida operasional menyusul
transposisi yg diblokir di volume 1644-1645.

Sumber:
  1. jacht de Zeerobbe (nevens fluijtschip den Zajer & jacht Cleen Battavia),
     Batavia->Atchijn, ~28 April 1648 [PDF hlm.88-89, cetak 74-75]: mengantar
     pulang duta ratu Atjeh yg sejak Desember 1647 di Batavia, ditemani
     oppercoopman Hubrecht van den Broecq yg ditugasi menyerahkan hadiah &
     memindahkan comptoir/residen VOC di Atjeh ke Malacca.

  2. fluijt de Noortstarre, Batavia->Cilleda (Salida), coopman Paulus Baert,
     berangkat 3 Juli 1648 [PDF hlm.117, cetak 103] "tot procure van peper".

  3. fluijt de Noortstarre, Cilleda (Salida)->Batavia, coopman Paulus Baert,
     kembali awal Agustus 1648 [PDF hlm.148, cetak 134] TANPA peper -- panglima
     & grooten Sileda menolak harga kain VOC yg di bawah pasar.

  4. schip Wesel, Batavia->Indrapoura, oppercoopman Pieter de Gojer, berangkat
     9 Juli 1648 [PDF hlm.119, cetak 105], eksplisit disebut "de laeste
     besendinge die dit jaer derwaerts gedaen zij" (pengiriman terakhir tahun
     ini ke sana).

  5. schip Wesel, Indrapoura->Batavia, oppercoopman Pieter de Gojer, kembali
     awal Agustus 1648 [PDF hlm.148, cetak 134] TANPA peper, alasan sama dgn
     Noortstarre (sengketa harga kain).

  6. fluijtschip de Wolff, dari Ticco ende Priaman->Batavia, tiba 25 September
     1648 [PDF hlm.163, cetak 149], 182 bhaar peper + banyak kain tak laku.
     Origin dicatat sbg Tiku (disebut lebih dulu di sumber "Ticco ende
     Priaman"); ambiguitas 2 pelabuhan dicatat di all_products.

  7. fluijt den Swarten Beer, dari Ticco en Priaman->Batavia, coopman Hendrick
     Craijer (nama sama yg muncul di 3 surat Maret 1648), tiba ~4 Desember
     1648 [PDF hlm.185, cetak 171] "goede partie" -- kargo detail terpotong
     OCR di batas halaman.

Idempotent: skip per-baris bila (source, origin_id, destination_id, ship_name,
departure_date, arrival_date) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_1647_1648_voyages.py
"""
import os

from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

ACEH_FORT_ID = 17
BATAVIA_FORT_ID = 9
INDERAPURA_FORT_ID = 16
SALIDO_FORT_ID = 12
TIKU_FORT_ID = 10


def build_voyage_records():
    return [
        {
            "voyage_ref": None,
            "origin_id": BATAVIA_FORT_ID, "destination_id": ACEH_FORT_ID,
            "origin_name_raw": "Battavia", "destination_name_raw": "Atchijn",
            "ship_name": "jacht de Zeerobbe",
            "captain": None,
            "tonnage": None, "year": 1648,
            "departure_date": "1648-04-28", "arrival_date": None,
            "total_gulden": None, "main_product": None,
            "all_products": (
                "Tak ada kargo dagang tercatat -- mengantar pulang duta ratu Atjeh (sejak Des "
                "1647 di Batavia) beserta rombongan, ditemani oppercoopman Hubrecht van den "
                "Broecq yg ditugasi menyerahkan missive & hadiah VOC ke ratu, dan memindahkan "
                "comptoir/residen VOC di Atjeh ke Malacca. Berlayar bersama fluijtschip den "
                "Zajer & jacht Cleen Battavia (tak dicatat terpisah di sini)."
            ),
            "cargo_count": 0, "destination": "Atchijn", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": BATAVIA_FORT_ID, "destination_id": SALIDO_FORT_ID,
            "origin_name_raw": "Battavia", "destination_name_raw": "Cilleda",
            "ship_name": "fluijt de Noortstarre",
            "captain": "coopman Paulus Baert",
            "tonnage": None, "year": 1648,
            "departure_date": "1648-07-03", "arrival_date": None,
            "total_gulden": None, "main_product": None,
            "all_products": "Berangkat 'tot procure van peper' (kosong, tujuan beli peper di tempat).",
            "cargo_count": 0, "destination": "Cilleda", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": SALIDO_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Sillida", "destination_name_raw": "Battavia",
            "ship_name": "fluijt de Noortstarre",
            "captain": "coopman Paulus Baert",
            "tonnage": None, "year": 1648,
            "departure_date": None, "arrival_date": "1648-08-09",
            "total_gulden": None, "main_product": None,
            "all_products": (
                "TANPA peper ('sonder een correl peper van daer mede te brengen') -- panglima & "
                "grooten Sileda menolak harga kain Coromandel/Gujarat VOC yg di bawah pasar. "
                "Tanggal arrival diinferensi dari OCR 'gendo' (kemungkinan '9en do') dlm konteks "
                "September 1648 -- caveat presisi tanggal."
            ),
            "cargo_count": 0, "destination": "Battavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": BATAVIA_FORT_ID, "destination_id": INDERAPURA_FORT_ID,
            "origin_name_raw": "Battavia", "destination_name_raw": "Indrapoura",
            "ship_name": "schip Wesel",
            "captain": "oppercoopman Pieter de Gojer",
            "tonnage": None, "year": 1648,
            "departure_date": "1648-07-09", "arrival_date": None,
            "total_gulden": None, "main_product": None,
            "all_products": (
                "Berangkat 'tot procure van peper', eksplisit dicatat sbg 'de laeste besendinge "
                "die dit jaer derwaerts gedaen zij' (pengiriman terakhir tahun ini ke Indrapoura)."
            ),
            "cargo_count": 0, "destination": "Indrapoura", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": INDERAPURA_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Indrapoura", "destination_name_raw": "Battavia",
            "ship_name": "schip Wesel",
            "captain": "oppercoopman Pieter de Gojer",
            "tonnage": None, "year": 1648,
            "departure_date": None, "arrival_date": "1648-08-09",
            "total_gulden": None, "main_product": None,
            "all_products": (
                "TANPA peper, alasan sama dgn fluijt de Noortstarre dari Sillida (sengketa harga "
                "kain, kejadian bareng dilaporkan halaman sumber sama). Tanggal arrival "
                "diinferensi dari OCR 'gendo' -- caveat presisi tanggal."
            ),
            "cargo_count": 0, "destination": "Battavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": TIKU_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Ticco ende Priaman", "destination_name_raw": "Battavia",
            "ship_name": "fluijtschip de Wolff",
            "captain": None,
            "tonnage": None, "year": 1648,
            "departure_date": None, "arrival_date": "1648-09-25",
            "total_gulden": None, "main_product": "peper",
            "all_products": (
                "182 bhaar peper ('nietmeer dan' -- dianggap sedikit) + banyak kain tak laku "
                "terjual. Sumber sebut asal 'Ticco ende Priaman' bersamaan (2 pelabuhan, 1 "
                "kapal) -- origin_id dicatat Tiku krn disebut lebih dulu, CAVEAT ambigu."
            ),
            "cargo_count": 1, "destination": "Battavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": TIKU_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Ticco en Priaman", "destination_name_raw": "Battavia",
            "ship_name": "fluijt den Swarten Beer",
            "captain": "coopman Hendrick Craijer",
            "tonnage": None, "year": 1648,
            "departure_date": None, "arrival_date": "1648-12-04",
            "total_gulden": None, "main_product": None,
            "all_products": (
                "'goede partie' -- rincian kargo terpotong OCR di batas halaman sumber, tak bisa "
                "direkonstruksi. Hendrick Craijer nama sama yg dibela dlm surat panglima Bhandar "
                "Galiffa Maret 1648 (lihat atjeh_trade_records). Origin 'Ticco en Priaman' "
                "ambigu sama spt fluijtschip de Wolff -- origin_id dicatat Tiku."
            ),
            "cargo_count": 0, "destination": "Battavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
    ]


def main():
    records = build_voyage_records()

    engine = create_engine(DATABASE_SYNC_URL, future=True)
    from models import Voyage

    added, skipped = 0, 0
    with Session(engine) as session:
        for rec in records:
            existing = session.execute(
                select(Voyage.id).where(and_(
                    Voyage.source == rec["source"],
                    Voyage.origin_id == rec["origin_id"],
                    Voyage.destination_id == rec["destination_id"],
                    Voyage.ship_name == rec["ship_name"],
                    Voyage.departure_date.is_(rec["departure_date"]) if rec["departure_date"] is None
                        else Voyage.departure_date == rec["departure_date"],
                    Voyage.arrival_date.is_(rec["arrival_date"]) if rec["arrival_date"] is None
                        else Voyage.arrival_date == rec["arrival_date"],
                ))
            ).scalar_one_or_none()

            if existing is not None:
                print(f"Sudah ada (id={existing}): {rec['ship_name']} {rec['origin_name_raw']}->{rec['destination_name_raw']} -- dilewati")
                skipped += 1
                continue

            session.execute(Voyage.__table__.insert(), [rec])
            added += 1
            print(f"Ditambahkan: {rec['ship_name']} {rec['origin_name_raw']}->{rec['destination_name_raw']} ({rec['departure_date'] or rec['arrival_date']})")

        session.commit()

    print("=" * 60)
    print(f"{added} baris baru, {skipped} dilewati (idempotent)")
    print("=" * 60)

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:voyages")
        print(f"cache voyages di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
