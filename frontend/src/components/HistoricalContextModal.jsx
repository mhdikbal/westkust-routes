import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { X, MapPin, Calendar, Ship, Package } from "lucide-react";
import { Button } from "@/components/ui/button";

const PORT_HISTORY = {
  Padang: {
    name: "Padang (Muaro Padang)",
    period: "1700-1789",
    description: "Padang merupakan pelabuhan utama di Pantai Barat Sumatra yang menjadi pusat perdagangan emas dan lada. Sebagai pintu gerbang perdagangan VOC di wilayah Minangkabau, Padang memainkan peran vital dalam ekspor komoditas bernilai tinggi ke Batavia.",
    mainProducts: ["Emas (Goud)", "Lada (Peper)", "Kamfer", "Benzoë"],
    significance: "Hub perdagangan emas terbesar di Sumatra Barat pada abad ke-18",
    funFacts: [
      "Padang menjadi kompetitor utama Bengkulu dalam perdagangan lada",
      "Emas dari tambang pedalaman Minangkabau diekspor melalui Padang",
      "VOC mendirikan loji (kantor dagang) permanen di Padang pada 1663"
    ]
  },
  "Pulau Cingkuak": {
    name: "Pulau Cingkuak",
    period: "1700-1789",
    description: "Pulau Cingkuak adalah pulau kecil di lepas pantai Sumatra Barat yang berfungsi sebagai pos perdagangan strategis. Lokasi geografisnya yang ideal membuatnya menjadi titik persinggahan penting untuk kapal-kapal VOC.",
    mainProducts: ["Lada", "Emas", "Kayu Manis"],
    significance: "Pos perdagangan dan navigasi strategis di jalur maritim Sumatra-Java",
    funFacts: [
      "Pulau ini sering digunakan sebagai tempat berlabuh sementara",
      "Memiliki sumber air tawar yang penting untuk perbekalan kapal",
      "Benteng kecil VOC pernah dibangun untuk melindungi jalur perdagangan"
    ]
  },
  "Air Haji": {
    name: "Air Haji",
    period: "1700-1789",
    description: "Air Haji adalah pelabuhan kecil di selatan Padang yang berkembang sebagai alternatif jalur perdagangan. Meskipun lebih kecil dari Padang, Air Haji tetap penting dalam jaringan perdagangan VOC di Sumatra Barat.",
    mainProducts: ["Lada", "Kamfer", "Kopi"],
    significance: "Pelabuhan alternatif dengan akses ke wilayah pedalaman yang kaya rempah",
    funFacts: [
      "Nama 'Air Haji' berasal dari sumber mata air yang digunakan jamaah haji",
      "Pelabuhan ini lebih tenang dan aman dari badai dibanding pelabuhan terbuka",
      "Komoditas dari daerah Kerinci sering diekspor via Air Haji"
    ]
  },
  Batavia: {
    name: "Batavia (Sunda Kelapa/Jakarta)",
    period: "1619-1800",
    description: "Batavia adalah pusat administrasi dan perdagangan VOC di Asia. Sebagai ibukota Hindia Belanda, Batavia menjadi tujuan utama seluruh komoditas dari Nusantara sebelum dikirim ke Eropa. Kota ini berkembang menjadi salah satu kota terpenting di Asia pada abad ke-17 dan ke-18.",
    mainProducts: ["Pusat distribusi semua komoditas Nusantara"],
    significance: "Pusat kekuasaan VOC dan hub perdagangan internasional",
    funFacts: [
      "Batavia dijuluki 'Queen of the East' pada masa jayanya",
      "Pelabuhan Batavia dapat menampung ratusan kapal sekaligus",
      "Sistem kanal Batavia meniru Amsterdam, kota asal VOC",
      "Pasar budak terbesar di Asia Tenggara berada di Batavia"
    ]
  }
};

export default function HistoricalContextModal({ port, open, onClose }) {
  if (!port || !PORT_HISTORY[port]) return null;

  const history = PORT_HISTORY[port];

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl bg-[#FDFBF7] border-[#E6E2D6] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="font-serif text-3xl font-bold text-[#1A2421] flex items-center gap-3">
            <MapPin className="w-8 h-8 text-[#B85D19]" />
            {history.name}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6 mt-4">
          {/* Period */}
          <div className="flex items-center gap-2 text-[#5C6A66]">
            <Calendar className="w-5 h-5 text-[#B85D19]" />
            <span className="text-sm font-medium">Periode: {history.period}</span>
          </div>

          {/* Description */}
          <div className="bg-white p-5 rounded-lg border border-[#E6E2D6]">
            <p className="text-[#1A2421] leading-relaxed">{history.description}</p>
          </div>

          {/* Significance */}
          <div className="bg-gradient-to-r from-[#B85D19]/10 to-[#D4AF37]/10 p-5 rounded-lg border-l-4 border-[#B85D19]">
            <h3 className="font-serif text-lg font-semibold text-[#1A2421] mb-2">
              Signifikansi Historis
            </h3>
            <p className="text-[#5C6A66] italic">{history.significance}</p>
          </div>

          {/* Main Products */}
          <div className="bg-white p-5 rounded-lg border border-[#E6E2D6]">
            <div className="flex items-center gap-2 mb-3">
              <Package className="w-5 h-5 text-[#B85D19]" />
              <h3 className="font-serif text-lg font-semibold text-[#1A2421]">
                Komoditas Utama
              </h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {history.mainProducts.map((product, idx) => (
                <span
                  key={idx}
                  className="px-4 py-2 bg-[#FDFBF7] border-2 border-[#B85D19] rounded-full text-sm font-medium text-[#1A2421]"
                >
                  {product}
                </span>
              ))}
            </div>
          </div>

          {/* Fun Facts */}
          <div className="bg-white p-5 rounded-lg border border-[#E6E2D6]">
            <h3 className="font-serif text-lg font-semibold text-[#1A2421] mb-3">
              📚 Fakta Menarik
            </h3>
            <ul className="space-y-2">
              {history.funFacts.map((fact, idx) => (
                <li key={idx} className="flex items-start gap-3">
                  <span className="text-[#B85D19] font-bold mt-1">•</span>
                  <span className="text-[#5C6A66]">{fact}</span>
                </li>
              ))}
            </ul>
          </div>

          <Button
            onClick={onClose}
            className="w-full bg-[#B85D19] hover:bg-[#9a4d15] text-white font-medium py-6"
          >
            Tutup
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
