import { useState, useEffect, useRef, useCallback } from "react";
import Map, { Popup, useMap } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import Sidebar from "@/components/Sidebar";
import TimelineSlider from "@/components/TimelineSlider";
import WelcomeModal from "@/components/WelcomeModal";
import VoyageDetailModal from "@/components/VoyageDetailModal";
import RoutesLayer from "@/components/RoutesLayer";
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
  const [allVoyages, setAllVoyages] = useState([]);
  const [voyages, setVoyages] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedPorts, setSelectedPorts] = useState(["Padang", "Pulau Cingkuak", "Air Haji"]);
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [yearRange, setYearRange] = useState([1700, 1789]);
  const [selectedVoyage, setSelectedVoyage] = useState(null);
  const [showWelcome, setShowWelcome] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [hoveredRoute, setHoveredRoute] = useState(null);

  useEffect(() => {
    fetchVoyages();
    fetchStats();
  }, [yearRange, selectedPorts, selectedProducts]);

  const fetchVoyages = async () => {
    try {
      const params = {
        year_from: yearRange[0],
        year_to: yearRange[1],
      };
      const response = await axios.get(`${API}/voyages`, { params });
      setAllVoyages(response.data);
      
      let filtered = response.data.filter((v) =>
        selectedPorts.includes(v.asal)
      );

      if (selectedProducts.length > 0) {
        filtered = filtered.filter((v) =>
          selectedProducts.includes(v.produk_utama)
        );
      }

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

  const handleVoyageClick = (voyage) => {
    setSelectedVoyage(voyage);
    setHoveredRoute(voyage.id);
  };

  const handleRouteClick = (routeId) => {
    const voyage = voyages.find((v) => v.id === routeId);
    if (voyage) {
      handleVoyageClick(voyage);
    }
  };

  const handleRouteHover = (routeId) => {
    setHoveredRoute(routeId);
  };

  // Get map bounds to fit the route
  const getRouteBounds = (voyage) => {
    if (!voyage) return null;
    const origin = PORTS[voyage.asal];
    const destination = PORTS["Batavia"];
    
    return [
      [Math.min(origin[0], destination[0]) - 2, Math.min(origin[1], destination[1]) - 1],
      [Math.max(origin[0], destination[0]) + 2, Math.max(origin[1], destination[1]) + 1]
    ];
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-[#FDFBF7]">
      <WelcomeModal open={showWelcome} onClose={() => setShowWelcome(false)} />

      <Map
        mapLib={import("maplibre-gl")}
        initialViewState={{
          longitude: 103.5,
          latitude: -2.5,
          zoom: 6,
        }}
        style={{ width: "100%", height: "100%" }}
        mapStyle="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
      >
        <RoutesLayer
          voyages={voyages}
          ports={PORTS}
          hoveredRoute={hoveredRoute}
          onRouteClick={handleRouteClick}
          onRouteHover={handleRouteHover}
        />
      </Map>

      <VoyageDetailModal
        voyage={selectedVoyage}
        open={!!selectedVoyage}
        onClose={() => {
          setSelectedVoyage(null);
          setHoveredRoute(null);
        }}
      />

      <Sidebar
        voyages={voyages}
        allVoyages={allVoyages}
        stats={stats}
        selectedPorts={selectedPorts}
        setSelectedPorts={setSelectedPorts}
        selectedProducts={selectedProducts}
        setSelectedProducts={setSelectedProducts}
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