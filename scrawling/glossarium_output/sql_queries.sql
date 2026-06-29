-- ============================================================
-- VOC Glossarium × Voyage Products — SQL Queries
-- Dialect: PostgreSQL 15+ (PostGIS optional, tidak dipakai di sini)
-- ============================================================


-- ── 1. Ekstrak semua istilah produk unik dari dataset voyage ────────────────
-- Gunakan ini untuk export JSON yang dipakai --products-json di scraper

WITH terms AS (
  SELECT DISTINCT TRIM(t) AS product
  FROM voyages,
       UNNEST(string_to_array(all_products, ' | ')) AS t(t)
  WHERE all_products IS NOT NULL
    AND TRIM(t) <> ''
)
SELECT product, COUNT(*) OVER () AS total_unique
FROM terms
ORDER BY product;


-- ── 2. Seed glossary dari CSV hasil scraping ────────────────────────────────
-- Jalankan di psql dengan \COPY atau via Python seed script.
-- Contoh dari psql:
--
-- \COPY commodity_glossary (term, term_display, variants, definition_nl)
-- FROM 'scrawling/glossarium_output/voc_glossarium.csv'
-- WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"',
--       NULL '', ENCODING 'UTF8');
--
-- Untuk kolom variants (TEXT[]), CSV harus format: "{varian1,varian2}"
-- Parser Python di seed_glossary.py menangani konversi ini.


-- ── 3. Coverage check: berapa % produk voyage sudah tercakup glossary ───────

WITH voyage_terms AS (
  SELECT DISTINCT LOWER(TRIM(t)) AS term
  FROM voyages,
       UNNEST(string_to_array(all_products, ' | ')) AS t(t)
  WHERE all_products IS NOT NULL
),
matched AS (
  SELECT vt.term,
         cg.definition_id IS NOT NULL AS has_id_def,
         cg.definition_nl IS NOT NULL AS has_nl_def
  FROM voyage_terms vt
  LEFT JOIN commodity_glossary cg
    ON vt.term = cg.term
    OR vt.term = ANY(cg.variants)   -- cek juga ejaan alternatif
)
SELECT
  COUNT(*)                                    AS total_terms,
  COUNT(*) FILTER (WHERE has_nl_def)          AS matched_nl,
  COUNT(*) FILTER (WHERE has_id_def)          AS matched_id,
  ROUND(
    COUNT(*) FILTER (WHERE has_nl_def)::numeric / COUNT(*) * 100, 1
  )                                           AS coverage_pct_nl,
  ROUND(
    COUNT(*) FILTER (WHERE has_id_def)::numeric / COUNT(*) * 100, 1
  )                                           AS coverage_pct_id
FROM matched;


-- ── 4. Query utama: voyage list dengan definisi per produk ──────────────────
-- Digunakan oleh API endpoint GET /api/glossary/products?terms=peper,kamfer

WITH input_terms AS (
  -- Ganti :terms dengan array dari query param
  SELECT UNNEST(string_to_array(:terms, ',')) AS raw_term
),
normalized AS (
  SELECT LOWER(TRIM(raw_term)) AS term FROM input_terms
),
resolved AS (
  SELECT
    n.term                AS queried_term,
    COALESCE(cg.term_display, n.term) AS term_display,
    cg.definition_id,
    cg.definition_nl,
    cg.category,
    cg.variants
  FROM normalized n
  LEFT JOIN commodity_glossary cg
    ON n.term = cg.term
    OR n.term = ANY(cg.variants)
)
SELECT *
FROM resolved
ORDER BY queried_term;


-- ── 5. Fuzzy matching untuk istilah yang tidak exact-match ──────────────────
-- pg_trgm diperlukan: CREATE EXTENSION IF NOT EXISTS pg_trgm;
-- Aktifkan dulu di DB: docker compose exec db psql -U vocuser -d vocdb -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

-- Cari istilah voyage yang belum punya definisi + saran closest match
WITH unmatched AS (
  SELECT DISTINCT LOWER(TRIM(t)) AS term
  FROM voyages,
       UNNEST(string_to_array(all_products, ' | ')) AS t(t)
  WHERE all_products IS NOT NULL
  EXCEPT
  SELECT cg.term FROM commodity_glossary cg
  EXCEPT
  SELECT LOWER(v) FROM commodity_glossary cg, UNNEST(cg.variants) AS v
),
candidates AS (
  SELECT
    u.term                           AS voyage_term,
    cg.term                          AS glossary_term,
    cg.definition_nl,
    SIMILARITY(u.term, cg.term)      AS sim_score
  FROM unmatched u
  CROSS JOIN LATERAL (
    SELECT cg2.term, cg2.definition_nl
    FROM commodity_glossary cg2
    WHERE cg2.term % u.term           -- trigram threshold (default 0.3)
    ORDER BY SIMILARITY(u.term, cg2.term) DESC
    LIMIT 1
  ) cg
)
SELECT *
FROM candidates
WHERE sim_score > 0.4
ORDER BY sim_score DESC;


