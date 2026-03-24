import { Anchor, Ship, TrendingUp, Package } from "lucide-react";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";

export default function Sidebar({
  voyages,
  stats,
  selectedPorts,
  setSelectedPorts,
  searchTerm,
  setSearchTerm,
  onVoyageClick,
}) {
  const ports = ["Padang", "Pulau Cingkuak", "Air Haji"];

  const togglePort = (port) => {
    if (selectedPorts.includes(port)) {
      setSelectedPorts(selectedPorts.filter((p) => p !== port));
    } else {
      setSelectedPorts([...selectedPorts, port]);
    }
  };

  const filteredVoyages = voyages.filter((v) =>
    v.nama_kapal.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div
      className="absolute left-6 top-6 bottom-24 w-96 bg-[#FDFBF7]/90 backdrop-blur-xl rounded-lg border border-[#E6E2D6] shadow-[0_8px_32px_rgba(26,36,33,0.08)] overflow-hidden flex flex-col"
      data-testid="sidebar-panel"
    >
      <div className="p-6 border-b border-[#E6E2D6]">
        <div className="flex items-center gap-3 mb-2">
          <Anchor className="w-6 h-6 text-[#B85D19]" />
          <h1 className="font-serif text-2xl font-bold text-[#1A2421] tracking-tight">
            Westkust Routes
          </h1>
        </div>
        <p className="text-sm text-[#5C6A66] leading-relaxed">
          Jalur Pelayaran Sumatra ke Batavia (1700-1789)
        </p>
      </div>

      {stats && (
        <div className="p-6 border-b border-[#E6E2D6] space-y-4">
          <h2 className="font-serif text-lg font-semibold text-[#1A2421] mb-3">
            Statistik
          </h2>
          <div className="grid grid-cols-2 gap-3">
            <Card className="p-4 bg-white border border-[#E6E2D6] shadow-none">
              <div className="flex items-center gap-2 mb-1">
                <Ship className="w-4 h-4 text-[#B85D19]" />
                <p className="text-xs uppercase tracking-[0.2em] text-[#8A9A95]">
                  Kapal
                </p>
              </div>
              <p className="text-2xl font-serif font-bold text-[#1A2421]">
                {stats.total_voyages}
              </p>
            </Card>
            <Card className="p-4 bg-white border border-[#E6E2D6] shadow-none">
              <div className="flex items-center gap-2 mb-1">
                <TrendingUp className="w-4 h-4 text-[#D4AF37]" />
                <p className="text-xs uppercase tracking-[0.2em] text-[#8A9A95]">
                  Nilai
                </p>
              </div>
              <p className="text-xl font-serif font-bold text-[#1A2421]">
                {(stats.total_cargo_value / 1000000).toFixed(1)}M
              </p>
            </Card>
          </div>
        </div>
      )}

      <div className="p-6 border-b border-[#E6E2D6]">
        <h2 className="font-serif text-lg font-semibold text-[#1A2421] mb-3">
          Filter Pelabuhan
        </h2>
        <div className="space-y-3">
          {ports.map((port) => (
            <div key={port} className="flex items-center space-x-2">
              <Checkbox
                id={port}
                checked={selectedPorts.includes(port)}
                onCheckedChange={() => togglePort(port)}
                data-testid={`port-filter-${port.toLowerCase().replace(" ", "-")}`}
              />
              <label
                htmlFor={port}
                className="text-sm font-medium text-[#1A2421] leading-none cursor-pointer"
              >
                {port}
              </label>
            </div>
          ))}
        </div>
      </div>

      <div className="p-6 flex-1 flex flex-col min-h-0">
        <div className="mb-4">
          <Input
            placeholder="Cari nama kapal..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-white border-[#E6E2D6] focus:ring-[#B85D19]"
            data-testid="ship-search-input"
          />
        </div>

        <ScrollArea className="flex-1">
          <div className="space-y-2 pr-4">
            {filteredVoyages.map((voyage) => (
              <button
                key={voyage.id}
                onClick={() => onVoyageClick(voyage)}
                className="w-full text-left p-3 rounded-md border border-[#E6E2D6] bg-white hover:bg-[#FDFBF7] hover:translate-y-[-2px] hover:shadow-md transition-all duration-200"
                data-testid={`voyage-item-${voyage.id}`}
              >
                <p className="font-serif font-semibold text-[#1A2421] text-sm mb-1">
                  {voyage.nama_kapal}
                </p>
                <div className="flex items-center gap-2 text-xs text-[#5C6A66]">
                  <span>{voyage.tahun}</span>
                  <span>•</span>
                  <span>{voyage.asal}</span>
                </div>
                <p className="text-xs text-[#B85D19] font-medium mt-1">
                  {voyage.total_gulden_nl.toLocaleString()} Gulden
                </p>
              </button>
            ))}
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}