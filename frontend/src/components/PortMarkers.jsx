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

// Function to generate a procedural 3D fort GeoJSON with base and towers
function createFortGeometry(name, coords, color) {
  const [lng, lat] = coords;
  // Radius roughly translates to size. 0.05 degrees is huge, 0.005 is solid.
  const rBase = 0.02; // Base size
  const rTower = 0.006; // Tower size
  
  // Height configurations (in meters)
  const baseHeight = 0;
  const topBaseHeight = 40;
  
  const towerBaseHeight = 0;
  const topTowerHeight = 80;

  const features = [];

  // Helper to create a Box polygon
  const createBox = (cx, cy, r, h, bh, boxColor) => ({
    type: "Feature",
    properties: {
      name,
      color: boxColor,
      height: h,
      base_height: bh,
    },
    geometry: {
      type: "Polygon",
      coordinates: [[
        [cx - r, cy - r],
        [cx + r, cy - r],
        [cx + r, cy + r],
        [cx - r, cy + r],
        [cx - r, cy - r]
      ]]
    }
  });

  // 1. Central Base (The Fort Wall/Base structure)
  features.push(createBox(lng, lat, rBase, topBaseHeight, baseHeight, color));

  // 2. The four corner Watchtowers (Menara pengawas)
  // Top-Left
  features.push(createBox(lng - rBase, lat + rBase, rTower, topTowerHeight, towerBaseHeight, "#E0E0E0"));
  // Top-Right
  features.push(createBox(lng + rBase, lat + rBase, rTower, topTowerHeight, towerBaseHeight, "#E0E0E0"));
  // Bottom-Left
  features.push(createBox(lng - rBase, lat - rBase, rTower, topTowerHeight, towerBaseHeight, "#E0E0E0"));
  // Bottom-Right
  features.push(createBox(lng + rBase, lat - rBase, rTower, topTowerHeight, towerBaseHeight, "#E0E0E0"));

  return {
    type: "FeatureCollection",
    features
  };
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
        
        portEntries.forEach(([name, coords]) => {
          const color = portColors?.[name] || "#B85D19";
          const portType = PORT_TYPE_MAP[name] || "departure";
          const displayName = name === "Batavia" ? "Sunda Kelapa (Batavia)" : name;
          
          const sourceId = `port-3d-src-${name.replace(/\\s/g, "-").toLowerCase()}`;
          const extrusionLayerId = `port-3d-extrusion-lyr-${name.replace(/\\s/g, "-").toLowerCase()}`;
          const textLayerId = `port-3d-text-lyr-${name.replace(/\\s/g, "-").toLowerCase()}`;

          // Create the 3D fortress block geometries
          const geojsonData = createFortGeometry(name, coords, color);

          if (!maplibreMap.getSource(sourceId)) {
            maplibreMap.addSource(sourceId, {
              type: "geojson",
              data: geojsonData
            });
          }

          // Add the 3D Fill Extrusion Layer
          if (!maplibreMap.getLayer(extrusionLayerId)) {
            maplibreMap.addLayer({
              id: extrusionLayerId,
              type: "fill-extrusion",
              source: sourceId,
              paint: {
                // Get the fill-extrusion-color from the source 'color' property.
                "fill-extrusion-color": ["get", "color"],
                // Get fill-extrusion-height from the source 'height' property.
                "fill-extrusion-height": ["get", "height"],
                // Get fill-extrusion-base from the source 'base_height' property.
                "fill-extrusion-base": ["get", "base_height"],
                // Make extrusions slightly opaque
                "fill-extrusion-opacity": 0.9,
                // Add ambient Light interaction
                "fill-extrusion-vertical-gradient": true
              }
            });

            // Make the 3D object clickable
            maplibreMap.on("click", extrusionLayerId, (e) => {
              if (e.features && e.features.length > 0) {
                const portName = e.features[0].properties.name;
                onPortClick(portName);
                e.originalEvent.stopPropagation();
              }
            });

            maplibreMap.on("mouseenter", extrusionLayerId, () => {
              maplibreMap.getCanvas().style.cursor = "pointer";
            });

            maplibreMap.on("mouseleave", extrusionLayerId, () => {
              maplibreMap.getCanvas().style.cursor = "";
            });
          }

          // Add a floating text label layer hovering above the fortress
          if (!maplibreMap.getLayer(textLayerId)) {
            // We just need one label per port. We can use a separate feature or just reference the center point.
            // Maplibre handles labels on polygons by placing it at the centroid!
            maplibreMap.addLayer({
              id: textLayerId,
              type: "symbol",
              source: sourceId,
              layout: {
                "text-field": displayName,
                "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
                "text-size": 14,
                "text-offset": [0, -3], // Lift it high above the structure
                "text-anchor": "bottom",
                "text-allow-overlap": false
              },
              paint: {
                "text-color": "#FFFFFF",
                "text-halo-color": color, 
                "text-halo-width": 2,
              },
              filter: ["==", ["get", "height"], 40] // Only place label on the Base Geometry feature to avoid duplicate labels
            });
          }
        });

        markersAdded.current = true;
        console.log(`✅ Added 3D Fortress blocks for ${portEntries.length} ports`);
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
