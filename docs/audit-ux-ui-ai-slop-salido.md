# Audit UX/UI Senior Manager
## Mengapa Tampilan Kronik Salido Terasa seperti “AI Slop”

**Produk:** Kronik sejarah interaktif Salido  
**Frontend:** AstroJS  
**Konteks evaluasi:** Tampilan desktop tiga kolom yang menampilkan era sejarah, visualisasi peta Pantai Barat Sumatra, dan detail peristiwa aktif  
**Tujuan dokumen:** Mengidentifikasi penyebab kesan “AI slop” dan menetapkan arah perbaikan visual yang terukur

---

## 1. Ringkasan Eksekutif

Kesan pertama terhadap tampilan saat ini memang mengarah pada **“AI slop”**, walaupun fondasi konsepnya sebenarnya kuat. AstroJS bukan penyebab masalah tersebut. Kesan itu muncul karena terlalu banyak ide visual dimasukkan ke satu layar tanpa proses kurasi, pengurangan, dan penyatuan bahasa desain.

> **AI slop dalam konteks ini adalah tampilan yang memiliki banyak elemen menarik secara individual, tetapi secara keseluruhan terasa seperti hasil prompt yang belum melewati keputusan desain manusia yang tegas.**

Masalah utamanya bukan sekadar jumlah elemen, melainkan tidak adanya hierarki yang jelas antara:

- informasi utama;
- data pendukung;
- dekorasi;
- status aktif;
- konteks historis;
- navigasi;
- dan sumber primer.

Tampilan saat ini mencoba menyampaikan peta, kapal, arus, riak, orbit, rute, kompas, era, kutipan, sumber, kategori, dan interaksi sekaligus. Hasilnya kaya secara visual, tetapi miskin fokus.

---

## 2. Temuan Berdasarkan Tampilan

Tampilan terdiri dari tiga bidang utama:

1. **Kolom kiri** berisi daftar era sejarah.
2. **Bidang tengah** berisi peta Sumatra, jalur perdagangan, node pelabuhan, kapal, riak, orbit, dan elemen kartografi.
3. **Kolom kanan** berisi detail peristiwa aktif tahun 1600, judul kontrak perdagangan, metadata, kutipan sumber, status verifikasi, dan tombol tindakan.

Elemen visual yang terlihat pada bidang tengah meliputi:

- pusat kekuasaan Aceh dengan lingkaran konsentris;
- garis rute berwarna emas;
- beberapa garis putus-putus paralel;
- jejak berbentuk blok kecil;
- garis panah kecil di sepanjang pesisir;
- orbit berbentuk elips;
- kompas;
- label besar “SUMATRA”;
- label lokasi Singkil, Barus, Nias, Natal, Air Bangis, Tiku, Pariaman, Padang, Bayang, Salido, Painan, dan Air Haji;
- kapal besar sebagai background;
- beberapa kapal putih sebagai foreground;
- garis ekuator;
- layer peta sejarah;
- dan pembatas garis pantai.

Secara visual, elemen-elemen tersebut saling bersaing untuk menjadi pusat perhatian.

---

## 3. Terlalu Banyak Metafora Dijalankan Bersamaan

Tampilan menggabungkan terlalu banyak metafora visual:

- peta tua;
- kapal dagang;
- rute perdagangan;
- riak kekuasaan;
- orbit;
- arus;
- kompas;
- garis pesisir;
- timeline era;
- panel arsip;
- kutipan primer;
- badge kategori;
- dan tombol aksi.

Masalahnya bukan bahwa elemen tersebut tidak relevan. Masalahnya adalah semua elemen ditampilkan dengan bobot visual yang hampir sama.

Pengguna akhirnya tidak mengetahui apakah pusat pengalaman adalah:

1. peta Sumatra;
2. perjalanan kapal;
3. pengaruh Aceh;
4. daftar era;
5. peristiwa aktif;
6. atau dokumen sumber primer.

### Keputusan desain yang lebih tajam

Gunakan hierarki metafora berikut:

- **Metafora utama:** arus kekuasaan dari Aceh.
- **Metafora sekunder:** jalur perdagangan.
- **Elemen pendukung:** kapal, pelabuhan, dan sumber primer.

Riak, orbit, panah, kompas, jejak, dan garis putus-putus tidak harus muncul dalam satu state yang sama.

---

## 4. Peta Tengah Terlalu Sibuk

