import { useEffect, useRef } from "react";
import { useMap } from "react-map-gl/maplibre";

/**
 * PortMarkers — Fort/port icons on the map
 *
 * Renders all 9 ports with SVG fort icons.
 * Port type indicated by color ring:
 *   - Departure ports: teal ring
 *   - Arrival ports: coral ring
 *   - Both: gold ring (Padang)
 */

const PORT_TYPE_MAP = {
  Barus: "departure",
  "Air Bangis": "departure",
  Padang: "both",
  "Pulau Cingkuak": "departure",
  "Air Haji": "departure",
  Jambi: "arrival",
  Palembang: "arrival",
  Lampung: "arrival",
  Batavia: "arrival",
};

const TYPE_RING_COLOR = {
  departure: "#00D4AA",
  arrival: "#FF6B6B",
  both: "#FFD93D",
};

function createFortSVG(portColor, ringColor) {
  return `
    <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
      <!-- Outer glow -->
      <circle cx="20" cy="20" r="18" fill="none" stroke="${ringColor}" stroke-width="2" opacity="0.4"/>
      <!-- Main circle -->
      <circle cx="20" cy="20" r="14" fill="${portColor}" stroke="#FFFFFF" stroke-width="2"/>
      <!-- Fort silhouette -->
      <g transform="translate(20, 20)">
        <rect x="-6" y="-4" width="12" height="8" fill="#FFFFFF" rx="1"/>
        <rect x="-8" y="-7" width="3" height="3" fill="#FFFFFF" rx="0.5"/>
        <rect x="5" y="-7" width="3" height="3" fill="#FFFFFF" rx="0.5"/>
        <rect x="-1.5" y="-1" width="3" height="5" fill="${portColor}" rx="0.5"/>
      </g>
    </svg>
  `;
}

export default function PortMarkers({ ports, onPortClick, portColors }) {
  const { current: map } = useMap();
  const markersAdded = useRef(false);

  useEffect(() => {
    if (!map || !map.getMap || markersAdded.current) return;

    const maplibreMap = map.getMap();
    if (!maplibreMap) return;

    const setupMarkers = async () => {
      try {
        const portEntries = Object.entries(ports);
        
        // Create an image for each port (unique color)
        const imagePromises = portEntries.map(([name, coords]) => {
          return new Promise((resolve) => {
            const color = portColors?.[name] || "#B85D19";
            const portType = PORT_TYPE_MAP[name] || "departure";
            const ringColor = TYPE_RING_COLOR[portType];
            const svg = createFortSVG(color, ringColor);
            
            const img = new Image(40, 40);
            img.onload = () => {
              const imageId = `fort-${name.replace(/\s/g, "-").toLowerCase()}`;
              if (!maplibreMap.hasImage(imageId)) {
                maplibreMap.addImage(imageId, img);
              }
              resolve({ name, coords, imageId, portType });
            };
            img.onerror = () => resolve(null);
            img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
          });
        });

        const portData = (await Promise.all(imagePromises)).filter(Boolean);

        // Add a separate source and layer for each port (so each uses its own icon)
        portData.forEach(({ name, coords, imageId, portType }) => {
          const sourceId = `port-src-${name.replace(/\s/g, "-").toLowerCase()}`;
          const layerId = `port-lyr-${name.replace(/\s/g, "-").toLowerCase()}`;

          const displayName = name === "Batavia" ? "Sunda Kelapa (Batavia)" : name;
          const typeLabel = portType === "departure" ? "⬆ Keberangkatan"
            : portType === "arrival" ? "⬇ Kedatangan"
            : "⬆⬇ Keberangkatan & Kedatangan";

          if (!maplibreMap.getSource(sourceId)) {
            maplibreMap.addSource(sourceId, {
              type: "geojson",
              data: {
                type: "FeatureCollection",
                features: [{
                  type: "Feature",
                  properties: { name, displayName, typeLabel },
                  geometry: { type: "Point", coordinates: coords },
                }],
              },
            });
          }

          if (!maplibreMap.getLayer(layerId)) {
            maplibreMap.addLayer({
              id: layerId,
              type: "symbol",
              source: sourceId,
              layout: {
                "icon-image": imageId,
                "icon-size": 1,
                "icon-allow-overlap": true,
                "text-field": ["get", "displayName"],
                "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
                "text-size": 12,
                "text-offset": [0, 2.2],
                "text-anchor": "top",
              },
              paint: {
                "text-color": "#FFFFFF",
                "text-halo-color": "rgba(0,0,0,0.7)",
                "text-halo-width": 2,
              },
            });

            // Click handler
            maplibreMap.on("click", layerId, (e) => {
              if (e.features && e.features.length > 0) {
                const portName = e.features[0].properties.name;
                onPortClick(portName);
                e.originalEvent.stopPropagation();
              }
            });

            maplibreMap.on("mouseenter", layerId, () => {
              maplibreMap.getCanvas().style.cursor = "pointer";
            });

            maplibreMap.on("mouseleave", layerId, () => {
              maplibreMap.getCanvas().style.cursor = "";
            });
          }
        });

        markersAdded.current = true;
        console.log(`✅ Added fort markers for ${portData.length} ports`);
      } catch (error) {
        console.error("Error adding port markers:", error);
      }
    };

    if (!maplibreMap.isStyleLoaded()) {
      maplibreMap.once("styledata", setupMarkers);
    } else {
      setupMarkers();
    }

    return () => {};
  }, [map, ports, onPortClick, portColors]);

  return null;
}
