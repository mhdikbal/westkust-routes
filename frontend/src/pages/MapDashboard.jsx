import { useState, useEffect, useCallback, useRef } from "react";
import Map from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import Sidebar from "@/components/Sidebar";
import TimelineSlider from "@/components/TimelineSlider";
import TimelineAnimationControl from "@/components/TimelineAnimationControl";
import WelcomeModal from "@/components/WelcomeModal";
import VoyageDetailModal from "@/components/VoyageDetailModal";
import PortMarkers from "@/components/PortMarkers";
import PortShipListModal from "@/components/PortShipListModal";
import HistoricalContextModal from "@/components/HistoricalContextModal";
import RoutesLayer from "@/components/RoutesLayer";
import RouteLegend from "@/components/RouteLegend";
import NetworkGraph from "@/components/NetworkGraph";
import TemporalHeatmap from "@/components/TemporalHeatmap";
import PortComparison from "@/components/PortComparison";
import CommoditySankey from "@/components/CommoditySankey";
import StorytellingOverlay from "@/components/StorytellingOverlay";
import { HISTORIC_TOURS } from "@/data/tours";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

// All 9 ports with coordinates — must match FORTS_META in seed_data.py
const PORTS = {
  Barus:           [98.3993198,  2.0144566],
  "Air Bangis":    [99.3755554,  0.1974875],
  Padang:          [100.3538894, -0.9655545],
  "Pulau Cingkuak":[100.5599951, -1.3528370],
  "Air Haji":      [100.8669821, -1.9339388],
  Jambi:           [104.1757178, -1.0984482],
  Palembang:       [104.7801890, -3.0029119],
  Lampung:         [105.2803866, -5.3578004],
  Batavia:         [106.8165121, -6.1165019],
};

// Port colors matching seed_data.py
const PORT_COLORS = {
  Barus: "#16a085",
  "Air Bangis": "#2980b9",
  Padang: "#c0392b",
  "Pulau Cingkuak": "#e67e22",
  "Air Haji": "#27ae60",
  Jambi: "#d35400",
  Palembang: "#8e44ad",
  Lampung: "#7f8c8d",
  Batavia: "#2c3e50",
};

