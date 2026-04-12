import { Anchor, Ship, TrendingUp, Package } from "lucide-react";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ExportButton from "@/components/ExportButton";
import StatisticsPanel from "@/components/StatisticsPanel";
import ProductFilter from "@/components/ProductFilter";

// Direction badge colors
const DIRECTION_BADGE = {
  outbound: { bg: "rgba(0,212,170,0.15)", color: "#00D4AA", label: "⬆ Keluar" },
  inbound:  { bg: "rgba(255,107,107,0.15)", color: "#FF6B6B", label: "⬇ Masuk" },
  transit:  { bg: "rgba(255,217,61,0.15)", color: "#FFD93D", label: "🔄 Transit" },
};

export default function Sidebar({
  voyages,
  allVoyages,
  stats,
  selectedPorts,
  setSelectedPorts,
  selectedProducts,
  setSelectedProducts,
  searchTerm,
  setSearchTerm,
  onVoyageClick,
}) {
  // All 9 ports for filtering
  const ports = ["Padang", "Barus", "Air Bangis", "Pulau Cingkuak", "Air Haji"];

  const togglePort = (port) => {
    if (selectedPorts.includes(port)) {
      setSelectedPorts(selectedPorts.filter((p) => p !== port));
    } else {
      setSelectedPorts([...selectedPorts, port]);
    }
  };

  const filteredVoyages = voyages.filter((v) =>
    (v.ship_name || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div
      className="absolute left-6 top-6 bottom-24 w-96 bg-[#0d1221]/90 backdrop-blur-xl rounded-lg border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.3)] overflow-hidden flex flex-col"
      data-testid="sidebar-panel"
    >
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-3">
            <Anchor className="w-6 h-6 text-[#00D4AA]" />
            <h1 className="font-serif text-2xl font-bold text-white tracking-tight">
              Westkust Routes
            </h1>
          </div>
        </div>
        <p className="text-sm text-white/50 leading-relaxed mb-3">
          Jalur Pelayaran VOC Sumatera Westkust (1700-1789)
        </p>
        <ExportButton voyages={filteredVoyages} />
      </div>

      <Tabs defaultValue="voyages" className="flex-1 flex flex-col min-h-0">
        <TabsList className="mx-6 mt-4 bg-white/5 border border-white/10">
          <TabsTrigger value="voyages" className="text-xs text-white/70 data-[state=active]:text-white data-[state=active]:bg-white/10">Pelayaran</TabsTrigger>
          <TabsTrigger value="statistics" className="text-xs text-white/70 data-[state=active]:text-white data-[state=active]:bg-white/10">Statistik</TabsTrigger>
        </TabsList>

        <TabsContent value="voyages" className="flex-1 flex flex-col min-h-0 mt-4">
          <div className="px-6 space-y-4">
            <div>
              <h2 className="font-serif text-sm font-semibold text-white/80 mb-3">
                Filter Pelabuhan Keberangkatan
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
                      className="text-sm font-medium text-white/80 leading-none cursor-pointer"
                    >
                      {port}
                    </label>
                  </div>
                ))}
              </div>
            </div>

            <ProductFilter
              voyages={allVoyages}
              selectedProducts={selectedProducts}
              setSelectedProducts={setSelectedProducts}
            />

            <div>
              <Input
                placeholder="Cari nama kapal..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="bg-white/5 border-white/10 text-white placeholder:text-white/30 focus:ring-[#00D4AA]"
                data-testid="ship-search-input"
              />
            </div>
          </div>

          <ScrollArea className="flex-1 mt-4 px-6">
            <div className="space-y-2 pr-4 pb-4">
              {filteredVoyages.slice(0, 100).map((voyage) => {
                const badge = DIRECTION_BADGE[voyage.direction] || DIRECTION_BADGE.transit;
                return (
                  <button
                    key={voyage.id}
                    onClick={() => onVoyageClick(voyage)}
                    className="w-full text-left p-3 rounded-md border border-white/10 bg-white/5 hover:bg-white/10 hover:translate-y-[-2px] hover:shadow-md transition-all duration-200"
                    data-testid={`voyage-item-${voyage.id}`}
                  >
                    <div className="flex items-start justify-between">
                      <p className="font-serif font-semibold text-white text-sm mb-1">
                        {voyage.ship_name}
                      </p>
                      <span
                        className="text-[10px] font-medium px-2 py-0.5 rounded-full whitespace-nowrap"
                        style={{ backgroundColor: badge.bg, color: badge.color }}
                      >
                        {badge.label}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-white/50">
                      <span>{voyage.year}</span>
                      <span>•</span>
                      <span>{voyage.origin_name_raw || "—"}</span>
                      <span>→</span>
                      <span>{voyage.destination_name_raw || "—"}</span>
                    </div>
                    <p className="text-xs text-[#00D4AA] font-medium mt-1">
                      {(voyage.total_gulden || 0).toLocaleString()} Gulden
                    </p>
                  </button>
                );
              })}
              {filteredVoyages.length > 100 && (
                <p className="text-center text-xs text-white/30 py-2">
                  + {filteredVoyages.length - 100} pelayaran lainnya
                </p>
              )}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="statistics" className="flex-1 overflow-y-auto px-6 pb-4">
          <StatisticsPanel voyages={filteredVoyages} stats={stats} />
        </TabsContent>
      </Tabs>
    </div>
  );
}