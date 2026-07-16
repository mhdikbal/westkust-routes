# PRD: Redesign Kronik Pantai Barat — Anti AI Slop

**Status:** Sprint 1, 2, 3 selesai (Sprint 1&2 di-commit `1d52078`..`f8ec1e0`; Sprint 3 P3.1-P3.4 selesai 2026-07-16, siap commit). Fase P1 lama dibubarkan (selesai/superseded, lihat §5). Sprint 4 (P3.5 footer 5-kolom + motion P2) menanti -- lihat §8.
**Sumber:** `docs/audit-ux-ui-ai-slop-salido.md` (audit UX/UI senior manager) + temuan susulan dari `docs/audit-redesign-ruang-kosong-django-tailwind.md` (lihat §2b).
**Target:** `/linimasa` di repo ini (Django template + vanilla JS + SVG)
**Scope:** P0 + P1 + P2 (full scope sesuai audit §16) + item susulan §2b

**Sudah dikerjakan di luar sprint (fix bug, bukan keputusan desain):**
- Path gambar panggung peta (`#chrMap`) menunjuk ke `amh-5147-na.jpg` yang filenya sudah tidak ada (peninggalan folder `astro-linimasa` yang dihapus) — diganti ke `map_app/img/peta-untukruangtengah.png` (aset engraving resmi, sama dengan yang dipakai desainer di `Designer-fix.png`). Overlay opacity/filter (`opacity:.5; grayscale(60%); brightness(.7)`) **belum diubah** — itu keputusan P1.6, lihat §2b.

---

## 1. Konteks

Dokumen audit (`audit-ux-ui-slop-salido.md`) mengidentifikasi bahwa tampilan Kronik Salido terkesan "AI slop" — banyak elemen visual menarik secara individual, tapi tanpa hierarki, kurasi, dan keputusan desain yang tegas. Audit ditujukan untuk linimasa.html di repo ini (konfirmasi user), meski disebut "AstroJS" ( referensi ke proyek salido-web yang terpisah).

**Gap platform:** Spec desain asli menulis AstroJS + Flask. Repo ini Django + vanilla JS. Keputusan: adopsi penuh filosofi visual, tipografi, palet, dan prinsip aksesibilitas — terjemahkan ke stack Django yang sudah ada.

**Yang sudah cocok tanpa perubahan** (dari PRD sebelumnya §3):
- Tipografi: EB Garamond + Space Grotesk sudah digunakan
- Model kepercayaan sumber: `confidence_flag`, `text_asli` wajib
- Traktat Painan sebagai klimaks naratif
- SSR fallback untuk konten utama

---

## 2. Pemetaan Audit → Kode Saat Ini

| Temuan Audit | Lokasi di Kode | Masalah Spesifik |
|---|---|---|
| §4 Peta terlalu sibuk | `linimasa.html:1006-1084` (SVG stage build) | 14 port selalu terlihat, semua orbit + VOC lines + ripples + kompas + rhumb lines + hatching + ridges + ships muncul bersamaan |
| §5 Gaya kapal tidak konsisten | `linimasa.html:1069-1075` | Dua kapal SVG — satu `.chr-ship` (animasi), satu `.chr-ship2` (statis, scale .55) — meski path sama, opacity/ukuran beda terasa seperti gaya berbeda |
| §6 Sidebar kiri seperti admin | `linimasa.html:278-288` (`.chr-era`) | Dot `::before` menyerupai radio button; era aktif cuma beda warna dot + tampilkan summary |
| §7 Panel kanan generic drawer | `linimasa.html:1118-1146` (`renderPanel()`) | Struktur: live indicator → tahun besar → judul → badges → meta → quote → src → actions. Terasa seperti detail drawer dashboard |
| §8 Tipografi belum disutradarai | CSS `:root` + `.chr-*` classes | Sudah pakai 2 font, tapi treatment belum disiplin — tahun di panel pakai mono, di scrubber pakai mono, di card pakai mono — tidak ada hierarki ukuran yang jelas |
| §9 Garis rute = efek, bukan informasi | `linimasa.html:1064-1066` | Orbit emas (semua port → Aceh) + VOC lines (Batavia → Padang → 8 port) — semua muncul tanpa konteks event aktif |
| §10 Label bertabrakan | `linimasa.html:1078-1084` | 14 label port selalu tampil — cluster selatan (Tiku–Inderapura) sangat rapat |
| §11 Background/data tidak terpisah | `linimasa.html:294-298` (`.chr-stage::before`) | Static image + scrim gelap — tidak ada pemisahan layer atmosfer/geografi/peristiwa |
| §12 Tidak ada focal point stabil | `setActive()` di `linimasa.html:1152-1164` | Perhatian berpindah ke 7 tempat — tidak ada urutan visual yang disutradarai |
| §13 Proporsi mekanis | `linimasa.html:265-268` (grid) | `minmax(200px,19%) 1fr minmax(300px,29%)` — garis pemisah keras, panel statis |
| §14 Microcopy data mentah | `linimasa.html:1136` | `vol. CD1 · hlm. 47 (19–20) · unverified` — campur bahasa, istilah teknis |

---

## 2b. Temuan Susulan — Design Critique atas `Designer-fix.png`

Sesi critique terpisah membandingkan mockup final desainer (`docs/Designer-fix.png`) terhadap audit ruang kosong. Dua temuan tervalidasi terhadap kode saat ini, dua lainnya sudah tercakup rencana P0/P1 yang ada:

| Temuan | Lokasi di Kode | Status | Item Baru |
|---|---|---|---|
| Bar statistik (tiles) murni display, tidak ada afordansi klik/filter — padahal ini akar kesan "dashboard BI" | `linimasa.html:149-154` (`.tiles`, `.tile`), markup `:601-608` | Belum ada di P0/P1 manapun | **P0.8** (baru, lihat §4) |
| Kapal engraving pada panggung peta berisiko tenggelam overlay gelap | `linimasa.html:634-637` (`#chrMap` inline style `opacity:.5; grayscale(60%); brightness(.7)`) | Sudah tercakup **P1.6** — tapi asumsi lama P1.6 memakai gambar peta lama yang filenya hilang; sekarang aset benar (`peta-untukruangtengah.png`, 3 kapal terlihat jelas di sumber), overlay harus diverifikasi ulang supaya tidak menutupi kapal | Update catatan implementasi P1.6, bukan item baru |
| Risiko konflik tinggi viewport bila footer sumber (5/2-kolom) dan timeline scrubber tampil bersamaan di satu state | `linimasa.html:644-652` (`.chr-scrub--full`, mode peta) vs `:655-801` (`#listView` + `.sources-footer`, mode daftar) | **Sudah aman** — footer ada di dalam `#listView` yang di-`display:none` saat mode peta aktif (`.js #listView{display:none}` di `:307`); scrubber cuma tampil di mode peta. Tidak ada konflik di kode saat ini. | Tidak perlu perubahan — catat sebagai **constraint**: jangan pernah render `.sources-footer` dan `.chr-scrub--full` di viewport yang sama saat P1.7 (responsive) dikerjakan |
| Kontras kutipan sumber primer (italic, kecil, di atas background gelap) belum diverifikasi WCAG AA | `linimasa.html` — cari `.chr-quote` / `.quote` | Belum diverifikasi | Ditambahkan ke checklist verifikasi Sprint 2 (§8) |

**Koreksi ground-truth saat mulai eksekusi Sprint 1 (2026-07-16):** Audit asli (dan draft P0/P1 di atas) menyebut kompas, rhumb lines, hatching, ridge, coastline vector, ripple, dan dua kapal (`.chr-ship`/`.chr-ship2`) sebagai elemen yang perlu diredupkan/disederhanakan. Penelusuran kode saat ini menunjukkan **CSS untuk semua kelas itu (`.chr-compass`, `.chr-rhumb`, `.chr-ridge`, `.chr-hatch`, `.chr-coast`, `.chr-isle`, `.ripple`, `.chr-ship`, `.chr-ship2`, `.orbit`, `.vocline`) tidak pernah dipasang ke elemen HTML manapun** — tidak ada di markup statis maupun di-generate JS (satu-satunya builder overlay adalah `drawRoutes()` di `:964-1011`, yang memakai class `route-voc`/`route-orbit`, bukan `.vocline`/`.orbit`). Kesimpulan: panggung peta sudah disederhanakan sebelumnya dari sistem SVG schematic penuh menjadi gambar raster (`#chrMap`) + dot pelabuhan + garis rute JS — CSS lama untuk sistem SVG schematic itu jadi *dead code*. Dampak ke scope:

- **P0.2 dianggap tidak berlaku** — tidak ada elemen kapal di overlay interaktif untuk distandarisasi (kapal cuma ada sebagai bagian gambar statis `peta-untukruangtengah.png`)
- **P0.5 bagian kompas/rhumb/ridge/hatch dianggap tidak berlaku** — tidak pernah dirender, tidak perlu diredupkan
- **P0.1 & P0.6 tetap valid dan jadi prioritas nyata**: 14 garis `route-voc`/`route-orbit` selalu tampil statis (opacity .3–.35) tanpa filter terhadap event aktif — ini persis masalah audit §9 ("garis rute = efek, bukan informasi") dan belum diperbaiki. Port dot aktif/related/dormant **sudah** diimplementasi di `setActive()` (`:1138-1172`) — verifikasi saja, bukan build baru.
- Rekomendasi: hapus CSS dead code (`.chr-compass` dkk.) di sprint pembersihan terpisah agar tidak membingungkan kontributor berikutnya — di luar scope P0/P1 saat ini.

