"""
seed_linimasa_events.py

Muat data/research/linimasa_events.csv (peristiwa suksesi/politik kekuasaan
Atjeh atas pantai barat Sumatra, dari Sultan Iskandar Muda sampai Traktat
Painan 1663 dan pengusiran Atjeh 1664-1665, sampai penyerahan Sillida 1667 &
traktat Barus 1681) ke tabel linimasa_events. Idempotent -- truncate & reload
tiap run (dataset kecil, hand-curated, sama pola dgn seed_atjeh_trade.py).

Dua sumber pipeline campur di CSV ini -- dibedakan via source_document:
  - "1624-1629" | "1631-1634" | "1636" | "1637" | "1643-1644" | "1647-1648" |
    "1656-1657": didistilasi dari baris direction='politik' di
    atjeh_trade_records (OCR PDF docs/ kita, ejaan asli VOC-Belanda
    dipertahankan di text_asli). Baris 1624-1629 (1625) berisi klaim
    yurisdiksi TERLUAS -- event TERTUA di linimasa. Baris 1656-1657
    mengungkap PERANG TERBUKA VOC-Atjeh, 6 tahun sebelum Traktat Painan.
    GOTCHA: SETIAP kali atjeh_trade_records dapat volume baru dgn baris
    politik, cek juga apakah perlu didistilasi ke sini -- jangan cuma proses
    volume yg lagi disisir sesi itu (kejadian nyata: 1624-1629 & 1636
    terlewat berbulan-bulan sampai user menegur).
  - "1661" | "1663" | "1664" | "1665" | "1681": dari
    docs/thesis/dr/korpus_tema_slim.csv (corpus GLOBALISE/Huygens TERPISAH,
    sudah diterjemahkan Indonesia) -- text_asli di sini BUKAN OCR Belanda,
    melainkan kutipan terjemahan Indonesia. Provenance (corpus_id asal)
    dicatat eksplisit di kolom notes tiap baris. TEMUAN BESAR baris 1681:
    traktat Barus -- bukti Atjeh-Barus PERTAMA di seluruh korpus riset.

Jalankan: docker compose exec backend python seed_linimasa_events.py
"""
import csv
import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

_BASE = Path(__file__).parent.parent
CSV_CANDIDATES = [
    Path("/app/data/research/linimasa_events.csv"),
    _BASE / "data" / "research" / "linimasa_events.csv",
]
CSV_FILE = next((c for c in CSV_CANDIDATES if c.exists()), None)

