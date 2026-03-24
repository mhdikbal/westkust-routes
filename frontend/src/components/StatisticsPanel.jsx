import { Card } from "@/components/ui/card";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { TrendingUp, Package, Ship, Calendar } from "lucide-react";

export default function StatisticsPanel({ voyages, stats }) {
  // Prepare data for yearly statistics
  const yearlyData = voyages.reduce((acc, voyage) => {
    const year = voyage.tahun;
    if (!acc[year]) {
      acc[year] = { year, count: 0, value: 0 };
    }
    acc[year].count += 1;
    acc[year].value += voyage.total_gulden_nl;
    return acc;
  }, {});

  const chartData = Object.values(yearlyData)
    .sort((a, b) => a.year - b.year)
    .map(d => ({
      year: d.year,
      kapal: d.count,
      nilai: Math.round(d.value / 1000), // Convert to thousands
    }));

  // Product statistics
  const productStats = voyages.reduce((acc, voyage) => {
    const product = voyage.produk_utama;
    if (!acc[product]) {
      acc[product] = 0;
    }
    acc[product] += 1;
    return acc;
  }, {});

  const topProducts = Object.entries(productStats)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([name, count]) => ({ name, count }));

  return (
    <div className="space-y-6" data-testid="statistics-panel">
      {/* Summary Cards */}
      <div className="grid grid-cols-2 gap-3">
        <Card className="p-4 bg-white border border-[#E6E2D6] shadow-none">
          <div className="flex items-center gap-2 mb-1">
            <Ship className="w-4 h-4 text-[#B85D19]" />
            <p className="text-xs uppercase tracking-[0.2em] text-[#8A9A95]">Total Kapal</p>
          </div>
          <p className="text-2xl font-serif font-bold text-[#1A2421]">{voyages.length}</p>
        </Card>

        <Card className="p-4 bg-white border border-[#E6E2D6] shadow-none">
          <div className="flex items-center gap-2 mb-1">
            <TrendingUp className="w-4 h-4 text-[#D4AF37]" />
            <p className="text-xs uppercase tracking-[0.2em] text-[#8A9A95]">Total Nilai</p>
          </div>
          <p className="text-xl font-serif font-bold text-[#1A2421]">
            {(voyages.reduce((sum, v) => sum + v.total_gulden_nl, 0) / 1000000).toFixed(1)}M
          </p>
        </Card>
      </div>

      {/* Yearly Chart */}
      <Card className="p-4 bg-white border border-[#E6E2D6] shadow-none">
        <div className="flex items-center gap-2 mb-4">
          <Calendar className="w-4 h-4 text-[#B85D19]" />
          <h3 className="font-serif text-sm font-semibold text-[#1A2421]">
            Pelayaran per Tahun
          </h3>
        </div>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E6E2D6" />
            <XAxis 
              dataKey="year" 
              tick={{ fontSize: 10, fill: '#5C6A66' }}
              tickFormatter={(value) => value}
            />
            <YAxis tick={{ fontSize: 10, fill: '#5C6A66' }} />
            <Tooltip 
              contentStyle={{ 
                background: '#FDFBF7', 
                border: '1px solid #E6E2D6',
                borderRadius: '8px',
                fontSize: '12px'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="kapal" 
              stroke="#B85D19" 
              strokeWidth={2}
              dot={{ fill: '#B85D19', r: 3 }}
              name="Jumlah Kapal"
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Top Products */}
      <Card className="p-4 bg-white border border-[#E6E2D6] shadow-none">
        <div className="flex items-center gap-2 mb-4">
          <Package className="w-4 h-4 text-[#B85D19]" />
          <h3 className="font-serif text-sm font-semibold text-[#1A2421]">
            Produk Utama
          </h3>
        </div>
        <div className="space-y-2">
          {topProducts.map((product, idx) => (
            <div key={idx} className="flex items-center justify-between">
              <span className="text-xs text-[#5C6A66] capitalize">{product.name}</span>
              <div className="flex items-center gap-2">
                <div 
                  className="h-2 bg-[#B85D19] rounded"
                  style={{ width: `${(product.count / topProducts[0].count) * 60}px` }}
                />
                <span className="text-xs font-medium text-[#1A2421] w-8 text-right">
                  {product.count}
                </span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}