**Bug tambahan ditemukan saat verifikasi Sprint 1 (screenshot Playwright):** `#chrMapWrap` dikunci `aspect-ratio:3/2` (`linimasa.html:633`) padahal parent-nya (`.chr-stage`, flex column yang mengisi tinggi grid `100dvh`) lebih tinggi dari rasio itu — menyisakan celah kosong di bawah gambar peta yang menampakkan `.chr-stage::before` (background `linimasa-hero.jpg`, gambar berbeda) tembus, menciptakan efek "dua peta bertumpuk". **Sudah diperbaiki**: `aspect-ratio:3/2` diganti `flex:1;min-height:0` supaya gambar mengisi penuh panggung tanpa celah. Diverifikasi via screenshot Playwright — kapal dan kompas dari `peta-untukruangtengah.png` sekarang terlihat penuh, bukan cuma sepotong.

---

## 2c. Arahan Desain Langsung User — Peta Polos + Thumbnail Dokumen Tulisan Tangan (2026-07-16)

User (bukan dari dokumen audit) memberi arahan langsung setelah melihat panggung peta jalan: peta terlalu ramai dengan tulisan/garis, dan warnanya sengaja diredupkan padahal aslinya berwarna. Ini **membalik sebagian keputusan P0.1** yang baru dikerjakan Sprint 1 — dicatat di sini supaya tidak ada yang bingung kenapa `ROUTE_LINES`/filter aktif-sekunder-dorman hilang lagi dari histori commit.

**Perubahan:**
- Label nama pelabuhan (`.lbl` span, 14 kota) **dihapus total** dari overlay peta — port ditandai titik polos saja (`.core`/`.halo`), tanpa teks. Keputusan user: lokasi cukup ditunjukkan lewat panel kanan + caption era, bukan tulisan di atas gambar.
- Garis rute `route-voc`/`route-orbit` (fungsi `drawRoutes()`, array `ROUTE_LINES`, dan logic active/secondary/dormant di `setActive()` yang baru dibuat P0.1) **dihapus seluruhnya**, bukan cuma diredupkan. Peta sekarang murni ilustrasi + titik pelabuhan, tanpa elemen garis.
- `#chrMap` inline style `opacity:.5; filter:grayscale(60%) brightness(.7)` **dihapus** — gambar `peta-untukruangtengah.png` tampil warna asli (opacity 1, tanpa filter).
- **Item baru:** thumbnail dokumen di panel `Sumber Primer` — perkamen `docs/traktat.png` (dicopy ke `static/map_app/img/traktat.png`) dengan kutipan pembuka `ev.text_asli` (≤90 karakter, kutipan arsip nyata Dagh-register/Corpus Diplomaticum, bukan teks placeholder) yang dirender pakai font tulisan-tangan custom `docs/Yasraf-Amir-Piliang.otf` (dicopy ke `static/map_app/fonts/`, didaftarkan via `@font-face`). Berlaku utk **semua 101 event** (bukan cuma Traktat Painan) — sesuai arahan user, supaya jadi satu sistem ilustrasi konsisten, bukan dekorasi sekali pakai. Kutipan lengkap tetap ada di `.chr-quote` yang mudah dibaca; thumbnail murni penguat visual (`aria-hidden="true"`, tidak duplikat ke screen reader).

**Dampak ke item PRD sebelumnya:**
- P0.1 (audit §9, "garis rute = efek bukan informasi") — **selesai dengan cara berbeda dari rencana**: bukan diberi hierarki aktif/sekunder/dorman, tapi dihapus total atas keputusan desain user. Tidak perlu dikerjakan ulang.
- P1.6 (pisahkan layer atmosfer/geografi/peristiwa, opacity overlay) — **berubah arah**: overlay dihapus total (bukan diturunkan sebagian), karena user minta warna asli. Item P1.6 dianggap selesai dengan solusi paling sederhana (tidak ada overlay).

**File:** `linimasa.html` — hapus `.lbl` span & CSS terkait, hapus `drawRoutes()`/`ROUTE_LINES`, ubah inline style `#chrMap`, tambah `@font-face` + `.chr-doc-thumb` CSS + markup di `renderPanel()` + helper `openingWords()`

---

## 2d. Thumbnail Dokumen Dihapus + Perbaikan Ukuran Peta (2026-07-16, susulan §2c)

User menilai thumbnail `traktat.png` (baru ditambahkan §2c) **terlalu ramai** — dicabut lagi. Sekaligus melaporkan dua masalah nyata pada ukuran panggung peta yang ternyata **berhubungan sebab-akibat**, ditemukan lewat pengukuran DOM langsung (bukan tebakan):

**Diagnosis:** `#chrMapWrap` dari Sprint 1 pakai `flex:1` (mengisi penuh tinggi grid `.chronicle`, `min-height:100dvh`) — di viewport 1440×900 kotaknya jadi **748×1021px (rasio ~0.73, portrait)**, padahal `peta-untukruangtengah.png` asli **1536×1024px (rasio 1.5, landscape 3:2)**. `object-fit:cover` pada rasio kotak yang salah ini meng-crop/zoom parah secara horizontal — dan karena posisi titik pelabuhan (`PORT_PCT`, persentase tetap terhadap kotak) dikalibrasi utk rasio 3:2, titik-titik itu jadi bergeser dari lokasi geografis yang benar begitu rasio kotak berubah ("bocor" yang dilaporkan user — cek DOM nunjukkan `<span class="core">` port Aceh nongkrong di posisi yang tidak konsisten dgn crop gambar). Masalah ini laten sejak Sprint 1, baru kentara sekarang karena user memperhatikan detail posisi titik.

**Perbaikan:**
- `#chrMapWrap`: `flex:1` → `aspect-ratio:3/2` (rasio asli gambar, persis) — dot pelabuhan otomatis akurat lagi krn kotak kembali ke rasio yang sama dgn saat `PORT_PCT` dikalibrasi
- `.chr-stage`: tambah `justify-content:center` supaya kotak peta (skrg berukuran tetap, bukan mengisi penuh) berada di tengah scara vertikal
- `.chr-stage::before` (background `linimasa-hero.jpg` yang bleed di belakang, sisa dari rencana lama "layer atmosfer" P1.6) **dihapus total** — kalau tidak, sisa ruang vertikal di atas/bawah kotak peta yang sekarang lebih pendek akan menampakkan gambar hero yang beda, mengulang bug "dua peta bertumpuk" dari Sprint 1. Sisa ruang sekarang jadi letterbox solid `#0b1c1e` (warna latar `.chr-stage` yang sudah ada) — matte rapi, bukan gambar kedua
- `.chr-stage.climax::before`/`.chr-stage[data-era]::before` (variasi opacity utk climax Traktat Painan) ikut dihapus — sudah tidak relevan tanpa `::before`
- Thumbnail `.chr-doc-thumb`/`traktat.png`/font `Yasraf Piliang` **dihapus dari rendering** (markup, CSS, helper `openingWords()`, variabel `docExcerpt`) — aset font & gambar dibiarkan ada di `static/` (tidak dihapus filenya), cuma tidak dipakai. Kalau nanti mau dipakai lagi di tempat lain, tidak perlu upload ulang.

**Verifikasi Playwright:** `wrapAspect` terukur `1.500`, persis `3/2`; dot Aceh terkonfirmasi berada dalam batas kotak (`acehDotVisibleWithinWrap: true`); `.chr-doc-thumb` terkonfirmasi tidak ada lagi di DOM. Screenshot menunjukkan peta utuh, dua kapal & kompas terlihat, letterbox atas-bawah solid tanpa gambar kedua bocor.

**File:** `linimasa.html` — CSS `#chrMapWrap` (inline style), `.chr-stage` (`justify-content:center`, hapus `::before` & variannya), hapus markup/CSS/JS `.chr-doc-thumb`

**Susulan (2026-07-16, user hard-restart tapi ruang kosong masih ada):** perbaikan §2d di atas menghilangkan bug crop/dot-salah-tempat, tapi menyisakan letterbox solid ~200px di atas+bawah peta pada 1440×900 (diukur via Playwright: `leftoverTop`/`leftoverBottom` ±199px tiap sisi) — karena `.chronicle{min-height:100dvh}` (permintaan user **lain, lebih lama**: "lini masa full width sebagai hero, halaman penuh seperti foto di awal") memaksa section setinggi viewport penuh, padahal peta rasio 3:2 di lebar kolom tengah cuma butuh ~500px. Dua requirement ini bentrok. **Diprioritaskan menghilangkan ruang kosong** (sejalan dgn prinsip inti proyek §3 di bawah) — `min-height:100dvh` dihapus dari `.chronicle`, tinggi section sekarang mengikuti konten kolom terpanjang secara alami (bukan dipaksa 1 layar).

**Hasil terukur:** leftover per sisi turun dari ±199px → ±83px (1440×900), ±0px (1920×1080, peta pas persis dgn tinggi sidebar/panel), ±107px (1366×768). Tidak nol sempurna di semua ukuran (kolom sidebar/panel kadang lebih tinggi dari peta secara alami), tapi jauh berkurang dan terlihat proporsional, bukan area kosong yang mencolok. Kalau butuh nol mutlak di semua ukuran, perlu redesain proporsi lebar kolom grid supaya rasionya pas dgn 3:2 peta — di luar scope perbaikan cepat ini.

