import { Anchor, Ship, TrendingUp, Package, Network, Grid3X3, GitCompareArrows } from "lucide-react";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
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
  onOpenNetworkGraph,
  onOpenHeatmap,
  onOpenPortComparison,
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
          <TabsTrigger value="analytics" className="text-xs text-white/70 data-[state=active]:text-white data-[state=active]:bg-white/10">
            Analitik
          </TabsTrigger>
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

          <div className="flex-1 overflow-y-auto mt-4 px-6 border-t border-white/10 pt-4">
            <div className="space-y-2 pb-4">
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
                      <p className="font-serif font-semibold text-white text-sm mb-1 line-clamp-2 pr-2">
                        {voyage.ship_name}
                      </p>
                      <span
                        className="text-[10px] font-medium px-2 py-0.5 rounded-full whitespace-nowrap shrink-0"
                        style={{ backgroundColor: badge.bg, color: badge.color }}
                      >
                        {badge.label}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-[11px] text-white/50 mt-1 flex-wrap">
                      <span className="font-mono text-white/70">{voyage.year}</span>
                      <span>•</span>
                      <span className="truncate max-w-[80px]">{voyage.origin_name_raw || "—"}</span>
                      <span>→</span>
                      <span className="truncate max-w-[80px]">{voyage.destination_name_raw || "—"}</span>
                    </div>
                    <p className="text-xs font-mono text-[#00D4AA] font-bold mt-2">
                      +{(voyage.total_gulden || 0).toLocaleString()} ƒ
                    </p>
                  </button>
                );
              })}
              {filteredVoyages.length > 100 && (
                <p className="text-center text-xs text-white/30 py-4 font-mono">
                  + {filteredVoyages.length - 100} riwayat lainnya
                </p>
              )}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="statistics" className="flex-1 overflow-y-auto px-6 pb-4">
          <StatisticsPanel voyages={filteredVoyages} stats={stats} />
        </TabsContent>

        {/* ═══════════════ Analytics Tab ═══════════════ */}
        <TabsContent value="analytics" className="flex-1 overflow-y-auto px-6 pb-4">
          <div className="space-y-4 mt-4">
            <p className="text-xs text-white/40 leading-relaxed">
              Visualisasi analitik interaktif untuk mengeksplorasi pola perdagangan VOC
              di Sumatera Westkust secara mendalam.
            </p>

            {/* Network Graph Card */}
            <button
              onClick={onOpenNetworkGraph}
              className="w-full text-left group"
              data-testid="open-network-graph"
            >
              <Card className="p-4 bg-gradient-to-br from-[#00D4AA]/10 to-transparent border border-[#00D4AA]/20 shadow-none hover:border-[#00D4AA]/40 hover:bg-[#00D4AA]/5 transition-all group-hover:translate-y-[-2px] group-hover:shadow-lg">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 rounded-lg bg-[#00D4AA]/20 flex items-center justify-center">
                    <Network className="w-5 h-5 text-[#00D4AA]" />
                  </div>
                  <div>
                    <h3 className="font-serif font-bold text-white text-sm">Network Graph</h3>
                    <p className="text-[11px] text-white/40">Jaringan pelabuhan & rute</p>
                  </div>
                </div>
                <p className="text-xs text-white/50 leading-relaxed">
                  Visualisasi force-directed graph yang menunjukkan pola hubungan perdagangan
                  antar pelabuhan. Node = pelabuhan, edge = rute, ketebalan = frekuensi.
                </p>
              </Card>
            </button>

            {/* Heatmap Card */}
            <button
              onClick={onOpenHeatmap}
              className="w-full text-left group"
              data-testid="open-heatmap"
            >
              <Card className="p-4 bg-gradient-to-br from-[#FFD93D]/10 to-transparent border border-[#FFD93D]/20 shadow-none hover:border-[#FFD93D]/40 hover:bg-[#FFD93D]/5 transition-all group-hover:translate-y-[-2px] group-hover:shadow-lg">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 rounded-lg bg-[#FFD93D]/20 flex items-center justify-center">
                    <Grid3X3 className="w-5 h-5 text-[#FFD93D]" />
                  </div>
                  <div>
                    <h3 className="font-serif font-bold text-white text-sm">Heatmap Temporal</h3>
                    <p className="text-[11px] text-white/40">Aktivitas per tahun × pelabuhan</p>
                  </div>
                </div>
                <p className="text-xs text-white/50 leading-relaxed">
                  Grid heatmap di mana sumbu X = tahun, sumbu Y = pelabuhan, dan warna
                  menunjukkan intensitas perdagangan. Langsung terlihat kapan pelabuhan mana paling aktif.
                </p>
              </Card>
            </button>

            {/* Port Comparison Card */}
            <button
              onClick={onOpenPortComparison}
              className="w-full text-left group"
              data-testid="open-port-comparison"
            >
              <Card className="p-4 bg-gradient-to-br from-[#FF6B6B]/10 to-transparent border border-[#FF6B6B]/20 shadow-none hover:border-[#FF6B6B]/40 hover:bg-[#FF6B6B]/5 transition-all group-hover:translate-y-[-2px] group-hover:shadow-lg">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 rounded-lg bg-[#FF6B6B]/20 flex items-center justify-center">
                    <GitCompareArrows className="w-5 h-5 text-[#FF6B6B]" />
                  </div>
                  <div>
                    <h3 className="font-serif font-bold text-white text-sm">Perbandingan Pelabuhan</h3>
                    <p className="text-[11px] text-white/40">Side-by-side analysis</p>
                  </div>
                </div>
                <p className="text-xs text-white/50 leading-relaxed">
                  Bandingkan 2-5 pelabuhan secara langsung: volume, komoditas, tren tahunan.
                  Untuk analisis kompetisi antar pelabuhan — misal Padang vs Barus vs Air Bangis.
                </p>
              </Card>
            </button>

            {/* Quick stats from API */}
            {stats && (
              <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
                <h3 className="font-serif text-xs font-semibold text-white/60 mb-3 uppercase tracking-wider">
                  Ringkasan Dataset
                </h3>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-white/40">Total Pelayaran</span>
                    <span className="text-white font-mono">{stats.total_voyages}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/40">Total Nilai</span>
                    <span className="text-[#FFD93D] font-mono">
                      {(stats.total_cargo_value / 1000000).toFixed(1)}M ƒ
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/40">Outbound</span>
                    <span className="text-[#00D4AA] font-mono">{stats.outbound_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/40">Inbound</span>
                    <span className="text-[#FF6B6B] font-mono">{stats.inbound_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/40">Periode</span>
                    <span className="text-white font-mono">
                      {stats.year_min}–{stats.year_max}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/40">Pelabuhan</span>
                    <span className="text-white font-mono">{stats.ports?.length || 0}</span>
                  </div>
                </div>
              </Card>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}