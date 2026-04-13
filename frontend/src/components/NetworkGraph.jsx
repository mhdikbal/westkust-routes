import { useState, useEffect, useRef, useCallback } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Network, ZoomIn, ZoomOut, Maximize2, X, Loader2 } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

export default function NetworkGraph({ open, onClose }) {
  const svgRef = useRef(null);
  const containerRef = useRef(null);
  const simulationRef = useRef(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [yearRange, setYearRange] = useState([1700, 1789]);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [hoveredEdge, setHoveredEdge] = useState(null);
  const [dimensions, setDimensions] = useState({ width: 900, height: 600 });
  const [transform, setTransform] = useState({ x: 0, y: 0, k: 1 });

  // Fetch network data
  useEffect(() => {
    if (!open) return;
    setLoading(true);
    axios
      .get(`${API}/voyages/analytics/network`, {
        params: { year_from: yearRange[0], year_to: yearRange[1] },
      })
      .then((res) => setData(res.data))
      .catch((err) => console.error("Network fetch error:", err))
      .finally(() => setLoading(false));
  }, [open, yearRange]);

  // Update dimensions on resize
  useEffect(() => {
    if (!containerRef.current || !open) return;
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        if (width > 0 && height > 0) {
          setDimensions({ width, height });
        }
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [open]);

  // D3 force simulation
  const renderGraph = useCallback(() => {
    if (!data || !svgRef.current || !open) return;
    
    // Clear previous
    const svg = svgRef.current;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    
    const { width, height } = dimensions;
    const nodes = data.nodes.map((n) => ({
      ...n,
      x: width / 2 + (Math.random() - 0.5) * 200,
      y: height / 2 + (Math.random() - 0.5) * 200,
    }));
    const edges = data.edges.map((e) => ({ ...e }));

    // Map node IDs
    const nodeMap = {};
    nodes.forEach((n) => (nodeMap[n.id] = n));

    // Resolve edges
    const resolvedEdges = edges
      .filter((e) => nodeMap[e.source] && nodeMap[e.target])
      .map((e) => ({
        ...e,
        sourceNode: nodeMap[e.source],
        targetNode: nodeMap[e.target],
      }));

    // Scale functions
    const maxVoyages = Math.max(...nodes.map((n) => n.total_voyages), 1);
    const maxWeight = Math.max(...resolvedEdges.map((e) => e.weight), 1);
    const nodeRadius = (v) => 12 + (v / maxVoyages) * 30;
    const edgeWidth = (w) => 1 + (w / maxWeight) * 8;

    // Simple force simulation (no D3 dependency needed for basic layout)
    const centerX = width / 2;
    const centerY = height / 2;

    // Position nodes in a circular layout initially
    const angleStep = (2 * Math.PI) / nodes.length;
    nodes.forEach((n, i) => {
      n.x = centerX + Math.cos(angleStep * i) * Math.min(width, height) * 0.35;
      n.y = centerY + Math.sin(angleStep * i) * Math.min(width, height) * 0.35;
    });

    // Simple spring simulation
    const simulate = () => {
      for (let iter = 0; iter < 100; iter++) {
        // Repulsion between nodes
        for (let i = 0; i < nodes.length; i++) {
          for (let j = i + 1; j < nodes.length; j++) {
            const dx = nodes[j].x - nodes[i].x;
            const dy = nodes[j].y - nodes[i].y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;
            const force = 5000 / (dist * dist);
            const fx = (dx / dist) * force;
            const fy = (dy / dist) * force;
            nodes[i].x -= fx;
            nodes[i].y -= fy;
            nodes[j].x += fx;
            nodes[j].y += fy;
          }
        }

        // Attraction along edges
        resolvedEdges.forEach((e) => {
          const dx = e.targetNode.x - e.sourceNode.x;
          const dy = e.targetNode.y - e.sourceNode.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          const force = (dist - 150) * 0.01;
          const fx = (dx / dist) * force;
          const fy = (dy / dist) * force;
          e.sourceNode.x += fx;
          e.sourceNode.y += fy;
          e.targetNode.x -= fx;
          e.targetNode.y -= fy;
        });

        // Center gravity
        nodes.forEach((n) => {
          n.x += (centerX - n.x) * 0.01;
          n.y += (centerY - n.y) * 0.01;
          // Bounds
          n.x = Math.max(50, Math.min(width - 50, n.x));
          n.y = Math.max(50, Math.min(height - 50, n.y));
        });
      }
    };

    simulate();

    // Create SVG elements
    const ns = "http://www.w3.org/2000/svg";

    // Defs for arrows and glow
    const defs = document.createElementNS(ns, "defs");
    
    // Glow filter
    const filter = document.createElementNS(ns, "filter");
    filter.setAttribute("id", "glow");
    filter.setAttribute("x", "-50%");
    filter.setAttribute("y", "-50%");
    filter.setAttribute("width", "200%");
    filter.setAttribute("height", "200%");
    const blur = document.createElementNS(ns, "feGaussianBlur");
    blur.setAttribute("stdDeviation", "3");
    blur.setAttribute("result", "coloredBlur");
    filter.appendChild(blur);
    const merge = document.createElementNS(ns, "feMerge");
    const mergeNode1 = document.createElementNS(ns, "feMergeNode");
    mergeNode1.setAttribute("in", "coloredBlur");
    const mergeNode2 = document.createElementNS(ns, "feMergeNode");
    mergeNode2.setAttribute("in", "SourceGraphic");
    merge.appendChild(mergeNode1);
    merge.appendChild(mergeNode2);
    filter.appendChild(merge);
    defs.appendChild(filter);

    // Arrow markers
    const EDGE_COLORS = { outbound: "#00D4AA", inbound: "#FF6B6B" };
    Object.entries(EDGE_COLORS).forEach(([dir, color]) => {
      const marker = document.createElementNS(ns, "marker");
      marker.setAttribute("id", `arrow-${dir}`);
      marker.setAttribute("viewBox", "0 0 10 10");
      marker.setAttribute("refX", "10");
      marker.setAttribute("refY", "5");
      marker.setAttribute("markerWidth", "6");
      marker.setAttribute("markerHeight", "6");
      marker.setAttribute("orient", "auto-start-reverse");
      const path = document.createElementNS(ns, "path");
      path.setAttribute("d", "M 0 0 L 10 5 L 0 10 z");
      path.setAttribute("fill", color);
      path.setAttribute("opacity", "0.7");
      marker.appendChild(path);
      defs.appendChild(marker);
    });

    svg.appendChild(defs);

    // Transform group
    const g = document.createElementNS(ns, "g");
    g.setAttribute("transform", `translate(${transform.x},${transform.y}) scale(${transform.k})`);

    // Draw edges
    resolvedEdges.forEach((e) => {
      const line = document.createElementNS(ns, "line");
      line.setAttribute("x1", e.sourceNode.x);
      line.setAttribute("y1", e.sourceNode.y);
      line.setAttribute("x2", e.targetNode.x);
      line.setAttribute("y2", e.targetNode.y);
      const edgeColor = EDGE_COLORS[e.direction] || "#ffffff";
      line.setAttribute("stroke", edgeColor);
      line.setAttribute("stroke-width", edgeWidth(e.weight));
      line.setAttribute("stroke-opacity", "0.3");
      line.setAttribute("stroke-linecap", "round");
      line.setAttribute("marker-end", `url(#arrow-${e.direction || "outbound"})`);

      // Hover events
      line.addEventListener("mouseenter", () => {
        line.setAttribute("stroke-opacity", "0.8");
        line.setAttribute("stroke-width", edgeWidth(e.weight) + 2);
        setHoveredEdge(e);
      });
      line.addEventListener("mouseleave", () => {
        line.setAttribute("stroke-opacity", "0.3");
        line.setAttribute("stroke-width", edgeWidth(e.weight));
        setHoveredEdge(null);
      });

      g.appendChild(line);

      // Weight label on edge
      if (e.weight > 5) {
        const label = document.createElementNS(ns, "text");
        label.setAttribute("x", (e.sourceNode.x + e.targetNode.x) / 2);
        label.setAttribute("y", (e.sourceNode.y + e.targetNode.y) / 2 - 5);
        label.setAttribute("text-anchor", "middle");
        label.setAttribute("fill", "rgba(255,255,255,0.3)");
        label.setAttribute("font-size", "9");
        label.setAttribute("font-family", "monospace");
        label.textContent = `${e.weight}×`;
        g.appendChild(label);
      }
    });

    // Draw nodes
    nodes.forEach((n) => {
      const r = nodeRadius(n.total_voyages);
      
      // Glow circle
      const glow = document.createElementNS(ns, "circle");
      glow.setAttribute("cx", n.x);
      glow.setAttribute("cy", n.y);
      glow.setAttribute("r", r + 4);
      glow.setAttribute("fill", n.color);
      glow.setAttribute("opacity", "0.15");
      glow.setAttribute("filter", "url(#glow)");
      g.appendChild(glow);

      // Main circle
      const circle = document.createElementNS(ns, "circle");
      circle.setAttribute("cx", n.x);
      circle.setAttribute("cy", n.y);
      circle.setAttribute("r", r);
      circle.setAttribute("fill", n.color);
      circle.setAttribute("stroke", "rgba(255,255,255,0.3)");
      circle.setAttribute("stroke-width", "2");
      circle.setAttribute("cursor", "pointer");
      circle.style.transition = "r 0.2s, stroke-width 0.2s";

      circle.addEventListener("mouseenter", () => {
        circle.setAttribute("r", r + 4);
        circle.setAttribute("stroke-width", "3");
        circle.setAttribute("stroke", "rgba(255,255,255,0.8)");
        setHoveredNode(n);
      });
      circle.addEventListener("mouseleave", () => {
        circle.setAttribute("r", r);
        circle.setAttribute("stroke-width", "2");
        circle.setAttribute("stroke", "rgba(255,255,255,0.3)");
        setHoveredNode(null);
      });
      g.appendChild(circle);

      // Label
      const label = document.createElementNS(ns, "text");
      label.setAttribute("x", n.x);
      label.setAttribute("y", n.y + r + 16);
      label.setAttribute("text-anchor", "middle");
      label.setAttribute("fill", "white");
      label.setAttribute("font-size", "12");
      label.setAttribute("font-weight", "600");
      label.setAttribute("font-family", "'Georgia', serif");
      label.style.textShadow = "0 1px 3px rgba(0,0,0,0.8)";
      label.textContent = n.id;
      g.appendChild(label);

      // Voyage count inside node
      const count = document.createElementNS(ns, "text");
      count.setAttribute("x", n.x);
      count.setAttribute("y", n.y + 4);
      count.setAttribute("text-anchor", "middle");
      count.setAttribute("fill", "white");
      count.setAttribute("font-size", r > 20 ? "11" : "8");
      count.setAttribute("font-weight", "700");
      count.setAttribute("font-family", "monospace");
      count.textContent = n.total_voyages;
      g.appendChild(count);
    });

    svg.appendChild(g);
  }, [data, dimensions, transform, open]);

  useEffect(() => {
    renderGraph();
  }, [renderGraph]);

  const handleZoom = (delta) => {
    setTransform((prev) => ({
      ...prev,
      k: Math.max(0.3, Math.min(3, prev.k + delta)),
    }));
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-[95vw] max-h-[95vh] w-[95vw] h-[90vh] bg-[#080c16] border-white/10 text-white p-0 overflow-hidden flex flex-col" data-testid="network-graph-modal">
        <DialogHeader className="p-4 pb-0 border-b border-white/10">
          <DialogTitle className="font-serif text-2xl font-bold text-white flex items-center gap-3">
            <Network className="w-7 h-7 text-[#00D4AA]" />
            Jaringan Pelabuhan VOC
            <span className="text-sm font-normal text-white/40 ml-2">
              Network Graph — {yearRange[0]}–{yearRange[1]}
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
              className="flex-1"
            />
            <span className="text-xs font-mono text-[#FF6B6B] w-10">{yearRange[1]}</span>
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => handleZoom(0.2)}
              className="p-1.5 rounded bg-white/5 hover:bg-white/10 text-white/60 hover:text-white transition-colors"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
            <button
              onClick={() => handleZoom(-0.2)}
              className="p-1.5 rounded bg-white/5 hover:bg-white/10 text-white/60 hover:text-white transition-colors"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
            <button
              onClick={() => setTransform({ x: 0, y: 0, k: 1 })}
              className="p-1.5 rounded bg-white/5 hover:bg-white/10 text-white/60 hover:text-white transition-colors"
            >
              <Maximize2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Graph Container */}
        <div ref={containerRef} className="flex-1 relative overflow-hidden">
          {loading && (
            <div className="absolute inset-0 flex items-center justify-center bg-[#080c16]/80 z-10">
              <Loader2 className="w-8 h-8 animate-spin text-[#00D4AA]" />
              <span className="ml-3 text-white/60">Memuat jaringan...</span>
            </div>
          )}

          <svg
            ref={svgRef}
            width={dimensions.width}
            height={dimensions.height}
            className="w-full h-full"
            style={{ background: "radial-gradient(circle at center, #0f1729 0%, #080c16 100%)" }}
          />

          {/* Tooltip for hovered node */}
          {hoveredNode && (
            <div className="absolute top-4 right-4 bg-[#0d1221]/95 backdrop-blur-xl border border-white/10 rounded-lg p-4 min-w-[200px] shadow-2xl z-20">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: hoveredNode.color }} />
                <h4 className="font-serif font-bold text-white">{hoveredNode.id}</h4>
              </div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-white/40">Total Pelayaran</span>
                  <span className="text-white font-mono">{hoveredNode.total_voyages}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/40">Total Nilai</span>
                  <span className="text-[#FFD93D] font-mono">{hoveredNode.total_value.toLocaleString()} ƒ</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/40">Tipe</span>
                  <span className="text-white/70 capitalize">{hoveredNode.port_type}</span>
                </div>
              </div>
            </div>
          )}

          {/* Tooltip for hovered edge */}
          {hoveredEdge && !hoveredNode && (
            <div className="absolute top-4 right-4 bg-[#0d1221]/95 backdrop-blur-xl border border-white/10 rounded-lg p-4 min-w-[200px] shadow-2xl z-20">
              <h4 className="font-serif font-bold text-white text-sm mb-2">
                {hoveredEdge.source} → {hoveredEdge.target}
              </h4>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-white/40">Frekuensi</span>
                  <span className="text-white font-mono">{hoveredEdge.weight}×</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/40">Total Nilai</span>
                  <span className="text-[#FFD93D] font-mono">{hoveredEdge.total_value.toLocaleString()} ƒ</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/40">Arah</span>
                  <span className={hoveredEdge.direction === "outbound" ? "text-[#00D4AA]" : "text-[#FF6B6B]"}>
                    {hoveredEdge.direction === "outbound" ? "🚢 Keluar" : "🏠 Masuk"}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Legend */}
          <div className="absolute bottom-4 left-4 bg-[#0d1221]/90 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-xs space-y-2">
            <p className="text-white/40 uppercase tracking-wider text-[10px] font-semibold mb-1">Legenda</p>
            <div className="flex items-center gap-2">
              <div className="w-8 h-0.5 bg-[#00D4AA]" />
              <span className="text-white/60">Outbound (keluar)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-0.5 bg-[#FF6B6B]" />
              <span className="text-white/60">Inbound (masuk)</span>
            </div>
            <div className="flex items-center gap-2 mt-1">
              <div className="flex gap-1">
                <div className="w-2 h-2 rounded-full bg-white/40" />
                <div className="w-4 h-4 rounded-full bg-white/40" />
              </div>
              <span className="text-white/60">Ukuran = jumlah pelayaran</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex flex-col gap-0.5">
                <div className="w-8 h-px bg-white/40" />
                <div className="w-8 h-1 bg-white/40" />
              </div>
              <span className="text-white/60">Ketebalan = frekuensi rute</span>
            </div>
          </div>

          {/* Stats overlay */}
          {data && !loading && (
            <div className="absolute bottom-4 right-4 bg-[#0d1221]/90 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-xs grid grid-cols-2 gap-x-6 gap-y-1">
              <span className="text-white/40">Pelabuhan</span>
              <span className="text-white font-mono text-right">{data.nodes.length}</span>
              <span className="text-white/40">Rute</span>
              <span className="text-white font-mono text-right">{data.edges.length}</span>
              <span className="text-white/40">Total Perjalanan</span>
              <span className="text-white font-mono text-right">
                {data.edges.reduce((s, e) => s + e.weight, 0)}
              </span>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
