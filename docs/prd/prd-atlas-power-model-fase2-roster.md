# PRD: Fase 2 — Ekspansi Roster `Fort` untuk `/atlas`

**Status:** Draft desain, lanjutan `prd-atlas-power-model.md` §4 ("Fase 2, backlog, TIDAK dirancang detail di sana"). Ditulis setelah backfill `fort_id`/`dominion_status` Fase 1 selesai (58/101 `linimasa_events` terafiliasi ke 12 fort roster, lihat commit backfill terkait migrasi `011_add_linimasa_power_status.py`).
**Konteks:** Fase 1 sengaja membatasi `fort_id` ke 12 fort yang sudah punya titik di peta. Sesi backfill itu membuktikan **43/101 event tetap `fort_id=NULL`** — sebagian genuinely tak bisa diatribusikan ke satu fort (klaim Aceh umum, traktat multi-lokasi), tapi sebagian besar sisanya justru event dgn lokasi jelas & padat sitasi yang **belum punya titik di roster**. PRD ini merancang lokasi mana yang layak ditambah, urutan prioritas, dan apa yang masih perlu diriset sebelum eksekusi.

---

## 1. Temuan dari Backfill Fase 1 (Koreksi thd §4 PRD Sebelumnya)

Daftar backlog asli di `prd-atlas-power-model.md` §4 ternyata **terlalu luas** — sesi backfill menemukan 3 dari 6 item di daftar itu sebenarnya BISA diatribusikan ke fort roster yang sudah ada lewat *proxy geografis* (bukan titik baru), begitu diverifikasi dgn konteks lokal:

| Item backlog lama | Resolusi Fase 1 | Bukti |
|---|---|---|
| Tigablas Cottas & Doeapoeloeh-Kotta | **Diproxy ke Padang** | Konfirmasi user: Tigablas Kota = Kubung XIII (Solok modern), terhubung Padang lewat jalur dagang gunung — traktat 1741 & 1763 (id 93, 99) sudah terafiliasi Padang |
| Batang Kapas/Tello/Tarato/sisa Sapuluh Buah Bandar | **Sebagian diproxy** | "Sepuluh Pelabuhan" 1685 (id 66) → Painan (selatan Painan, teluk Batang Kapas); Troussang/Trusan 1755 (id 94) → Bayang (konfirmasi user: urutan wilayah Tarusan-Bayang-Salido-Painan, Troussang = Tarusan modern) |
| Sorkam, Pasariboe | **Sebagian diproxy** | Pasariboe-Baros 1731 (id 91) → Barus (treaty eksplisit sebut Barus sbg pihak) |

**Implikasi:** jangan asumsikan backlog lama masih akurat apa adanya — daftar di bawah ini (§2) sudah dikoreksi berdasar apa yg TERBUKTI masih butuh titik baru, bukan disalin ulang dari PRD lama.

---

## 2. Backlog yang Terverifikasi Masih Butuh Titik Baru

Dihitung dari 43 baris `fort_id=NULL` pasca-backfill Fase 1, dikelompokkan per entitas geografis (bukan status Aceh umum/traktat multi-fort yg memang di luar scope manapun — lihat §5 Non-Goals):

| Entitas | Jumlah event | Rentang tahun | id (linimasa_events, 1-indexed) | Catatan |
|---|---|---|---|---|
| **Pulau Nias** (7 negeri terpisah) | 7 | 1693 | 72, 74, 75, 76, 77, 78, 79 | Ekspedisi Sas (Jan-Mei 1693): Sillibo/Rarago-Bodo, Nay-Lambara, Malakerre-Telok Dalam, Hinako-Maros, Lahomi-Laoesa, Gunung Jarroe, Gomboe — 7 traktat aliansi anti-Aceh terpisah, densitas tertinggi di seluruh backlog |
| **Natal** | 2 | 1760 | 97, 98 | Episode Belanda→Inggris→Prancis→Belanda dlm satu tahun — CONTOH ASLI yang memicu `prd-atlas-power-model.md` §1 ("tak tergambar sama sekali") |
| **Singkil/Cinkel** | 2 | 1672, 1681 | 49, 59 | Traktat lepas-Aceh 1672 & pembaruan 1681 (radja pro-Aceh diusir, rumah dibakar) — 1 event lain (1707, id 86) sudah diproxy ke Barus |
| **Paoeh/Kotta-tengah** | 3 | 1680, 1682, 1716 | 55, 63, 88 | Konfederasi pedalaman pro-Aceh berulang (konfirmasi user sesi ini) — pola "tunduk-berontak-tunduk" 3x tercatat, relevan jg utk kerangka reframing "counter-monopoly" yg sedang digagas terpisah |
| **Sorkam/Kolang** | 1 | 1693 | 73 | VOC+Barus menengahi sengketa internal 2 kepala suku — event tunggal, prioritas rendah kecuali diriset bareng Singkil (geografis berdekatan) |

**Total: 15 event akan langsung terafiliasi kalau 5 entitas ini masuk roster** (dari 43 yang NULL, sisanya ~28 tetap NULL krn genuinely bukan soal 1 lokasi — lihat §5).

---

