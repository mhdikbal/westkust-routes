import { useState, useEffect, useMemo } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Slider } from "@/components/ui/slider";
import { Grid3X3, Loader2, BarChart3, Hash } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

// Color scale from dark navy → teal → gold → white-hot
function getHeatColor(value, max) {
  if (max === 0 || value === 0) return "rgba(255,255,255,0.02)";
  const t = Math.min(value / max, 1);

  // Multi-stop gradient
  if (t < 0.25) {
    const lt = t / 0.25;
    return `rgba(${Math.round(13 + lt * 7)}, ${Math.round(18 + lt * 40)}, ${Math.round(33 + lt * 70)}, ${0.3 + lt * 0.3})`;
  } else if (t < 0.5) {
    const lt = (t - 0.25) / 0.25;
    return `rgba(${Math.round(20 + lt * 0)}, ${Math.round(58 + lt * 150)}, ${Math.round(103 + lt * 67)}, ${0.6 + lt * 0.2})`;
  } else if (t < 0.75) {
    const lt = (t - 0.5) / 0.25;
    return `rgba(${Math.round(20 + lt * 235)}, ${Math.round(208 - lt * 40)}, ${Math.round(170 - lt * 100)}, ${0.8 + lt * 0.1})`;
  } else {
    const lt = (t - 0.75) / 0.25;
    return `rgba(${Math.round(255)}, ${Math.round(168 + lt * 49)}, ${Math.round(70 - lt * 9)}, ${0.9 + lt * 0.1})`;
  }
}

function getCountColor(value, max) {
  if (max === 0 || value === 0) return "rgba(255,255,255,0.02)";
  const t = Math.min(value / max, 1);
  
  if (t < 0.33) {
    const lt = t / 0.33;
    return `rgba(0, ${Math.round(80 + lt * 132)}, ${Math.round(80 + lt * 90)}, ${0.3 + lt * 0.3})`;
  } else if (t < 0.66) {
    const lt = (t - 0.33) / 0.33;
    return `rgba(${Math.round(lt * 255)}, ${Math.round(212 - lt * 0)}, ${Math.round(170 - lt * 107)}, ${0.6 + lt * 0.2})`;
  } else {
    const lt = (t - 0.66) / 0.34;
    return `rgba(255, ${Math.round(212 - lt * 105)}, ${Math.round(63 - lt * 2)}, ${0.8 + lt * 0.2})`;
  }
}