ALLOWED_SOURCE_DOCUMENTS = {"1624-1629", "1631-1634", "1636", "1637", "1643-1644", "1647-1648", "1656-1657", "1659", "1661", "1663", "1664", "1665", "1681", "CD1", "CD2", "CD3", "CD4", "CD5", "CD6", "buku-padang-1718", "buku-vogel-1690", "eic-bl-ior-g35", "gm-vol04-05", "lancaster-1601-1603", "kathirithamby-1965", "botham-letter-1781"}
ALLOWED_EVENT_TYPES = {"suksesi", "perjanjian", "konflik", "diplomasi", "administratif"}
ALLOWED_ERAS = {"klaim-awal", "ratu-puncak", "perang-damai", "retak-painan", "pengusiran-penataan"}
# Model 2 rantai Markov `dominion_status` (docs/prd/prd-atlas-power-model.md §3.2,
# docs/prd/prd-pemodelan-kekuasaan-dagang.md §6) -- kolom OPSIONAL per baris (banyak
# event teknis/multi-lokasi/fort-di-luar-roster sengaja NULL, bukan wajib diisi).
# Backfill CSV dikerjakan BERTAHAP di sesi terpisah (PRD §6), bukan skrip ini.
ALLOWED_DOMINION_STATUS = {
    "aceh_dominion", "voc_alliance", "independence", "relapse_aceh",
    "foreign_orbit", "voc_withdrawal", "internal_conflict",
}
# Babak naratif Fase 1 /linimasa (docs/prd/prd-linimasa-kronik-pantai-barat.md) --
# label/headline tiap era ada di frontend/map_app/views.py ERAS dict, BUKAN di sini
# (data event vs copy editorial sengaja dipisah). Rentang tahun berbasis data
# yg BENAR2 ada, bukan skema 1600-1690 design spec sumber.
#
# source_document="CD1" (2026-07-14): docs/CD1.pdf, Corpus Diplomaticum
# Neerlando-Indicum jilid I (ed. J.E. Heeres) -- kompilasi traktat/kontrak VOC,
# BEDA dari 9 volume Dagh-register (jurnal harian) & korpus_tema_slim.csv
# (GLOBALISE, sudah diterjemahkan). CD1 tetap OCR pipeline kita sendiri, ejaan
# VOC-Belanda asli dipertahankan -- TAPI buku ini juga berisi anotasi editorial
# modern (footnote Heeres) yg kadang jadi satu-satunya sumber suatu fakta (mis.
# identitas "Iskander Tsani"/Iskandar Thani) -- baris begitu ditandai eksplisit
# "catatan editor" di notes, beda dari kutipan traktat periode VOC asli. Mundurkan
# titik awal linimasa dari 1625 ke 1600 (2 traktat VOC-Atjeh pertama, 1600 & 1607).
#
# source_document="CD2" (2026-07-15): docs/CD2.pdf, Corpus Diplomaticum
# Neerlando-Indicum jilid II -- lanjutan kronologis CD1 (~1655-1673), lensa
# sisir tol/pajak & hadiah diplomasi. 14 event baru, termasuk RANGKAIAN
# pelepasan diri pantai barat dari Atjeh (Indrapoura 1663, Sillida 1667,
# Barus 1668, Priaman 1671, Cinkel/Singkil 1672) -- semua pakai frasa "kuk tak
# tertahankan" (onverdraeglijck jock). Beberapa baris CD2 MELENGKAPI event yg
# sudah ada dari source_document lain (mis. 1663 Songypagouers CD2 melengkapi
# 'Traktat Painan' dari korpus_tema_slim.csv dgn teks traktat primer) --
# ditandai eksplisit di notes sbg pelengkap, BUKAN duplikat/pengganti. Traktat
# Barus 1668 (CD2) mundurkan bukti Aceh-Barus dari 1681 -- caveat lama "Barus
# nihil sampai 1681" di riset_atjeh.html & sini WAJIB update.
#
# source_document="CD3" (2026-07-15): docs/CD3.pdf, Corpus Diplomaticum
# Neerlando-Indicum jilid III -- lanjutan kronologis CD2 (~1678-1690), volume
# PALING PADAT sejauh ini (18 event baru). Siklus berulang pemberontakan-
# tunduk pantai barat (Priaman, Tiku, Bajang, Kotta-tengah, Baros, Singkil),
# puncaknya traktat aliansi UMUM 29 Agustus 1680 yg menyatukan SEMUA
# penguasa westkust dari Seblat sampai Air Bangis di bawah VOC. MAJUKAN
# titik akhir linimasa dari 1681 ke 1690 (era "pengusiran-penataan" diperluas
# 1664-1681 -> 1664-1690). Paruh kedua volume: konteks baru persaingan
# Inggris (diusir dari Bantam) mencoba pijakan westkust. Beberapa baris
# MELENGKAPI event lama (Sillida 1667, Barus 1681, Cinkel 1672) dgn detail
# lanjutan -- ditandai eksplisit, bukan duplikat.
#
# source_document="CD4" (2026-07-15): docs/CD4.pdf, Corpus Diplomaticum
# Neerlando-Indicum jilid IV -- lanjutan kronologis CD3, rentang jauh lebih
# panjang (1693-1716). 20 event baru, volume TERPADAT sejauh ini. Ekspedisi
# vaandrig Johannes Sas (Jan-Mei 1693) menumpas "lorrendraeyers" Aceh, MELUAS
# ke pulau Nias (7 traktat terpisah, termasuk serbuan benteng Aceh di Gido,
# 15 Maret 1693) -- jangkauan geografis terjauh utara di seluruh korpus kami.
# Baros direstrukturisasi total 1694 pasca-pembunuhan pegawai VOC. Padang &
# Sillida lepas hak pungut "salimoet" demi harga peper naik (1698). Priaman
# dkk RELAPS ke Aceh ~20 tahun (jeda relaps terlama tercatat), ditundukkan
# ulang 1712. Indrapoera sempat berpaling ke Inggris pasca-1684, kembali
# minta perlindungan VOC 1716. MAJUKAN titik akhir linimasa dari 1690 ke
# 1716 (era "pengusiran-penataan" diperluas 1664-1690 -> 1664-1716).
# Beberapa baris MELENGKAPI event lama (Baros 1694 x Minuassa 1698/1707,
# Indrapoera 1660/1663, Padang 1680) -- ditandai eksplisit, bukan duplikat.
#
# source_document="CD5" (2026-07-15): docs/CD5.pdf, Corpus Diplomaticum
# Neerlando-Indicum jilid V (~1727-1741). Volume PALING SEDIKIT konten
# westkust/Aceh sejauh ini -- cuma 4 event, buku didominasi Ternate/Molukka/
# Persia/Bantam/Koromandel. Dua traktat aliansi Tigablas & Doeapoeloeh-Kotta
# (1727 & 1741) -- yang kedua di tengah PEMBERONTAKAN BESAR 1740 (Paoeh/
# Kotta-Tengah/Priaman bersatu di bawah Abdul Jalil, VOC lepas benteng
# Priaman). Traktat Pasariboe-Baros 1731 & sewa tambang emas Sillida 1737
# (VOC lepas operasi langsung tapi pertahankan hak kedaulatan fiskal). MAJUKAN
# titik akhir linimasa dari 1716 ke 1741 (era "pengusiran-penataan" diperluas
# 1664-1716 -> 1664-1741).
#
# source_document="CD6" (2026-07-15): docs/CD6.pdf, Corpus Diplomaticum
# Neerlando-Indicum jilid VI (~1755-1775). 8 event baru. Dibuka RANGKAIAN
# RENOVASI BESAR (Feb 1755-Jan 1756): cemas aktivitas Inggris, VOC perbarui
# traktat ~30 negeri di SELURUH pantai barat dalam <1 tahun. Perang Tujuh
# Tahun (1756-63) merembet westkust: benteng Natal direbut Inggris lalu
# Prancis (1760), diserahkan ke VOC lewat penguasa lokal -- Natal formal
# kembali ke VOC stlh sempat menyimpang ke pengaruh Inggris. Traktat
# Tigablas Cottas (1763): hadiah tahunan VOC demi jaga jalur gunung.
# Pemberontakan Klein-Pasaman (1766-67, bukan faksi Aceh) ditumpas. VOC
# tarik mundur dari loge Baros (1775) krn kalah saing Inggris Bengkulu.
# MAJUKAN titik akhir linimasa dari 1741 ke 1775 (era "pengusiran-penataan"
# diperluas 1664-1741 -> 1664-1775).
#
# source_document="buku-padang-1718" (2026-07-24, docs/prd/prd-atlas-
# power-model-fase2-roster.md, Fase 2): Padang Abad XVII-XVIII (Yusri &
# Deddy Arsya, 2024, review Prof. Gusti Asnan), docs/thesis/Padang Abad
# XVII-XVIII FINISH.pdf hlm 237-238 -- SUMBER SEKUNDER-AKADEMIK, BUKAN
# korpus arsip primer CD/Daghregister kami sendiri, jadi source_document
# terpisah (jangan dikira OCR CD). 7 event Koto Tangah (1660-1755) MELENGKAPI
# 2 event CD3 yg sudah ada (1680/1682, source_document="CD3") -- sebelum
# 1660 Koto Tangah justru musuh terberat Panglima Aceh (tak ada wakil Aceh
# ditempatkan di sana, beda dari Pariaman yg sepenuhnya dikuasai Aceh).
# 1670 (dominion_status="internal_conflict", BUKAN "relapse_aceh" -- sumber
# tak sebut Aceh di episode ini, beda dari insiden 1665 yg eksplisit
# dihasut Aceh) Koto Tangah memberontak, nagari dibakar VOC. Traktat 8 Sep
# 1671 kemungkinan cocok Corpus Diplomaticum CCCXXXI "Sumatra's Westkust,
# 8-10 September 1671" (dicek dari bibliografi buku hlm 355, BELUM
# diverifikasi teks traktat lengkap).
#
# source_document="buku-vogel-1690" (2026-07-24): Johann Wilhelm Vogel,
# Ost-Indianische Reise-Beschreibung (~1690), docs/bsb10468472.txt (scan OCR
# Fraktur, Bayerische Staatsbibliothek, 828 hlm) -- memoar PRIBADI mantan
# Fähnrich & Berg-Hauptmann (kepala tambang) VOC di Sillida (Salido), BUKAN
# arsip resmi VOC maupun historiografi akademik modern -- tier sumber
# terpisah lagi dari CD/buku-padang-1718. Mengisi celah 1664-1716 Inderapura:
# Sultan Mametchia (nama sama muncul CD4/1662 & CD4/1716 existing) membelot
# VOC ke perlindungan Inggris th 1686 krn Komandan Joan van Leene (nama sama
# muncul CD3/1682 Kotta-tengah) otoriter & tak beri bantuan lawan bangsawan
# pemberontak -- CD4/1716 (event existing) sendiri sebut "sejak 1684" tanpa
# tahun presisi, Vogel MELENGKAPI dgn tahun eksak. Cross-corroborasi
# independen ganda: (a) identitas Sultan Mametchia, (b) watak kontroversial
# Van Leene -- 2 sumber tak berkaitan (arsip vs memoar pribadi) sepakat.
#
# source_document="eic-bl-ior-g35" (2026-07-24): British Library, India
# Office Records, seri G/35 f.198 (via platform AmDigital,
# eastindiacompany.amdigital.co.uk) -- surat dari York Fort (Bengkulu/
# Bencoolen, pos EIC), tertanggal 18/22 Sept 1686, docs/BL_IOR_G_35_198.txt
# (transkripsi Inggris modern, disediakan user). Tier sumber KE-4 yg
# terpisah dari CD/buku-padang-1718/buku-vogel-1690 -- arsip Inggris (EIC),
# bukan Belanda maupun memoar Jerman. Isinya laporan bahwa seseorang
# mengaku "Raja Manacabo (Minangkabau)" memberi konsesi dagang Barus-Silebar
# ke Inggris, dipakai Mr. Potts membenarkan pendirian pos EIC di Batang
# Capas -- lalu direbut VOC. CROSS-VALIDASI independen thd row
# Painan/1686/buku-vogel-1690 yg SUDAH ADA (VOC serbu Batang Capas 1 Sept
# 1686, versi Jerman/Vogel) -- surat Inggris ini ditulis 18-22 Sept 1686,
# PERSIS beberapa minggu SESUDAH peristiwa yg sama, dari sisi yg kalah.
# "Raja Manacabo" kemungkinan besar tokoh yg sama dgn "Jang de Pertuan
# (pangeran Minangkabau)" di CD3/23-Jan-1687 (Painan) yg membatalkan
# SEMUA konsesi tanah ke Inggris 4 bulan kemudian -- ejaan beda tapi
# gelar & konteks (raja Minangkabau, urusan konsesi Inggris) cocok;
# BELUM dipastikan identik, dicatat sbg hipotesis kuat bukan fakta.
# Fort York sendiri BUKAN bagian jaringan VOC/roster "westkust" inti,
# ditambahkan krn permintaan eksplisit user (di luar cakupan geografis
# normal proyek, selatan Silebar).
#
# source_document="gm-vol04-05" (2026-07-24): Generale Missiven volume 04
# (1675-1684) & 05 (1686-1694), docs/thesis/GM/gm_corpus_filtered_1660_1789.csv
# -- edisi RGP resmi (Belanda asli + terjemahan Indonesia + catatan editorial
# ilmiah), BUKAN OCR mentah/memoar pribadi -- tier setara CD1-CD6 (arsip
# resmi VOC), terpisah dari buku-vogel-1690 (memoar) & eic-bl-ior-g35 (EIC).
# Ditemukan via riset dataverse.nl (GLOBALISE index Generale Missiven
# 1618-1793) yg mengarah balik ke corpus GM yg SUDAH ada di proyek ini,
# blm pernah disisir utk 1675-1694. Cross-corroborasi kuat dgn buku-vogel-1690:
# Bilandre/Achterbergh (tanggal pulang persis sama, April/Nov 1681), Olits
# (lemah 1681, wafat 1682), Sire Narra (Gubernur Sillida, sama nama).
# 3 event baru:
#   (a) Koto Tangah 1676: serangan Koto Tangah+Pauh ke Padang (Juni), Sire
#       Narra dituduh korespondensi rahasia mendukung "Nachoda Poety" --
#       kemungkinan BESAR org yg sama dgn "Gouverneur Pouti" yg dieksekusi
#       1682 (CD3, sudah di data) krn muncul dlm konteks Cottetenge yg sama
#       persis di paragraf ini -- BELUM 100% pasti (gelar "Nachoda"=nakhoda
#       kapal/pedagang, beda dari "Gouverneur"), dicatat sbg hipotesis kuat.
#   (b) Bayang 22 Des 1687: traktat Radja Itam/Hitam + 12 penghulu dgn
#       komisaris Lobs (Corpus III referensi editorial, blm diverifikasi
#       teks traktat lengkap) -- pasca Radja Bayang sempat lari ke gunung.
#   (c) Inderapura ~1688: rumor SIMPANG SIUR (dicatat VOC sendiri sbg 2
#       versi bertentangan) -- Sultan Mametchia lari ke gunung ditinggal
#       rakyatnya, diganti Radja Boedjang yg tak dikenal VOC; ATAU Mametchia
#       & Majutte "berdamai" krn tak aman baginya tinggal. Dicatat sbg
#       ketidakpastian eksplisit, BUKAN salah satu rumor dipilih jadi fakta.
#
# source_document="lancaster-1601-1603" (2026-07-24): James Lancaster,
# "The Voyages of Sir James Lancaster to Brazil and the East Indies,
# 1591-1603", ed. Sir William Foster, Hakluyt Society 1940 (docs/The
# voyages of Sir James Lancaster.docx). Akun pelayaran EIC PERTAMA (armada
# 4 kapal, 1601-1603) -- tier sumber TERPISAH lagi: Inggris, PRA-VOC (VOC
# baru berdiri 1602, saat armada ini sedang berlayar), jauh lebih tua dari
# semua sumber lain di korpus (CD1 mulai 1600 tp itu klaim yurisdiksi
# retrospektif, bukan akun mata-kaki langsung). November 1602: armada
# singgah di Priaman dlm perjalanan pulang dari Aceh, temukan kapal Susan
# (dikirim jenderal lebih dulu dari Aceh) sudah muat ~600 bahar lada + 66
# bahar cengkeh. Priaman digambarkan TANPA komoditas lain selain emas
# (debu/butiran dicuci dari pasir sungai pasca hujan) & lada yg didatangkan
# dari "Manangcabo" (Minangkabau) 8-10 liga pedalaman -- konfirmasi paling
# awal di korpus soal jalur dagang emas+lada Priaman-Minangkabau, 55 tahun
# sblm event Pariaman tertua existing (1657). TIDAK ada penguasa politik
# Priaman disebut eksplisit dlm akun ini (murni deskripsi dagang) --
# dominion_status SENGAJA dikosongkan, bukan diasumsikan.
#
# source_document="kathirithamby-1965" (2026-07-25): Jeyamalar Kathirithamby,
# "British West Sumatra During the Presidency Period, 1760 to 1785", PhD
# thesis, University of London, Februari 1965 (docs/EIC_alternatif.json, OCR
# 378 hlm, judul_file asli "EIC.pdf"). Sisir penuh via 6 subagent paralel --
# tier sumber akademik SEKUNDER (spt buku-padang-1718) tapi PERSPEKTIF EIC,
# bukan VOC. Temuan utama: rangkaian EIC merebut Padang & Pulau Cingkuak dari
# VOC Agustus 1781, kuasai s.d. dikembalikan via traktat damai 1784/85 --
# celah besar yg blm ada di data (Padang selama ini dianggap "selalu
# voc_alliance"). Cross-corroborasi dgn source_document="botham-letter-1781"
# (surat asli pelaku langsung).
#
# source_document="botham-letter-1781" (2026-07-25): Henry Botham (Residen
# EIC) kepada "My Lord" [Direktur/Gubernur Jenderal EIC], Fort Marlborough,
# 12 Oktober 1781 -- surat asli, docs/HenryBotham (transkripsi user dari
# National Library of Australia, nla.obj-2387557233). Sumber PRIMER tier
# tertinggi (pelaku langsung menulis 2 bulan sesudah kejadian) -- BEDA dari
# Kathirithamby (akademik sekunder) meski cerita sama. Botham sendiri sebut
# rebut Padang TANPA perlawanan (gubernur VOC serahkan begitu diminta), lalu
# ambil alih 3 subordinat: "Prols Cinquo" (=Pulau Cingkuak), "Priamang"
# (=Pariaman), dan "Ayer Adjee" -- identitas "Ayer Adjee" BELUM PASTI, diduga
# Air Haji (fonetik lebih cocok drpd Air Bangis) tapi dicatat sbg dugaan,
# bukan fakta pasti.


