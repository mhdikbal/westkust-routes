import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Ship, Package, Calendar, Info } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";

const DIRECTION_BADGE = {
  outbound: { bg: "rgba(0,212,170,0.15)", color: "#00D4AA", label: "Keluar" },
  inbound:  { bg: "rgba(255,107,107,0.15)", color: "#FF6B6B", label: "Masuk" },
  transit:  { bg: "rgba(255,217,61,0.15)", color: "#FFD93D", label: "Transit" },
};

export default function PortShipListModal({ port, ships, open, onClose, onViewDetail, onViewHistory }) {
  if (!port || !ships) return null;

  const displayPortName = port === "Batavia" ? "Sunda Kelapa (Batavia)" : port;
  
  // Count ships and total value — use new field name
  const totalShips = ships.length;
  const totalValue = ships.reduce((sum, ship) => sum + (ship.total_gulden || 0), 0);

  // Count by direction
  const outCount = ships.filter(s => s.direction === "outbound").length;
  const inCount = ships.filter(s => s.direction === "inbound").length;

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl bg-[#0d1221] border-white/10 text-white" data-testid="port-ship-list-modal">
        <DialogHeader>
          <DialogTitle className="font-serif text-3xl font-bold text-white flex items-center gap-3">
            🏰 Pelabuhan {displayPortName}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4 mt-4">
          {/* Summary Stats */}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-white/5 p-4 rounded-lg border border-white/10">
              <div className="flex items-center gap-2 mb-1">
                <Ship className="w-5 h-5 text-[#00D4AA]" />
                <span className="text-sm font-medium text-white/60">Total Kapal</span>
              </div>
              <p className="text-3xl font-serif font-bold text-white">{totalShips}</p>
            </div>
            <div className="bg-white/5 p-4 rounded-lg border border-white/10">
              <div className="flex items-center gap-2 mb-1">
                <Package className="w-5 h-5 text-[#FFD93D]" />
                <span className="text-sm font-medium text-white/60">Nilai Cargo</span>
              </div>
              <p className="text-xl font-serif font-bold text-[#00D4AA]">
                {(totalValue / 1000000).toFixed(2)}M
              </p>
              <p className="text-xs text-white/40">Gulden</p>
            </div>
            <div className="bg-white/5 p-4 rounded-lg border border-white/10">
              <div className="text-xs text-white/40 mb-2">Arah</div>
              <div className="space-y-1">
                <p className="text-sm"><span className="text-[#00D4AA]">⬆ {outCount}</span> keluar</p>
                <p className="text-sm"><span className="text-[#FF6B6B]">⬇ {inCount}</span> masuk</p>
              </div>
            </div>
          </div>

          {/* Historical Context Button */}
          <Button
            onClick={() => {
              onClose();
              onViewHistory(port);
            }}
            variant="outline"
            className="w-full border-[#00D4AA] text-[#00D4AA] hover:bg-[#00D4AA] hover:text-white"
          >
            <Info className="w-4 h-4 mr-2" />
            Lihat Sejarah Pelabuhan {displayPortName}
          </Button>

          {/* Ships List */}
          <div className="bg-white/5 rounded-lg border border-white/10 p-4">
            <h3 className="font-serif text-lg font-semibold text-white mb-3">
              Daftar Kapal ({totalShips})
            </h3>
            <ScrollArea className="h-[400px] pr-4">
              <div className="space-y-3">
                {ships.map((ship) => {
                  const badge = DIRECTION_BADGE[ship.direction] || DIRECTION_BADGE.transit;
                  return (
                    <div
                      key={ship.id}
                      className="p-4 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 transition-all"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <h4 className="font-serif text-lg font-bold text-white">
                              {ship.ship_name}
                            </h4>
                            <span
                              className="text-[10px] font-medium px-2 py-0.5 rounded-full"
                              style={{ backgroundColor: badge.bg, color: badge.color }}
                            >
                              {badge.label}
                            </span>
                          </div>
                          <div className="grid grid-cols-2 gap-2 text-sm">
                            <div className="flex items-center gap-2">
                              <Calendar className="w-4 h-4 text-white/40" />
                              <span className="text-white/40">Tahun:</span>
                              <span className="font-semibold text-white">{ship.year}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <Package className="w-4 h-4 text-white/40" />
                              <span className="text-white/40">Produk:</span>
                              <span className="font-semibold text-white capitalize">
                                {ship.main_product || "—"}
                              </span>
                            </div>
                          </div>
                          <p className="text-lg font-bold text-[#00D4AA] mt-2">
                            {(ship.total_gulden || 0).toLocaleString()} Gulden
                          </p>
                        </div>
                        <Button
                          onClick={() => onViewDetail(ship)}
                          size="sm"
                          className="bg-[#00D4AA] hover:bg-[#00b894] text-white"
                          data-testid={`view-detail-${ship.id}`}
                        >
                          Detail
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </ScrollArea>
          </div>

          <Button
            onClick={onClose}
            variant="outline"
            className="w-full border-white/10 text-white/60 hover:bg-white/5"
          >
            Tutup
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