export default function TemporalHeatmap({ open, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metric, setMetric] = useState("count"); // "count" | "value"
  const [hoveredCell, setHoveredCell] = useState(null);
  const [yearRange, setYearRange] = useState([1700, 1789]);

  useEffect(() => {
    if (!open) return;
    setLoading(true);
    axios
      .get(`${API}/voyages/analytics/heatmap`, {
        params: { metric, year_from: yearRange[0], year_to: yearRange[1] },
      })
      .then((res) => setData(res.data))
      .catch((err) => console.error("Heatmap fetch error:", err))
      .finally(() => setLoading(false));
  }, [open, metric, yearRange]);

  // Build lookup matrix
  const { matrix, maxVal } = useMemo(() => {
    if (!data) return { matrix: {}, maxVal: 0 };
    const m = {};
    let max = 0;
    data.data.forEach((cell) => {
      const key = `${cell.year}-${cell.port}`;
      const val = metric === "count" ? cell.count : cell.value;
      m[key] = { count: cell.count, value: cell.value };
      if (val > max) max = val;
    });
    return { matrix: m, maxVal: max };
  }, [data, metric]);

  const colorFn = metric === "count" ? getCountColor : getHeatColor;

  // Cell size calculation
  const years = data?.years || [];
  const ports = data?.ports || [];
  const cellW = years.length > 50 ? 14 : years.length > 30 ? 18 : 24;
  const cellH = 36;

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-[95vw] max-h-[95vh] w-[95vw] h-[90vh] bg-[#080c16] border-white/10 text-white p-0 overflow-hidden flex flex-col" data-testid="heatmap-modal">
        <DialogHeader className="p-4 pb-0 border-b border-white/10">
          <DialogTitle className="font-serif text-2xl font-bold text-white flex items-center gap-3">
            <Grid3X3 className="w-7 h-7 text-[#FFD93D]" />
            Heatmap Temporal Perdagangan
            <span className="text-sm font-normal text-white/40 ml-2">
              {yearRange[0]}–{yearRange[1]}
            </span>
          </DialogTitle>
        </DialogHeader>

        {/* Controls */}
        <div className="px-4 py-3 border-b border-white/10 flex items-center gap-6">
          <div className="flex items-center gap-3 flex-1">
            <span className="text-xs text-white/50 w-16">Periode:</span>
            <span className="text-xs font-mono text-[#00D4AA] w-10">{yearRange[0]}</span>
            <Slider
              value={yearRange}
              min={1700}
              max={1789}
              step={1}
              onValueChange={setYearRange}
              className="flex-1 max-w-md"
            />
            <span className="text-xs font-mono text-[#FF6B6B] w-10">{yearRange[1]}</span>
          </div>

          {/* Metric toggle */}
          <div className="flex items-center gap-1 bg-white/5 rounded-lg p-0.5 border border-white/10">
            <button
              onClick={() => setMetric("count")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                metric === "count"
                  ? "bg-[#00D4AA]/20 text-[#00D4AA]"
                  : "text-white/40 hover:text-white/60"
              }`}
            >
              <Hash className="w-3 h-3" />
              Jumlah
            </button>
            <button
              onClick={() => setMetric("value")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                metric === "value"
                  ? "bg-[#FFD93D]/20 text-[#FFD93D]"
                  : "text-white/40 hover:text-white/60"
              }`}
            >
              <BarChart3 className="w-3 h-3" />
              Nilai (Gulden)
            </button>
          </div>
        </div>

        {/* Heatmap */}
        <div className="flex-1 overflow-auto p-4">
          {loading && (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="w-8 h-8 animate-spin text-[#00D4AA]" />
              <span className="ml-3 text-white/60">Memuat heatmap...</span>
            </div>
          )}

          {!loading && data && (
            <div className="relative">
              {/* Grid */}
              <div className="flex">
                {/* Port labels (Y axis) */}
                <div className="flex flex-col flex-shrink-0" style={{ marginTop: cellH + 4 }}>
                  {ports.map((port) => (
                    <div
                      key={port}
                      className="flex items-center justify-end pr-3 font-serif text-xs text-white/70 font-semibold"
                      style={{ height: cellH }}
                    >
                      {port}
                    </div>
                  ))}
                </div>

                {/* Heatmap grid */}
                <div className="overflow-x-auto flex-1">
                  {/* Year labels (X axis) */}
                  <div className="flex" style={{ height: cellH }}>
                    {years.map((year) => (
                      <div
                        key={year}
                        className="text-center text-[10px] text-white/40 font-mono flex items-end justify-center pb-1"
                        style={{ width: cellW, minWidth: cellW }}
                      >
                        {year % 5 === 0 ? year : ""}
                      </div>
                    ))}
                  </div>

                  {/* Cells */}
                  {ports.map((port) => (
                    <div key={port} className="flex" style={{ height: cellH }}>
                      {years.map((year) => {
                        const key = `${year}-${port}`;
                        const cell = matrix[key] || { count: 0, value: 0 };
                        const val = metric === "count" ? cell.count : cell.value;
                        const isHovered =
                          hoveredCell?.year === year && hoveredCell?.port === port;

                        return (
                          <div
                            key={key}
                            className="border border-white/[0.03] transition-all duration-150 cursor-crosshair relative"
                            style={{
                              width: cellW,
                              minWidth: cellW,
                              height: cellH - 2,
                              backgroundColor: colorFn(val, maxVal),
                              transform: isHovered ? "scale(1.3)" : "scale(1)",
                              zIndex: isHovered ? 10 : 1,
                              borderColor: isHovered
                                ? "rgba(255,255,255,0.5)"
                                : "rgba(255,255,255,0.03)",
                              borderRadius: isHovered ? "4px" : "1px",
                            }}
                            onMouseEnter={() =>
                              setHoveredCell({ year, port, ...cell })
                            }
                            onMouseLeave={() => setHoveredCell(null)}
                          >
                            {/* Show value in cell if big enough */}
                            {cellW >= 22 && val > 0 && (
                              <span className="absolute inset-0 flex items-center justify-center text-[8px] font-mono text-white/50">
                                {metric === "count"
                                  ? val
                                  : val >= 1000
                                  ? `${(val / 1000).toFixed(0)}k`
                                  : val.toFixed(0)}
                              </span>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  ))}
                </div>
              </div>

              {/* Hover tooltip */}
              {hoveredCell && (
                <div className="fixed z-50 pointer-events-none" style={{
                  left: "50%",
                  top: "10%",
                  transform: "translateX(-50%)",
                }}>
                  <div className="bg-[#0d1221]/95 backdrop-blur-xl border border-white/10 rounded-lg p-4 shadow-2xl min-w-[220px]">
                    <div className="flex items-center gap-2 mb-2">
                      <div
                        className="w-3 h-3 rounded"
                        style={{
                          backgroundColor: colorFn(
                            metric === "count" ? hoveredCell.count : hoveredCell.value,
                            maxVal
                          ),
                        }}
                      />
                      <h4 className="font-serif font-bold text-white text-sm">
                        {hoveredCell.port} — {hoveredCell.year}
                      </h4>
                    </div>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-white/40">Jumlah Pelayaran</span>
                        <span className="text-[#00D4AA] font-mono font-bold">
                          {hoveredCell.count}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-white/40">Nilai Cargo</span>
                        <span className="text-[#FFD93D] font-mono font-bold">
                          {hoveredCell.value > 0
                            ? `${hoveredCell.value.toLocaleString()} ƒ`
                            : "—"}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Color scale legend */}
              <div className="mt-6 flex items-center justify-center gap-4">
                <span className="text-[10px] text-white/30 uppercase tracking-wider">
                  {metric === "count" ? "Sedikit" : "Rendah"}
                </span>
                <div className="flex h-3 rounded-full overflow-hidden border border-white/10 w-48">
                  {Array.from({ length: 20 }, (_, i) => (
                    <div
                      key={i}
                      className="flex-1"
                      style={{
                        backgroundColor: colorFn(
                          (i / 19) * maxVal,
                          maxVal
                        ),
                      }}
                    />
                  ))}
                </div>
                <span className="text-[10px] text-white/30 uppercase tracking-wider">
                  {metric === "count" ? "Banyak" : "Tinggi"}
                </span>
                <span className="text-[10px] text-white/20 ml-2">
                  Max: {metric === "count" ? maxVal : `${maxVal.toLocaleString()} ƒ`}
                </span>
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