**File:** `linimasa.html` — CSS `.chronicle` (hapus `min-height:100dvh`)

---

## 2e. Tipografi Disamakan dengan `salido.my.id` (2026-07-17)

User melaporkan font `/linimasa` terasa sangat kecil, minta dicek terhadap font di halaman utama `salido.my.id`. **Temuan penting saat verifikasi:** `salido.my.id` bukan bagian dari repo Django ini — itu proyek Astro terpisah (`salido-web`, lihat memori server production). Diambil langsung dari HTML/CSS live (`curl` ke domain produksi):

| | `salido.my.id` (live, Astro) | `/linimasa` (sebelum) |
|---|---|---|
| Font serif/heading | `"EB Garamond"` | `"Cormorant Garamond"` |
| Font UI/sans | `"Space Grotesk"` | `"IBM Plex Sans"` |
| Body base size | `1.0625rem` (~17px) | 16px (default, tak diset) |
| Body line-height | `1.8` | `1.55` |

Dua sistem font yang sama sekali berbeda antara halaman utama situs dan `/linimasa` — bukan cuma soal ukuran. User memilih **disamakan penuh** (opsi lain yang ditawarkan: pertahankan font lama, cuma naikkan ukuran — ditolak).

**Implementasi:**
- Google Fonts `<link>`: `Cormorant+Garamond` + `IBM+Plex+Sans` → `EB+Garamond` + `Space+Grotesk`
- CSS vars: `--serif`, `--sans`, `--mono` diarahkan ke font baru
- **Root fix penting:** `html{font-size:106.25%}` (≈17px) ditambahkan — bukan `body{font-size}`. `rem` dihitung relatif ke `<html>`, bukan `<body>`; sempat salah taruh di `body` dulu (tidak berpengaruh ke elemen manapun karena semua ukuran di file ini pakai `rem`), dikoreksi sebelum rebuild
- `body{line-height:1.55→1.8}` menyamakan kelonggaran baris dgn situs utama
- Elemen bacaan yang jauh di bawah baseline dinaikkan manual (di atas efek scale 106.25% otomatis): `.chr-quote` .93rem→1.1rem, `.chr-meta-item` .8rem→.92rem, `.chr-era .sum` .76rem→.88rem, `.chr-source-name`/`.chr-source-page` .84rem→.94rem. Label kecil huruf-kapital (`.evt-counter`, `.chr-source-header`, `.chr-status` — pola "eyebrow" yang salido.my.id sendiri pakai di `.eyebrow{font-size:.65rem}`) **tidak diubah**, itu gaya label yang disengaja kecil, bukan teks bacaan

**Verifikasi Playwright:** `rootFontSize` terukur `17px`, `bodyFont`/`quoteFontFamily`/`titleFontFamily` semua terkonfirmasi `"Space Grotesk"`/`"EB Garamond"`, `.chr-quote` terukur `18.7px` (dari ~14.9px sebelumnya). Screenshot tampilan peta dan tampilan daftar keduanya dicek.

**Observasi sampingan (belum diperbaiki, di luar scope task ini):** toolbar (P3.1) dan timeline scrubber+era-band (P3.4) adalah sibling dari `.chronicle`, bukan child-nya — jadi tetap terlihat saat pindah ke mode Daftar (`.js.show-list .chronicle{display:none}` tidak menyembunyikan mereka). Kemungkinan sudah begitu sejak scrubber pertama dibuat, bukan regresi dari sesi ini. Tidak dieksekusi karena user tidak memintanya kali ini.

**File:** `linimasa.html` — `<link>` Google Fonts, CSS vars `--serif`/`--sans`/`--mono`, `html{font-size}`, `body{line-height}`, `.chr-quote`/`.chr-meta-item`/`.chr-era .sum`/`.chr-source-name`/`.chr-source-page`

---

## 2f. Empat Perbaikan Susulan (2026-07-17): Ruang Kosong Kembali, Kebocoran Dot, Toolbar/Scrubber, Ikon Hilang

Efek samping dari §2e (tipografi lebih besar) + tindak lanjut observasi sampingan yang dicatat di §2e.

**1. Ruang kosong peta kembali muncul.** Root cause: setelah `min-height:100dvh` dihapus dari `.chronicle` (§2d), section jadi *auto-height* mengikuti kolom terpanjang — sebelum §2e itu cukup kecil (~664px di 1440×900), tapi setelah font/line-height dibesarkan, panel kanan (badge+meta-row+quote lebih besar) jadi kolom terpanjang alami di **836px**, dan `#chrNav`/`#chrPanel` yang didesain `overflow-y:auto` untuk scroll internal jadi tidak pernah aktif (tak ada batas tinggi utk discroll), keduanya melar penuh, ikut menyeret `.chr-stage`/peta jadi 836px juga — letterbox balik ke ±169px per sisi. **Perbaikan:** `.chronicle` dikunci `height:min(78vh,720px)` (bukan auto, bukan 100dvh) — sidebar/panel yang lebih panjang dari itu scroll internal (fitur yang memang sudah didesain, cuma tidak pernah ketemu situasi utk aktif), peta dapat letterbox yang lebih konsisten dan tidak lagi terikat panjang konten sidebar/panel. Hasil: leftover turun ke ±100px per sisi (1440×900) — tidak senol sebelum §2e krn font memang sengaja dibesarkan, tapi jauh dari ±169px dan sekarang **stabil** (tidak lagi tergantung panjang quote/konten).

**2. "Kebocoran" dot pelabuhan.** User menunjukkan ulang `<span class="core" style="...">` yang sama persis dua kali — setelah dicek, bukan bug visual baru (posisi dot sudah benar sejak perbaikan rasio 3:2), melainkan keluhan soal **inline style JS yang bulky** (~300 karakter per dot × 14 dot, semua warna/ukuran/posisi state di-set langsung via `core.style.xxx` dari JS, bukan class CSS) — gaya ini sendiri yang "bocor" ke markup. **Perbaikan:** refactor total — `.chr-port .core`/`.halo` dan modifier `.active`/`.related`/`.dormant` sepenuhnya jadi CSS class (termasuk ukuran, warna, opacity per state), JS di `setActive()` disederhanakan jadi murni `classList.add/remove` tanpa satupun `element.style.xxx`. Bonus: ditemukan CSS mati peninggalan versi SVG lama (`.chr-port circle.core`, `.chr-port text` — selector yang tak pernah match elemen HTML `<div>`/`<span>` yang dipakai sekarang) — dihapus. Bonus lain: `haloPulse` keyframe punya bug laten (animasi `transform:scale()` menimpa `transform:translate(-50%,-50%)` dasarnya, bikin halo "meloncat" posisi saat animasi) — diperbaiki sekalian jadi `translate(-50%,-50%) scale()` gabungan.

**3. Toolbar & scrubber muncul di tampilan Daftar.** Dikonfirmasi bug nyata (bukan cuma observasi) — `#chrToolbar`/`#chrScrub`/`#chrEraBands` adalah sibling `.chronicle`, bukan child, jadi `.js.show-list .chronicle{display:none}` tidak menyembunyikan mereka. **Perbaikan:** tambah `.js.show-list #chrToolbar, #chrScrub, #chrEraBands{display:none}`. Diverifikasi: ketiganya `display:none` saat mode Daftar aktif.

**4. Ikon hilang di toolbar.** User tanya soal Streamline (streamlinehq.com) sbg sumber ikon. Dicek: search box toolbar (P3.1) tidak punya ikon kaca pembesar, tombol Reset tidak punya ikon — gap nyata dibanding elemen lain yang sudah konsisten pakai outline 24×24/stroke-width 2 (gaya setara Feather/Lucide, semua inline SVG hand-coded, tanpa dependency eksternal). **Keputusan:** tambah ikon yang hilang (search glyph di search box, refresh-icon di tombol Reset) dengan gaya yang SAMA (bukan pindah ke Streamline) — lihat jawaban lengkap di respons chat soal kenapa Streamline tidak direkomendasikan utk proyek ini (lisensi berbayar utk sebagian besar set, dependency eksternal baru utk sesuatu yang sudah bisa dibuat konsisten inline).

**Verifikasi Playwright:** leftover ±100px (turun dari ±169px), `navScrollable`/`panelScrollable` keduanya `true` (scroll internal aktif), `chrToolbar`/`chrScrub`/`chrEraBands` semua `display:none` di mode Daftar, tanpa console/page error.

**File:** `linimasa.html` — CSS `.chronicle` (`height:min(78vh,720px)`), `.chr-port`/`.core`/`.halo` + modifier (refactor dari inline style), JS `setActive()` port-state loop (disederhanakan), `.js.show-list` rules baru, markup+CSS ikon search/reset toolbar

---

## 2g. Era Band Dihapus, Font Kutipan Dikonfirmasi (2026-07-17)

Dua item cepat susulan §2f:

1. **`.chr-quote` pakai font apa?** User tanya apakah kutipan arsip pakai font tulisan-tangan `Yasraf-Amir-Piliang.otf` (docs/). Dicek: **tidak** — `.chr-quote` pakai `var(--serif)` = EB Garamond italic (§2e). Yasraf Piliang cuma pernah dipakai di thumbnail `traktat.png` yang sudah dihapus user sebelumnya. **Rekomendasi: jangan pakai font tulisan-tangan untuk kutipan** — kutipan arsip bisa 300–400 karakter teks Belanda arkais, font script/handwriting akan menurunkan keterbacaan drastis, bertentangan dengan perbaikan tipografi §2e. EB Garamond italic sudah tepat, dipertahankan. `@font-face "Yasraf Piliang"` yang sudah tidak dipakai di mana pun dihapus (aset font tetap ada di `static/`, cuma tidak direferensikan).

