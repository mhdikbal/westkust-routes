import { useEffect, useRef, useCallback } from "react";
import { useMap } from "react-map-gl/maplibre";

/**
 * RoutesLayer — Animated trade route visualization
 * 
 * Features:
 *  - Bezier curved paths between origin and destination ports
 *  - Color coding: Outbound (#00D4AA teal) vs Inbound (#FF6B6B coral)
 *  - Line width proportional to trade volume
 *  - Animated dash-offset for sailing effect
 *  - Glow effect on routes
 */

// Direction colors
const OUTBOUND_COLOR = "#00D4AA";  // Teal — departing from Sumatera
const INBOUND_COLOR  = "#FF6B6B";  // Coral — arriving at Sumatera
const TRANSIT_COLOR  = "#FFD93D";  // Gold — transit between non-Westkust
const DEFAULT_COLOR  = "#8899AA";

function getDirectionColor(direction) {
  switch (direction) {
    case "outbound": return OUTBOUND_COLOR;
    case "inbound": return INBOUND_COLOR;
    case "transit": return TRANSIT_COLOR;
    default: return DEFAULT_COLOR;
  }
}

/**
 * Generate a curved path (quadratic Bezier approximation) between two points.
 * The curve bows perpendicular to the line, giving a natural "arc" appearance.
 */
function generateBezierCurve(start, end, curveStrength = 0.3, numPoints = 40) {
  const [x1, y1] = start;
  const [x2, y2] = end;
  
  // Midpoint
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  
  // Perpendicular offset for curve
  const dx = x2 - x1;
  const dy = y2 - y1;
  const dist = Math.sqrt(dx * dx + dy * dy);
  
  // Control point offset perpendicular to the line
  const offsetX = -dy * curveStrength;
  const offsetY = dx * curveStrength;
  
  // Control point
  const cx = mx + offsetX;
  const cy = my + offsetY;
  
  // Generate points along quadratic Bezier: B(t) = (1-t)²P0 + 2(1-t)tP1 + t²P2
  const points = [];
  for (let i = 0; i <= numPoints; i++) {
    const t = i / numPoints;
    const mt = 1 - t;
    const px = mt * mt * x1 + 2 * mt * t * cx + t * t * x2;
    const py = mt * mt * y1 + 2 * mt * t * cy + t * t * y2;
    points.push([px, py]);
  }
  return points;
}


