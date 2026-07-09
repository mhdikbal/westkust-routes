# Runbook — Deploy Sankey Tema-Korpus ke Production (salido.my.id)

**Disusun:** 2026-07-09 · **Fitur:** SNK-1..5 (endpoint `research` + halaman `/riset/tema`)
**Target URL prod:** `https://salido.my.id/atlas/riset/tema`

---

## 0. Kondisi terverifikasi (2026-07-09)

| Hal | Status |
|---|---|
| Repo VPS | `/home/ubuntu/westkust-routes` (deploy = git pull + docker compose build) |
| Container prod | voc_db (10h), **voc_redis Up 2 days healthy**, voc_backend/frontend Up 24h (build LAMA), voc_nginx |
| **Redis** | ✅ **SUDAH jalan di prod** (ADR-001). `REDIS_URL` sudah di-wire. Tak perlu ditambah lagi. |
| Backend prod | build lama → `/api/research/*` = 404, `/atlas/riset/tema` = 404 |
| Sankey code | committed+pushed branch `feat/sankey-tema-korpus`; `data/research/korpus_tema_slim.csv` (1005 baris) ikut di repo |
| Routing prod | nginx `/atlas/` → Docker 127.0.0.1:8084; route Django `riset/tema/` otomatis jadi `/atlas/riset/tema`. Fetch JS ke `/api/research/*` → nginx `/api/` → backend (absolut, tak kena sub_filter) |

**Isolasi risiko:** `research_theme_rows` tabel BARU & mandiri (tak ada FK ke forts/voyages) → deploy tak menyentuh data daghregister/voyage yang sudah live.

---

## 1. [LOKAL/GitHub — saya bisa] Merge & push
```bash
# opsi A (review): buka PR feat/sankey-tema-korpus -> main, merge di GitHub
# opsi B (langsung):
git checkout main && git merge --no-ff feat/sankey-tema-korpus && git push origin main
```

## 2. [VPS — butuh SSH, Anda jalankan] Deploy code
```bash
ssh westkust-prod
cd /home/ubuntu/westkust-routes
git pull origin main
docker compose up -d --build backend frontend
# create_all() saat start auto-buat tabel research_theme_rows
```

## 3. [VPS] Sinkron alembic (hindari gotcha create_all vs 007)
`create_all()` sudah membuat tabel, jadi JANGAN `alembic upgrade` (akan gagal "table exists" — persis insiden daghregister). Cukup stamp:
```bash
docker compose exec backend alembic stamp head
docker compose exec backend alembic current   # verifikasi = 007
```

## 4. [VPS] Seed 1005 baris ke DB prod
Idempotent by `corpus_id`; baca `data/research/korpus_tema_slim.csv` yang ikut ter-pull (bukan replikasi name-keyed spt daghregister — tabel ini mandiri):
```bash
docker compose exec backend python seed_research_tema.py
# verifikasi granular (WAJIB, pelajaran feedback_sisir_semua_titik_pemakaian):
docker compose exec db psql -U vocuser -d vocdb -t -c \
 "SELECT count(*) total, count(*) filter(where corpus_asal='daghregister') dr, \
         count(*) filter(where corpus_asal='globalise') glob, \
         count(*) filter(where low_confidence) low FROM research_theme_rows;"
# harus: total=1005 | dr=470 | glob=535 | low=251
```

## 5. Verifikasi live (saya bisa curl publik)
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://salido.my.id/api/research/sankey-tema/triples   # 200
curl -s https://salido.my.id/api/research/sankey-tema/triples | python3 -c "import sys,json;d=json.load(sys.stdin);print('triples',len(d['triples']),'total',d['meta']['total'])"  # 512 / 1005
curl -s -o /dev/null -w "%{http_code}\n" https://salido.my.id/atlas/riset/tema/                  # 200
```
Lalu browser: `https://salido.my.id/atlas/riset/tema` → Sankey render, drill-down klik → teks. Cek `docker compose logs backend --tail 30` bersih.

## 6. Redis / caching (opsional — redis SUDAH ada)
Redis prod aktif tapi **endpoint research belum pakai cache** (data kecil, ~188ms — tak wajib). Bila mau konsisten ADR-001 (read-heavy cache-aside):
- Tambah dekorator cache di `routers/research.py` (pola sama `voyages.py` yg sudah pakai cache), key by `year_from/year_to`, invalidate saat re-seed.
- **Saya bisa siapkan** patch ini sebelum deploy bila Anda mau.

## 7. Rollback
```bash
# di VPS:
git checkout <commit-sebelum-merge> && docker compose up -d --build backend frontend
# research_theme_rows boleh ditinggal (mandiri, tak ganggu); atau DROP TABLE bila mau bersih
```
Downtime rebuild ~1–5 menit (pola daghregister). `restart: always` menjaga container.

---

## Pembagian kerja
- **Saya (aman, non-prod):** step 1 (merge+push), siapkan patch caching (step 6) bila diminta, verifikasi publik (step 5).
- **Anda (akses VPS, di-gate auto-mode):** step 2–4 (git pull + build + stamp + seed di VPS) — saya siapkan perintah persisnya di atas, tinggal paste via SSH.

**Urutan aman:** 1 → 2 → 3 → 4 → 5. Jangan seed (4) sebelum stamp (3) & build (2).
