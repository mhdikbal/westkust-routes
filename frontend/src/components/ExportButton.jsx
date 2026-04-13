import { Button } from "@/components/ui/button";
import { Download, FileText, Code, Image, BookOpen } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export default function ExportButton({ voyages }) {
  // ── Standard Exports ──────────────────────────────────────────────
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

    downloadFile(csvContent, "text/csv;charset=utf-8;", "westkust-voyages.csv");
  };

  const exportToJSON = () => {
    const jsonContent = JSON.stringify(voyages, null, 2);
    downloadFile(jsonContent, "application/json", "westkust-voyages.json");
  };

  // ── Academic Exports ──────────────────────────────────────────────
  const exportToLaTeX = () => {
    const escLatex = (s) => (s || "").replace(/[&%$#_{}~^\\]/g, (c) => `\\${c}`);
    
    const lines = [
      "% VOC Sumatera Westkust — Voyage Data",
      "% Generated from VOC Trade Atlas application",
      `% Date: ${new Date().toISOString().split("T")[0]}`,
      `% Total records: ${voyages.length}`,
      "",
      "\\begin{table}[htbp]",
      "\\centering",
      "\\caption{VOC Shipping Records — Sumatera Westkust}",
      "\\label{tab:voc-voyages}",
      "\\footnotesize",
      "\\begin{tabular}{|l|c|l|l|l|r|l|}",
      "\\hline",
      "\\textbf{Kapal} & \\textbf{Tahun} & \\textbf{Asal} & \\textbf{Tujuan} & \\textbf{Arah} & \\textbf{Nilai (ƒ)} & \\textbf{Produk Utama} \\\\",
      "\\hline",
    ];

    // Limit to 200 rows for practical LaTeX output
    const subset = voyages.slice(0, 200);
    subset.forEach((v) => {
      lines.push(
        `${escLatex(v.ship_name || "—")} & ${v.year || "—"} & ${escLatex(
          v.origin_name_raw || "—"
        )} & ${escLatex(v.destination_name_raw || "—")} & ${
          v.direction || "—"
        } & ${(v.total_gulden || 0).toLocaleString("en")} & ${escLatex(
          v.main_product || "—"
        )} \\\\`
      );
    });

    if (voyages.length > 200) {
      lines.push(`\\multicolumn{7}{|c|}{\\textit{... ${voyages.length - 200} more records omitted}} \\\\`);
    }

    lines.push("\\hline");
    lines.push("\\end{tabular}");
    lines.push("");
    
    // Summary statistics
    const totalValue = voyages.reduce((s, v) => s + (v.total_gulden || 0), 0);
    lines.push("\\vspace{0.5em}");
    lines.push(`\\noindent\\textit{Total: ${voyages.length} pelayaran, Nilai total: ${totalValue.toLocaleString("en")} Gulden}`);
    lines.push("");
    lines.push("\\end{table}");

    downloadFile(lines.join("\n"), "text/plain;charset=utf-8", "voc-voyages.tex");
  };

  const exportToBibTeX = () => {
    const today = new Date();
    const bib = [
      "@misc{voc_westkust_atlas,",
      "  author       = {{Boekhouder-Generaal Batavia (BGB)}},",
      "  title        = {VOC Shipping Records: Sumatera Westkust Trade Routes (1700--1789)},",
      "  year         = {1700/1789},",
      "  howpublished = {\\url{https://resources.huygens.knaw.nl/bgb/}},",
      `  note         = {Dataset of ${voyages.length} voyage records. Accessed ${today.toISOString().split("T")[0]}},`,
      "  publisher    = {Huygens ING / KNAW Humanities Cluster},",
      "  address      = {Amsterdam, The Netherlands},",
      "}",
      "",
      "@inbook{bgb_project,",
      "  author    = {Gerritsen, Ruud},",
      "  title     = {Bookkeeper-General Batavia},",
      "  booktitle = {Digital Resources for the Humanities},",
      "  publisher = {Huygens ING},",
      "  year      = {2017},",
      "  address   = {Amsterdam},",
      `  note      = {Source database for VOC trade cargo records, ${voyages.length} voyages extracted},`,
      "}",
    ];

    downloadFile(bib.join("\n"), "text/plain;charset=utf-8", "voc-westkust.bib");
  };

  const exportChartSVG = () => {
    // Find all SVG elements from Recharts in the page
    const svgElements = document.querySelectorAll(".recharts-wrapper svg");
    if (svgElements.length === 0) {
      alert("Tidak ada chart yang ditemukan di halaman. Buka tab Statistik atau Analitik terlebih dahulu.");
      return;
    }

    // Export first available chart
    const svg = svgElements[0];
    const serializer = new XMLSerializer();
    let svgString = serializer.serializeToString(svg);

    // Add XML declaration and namespace
    svgString = `<?xml version="1.0" encoding="UTF-8"?>\n` +
      svgString.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"');

    downloadFile(svgString, "image/svg+xml", "voc-chart.svg");
  };

  const exportChartPNG = () => {
    const svgElements = document.querySelectorAll(".recharts-wrapper svg");
    if (svgElements.length === 0) {
      alert("Tidak ada chart yang ditemukan di halaman. Buka tab Statistik atau Analitik terlebih dahulu.");
      return;
    }

    const svg = svgElements[0];
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svg);

    // Create high-res canvas (300 DPI equivalent)
    const scale = 3; // 3x for high resolution
    const canvas = document.createElement("canvas");
    const bbox = svg.getBoundingClientRect();
    canvas.width = bbox.width * scale;
    canvas.height = bbox.height * scale;

    const ctx = canvas.getContext("2d");
    ctx.scale(scale, scale);

    // Set dark background
    ctx.fillStyle = "#0d1221";
    ctx.fillRect(0, 0, bbox.width, bbox.height);

    const img = new window.Image();
    const svgBlob = new Blob([svgString], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(svgBlob);

    img.onload = () => {
      ctx.drawImage(img, 0, 0, bbox.width, bbox.height);
      URL.revokeObjectURL(url);

      canvas.toBlob(
        (blob) => {
          const link = document.createElement("a");
          link.href = URL.createObjectURL(blob);
          link.download = `voc-chart-${new Date().toISOString().split("T")[0]}.png`;
          link.click();
        },
        "image/png",
        1.0
      );
    };
    img.src = url;
  };

  // ── Helper ────────────────────────────────────────────────────────
  const downloadFile = (content, type, filename) => {
    const date = new Date().toISOString().split("T")[0];
    const blob = new Blob([content], { type });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${date}-${filename}`;
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
      <DropdownMenuContent className="bg-[#0d1221] border-white/10 min-w-[220px]">
        {/* Standard exports */}
        <DropdownMenuLabel className="text-[10px] uppercase tracking-wider text-white/30">
          Data Export
        </DropdownMenuLabel>
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

        <DropdownMenuSeparator className="bg-white/10" />

        {/* Academic exports */}
        <DropdownMenuLabel className="text-[10px] uppercase tracking-wider text-white/30">
          Akademik & Publikasi
        </DropdownMenuLabel>
        <DropdownMenuItem 
          onClick={exportToLaTeX}
          className="cursor-pointer text-white/70 hover:bg-white/10 hover:text-white"
          data-testid="export-latex"
        >
          <Code className="w-4 h-4 mr-2 text-[#00D4AA]" />
          Tabel LaTeX (.tex)
        </DropdownMenuItem>
        <DropdownMenuItem 
          onClick={exportToBibTeX}
          className="cursor-pointer text-white/70 hover:bg-white/10 hover:text-white"
          data-testid="export-bibtex"
        >
          <BookOpen className="w-4 h-4 mr-2 text-[#FFD93D]" />
          Sitasi BibTeX (.bib)
        </DropdownMenuItem>

        <DropdownMenuSeparator className="bg-white/10" />

        {/* Chart exports */}
        <DropdownMenuLabel className="text-[10px] uppercase tracking-wider text-white/30">
          Grafik (dari tab Statistik)
        </DropdownMenuLabel>
        <DropdownMenuItem 
          onClick={exportChartSVG}
          className="cursor-pointer text-white/70 hover:bg-white/10 hover:text-white"
          data-testid="export-svg"
        >
          <Image className="w-4 h-4 mr-2 text-[#FF6B6B]" />
          Chart sebagai SVG (vektor)
        </DropdownMenuItem>
        <DropdownMenuItem 
          onClick={exportChartPNG}
          className="cursor-pointer text-white/70 hover:bg-white/10 hover:text-white"
          data-testid="export-png"
        >
          <Image className="w-4 h-4 mr-2 text-[#8e44ad]" />
          Chart sebagai PNG (300 DPI)
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}