def _clean(v):
    v = (v or "").strip()
    return v or None


def _int(v):
    v = (v or "").strip()
    if not v:
        return None
    try:
        return int(v)
    except ValueError:
        return None


def parse_row(row):
    source_document = _clean(row.get("source_document"))
    if source_document not in ALLOWED_SOURCE_DOCUMENTS:
        raise ValueError(f"source_document '{source_document}' tidak valid, harus salah satu dari {ALLOWED_SOURCE_DOCUMENTS}")

    source_page = _clean(row.get("source_page"))
    if not source_page:
        raise ValueError("source_page wajib ada")

    event_type = _clean(row.get("event_type"))
    if event_type not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"event_type '{event_type}' tidak valid, harus salah satu dari {ALLOWED_EVENT_TYPES}")

    title = _clean(row.get("title"))
    if not title:
        raise ValueError("title wajib ada")

    text_asli = _clean(row.get("text_asli"))
    if not text_asli:
        raise ValueError("text_asli wajib ada -- jejak verifikasi ke sumber")

    era_slug = _clean(row.get("era_slug"))
    if era_slug not in ALLOWED_ERAS:
        raise ValueError(f"era_slug '{era_slug}' tidak valid, harus salah satu dari {ALLOWED_ERAS}")

    dominion_status = _clean(row.get("dominion_status"))
    if dominion_status is not None and dominion_status not in ALLOWED_DOMINION_STATUS:
        raise ValueError(f"dominion_status '{dominion_status}' tidak valid, harus salah satu dari {ALLOWED_DOMINION_STATUS} atau kosong")

    tags_raw = _clean(row.get("tags"))  # pipe-separated di CSV, mis. "tol|hadiah" (PRD §3.3)
    tags = [t.strip() for t in tags_raw.split("|") if t.strip()] if tags_raw else None

    return {
        "source_document": source_document,
        "source_page": int(source_page),
        "book_page": _clean(row.get("book_page")),
        "event_date_raw": _clean(row.get("event_date_raw")),
        "year": _int(row.get("year")),
        "event_type": event_type,
        "ruler_actor": _clean(row.get("ruler_actor")),
        "title": title,
        "era_slug": era_slug,
        "fort_name": _clean(row.get("fort_name")),  # resolve ke fort_id di main() -- butuh query DB, bukan hardcode
        "dominion_status": dominion_status,
        "tags": tags,
        "text_asli": text_asli,
        "notes": _clean(row.get("notes")),
        "confidence_flag": "unverified",
    }


