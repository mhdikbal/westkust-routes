import { Card } from "@/components/ui/card";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { TrendingUp, Package, Ship, Calendar } from "lucide-react";

export default function StatisticsPanel({ voyages, stats }) {
  // Prepare data for yearly statistics — use new field names
  const yearlyData = voyages.reduce((acc, voyage) => {
    const year = voyage.year;
    if (!year) return acc;
    if (!acc[year]) {
      acc[year] = { year, count: 0, value: 0 };
    }
    acc[year].count += 1;
    acc[year].value += (voyage.total_gulden || 0);
    return acc;
  }, {});

  const chartData = Object.values(yearlyData)
    .sort((a, b) => a.year - b.year)
    .map(d => ({
      year: d.year,
      kapal: d.count,
      nilai: Math.round(d.value / 1000), // Convert to thousands
    }));

  // Product statistics — use new field name
  const productStats = voyages.reduce((acc, voyage) => {
    const product = voyage.main_product;
    if (!product) return acc;
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
        <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
          <div className="flex items-center gap-2 mb-1">
            <Ship className="w-4 h-4 text-[#00D4AA]" />
            <p className="text-xs uppercase tracking-[0.2em] text-white/40">Total Kapal</p>
          </div>
          <p className="text-2xl font-serif font-bold text-white">{voyages.length}</p>
        </Card>

        <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
          <div className="flex items-center gap-2 mb-1">
            <TrendingUp className="w-4 h-4 text-[#FFD93D]" />
            <p className="text-xs uppercase tracking-[0.2em] text-white/40">Total Nilai</p>
          </div>
          <p className="text-xl font-serif font-bold text-[#00D4AA]">
            {(voyages.reduce((sum, v) => sum + (v.total_gulden || 0), 0) / 1000000).toFixed(1)}M
          </p>
        </Card>
      </div>

      {/* Yearly Chart */}
      <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
        <div className="flex items-center gap-2 mb-4">
          <Calendar className="w-4 h-4 text-[#00D4AA]" />
          <h3 className="font-serif text-sm font-semibold text-white">
            Pelayaran per Tahun
          </h3>
        </div>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis 
              dataKey="year" 
              tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.5)' }}
              tickFormatter={(value) => value}
            />
            <YAxis tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.5)' }} />
            <Tooltip 
              contentStyle={{ 
                background: '#0d1221', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '8px',
                fontSize: '12px',
                color: '#fff',
              }}
            />
            <Line 
              type="monotone" 
              dataKey="kapal" 
              stroke="#00D4AA" 
              strokeWidth={2}
              dot={{ fill: '#00D4AA', r: 3 }}
              name="Jumlah Kapal"
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Top Products */}
      <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
        <div className="flex items-center gap-2 mb-4">
          <Package className="w-4 h-4 text-[#00D4AA]" />
          <h3 className="font-serif text-sm font-semibold text-white">
            Produk Utama
          </h3>
        </div>
        <div className="space-y-2">
          {topProducts.map((product, idx) => (
            <div key={idx} className="flex items-center justify-between">
              <span className="text-xs text-white/60 capitalize">{product.name}</span>
              <div className="flex items-center gap-2">
                <div 
                  className="h-2 bg-[#00D4AA] rounded"
                  style={{ width: `${(product.count / (topProducts[0]?.count || 1)) * 60}px` }}
                />
                <span className="text-xs font-medium text-white w-8 text-right">
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