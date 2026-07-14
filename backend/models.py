from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Index, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INT4RANGE, JSONB, ARRAY
from geoalchemy2 import Geometry
from database import Base


class Fort(Base):
    __tablename__ = "forts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    color = Column(String(20), nullable=False, default="#c0392b")
    description = Column(Text, nullable=True)
    # "departure" | "arrival" | "both"
    port_type = Column(String(20), nullable=False, server_default="departure")
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    # AMH enrichment fields (US-06 — Sprint ATM)
    nama_historis   = Column(String(255), nullable=True)
    designasi_voc   = Column(String(100), nullable=True)
    fungsi_historis = Column(Text,        nullable=True)
    periode_aktif   = Column(INT4RANGE,   nullable=True)
    amh_url         = Column(String(500), nullable=True)
    amh_images      = Column(JSONB,        nullable=True)

    # Relationships
    outbound_voyages = relationship(
        "Voyage", 
        foreign_keys="Voyage.origin_id", 
        back_populates="origin_fort", 
        cascade="all, delete-orphan"
    )
    inbound_voyages = relationship(
        "Voyage", 
        foreign_keys="Voyage.destination_id", 
        back_populates="destination_fort", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Fort(name='{self.name}', type='{self.port_type}')>"


class Voyage(Base):
    __tablename__ = "voyages"

    id = Column(Integer, primary_key=True, index=True)
    voyage_ref = Column(Integer, unique=True, nullable=True, index=True)  # Original ID from JSON
    origin_id = Column(Integer, ForeignKey("forts.id", ondelete="CASCADE"), nullable=True, index=True)
    destination_id = Column(Integer, ForeignKey("forts.id", ondelete="CASCADE"), nullable=True, index=True)
    
    origin_name_raw = Column(String(200), nullable=True)
    destination_name_raw = Column(String(200), nullable=True)
    
    ship_name = Column(String(200), nullable=False)
    captain = Column(String(200), nullable=True)
    tonnage = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True, index=True)
    
    departure_date = Column(String(30), nullable=True)   # ISO date string from JSON
    arrival_date = Column(String(30), nullable=True)      # ISO date string from JSON
    
    total_gulden = Column(Float, nullable=True)
    main_product = Column(String(200), nullable=True)
    all_products = Column(Text, nullable=True)
    cargo_count = Column(Integer, nullable=True)          # Number of cargo items
    
    # Redundant field for backward compatibility/simplicity
    destination = Column(String(200), nullable=True)
    
    duration_days = Column(Integer, nullable=True)
    direction = Column(String(20), nullable=True, index=True)  # "outbound" or "inbound"
    source_url = Column(Text, nullable=True)
    # Provenance (P0.3b, docs/prd-cleaning-daghregister-1660-1669.md): "bgb_huygens" (default,
    # data terstruktur existing) | "daghregister_batavia" | "globalise_obp" (hasil promosi staging)
    source = Column(String(50), nullable=False, server_default="bgb_huygens", index=True)

    # Relationship to cargo items
    cargo_items = relationship("CargoItem", back_populates="voyage", cascade="all, delete-orphan")

    # Relationships
    origin_fort = relationship("Fort", foreign_keys=[origin_id], back_populates="outbound_voyages")
    destination_fort = relationship("Fort", foreign_keys=[destination_id], back_populates="inbound_voyages")

    def __repr__(self):
        return f"<Voyage(ship='{self.ship_name}', {self.origin_name_raw} -> {self.destination_name_raw}, dir={self.direction})>"


class CargoItem(Base):
    """Individual cargo item carried on a voyage."""
    __tablename__ = "cargo_items"

    id = Column(Integer, primary_key=True, index=True)
    voyage_id = Column(Integer, ForeignKey("voyages.id", ondelete="CASCADE"), nullable=False, index=True)
    produk = Column(String(200), nullable=False, index=True)
    spesifikasi = Column(String(300), nullable=True)
    qty_asli = Column(String(100), nullable=True)
    unit = Column(String(50), nullable=True)
    nilai_numerik = Column(Float, nullable=True)
    gram = Column(Float, nullable=True)
    gulden_nl = Column(Float, nullable=True)
    gulden_india = Column(Float, nullable=True)
    catatan = Column(Text, nullable=True)

    # Relationship
    voyage = relationship("Voyage", back_populates="cargo_items")

    def __repr__(self):
        return f"<CargoItem(produk='{self.produk}', qty='{self.qty_asli}', unit='{self.unit}')>"