Bidang tengah seharusnya menjadi pusat pengalaman, tetapi saat ini terlalu padat.

Pengguna melihat sekaligus:

- banyak garis emas paralel;
- garis putus-putus;
- blok kecil seperti jejak;
- garis tipis abu-abu;
- lingkaran konsentris Aceh;
- orbit elips di laut;
- panah kecil sepanjang pesisir;
- beberapa kapal putih;
- banyak label lokasi;
- garis batas Sumatra;
- kapal background;
- dan peta bertekstur gelap.

Tidak ada pemisahan yang cukup tegas antara:

- data aktif;
- data historis;
- dekorasi;
- background;
- rute utama;
- rute sekunder;
- dan status interaksi.

### Gejala khas AI slop

AI cenderung menerjemahkan “pengalaman yang kaya” sebagai “semakin banyak simbol semakin baik”. Desain profesional justru membangun kekayaan melalui seleksi, ritme, dan penghilangan.

### Rekomendasi

Dalam satu state peristiwa, tampilkan maksimal:

- satu rute utama aktif;
- satu atau dua rute sekunder dengan opacity rendah;
- satu kapal utama;
- lima sampai tujuh pelabuhan relevan;
- satu pusat riak kekuasaan;
- satu legenda kontekstual.

Elemen yang tidak relevan harus disembunyikan atau diredupkan.

---

## 5. Bahasa Ilustrasi Kapal Tidak Konsisten

Terdapat setidaknya tiga gaya kapal:

1. kapal besar realistis atau engraving pada background kiri;
2. kapal putih kecil seperti ikon piksel;
3. kapal putih besar seperti clip-art pada area Tiku–Pariaman.

Ketiga gaya tersebut tidak berasal dari satu sistem ilustrasi. Kapal putih terlihat ditempel di atas peta, bukan menjadi bagian dari dunia visual yang sama.

Kapal putih berukuran besar juga terlalu terang sehingga merebut perhatian dari pelabuhan dan rute aktif.

### Rekomendasi

Gunakan satu sistem ilustrasi kapal:

- seluruh kapal dibuat dalam gaya engraving;
- gunakan satu warna off-white atau emas kusam;
- ketebalan garis konsisten;
- kapal aktif sedikit lebih terang;
- ukuran kapal memiliki makna interaksi;
- background kapal besar hanya berfungsi sebagai atmosfer;
- hindari ikon kapal putih bergaya aplikasi atau clip-art.

---

## 6. Sidebar Kiri Terlihat seperti Panel Admin

Bagian **ERA SEJARAH** menggunakan pola yang menyerupai:

- radio button;
- stepper formulir;
- filter dashboard;
- sidebar dokumentasi;
- atau progress checkout.

Pola tersebut tidak mendukung pengalaman kronik sejarah. Pengguna terasa sedang memilih opsi, bukan menjelajahi bab sejarah.

Era aktif juga mempunyai deskripsi lebih panjang daripada era lainnya. Perbedaan tinggi konten membuat ritme vertikal tidak stabil.

### Rekomendasi

Ubah daftar era menjadi daftar bab editorial:

```text
01
1600–1637

KONTRAK PERTAMA
DAN KEKUASAAN
ISKANDAR MUDA
```

Era berikutnya:

```text
02
1641–1650

RATU ATJEH DAN
PUNCAK KEKUASAAN
```

Gunakan garis perjalanan vertikal dan nomor bab. Hilangkan radio button.

---

## 7. Panel Kanan Terasa seperti Detail Drawer Generik

Struktur panel kanan sebenarnya logis:

- label peristiwa aktif;
- tahun;
- judul;
- kategori;
- tanggal dan tokoh;
- kutipan;
- referensi;
- tombol tindakan.

Namun komposisi tersebut masih terasa seperti detail drawer dari dashboard.

Penyebabnya:

- ruang kosong bawah terlalu besar;
- semua konten menumpuk di atas;
- tahun berdiri sendiri tanpa hubungan kuat dengan judul;
- badge kategori terlalu kecil dan generik;
- tombol hitam solid terasa administratif;
- kutipan memakai kotak krem standar;
- scrollbar terlihat mentah;
- panel lebar tetapi pemanfaatan ruangnya lemah.

### Struktur editorial yang disarankan

