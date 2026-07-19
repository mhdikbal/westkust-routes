#!/usr/bin/env python3
"""
classify_diplomasi_llm.py — LLM-judge label `diplomasi` (CASCADE).

Zero-shot mDeBERTa GAGAL gerbang validasi utk `diplomasi` (over-fire: bentuk
surat resmi dikira diplomasi). Lihat docs/prd/prd-diplomasi-llm-judge.md.

Pola CASCADE (retrieve-then-rerank):
  Tier-0 RECALL : zero-shot skor_diplomasi >= AMBANG  -> kandidat (~630)
  Tier-1 PRESISI: LLM-judge tiap kandidat -> {diplomasi, confidence, alasan}
Non-kandidat (skor < ambang) diasumsikan non-diplomasi; asumsi ini DIVALIDASI
dengan menilai sampel acak non-kandidat (recall check).

Aman: kolom lama (tema_dominan/Sankey live) TIDAK disentuh — output kolom baru.
0 GPU. Idempotent/resume by corpus_id. temperature=0.

Jalankan:
  export SUMOPOD_API_KEY=sk-...           # JANGAN hardcode key
  python classify_diplomasi_llm.py \
      --input docs/thesis/dr/korpus_tema_diplomasi.csv \
      --output docs/thesis/dr/diplomasi_llm_judge.csv
Di Colab: set --input ke path Drive; API key via os.environ/secret.
"""
import os, sys, csv, json, re, time, random, argparse

# ── konfigurasi (semua bisa lewat env / arg) ────────────────────────────────
API_KEY  = os.getenv("SUMOPOD_API_KEY") or os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL", "https://ai.sumopod.com/v1")
MODEL    = os.getenv("LLM_MODEL", "gpt-4o-mini")
csv.field_size_limit(sys.maxsize)  # text_asli bisa 4MB (walau kita tak pakai)

RUBRIK = (
    "Anda penilai historiografi VOC pesisir barat Sumatra. Nilai apakah SATU teks "
    "arsip TERUTAMA tentang hubungan/aksi DIPLOMATIK antar penguasa atau negeri: "
    "perundingan, perjanjian/kontrak politik, pengiriman atau penerimaan UTUSAN resmi, "
    "sumpah setia/aliansi, atau upaya perdamaian.\n"
    "BUKAN diplomasi (false): daftar kargo/muatan, laporan perang murni tanpa "
    "perundingan, register/daftar dokumen, perkara hukum, instruksi administratif "
    "rutin, surat dagang biasa. Fokus pada ISI, bukan sekadar BENTUK surat resmi.\n"
    'Balas HANYA JSON: {"diplomasi": true|false, "confidence": 0.0-1.0, '
    '"alasan": "<=15 kata"}'
)

# few-shot dari FALSE-POSITIVE nyata run zero-shot yang gagal (+ contoh benar)
FEWSHOT = [
    ("000 potong kain linen guinee; 5090 bafta; 5980 siouters; muatan naik jagt Constantia",
     {"diplomasi": False, "confidence": 0.95, "alasan": "daftar kargo dagang"}),
    ("19 Maret. Kabar buruk, mereka dari Songeytrap dengan 12 benteng sedang berperang",
     {"diplomasi": False, "confidence": 0.9, "alasan": "laporan perang, bukan perundingan"}),
    ("Daftar semua kertas-kertas yang berturut-turut tahun ini diterima dari Bassoura",
     {"diplomasi": False, "confidence": 0.92, "alasan": "register dokumen administratif"}),
    ("Surat dari Paducca Siry Sultan Nulma Alam yang memerintah negeri Achin kepada "
     "Gouverneur Generaal Joan Maetsuyker di kastel Batavia",
     {"diplomasi": True, "confidence": 0.97, "alasan": "surat antar penguasa Aceh-VOC"}),
    ("memanggil Sultan Mahomettha dari Indrapoura untuk melihat apakah perkara itu "
     "dapat didamaikan, dan dikirim utusan dari Padang",
     {"diplomasi": True, "confidence": 0.9, "alasan": "perundingan damai + utusan"}),
]

def build_messages(text):
    msgs = [{"role": "system", "content": RUBRIK}]
    for t, ans in FEWSHOT:
        msgs.append({"role": "user", "content": t})
        msgs.append({"role": "assistant", "content": json.dumps(ans, ensure_ascii=False)})
    msgs.append({"role": "user", "content": text[:1500]})
    return msgs

def extract_json(s):
    m = re.search(r"\{.*\}", s, re.S)
    if not m:
        return None
    return json.loads(m.group(0))