2. **Era band di timeline dihapus.** User: "menggangu estetika tampilan". P3.4 (Sprint 3, era band proporsional di bawah scrubber) dicabut total — markup `#chrEraBands`, CSS `.chr-era-bands`/`.chr-era-band`, JS builder (`ERA_BAND_BTNS` + populate loop), referensi toggle `.active` di `setActive()`, dan rule `.js.show-list #chrEraBands`. Navigasi era tetap tersedia via sidebar kiri (`.chr-era` buttons) — tidak ada fungsi yang hilang, cuma satu jalur akses redundan yang dihapus.

**Verifikasi Playwright:** `chrEraBands` terkonfirmasi tidak ada lagi di DOM; `.chr-quote` computed font-family terkonfirmasi `"EB Garamond", Georgia, "Times New Roman", serif`; screenshot scrubber bersih tanpa strip era band.

**File:** `linimasa.html` — hapus `@font-face` Yasraf Piliang, markup/CSS/JS `.chr-era-bands`/`#chrEraBands`/`ERA_BAND_BTNS`

---

## 3. Prinsip Desain

Dari audit §15 — yang menjadi north star redesign:

1. **Satu metafora dominan:** arus kekuasaan dari Aceh
2. **Satu sistem ilustrasi:** engraving konsisten
3. **Informasi muncul berdasarkan konteks:** tidak semua elemen tampil sekaligus
4. **Setiap detail visual punya fungsi:** hapus dekorasi tanpa makna
5. **Ruang kosong mengarahkan perhatian**
6. **Teks melewati proses editorial:** bukan data mentah
7. **Berani menghapus:** radical subtraction

---

## 4. Fase P0 — Hilangkan Kesan Slop

### P0.1 Kurangi elemen SVG stage simultan

**Masalah:** Semua orbit, VOC lines, ripples, compass, rhumb lines tampil bersamaan.
**Solusi:** Dalam satu state peristiwa, tampilkan maksimal:
- 1 pusat riak (Aceh)
- 1 rute utama aktif (berdasarkan event)
- 1-2 rute sekunder (opacity rendah)
- 5-7 port relevan (bukan semua 14)
- 1 legenda kontekstual

**Implementasi:**
- Saat `setActive(i)`, tentukan port mana yang relevan dengan event (sudah ada `portOf()`)
- Port non-relevan: sembunyikan label, kecilkan node (radius 2px, opacity 0.3)
- Orbit hanya tampilkan untuk port aktif + 2 tetangga terdekat
- VOC lines: hanya tampilkan yang melewati port aktif
- Compass: sembunyikan saat event aktif (hanya tampil di state default/awal)
- Rhumb lines: opacity 0.04 (saat ini 0.08), atau sembunyikan total

**File:** `linimasa.html` — modifikasi `setActive()` dan SVG build section

### P0.2 Standarisasi kapal

**Masalah:** Dua kapal dengan ukuran/opacity berbeda terasa seperti gaya berbeda.
**Solusi:** Satu kapal aktif (bergerak di rute), satu kapal dekoratif (statis, jauh lebih redup).

**Implementasi:**
- `.chr-ship2`: opacity turun ke 0.15 (dari 0.45), scale tetap 0.55
- Kapal aktif: warna `#d8cdb8` (sudah benar), animasi `sail` tetap
- Pertimbangkan: kapal dekoratif dihapus total jika masih terasa ramai

**File:** `linimasa.html` — CSS `.chr-ship2`

### P0.3 Ubah sidebar era dari radio button ke bab editorial — ✅ SUDAH SELESAI (verifikasi 2026-07-16)

**Ground-truth check saat mulai Sprint 2:** dicek langsung `document.getElementById('chrNav').outerHTML` di browser — `.chr-era::before` sudah pakai `counter(cera,decimal-leading-zero)` (nomor bab 01/02/03, bukan dot), sudah ada rail vertikal (`.chr-nav::before/::after`, progress mengikuti era aktif), label pakai `.lbl` (serif), summary (`.sum`) hanya tampil saat aktif. **Tidak ada dot radio-button di kode saat ini** — audit ini menjelaskan versi kode yang lebih lama. Tidak perlu kerja lagi untuk item ini.

**Masalah (versi audit asli, sudah tidak berlaku):** Dot `::before` menyerupai radio button / stepper formulir.
**Solusi:** Format bab kronik:

```
01
1600–1637

Kontrak Pertama
dan Kekuasaan
Iskandar Muda
```

**Implementasi:**
- Hapus `.chr-era::before` (dot radio button)
- Ganti dengan nomor bab (urutan 01, 02, 03...) menggunakan `::before` counter
- Tahun range tetap
- Label era: font EB Garamond (dari Space Grotesk)
- Gunakan garis vertikal tipis sebagai pengganti dot (timeline rail)
- Era aktif: teks lebih tebal + garis terisi (bukan dot berwarna)

**File:** `linimasa.html` — CSS `.chr-era`, `.chr-era::before`, `.chr-era.active`

### P0.4 Redesign panel kanan menjadi lembar editorial — ✅ SUDAH SELESAI (verifikasi 2026-07-16)

**Ground-truth check:** `renderPanel()` saat ini SUDAH menghasilkan persis format target: counter "PERISTIWA 01 / 101", tahun besar + `<hr class="chr-divider">`, judul, subtitle (`event_type · ruler_actor`), quote, source details ("Arsip CD1" / "Halaman 47, baris 19–20"), status editorial ("Belum diverifikasi silang"), tombol "Baca transkrip" + "Tampilkan pada peta". Tidak perlu kerja lagi untuk item ini — **kecuali** temuan baru P0.10 di bawah (kebocoran `chr-notes`).

**Masalah (versi audit asli, sudah tidak berlaku):** Panel terasa seperti detail drawer dashboard.
**Solusi:** Format editorial:

```
PERISTIWA 01 / 101

1600
────────────

Kontrak Dagang Lada Pertama
VOC–Aceh

PERJANJIAN · PERDAGANGAN

Desember 1600
Aceh Darussalam

Ringkasan editorial peristiwa...

SUMBER PRIMER
"Kutipan sumber..."

Arsip CD1
Halaman 47

Status: Belum diverifikasi silang

[Baca transkrip]
Tampilkan pada peta →
```

**Implementasi:**
- Modifikasi `renderPanel()` di `linimasa.html:1121-1146`
- Tambahkan counter "PERISTIWA X / 101" (dari `active + 1` dan `SEQ.length`)
- Tahun berdiri sendiri, terpisah dari judul
- Garis horizontal pemisah setelah tahun
- Subtitle kota/lokasi di bawah judul
- Metadata source: bahasa Indonesia, bukan campur
- Tombol: "Baca transkrip" (sudah ada) + "Tampilkan pada peta" (ganti "Lihat di peta")
- Sembunyikan `confidence_flag` raw — ganti dengan status editorial

**File:** `linimasa.html` — fungsi `renderPanel()`

### P0.5 Hilangkan elemen tanpa makna langsung

**Daftar hapus/redupkan:**
- Orbit elips: sembunyikan saat event aktif (hanya tampil di state awal "semua rute")
- Panah kecil di sepanjang pesisir: tidak ada di kode saat ini (audit mungkin merujuk ke design lain) — skip
- Rhumb lines (kompas portolan): opacity dari 0.08 ke 0.03, atau hapus
- Kompas mawar: sembunyikan saat event aktif (`.chr-stage[data-era] .chr-compass { opacity: 0 }`)
- Label "SUMATRA" (landname): opacity dari 0.26 ke 0.12

**File:** `linimasa.html` — CSS rules untuk `.orbit`, `.chr-rhumb`, `.chr-compass`, `.chr-landname`

### P0.6 Tetapkan satu focal point per state

**Focal path yang ideal (audit §12):**
1. Tahun dan judul peristiwa (panel kanan atas)
2. Lokasi aktif pada peta (node emas bercahaya)
3. Rute yang menjelaskan hubungan (1 garis utama)
4. Konteks era (sidebar)
5. Sumber primer (panel kanan bawah)

**Implementasi:**
- Node port aktif: `r=8` + `fill:#e3c15c` + animated halo (sudah ada)
- Port lain: `r=2.5`, `opacity:0.25`, no label
- Rute utama: `stroke-width:2`, `opacity:0.8`
- Rute sekunder: `stroke-width:1`, `opacity:0.2`
- Panel kanan: tahun + judul harus paling terang dan paling besar

### P0.7 Microcopy bahasa Indonesia — ✅ SUDAH SELESAI (verifikasi 2026-07-16)

**Ground-truth check:** semua mapping di bawah ini SUDAH ada di `renderPanel()`/`statusMap` saat ini. Tidak perlu kerja lagi untuk item ini — kecuali baris terakhir ("Aceh" vs "Atjeh"), lihat catatan di bawah.

