# 🚢 Westkust Maritime Routes

Aplikasi visualisasi interaktif jalur pelayaran historis dari **Sumatra's Westkust** (Pantai Barat Sumatra) ke **Batavia** pada masa VOC (1700-1789).

![Westkust Routes](https://img.shields.io/badge/Period-1700--1789-orange) ![Ships](https://img.shields.io/badge/Ships-176-blue) ![Tech](https://img.shields.io/badge/Tech-React%20%7C%20FastAPI%20%7C%20MongoDB-green)

## 📖 Deskripsi

Aplikasi ini menampilkan data historis pelayaran kapal VOC dari tiga pelabuhan utama di Pantai Barat Sumatra:
- **Padang** (Muaro Padang)
- **Pulau Cingkuak**
- **Air Haji**

Menuju **Sunda Kelapa (Batavia, Jakarta)** dengan total **176 voyage records** yang mencakup informasi detail tentang:
- Nama kapal
- Tahun keberangkatan (1700-1789)
- Nilai cargo dalam Gulden Belanda
- Komoditi yang diperdagangkan (Emas/Goud, Lada/Peper, Kamfer, Benzoë, dll)

## ✨ Fitur Utama

### 🗺️ Peta Interaktif
- **4 Fort Icons** menandai pelabuhan utama:
  - Padang (Muaro Padang)
  - Pulau Cingkuak
  - Air Haji
  - Sunda Kelapa (Batavia)
- Peta menggunakan **Maplibre GL JS** dengan basemap Carto Voyager
- Zoom dan pan interaktif

### 🚢 Detail Pelayaran
- **Klik nama kapal** di sidebar → Modal detail muncul dengan:
  - Visualisasi rute (Pelabuhan Asal → Batavia)
  - Tahun keberangkatan
  - Nilai cargo (format Gulden NL)
  - Produk utama
  - **Semua komoditi** dalam pills/badges interaktif
  - Link ke sumber data (BGC Huygens)

### 🔍 Filter & Search
- **Filter Pelabuhan**: Padang, Pulau Cingkuak, Air Haji
- **Filter Produk**: Goud, Berggoud, Benzoë, Peper, Kamfer, dll
- **Pencarian Kapal**: Cari berdasarkan nama kapal
- **Timeline Slider**: Filter berdasarkan tahun (1700-1789)

### 📊 Statistik
- Tab Statistik dengan:
  - Total kapal dan nilai cargo
  - Grafik pelayaran per tahun (Line Chart)
  - Top 5 produk utama
  - Breakdown per pelabuhan

### 📥 Ekspor Data
- Export ke **CSV** format
- Export ke **JSON** format
- Include semua detail pelayaran

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI Framework
- **Maplibre GL JS** - Interactive Maps
- **Shadcn/UI** - Component Library
- **Tailwind CSS** - Styling
- **Recharts** - Data Visualization
- **Axios** - HTTP Client

### Backend
- **FastAPI** - Python Web Framework
- **MongoDB** - NoSQL Database (Motor async driver)
- **Pydantic** - Data Validation

### Development
- **Yarn** - Package Manager
- **Supervisor** - Process Manager
- **React Scripts** - Build Tools

## 📁 Struktur Project

```
westkust-routes/
├── backend/
│   ├── server.py              # FastAPI application
│   ├── seed_data.py           # Database seeder
│   ├── voyages_data.json      # Voyage data
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main app component
│   │   ├── App.css           # Global styles
│   │   ├── index.css         # Base styles + fonts
│   │   ├── pages/
│   │   │   └── MapDashboard.jsx      # Main dashboard page
│   │   └── components/
│   │       ├── Sidebar.jsx           # Filter & ship list
│   │       ├── TimelineSlider.jsx    # Year range slider
│   │       ├── WelcomeModal.jsx      # Welcome screen
│   │       ├── VoyageDetailModal.jsx # Ship detail popup
│   │       ├── PortMarkers.jsx       # Fort icons on map
│   │       ├── PortShipListModal.jsx # Port ship list
│   │       ├── StatisticsPanel.jsx   # Stats & charts
│   │       ├── ProductFilter.jsx     # Product filter
│   │       ├── ExportButton.jsx      # Data export
│   │       └── ui/                   # Shadcn components
│   ├── package.json          # Node dependencies
│   ├── tailwind.config.js    # Tailwind configuration
│   └── .env                  # Frontend env variables
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Node.js 16+ dan Yarn
- Python 3.9+
- MongoDB

### 1. Clone Repository
```bash
git clone https://github.com/mhdikbal/westkust-routes.git
cd westkust-routes
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup .env file
cp .env.example .env
# Edit .env dengan MongoDB connection string Anda

# Seed database
python seed_data.py

# Run backend
uvicorn server:app --reload --port 8001
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
yarn install

# Setup .env file
cp .env.example .env
# Edit REACT_APP_BACKEND_URL ke backend URL Anda

# Run frontend
yarn start
```

Frontend akan berjalan di `http://localhost:3000`

## 📊 Data Source

Data pelayaran bersumber dari:
- **Bookkeeper-General Batavia (BGC)** - Huygens Institute KNAW
- URL: https://resources.huygens.knaw.nl/bgb/

Dataset mencakup:
- **176 voyage records** (1700-1789)
- **3 pelabuhan** keberangkatan di Sumatra Barat
- **50+ jenis komoditi** yang diperdagangkan
- **Total nilai cargo**: 15.7 juta Gulden

## 🗺️ Koordinat Pelabuhan

```javascript
const PORTS = {
  Padang: [100.35659, -0.96543],           // Muaro Padang
  "Pulau Cingkuak": [100.55977, -1.35303], // Pulau Cingkuak
  "Air Haji": [100.86801, -1.94012],       // Air Haji
  Batavia: [106.8456, -6.2088],            // Sunda Kelapa (Jakarta)
};
```

## 🎨 Design System

### Colors
- **Primary**: `#B85D19` (Terracotta/Orange)
- **Background**: `#FDFBF7` (Cream)
- **Text**: `#1A2421` (Dark Green)
- **Accent**: `#D4AF37` (Gold)
- **Border**: `#E6E2D6` (Light Beige)

### Typography
- **Headings**: Playfair Display (Serif)
- **Body**: IBM Plex Sans
- **Theme**: Museum/Archival dengan nuansa historical

## 📱 Fitur Detail

### Welcome Modal
- Greeting screen dengan overview aplikasi
- Penjelasan fitur utama
- Button "Mulai Jelajahi Peta"

### Sidebar Panel
- **Tab Pelayaran**: List kapal dengan search & filter
- **Tab Statistik**: Dashboard analytics
- Sticky positioning di kiri layar
- Scrollable ship list

### Timeline Slider
- Range slider untuk filter tahun
- Display current year range
- Real-time update map & data

### Voyage Detail Modal
- Full-screen modal dengan detail lengkap:
  - Visual route dengan arrow
  - Tahun keberangkatan (card)
  - Nilai cargo (card)
  - Produk utama (card)
  - Semua komoditi (pills dengan hover effect)
  - Link sumber data

### Port Ship List Modal (In Progress)
- Modal list kapal per pelabuhan
- Summary statistics (total kapal, total nilai)
- Scrollable ship list dengan button "Detail Komoditi"

## 🔌 API Endpoints

### GET /api/voyages
Dapatkan semua voyage dengan filter
```
Query Parameters:
- year_from: int (optional)
- year_to: int (optional)
- port: string (optional) - "Padang" | "Pulau Cingkuak" | "Air Haji"
- search: string (optional) - search by ship name

Response: Array of Voyage objects
```

### GET /api/voyages/stats
Dapatkan statistik voyages
```
Query Parameters:
- year_from: int (optional)
- year_to: int (optional)

Response: {
  total_voyages: int,
  total_cargo_value: float,
  year_range: { min: int, max: int },
  ports: { [portName]: { count: int, value: float } },
  top_products: [{ name: string, count: int }]
}
```

## 🎯 Use Cases

1. **Penelitian Sejarah Maritim**
   - Analisis pola perdagangan VOC
   - Studi komoditi ekspor Sumatra
   - Riset jalur pelayaran historis

2. **Edukasi**
   - Pembelajaran sejarah perdagangan maritim Indonesia
   - Visualisasi data historis
   - Material untuk museum dan pameran

3. **Data Journalism**
   - Investigasi ekonomi kolonial
   - Visualisasi perdagangan masa VOC
   - Story-telling berbasis data

## 🐛 Known Issues

1. **Fort Icon Click Handler** - Click pada fort icons belum trigger modal list kapal (workaround: klik nama kapal di sidebar)
2. **"Made with Emergent" Badge** - Masih terlihat di production (CSS needs update)

## 🔮 Future Enhancements

- [ ] Fix fort icon click handler untuk membuka port ship list
- [ ] Tambahkan animasi kapal bergerak di rute
- [ ] Curve/arc pada rute untuk visualisasi lebih baik
- [ ] Export ke PDF dengan visualisasi peta
- [ ] Heatmap intensitas pelayaran
- [ ] Dark mode toggle
- [ ] Multi-language support (EN/ID)
- [ ] Mobile responsive optimization

## 👥 Contributing

Contributions are welcome! Please:
1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Data pelayaran bersumber dari Bookkeeper-General Batavia (BGC) - Huygens Institute KNAW.

## 🙏 Acknowledgments

- **Huygens Institute KNAW** - Untuk dataset BGC Batavia
- **Atlas of Mutual Heritage** - Inspirasi desain dan konsep
- Data historians yang telah digitalisasi arsip VOC

## 📧 Contact

**Muhammad Ikbal**
- GitHub: [@mhdikbal](https://github.com/mhdikbal)
- Repository: [westkust-routes](https://github.com/mhdikbal/westkust-routes)

---

**Built with ❤️ for Maritime History Research**

🏰 Preserving and visualizing Indonesia's maritime heritage
