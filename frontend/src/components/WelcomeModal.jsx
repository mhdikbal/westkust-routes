import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Ship } from "lucide-react";

export default function WelcomeModal({ open, onClose }) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px] bg-[#FDFBF7] border-[#E6E2D6]" data-testid="welcome-modal">
        <DialogHeader>
          <div className="flex items-center gap-3 mb-4">
            <Ship className="w-8 h-8 text-[#B85D19]" />
            <DialogTitle className="font-serif text-3xl font-bold text-[#1A2421] tracking-tight">
              Westkust Maritime Routes
            </DialogTitle>
          </div>
        </DialogHeader>

        <div className="space-y-4">
          <div
            className="w-full h-64 rounded-lg overflow-hidden mb-4"
            style={{
              backgroundImage:
                "url('https://images.unsplash.com/photo-1773593625870-bb7549da24d9?crop=entropy&cs=srgb&fm=jpg&q=85')",
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          />

          <p className="text-[#5C6A66] leading-relaxed">
            Jelajahi jalur pelayaran bersejarah dari Pantai Barat Sumatra (Sumatra Westkust)
            ke Batavia pada masa VOC (1700-1789). Visualisasi interaktif ini menampilkan
            ratusan pelayaran dengan detail nama kapal, nilai kargo, dan produk yang
            diperdagangkan.
          </p>

          <div className="bg-white border border-[#E6E2D6] rounded-lg p-4 space-y-2">
            <h3 className="font-serif font-semibold text-[#1A2421] mb-2">
              Fitur Utama:
            </h3>
            <ul className="space-y-1 text-sm text-[#5C6A66]">
              <li>🗺️ Visualisasi rute pelayaran interaktif</li>
              <li>📅 Filter berdasarkan periode tahun (1700-1789)</li>
              <li>⚓ Filter pelabuhan: Padang, Pulau Cingkuak, Air Haji</li>
              <li>🚢 Detail kapal: nama, nilai kargo, produk utama</li>
              <li>📊 Statistik perdagangan maritim</li>
            </ul>
          </div>

          <Button
            onClick={onClose}
            className="w-full bg-[#B85D19] hover:bg-[#9a4d15] text-white font-medium py-6 rounded-lg"
            data-testid="welcome-modal-close"
          >
            Mulai Jelajahi Peta
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}