import { useState } from "react";

/**
 * RouteLegend — Direction filter + visual legend overlay
 * 
 * Shows outbound/inbound/transit colors and counts.
 * Toggle between "all", "outbound", "inbound" directions.
 */

const DIRECTION_CONFIG = {
  outbound: {
    color: "#00D4AA",
    label: "Keberangkatan",
    sublabel: "Dari Sumatera Westkust",
    icon: "🚢",
  },
  inbound: {
    color: "#FF6B6B",
    label: "Kedatangan",
    sublabel: "Menuju Sumatera Westkust",
    icon: "🏠",
  },
  transit: {
    color: "#FFD93D",
    label: "Transit",
    sublabel: "Antar pelabuhan lain",
    icon: "🔄",
  },
};

export default function RouteLegend({ directionFilter, setDirectionFilter, stats }) {
  const [isExpanded, setIsExpanded] = useState(true);

  const outboundCount = stats?.outbound_count || 0;
  const inboundCount = stats?.inbound_count || 0;
  const transitCount = stats?.transit_count || 0;
  const totalVoyages = stats?.total_voyages || 0;

  return (
    <div
      className="absolute top-4 right-4 z-20"
      style={{
        fontFamily: "'Inter', 'Segoe UI', sans-serif",
      }}
    >
      {/* Toggle button */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="mb-2 ml-auto block"
        style={{
          background: "rgba(15, 20, 35, 0.85)",
          backdropFilter: "blur(12px)",
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: "8px",
          padding: "6px 12px",
          color: "#fff",
          fontSize: "12px",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          gap: "6px",
        }}
      >
        <span style={{ fontSize: "14px" }}>🗺️</span>
        {isExpanded ? "Tutup Legenda" : "Legenda Rute"}
      </button>

      {isExpanded && (
        <div
          style={{
            background: "rgba(15, 20, 35, 0.9)",
            backdropFilter: "blur(16px)",
            border: "1px solid rgba(255,255,255,0.08)",
            borderRadius: "12px",
            padding: "16px",
            minWidth: "220px",
            boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
          }}
        >
          {/* Title */}
          <div style={{ marginBottom: "12px" }}>
            <h3 style={{
              color: "#fff",
              fontSize: "13px",
              fontWeight: 600,
              margin: 0,
              letterSpacing: "0.5px",
            }}>
              ARAH PELAYARAN
            </h3>
            <p style={{
              color: "rgba(255,255,255,0.4)",
              fontSize: "11px",
              margin: "4px 0 0",
            }}>
              {totalVoyages.toLocaleString()} total voyages
            </p>
          </div>

          {/* "All" filter button */}
          <button
            onClick={() => setDirectionFilter("all")}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              width: "100%",
              padding: "8px 10px",
              marginBottom: "6px",
              borderRadius: "8px",
              border: directionFilter === "all"
                ? "1px solid rgba(255,255,255,0.3)"
                : "1px solid transparent",
              background: directionFilter === "all"
                ? "rgba(255,255,255,0.1)"
                : "transparent",
              color: "#fff",
              cursor: "pointer",
              fontSize: "12px",
              transition: "all 0.2s ease",
            }}
          >
            <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <span style={{ fontSize: "14px" }}>🌐</span>
              <span>Semua Arah</span>
            </span>
            <span style={{
              fontSize: "11px",
              color: "rgba(255,255,255,0.5)",
              fontWeight: 500,
            }}>
              {totalVoyages.toLocaleString()}
            </span>
          </button>

          {/* Direction buttons */}
          {Object.entries(DIRECTION_CONFIG).map(([key, config]) => {
            const count = key === "outbound" ? outboundCount
              : key === "inbound" ? inboundCount
              : transitCount;
            const isActive = directionFilter === key;

            return (
              <button
                key={key}
                onClick={() => setDirectionFilter(isActive ? "all" : key)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  width: "100%",
                  padding: "8px 10px",
                  marginBottom: "4px",
                  borderRadius: "8px",
                  border: isActive
                    ? `1px solid ${config.color}40`
                    : "1px solid transparent",
                  background: isActive
                    ? `${config.color}15`
                    : "transparent",
                  color: "#fff",
                  cursor: "pointer",
                  fontSize: "12px",
                  transition: "all 0.2s ease",
                }}
              >
                <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  {/* Color dot */}
                  <span
                    style={{
                      width: "10px",
                      height: "10px",
                      borderRadius: "50%",
                      backgroundColor: config.color,
                      boxShadow: isActive ? `0 0 8px ${config.color}80` : "none",
                      transition: "box-shadow 0.3s ease",
                    }}
                  />
                  <span style={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
                    <span style={{ fontWeight: 500 }}>{config.label}</span>
                    <span style={{
                      fontSize: "10px",
                      color: "rgba(255,255,255,0.3)",
                      marginTop: "1px",
                    }}>
                      {config.sublabel}
                    </span>
                  </span>
                </span>
                <span style={{
                  fontSize: "11px",
                  color: isActive ? config.color : "rgba(255,255,255,0.5)",
                  fontWeight: 600,
                  fontVariantNumeric: "tabular-nums",
                }}>
                  {count.toLocaleString()}
                </span>
              </button>
            );
          })}

          {/* Animated line preview */}
          <div style={{
            marginTop: "12px",
            padding: "8px",
            borderRadius: "8px",
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.05)",
          }}>
            <svg width="100%" height="24" viewBox="0 0 190 24">
              {/* Outbound preview */}
              <line x1="5" y1="8" x2="90" y2="8" stroke="#00D4AA" strokeWidth="2.5" strokeLinecap="round">
                <animate attributeName="stroke-dashoffset" from="20" to="0" dur="2s" repeatCount="indefinite" />
              </line>
              <line x1="5" y1="8" x2="90" y2="8" stroke="#00D4AA" strokeWidth="2.5" strokeDasharray="4 6" strokeLinecap="round" opacity="0.6">
                <animate attributeName="stroke-dashoffset" from="20" to="0" dur="1.5s" repeatCount="indefinite" />
              </line>
              <text x="50" y="22" fill="rgba(255,255,255,0.3)" fontSize="8" textAnchor="middle">OUTBOUND</text>

              {/* Inbound preview */}
              <line x1="100" y1="8" x2="185" y2="8" stroke="#FF6B6B" strokeWidth="2.5" strokeLinecap="round">
                <animate attributeName="stroke-dashoffset" from="0" to="20" dur="2s" repeatCount="indefinite" />
              </line>
              <line x1="100" y1="8" x2="185" y2="8" stroke="#FF6B6B" strokeWidth="2.5" strokeDasharray="4 6" strokeLinecap="round" opacity="0.6">
                <animate attributeName="stroke-dashoffset" from="0" to="20" dur="1.5s" repeatCount="indefinite" />
              </line>
              <text x="143" y="22" fill="rgba(255,255,255,0.3)" fontSize="8" textAnchor="middle">INBOUND</text>
            </svg>
          </div>
        </div>
      )}
    </div>
  );
}