## 3. Pertanyaan Desain: Granularitas Nias

Nias adalah kasus khusus — 7 event, 7 negeri **berbeda secara eksplisit di sumber** (bukan 1 lokasi disebut 7x). Dua opsi:

**Opsi A — 1 titik "Nias" agregat.** Simpel, cepat riset (1 lat/lon), konsisten dgn skala 12 fort lain (masing-masing 1 pelabuhan). Kekurangan: 7 event beririsan di 1 titik peta, hilang resolusi geografis dalam-pulau (Sillibo di Gido, Lahomi-Laoesa, dst tersebar di berbagai sisi Nias).

**Opsi B — 7 titik per negeri.** Presisi penuh, tapi riset lat/lon 7 lokasi desa-tua abad-17 di Nias jauh lebih berat drpd 4 entitas lain digabung, dan berisiko coordinate-guessing kalau sumber sekunder modern minim (banyak nama negeri VOC-era sudah berubah/hilang di peta modern).

**Rekomendasi:** mulai Opsi A (1 titik Nias, mis. di lokasi pusat/paling terdokumentasi seperti Gido) untuk rilis awal, catat 7 event tetap granular di `text_asli`/tooltip per event meski garis dominion cuma 1 titik. Opsi B jadi Fase 3 kalau ada kebutuhan riil (mis. riset lanjut nemenukan koordinat individual). **Keputusan final: user/tim UI-UX.**

---

## 4. Perubahan yang Dibutuhkan

Berbeda dari Fase 1 (yang butuh migrasi skema + kolom baru), Fase 2 **tidak butuh migrasi baru** — `forts` table sudah generik (`name`, `latitude`, `longitude`, `color`, `port_type`, dst, lihat `backend/models.py` `Fort`). Yang dibutuhkan:

1. **Riset lat/lon** per entitas di §2 (dan turunan per-negeri kalau Opsi B Nias dipilih) — historis, bukan modern administratif serampangan (preseden: 12 fort existing dicocokkan ke lokasi pesisir riil, bukan pusat kecamatan modern).
2. **`backend/seed_data.py`**: tambah entri `FORTS_META` baru (pola sama 12 entri existing) — `name`, `latitude`, `longitude`, `color` (perlu skema warna baru atau reuse — lihat Pertanyaan Terbuka §6), `port_type`.
3. **Re-run `seed_linimasa_events.py`** setelah roster bertambah — 15 baris di §2 yang sekarang `fort_name=''` diisi nama baru, sisanya (~28 baris genuinely non-atribusi) tetap kosong.
4. **Tidak ada perubahan `backend/routers/forts.py`** — endpoint `/power-status` & `/diplomacy-markers` (`prd-atlas-power-model.md` §5) sudah generik per `fort_id`, otomatis mencakup fort baru begitu ada.

---

## 5. Non-Goals (Tetap di Luar Scope Fase 2 Ini)

- **Traktat multi-fort** (id 16, 34, 35, 41 — masing-masing menyebut 3-4 fort roster SEKALIGUS dalam satu dokumen) — perluasan roster tak menyelesaikan ini, butuh keputusan model data terpisah (mis. `fort_ids` array vs `fort_id` tunggal) — bukan scope PRD ini.
- **Klaim Aceh umum tanpa lokasi spesifik** (mis. id 1-4, 10, 20, 24-26, 29-32, 36-38 — subjeknya Sultan/Ratu Aceh sendiri, atau Perak di semenanjung Malaya) — tetap `fort_id=NULL` selamanya, bukan gap yang bisa ditutup roster.
- **Sillebar (id 39) & Majutta-Korintji (id 44)** — di luar wilayah inti pantai barat (Sillebar di bawah Bantam; Majutta-Korintji jauh ke pedalaman selatan Indrapoura), signifikansi historisnya beda kelas dgn 5 entitas §2 — evaluasi terpisah kalau ada kebutuhan spesifik, bukan bagian scope default.
- **Skema warna/visual `dominion_status`** — sudah jadi pertanyaan terbuka §7 PRD Fase 1, belum berubah di sini.
- **Implementasi kode** — PRD ini murni desain cakupan & prioritas riset, bukan migrasi/seed yang sudah dieksekusi.

---

## 6. Pertanyaan Terbuka

1. **Prioritas eksekusi** — riset lat/lon 5 entitas sekaligus, atau bertahap (mis. Natal dulu krn sudah jadi contoh eksplisit di PRD Fase 1, lalu Nias krn densitas tertinggi)?
2. **Granularitas Nias** — Opsi A (1 titik) atau B (7 titik), lihat §3.
3. **Sumber riset lat/lon** — peta VOC-era (Corpus Diplomaticum sendiri kadang sebut referensi geografis), atau gazetteer modern (mis. GLOBALISE project sudah punya sebagian koordinat pantai barat)?
4. **`port_type`** fort baru — Nias/Natal/Singkil/Paoeh/Sorkam semuanya `"departure"` (pola default existing), atau ada yang perlu `"both"`?
5. Apakah 5 entitas ini masuk **satu batch seed** atau dipisah per sesi riset (pola sama backfill Fase 1 yang sengaja bertahap per cluster)?
