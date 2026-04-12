import { Button } from "@/components/ui/button";
import { Download, FileText } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export default function ExportButton({ voyages }) {
  const exportToCSV = () => {
    const headers = [
      "Nama Kapal",
      "Tahun",
      "Asal",
      "Tujuan",
      "Arah",
      "Nilai Cargo (Gulden)",
      "Produk Utama",
      "Semua Produk",
      "Tgl Berangkat",
      "Tgl Tiba",
      "URL"
    ];

    const csvContent = [
      headers.join(","),
      ...voyages.map(v => [
        `"${v.ship_name || ''}"`,
        v.year || '',
        `"${v.origin_name_raw || ''}"`,
        `"${v.destination_name_raw || v.destination || ''}"`,
        `"${v.direction || ''}"`,
        v.total_gulden || 0,
        `"${v.main_product || ''}"`,
        `"${(v.all_products || '').replace(/"/g, '""')}"`,
        `"${v.departure_date || ''}"`,
        `"${v.arrival_date || ''}"`,
        `"${v.source_url || ''}"`
      ].join(","))
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `westkust-voyages-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  const exportToJSON = () => {
    const jsonContent = JSON.stringify(voyages, null, 2);
    const blob = new Blob([jsonContent], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `westkust-voyages-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="bg-white/5 border-white/10 hover:bg-white/10 text-white"
          data-testid="export-button"
        >
          <Download className="w-4 h-4 mr-2" />
          Ekspor Data
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="bg-[#0d1221] border-white/10">
        <DropdownMenuItem 
          onClick={exportToCSV}
          className="cursor-pointer text-white/70 hover:bg-white/10 hover:text-white"
          data-testid="export-csv"
        >
          <FileText className="w-4 h-4 mr-2" />
          Ekspor sebagai CSV
        </DropdownMenuItem>
        <DropdownMenuItem 
          onClick={exportToJSON}
          className="cursor-pointer text-white/70 hover:bg-white/10 hover:text-white"
          data-testid="export-json"
        >
          <FileText className="w-4 h-4 mr-2" />
          Ekspor sebagai JSON
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}