def main():
    if CSV_FILE is None:
        raise RuntimeError(f"linimasa_events.csv tidak ditemukan di: {CSV_CANDIDATES}")
    print(f"Sumber : {CSV_FILE}")

    records = []
    with CSV_FILE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            records.append(parse_row(row))
    print(f"Terbaca: {len(records)} baris")

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    for r in records:
        r["created_at"] = now

    engine = create_engine(DATABASE_SYNC_URL, future=True)
    from models import LinimasaEvent, Fort  # tabel dibuat via migration 009 / 011

    with Session(engine) as session:
        # resolve fort_name -> fort_id via query Fort by name (bukan hardcode, PRD §6) --
        # fort_id TETAP NULL kalau fort_name kosong (event teknis/multi-lokasi/di luar
        # roster 13, §3.1), tapi ERROR kalau fort_name diisi tapi tak match satu pun
        # nama di roster -- data integrity, bukan silently NULL-kan typo nama fort.
        fort_name_to_id = dict(session.execute(text("SELECT name, id FROM forts")).all())
        for r in records:
            fort_name = r.pop("fort_name")
            if fort_name is None:
                r["fort_id"] = None
            elif fort_name in fort_name_to_id:
                r["fort_id"] = fort_name_to_id[fort_name]
            else:
                raise ValueError(f"fort_name '{fort_name}' tidak ditemukan di tabel forts -- cek ejaan atau roster 13 fort")

        session.execute(text("TRUNCATE TABLE linimasa_events RESTART IDENTITY"))
        session.execute(LinimasaEvent.__table__.insert(), records)
        session.commit()
        after = session.execute(text("SELECT COUNT(*) FROM linimasa_events")).scalar()

        by_type = session.execute(text(
            "SELECT event_type, COUNT(*) FROM linimasa_events GROUP BY event_type ORDER BY event_type"
        )).all()
        by_document = session.execute(text(
            "SELECT source_document, COUNT(*) FROM linimasa_events GROUP BY source_document ORDER BY source_document"
        )).all()
        by_era = session.execute(text(
            "SELECT era_slug, COUNT(*) FROM linimasa_events GROUP BY era_slug ORDER BY MIN(year)"
        )).all()
        n_dominion_status = session.execute(text(
            "SELECT COUNT(*) FROM linimasa_events WHERE dominion_status IS NOT NULL"
        )).scalar()
        n_fort_id = session.execute(text(
            "SELECT COUNT(*) FROM linimasa_events WHERE fort_id IS NOT NULL"
        )).scalar()

    print("=" * 60)
    print(f"linimasa_events: {after} baris")
    print(f"per tipe: {dict(by_type)}")
    print(f"per volume: {dict(by_document)}")
    print(f"per era: {dict(by_era)}")
    print(f"dominion_status terisi: {n_dominion_status}/{after}  |  fort_id terisi: {n_fort_id}/{after}  "
          f"(backfill BERTAHAP per docs/prd/prd-pemodelan-kekuasaan-dagang.md §6, 0 itu normal sblm backfill jalan)")
    print("=" * 60)

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:research_linimasa")
        flushed_power = invalidate_prefix_sync("voc:forts-power-status")
        print(f"cache linimasa di-invalidate: {flushed} key | power-status: {flushed_power} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
