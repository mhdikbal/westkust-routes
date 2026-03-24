import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { X, Ship, Calendar, DollarSign, Package, MapPin } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function VoyageDetailModal({ voyage, open, onClose }) {
  if (!voyage) return null;

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl bg-[#FDFBF7] border-[#E6E2D6]" data-testid="voyage-detail-modal">
        <DialogHeader>
          <DialogTitle className="font-serif text-3xl font-bold text-[#1A2421] flex items-center gap-3">
            <Ship className="w-8 h-8 text-[#B85D19]" />
            {voyage.nama_kapal}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6 mt-4">
          {/* Route Visualization */}
          <div className="bg-white p-4 rounded-lg border-2 border-[#E6E2D6]">
            <h3 className="text-sm font-semibold text-[#5C6A66] mb-3 flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              Rute Pelayaran
            </h3>
            <div className="flex items-center justify-between">
              <div className="flex flex-col items-center">
                <div 
                  className="w-4 h-4 rounded-full mb-2 shadow-md" 
                  style={{ backgroundColor: voyage.warna_asal }}
                ></div>
                <span className="font-bold text-[#1A2421] text-lg">{voyage.asal}</span>
                <span className="text-xs text-[#8A9A95]">Keberangkatan</span>
              </div>
              
              <div className="flex-1 mx-6 relative">
                <div 
                  className="h-1 w-full rounded" 
                  style={{ backgroundColor: voyage.warna_asal }}
                ></div>
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#FDFBF7] px-2">
                  <svg width="30" height="30" viewBox="0 0 30 30" fill="none">
                    <path 
                      d="M8 15L22 15M22 15L18 11M22 15L18 19" 
                      stroke={voyage.warna_asal} 
                      strokeWidth="3" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
              </div>
              
              <div className="flex flex-col items-center">
                <div className="w-4 h-4 rounded-full bg-[#B85D19] mb-2 shadow-md"></div>
                <span className="font-bold text-[#1A2421] text-lg">Batavia</span>
                <span className="text-xs text-[#8A9A95]">Tujuan</span>
              </div>
            </div>
          </div>

          {/* Details Grid */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-lg border border-[#E6E2D6]">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-5 h-5 text-[#B85D19]" />
                <span className="text-sm font-medium text-[#5C6A66]">Tahun Keberangkatan</span>
              </div>
              <p className="text-2xl font-serif font-bold text-[#1A2421]">{voyage.tahun}</p>
            </div>

            <div className="bg-white p-4 rounded-lg border border-[#E6E2D6]">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="w-5 h-5 text-[#D4AF37]" />
                <span className="text-sm font-medium text-[#5C6A66]">Nilai Cargo</span>
              </div>
              <p className="text-2xl font-serif font-bold text-[#B85D19]">
                {voyage.total_gulden_nl.toLocaleString()}
              </p>
              <p className="text-xs text-[#8A9A95]">Gulden (NL)</p>
            </div>
          </div>

          {/* Main Product */}
          <div className="bg-white p-4 rounded-lg border border-[#E6E2D6]">
            <div className="flex items-center gap-2 mb-2">
              <Package className="w-5 h-5 text-[#B85D19]" />
              <span className="text-sm font-medium text-[#5C6A66]">Produk Utama</span>
            </div>
            <p className="text-xl font-semibold text-[#1A2421] capitalize">{voyage.produk_utama}</p>
          </div>

          {/* All Products */}
          <div className="bg-[#FDFBF7] p-4 rounded-lg border-2 border-[#E6E2D6]">
            <h3 className="text-sm font-semibold text-[#5C6A66] mb-3">
              Semua Komoditi yang Dibawa
            </h3>
            <div className="flex flex-wrap gap-2">
              {voyage.semua_produk.split('|').map((product, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1.5 bg-white border-2 border-[#E6E2D6] rounded-full text-sm font-medium text-[#1A2421] capitalize hover:bg-[#B85D19] hover:text-white hover:border-[#B85D19] transition-colors"
                >
                  {product.trim()}
                </span>
              ))}
            </div>
          </div>

          {/* Source Link */}
          {voyage.url && (
            <div className="border-t border-[#E6E2D6] pt-4">
              <a
                href={voyage.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-[#B85D19] hover:underline flex items-center gap-1"
              >
                📖 Lihat sumber data lengkap di BGC Huygens →
              </a>
            </div>
          )}

          {/* Close Button */}
          <Button
            onClick={onClose}
            className="w-full bg-[#B85D19] hover:bg-[#9a4d15] text-white font-medium py-6"
            data-testid="close-voyage-modal"
          >
            Tutup
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