export default function RoutesLayer({ routes, ports, portColors, hoveredRoute, directionFilter }) {
  const { current: map } = useMap();
  const animFrameRef = useRef(null);
  const dashOffsetRef = useRef(0);
  const layersAddedRef = useRef(false);

  // Build GeoJSON features from aggregated routes
  const buildRoutesGeoJSON = useCallback(() => {
    if (!routes || routes.length === 0) return null;

    const features = routes
      .filter(route => {
        // Must have coordinates for both ends
        if (!route.origin_lat || !route.origin_lon || !route.dest_lat || !route.dest_lon) return false;
        return true;
      })
      .map((route, index) => {
        const start = [route.origin_lon, route.origin_lat];
        const end = [route.dest_lon, route.dest_lat];
        
        // Vary curve strength based on index to prevent overlap
        const baseCurve = 0.15;
        const variation = ((index % 7) - 3) * 0.05;
        const curveStrength = baseCurve + variation;
        
        const coordinates = generateBezierCurve(start, end, curveStrength, 40);
        
        // Scale line width by count (log scale)
        const lineWidth = Math.max(1.5, Math.min(8, Math.log2(route.count + 1) * 1.5));
        
        return {
          type: "Feature",
          properties: {
            id: `${route.origin_name}-${route.destination_name}-${route.direction}`,
            direction: route.direction || "unknown",
            color: getDirectionColor(route.direction),
            count: route.count,
            total_value: route.total_value,
            origin_name: route.origin_name,
            destination_name: route.destination_name,
            lineWidth: lineWidth,
          },
          geometry: {
            type: "LineString",
            coordinates: coordinates,
          },
        };
      });

    return {
      type: "FeatureCollection",
      features: features,
    };
  }, [routes]);

  // Main layer setup
  useEffect(() => {
    if (!map || !map.getMap) return;
    const maplibreMap = map.getMap();
    if (!maplibreMap) return;

    const addLayers = () => {
      try {
        // Clean up existing layers
        ["routes-glow", "routes-main", "routes-dash"].forEach(layerId => {
          if (maplibreMap.getLayer(layerId)) maplibreMap.removeLayer(layerId);
        });
        if (maplibreMap.getSource("routes-source")) {
          maplibreMap.removeSource("routes-source");
        }

        const geojson = buildRoutesGeoJSON();
        if (!geojson || geojson.features.length === 0) return;

        maplibreMap.addSource("routes-source", {
          type: "geojson",
          data: geojson,
        });

        // Layer 1: Glow effect (wider, semi-transparent)
        maplibreMap.addLayer({
          id: "routes-glow",
          type: "line",
          source: "routes-source",
          paint: {
            "line-color": ["get", "color"],
            "line-width": ["*", ["get", "lineWidth"], 2.5],
            "line-opacity": 0.15,
            "line-blur": 6,
          },
          layout: {
            "line-cap": "round",
            "line-join": "round",
          },
        });

        // Layer 2: Main solid line
        maplibreMap.addLayer({
          id: "routes-main",
          type: "line",
          source: "routes-source",
          paint: {
            "line-color": ["get", "color"],
            "line-width": ["get", "lineWidth"],
            "line-opacity": 0.7,
          },
          layout: {
            "line-cap": "round",
            "line-join": "round",
          },
        });

        // Layer 3: Animated dash overlay (sailing effect)
        maplibreMap.addLayer({
          id: "routes-dash",
          type: "line",
          source: "routes-source",
          paint: {
            "line-color": "#ffffff",
            "line-width": ["*", ["get", "lineWidth"], 0.4],
            "line-opacity": 0.6,
            "line-dasharray": [0, 4, 3],
          },
          layout: {
            "line-cap": "round",
            "line-join": "round",
          },
        });

        layersAddedRef.current = true;
        console.log(`✅ Routes rendered: ${geojson.features.length} curved paths`);
      } catch (error) {
        console.error("Error adding route layers:", error);
      }
    };

    if (!maplibreMap.isStyleLoaded()) {
      maplibreMap.once("styledata", addLayers);
    } else {
      addLayers();
    }

    return () => {
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
      if (maplibreMap && maplibreMap.getStyle()) {
        try {
          ["routes-glow", "routes-main", "routes-dash"].forEach(layerId => {
            if (maplibreMap.getLayer(layerId)) maplibreMap.removeLayer(layerId);
          });
          if (maplibreMap.getSource("routes-source")) {
            maplibreMap.removeSource("routes-source");
          }
        } catch (e) { /* ignore cleanup errors */ }
      }
      layersAddedRef.current = false;
    };
  }, [map, routes, buildRoutesGeoJSON]);

  // Animate the dash pattern
  useEffect(() => {
    if (!map || !map.getMap || !layersAddedRef.current) return;
    const maplibreMap = map.getMap();

    let step = 0;
    const animate = () => {
      step = (step + 1) % 100;
      
      if (maplibreMap.getLayer("routes-dash")) {
        // Shift dash pattern to create movement effect
        const dashA = (step % 20) / 5;
        const dashB = 4;
        const dashC = 3;
        try {
          maplibreMap.setPaintProperty("routes-dash", "line-dasharray", [dashA, dashB, dashC]);
        } catch (e) { /* ignore */ }
      }
      
      animFrameRef.current = requestAnimationFrame(animate);
    };

    // Start animation with slight delay
    const timer = setTimeout(() => {
      animFrameRef.current = requestAnimationFrame(animate);
    }, 500);

    return () => {
      clearTimeout(timer);
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [map, routes]);

  return null;
}