```text
PERISTIWA 01 / 12

1600
────────────

Kontrak Dagang Lada Pertama
VOC–Aceh

PERJANJIAN · PERDAGANGAN

Desember 1600
Aceh Darussalam

Ringkasan editorial peristiwa.

SUMBER PRIMER
“Kutipan sumber...”

Cornick van Atchijn
Arsip CD1 · halaman 47
Status verifikasi

[Baca transkrip]
Tampilkan pada peta →
```

Tahun, judul, kutipan, dan sumber harus menjadi satu komposisi editorial, bukan kumpulan komponen terpisah.

---

## 8. Sistem Tipografi Belum Disutradarai

Tampilan menggunakan banyak treatment tipografi:

- serif tebal pada judul era;
- sans-serif tebal ber-outline pada label peta;
- sans-serif geometrik pada tahun 1600;
- serif pada judul peristiwa;
- italic serif pada kutipan;
- sans-serif bold pada tombol;
- condensed uppercase pada label periode.

Kombinasi serif dan sans-serif sebenarnya tepat, tetapi penerapannya belum memiliki batas yang jelas. Tampilan terasa seperti campuran peta sejarah, dashboard data, majalah editorial, poster sinematik, dan game strategi.

### Sistem yang lebih disiplin

Gunakan hanya:

- **EB Garamond:** tahun, judul peristiwa, kutipan, dan narasi.
- **Space Grotesk:** navigasi, label lokasi, metadata, kategori, dan tombol.

Batasi menjadi:

- maksimal lima ukuran utama;
- maksimal tiga bobot font;
- satu sistem tracking label;
- satu sistem line-height narasi;
- satu sistem halo label peta yang halus.

---

## 9. Garis Rute Tampak seperti Efek, Bukan Informasi

Banyak garis berasal dari Aceh menuju Pantai Barat, tetapi pengguna sulit membedakan maknanya.

Garis tersebut dapat ditafsirkan sebagai:

- rute kapal;
- jangkauan kekuasaan;
- arus laut;
- izin dagang;
- hubungan diplomatik;
- atau batas geografis.

Garis-garis terlihat kompleks, tetapi tidak menghasilkan keterbacaan data yang setara.

### Semantik visual yang disarankan

- **Garis emas solid:** pengaruh politik Aceh.
- **Garis tembaga putus:** rute VOC.
- **Garis biru tinta tipis:** perdagangan lokal.
- **Riak konsentris:** intensitas pusat kekuasaan.
- **Node emas:** pelabuhan aktif.
- **Node putih:** pelabuhan terkait.
- **Node abu-abu:** lokasi tidak relevan dengan event aktif.

Sediakan satu legenda yang konsisten di seluruh era.

---

## 10. Label Lokasi Bertabrakan

Bagian selatan peta menampilkan banyak label yang rapat:

- Tiku;
- Pariaman;
- Padang;
- Bayang;
- Salido;
- Painan;
- Air Haji.

Beberapa label berada pada baseline yang hampir sama. Kapal putih besar juga menutupi jalur di area tersebut.

Hal ini menunjukkan bahwa data lokasi sudah diletakkan pada peta, tetapi belum melalui proses penempatan label kartografis yang matang.

### Rekomendasi

- Tampilkan label yang relevan dengan event aktif.
- Lokasi lain cukup ditampilkan sebagai node.
- Tampilkan label tambahan saat hover atau keyboard focus.
- Gunakan deteksi benturan sederhana.
- Letakkan label bergantian di sisi kiri dan kanan garis pantai.
- Gunakan leader line tipis pada area yang padat.

---

## 11. Background dan Data Tidak Terpisah

Background peta dan kapal sangat gelap. Data overlay menggunakan emas gelap dan abu-abu sehingga beberapa elemen kehilangan kontras.

Contoh masalah:

- tulisan besar “SUMATRA” terlalu redup untuk menjadi informasi tetapi terlalu terlihat untuk dianggap dekorasi;
- orbit elips tidak mempunyai makna yang jelas;
- kompas berimpit dengan garis dan kapal;
- jalur emas hilang ketika melewati background yang terang atau padat.

### Gunakan tiga lapisan visual

```text
LAYER 1 · ATMOSFER
Kapal background, tekstur peta, gelombang, dan vignette.

LAYER 2 · GEOGRAFI
Garis pantai, node dasar, label utama, dan ekuator.

LAYER 3 · PERISTIWA AKTIF
Rute, kapal aktif, riak, lokasi aktif, dan anotasi.
```