**Catatan tersisa (bukan bug template, keputusan editorial data):** judul event masih memakai ejaan "Atjeh" pada teks yang jelas ditulis modern/editorial (bukan kutipan), mis. "Kontrak dagang lada pertama VOC-**Atjeh**". Audit minta "Aceh" di narasi modern, "Atjeh" hanya di kutipan sumber. ini nilai di data JSON (title event), bukan di template — perbaikannya butuh sentuh sumber data, di luar scope perubahan template `linimasa.html`. Tidak dieksekusi di sprint ini; catat sebagai item terbuka untuk tim data/kurator.

**Masalah (versi audit asli):** `vol. CD1 · hlm. 47 (19–20) · unverified`
**Solusi:**

```
STATUS SUMBER
Belum diverifikasi silang

Arsip CD1
Halaman 47
```

**Implementasi:**
- Di `renderPanel()`: format ulang `.chr-src`
- `confidence_flag: "unverified"` → "Belum diverifikasi silang"
- `confidence_flag: "verified"` → "Terverifikasi silang"
- `source_document` → "Arsip CD1" (bukan "vol. CD1")
- `source_page` → "Halaman 47" (bukan "hlm. 47")
- Hapus `book_page` dari tampilan utama (simpan di tooltip/hover)
- Konsistensi: "Aceh" di narasi modern, "Atjeh" hanya di kutipan sumber

**File:** `linimasa.html` — fungsi `renderPanel()`, juga template kartu di `#listView`

### P0.8 Statistik sebagai filter interaktif (baru, dari §2b)

**Masalah:** `.tiles` di header (`101 peristiwa`, `4 suksesi`, `51 perjanjian`, dst.) murni display — tanpa afordansi klik, semua kotak berbobot visual sama. Ini akar kesan "dashboard BI" yang justru disebut sebagai masalah inti, bukan cuma efek samping ruang kosong.

**Solusi:**
- `101 peristiwa` dan rentang tahun (`1600–1775`) tetap sebagai anchor metric — beri ukuran font/berat lebih besar daripada tile kategori (bukan grid seragam seperti sekarang)
- Tile kategori (`suksesi`, `perjanjian`, `konflik`, `diplomasi`, `administratif`) jadi `<button>` yang mem-filter `#listView` dan menyorot event bertipe sama di panggung peta/scrubber
- State aktif: background gading solid; state lain: border tipis (selaras token warna P1.1)
- `aria-pressed` pada tiap tile-button, `:focus-visible` eksplisit

**Implementasi:**
- Ubah markup `.tile` di `:601-607` dari `<div>` ke `<button type="button" data-filter="perjanjian">`
- Tambah handler klik yang reuse logic filter yang sudah ada di `#typeFilter` (`:670-677`) supaya satu sumber kebenaran filter, bukan duplikasi state
- CSS: pisahkan `.tile--primary` (peristiwa + rentang tahun, font lebih besar) dari `.tile--filter` (kategori, interaktif)

**File:** `linimasa.html` — markup `.tiles` (`:601-608`), CSS `.tile`, JS filter handler

### P0.9 Footer ringkasan "Periode Aktif" pada sidebar era (baru, verifikasi Sprint 2)

**Masalah:** Diverifikasi via Playwright — `#chrNav` tinggi 898px, era terakhir berakhir di 465px → **~433px ruang kosong** di bawah daftar 5 era. Ini persis dead space audit ruang-kosong §2.3/§6, dan belum ada penanganannya di kode saat ini (JS cuma `nav.appendChild(b)` untuk tiap era, tidak ada elemen footer).

**Solusi (dari audit ruang-kosong §6):**
```
PERIODE AKTIF
1600–1637

5 peristiwa dari 101

Lihat seluruh peristiwa era →
```

**Implementasi:**
- Tambah `<footer>` statis di dalam `.chr-nav` (setelah loop era), diisi oleh `setActive()`: era aktif range + label, jumlah event di era itu (hitung dari `SEQ.filter(ev => ev.era_slug === activeEraSlug).length`) dari total `SEQ.length`
- Link "Lihat seluruh peristiwa era" scroll/filter ke era aktif (reuse `#typeFilter`-style filtering atau scroll ke `#listView` dengan filter era)
- CSS: `.chr-nav` jadi flex column dengan footer `margin-top:auto` supaya menempel ke bawah tanpa mengubah tinggi 5 tombol era di atasnya

**File:** `linimasa.html` — markup `.chr-nav` (tambah footer), JS `setActive()`, CSS `.chr-nav-footer`

### P0.10 Sembunyikan `chr-notes` (catatan kurator internal) dari panel publik (baru, verifikasi Sprint 2)

**Masalah:** Dicek via API `/api/research/linimasa` — **101/101 event** (100%) punya field `notes` berisi catatan riset internal mentah ("SUMBER: Corpus Diplomaticum (CD1.pdf)...", "Didistilasi dari atjeh_trade_records...", "TEMUAN PENTING -- ..."). Field ini dirender apa adanya ke pengunjung publik di `renderPanel()` (`${ev.notes ? '<div class="chr-notes">'+esc(ev.notes)+'</div>' : ''}`) — ini pelanggaran langsung prinsip "teks melewati proses editorial, bukan data mentah" (audit §15), dan sistemik (bukan kasus khusus 1-2 event).

**Solusi:** Hapus render `.chr-notes` dari panel yang dilihat publik. Data JSON **tidak diubah** (sesuai CLAUDE.md — sumber data historis tidak diedit langsung), hanya template berhenti menampilkannya. Jika suatu saat dibutuhkan untuk debugging, tampilkan lewat `console.debug()`, bukan DOM visible.

**Implementasi:**
- `linimasa.html` — hapus baris `${ev.notes ? ... : ''}` dari `renderPanel()`
- CSS `.chr-notes` jadi dead code — boleh dibiarkan (dead CSS lain sudah ada preseden) atau dihapus sekalian saat sprint pembersihan

**File:** `linimasa.html` — fungsi `renderPanel()`

**Regresi ditemukan user (2026-07-16), sudah diperbaiki:** tombol "Baca Transkrip" **tidak dihapus** saat P0.10 dikerjakan — tombol ini didesain khusus untuk mem-toggle `.open-transcript` yang menampilkan `.chr-notes` (via CSS `.chr-panel.open-transcript .chr-notes{display:block}`). Setelah div `.chr-notes` dihapus dari markup, klik tombol itu cuma memicu efek samping resize grid P1.7 (`.chronicle.reading`, sidebar menyempit/panel melebar) **tanpa konten baru muncul** — persis keluhan user "ukuran dan posisi huruf berubah tapi tidak ada perubahan lain". Root cause: dependensi antara P0.10 dan tombol transkrip tidak diperiksa silang saat P0.10 dikerjakan.

**Perbaikan:** tombol "Baca Transkrip" **dihapus total** (bukan diperbaiki untuk menampilkan sesuatu) — `ev.text_asli` (transkrip/kutipan arsip asli) sudah tampil penuh di `.chr-quote`, dan `ev.notes` (yang tombol ini dulu buka) memang sengaja disembunyikan karena isinya catatan kurator internal, bukan transkrip. Tidak ada konten legitimate lagi untuk tombol ini buka. Ikut dihapus: CSS `.chr-notes`, `.chr-panel.open-transcript .chr-notes`, `.chronicle.reading` grid (P1.7 jadi N/A lagi — trigger satu-satunya sudah tidak ada), dan referensi `.chr-notes`/`.chr-meta` mati di `.chr-panel.treaty`.

---

## 5. Fase P1 — Bangun Sistem Visual

### P1.1 Semantik warna dan garis — ⛔ TIDAK BERLAKU (superseded 2026-07-16, lihat §2c)

Seluruh rute (`route-voc`/`route-orbit`), orbit, dan node aktif/related/dormant berbasis garis **dihapus total** atas arahan langsung user (§2c) — peta sekarang murni ilustrasi + titik pelabuhan polos, tanpa garis apa pun. Tidak ada lagi "semantik garis" untuk diformalkan karena garisnya sendiri sudah tidak ada. Item ini ditutup tanpa implementasi.

**Masalah (versi audit asli, sudah tidak berlaku):**

Dari audit §9 — formalisasikan makna setiap elemen visual:

| Elemen | Makna | Warna/Style |
|---|---|---|
| Riak konsentris | Pusat kekuasaan Aceh | `#e3c15c`, `stroke-width:1.2` |
| Garis emas solid | Pengaruh politik Aceh | `#c49a47`, `stroke-dasharray:none` |
| Garis tembaga putus | Rute VOC | `#a04a35`, `stroke-dasharray:7 4` |
| Node emas | Port aktif (event) | `fill:#e3c15c`, `r:8` |
| Node putih | Port terkait | `fill:#f3ead9`, `r:4.5` |
| Node abu-abu | Port tidak relevan | `fill:#f3ead9`, `opacity:0.25`, `r:2.5` |

**Implementasi:**
- Buat CSS custom properties baru: `--route-aceh`, `--route-voc`, `--route-local`, `--node-active`, `--node-related`, `--node-dormant`
- Terapkan ke SVG elements yang sudah ada
- Hapus SEMUA orbit emas (ganti dengan 1 garis solid Aceh→port aktif)

**File:** `linimasa.html` — `:root` CSS vars + SVG build

### P1.2 Sistem ukuran kapal dan node — ⛔ TIDAK BERLAKU (superseded 2026-07-16)

