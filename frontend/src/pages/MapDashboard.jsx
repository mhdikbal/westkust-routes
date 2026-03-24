import { useState, useEffect, useRef, useCallback } from "react";
import Map, { Popup, useMap } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import Sidebar from "@/components/Sidebar";
import TimelineSlider from "@/components/TimelineSlider";
import WelcomeModal from "@/components/WelcomeModal";
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
        <RoutesLayer
          voyages={voyages}
          ports={PORTS}
          hoveredRoute={hoveredRoute}
          onRouteClick={handleRouteClick}
          onRouteHover={handleRouteHover}
        />

        {selectedVoyage && (
          <Popup
            longitude={PORTS[selectedVoyage.asal][0]}
            latitude={PORTS[selectedVoyage.asal][1]}
            onClose={() => {
              setSelectedVoyage(null);
              setHoveredRoute(null);
            }}
            closeButton={true}
            closeOnClick={false}
            className="voyage-popup"
            maxWidth="400px"
          >
            <div className="p-4 max-w-md">
              <h3 className="font-serif text-xl font-bold text-[#1A2421] mb-3 border-b border-[#E6E2D6] pb-2">
                {selectedVoyage.nama_kapal}
              </h3>
              
              {/* Route visualization */}
              <div className="bg-[#FDFBF7] p-3 rounded-lg mb-3 border border-[#E6E2D6]">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex flex-col items-center">
                    <div className="w-3 h-3 rounded-full mb-1" style={{ backgroundColor: selectedVoyage.warna_asal }}></div>
                    <span className="font-semibold text-[#1A2421]">{selectedVoyage.asal}</span>
                  </div>
                  <div className="flex-1 mx-3 relative">
                    <div className="h-0.5 w-full" style={{ backgroundColor: selectedVoyage.warna_asal }}></div>
                    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M5 10L15 10M15 10L11 6M15 10L11 14" stroke={selectedVoyage.warna_asal} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </div>
                  </div>
                  <div className="flex flex-col items-center">
                    <div className="w-3 h-3 rounded-full bg-[#B85D19] mb-1"></div>
                    <span className="font-semibold text-[#1A2421]">Batavia</span>
                  </div>
                </div>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex items-start">
                  <span className="font-medium text-[#5C6A66] w-24 shrink-0">Tahun:</span>
                  <span className="text-[#1A2421] font-semibold">{selectedVoyage.tahun}</span>
                </div>
                
                <div className="flex items-start">
                  <span className="font-medium text-[#5C6A66] w-24 shrink-0">Nilai Cargo:</span>
                  <span className="text-[#B85D19] font-bold">
                    {selectedVoyage.total_gulden_nl.toLocaleString()} Gulden
                  </span>
                </div>

                <div className="flex items-start">
                  <span className="font-medium text-[#5C6A66] w-24 shrink-0">Produk Utama:</span>
                  <span className="text-[#1A2421] capitalize">{selectedVoyage.produk_utama}</span>
                </div>

                {/* All products with better formatting */}
                <div className="border-t border-[#E6E2D6] pt-2 mt-2">
                  <p className="font-medium text-[#5C6A66] mb-2">Semua Komoditi:</p>
                  <div className="flex flex-wrap gap-1">
                    {selectedVoyage.semua_produk.split('|').slice(0, 8).map((product, idx) => (
                      <span
                        key={idx}
                        className="text-xs px-2 py-1 bg-[#FDFBF7] border border-[#E6E2D6] rounded-full text-[#1A2421] capitalize"
                      >
                        {product.trim()}
                      </span>
                    ))}
                    {selectedVoyage.semua_produk.split('|').length > 8 && (
                      <span className="text-xs px-2 py-1 text-[#8A9A95]">
                        +{selectedVoyage.semua_produk.split('|').length - 8} lainnya
                      </span>
                    )}
                  </div>
                </div>

                {selectedVoyage.url && (
                  <div className="border-t border-[#E6E2D6] pt-2 mt-2">
                    <a
                      href={selectedVoyage.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-[#B85D19] hover:underline"
                    >
                      Lihat detail lengkap →
                    </a>
                  </div>
                )}
              </div>
            </div>
          </Popup>
        )}
      </Map>

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