-- ── 6. Top 30 produk paling sering + status definisi ───────────────────────
-- Untuk prioritas pengisian definition_id (terjemahan Indonesia) manual

WITH term_freq AS (
  SELECT
    LOWER(TRIM(t)) AS term,
    COUNT(*)       AS voyage_count
  FROM voyages,
       UNNEST(string_to_array(all_products, ' | ')) AS t(t)
  WHERE all_products IS NOT NULL
  GROUP BY 1
),
enriched AS (
  SELECT
    tf.term,
    tf.voyage_count,
    cg.definition_nl,
    cg.definition_id,
    cg.category,
    CASE
      WHEN cg.definition_id IS NOT NULL THEN 'lengkap'
      WHEN cg.definition_nl IS NOT NULL THEN 'perlu_terjemah'
      ELSE 'belum_ada'
    END AS status
  FROM term_freq tf
  LEFT JOIN commodity_glossary cg
    ON tf.term = cg.term OR tf.term = ANY(cg.variants)
)
SELECT *
FROM enriched
ORDER BY voyage_count DESC
LIMIT 30;


-- ── 7. Update definition_id secara batch (setelah terjemahan manual/GPT) ────
-- Jalankan ini setelah mengisi kolom definition_id via CSV import atau manual

UPDATE commodity_glossary
SET definition_id = updates.def_id
FROM (VALUES
  -- format: (term, terjemahan_indonesia)
  ('benzoë',         'Kemenyan; resin harum dari pohon Styrax benzoin, tumbuh di Sumatra'),
  ('kamfer',         'Kamper; zat kristal putih beraroma dari pohon Cinnamomum camphora'),
  ('peper',          'Lada hitam/putih; rempah utama perdagangan VOC dari Sumatra Barat'),
  ('goud',           'Emas; logam mulia, komoditas ekspor utama dari tambang Minangkabau'),
  ('foelie',         'Fuli; selaput biji pala (Myristica fragrans), rempah bernilai tinggi'),
  ('nootmuskaat',    'Pala; biji Myristica fragrans dari Maluku, monopoli VOC'),
  ('bindrotan',      'Rotan ikat; rotan jenis kecil untuk anyaman dan ikat'),
  ('tin',            'Timah putih; logam dari Bangka-Belitung, komoditas ekspor penting'),
  ('koper',          'Tembaga; logam merah, digunakan untuk peralatan dan senjata'),
  ('indigo',         'Nila; tanaman penghasil pewarna biru alami'),
  ('sapanhout',      'Kayu secang (Caesalpinia sappan); kayu merah untuk pewarna dan obat'),
  ('arak',           'Arak; minuman keras sulingan dari beras atau nira kelapa'),
  ('rijst',          'Beras; bahan makanan pokok, dibawa sebagai perbekalan kapal'),
  ('zeep',           'Sabun; produk manufaktur VOC dari minyak kelapa'),
  ('lood',           'Timbal; logam berat untuk peluru dan pemberat'),
  ('buskruit',       'Mesiu; bubuk senjata api (belerang + arang + kalium nitrat)'),
  ('garioffelnagel', 'Cengkih (Syzygium aromaticum); rempah dari Maluku, monopoli VOC'),
  ('kamferolie',     'Minyak kapur barus; minyak esensial dari kayu kamper Sumatra'),
  ('drakenbloed',    'Damar dragon (Daemonorops draco); resin merah untuk cat dan obat'),
  ('calaturshout',   'Kayu kalatur; kayu keras tropis Sumatra untuk furnitur dan bangunan'),
  ('kadjangmat',     'Kajang mat; tikar anyaman dari daun pandan atau rumbia'),
  ('sits',           'Kain cetis; kain katun bermotif cetak dari India (chintz)'),
  ('salempuris',     'Kain salempuri; kain katun putih halus dari India'),
  ('laken',          'Kain laken; kain wol tebal dari Eropa'),
  ('brandewijn',     'Brendi; minuman keras sulingan anggur dari Eropa'),
  ('spijker',        'Paku besi; bahan bangunan dan perkapalan'),
  ('ijzer',          'Besi; logam dasar untuk perkakas, senjata, dan bangunan kapal'),
  ('koffieboon',     'Biji kopi; tanaman introduksi VOC dari Arabia ke Jawa sekitar 1696'),
  ('poedersuiker',   'Gula bubuk; gula halus hasil penggilingan dari perkebunan Jawa')
) AS updates(term_key, def_id)
WHERE commodity_glossary.term = updates.term_key;
