import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MapDashboard from "@/pages/MapDashboard";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MapDashboard />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;