class ApiKey(Base):
    """API key per-notebook untuk endpoint ingesti staging (bukan untuk publik)."""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String(64), unique=True, nullable=False, index=True)  # sha256 hex digest
    label = Column(String(100), nullable=False)  # mis. "daghregister_colab", "globalise_colab"
    active = Column(String(10), nullable=False, server_default="true")  # "true"/"false" (String utk konsistensi migrasi sederhana)
    created_at = Column(String(30), nullable=False)

    def __repr__(self):
        return f"<ApiKey(label='{self.label}', active={self.active})>"


class StagingExtraction(Base):
    """Hasil ekstraksi mentah dari notebook Colab (Daghregister, GLOBALISE, dll),
    menunggu review manual sebelum di-promote ke Voyage/CargoItem resmi."""
    __tablename__ = "staging_extractions"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)
    external_ref = Column(String(200), nullable=False)
    batch_id = Column(String(36), nullable=True, index=True)

    text_indonesia = Column(Text, nullable=False)
    text_asli = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)

    confidence_flag = Column(String(20), nullable=False, server_default="unverified")
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(String(30), nullable=True)
    created_at = Column(String(30), nullable=False)

    __table_args__ = (
        Index("ix_staging_source_ref", "source", "external_ref", unique=True),
    )

    def __repr__(self):
        return f"<StagingExtraction(source='{self.source}', ref='{self.external_ref}', flag='{self.confidence_flag}')>"


class PortArrivalTally(Base):
    """Rekap kedatangan bulanan multi-kapal-tak-bernama dari daghregister_corpus.csv
    (record_type=port_tally_aggregate). Satu baris staging_extractions di-expand jadi
    banyak baris di sini -- satu per kelompok-pelabuhan-asal.
    Lihat docs/prd-port-tally-aggregate.md."""
    __tablename__ = "port_arrival_tallies"

    id = Column(Integer, primary_key=True, index=True)
    staging_extraction_id = Column(Integer, ForeignKey("staging_extractions.id"), nullable=False, index=True)
    volume = Column(String(100), nullable=False)
    tanggal_perkiraan = Column(String(50), nullable=True)

    origin_port_raw = Column(String(100), nullable=False)
    origin_fort_id = Column(Integer, ForeignKey("forts.id"), nullable=True, index=True)

    ship_count = Column(Integer, nullable=True)
    person_count = Column(Integer, nullable=True)

    cargo_text = Column(Text, nullable=False)
    cargo_items_json = Column(JSONB, nullable=True)

    confidence_flag = Column(String(20), nullable=False, server_default="unverified")
    created_at = Column(String(30), nullable=False)

    def __repr__(self):
        return f"<PortArrivalTally(origin='{self.origin_port_raw}', ships={self.ship_count})>"


