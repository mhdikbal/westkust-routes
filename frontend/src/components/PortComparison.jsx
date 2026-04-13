import { useState, useEffect, useMemo } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Checkbox } from "@/components/ui/checkbox";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import {
  BarChart, Bar, LineChart, Line, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend, Area, AreaChart,
} from "recharts";
import { GitCompareArrows, Loader2, Ship, TrendingUp, DollarSign, Package, ArrowUpRight, ArrowDownLeft } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

const PORTS = [
  { id: 1, name: "Barus", color: "#16a085" },
  { id: 2, name: "Air Bangis", color: "#2980b9" },
  { id: 3, name: "Padang", color: "#c0392b" },
  { id: 4, name: "Pulau Cingkuak", color: "#e67e22" },
  { id: 5, name: "Air Haji", color: "#27ae60" },
  { id: 6, name: "Jambi", color: "#d35400" },
  { id: 7, name: "Palembang", color: "#8e44ad" },
  { id: 8, name: "Lampung", color: "#7f8c8d" },
  { id: 9, name: "Batavia", color: "#2c3e50" },
];

const CHART_TOOLTIP_STYLE = {
  contentStyle: {
    background: "#0d1221",
    border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: "8px",
    fontSize: "12px",
    color: "#fff",
  },
};

export default function PortComparison({ open, onClose }) {
  const [selectedIds, setSelectedIds] = useState([3, 1, 2]); // Padang, Barus, Air Bangis
  const [yearRange, setYearRange] = useState([1700, 1789]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const togglePort = (id) => {
    if (selectedIds.includes(id)) {
      if (selectedIds.length > 2) {
        setSelectedIds(selectedIds.filter((x) => x !== id));
      }
    } else if (selectedIds.length < 5) {
      setSelectedIds([...selectedIds, id]);
    }
  };

  // Fetch comparison data
  useEffect(() => {
    if (!open || selectedIds.length < 2) return;
    setLoading(true);
    axios
      .get(`${API}/forts/compare`, {
        params: {
          ids: selectedIds.join(","),
          year_from: yearRange[0],
          year_to: yearRange[1],
        },
      })
      .then((res) => setData(res.data))
      .catch((err) => console.error("Compare fetch error:", err))
      .finally(() => setLoading(false));
  }, [open, selectedIds, yearRange]);

  // Process yearly trend data for overlay chart
  const trendData = useMemo(() => {
    if (!data?.ports) return [];
    const yearMap = {};
    data.ports.forEach((port) => {
      port.yearly_trend.forEach((t) => {
        if (!yearMap[t.year]) yearMap[t.year] = { year: t.year };
        yearMap[t.year][port.name] = t.count;
        yearMap[t.year][`${port.name}_val`] = t.value;
      });
    });
    return Object.values(yearMap).sort((a, b) => a.year - b.year);
  }, [data]);

  // Radar chart data
  const radarData = useMemo(() => {
    if (!data?.ports) return [];
    const maxVoyages = Math.max(...data.ports.map((p) => p.total_voyages), 1);
    const maxValue = Math.max(...data.ports.map((p) => p.total_value), 1);
    const maxOut = Math.max(...data.ports.map((p) => p.outbound), 1);
    const maxIn = Math.max(...data.ports.map((p) => p.inbound), 1);
    const maxAvg = Math.max(...data.ports.map((p) => p.avg_cargo_value), 1);
    const maxProducts = Math.max(...data.ports.map((p) => p.top_products.length), 1);

    return [
      {
        metric: "Pelayaran",
        ...Object.fromEntries(
          data.ports.map((p) => [p.name, Math.round((p.total_voyages / maxVoyages) * 100)])
        ),
      },
      {
        metric: "Nilai Total",
        ...Object.fromEntries(
          data.ports.map((p) => [p.name, Math.round((p.total_value / maxValue) * 100)])
        ),
      },
      {
        metric: "Outbound",
        ...Object.fromEntries(
          data.ports.map((p) => [p.name, Math.round((p.outbound / maxOut) * 100)])
        ),
      },
      {
        metric: "Inbound",
        ...Object.fromEntries(
          data.ports.map((p) => [p.name, Math.round((p.inbound / maxIn) * 100)])
        ),
      },
      {
        metric: "Rata-rata",
        ...Object.fromEntries(
          data.ports.map((p) => [p.name, Math.round((p.avg_cargo_value / maxAvg) * 100)])
        ),
      },
      {
        metric: "Keragaman",
        ...Object.fromEntries(
          data.ports.map((p) => [p.name, Math.round((p.top_products.length / maxProducts) * 100)])
        ),
      },
    ];
  }, [data]);

  // Bar chart data
  const barData = useMemo(() => {
    if (!data?.ports) return [];
    return data.ports.map((p) => ({
      name: p.name,
      pelayaran: p.total_voyages,
      outbound: p.outbound,
      inbound: p.inbound,
      nilai: Math.round(p.total_value / 1000),
      fill: p.color,
    }));
  }, [data]);

  const portColorMap = useMemo(() => {
    const m = {};
    PORTS.forEach((p) => (m[p.name] = p.color));
    if (data?.ports) data.ports.forEach((p) => (m[p.name] = p.color));
    return m;
  }, [data]);

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-[95vw] max-h-[95vh] w-[95vw] h-[90vh] bg-[#080c16] border-white/10 text-white p-0 overflow-hidden flex flex-col" data-testid="port-comparison-modal">
        <DialogHeader className="p-4 pb-0 border-b border-white/10">
          <DialogTitle className="font-serif text-2xl font-bold text-white flex items-center gap-3">
            <GitCompareArrows className="w-7 h-7 text-[#FF6B6B]" />
            Perbandingan Antar Pelabuhan
            <span className="text-sm font-normal text-white/40 ml-2">
              Side-by-side Analysis
            </span>
          </DialogTitle>
        </DialogHeader>

        {/* Controls */}
        <div className="px-4 py-3 border-b border-white/10 flex items-center gap-6 flex-wrap">
          {/* Port selector */}
          <div className="flex items-center gap-3 flex-wrap">
            <span className="text-xs text-white/50">Pelabuhan:</span>
            {PORTS.map((port) => (
              <label
                key={port.id}
                className={`flex items-center gap-1.5 px-2 py-1 rounded-full border text-xs cursor-pointer transition-all ${
                  selectedIds.includes(port.id)
                    ? "border-white/30 bg-white/10 text-white"
                    : "border-white/5 text-white/30 hover:text-white/50"
                }`}
                onClick={() => togglePort(port.id)}
              >
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: port.color }} />
                {port.name}
              </label>
            ))}
          </div>

          {/* Year range */}
          <div className="flex items-center gap-3 min-w-[300px]">
            <span className="text-xs text-white/50">Periode:</span>
            <span className="text-xs font-mono text-[#00D4AA] w-10">{yearRange[0]}</span>
            <Slider
              value={yearRange}
              min={1700}
              max={1789}
              step={1}
              onValueChange={setYearRange}
              className="flex-1"
            />
            <span className="text-xs font-mono text-[#FF6B6B] w-10">{yearRange[1]}</span>
          </div>
        </div>

        {/* Content */}
        <ScrollArea className="flex-1">
          <div className="p-4 space-y-6">
            {loading && (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="w-8 h-8 animate-spin text-[#00D4AA]" />
                <span className="ml-3 text-white/60">Memuat perbandingan...</span>
              </div>
            )}

            {!loading && data?.ports && (
              <>
                {/* Summary Cards */}
                <div className="grid gap-4" style={{
                  gridTemplateColumns: `repeat(${data.ports.length}, 1fr)`,
                }}>
                  {data.ports.map((port) => (
                    <Card
                      key={port.id}
                      className="p-4 bg-white/5 border border-white/10 shadow-none relative overflow-hidden"
                    >
                      {/* Color accent bar */}
                      <div
                        className="absolute top-0 left-0 right-0 h-1"
                        style={{ backgroundColor: port.color }}
                      />

                      <div className="flex items-center gap-2 mb-3 mt-1">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: port.color }} />
                        <h3 className="font-serif font-bold text-white text-sm">{port.name}</h3>
                        <span className="text-[10px] text-white/30 capitalize ml-auto">{port.port_type}</span>
                      </div>

                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <div className="flex items-center gap-1 mb-0.5">
                            <Ship className="w-3 h-3 text-white/30" />
                            <span className="text-[10px] text-white/30 uppercase tracking-wider">Pelayaran</span>
                          </div>
                          <p className="text-xl font-bold font-mono text-white">{port.total_voyages}</p>
                        </div>
                        <div>
                          <div className="flex items-center gap-1 mb-0.5">
                            <DollarSign className="w-3 h-3 text-[#FFD93D]/50" />
                            <span className="text-[10px] text-white/30 uppercase tracking-wider">Nilai</span>
                          </div>
                          <p className="text-xl font-bold font-mono text-[#FFD93D]">
                            {port.total_value >= 1000000
                              ? `${(port.total_value / 1000000).toFixed(1)}M`
                              : `${(port.total_value / 1000).toFixed(0)}K`}
                          </p>
                        </div>
                        <div>
                          <div className="flex items-center gap-1 mb-0.5">
                            <ArrowUpRight className="w-3 h-3 text-[#00D4AA]/50" />
                            <span className="text-[10px] text-white/30">OUT</span>
                          </div>
                          <p className="text-sm font-mono text-[#00D4AA]">{port.outbound}</p>
                        </div>
                        <div>
                          <div className="flex items-center gap-1 mb-0.5">
                            <ArrowDownLeft className="w-3 h-3 text-[#FF6B6B]/50" />
                            <span className="text-[10px] text-white/30">IN</span>
                          </div>
                          <p className="text-sm font-mono text-[#FF6B6B]">{port.inbound}</p>
                        </div>
                      </div>

                      <div className="mt-3 pt-2 border-t border-white/5">
                        <span className="text-[10px] text-white/30 uppercase tracking-wider">Avg Cargo</span>
                        <p className="text-sm font-mono text-white/70">
                          {port.avg_cargo_value.toLocaleString()} ƒ
                        </p>
                      </div>
                    </Card>
                  ))}
                </div>

                {/* Charts Row */}
                <div className="grid grid-cols-2 gap-4">
                  {/* Bar Chart */}
                  <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
                    <h3 className="font-serif text-sm font-semibold text-white mb-4 flex items-center gap-2">
                      <Ship className="w-4 h-4 text-[#00D4AA]" />
                      Volume Pelayaran
                    </h3>
                    <ResponsiveContainer width="100%" height={250}>
                      <BarChart
                        data={barData}
                        layout="vertical"
                        margin={{ left: 60 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                        <XAxis type="number" tick={{ fontSize: 10, fill: "rgba(255,255,255,0.5)" }} />
                        <YAxis
                          type="category"
                          dataKey="name"
                          tick={{ fontSize: 11, fill: "rgba(255,255,255,0.7)", fontFamily: "Georgia, serif" }}
                          width={80}
                        />
                        <Tooltip {...CHART_TOOLTIP_STYLE} />
                        <Bar dataKey="outbound" stackId="a" fill="#00D4AA" name="Outbound" radius={[0, 0, 0, 0]} />
                        <Bar dataKey="inbound" stackId="a" fill="#FF6B6B" name="Inbound" radius={[0, 4, 4, 0]} />
                        <Legend
                          wrapperStyle={{ fontSize: "10px", color: "rgba(255,255,255,0.5)" }}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </Card>

                  {/* Radar Chart */}
                  <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
                    <h3 className="font-serif text-sm font-semibold text-white mb-4 flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-[#FFD93D]" />
                      Profil Pelabuhan
                    </h3>
                    <ResponsiveContainer width="100%" height={250}>
                      <RadarChart data={radarData}>
                        <PolarGrid stroke="rgba(255,255,255,0.1)" />
                        <PolarAngleAxis
                          dataKey="metric"
                          tick={{ fontSize: 10, fill: "rgba(255,255,255,0.6)" }}
                        />
                        <PolarRadiusAxis
                          angle={30}
                          domain={[0, 100]}
                          tick={{ fontSize: 8, fill: "rgba(255,255,255,0.3)" }}
                        />
                        {data.ports.map((port) => (
                          <Radar
                            key={port.name}
                            name={port.name}
                            dataKey={port.name}
                            stroke={port.color}
                            fill={port.color}
                            fillOpacity={0.15}
                            strokeWidth={2}
                          />
                        ))}
                        <Legend
                          wrapperStyle={{ fontSize: "10px", color: "rgba(255,255,255,0.5)" }}
                        />
                        <Tooltip {...CHART_TOOLTIP_STYLE} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </Card>
                </div>

                {/* Yearly Trend Overlay */}
                <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
                  <h3 className="font-serif text-sm font-semibold text-white mb-4 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-[#00D4AA]" />
                    Tren Pelayaran per Tahun
                  </h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={trendData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                      <XAxis
                        dataKey="year"
                        tick={{ fontSize: 10, fill: "rgba(255,255,255,0.4)" }}
                      />
                      <YAxis tick={{ fontSize: 10, fill: "rgba(255,255,255,0.4)" }} />
                      <Tooltip {...CHART_TOOLTIP_STYLE} />
                      {data.ports.map((port) => (
                        <Area
                          key={port.name}
                          type="monotone"
                          dataKey={port.name}
                          stroke={port.color}
                          fill={port.color}
                          fillOpacity={0.1}
                          strokeWidth={2}
                          name={port.name}
                          dot={false}
                          activeDot={{ r: 4, fill: port.color }}
                        />
                      ))}
                      <Legend
                        wrapperStyle={{ fontSize: "10px", color: "rgba(255,255,255,0.5)" }}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </Card>

                {/* Top Products per Port */}
                <div className="grid gap-4" style={{
                  gridTemplateColumns: `repeat(${data.ports.length}, 1fr)`,
                }}>
                  {data.ports.map((port) => (
                    <Card
                      key={port.id}
                      className="p-4 bg-white/5 border border-white/10 shadow-none"
                    >
                      <div className="flex items-center gap-2 mb-3">
                        <Package className="w-4 h-4" style={{ color: port.color }} />
                        <h4 className="font-serif text-xs font-semibold text-white">{port.name}</h4>
                      </div>
                      <div className="space-y-2">
                        {port.top_products.slice(0, 6).map((prod, i) => {
                          const maxCount = port.top_products[0]?.count || 1;
                          return (
                            <div key={i} className="flex items-center justify-between">
                              <span className="text-[11px] text-white/60 capitalize truncate flex-1">
                                {prod.name}
                              </span>
                              <div className="flex items-center gap-2 ml-2">
                                <div
                                  className="h-1.5 rounded"
                                  style={{
                                    width: `${(prod.count / maxCount) * 50}px`,
                                    backgroundColor: port.color,
                                    opacity: 0.7,
                                  }}
                                />
                                <span className="text-[10px] font-mono text-white/40 w-6 text-right">
                                  {prod.count}
                                </span>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </Card>
                  ))}
                </div>
              </>
            )}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
