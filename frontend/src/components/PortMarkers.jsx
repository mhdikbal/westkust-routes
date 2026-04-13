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

// Function to generate Star Fort (Benteng Bintang) GeoJSON
function createFortGeometry(name, coords, color) {
  const [lng, lat] = coords;
  
  // Ratios for rendering the star trace
  const rOuter = 0.015; // Outer bastion radius
  const rInner = 0.006;  // Inner curtain wall radius
  const rCore = 0.004;   // Central keep radius
  
  // Height configurations (in meters)
  const baseHeight = 0;
  const bastionHeight = 35; 
  const coreHeight = 85; 

  const features = [];

  // Generate a Star Star Polygon (4 points Bastion)
  const starCoords = [];
  const numPoints = 4;
  for (let i = 0; i <= numPoints * 2; i++) {
    const angle = (i * Math.PI) / numPoints;
    // Alternate between outer bastion and inner indent
    const radius = i % 2 === 0 ? rInner : rOuter;
    // We adjust by PI/4 so the bastions point diagonally or cardinally
    const adjustedAngle = angle + (Math.PI / 4);
    starCoords.push([
      lng + radius * Math.cos(adjustedAngle),
      lat + radius * Math.sin(adjustedAngle)
    ]);
  }
  
  features.push({
    type: "Feature",
    properties: {
      name,
      color: color,
      height: bastionHeight,
      base_height: baseHeight,
      isCore: false
    },
    geometry: {
      type: "Polygon",
      coordinates: [starCoords]
    }
  });

  // Generate Central Keep (Octagon core inside the star)
  const coreCoords = [];
  for (let i = 0; i <= 8; i++) {
    const angle = (i * Math.PI) / 4;
    coreCoords.push([
      lng + rCore * Math.cos(angle),
      lat + rCore * Math.sin(angle)
    ]);
  }

  // To give it a gleaming crown, we make the core slightly brighter or distinct
  features.push({
    type: "Feature",
    properties: {
      name,
      // A brighter tint of the main color for the inner dome
      color: "#FFFFFF",
      height: coreHeight,
      base_height: bastionHeight, // Sits on top of the bastion!
      isCore: true
    },
    geometry: {
      type: "Polygon",
      coordinates: [coreCoords]
    }
  });

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
          const glowLayerId = `port-3d-glow-lyr-${name.replace(/\\s/g, "-").toLowerCase()}`;
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

          // Add a holographic glowing base under the fort
          if (!maplibreMap.getLayer(glowLayerId)) {
            maplibreMap.addLayer({
              id: glowLayerId,
              type: "circle",
              source: sourceId,
              filter: ["==", ["get", "isCore"], true], // Target only the core point wrapper
              paint: {
                "circle-color": color,
                "circle-radius": 35,
                "circle-blur": 1.5,
                "circle-opacity": 0.5,
                "circle-pitch-alignment": "map" // Lays flat on the ground
              }
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
                "text-size": 13,
                "text-offset": [0, -3], // Lift it high above the structure
                "text-anchor": "bottom",
                "text-allow-overlap": false
              },
              paint: {
                "text-color": "#FFFFFF",
                "text-halo-color": "rgba(0,0,0,0.8)", 
                "text-halo-width": 2,
              },
              filter: ["==", ["get", "isCore"], true] // Only place label on the Core Geometry
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