Tidak ada elemen kapal di overlay peta (lihat P0.2 §2). Ukuran node aktif/related/dormant **sudah** diimplementasi di `setActive()` sejak Sprint 1 (verifikasi P0.6) — port polos tanpa label, tapi ukuran/opacity 3-state-nya tetap berlaku. Tabel di bawah untuk referensi historis saja.

| Elemen | Ukuran | Keterangan |
|---|---|---|
| Aceh (pusat) | `r:8` + halo | Selalu paling besar |
| Port aktif | `r:6` + gold fill | Muncul saat event |
| Port terkait | `r:4.5` + white fill | Tetangga dalam rute |
| Port dorman | `r:2.5` + low opacity | Tidak relevan |
| Kapal aktif | `scale:1` + animasi | Bergerak di rute |
| Kapal dekoratif | `scale:0.4` + opacity 0.12 | Statis, background |

### P1.3 Batasi tipografi — ✅ SUDAH SELESAI (verifikasi 2026-07-16)

**Ground-truth check:** `.chr-year{font-family:var(--serif);font-weight:600;font-size:2.5rem}` (`linimasa.html:475`) — persis target tabel di bawah. Font stack pakai "Cormorant Garamond" (bukan literal "EB Garamond") tapi serif editorial yang sama fungsinya — keputusan yang sudah dikunci, bukan gap. Tidak perlu kerja lagi.

Dari audit §8:

| Elemen | Font | Size | Weight |
|---|---|---|---|
| Tahun (panel) | EB Garamond | 2.5rem | 600 |
| Judul peristiwa | EB Garamond | 1.3rem | 600 |
| Kutipan sumber | EB Garamond italic | 0.93rem | 400 |
| Narasi era | EB Garamond | 1.05rem | 400 |
| Label port (SVG) | Space Grotesk | 10.5px | 600 |
| Navigasi era | Space Grotesk | 0.94rem | 600 |
| Metadata | Space Grotesk | 0.8rem | 400 |
| Badge event type | Space Grotesk | 0.68rem | 600 |
| Tombol | Space Grotesk | 0.78rem | 600 |

**Implementasi:**
- Tahun di panel: ganti dari `var(--mono)` ke `var(--serif)` — konsisten dengan audit §8
- Tahun di scrubber: tetap mono (tabular nums untuk alignment)
- Judul era di sidebar: ganti ke EB Garamond (sudah benar di `.era-label`)

**File:** `linimasa.html` — CSS `.chr-year`, `.chr-title`, `.era-label`

### P1.4 Ubah sidebar kiri menjadi daftar bab kronik — ✅ SUDAH SELESAI (via P0.3, verifikasi 2026-07-16)

Rail vertikal, nomor bab, dan footer "Periode Aktif" sudah ada (P0.3 + P0.9). Tidak perlu kerja lagi.

Dari P0.3 + enhancement:

```
┌──────────────┐
│ BAB KRONIK   │
│              │
│ ────────── 01
│ 1600–1637    │
│              │
│ Kontrak      │
│ Pertama &    │
│ Kekuasaan    │
│ Iskandar Muda│
│              │
│ ────────── ● 02  ← aktif
│ 1641–1650    │
│              │
│ Ratu Atjeh & │
│ Puncak       │
│ Kekuasaan    │
│              │
│ ────────── 03
│ ...          │
└──────────────┘
```

**Implementasi:**
- Garis vertikal tipis di kiri (timeline rail)
- Nomor bab di atas garis
- Tahun range di bawah nomor
- Label judul: EB Garamond, wrap natural
- Era aktif: garis terisi emas, judul lebih gelap
- Era lain: garis abu-abu tipis, judul muted
- Hilangkan headline/summary dari sidebar (pindah ke panel kanan atau hapus)
- `overflow-y:auto` + `scroll-snap` untuk navigasi panjang

**File:** `linimasa.html` — CSS `.chr-nav`, `.chr-era`, `.chr-era::before`

### P1.5 Buat legenda kontekstual — ⛔ TIDAK BERLAKU (superseded 2026-07-16)

Peta sekarang polos (tanpa rute/label/orbit) — tidak ada lagi elemen visual yang perlu dijelaskan lewat legenda. `.chr-legend` tetap CSS mati, sengaja tidak dibangun. Jika suatu saat peta menambah simbol baru, legenda bisa dipertimbangkan lagi saat itu.

**Rencana asli (tidak lagi relevan):**

Saat ini legenda statis (`.chr-legend`). Ubah menjadi dinamis:

```
┌─────────────────────┐
│ ● Aceh (pusat)      │
│ ─ Rute aktif        │
│ ·· Rute terkait     │
│ ○ Port aktif        │
│ ○ Port terkait      │
└─────────────────────┘
```

- Hanya tampilkan elemen yang ADA di state saat ini
- Sembunyikan legenda saat compass/rhumb lines tidak terlihat
- Format: horizontal di bawah scrubber, bukan overlay kiri bawah

**File:** `linimasa.html` — buat `renderLegend()` baru, CSS `.chr-legend`

### P1.6 Pisahkan layer atmosfer/geografi/peristiwa — ✅ SELESAI DENGAN SOLUSI LEBIH SEDERHANA (§2c, 2026-07-16)

Overlay gelap dihapus total (bukan diturunkan sebagian) — user minta warna peta asli. Tidak ada lagi "layer" untuk dipisahkan karena cuma tersisa satu gambar utuh + titik pelabuhan polos.

Dari audit §11:

| Layer | Isi | Z-index |
|---|---|---|
| ATMOSFER | Background image, vignette, texture | 0 |
| GEOGRAFI | Coastline, islands, equator, labels, Bukit Barisan | 1 |
| PERISTIWA | Routes, active port, ripples, ship, annotations | 2 |

**Implementasi:**
- Saat event aktif: `.chr-stage::before` opacity turun (image lebih redup)
- Coastline + islands: tetap visible tapi muted
- Routes + active port: paling tajam dan kontras
- Ripple Aceh: opacity mengikuti era (sudah ada di CSS `data-era` rules)
- **Update (§2b):** aset `#chrMap` sekarang benar (`peta-untukruangtengah.png`, 3 kapal engraving terlihat jelas di sumber asli). Inline style saat ini (`opacity:.5; grayscale(60%); brightness(.7)` di `linimasa.html:636`) belum diverifikasi terhadap aset baru — cek apakah kombinasi ini masih menenggelamkan siluet kapal. Jika ya, naikkan opacity dasar atau turunkan darkness overlay `#chrMapOverlay` (`:638`), bukan menghapus kapal dari aset

**File:** `linimasa.html` — CSS `.chr-stage::before`, `.chr-coast`, `.chr-isle`, inline style `#chrMap`

### P1.7 Responsive: panel kanan menyempit/melebar — ⛔ TIDAK BERLAKU LAGI (regresi ditemukan & diperbaiki 2026-07-16, lihat P0.10)

Sebelumnya ditandai selesai karena tombol "Baca Transkrip" memicu `.chronicle.reading` (grid resize). Tombol itu ternyata sudah tidak berfungsi sejak `.chr-notes` dihapus di P0.10 (klik cuma resize tanpa konten baru — bug yang ditemukan user). Tombol beserta seluruh mekanisme `.reading`/`.open-transcript` **dihapus total**, bukan diperbaiki, karena tidak ada konten legitimate lagi untuk trigger ini. Item ditutup tanpa implementasi — kalau nanti ada kebutuhan nyata utk expand/collapse panel, desain ulang dari awal, jangan pakai sisa mekanisme lama.

Dari audit §13:
- Saat eksplorasi peta: panel kanan menyempit (300px)
- Saat membaca sumber: panel kanan melebar (400px)
- Panel kiri: rail yang lebih ringan (180px → 160px)

**Implementasi:**
- Tambahkan state "reading mode" yang dipicu saat user klik "Baca transkrip"
- CSS transition pada `grid-template-columns`
- Mobile (< 980px): sudah single column, pertahankan

**File:** `linimasa.html` — CSS `.chronicle` grid, JS state management

---

## 5b. Fase P3 — Gap dari `Designer-fix.png` (audit ruang-kosong, belum pernah masuk sprint manapun)

Ditemukan lewat perbandingan screenshot langsung terhadap `docs/Designer-fix.png` (2026-07-16) — bukan dari audit anti-slop, tapi dari audit ruang-kosong yang PRD-nya terpisah dan rekomendasi toolbar/footer-nya belum pernah dieksekusi di sprint manapun. Legenda peta (rencana lama P1.5) **tidak dimasukkan** ke sini karena sudah tidak relevan (peta polos, tidak ada elemen untuk dijelaskan).

### P3.1 Toolbar eksplorasi di bawah statistik (mode Peta) — ✅ SELESAI (2026-07-16, scope disesuaikan)

**Masalah:** Di mode Peta, satu-satunya kontrol adalah tombol "Tampilan daftar" berdiri sendiri — tidak ada cara mencari/memfilter tanpa pindah ke mode Daftar dulu. Ini persis dead-space yang diflag audit ruang-kosong §2.2, tapi belum pernah diimplementasikan.

