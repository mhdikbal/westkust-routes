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
      "Nilai Cargo (Gulden)",
      "Produk Utama",
      "Semua Produk",
      "URL"
    ];

    const csvContent = [
      headers.join(","),
      ...voyages.map(v => [
        `"${v.nama_kapal}"`,
        v.tahun,
        `"${v.asal}"`,
        `"${v.tujuan}"`,
        v.total_gulden_nl,
        `"${v.produk_utama}"`,
        `"${v.semua_produk}"`,
        `"${v.url}""`
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
          className="bg-white border-[#E6E2D6] hover:bg-[#FDFBF7] text-[#1A2421]"
          data-testid="export-button"
        >
          <Download className="w-4 h-4 mr-2" />
          Ekspor Data
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="bg-[#FDFBF7] border-[#E6E2D6]">
        <DropdownMenuItem 
          onClick={exportToCSV}
          className="cursor-pointer hover:bg-white"
          data-testid="export-csv"
        >
          <FileText className="w-4 h-4 mr-2" />
          Ekspor sebagai CSV
        </DropdownMenuItem>
        <DropdownMenuItem 
          onClick={exportToJSON}
          className="cursor-pointer hover:bg-white"
          data-testid="export-json"
        >
          <FileText className="w-4 h-4 mr-2" />
          Ekspor sebagai JSON
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}