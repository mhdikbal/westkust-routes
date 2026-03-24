import { useState, useEffect, useRef, useCallback } from "react";
import Map, { Popup, useMap } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import Sidebar from "@/components/Sidebar";
import TimelineSlider from "@/components/TimelineSlider";
import TimelineAnimationControl from "@/components/TimelineAnimationControl";
import WelcomeModal from "@/components/WelcomeModal";
import VoyageDetailModal from "@/components/VoyageDetailModal";
import PortMarkers from "@/components/PortMarkers";
import PortShipListModal from "@/components/PortShipListModal";
import HistoricalContextModal from "@/components/HistoricalContextModal";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PORTS = {
  Padang: [100.35659, -0.96543],
  "Pulau Cingkuak": [100.55977, -1.35303],
  "Air Haji": [100.86801, -1.94012],
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
  const [selectedPort, setSelectedPort] = useState(null);
  const [portShips, setPortShips] = useState([]);
  const [historicalPort, setHistoricalPort] = useState(null);
  const [showAnimation, setShowAnimation] = useState(false);

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

  const handlePortClick = (portName) => {
    // Get all ships from this port
    const shipsFromPort = allVoyages.filter((v) => {
      if (portName === "Batavia") {
        return v.tujuan.includes("Batavia");
      }
      return v.asal === portName;
    });
    
    setSelectedPort(portName);
    setPortShips(shipsFromPort);
  };

  const handleViewShipDetail = (ship) => {
    setSelectedPort(null); // Close port list modal
    setSelectedVoyage(ship); // Open ship detail modal
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
          longitude: 102,
          latitude: -3,
          zoom: 5.2,
        }}
        style={{ width: "100%", height: "100%" }}
        mapStyle="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
        attributionControl={false}
      >
        <PortMarkers ports={PORTS} onPortClick={handlePortClick} />
      </Map>

      <PortShipListModal
        port={selectedPort}
        ships={portShips}
        open={!!selectedPort}
        onClose={() => setSelectedPort(null)}
        onViewDetail={handleViewShipDetail}
        onViewHistory={(port) => setHistoricalPort(port)}
      />

      <HistoricalContextModal
        port={historicalPort}
        open={!!historicalPort}
        onClose={() => setHistoricalPort(null)}
      />

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
        onToggleAnimation={() => setShowAnimation(!showAnimation)}
        showAnimation={showAnimation}
      />

      {showAnimation && (
        <TimelineAnimationControl
          yearRange={yearRange}
          setYearRange={setYearRange}
          minYear={1700}
          maxYear={1789}
        />
      )}
    </div>
  );
}