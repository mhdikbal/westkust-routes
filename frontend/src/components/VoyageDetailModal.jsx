import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { X, Ship, Calendar, DollarSign, Package, MapPin, Compass, Clock, Anchor, ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

const DIRECTION_COLORS = {
  outbound: { color: "#00D4AA", label: "Keberangkatan (Outbound)", icon: "🚢" },
  inbound:  { color: "#FF6B6B", label: "Kedatangan (Inbound)", icon: "🏠" },
  transit:  { color: "#FFD93D", label: "Transit", icon: "🔄" },
};

// Product category colors for cargo badges
const PRODUCT_COLORS = {
  goud: "#FFD700",
  peper: "#e74c3c",
  kamfer: "#3498db",
  benzoe: "#9b59b6",
  lijfeigene: "#e67e22",
  kanon: "#7f8c8d",
  buskruit: "#2c3e50",
  default: "#00D4AA",
};

function getProductColor(produk) {
  const key = (produk || "").toLowerCase();
  for (const [k, v] of Object.entries(PRODUCT_COLORS)) {
    if (key.includes(k)) return v;
  }
  return PRODUCT_COLORS.default;
}

export default function VoyageDetailModal({ voyage, open, onClose }) {
  const [cargoItems, setCargoItems] = useState([]);
  const [cargoLoading, setCargoLoading] = useState(false);
  const [showCargo, setShowCargo] = useState(false);
  const [sortField, setSortField] = useState("gulden_india");
  const [sortAsc, setSortAsc] = useState(false);

  // Fetch cargo when modal opens
  useEffect(() => {
    if (open && voyage?.id) {
      setCargoLoading(true);
      setShowCargo(false);
      axios
        .get(`${API}/voyages/${voyage.id}/cargo`)
        .then((res) => {
          setCargoItems(res.data || []);
          if (res.data && res.data.length > 0) {
            setShowCargo(true);
          }
        })
        .catch((err) => {
          console.error("Error fetching cargo:", err);
          setCargoItems([]);
        })
        .finally(() => setCargoLoading(false));
    } else {
      setCargoItems([]);
      setShowCargo(false);
    }
  }, [open, voyage?.id]);

  if (!voyage) return null;

  const dir = DIRECTION_COLORS[voyage.direction] || DIRECTION_COLORS.transit;
  const routeColor = dir.color;

  // Sort cargo items
  const sortedCargo = [...cargoItems].sort((a, b) => {
    const aVal = a[sortField] || 0;
    const bVal = b[sortField] || 0;
    return sortAsc ? aVal - bVal : bVal - aVal;
  });

  // Cargo totals
  const cargoTotals = cargoItems.reduce(
    (acc, item) => ({
      gulden_nl: acc.gulden_nl + (item.gulden_nl || 0),
      gulden_india: acc.gulden_india + (item.gulden_india || 0),
      count: acc.count + 1,
    }),
    { gulden_nl: 0, gulden_india: 0, count: 0 }
  );

  const handleSort = (field) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  const SortIcon = ({ field }) => {
    if (sortField !== field) return null;
    return sortAsc ? (
      <ChevronUp className="w-3 h-3 inline ml-1" />
    ) : (
      <ChevronDown className="w-3 h-3 inline ml-1" />
    );
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] bg-[#0d1221] border-white/10 text-white overflow-hidden flex flex-col" data-testid="voyage-detail-modal">
        <DialogHeader>
          <DialogTitle className="font-serif text-3xl font-bold text-white flex items-center gap-3">
            <Ship className="w-8 h-8" style={{ color: routeColor }} />
            {voyage.ship_name}
          </DialogTitle>
        </DialogHeader>

        <ScrollArea className="flex-1 pr-4">
          <div className="space-y-6 mt-4">
            {/* Route Visualization */}
            <div className="bg-white/5 p-4 rounded-lg border border-white/10">
              <h3 className="text-sm font-semibold text-white/60 mb-3 flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                Rute Pelayaran
                <span
                  className="ml-auto text-xs font-medium px-2 py-0.5 rounded-full"
                  style={{ backgroundColor: `${routeColor}20`, color: routeColor }}
                >
                  {dir.icon} {dir.label}
                </span>
              </h3>
              <div className="flex items-center justify-between">
                <div className="flex flex-col items-center">
                  <div 
                    className="w-4 h-4 rounded-full mb-2 shadow-md" 
                    style={{ backgroundColor: routeColor }}
                  ></div>
                  <span className="font-bold text-white text-lg">{voyage.origin_name_raw || "—"}</span>
                  <span className="text-xs text-white/40">Asal</span>
                </div>
                
                <div className="flex-1 mx-6 relative">
                  <div 
                    className="h-1 w-full rounded" 
                    style={{ backgroundColor: routeColor }}
                  ></div>
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#0d1221] px-2">
                    <svg width="30" height="30" viewBox="0 0 30 30" fill="none">
                      <path 
                        d={voyage.direction === "inbound" 
                          ? "M22 15L8 15M8 15L12 11M8 15L12 19" 
                          : "M8 15L22 15M22 15L18 11M22 15L18 19"
                        }
                        stroke={routeColor} 
                        strokeWidth="3" 
                        strokeLinecap="round" 
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                </div>
                
                <div className="flex flex-col items-center">
                  <div className="w-4 h-4 rounded-full mb-2 shadow-md" style={{ backgroundColor: routeColor, opacity: 0.6 }}></div>
                  <span className="font-bold text-white text-lg">{voyage.destination_name_raw || voyage.destination || "—"}</span>
                  <span className="text-xs text-white/40">Tujuan</span>
                </div>
              </div>
            </div>

            {/* Details Grid */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                <div className="flex items-center gap-2 mb-2">
                  <Calendar className="w-5 h-5" style={{ color: routeColor }} />
                  <span className="text-sm font-medium text-white/60">Tahun</span>
                </div>
                <p className="text-2xl font-serif font-bold text-white">{voyage.year || "—"}</p>
                {voyage.departure_date && (
                  <p className="text-xs text-white/40 mt-1">Berangkat: {voyage.departure_date}</p>
                )}
                {voyage.arrival_date && (
                  <p className="text-xs text-white/40">Tiba: {voyage.arrival_date}</p>
                )}
              </div>

              <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                <div className="flex items-center gap-2 mb-2">
                  <DollarSign className="w-5 h-5 text-[#FFD93D]" />
                  <span className="text-sm font-medium text-white/60">Nilai Cargo</span>
                </div>
                <p className="text-2xl font-serif font-bold" style={{ color: routeColor }}>
                  {(voyage.total_gulden || 0).toLocaleString()}
                </p>
                <p className="text-xs text-white/40">Gulden (NL)</p>
              </div>
            </div>

            {/* Extra info row */}
            <div className="grid grid-cols-3 gap-3">
              {voyage.captain && (
                <div className="bg-white/5 p-3 rounded-lg border border-white/10">
                  <p className="text-xs text-white/40 mb-1">Kapten</p>
                  <p className="text-sm font-semibold text-white">{voyage.captain}</p>
                </div>
              )}
              {voyage.duration_days && (
                <div className="bg-white/5 p-3 rounded-lg border border-white/10">
                  <p className="text-xs text-white/40 mb-1">Durasi</p>
                  <p className="text-sm font-semibold text-white">{voyage.duration_days} hari</p>
                </div>
              )}
              {voyage.cargo_count && (
                <div className="bg-white/5 p-3 rounded-lg border border-white/10">
                  <p className="text-xs text-white/40 mb-1">Jenis Kargo</p>
                  <p className="text-sm font-semibold text-white">{voyage.cargo_count} item</p>
                </div>
              )}
            </div>

            {/* Main Product */}
            <div className="bg-white/5 p-4 rounded-lg border border-white/10">
              <div className="flex items-center gap-2 mb-2">
                <Package className="w-5 h-5" style={{ color: routeColor }} />
                <span className="text-sm font-medium text-white/60">Produk Utama</span>
              </div>
              <p className="text-xl font-semibold text-white capitalize">{voyage.main_product || "—"}</p>
            </div>

            {/* ═══════════════════════════════════════════════════════════════ */}
            {/* CARGO TABLE — Feature 4 */}
            {/* ═══════════════════════════════════════════════════════════════ */}
            <div className="bg-gradient-to-b from-white/[0.07] to-white/[0.03] p-4 rounded-lg border border-white/10">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-white/80 flex items-center gap-2">
                  <Package className="w-4 h-4" style={{ color: routeColor }} />
                  Detail Kargo
                  {cargoItems.length > 0 && (
                    <span className="text-xs font-normal text-white/40 ml-1">
                      ({cargoItems.length} item)
                    </span>
                  )}
                </h3>
                {cargoItems.length > 0 && (
                  <button
                    onClick={() => setShowCargo(!showCargo)}
                    className="text-xs px-3 py-1 rounded-full border border-white/10 text-white/60 hover:text-white hover:bg-white/10 transition-all"
                  >
                    {showCargo ? "Sembunyikan" : "Tampilkan"}
                  </button>
                )}
              </div>

              {cargoLoading && (
                <div className="flex items-center justify-center py-8 gap-2 text-white/40">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span className="text-sm">Memuat data kargo...</span>
                </div>
              )}

              {!cargoLoading && cargoItems.length === 0 && (
                <p className="text-sm text-white/30 text-center py-4">
                  Tidak ada data kargo detail untuk pelayaran ini.
                </p>
              )}

              {showCargo && cargoItems.length > 0 && (
                <div className="space-y-3 animate-in fade-in slide-in-from-top-2 duration-300">
                  {/* Summary Cards */}
                  <div className="grid grid-cols-3 gap-2 mb-3">
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <p className="text-[10px] text-white/40 uppercase tracking-wider">Total Item</p>
                      <p className="text-lg font-bold text-white">{cargoTotals.count}</p>
                    </div>
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <p className="text-[10px] text-white/40 uppercase tracking-wider">Gulden NL</p>
                      <p className="text-lg font-bold text-[#FFD93D]">
                        {cargoTotals.gulden_nl > 0 ? cargoTotals.gulden_nl.toLocaleString(undefined, {maximumFractionDigits: 1}) : "—"}
                      </p>
                    </div>
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <p className="text-[10px] text-white/40 uppercase tracking-wider">Gulden India</p>
                      <p className="text-lg font-bold text-[#00D4AA]">
                        {cargoTotals.gulden_india > 0 ? cargoTotals.gulden_india.toLocaleString(undefined, {maximumFractionDigits: 1}) : "—"}
                      </p>
                    </div>
                  </div>

                  {/* Table */}
                  <div className="overflow-x-auto rounded-lg border border-white/10">
                    <table className="w-full text-sm" data-testid="cargo-table">
                      <thead>
                        <tr className="bg-white/5 border-b border-white/10">
                          <th className="text-left px-3 py-2 text-xs font-semibold text-white/50 uppercase tracking-wider">
                            Produk
                          </th>
                          <th className="text-left px-3 py-2 text-xs font-semibold text-white/50 uppercase tracking-wider">
                            Spesifikasi
                          </th>
                          <th className="text-right px-3 py-2 text-xs font-semibold text-white/50 uppercase tracking-wider">
                            Qty
                          </th>
                          <th className="text-left px-3 py-2 text-xs font-semibold text-white/50 uppercase tracking-wider">
                            Unit
                          </th>
                          <th 
                            className="text-right px-3 py-2 text-xs font-semibold text-white/50 uppercase tracking-wider cursor-pointer hover:text-white/80 transition-colors"
                            onClick={() => handleSort("gulden_nl")}
                          >
                            Gulden NL <SortIcon field="gulden_nl" />
                          </th>
                          <th 
                            className="text-right px-3 py-2 text-xs font-semibold text-white/50 uppercase tracking-wider cursor-pointer hover:text-white/80 transition-colors"
                            onClick={() => handleSort("gulden_india")}
                          >
                            Gulden India <SortIcon field="gulden_india" />
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {sortedCargo.map((item, idx) => (
                          <tr
                            key={item.id || idx}
                            className="border-b border-white/5 hover:bg-white/5 transition-colors"
                          >
                            <td className="px-3 py-2">
                              <span
                                className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium capitalize"
                                style={{
                                  backgroundColor: `${getProductColor(item.produk)}15`,
                                  color: getProductColor(item.produk),
                                }}
                              >
                                <span
                                  className="w-1.5 h-1.5 rounded-full"
                                  style={{ backgroundColor: getProductColor(item.produk) }}
                                />
                                {item.produk}
                              </span>
                            </td>
                            <td className="px-3 py-2 text-white/50 text-xs">
                              {item.spesifikasi && item.spesifikasi !== "-" ? item.spesifikasi : "—"}
                            </td>
                            <td className="px-3 py-2 text-right text-white/70 font-mono text-xs">
                              {item.qty_asli || "—"}
                            </td>
                            <td className="px-3 py-2 text-white/50 text-xs">
                              {item.unit || "—"}
                            </td>
                            <td className="px-3 py-2 text-right font-mono text-xs">
                              {item.gulden_nl
                                ? <span className="text-[#FFD93D]">{item.gulden_nl.toLocaleString(undefined, {maximumFractionDigits: 1})}</span>
                                : <span className="text-white/20">—</span>
                              }
                            </td>
                            <td className="px-3 py-2 text-right font-mono text-xs">
                              {item.gulden_india
                                ? <span className="text-[#00D4AA]">{item.gulden_india.toLocaleString(undefined, {maximumFractionDigits: 1})}</span>
                                : <span className="text-white/20">—</span>
                              }
                            </td>
                          </tr>
                        ))}
                      </tbody>
                      {/* Summary Footer */}
                      <tfoot>
                        <tr className="bg-white/5 border-t border-white/10">
                          <td colSpan={4} className="px-3 py-2 text-xs font-bold text-white/60 uppercase tracking-wider">
                            Total ({cargoTotals.count} item)
                          </td>
                          <td className="px-3 py-2 text-right font-mono text-xs font-bold text-[#FFD93D]">
                            {cargoTotals.gulden_nl > 0 ? cargoTotals.gulden_nl.toLocaleString(undefined, {maximumFractionDigits: 1}) : "—"}
                          </td>
                          <td className="px-3 py-2 text-right font-mono text-xs font-bold text-[#00D4AA]">
                            {cargoTotals.gulden_india > 0 ? cargoTotals.gulden_india.toLocaleString(undefined, {maximumFractionDigits: 1}) : "—"}
                          </td>
                        </tr>
                      </tfoot>
                    </table>
                  </div>

                  {/* Cargo catatan */}
                  {sortedCargo.some((c) => c.catatan && c.catatan.trim()) && (
                    <div className="mt-2">
                      <p className="text-[10px] uppercase tracking-wider text-white/30 mb-1">Catatan</p>
                      {sortedCargo
                        .filter((c) => c.catatan && c.catatan.trim())
                        .map((c, i) => (
                          <p key={i} className="text-xs text-white/40 italic">
                            • {c.produk}: {c.catatan}
                          </p>
                        ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* All Products (legacy display) */}
            {voyage.all_products && (
              <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                <h3 className="text-sm font-semibold text-white/60 mb-3">
                  Semua Komoditi yang Dibawa
                </h3>
                <div className="flex flex-wrap gap-2">
                  {voyage.all_products.split('|').map((product, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1.5 bg-white/5 border border-white/10 rounded-full text-sm font-medium text-white/80 capitalize hover:bg-white/10 transition-colors"
                    >
                      {product.trim()}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Source Link */}
            {voyage.source_url && (
              <div className="border-t border-white/10 pt-4">
                <a
                  href={voyage.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm hover:underline flex items-center gap-1"
                  style={{ color: routeColor }}
                >
                  📖 Lihat sumber data lengkap di BGC Huygens →
                </a>
              </div>
            )}

            {/* Close Button */}
            <Button
              onClick={onClose}
              className="w-full text-white font-medium py-6"
              style={{ backgroundColor: routeColor }}
              data-testid="close-voyage-modal"
            >
              Tutup
            </Button>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