Ketika event aktif, layer atmosfer harus lebih redup dan layer peristiwa harus paling tajam.

---

## 12. Tidak Ada Focal Point yang Stabil

Saat tampilan dibuka, perhatian pengguna dapat berpindah ke:

1. pusat riak Aceh;
2. kapal putih besar;
3. angka 1600;
4. judul peristiwa;
5. kapal background;
6. label Sumatra;
7. era aktif.

Focal path yang ideal:

1. tahun dan judul peristiwa;
2. lokasi aktif pada peta;
3. rute yang menjelaskan hubungan;
4. konteks era;
5. sumber primer.

Tampilan harus disutradarai mengikuti urutan tersebut.

---

## 13. Proporsi Tiga Kolom Terasa Mekanis

Pembagian tiga kolom secara fungsional masuk akal, tetapi garis pemisah vertikal yang keras membuat antarmuka terasa seperti enterprise dashboard.

### Rekomendasi

- Hindari dua panel putih permanen di kedua sisi peta.
- Gunakan warna kertas berbeda yang lebih halus.
- Panel kanan dapat sedikit menumpuk ke peta seperti lembar arsip.
- Kurangi batas vertikal keras.
- Gunakan layering, bukan shadow tebal.
- Panel kanan dapat menyempit saat eksplorasi peta.
- Panel kanan dapat melebar saat membaca sumber.
- Kolom kiri dapat menjadi rail yang lebih ringan.

Layout harus merespons tugas pengguna, bukan hanya mempertahankan grid statis.

---

## 14. Microcopy Terlihat seperti Data Mentah

Format berikut terlihat seperti payload database:

```text
vol. CD1 · hlm. 47 (19–20) · unverified
```

Masalahnya:

- penggunaan bahasa bercampur;
- istilah teknis muncul langsung;
- status verifikasi tidak dijelaskan;
- format sumber belum editorial;
- `Aceh` dan `Atjeh` berpotensi dipakai tidak konsisten.

### Rekomendasi

Gunakan bahasa Indonesia pada antarmuka:

```text
STATUS SUMBER
Belum diverifikasi silang

Arsip CD1
Halaman 47, baris 19–20
```

Aturan editorial:

- Gunakan **Aceh** pada narasi modern.
- Gunakan **Atjeh** hanya dalam kutipan atau nama historis sumber.
- Gunakan tanda baca dan kapitalisasi secara konsisten.
- Pisahkan fakta sumber dari interpretasi editorial.

---

## 15. Perbedaan “Dibuat AI” dan “AI-Assisted Design”

### Terlihat dibuat AI

- Banyak simbol muncul sekaligus.
- Dekorasi dianggap sebagai informasi.
- Semua metafora divisualisasikan.
- Gaya ikon tidak konsisten.
- Ruang kosong tidak dipakai secara sengaja.
- Data mentah ikut tampil.
- Tidak ada keputusan tentang apa yang harus disembunyikan.
- Tema sejarah diterjemahkan menjadi peta tua, kapal, emas, kompas, serif, dan tekstur sekaligus.

### Terlihat didesain manusia dengan bantuan AI

- Satu metafora dominan.
- Satu sistem ilustrasi.
- Informasi muncul berdasarkan konteks.
- Setiap detail visual mempunyai fungsi.
- Ruang kosong mengarahkan perhatian.
- Teks melewati proses editorial.
- Semua elemen dapat dijelaskan maknanya.
- Sebagian besar dekorasi berani dihapus.

---

## 16. Prioritas Pembenahan

### P0 · Hilangkan kesan slop

1. Hapus 50–60% garis rute yang terlihat bersamaan.
2. Hilangkan kapal putih bergaya clip-art.
3. Gunakan satu gaya kapal engraving.
4. Tampilkan hanya lokasi yang relevan dengan event aktif.
5. Hilangkan orbit elips tanpa makna langsung.
6. Kurangi panah kecil di sepanjang pesisir.
7. Tetapkan satu focal point per state.
8. Ubah status `unverified` menjadi status editorial bahasa Indonesia.

### P1 · Bangun sistem visual

1. Tetapkan semantik warna dan garis.
2. Tetapkan sistem ukuran kapal dan node.
3. Batasi sistem tipografi.
4. Ubah sidebar kiri menjadi daftar bab kronik.
5. Ubah panel kanan menjadi lembar arsip editorial.
6. Buat legenda kontekstual yang dapat dibuka dan ditutup.
7. Pisahkan layer atmosfer, geografi, dan peristiwa aktif.