class ResearchThemeRow(Base):
    """Satu baris hasil klasifikasi zero-shot tema-korpus (GLOBALISE + Dagh-register),
    sumber Sankey tema-korpus (namespace `research`, thesis-only — BUKAN peta publik).
    Muat dari data/research/korpus_tema_slim.csv via seed_research_tema.py.
    Lihat docs/prd-sankey-tema-korpus.md + docs/sprint-sankey-tema-korpus.md (SNK-1).

    Teks yang diklasifikasi model = kolom `text` (Indonesia). `text_asli` daghregister
    berisi cuplikan Belanda; utk GLOBALISE berisi POINTER inventaris (OCR penuh tak
    disimpan — lihat DATA-SNK-1). Idempotent by `corpus_id`."""
    __tablename__ = "research_theme_rows"

    id = Column(Integer, primary_key=True, index=True)
    corpus_id = Column(Integer, unique=True, nullable=False, index=True)  # natural key dari pipeline
    corpus_asal = Column(String(20), nullable=False, index=True)          # "globalise" | "daghregister"
    source = Column(String(50), nullable=True)                            # "globalise_obp" | "daghregister_batavia"
    volume = Column(String(200), nullable=True)
    inventaris_ref = Column(String(100), nullable=True)                   # "NL-HaNA_1.04.02_<n>" (globalise)

    tanggal_perkiraan = Column(Text, nullable=True)                      # free-form; globalise bisa rentetan tanggal panjang (>300 char)
    tahun = Column(Integer, nullable=True, index=True)                    # NULL = tak bertahun
    dekade = Column(Integer, nullable=True, index=True)                   # NULL -> bucket "Tak bertahun" di endpoint

    pelabuhan_disebut = Column(String(300), nullable=False)               # raw multi-port "; "-joined; explode di endpoint
    tema_dominan = Column(String(30), nullable=False, index=True)
    skor_dominan = Column(Float, nullable=True)
    low_confidence = Column(Boolean, nullable=False, server_default="false", index=True)

    # 7 skor tema independen (multi_label) — untuk audit/drill-down
    skor_pdr_drainase  = Column(Float, nullable=True)
    skor_etr_retensi   = Column(Float, nullable=True)
    skor_hak_adat      = Column(Float, nullable=True)
    skor_pelayaran     = Column(Float, nullable=True)
    skor_sengketa      = Column(Float, nullable=True)
    skor_syahbandar    = Column(Float, nullable=True)
    skor_tidak_relevan = Column(Float, nullable=True)

    text = Column(Text, nullable=False)        # Indonesia — yang benar-benar diklasifikasi model
    text_asli = Column(Text, nullable=True)    # cuplikan Belanda (DR) / pointer inventaris (globalise)

    __table_args__ = (
        Index("ix_research_theme_dekade_tema", "dekade", "tema_dominan"),
    )

    def __repr__(self):
        return f"<ResearchThemeRow(corpus_id={self.corpus_id}, tema='{self.tema_dominan}', dekade={self.dekade})>"


class AtjehTradeRecord(Base):
    """Baris hasil ekstraksi laporan dagang dari/ke/di Atjeh, sumber primer
    tujuh volume "Dagh-register gehouden int casteel Batavia" (docs/): 1643-1644,
    1631-1634, 1637, 1636, 1624-1629, 1644-1645, dan 1647-1648. Muat dari data/research/atjeh_trade.csv via
    seed_atjeh_trade.py. Baris direction='politik' adalah fakta politik/administratif
    (klaim yurisdiksi, penegakan tol, suksesi raja, status ratu), BUKAN transaksi
    dagang -- dipisah dari 'in_atjeh' (transaksi yg terjadi di Atjeh) 2026-07-13.

    commodity_raw/unit_raw/actor_raw SENGAJA memakai ejaan asli VOC-Belanda
    dari sumber (mis. "peper", "thin", "salpeter"), BUKAN terjemahan Indonesia --
    padanan/definisi ada di CommodityGlossary.term/variants, join manual saat perlu.

    confidence_flag='unverified' untuk semua baris awal: hasil pembacaan teks OCR
    PDF, belum dicocokkan ulang thd scan halaman asli (lihat memory
    feedback_verify_entity_extraction_before_trusting)."""
    __tablename__ = "atjeh_trade_records"

    id = Column(Integer, primary_key=True, index=True)

    source_document = Column(String(20), nullable=False, index=True)  # "1643-1644" | "1631-1634" | "1637" | "1636" | "1624-1629" | "1644-1645" | "1647-1648"
    source_page = Column(Integer, nullable=False, index=True)   # halaman PDF scan (source_document)
    book_page = Column(String(20), nullable=True)                # halaman cetak asli, jika diketahui
    entry_date_raw = Column(String(50), nullable=True)           # mis. "9 Mei 1644"; NULL = tak bertanggal jelas

    direction = Column(String(20), nullable=False, index=True)   # "naar_atjeh" | "van_atjeh" | "in_atjeh" | "politik"
    commodity_raw = Column(String(100), nullable=True, index=True)  # NULL = kargo kosong ("ledigh")
    quantity_raw = Column(String(50), nullable=True)
    unit_raw = Column(String(50), nullable=True)
    price_value = Column(Float, nullable=True)
    price_unit_raw = Column(String(50), nullable=True)

    actor_raw = Column(String(200), nullable=True)                # kapal/pedagang/bangsa terlibat
    text_asli = Column(Text, nullable=False)                       # cuplikan OCR mentah utk verifikasi

    confidence_flag = Column(String(20), nullable=False, server_default="unverified")
    notes = Column(Text, nullable=True)
    created_at = Column(String(30), nullable=False)

    def __repr__(self):
        return f"<AtjehTradeRecord(dir='{self.direction}', commodity='{self.commodity_raw}', p{self.source_page})>"


