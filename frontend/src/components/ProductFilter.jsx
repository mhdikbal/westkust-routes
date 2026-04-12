import { Checkbox } from "@/components/ui/checkbox";
import { Card } from "@/components/ui/card";
import { Package } from "lucide-react";

export default function ProductFilter({ voyages, selectedProducts, setSelectedProducts }) {
  // Get unique products — use new field name
  const productCounts = voyages.reduce((acc, voyage) => {
    const product = voyage.main_product;
    if (!product) return acc;
    if (!acc[product]) {
      acc[product] = 0;
    }
    acc[product] += 1;
    return acc;
  }, {});

  const products = Object.entries(productCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8) // Top 8 products
    .map(([name, count]) => ({ name, count }));

  const toggleProduct = (product) => {
    if (selectedProducts.includes(product)) {
      setSelectedProducts(selectedProducts.filter((p) => p !== product));
    } else {
      setSelectedProducts([...selectedProducts, product]);
    }
  };

  return (
    <Card className="p-4 bg-white/5 border border-white/10 shadow-none">
      <div className="flex items-center gap-2 mb-3">
        <Package className="w-4 h-4 text-[#00D4AA]" />
        <h3 className="font-serif text-sm font-semibold text-white">
          Filter Produk
        </h3>
      </div>
      <div className="space-y-2 max-h-48 overflow-y-auto">
        {products.map((product) => (
          <div key={product.name} className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Checkbox
                id={`product-${product.name}`}
                checked={selectedProducts.includes(product.name)}
                onCheckedChange={() => toggleProduct(product.name)}
                data-testid={`product-filter-${product.name.toLowerCase()}`}
              />
              <label
                htmlFor={`product-${product.name}`}
                className="text-xs text-white/60 capitalize cursor-pointer"
              >
                {product.name}
              </label>
            </div>
            <span className="text-xs text-white/30">({product.count})</span>
          </div>
        ))}
      </div>
    </Card>
  );
}