### P2 · Tambahkan motion setelah desain statis matang

1. Riak Aceh bergerak sangat lambat.
2. Satu kapal bergerak pada rute aktif.
3. Rute tergambar secara bertahap.
4. Panel sumber muncul seperti tinta yang tersibak.
5. Perubahan era memudarkan layer lama.
6. `prefers-reduced-motion` wajib didukung.

---

## 17. Arah Wireframe yang Lebih Matang

```text
┌──────────────┬──────────────────────────────────┬──────────────────────┐
│ BAB KRONIK   │ PETA AKTIF                       │ LEMBAR PERISTIWA     │
│              │                                  │                      │
│ 01           │  Satu pusat Aceh                 │ PERISTIWA 01 / 12    │
│ 1600–1637    │  Satu riak                       │                      │
│              │  Satu rute utama                 │ 1600                 │
│ Kontrak dan  │  Satu kapal konsisten            │                      │
│ Kekuasaan    │  5–7 node relevan                │ Kontrak Dagang       │
│              │                                  │ Lada Pertama         │
│              │             ○ Barus              │                      │
│ 02           │        ◉ Aceh                    │ Ringkasan            │
│ 1641–1650    │             ╲                    │ Kutipan              │
│              │              ╲ ○ Painan          │ Sumber               │
│              │                                  │                      │
│              │ [Legenda]      [Fokus lokasi]    │ [Baca transkrip]     │
└──────────────┴──────────────────────────────────┴──────────────────────┘
```

---

## 18. Sistem Visual Target

### Ilustrasi

- Kapal: engraving satu warna.
- Peta: tekstur redup sebagai atmosfer.
- Node: lingkaran sederhana dengan tiga state.
- Rute: maksimal tiga jenis garis bermakna.
- Riak: hanya untuk pusat kekuasaan aktif.
- Kompas: hanya tampil sebagai dekorasi redup atau di legenda, bukan di tengah data aktif.

### Warna

```text
Ink Black       #18150F
Archive Paper   #F3EAD9
Paper Deep      #DFCFB2
Aceh Gold       #A77A2E
VOC Copper      #8B4030
Sea Ink         #14282A
Muted Ink       #6F675A
```

### Tipografi

```text
EB Garamond
Tahun, judul, narasi, kutipan

Space Grotesk
Navigasi, label, metadata, kategori, tombol
```

---

## 19. Target Penilaian setelah Redesign

| Aspek | Saat ini | Target |
|---|---:|---:|
| Konsep historis | 8/10 | 9/10 |
| Atmosfer | 8/10 | 9/10 |
| Hierarki informasi | 4.5/10 | 9/10 |
| Konsistensi ilustrasi | 4/10 | 8.5/10 |
| Keterbacaan peta | 4/10 | 8.5/10 |
| Editorial polish | 5/10 | 9/10 |
| Kesan dirancang manusia | 4.5/10 | 9/10 |

---

## 20. Kesimpulan

Fondasi konsep Salido tidak buruk. Ide tentang kekuasaan Aceh, jalur perdagangan, pelabuhan Pantai Barat, dan sumber primer justru mempunyai potensi yang sangat kuat.

Masalahnya adalah tampilan mencoba membuktikan semua gagasan visual sekaligus:

- peta;
- kapal;
- arus;
- riak;
- orbit;
- rute;
- kompas;
- era;
- kutipan;
- sumber;
- dan animasi.

Belum ada creative direction yang cukup tegas untuk mengatakan:

> **Elemen ini penting, elemen ini harus diam, elemen ini hanya muncul dalam konteks tertentu, dan elemen ini harus dihapus.**

AstroJS hanyalah media implementasi. Solusinya bukan menambah library, efek, atau animasi. Solusinya adalah menjalankan satu putaran **radical subtraction**, menyatukan sistem ilustrasi, memperjelas semantik data, mengedit microcopy, dan mengembalikan fokus kepada:

1. satu peristiwa;
2. satu rute utama;
3. satu lokasi aktif;
4. dan satu sumber primer pada satu waktu.

> **Tujuan akhirnya bukan membuat antarmuka terlihat lebih ramai atau lebih sinematik, melainkan membuat sejarah lebih mudah dipahami, ditelusuri, dan dipercaya.**
