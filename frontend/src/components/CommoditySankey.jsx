import { useState, useEffect, useMemo } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Loader2, TrendingUp, PackageSearch, Filter, ZoomIn, ZoomOut, Maximize } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sankey, Tooltip, ResponsiveContainer } from "recharts";
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import axios from "axios";
import { Slider } from "@/components/ui/slider";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

const COMMODITY_COLORS = {
  goud: "#FFD700",
  peper: "#e74c3c",
  kamfer: "#3498db",
  benzoe: "#9b59b6",
  lijfeigene: "#e67e22",
  kanon: "#7f8c8d",
  buskruit: "#2c3e50",
  default: "#00D4AA",
};

const getColorFromName = (name) => {
  if (name.includes("(Asal)")) return "#00D4AA"; // Teal for Origin
  if (name.includes("(Tujuan)")) return "#FF6B6B"; // Coral for Destination
  
  const key = name.toLowerCase();
  for (const [k, v] of Object.entries(COMMODITY_COLORS)) {
    if (key.includes(k)) return v;
  }
  return "#FFD93D"; // Gold for default commodity
};

// Custom Node for Sankey
const CustomNode = ({ x, y, width, height, index, payload, containerWidth }) => {
  const isOut = x + width > containerWidth / 2;
  const color = getColorFromName(payload.name);
  
  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        fill={color}
        fillOpacity={0.8}
        rx={2}
      />
      <text
        x={isOut ? x - 6 : x + width + 6}
        y={y + height / 2}
        textAnchor={isOut ? "end" : "start"}
        alignmentBaseline="middle"
        fontSize={11}
        fill="#ffffff"
        fontFamily="sans-serif"
        opacity={0.8}
      >
        {payload.name}
      </text>
    </g>
  );
};

// Custom Tooltip
const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    // Difference between Link and Node payload structure
    const isLink = data.source && data.target;

    if (isLink) {
      return (
        <div className="bg-[#0d1221]/95 border border-white/10 p-3 rounded-lg shadow-xl max-w-xs backdrop-blur-md">
          <p className="text-xs text-white/50 mb-1">Aliran Komoditas</p>
          <div className="flex items-center gap-2 mb-2">
            <span className="font-semibold text-white">{data.source.name}</span>
            <span className="text-[#00D4AA]">→</span>
            <span className="font-semibold text-white">{data.target.name}</span>
          </div>
          <p className="text-[14px] font-mono font-bold text-[#FFD93D]">
            {(data.value).toLocaleString()} ƒ
          </p>
        </div>
      );
    } else {
      return (
        <div className="bg-[#0d1221]/95 border border-white/10 p-3 rounded-lg shadow-xl max-w-xs backdrop-blur-md">
          <p className="text-xs text-white/50 mb-1">Akumulasi Nilai</p>
          <p className="font-semibold text-white text-md mb-2">{data.name}</p>
          <p className="text-[14px] font-mono font-bold text-[#FFD93D]">
            {(data.value).toLocaleString()} ƒ
          </p>
        </div>
      );
    }
  }
  return null;
};

