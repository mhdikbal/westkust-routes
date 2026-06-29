from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Index
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


class CommodityGlossary(Base):
    __tablename__ = "commodity_glossary"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    term          = Column(String(200), nullable=False, unique=True, index=True)
    term_display  = Column(String(200), nullable=True)
    variants      = Column(ARRAY(Text), nullable=True)
    definition_nl = Column(Text, nullable=True)
    definition_id = Column(Text, nullable=True)
    category      = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<CommodityGlossary(term='{self.term}')>"