**Diimplementasikan:**
- Search box "Cari peristiwa, lokasi, atau tokoh…" — cari `title`/`ruler_actor`/`text_asli` (case-insensitive), lompat ke match pertama via `setActive()`. Tidak ketemu → `setCustomValidity` + `reportValidity()` (pesan native browser, bukan toast custom)
- Dropdown Kategori — **filter navigasi sungguhan**, bukan dekoratif: `categoryFilter` state + `matchesCategory()` + `findNextMatch()` membuat prev/next/panah keyboard **cuma berhenti di event yang cocok**, dot scrubber non-match diredupkan (`opacity:.15`)
- Dropdown Era — jump langsung ke event pertama era itu, setara klik sidebar/era-band
- Tombol Reset — clear search + kategori + era, kembalikan opacity semua dot
- **Drop dari rencana awal:** dropdown "Rentang Tahun" — tidak ada widget range yang pas tanpa membangun date-range-picker terpisah (scrubber sudah bisa discrub visual by year); dan tombol "Legenda" — tidak ada lagi elemen peta yang perlu dijelaskan (P1.5 superseded)

**File:** `linimasa.html` — markup `.chr-toolbar` sebelum `.chronicle`, CSS `.chr-toolbar*`/`.chr-tb-*`, JS state `categoryFilter`/`matchesCategory`/`findNextMatch`/`applyCategoryFilterVisual`, modifikasi listener `chrPrev`/`chrNext`/`ArrowLeft`/`ArrowRight` yang sudah ada

**Verifikasi Playwright:** search "Traktat Painan" ketemu match benar; filter "konflik" meredupkan 80/101 dot (tepat 101−21, cocok stat tile); 5× klik "Berikutnya" berturut-turut semua tetap badge "konflik" (navigasi benar-benar tertahan filter, bukan cuma tampilan); era jump & reset bekerja; tanpa page error.

**Bug ditemukan user (2026-07-16), sudah diperbaiki:** dropdown `#chrCategoryFilter`/`#chrEraJump` (dan `#typeFilter` lama di list view, bug yang sama, belum pernah dilaporkan sebelumnya) — teks opsi tak terbaca saat dropdown dibuka. Root cause: `<select>` di-styling `color:var(--ink)` (krem) di atas `background` transparan, tapi popup opsi dirender browser dengan background putih bawaan OS (di luar cascade normal CSS) — krem-di-atas-putih nyaris tak terbaca. Fix: `select option{background:#14100a;color:var(--ink)}` eksplisit di kedua tempat (`.chr-tb-select` dan `.controls select`).

### P3.2 Badge kategori berwarna di panel kanan — ✅ SELESAI (2026-07-16)

**Masalah:** Mockup menampilkan tag `PERJANJIAN`/`DIPLOMASI` sebagai pill berwarna terpisah. Panel kita saat ini cuma teks polos `perjanjian · sabander van Atchin (Raja Atjeh)` di `.chr-subtitle`. `TYPE_COLOR` map **sudah ada** di JS (`:842`) tapi tidak dipakai di `renderPanel()`.

**Diimplementasikan:** `.chr-badge` pakai teks berwarna (`color:currentColor` dari `TYPE_COLOR`) di atas background gelap translucent (`rgba(0,0,0,.35)`) + border-left aksen warna — **bukan** fill solid seperti draft awal, supaya kontras aman utk semua 5 warna kategori tanpa perlu cek manual satu-satu (beberapa `--evt-*` seperti `--admin-umber:#a08a6e` cukup terang, fill solid + teks krem akan gagal kontras). `.chr-subtitle`/`.chr-meta` lama (sekarang dead) dihapus.

**Temuan tambahan (belum diperbaiki, dicatat untuk nanti):** `--evt-suksesi` dan `--evt-perjanjian` sama-sama `#29484b` (variabel bernama "gold" tapi nilainya teal) — dua kategori berbeda jadi warna badge identik. Bukan bug baru dari sprint ini, tapi terekspos lebih jelas sekarang karena warnanya dipakai sebagai badge yang lebih menonjol daripada dot kecil di peta.

**File:** `linimasa.html` — `renderPanel()`, CSS `.chr-badges`/`.chr-badge`

### P3.3 Meta row dengan ikon (tanggal, lokasi, pihak terlibat) — ✅ SELESAI (2026-07-16)

**Masalah:** Mockup punya 3 baris meta berikon (kalender/lokasi/institusi: "Desember 1600", "Aceh Darussalam", "VOC & Kerajaan Aceh"). Data kita **tidak** punya field lokasi/institusi terpisah — cuma `event_date_raw` dan `ruler_actor` gabungan. Tidak boleh mengarang field baru (CLAUDE.md: sumber data historis tidak diedit langsung).

**Diimplementasikan** pakai data yang sudah ada, tanpa field baru:
- Ikon kalender + `event_date_raw`
- Ikon lokasi + hasil `portOf(ev)` (fungsi ini **sudah ada**, dipakai jg utk port dot di peta — reuse, bukan data baru)
- Ikon institusi + `ruler_actor` (dipisah dari lokasi, bukan digabung 1 baris subtitle spt sebelumnya)

**File:** `linimasa.html` — `renderPanel()`, CSS `.chr-meta-row`/`.chr-meta-item`

### P3.4 Era band pada timeline scrubber — ⛔ DICABUT (2026-07-17, lihat §2g)

Sempat selesai & diverifikasi 2026-07-16, tapi user menilai "menggangu estetika tampilan" — dihapus total 2026-07-17. Navigasi era tetap via sidebar kiri. Detail asli di bawah untuk referensi historis.

**Masalah:** Mockup punya baris segmen berwarna di bawah tick tahun, berlabel nama era ("Gelombang Penaklukan", dst.), era aktif disorot. Scrubber kita cuma titik + panah + 5 label tahun — tidak ada baris band era.

**Diimplementasikan:**
- `<div class="chr-era-bands">` di bawah `#chrScrub` (bukan di dalamnya — beda baris, scrubber tetap sticky, band tidak), di-generate dari `ERAS_META` yang sama dgn sidebar
- Lebar tiap band proporsional pakai `flex-grow` = jumlah tahun era itu (parse dari string `era.range`, mis. "1600–1637" → span 37) — CSS flexbox native, tanpa hitung persentase manual
- Era aktif: `background:var(--accent)`; era lain: muted, truncate dgn ellipsis kalau sempit (era pendek spt "Retak & Pemberontakan Painan" cuma 3 tahun — `title` attribute kasih label lengkap on-hover)
- Klik band = pindah ke event pertama era itu, sinkron dgn highlight sidebar

**File:** `linimasa.html` — markup `#chrEraBands`, JS build dari `ERAS_META` + toggle `.active` di `setActive()`, CSS `.chr-era-bands`/`.chr-era-band`

### P3.5 Footer 5-kolom yang selalu terlihat (bukan cuma di mode Daftar)

**Masalah:** Footer kita cuma 2 kolom (`Sumber & Metode` / `Corpus Diplomaticum & Cakupan`) dan **tersembunyi di mode Peta** (ada di dalam `#listView` yang `display:none` default). Mockup punya 5 kolom (`Tentang Kronik`, `Jelajah Cepat`, `Dokumen Terbaru`, `Statistik Periode Aktif`, `Arsip Digital`) yang selalu terlihat di bawah peta+scrubber.

**Solusi bertahap (jangan duplikasi footer 2-kolom yang sudah ada):**
- Pindahkan footer keluar dari `#listView` supaya selalu terlihat di kedua mode (di bawah `#chrScrub`)
- Tambah 3 kolom baru: `Jelajah Cepat` (link ke `/riset/*` yang sudah ada — Peta Pelabuhan, Jalur Perdagangan, Tokoh Penting), `Dokumen Terbaru` (perlu cek apakah backend punya endpoint utk "dokumen terbaru" atau ini hardcode dari beberapa event terbaru), `Statistik Periode Aktif` (hitung dari `SEQ.filter(era aktif)`, mirip `.chr-nav-footer` yang sudah ada — reuse logic, jangan duplikasi)
- `Arsip Digital` — cek dulu apakah ada halaman/endpoint arsip digital sungguhan sebelum bikin tombol yang mengarah ke tempat tidak ada (jangan bikin dead link)

**File:** `linimasa.html` — restrukturisasi markup footer, keluar dari `#listView`

**Catatan implementasi:** P3.5 punya risiko terbesar bikin dead link/konten kosong (Dokumen Terbaru, Arsip Digital) — cek ketersediaan data/halaman dulu sebelum build UI-nya, jangan sebaliknya.

---

## 6. Fase P2 — Motion Setelah Desain Statis Matang

### P2.1 Riak Aceh bergerak lambat

Sudah ada animasi `.ripple` (4.8s linear infinite). Pertahankan, tapi pastikan:
- Hanya muncul saat Aceh adalah pusat kekuasaan aktif
- `prefers-reduced-motion` sudah didukung (sudah ada)
- Durasi bisa diperlambat ke 6s untuk kesan lebih tenang

### P2.2 Satu kapal bergerak pada rute aktif

Sudah ada animasi `.chr-ship` (26s ease-in-out infinite alternate). Enhancement:
- Animasi kapal mengikuti path rute aktif (bukan translate statis)
- Implementasi: `offset-path` + `offset-distance` pada SVG ship
- Fallback: tetap translate statis jika browser tidak support

### P2.3 Rute tergambar secara bertahap

Saat event berubah, garis rute "tertulis" dari port asal ke port tujuan:
- Gunakan `stroke-dashoffset` animation
- Durasi: 800ms ease
- Hanya pada transisi antar event (bukan saat load pertama)

### P2.4 Perubahan era memudarkan layer lama

Saat user pindah era:
- Layer atmosfer: opacity transition 600ms
- Port lama: fade out 400ms
- Port baru: fade in 400ms (staggered 100ms per port)