export default function MapDashboard() {
  const [allVoyages, setAllVoyages] = useState([]);
  const [voyages, setVoyages] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedPorts, setSelectedPorts] = useState([
    "Padang", "Pulau Cingkuak", "Air Haji", "Barus", "Air Bangis",
  ]);
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
  const [directionFilter, setDirectionFilter] = useState("all"); // "all" | "outbound" | "inbound"

  const [showNetworkGraph, setShowNetworkGraph] = useState(false);
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [showPortComparison, setShowPortComparison] = useState(false);
  const [showSankey, setShowSankey] = useState(false);

  // Storytelling Tour States
  const mapRef = useRef(null);
  const [activeTour, setActiveTour] = useState(null);
  const [tourStepIndex, setTourStepIndex] = useState(0);

  // Fetch data on filter changes
  useEffect(() => {
    fetchVoyages();
    fetchRoutes();
    fetchStats();
  }, [yearRange, directionFilter]);

  const fetchVoyages = async () => {
    try {
      const params = {
        year_from: yearRange[0],
        year_to: yearRange[1],
        limit: 5000,
      };
      if (directionFilter !== "all") {
        params.direction = directionFilter;
      }
      const response = await axios.get(`${API}/voyages/`, { params });
      setAllVoyages(response.data);

      let filtered = response.data;
      if (selectedPorts.length > 0) {
        filtered = filtered.filter((v) =>
          selectedPorts.includes(v.origin_name_raw) ||
          selectedPorts.includes(v.destination_name_raw)
        );
      }
      if (selectedProducts.length > 0) {
        filtered = filtered.filter((v) =>
          selectedProducts.includes(v.main_product)
        );
      }
      setVoyages(filtered);
    } catch (error) {
      console.error("Error fetching voyages:", error);
    }
  };

  const fetchRoutes = async () => {
    try {
      const params = {
        year_from: yearRange[0],
        year_to: yearRange[1],
      };
      if (directionFilter !== "all") {
        params.direction = directionFilter;
      }
      const response = await axios.get(`${API}/voyages/routes`, { params });
      setRoutes(response.data);
    } catch (error) {
      console.error("Error fetching routes:", error);
    }
  };

  const fetchStats = async () => {
    try {
      const params = {
        year_from: yearRange[0],
        year_to: yearRange[1],
      };
      if (directionFilter !== "all") {
        params.direction = directionFilter;
      }
      const response = await axios.get(`${API}/voyages/stats`, { params });
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  // Re-filter locally when ports/products change (no API call needed)
  useEffect(() => {
    let filtered = allVoyages;
    if (selectedPorts.length > 0) {
      filtered = filtered.filter((v) =>
        selectedPorts.includes(v.origin_name_raw) ||
        selectedPorts.includes(v.destination_name_raw)
      );
    }
    if (selectedProducts.length > 0) {
      filtered = filtered.filter((v) =>
        selectedProducts.includes(v.main_product)
      );
    }
    setVoyages(filtered);
  }, [selectedPorts, selectedProducts, allVoyages]);

  const handleVoyageClick = (voyage) => {
    setSelectedVoyage(voyage);
    setHoveredRoute(voyage.id);
  };

  const handlePortClick = (portName) => {
    setSelectedPort(portName);
  };

  useEffect(() => {
    if (selectedPort) {
      const shipsFromPort = allVoyages.filter((v) => {
        return v.origin_name_raw === selectedPort || v.destination_name_raw === selectedPort;
      });
      setPortShips(shipsFromPort);
    } else {
      setPortShips([]);
    }
  }, [selectedPort, allVoyages]);

  const handleViewShipDetail = (ship) => {
    setSelectedPort(null);
    setSelectedVoyage(ship);
  };

  const handleRouteClick = useCallback((routeId) => {
    const voyage = voyages.find((v) => v.id === routeId);
    if (voyage) {
      handleVoyageClick(voyage);
    }
  }, [voyages]);

  const handleRouteHover = useCallback((routeId) => {
    setHoveredRoute(routeId);
  }, []);

  const handleStartTour = (tourId) => {
    const tour = HISTORIC_TOURS.find((t) => t.id === tourId);
    if (tour && tour.steps.length > 0) {
      setActiveTour(tour);
      setTourStepIndex(0);
      executeTourStep(tour.steps[0]);
    }
  };

  const executeTourStep = (step) => {
    if (mapRef.current) {
      mapRef.current.flyTo({
        center: [step.camera.longitude, step.camera.latitude],
        zoom: step.camera.zoom,
        pitch: step.camera.pitch || 0,
        bearing: step.camera.bearing || 0,
        duration: 3500,
        essential: true
      });
    }
    setYearRange(step.yearSpan); // Sync the timeline with the story
  };

  const handleNextTourStep = () => {
    if (activeTour && tourStepIndex < activeTour.steps.length - 1) {
      const nextIdx = tourStepIndex + 1;
      setTourStepIndex(nextIdx);
      executeTourStep(activeTour.steps[nextIdx]);
    }
  };

  const handlePrevTourStep = () => {
    if (activeTour && tourStepIndex > 0) {
      const prevIdx = tourStepIndex - 1;
      setTourStepIndex(prevIdx);
      executeTourStep(activeTour.steps[prevIdx]);
    }
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-[#0a0e1a]">
      <WelcomeModal open={showWelcome} onClose={() => setShowWelcome(false)} />

      <Map
        ref={mapRef}
        mapLib={import("maplibre-gl")}
        initialViewState={{
          longitude: 103,
          latitude: -2.5,
          zoom: 5.5,
        }}
        style={{ width: "100%", height: "100%" }}
        mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
        attributionControl={false}
      >
        <RoutesLayer
          routes={routes}
          ports={PORTS}
          portColors={PORT_COLORS}
          hoveredRoute={hoveredRoute}
          directionFilter={directionFilter}
        />
        <PortMarkers ports={PORTS} onPortClick={handlePortClick} portColors={PORT_COLORS} />
      </Map>

      {/* Direction Legend + Toggle */}
      <RouteLegend
        directionFilter={directionFilter}
        setDirectionFilter={setDirectionFilter}
        stats={stats}
      />

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

      {/* Analytics Overlays */}
      <NetworkGraph
        open={showNetworkGraph}
        onClose={() => setShowNetworkGraph(false)}
      />
      <TemporalHeatmap
        open={showHeatmap}
        onClose={() => setShowHeatmap(false)}
      />
      <PortComparison
        open={showPortComparison}
        onClose={() => setShowPortComparison(false)}
      />
      <CommoditySankey
        open={showSankey}
        onClose={() => setShowSankey(false)}
      />

      <StorytellingOverlay
        tour={activeTour}
        stepIndex={tourStepIndex}
        onNext={handleNextTourStep}
        onPrev={handlePrevTourStep}
        onClose={() => setActiveTour(null)}
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
        onOpenNetworkGraph={() => setShowNetworkGraph(true)}
        onOpenHeatmap={() => setShowHeatmap(true)}
        onOpenPortComparison={() => setShowPortComparison(true)}
        onOpenSankey={() => setShowSankey(true)}
        onStartTour={handleStartTour}
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