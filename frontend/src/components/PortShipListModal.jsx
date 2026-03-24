import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Ship, Package, Calendar, Info } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";

export default function PortShipListModal({ port, ships, open, onClose, onViewDetail, onViewHistory }) {
  if (!port || !ships) return null;

  const displayPortName = port === "Batavia" ? "Sunda Kelapa (Batavia)" : port;
  
  // Count ships and total value
  const totalShips = ships.length;
  const totalValue = ships.reduce((sum, ship) => sum + ship.total_gulden_nl, 0);

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl bg-[#FDFBF7] border-[#E6E2D6]" data-testid="port-ship-list-modal">
        <DialogHeader>
          <DialogTitle className="font-serif text-3xl font-bold text-[#1A2421] flex items-center gap-3">
            🏰 Pelabuhan {displayPortName}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4 mt-4">
          {/* Summary Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-lg border border-[#E6E2D6]">
              <div className="flex items-center gap-2 mb-1">
                <Ship className="w-5 h-5 text-[#B85D19]" />
                <span className="text-sm font-medium text-[#5C6A66]">Total Kapal</span>
              </div>
              <p className="text-3xl font-serif font-bold text-[#1A2421]">{totalShips}</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-[#E6E2D6]">
              <div className="flex items-center gap-2 mb-1">
                <Package className="w-5 h-5 text-[#D4AF37]" />
                <span className="text-sm font-medium text-[#5C6A66]">Total Nilai Cargo</span>
              </div>
              <p className="text-xl font-serif font-bold text-[#B85D19]">
                {(totalValue / 1000000).toFixed(2)}M
              </p>
              <p className="text-xs text-[#8A9A95]">Gulden</p>
            </div>
          </div>

          {/* Historical Context Button */}
          <Button
            onClick={() => {
              onClose();
              onViewHistory(port);
            }}
            variant="outline"
            className="w-full border-[#B85D19] text-[#B85D19] hover:bg-[#B85D19] hover:text-white"
          >
            <Info className="w-4 h-4 mr-2" />
            Lihat Sejarah Pelabuhan {displayPortName}
          </Button>

          {/* Ships List */}
          <div className="bg-white rounded-lg border border-[#E6E2D6] p-4">
            <h3 className="font-serif text-lg font-semibold text-[#1A2421] mb-3">
              Daftar Kapal ({totalShips})
            </h3>
            <ScrollArea className="h-[400px] pr-4">
              <div className="space-y-3">
                {ships.map((ship) => (
                  <div
                    key={ship.id}
                    className="p-4 rounded-lg border border-[#E6E2D6] bg-[#FDFBF7] hover:bg-white hover:shadow-md transition-all"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-serif text-lg font-bold text-[#1A2421] mb-2">
                          {ship.nama_kapal}
                        </h4>
                        <div className="grid grid-cols-2 gap-2 text-sm">
                          <div className="flex items-center gap-2">
                            <Calendar className="w-4 h-4 text-[#5C6A66]" />
                            <span className="text-[#5C6A66]">Tahun:</span>
                            <span className="font-semibold text-[#1A2421]">{ship.tahun}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Package className="w-4 h-4 text-[#5C6A66]" />
                            <span className="text-[#5C6A66]">Produk:</span>
                            <span className="font-semibold text-[#1A2421] capitalize">
                              {ship.produk_utama}
                            </span>
                          </div>
                        </div>
                        <p className="text-lg font-bold text-[#B85D19] mt-2">
                          {ship.total_gulden_nl.toLocaleString()} Gulden
                        </p>
                      </div>
                      <Button
                        onClick={() => onViewDetail(ship)}
                        size="sm"
                        className="bg-[#B85D19] hover:bg-[#9a4d15] text-white"
                        data-testid={`view-detail-${ship.id}`}
                      >
                        Detail Komoditi
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </div>

          <Button
            onClick={onClose}
            variant="outline"
            className="w-full border-[#E6E2D6] hover:bg-[#FDFBF7]"
          >
            Tutup
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
