import { useEffect, useRef } from "react";
import { useMap } from "react-map-gl/maplibre";

export default function PortMarkers({ ports, onPortClick }) {
  const { current: map } = useMap();
  const markersAdded = useRef(false);

  useEffect(() => {
    if (!map || !map.getMap || markersAdded.current) return;
    
    const maplibreMap = map.getMap();
    if (!maplibreMap) return;

    const setupMarkers = () => {
      try {
        const portFeatures = Object.entries(ports).map(([name, coords]) => ({
          type: "Feature",
          properties: { 
            name,
            displayName: name === "Batavia" ? "Sunda Kelapa (Batavia)" : name
          },
          geometry: {
            type: "Point",
            coordinates: coords,
          },
        }));

        const portsGeoJSON = {
          type: "FeatureCollection",
          features: portFeatures,
        };

        // Create fort SVG icon
        const fortSvg = `
          <svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <circle cx="24" cy="24" r="20" fill="#B85D19" stroke="#FFFFFF" stroke-width="3"/>
            <g transform="translate(24, 24)">
              <rect x="-8" y="-6" width="16" height="12" fill="#FFFFFF"/>
              <rect x="-10" y="-10" width="4" height="4" fill="#FFFFFF"/>
              <rect x="6" y="-10" width="4" height="4" fill="#FFFFFF"/>
              <rect x="-2" y="-2" width="4" height="6" fill="#B85D19"/>
            </g>
          </svg>
        `;

        const img = new Image(48, 48);
        img.onload = () => {
          if (!maplibreMap.hasImage("fort-icon")) {
            maplibreMap.addImage("fort-icon", img);
          }
          
          if (!maplibreMap.getSource("port-markers-source")) {
            maplibreMap.addSource("port-markers-source", {
               type: "geojson",
               data: portsGeoJSON,
            });
          }

          if (!maplibreMap.getLayer("port-markers")) {
            maplibreMap.addLayer({
              id: "port-markers",
              type: "symbol",
              source: "port-markers-source",
              layout: {
                "icon-image": "fort-icon",
                "icon-size": 1,
                "icon-allow-overlap": true,
                "text-field": ["get", "displayName"],
                "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
                "text-size": 14,
                "text-offset": [0, 2.5],
                "text-anchor": "top",
              },
              paint: {
                "text-color": "#1A2421",
                "text-halo-color": "#FFFFFF",
                "text-halo-width": 2,
              },
            });
          }

          // Add click handler with proper event attachment
          const clickHandler = (e) => {
            if (e.features && e.features.length > 0) {
              const portName = e.features[0].properties.name;
              console.log("Fort clicked:", portName);
              onPortClick(portName);
              e.originalEvent.stopPropagation();
            }
          };

          const mouseEnterHandler = () => {
            maplibreMap.getCanvas().style.cursor = "pointer";
          };

          const mouseLeaveHandler = () => {
            maplibreMap.getCanvas().style.cursor = "";
          };

          maplibreMap.on("click", "port-markers", clickHandler);
          maplibreMap.on("mouseenter", "port-markers", mouseEnterHandler);
          maplibreMap.on("mouseleave", "port-markers", mouseLeaveHandler);

          console.log("✅ Fort click handlers attached");
          
          markersAdded.current = true;
          console.log("✅ Added fort markers for", Object.keys(ports).length, "ports");
        };
        
        img.onerror = (e) => {
          console.error("Failed to load fort icon:", e);
        };
        
        img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(fortSvg);
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
  }, [map, ports, onPortClick]);

  return null;
}
