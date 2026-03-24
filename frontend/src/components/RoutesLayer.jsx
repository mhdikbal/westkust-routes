import { useEffect } from "react";
import { useMap } from "react-map-gl/maplibre";

export default function RoutesLayer({ voyages, ports, hoveredRoute, onRouteClick, onRouteHover }) {
  const { current: map } = useMap();

  useEffect(() => {
    if (!map || !map.getMap) return;

    const maplibreMap = map.getMap();
    if (!maplibreMap) return;

    // Wait for map to load
    const addLayersWhenReady = () => {
      if (!maplibreMap.isStyleLoaded()) {
        maplibreMap.once("styledata", addLayers);
      } else {
        addLayers();
      }
    };

    function addLayers() {
      try {
        // Remove existing layers and sources if they exist
        if (maplibreMap.getLayer("routes-layer")) {
          maplibreMap.removeLayer("routes-layer");
        }
        if (maplibreMap.getSource("routes-source")) {
          maplibreMap.removeSource("routes-source");
        }
        if (maplibreMap.getLayer("ports-layer")) {
          maplibreMap.removeLayer("ports-layer");
        }
        if (maplibreMap.getLayer("port-labels-layer")) {
          maplibreMap.removeLayer("port-labels-layer");
        }
        if (maplibreMap.getSource("ports-source")) {
          maplibreMap.removeSource("ports-source");
        }

        // Create routes GeoJSON
        const routesFeatures = voyages.map((voyage) => {
          const origin = ports[voyage.asal];
          const destination = ports["Batavia"];

          if (!origin || !destination) return null;

          return {
            type: "Feature",
            properties: {
              id: voyage.id,
              warna_asal: voyage.warna_asal,
            },
            geometry: {
              type: "LineString",
              coordinates: [origin, destination],
            },
          };
        }).filter((f) => f !== null);

        const routesGeoJSON = {
          type: "FeatureCollection",
          features: routesFeatures,
        };

        // Create ports GeoJSON
        const portsFeatures = Object.entries(ports).map(([name, coords]) => ({
          type: "Feature",
          properties: { name },
          geometry: {
            type: "Point",
            coordinates: coords,
          },
        }));

        const portsGeoJSON = {
          type: "FeatureCollection",
          features: portsFeatures,
        };

        // Add routes source and layer
        maplibreMap.addSource("routes-source", {
          type: "geojson",
          data: routesGeoJSON,
        });

        maplibreMap.addLayer({
          id: "routes-layer",
          type: "line",
          source: "routes-source",
          paint: {
            "line-color": ["get", "warna_asal"],
            "line-width": 5,
            "line-opacity": 0.8,
          },
        });

        // Add ports source and layers
        maplibreMap.addSource("ports-source", {
          type: "geojson",
          data: portsGeoJSON,
        });

        maplibreMap.addLayer({
          id: "ports-layer",
          type: "circle",
          source: "ports-source",
          paint: {
            "circle-radius": 12,
            "circle-color": "#B85D19",
            "circle-stroke-width": 4,
            "circle-stroke-color": "#FFFFFF",
          },
        });

        maplibreMap.addLayer({
          id: "port-labels-layer",
          type: "symbol",
          source: "ports-source",
          layout: {
            "text-field": ["get", "name"],
            "text-size": 12,
            "text-offset": [0, 1.5],
            "text-anchor": "top",
          },
          paint: {
            "text-color": "#1A2421",
            "text-halo-color": "#FFFFFF",
            "text-halo-width": 2,
          },
        });

        // Add click handler for routes
        maplibreMap.on("click", "routes-layer", (e) => {
          if (e.features.length > 0) {
            const featureId = e.features[0].properties.id;
            onRouteClick(featureId);
          }
        });

        // Add hover handlers
        maplibreMap.on("mouseenter", "routes-layer", (e) => {
          maplibreMap.getCanvas().style.cursor = "pointer";
          if (e.features.length > 0) {
            onRouteHover(e.features[0].properties.id);
          }
        });

        maplibreMap.on("mouseleave", "routes-layer", () => {
          maplibreMap.getCanvas().style.cursor = "grab";
          onRouteHover(null);
        });

        console.log(`✅ Added ${routesFeatures.length} routes to map`);
      } catch (error) {
        console.error("Error adding layers:", error);
      }
    }

    addLayersWhenReady();

    return () => {
      // Cleanup on unmount
      if (maplibreMap && maplibreMap.getStyle()) {
        try {
          if (maplibreMap.getLayer("routes-layer")) {
            maplibreMap.off("click", "routes-layer");
            maplibreMap.off("mouseenter", "routes-layer");
            maplibreMap.off("mouseleave", "routes-layer");
            maplibreMap.removeLayer("routes-layer");
          }
          if (maplibreMap.getSource("routes-source")) {
            maplibreMap.removeSource("routes-source");
          }
          if (maplibreMap.getLayer("ports-layer")) {
            maplibreMap.removeLayer("ports-layer");
          }
          if (maplibreMap.getLayer("port-labels-layer")) {
            maplibreMap.removeLayer("port-labels-layer");
          }
          if (maplibreMap.getSource("ports-source")) {
            maplibreMap.removeSource("ports-source");
          }
        } catch (error) {
          // Ignore cleanup errors
        }
      }
    };
  }, [map, voyages, hoveredRoute, onRouteClick, onRouteHover, ports]);

  // Update route styles when hoveredRoute changes
  useEffect(() => {
    if (!map || !map.getMap) return;
    const maplibreMap = map.getMap();
    if (!maplibreMap || !maplibreMap.getLayer("routes-layer")) return;

    try {
      maplibreMap.setPaintProperty("routes-layer", "line-width", [
        "case",
        ["==", ["get", "id"], hoveredRoute || ""],
        8,
        5,
      ]);

      maplibreMap.setPaintProperty("routes-layer", "line-opacity", [
        "case",
        ["==", ["get", "id"], hoveredRoute || ""],
        1,
        0.6,
      ]);
    } catch (error) {
      // Ignore style update errors
    }
  }, [map, hoveredRoute]);

  return null;
}