export default function CommoditySankey({ open, onClose }) {
  const [yearRange, setYearRange] = useState([1700, 1789]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open) return;
    setLoading(true);
    axios
      .get(`${API}/voyages/analytics/sankey`, {
        params: {
          year_from: yearRange[0],
          year_to: yearRange[1],
        },
      })
      .then((res) => {
        // Recharts Sankey requires non-empty arrays
        if (res.data.nodes.length > 0 && res.data.links.length > 0) {
          setData(res.data);
        } else {
          setData(null);
        }
      })
      .catch((err) => console.error("Sankey fetch error:", err))
      .finally(() => setLoading(false));
  }, [open, yearRange]);

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-[95vw] h-[90vh] bg-[#0d1221] border-white/10 text-white flex flex-col p-0 overflow-hidden" data-testid="commodity-sankey-modal">
        <DialogHeader className="p-4 pb-0 border-b border-white/10">
          <DialogTitle className="font-serif text-2xl font-bold text-white flex items-center gap-3">
            <TrendingUp className="w-7 h-7 text-[#FFD93D]" />
            Alir Komoditas Perdagangan (Sankey Flow)
            <span className="text-sm font-normal text-white/40 ml-2">
              Paduan Asal → Komoditas → Tujuan
            </span>
          </DialogTitle>
        </DialogHeader>

        <div className="px-6 py-4 flex items-center gap-4 border-b border-white/10 bg-white/5">
          <Filter className="w-4 h-4 text-white/50" />
          <span className="text-xs text-white/50">Periode Tahun:</span>
          <span className="text-xs font-mono text-[#00D4AA] w-10 text-right">{yearRange[0]}</span>
          <div className="w-[300px]">
            <Slider
              value={yearRange}
              min={1700}
              max={1789}
              step={1}
              onValueChange={setYearRange}
            />
          </div>
          <span className="text-xs font-mono text-[#FF6B6B] w-10">{yearRange[1]}</span>
          <span className="ml-auto text-xs text-white/30 italic flex items-center gap-1">
            <PackageSearch className="w-3 h-3" />
            Teragregasi dalam satuan Gulden (ƒ)
          </span>
        </div>

        <div className="flex-1 flex flex-col relative w-full h-full p-6">
          {loading && (
            <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-[#0d1221]/50 backdrop-blur-sm">
              <Loader2 className="w-10 h-10 animate-spin text-[#00D4AA] mb-4" />
              <p className="text-sm text-white/60">Menghitung matriks pasokan...</p>
            </div>
          )}

          {!loading && !data && (
            <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
              <PackageSearch className="w-12 h-12 text-white/20 mb-4" />
              <p className="text-white/60">Data komoditas untuk periode {yearRange[0]}-{yearRange[1]} tidak mencukupi untuk pemodelan visual.</p>
            </div>
          )}

          {!loading && data && data.nodes.length > 0 && (
            <div className="w-full h-full relative overflow-hidden bg-[#0d1221]/50 border border-white/5 rounded-lg">
              <TransformWrapper
                initialScale={0.9}
                minScale={0.2}
                maxScale={4}
                centerOnInit={true}
                wheel={{ step: 0.1 }}
              >
                {({ zoomIn, zoomOut, resetTransform }) => (
                  <>
                    <div className="absolute top-4 right-4 z-10 flex flex-col gap-2 bg-[#0d1221]/80 backdrop-blur-md p-2 rounded-lg border border-white/10 shadow-lg">
                      <button onClick={() => zoomIn(0.2)} className="p-2 bg-white/5 hover:bg-[#00D4AA]/20 text-white rounded transition-colors" title="Zoom In">
                        <ZoomIn className="w-5 h-5" />
                      </button>
                      <button onClick={() => zoomOut(0.2)} className="p-2 bg-white/5 hover:bg-[#FF6B6B]/20 text-white rounded transition-colors" title="Zoom Out">
                        <ZoomOut className="w-5 h-5" />
                      </button>
                      <button onClick={() => resetTransform()} className="p-2 bg-white/5 hover:bg-white/20 text-white rounded transition-colors" title="Reset View">
                        <Maximize className="w-5 h-5" />
                      </button>
                    </div>

                    <TransformComponent wrapperStyle={{ width: "100%", height: "100%" }}>
                      <div
                        style={{
                          width: 1400,
                          height: Math.max(700, data.nodes.length * 40),
                        }}
                        className="relative px-12 py-8"
                      >
                        <ResponsiveContainer width="100%" height="100%">
                          <Sankey
                            data={data}
                            nodePadding={30}
                            margin={{ top: 20, bottom: 20, left: 40, right: 60 }}
                            node={<CustomNode />}
                            link={{ stroke: 'rgba(255, 255, 255, 0.15)' }}
                            linkCurvature={0.4}
                          >
                            <Tooltip content={<CustomTooltip />} />
                          </Sankey>
                        </ResponsiveContainer>
                      </div>
                    </TransformComponent>
                  </>
                )}
              </TransformWrapper>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
