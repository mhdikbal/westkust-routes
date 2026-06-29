"""
VOC Glossarium PDF Scraper
Sumber: https://resources.huygens.knaw.nl/pdf/vocglossarium/VOCGlossarium.pdf

Strategi parsing:
  - VOC Glossarium disusun alfabetis, setiap entri dimulai dengan KATA KUNCI (bold atau
    semua kapital) diikuti tanda em-dash (—) atau titik dua, lalu definisi Belanda.
  - Satu entri bisa bersprawl beberapa baris.
  - Output: CSV + JSON siap di-seed ke tabel commodity_glossary.

Jalankan dari host (bukan container):
  pip install pdfplumber
  python3 scrawling/voc_glossarium_scraper.py --pdf /path/to/VOCGlossarium.pdf

Atau download dulu:
  curl -L https://resources.huygens.knaw.nl/pdf/vocglossarium/VOCGlossarium.pdf \
       -o /tmp/VOCGlossarium.pdf
  python3 scrawling/voc_glossarium_scraper.py --pdf /tmp/VOCGlossarium.pdf
"""

import re
import csv
import json
import argparse
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    raise SystemExit("Install dulu: pip install pdfplumber")


# ── Regex patterns ─────────────────────────────────────────────────────────────

# Entry dimulai dengan kata (huruf kecil/kapital) diikuti spasi + em-dash / n-dash / ' - '
# Contoh entri nyata:
#   benzoin — hars van de Styrax benzoin boom...
#   kamfer (kampher, kafur) — vluchtig...
#   goud — edelmetaal...
ENTRY_START = re.compile(
    r'^([a-z][a-zéèëàáâäüûùôóòêîïñç\'\-]+(?:\s+[a-z][a-zéèëàáâäüûùôóòêîïñç\'\-]+)?)'
    r'(?:\s*\([^)]+\))?'          # optional: varianten dalam kurung
    r'\s*(?:—|–|-)+'              # em-dash, n-dash, atau hyphen
    r'\s*(.+)',
    re.IGNORECASE
)

# Varian ejaan: kata dalam kurung di awal definisi
VARIANTS_RE = re.compile(r'^\(([^)]+)\)\s*')


def extract_text_from_pdf(pdf_path: str) -> list[str]:
    """Ekstrak semua baris teks dari PDF, bersih dari header/footer nomor halaman."""
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text(x_tolerance=2, y_tolerance=3)
            if not text:
                continue
            for line in text.splitlines():
                stripped = line.strip()
                # Skip nomor halaman dan header kosong
                if re.match(r'^\d+$', stripped):
                    continue
                if len(stripped) < 2:
                    continue
                lines.append(stripped)
    return lines


def parse_glossarium(lines: list[str]) -> list[dict]:
    """
    Parse baris teks menjadi daftar entri glossarium.

    Setiap entri: {term, variants, definition_nl}
    Multi-baris: gabungkan sampai entri berikutnya dimulai.
    """
    entries = []
    current_term = None
    current_variants = []
    current_def_parts = []

    def flush():
        if current_term:
            entries.append({
                "term": current_term.lower().strip(),
                "term_display": current_term.strip(),
                "variants": current_variants[:],
                "definition_nl": " ".join(current_def_parts).strip(),
            })

    for line in lines:
        m = ENTRY_START.match(line)
        if m:
            flush()
            current_term = m.group(1).strip()
            definition_raw = m.group(2).strip()

            # Cek varian ejaan di awal definisi, contoh: (kampher, kafur) — vluchtig...
            vm = VARIANTS_RE.match(definition_raw)
            if vm:
                current_variants = [v.strip() for v in vm.group(1).split(',')]
                definition_raw = definition_raw[vm.end():].strip()
            else:
                current_variants = []

            current_def_parts = [definition_raw] if definition_raw else []
        elif current_term:
            # Kelanjutan definisi entri sebelumnya
            current_def_parts.append(line)

    flush()
    return entries


def match_with_voyage_products(entries: list[dict], products: list[str]) -> list[dict]:
    """
    Tandai entri mana yang ada di dataset voyage (untuk prioritas translation).
    products: list of unique product terms dari query PostgreSQL.
    """
    product_set = {p.lower().strip() for p in products}

    for entry in entries:
        term = entry["term"]
        all_forms = {term} | {v.lower().strip() for v in entry.get("variants", [])}
        entry["in_dataset"] = bool(all_forms & product_set)

    return entries


def save_outputs(entries: list[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON — semua entri
    json_path = output_dir / "voc_glossarium.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"JSON: {json_path}  ({len(entries)} entri)")

    # CSV — semua entri
    csv_path = output_dir / "voc_glossarium.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "term", "term_display", "variants", "definition_nl", "in_dataset"
        ])
        writer.writeheader()
        for e in entries:
            writer.writerow({
                "term": e["term"],
                "term_display": e["term_display"],
                "variants": "; ".join(e.get("variants", [])),
                "definition_nl": e["definition_nl"],
                "in_dataset": e.get("in_dataset", False),
            })
    print(f"CSV: {csv_path}")

    # CSV hanya yang ada di dataset voyage (prioritas translate)
    priority_path = output_dir / "voc_glossarium_priority.csv"
    priority = [e for e in entries if e.get("in_dataset")]
    with open(priority_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["term", "term_display", "variants", "definition_nl"])
        writer.writeheader()
        for e in priority:
            writer.writerow({
                "term": e["term"],
                "term_display": e["term_display"],
                "variants": "; ".join(e.get("variants", [])),
                "definition_nl": e["definition_nl"],
            })
    print(f"Priority CSV (untuk terjemahan): {priority_path}  ({len(priority)} entri cocok dataset)")


def main():
    ap = argparse.ArgumentParser(description="Scrape VOC Glossarium PDF ke CSV/JSON")
    ap.add_argument("--pdf", required=True, help="Path ke VOCGlossarium.pdf")
    ap.add_argument("--out", default="scrawling/glossarium_output",
                    help="Direktori output (default: scrawling/glossarium_output)")
    ap.add_argument("--products-json", default=None,
                    help="Path ke JSON list produk voyage (opsional, untuk flag in_dataset)")
    args = ap.parse_args()

    print(f"Membaca PDF: {args.pdf}")
    lines = extract_text_from_pdf(args.pdf)
    print(f"  {len(lines)} baris teks diekstrak")

    entries = parse_glossarium(lines)
    print(f"  {len(entries)} entri glossarium di-parse")

    # Match dengan produk dari dataset jika ada
    if args.products_json:
        with open(args.products_json) as f:
            products = json.load(f)
        entries = match_with_voyage_products(entries, products)
        matched = sum(1 for e in entries if e.get("in_dataset"))
        print(f"  {matched} entri cocok dengan produk di dataset voyage")

    save_outputs(entries, Path(args.out))


if __name__ == "__main__":
    main()
