# Audit DBA — Data Layer Westkust Routes (Juli 2026)

Tanggal: 2026-07-02 · Scope: voc_redis, voc_db (PostgreSQL/PostGIS) · Auditor: tim DBA (Claude Code)

---

## 1. Redis (voc_redis)

| Metrik | Nilai | Status |
|---|---|---|
| keyspace_hits | 38 | — |
| keyspace_misses | 10 | — |
| **Hit ratio** | **79,2%** (38/48) | OK untuk sampel kecil; pantau setelah trafik naik |
| used_memory_human | 1,35 MB (peak 1,83 MB) | Sangat rendah |
| maxmemory | 128 MB | ✅ sesuai target |
| maxmemory_policy | `allkeys-lru` | ✅ sesuai target |
| DBSIZE | 2 keys | — |
| evicted_keys / expired_keys | 0 / 0 | Belum pernah eviction |

Sample TTL (kedua key `voc:*`):

```
voc:voyages:limit=200&skip=0&year_from=1701  TTL 86119 s (~23,9 jam)
voc:voyages:limit=200&skip=0                 TTL 86143 s (~23,9 jam)
```

TTL efektif 24 jam. Konfigurasi memori & eviction sudah sesuai spesifikasi (allkeys-lru, 128 MB) — tidak ada tindakan.

## 2. PostgreSQL — Index Tabel `voyages` & `forts`

Baseline: `voyages` 4.738 baris (heap 1.968 kB, total + index 2.808 kB); `forts` kecil (pkey 16 kB).

Index terpasang di `voyages` (sebelum audit — **tidak ada yang perlu ditambah**):

| Index | Kolom | Catatan |
|---|---|---|
| voyages_pkey | id | — |
| idx_voyages_direction_year | (direction, year) | Composite; melayani query panas (a) |
| idx_voyages_year | year | Melayani ORDER BY year |
| ix_voyages_year | year | ⚠️ **Duplikat** idx_voyages_year |
| ix_voyages_direction | direction | ⚠️ Redundan (prefix composite) |
| ix_voyages_id | id | ⚠️ Duplikat pkey |
| ix_voyages_origin_id | origin_id | ✅ FK terindeks |
| ix_voyages_destination_id | destination_id | ✅ FK terindeks |
| ix_voyages_voyage_ref | voyage_ref (UNIQUE) | — |

Filter (year, direction) dan FK origin_id/destination_id **sudah terlayani index** → migration `003_add_voyage_indexes.py` **tidak diperlukan**.

### 2.1 EXPLAIN ANALYZE — Query (a) filter year + direction

```sql
SELECT * FROM voyages WHERE year>=1700 AND year<=1750 AND direction='outbound'
ORDER BY year DESC LIMIT 200;
```

**Sebelum ANALYZE** (statistik planner belum pernah di-refresh — `last_analyze` kosong):

```
Limit → Index Scan Backward using idx_voyages_year
  Index Cond: (year >= 1700 AND year <= 1750)
  Filter: direction = 'outbound'   → Rows Removed by Filter: 385
Execution Time: 0.623 ms
```

**Sesudah `ANALYZE voyages;`** — planner beralih ke composite index:

```
Limit → Index Scan Backward using idx_voyages_direction_year
  Index Cond: (direction = 'outbound' AND year >= 1700 AND year <= 1750)
  (tanpa Filter, 0 rows removed)
Execution Time: 0.136 ms   (0.623 ms → 0.136 ms, ~4,6× lebih cepat)
```

### 2.2 EXPLAIN ANALYZE — Query (b) agregasi routes

```sql
SELECT origin_name_raw, destination_name_raw, count(id), coalesce(sum(total_gulden),0)
FROM voyages GROUP BY 1,2;
```

```
Sebelum : HashAggregate ← Seq Scan (est. 5322 rows vs aktual 4738) — 13.285 ms
Sesudah : HashAggregate ← Seq Scan (est. 4738 = aktual)            —  1.604 ms
```

Seq Scan **memang optimal** untuk agregasi full-table 4.738 baris; index tidak akan membantu di ukuran ini. Perbaikan timing berasal dari statistik segar + cache hangat.

Catatan data: kolom `direction` berisi `inbound` (177), `outbound` (181), `transit` (4.380) — huruf kecil, berbeda dari dokumentasi CLAUDE.md ("Outbound"/"Inbound").

## 3. Temuan Kritis — Chain Alembic Putus

`docker compose exec -T backend alembic current` / `heads` **gagal**: `KeyError: '002'`.

- `002_add_amh_images.py` → `revision = "002_amh_images"`
- `003_add_commodity_glossary.py` → `down_revision = '002'` ← **tidak ada revision bernama `002`**
- `alembic_version` di DB = `002_amh_images`; tabel `commodity_glossary` sudah ada di DB (dibuat di luar alembic).

Akibat: **semua `alembic upgrade head` ke depan akan gagal** sampai chain diperbaiki. Karena audit ini tidak menambah migration, perbaikan tidak dilakukan di kartu ini (di luar scope), tetapi wajib ditindaklanjuti.

## 4. Tindakan yang Dilakukan

1. `ANALYZE voyages; ANALYZE forts;` — statistik planner sebelumnya belum pernah dibuat (`last_analyze`/`last_autoanalyze` kosong). Efek langsung: query (a) pindah ke composite index, 4,6× lebih cepat.
2. Verifikasi suite: `pytest -q` → **151 passed, 41 skipped** (hijau).
3. Tidak ada migration index baru (semua sudah terlayani).

## 5. Rekomendasi Lanjut

1. **Perbaiki chain Alembic** (prioritas tinggi): ubah `down_revision = '002'` → `'002_amh_images'` di `003_add_commodity_glossary.py`, lalu `alembic stamp 003` (tabel sudah ada di DB). Tanpa ini migration berikutnya mustahil.
2. **Drop index duplikat** via migration setelah chain sehat: `ix_voyages_year` (duplikat `idx_voyages_year`), `ix_voyages_id` (duplikat pkey), `ix_voyages_direction` (prefix `idx_voyages_direction_year`). Hemat write-amplification saat seed ulang.
3. **Autovacuum/autoanalyze**: pastikan berjalan (saat audit `last_autoanalyze` kosong padahal DB sudah lama hidup). Minimal jadwalkan `ANALYZE` setelah setiap `seed_data.py`.
4. **Redis TTL**: 24 jam wajar untuk data historis statis; pertimbangkan turunkan ke 1–6 jam untuk endpoint agregasi jika data di-reseed sering. Pantau hit ratio setelah trafik produksi (target > 90%).
5. **Konsistensi `direction`**: sinkronkan dokumentasi (Outbound/Inbound) dengan nilai aktual DB (`inbound/outbound/transit`) agar query/filters tidak silent-miss.