class LinimasaEvent(Base):
    """Peristiwa suksesi/politik kekuasaan Atjeh atas pantai barat Sumatra,
    dari Sultan Iskandar Muda sampai Traktat Painan 1663 -- sumber halaman
    `/linimasa`. Dimuat dari data/research/linimasa_events.csv via
    seed_linimasa_events.py.

    BERBEDA dari AtjehTradeRecord: scope tabel ini "peristiwa politik/suksesi"
    (event_type), bukan "dagang dari/ke/di Atjeh" (direction). Sebagian baris
    didistilasi dari baris direction='politik' di atjeh_trade_records (sumber
    docs/ PDF kita), sebagian lagi (source_document='1663') dari corpus
    TERPISAH docs/thesis/dr/korpus_tema_slim.csv (GLOBALISE/Huygens, sudah
    diterjemahkan) -- provenance dicatat eksplisit di kolom notes, TIDAK
    diduplikasi ke atjeh_trade_records.

    text_asli WAJIB (disiplin sama spt AtjehTradeRecord) -- setiap event harus
    tertelusur ke kutipan sumber, bukan klaim tanpa bukti. confidence_flag
    default 'unverified' krn OCR/terjemahan mentah, belum dicocokkan scan asli."""
    __tablename__ = "linimasa_events"

    id = Column(Integer, primary_key=True, index=True)

    source_document = Column(String(20), nullable=False, index=True)  # "1631-1634" | "1637" | "1643-1644" | "1647-1648" | "1663"
    source_page = Column(Integer, nullable=False, index=True)
    book_page = Column(String(20), nullable=True)
    event_date_raw = Column(String(50), nullable=True)   # mis. "10 Des 1632", "27 Maret 1663"; NULL = tak bertanggal jelas
    year = Column(Integer, nullable=True, index=True)     # utk sort/filter linimasa

    event_type = Column(String(20), nullable=False, index=True)  # "suksesi" | "perjanjian" | "konflik" | "diplomasi" | "administratif"
    ruler_actor = Column(String(200), nullable=True)      # mis. "Sultan Iskandar Muda", "coninginne van Atchin", "Songypagouers"
    title = Column(String(300), nullable=False)           # judul ringkas utk marker linimasa

    text_asli = Column(Text, nullable=False)               # kutipan verbatim wajib
    notes = Column(Text, nullable=True)

    confidence_flag = Column(String(20), nullable=False, server_default="unverified")
    created_at = Column(String(30), nullable=False)

    def __repr__(self):
        return f"<LinimasaEvent(type='{self.event_type}', year={self.year}, title='{self.title}')>"


class CommodityGlossary(Base):
    __tablename__ = "commodity_glossary"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    term          = Column(String(200), nullable=False, unique=True, index=True)
    term_display  = Column(String(200), nullable=True)
    variants      = Column(ARRAY(Text), nullable=True)
    definition_nl = Column(Text, nullable=True)
    definition_id = Column(Text, nullable=True)
    category      = Column(String(100), nullable=True)
    source_citation = Column(Text, nullable=True)  # rujukan definisi, mis. "VOC-Glossarium (IHNG, 2000)"; NULL = asal tak tercatat

    def __repr__(self):
        return f"<CommodityGlossary(term='{self.term}')>"