### P2.5 prefers-reduced-motion

**Wajib didukung** (audit §16 P2.6):
- Semua animasi dihentikan
- Transisi tetap jalan (opacity, transform) tanpa `animation`
- Kapal statis di posisi tengah rute
- Ripples statis di scale 0.5, opacity 0.3

Sudah ada di kode saat ini — pastikan SEMUA animasi baru juga punya fallback ini.

---

## 7. File yang Diubah

| File | Perubahan |
|---|---|
| `frontend/map_app/templates/map_app/linimasa.html` | CSS: P0.3, P0.5, P1.1, P1.3, P1.4, P1.6, P1.7, P2.1-P2.5. JS: P0.1, P0.2, P0.4, P0.6, P0.7, P0.8, P1.2, P1.5. HTML: legenda dinamis, `.tiles` → filter buttons |
| `frontend/map_app/static/map_app/img/peta-untukruangtengah.png` | **Sudah ditambahkan** — aset panggung peta pengganti `amh-5147-na.jpg` yang hilang |
| `frontend/map_app/views.py` | Tidak berubah (data model sudah cukup) |
| `backend/models.py` | Tidak berubah |
| `backend/routers/research.py` | Tidak berubah |

**Total: 1 file utama** (`linimasa.html`) — semua perubahan CSS + JS + SVG inline.

---

## 8. Urutan Implementasi

### Sprint 1: Radical Subtraction (P0)
0. ~~Fix aset panggung peta (`amh-5147-na.jpg` hilang → `peta-untukruangtengah.png`)~~ — **selesai di luar sprint**, prasyarat sebelum verifikasi P1.6
1. P0.1 — Kurangi elemen SVG simultan (port, orbit, rute)
2. P0.5 — Hapus/redupkan elemen tanpa makna
3. P0.2 — Standarisasi kapal
4. P0.6 — Tetapkan focal point per state
5. **Verifikasi:** Buka `/linimasa`, pastikan tampilan lebih bersih, fokus ke event aktif; pastikan gambar panggung peta termuat (bukan broken image) — **SELESAI (2026-07-16)**, diverifikasi via Playwright headless: gambar termuat, filter rute aktif/sekunder/dorman bekerja di 6 event/port berbeda, tanpa console/page error, celah kosong `#chrMapWrap` diperbaiki (`flex:1` ganti `aspect-ratio:3/2`)

### Sprint 2: Editorial Polish (P0 continued)
6. ~~P0.3 — Ubah sidebar ke format bab kronik~~ — **sudah selesai**, diverifikasi ground-truth 2026-07-16 (lihat catatan di §4)
7. ~~P0.4 — Redesign panel kanan ke lembar editorial~~ — **sudah selesai**, diverifikasi ground-truth 2026-07-16
8. ~~P0.7 — Microcopy bahasa Indonesia~~ — **sudah selesai**, diverifikasi ground-truth 2026-07-16 (kecuali item data "Aceh"/"Atjeh", di luar scope template)
9. P0.8 — Statistik sebagai filter interaktif (baru, §2b)
10. P0.9 — Footer ringkasan "Periode Aktif" pada sidebar (baru, ditemukan saat verifikasi Sprint 2)
11. P0.10 — Sembunyikan `chr-notes` catatan kurator internal dari panel publik (baru, ditemukan saat verifikasi Sprint 2)
12. **Verifikasi:** Bandingkan dengan wireframe audit §17; cek kontras `.chr-quote`/`.quote` (kutipan sumber primer) terhadap WCAG AA; cek `aria-pressed` dan `:focus-visible` pada tile filter baru; screenshot sidebar footer mengisi dead space; pastikan tidak ada lagi teks `SUMBER:`/`Didistilasi dari` di panel publik — **SELESAI (2026-07-16)**, diverifikasi via Playwright: chr-notes leak hilang (101/101 event dicek via `.innerText` regex), footer sidebar mengisi ruang 747–878px dari 898px tinggi nav, tile filter "perjanjian" bekerja end-to-end (aria-pressed, sinkron ke `#typeFilter`, 51/101 kartu terfilter, auto-pindah ke tampilan daftar, toggle-off mengembalikan semua), tanpa console/page error. Kontras WCAG AA `.chr-quote` **belum** diukur numerik — item terbuka untuk sprint berikut.

### ~~Sprint 3: Sistem Visual (P1)~~ — dibubarkan, seluruh isinya sudah selesai/tidak berlaku
~~P1.1~~ (superseded, peta polos), ~~P1.2~~ (superseded, tanpa kapal), ~~P1.3~~ (sudah selesai — verifikasi ground-truth 2026-07-16), ~~P1.4~~ (sudah selesai via P0.3), ~~P1.5~~ (superseded, tanpa legenda), ~~P1.6~~ (selesai via §2c), ~~P1.7~~ (sudah selesai — reading-mode grid sudah ada). Tidak ada kerja tersisa dari Fase P1 asli.

### Sprint 3 (baru): Fitur Eksplorasi dari `Designer-fix.png` (P3, gap analysis 2026-07-16) — ✅ SELESAI
1. ~~P3.2~~ — Badge kategori berwarna di panel kanan — selesai, teks berwarna atas gelap (bukan fill solid, demi kontras)
2. ~~P3.3~~ — Meta row berikon (tanggal/lokasi/institusi via `portOf(ev)`) — selesai
3. ~~P3.4~~ — Era band pada timeline scrubber (`flex-grow` proporsional dari `ERAS_META`) — selesai
4. ~~P3.1~~ — Toolbar eksplorasi mode Peta — selesai, **kecuali** dropdown Rentang Tahun (dicoret, butuh keputusan desain terpisah utk widget range) dan tombol Legenda (dicoret, superseded)
5. **Verifikasi:** **SELESAI** via Playwright — search/filter kategori (navigasi benar-benar tertahan, bukan cuma dot diredupkan)/era-jump/reset semua diverifikasi bekerja end-to-end, tanpa page error. Kontras WCAG AA `.chr-quote` (item terbuka dari Sprint 2) **masih belum diukur numerik** — dibawa ke Sprint 4

### Sprint 4: Footer 5-Kolom + Motion (P3.5 + P2)
6. P3.5 — Footer 5-kolom selalu terlihat (**cek dulu ketersediaan konten** "Dokumen Terbaru"/"Arsip Digital" sebelum build, hindari dead link)
7. P2.1-P2.5 — Motion system (riak, kapal, rute tergambar bertahap — **catatan:** P2.2/P2.3 soal kapal & rute tergambar sudah tidak relevan karena keduanya dihapus per §2c, kemungkinan besar dicoret juga)
8. **Verifikasi:** Full test aksesibilitas + `prefers-reduced-motion`

---

## 9. Kriteria Keberhasilan

Dari audit §19 — target penilaian:

| Aspek | Saat ini | Target | Cara Ukur |
|---|---|---|---|
| Hierarki informasi | 4.5/10 | 9/10 | User test: "Apa peristiwa pertama yang kamu lihat?" → harus tahun + judul |
| Konsistensi ilustrasi | 4/10 | 8.5/10 | Audit visual: semua kapal = 1 gaya, semua node = 3 state |
| Keterbacaan peta | 4/10 | 8.5/10 | Jumlah elemen visible simultan ≤ 12 (dari ~25 saat ini) |
| Editorial polish | 5/10 | 9/10 | Microcopy bahasa Indonesia konsisten, tidak ada data mentah |
| Kesan dirancang manusia | 4.5/10 | 9/10 | Cek §15 checklist: 1 metafora dominan, 1 sistem ilustrasi, ruang kosong sengaja |

**Checklist audit §15 "Terlihat didesain manusia":**
- [ ] Satu metafora dominan (arus kekuasaan Aceh)
- [ ] Satu sistem ilustrasi (engraving konsisten)
- [ ] Informasi muncul berdasarkan konteks
- [ ] Setiap detail visual punya fungsi
- [ ] Ruang kosong mengarahkan perhatian
- [ ] Teks melewati proses editorial
- [ ] Semua elemen dapat dijelaskan maknanya
- [ ] Sebagian besar dekorasi berani dihapus

---

## 10. Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Terlalu banyak pengurangan → tampilan kosong | User bingung tidak ada yang dieksplorasi | Pertahankan 1 rute utama + 5-7 port + 1 kapal — minimalis bukan kosong |
| Sidebar editorial terlalu tinggi | User harus scroll panjang | Batasi 5 era (sudah ada), gunakan scroll snap |
| Panel kanan terlalu banyak teks | User overwhelmed | Gunakan progressive disclosure: ringkasan → kutipan → transkrip |
| SVG path berubah → broken di mobile | Layout rusak | Test di 375px width, pastikan viewBox scale |
| Motion mengganggu pembacaan | User tidak bisa fokus baca | `prefers-reduced-motion` + pause button |

---

## 11. Pertanyaan Terbuka

1. **Kapal dekoratif:** hapus total atau pertahankan dengan opacity sangat rendah (0.08)?
2. **Rhumb lines (kompas portolan):** hapus total atau pertahankan sebagai elemen arsip redup?
3. **Headline era di sidebar:** pertahankan atau pindahkan ke panel kanan?
4. **Treaty highlight (Traktat Painan):** pertahankan treatment khusus atau standardisasi ke format panel lain?
5. **Angka counter "PERISTIWA X / 101":** tampil selalu atau hanya saat hover/focus?
