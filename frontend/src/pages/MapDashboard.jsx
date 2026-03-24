import { useState, useEffect } from "react";
import Map, { Source, Layer, Popup } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import Sidebar from "@/components/Sidebar";
import TimelineSlider from "@/components/TimelineSlider";
import WelcomeModal from "@/components/WelcomeModal";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PORTS = {
  Padang: [-100.3543, -0.9471],
  "Pulau Cingkuak": [-100.1667, -0.7833],
  "Air Haji": [-100.4167, -0.5833],
  Batavia: [106.8456, -6.2088],
};

export default function MapDashboard() {
  const [voyages, setVoyages] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedPorts, setSelectedPorts] = useState(["Padang", "Pulau Cingkuak", "Air Haji"]);
  const [yearRange, setYearRange] = useState([1700, 1789]);
  const [selectedVoyage, setSelectedVoyage] = useState(null);
  const [showWelcome, setShowWelcome] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [hoveredRoute, setHoveredRoute] = useState(null);

  useEffect(() => {
    fetchVoyages();
    fetchStats();
  }, [yearRange, selectedPorts]);

  const fetchVoyages = async () => {
    try {
      const params = {
        year_from: yearRange[0],
        year_to: yearRange[1],
      };
      const response = await axios.get(`${API}/voyages`, { params });
      const filtered = response.data.filter((v) =>
        selectedPorts.includes(v.asal)
      );
      setVoyages(filtered);
    } catch (error) {
      console.error("Error fetching voyages:", error);
    }
  };

  const fetchStats = async () => {
    try {
      const params = {
        year_from: yearRange[0],
        year_to: yearRange[1],
      };
      const response = await axios.get(`${API}/voyages/stats`, { params });
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const createRouteGeoJSON = () => {
    const features = voyages.map((voyage, index) => {
      const origin = PORTS[voyage.asal];
      const destination = PORTS["Batavia"];

      if (!origin || !destination) return null;

      // Add slight curve to routes to prevent overlap
      const midLon = (origin[0] + destination[0]) / 2;
      const midLat = (origin[1] + destination[1]) / 2;
      const offset = (index % 3 - 1) * 0.5; // Small offset for visual separation
      
      const curvedMidPoint = [midLon + offset, midLat + offset * 0.3];

      return {
        type: "Feature",
        properties: {
          id: voyage.id,
          nama_kapal: voyage.nama_kapal,
          tahun: voyage.tahun,
          total_gulden_nl: voyage.total_gulden_nl,
          produk_utama: voyage.produk_utama,
          warna_asal: voyage.warna_asal,
        },
        geometry: {
          type: "LineString",
          coordinates: [origin, curvedMidPoint, destination],
        },
      };
    });

    return {
      type: "FeatureCollection",
      features: features.filter((f) => f !== null),
    };
  };

  const createPortsGeoJSON = () => {
    const features = Object.entries(PORTS)
      .filter(([name]) => selectedPorts.includes(name) || name === "Batavia")
      .map(([name, coords]) => ({
        type: "Feature",
        properties: { name },
        geometry: {
          type: "Point",
          coordinates: coords,
        },
      }));

    return {
      type: "FeatureCollection",
      features,
    };
  };

  const routeLayer = {
    id: "routes",
    type: "line",
    paint: {
      "line-color": ["get", "warna_asal"],
      "line-width": [
        "case",
        ["==", ["get", "id"], hoveredRoute || ""],
        6,
        4
      ],
      "line-opacity": [
        "case",
        ["==", ["get", "id"], hoveredRoute || ""],
        1.0,
        0.75
      ],
    },
  };

  const portLayer = {
    id: "ports",
    type: "circle",
    paint: {
      "circle-radius": 10,
      "circle-color": "#B85D19",
      "circle-stroke-width": 3,
      "circle-stroke-color": "#FFFFFF",
      "circle-opacity": 0.9,
    },
  };

  const handleVoyageClick = (voyage) => {
    setSelectedVoyage(voyage);
    setHoveredRoute(voyage.id);
  };

  const portLabelLayer = {
    id: "port-labels",
    type: "symbol",
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
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-[#FDFBF7]">
      <WelcomeModal open={showWelcome} onClose={() => setShowWelcome(false)} />

      <Map
        mapLib={import("maplibre-gl")}
        initialViewState={{
          longitude: 103,
          latitude: -3.2,
          zoom: 5.5,
        }}
        style={{ width: "100%", height: "100%" }}
        mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
      >
        <Source id="routes-source" type="geojson" data={createRouteGeoJSON()}>
          <Layer {...routeLayer} />
        </Source>

        <Source id="ports-source" type="geojson" data={createPortsGeoJSON()}>
          <Layer {...portLayer} />
          <Layer {...portLabelLayer} />
        </Source>

        {selectedVoyage && (
          <Popup
            longitude={PORTS[selectedVoyage.asal][0]}
            latitude={PORTS[selectedVoyage.asal][1]}
            onClose={() => setSelectedVoyage(null)}
            closeButton={true}
            closeOnClick={false}
            className="voyage-popup"
          >
            <div className="p-4 min-w-[280px]">
              <h3 className="font-serif text-lg font-semibold text-[#1A2421] mb-2">
                {selectedVoyage.nama_kapal}
              </h3>
              <div className="space-y-1 text-sm text-[#5C6A66]">
                <p>
                  <span className="font-medium">Tahun:</span> {selectedVoyage.tahun}
                </p>
                <p>
                  <span className="font-medium">Nilai Cargo:</span>{" "}
                  {selectedVoyage.total_gulden_nl.toLocaleString()} Gulden
                </p>
                <p>
                  <span className="font-medium">Produk Utama:</span>{" "}
                  {selectedVoyage.produk_utama}
                </p>
                <p>
                  <span className="font-medium">Rute:</span> {selectedVoyage.asal} →
                  Batavia
                </p>
              </div>
            </div>
          </Popup>
        )}
      </Map>

      <Sidebar
        voyages={voyages}
        stats={stats}
        selectedPorts={selectedPorts}
        setSelectedPorts={setSelectedPorts}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        onVoyageClick={handleVoyageClick}
      />

      <TimelineSlider
        yearRange={yearRange}
        setYearRange={setYearRange}
        minYear={1700}
        maxYear={1789}
      />
    </div>
  );
}