def judge(client, text, retries=3):
    for i in range(retries):
        try:
            r = client.chat.completions.create(
                model=MODEL, messages=build_messages(text),
                temperature=0, max_tokens=120,
            )
            d = extract_json(r.choices[0].message.content or "")
            if d is None:
                raise ValueError("JSON tak ditemukan di respons")
            return (bool(d.get("diplomasi")),
                    float(d.get("confidence", 0) or 0),
                    str(d.get("alasan", ""))[:120])
        except Exception as e:
            if i == retries - 1:
                return (None, None, f"ERROR: {e}")
            time.sleep(2 * (i + 1))  # backoff (script user-run, sleep OK)

def load_done(out_path):
    done = set()
    if os.path.exists(out_path):
        with open(out_path, newline="") as f:
            for row in csv.DictReader(f):
                done.add(row["corpus_id"])
    return done

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="docs/thesis/dr/korpus_tema_diplomasi.csv")
    ap.add_argument("--output", default="docs/thesis/dr/diplomasi_llm_judge.csv")
    ap.add_argument("--ambang", type=float, default=0.5, help="ambang kandidat skor_diplomasi (zero-shot)")
    ap.add_argument("--recall-sample", type=int, default=20, help="jumlah non-kandidat utk cek recall")
    args = ap.parse_args()

    if not API_KEY:
        sys.exit("SET dulu SUMOPOD_API_KEY (atau OPENAI_API_KEY) — JANGAN hardcode di file.")
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # ── stream CSV besar -> kandidat (skor>=ambang) + sampel non-kandidat ──
    kandidat, non_kandidat = [], []
    with open(args.input, newline="") as f:
        for d in csv.DictReader(f):
            try:
                skor = float(d.get("skor_diplomasi") or 0)
            except ValueError:
                skor = 0.0
            rec = {"corpus_id": d.get("corpus_id"),
                   "text": (d.get("text") or ""),
                   "skor": skor, "tema": d.get("tema_dominan"), "thn": d.get("tahun")}
            (kandidat if skor >= args.ambang else non_kandidat).append(rec)

    random.seed(42)
    recall = random.sample(non_kandidat, min(args.recall_sample, len(non_kandidat)))
    for r in kandidat: r["mode"] = "kandidat"
    for r in recall:   r["mode"] = "recall_check"
    work = kandidat + recall
    print(f"kandidat(skor>={args.ambang}): {len(kandidat)} | non-kandidat: {len(non_kandidat)} "
          f"| recall-sample: {len(recall)} | total dinilai: {len(work)}")

    # ── resume ──
    done = load_done(args.output)
    new_file = not os.path.exists(args.output)
    fh = open(args.output, "a", newline="")
    w = csv.writer(fh)
    if new_file:
        w.writerow(["corpus_id", "mode", "skor_zeroshot", "tema_dominan", "tahun",
                    "is_diplomasi", "confidence", "alasan"])

    n_done = n_true = n_err = 0
    for i, r in enumerate(work):
        if r["corpus_id"] in done:
            continue
        is_dip, conf, alasan = judge(client, r["text"])
        w.writerow([r["corpus_id"], r["mode"], f"{r['skor']:.3f}", r["tema"], r["thn"],
                    is_dip, conf, alasan]); fh.flush()
        n_done += 1
        if is_dip is True: n_true += 1
        if is_dip is None: n_err += 1
        if n_done % 25 == 0:
            print(f"  ...{n_done} dinilai (true={n_true}, error={n_err})")
    fh.close()
    print(f"\n✔ Selesai. {n_done} baru dinilai. Output: {args.output}")

    # ── ringkasan + GERBANG VALIDASI (baca manual) ──
    rows = list(csv.DictReader(open(args.output, newline="")))
    kand = [x for x in rows if x["mode"] == "kandidat"]
    rc   = [x for x in rows if x["mode"] == "recall_check"]
    kand_true = [x for x in kand if x["is_diplomasi"] == "True"]
    rc_true   = [x for x in rc   if x["is_diplomasi"] == "True"]
    print("=" * 68)
    print(f"KANDIDAT diplomasi=True: {len(kand_true)}/{len(kand)} "
          f"({100*len(kand_true)/max(len(kand),1):.0f}%)")
    print(f"RECALL-CHECK (non-kandidat) diplomasi=True: {len(rc_true)}/{len(rc)}  "
          f"<-- IDEALNYA 0. Kalau >0 -> ada diplomasi ter-lewat, TURUNKAN --ambang & ulang.")
    print("=" * 68)
    print("GERBANG PRESISI — baca 30 acak diplomasi=True (setuju? target >=0.8):")
    random.seed(7)
    for x in random.sample(kand_true, min(30, len(kand_true))):
        print(f"  [{x['confidence']}] thn={x['tahun']} tema={x['tema_dominan']:<11} "
              f"alasan={x['alasan']}")
    if rc_true:
        print("\n⚠ RECALL-CHECK yang di-flag True (periksa — mungkin ter-lewat cascade):")
        for x in rc_true:
            print(f"  cid={x['corpus_id']} skor_zs={x['skor_zeroshot']} alasan={x['alasan']}")

if __name__ == "__main__":
    main()
