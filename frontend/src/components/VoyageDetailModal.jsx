import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { X, Ship, Calendar, DollarSign, Package, MapPin, Compass, Clock, Anchor } from "lucide-react";
import { Button } from "@/components/ui/button";

const DIRECTION_COLORS = {
  outbound: { color: "#00D4AA", label: "Keberangkatan (Outbound)", icon: "🚢" },
  inbound:  { color: "#FF6B6B", label: "Kedatangan (Inbound)", icon: "🏠" },
  transit:  { color: "#FFD93D", label: "Transit", icon: "🔄" },
};

export default function VoyageDetailModal({ voyage, open, onClose }) {
  if (!voyage) return null;

  const dir = DIRECTION_COLORS[voyage.direction] || DIRECTION_COLORS.transit;
  const routeColor = dir.color;

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl bg-[#0d1221] border-white/10 text-white" data-testid="voyage-detail-modal">
        <DialogHeader>
          <DialogTitle className="font-serif text-3xl font-bold text-white flex items-center gap-3">
            <Ship className="w-8 h-8" style={{ color: routeColor }} />
            {voyage.ship_name}
          </DialogTitle>
        </DialogHeader>

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

          {/* All Products */}
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
      </DialogContent>
    </Dialog>
  );
}
