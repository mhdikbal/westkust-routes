# Audit dan Arah Redesign Ruang Kosong
## Kronik Sejarah Interaktif Berbasis Django dan Tailwind CSS

**Fokus:** Desktop UX/UI  
**Stack:** Django, Tailwind CSS  
**Konteks:** Halaman kronik dengan statistik, kontrol tampilan, daftar era, panggung peta, dan panel peristiwa aktif  
**Tujuan:** Mengubah ruang kosong yang tidak disengaja menjadi ruang fungsional tanpa membuat tampilan kembali padat atau terasa seperti dashboard generik

---

## 1. Ringkasan Eksekutif

Tampilan memiliki fondasi yang kuat: palet gelap, aksen emas, hirarki tiga kolom, sistem era, peta historis, sumber primer, dan kontrol eksplorasi. Masalah utamanya bukan kekurangan ornamen, melainkan beberapa container memiliki ukuran yang jauh lebih besar daripada volume informasi yang ditampung.

Ruang kosong harus dibedakan menjadi dua jenis:

- **Negative space yang sehat:** membantu fokus, memisahkan konteks, dan memberi napas visual.
- **Dead space:** terlihat seperti komponen gagal dimuat, container memiliki tinggi berlebihan, atau layout belum selesai.

Pada tampilan saat ini, dead space paling nyata berada pada:

1. area horizontal di bawah statistik;
2. area peta tengah yang terlalu gelap dan minim konteks;
3. bagian bawah sidebar era;
4. bagian bawah panel peristiwa aktif.

Solusi desain tidak boleh sekadar menambahkan dekorasi. Setiap ruang baru harus mempunyai fungsi yang jelas: mencari, memfilter, menavigasi, menjelaskan, atau memperkuat hubungan antara peristiwa dan peta.

---

## 2. Temuan Visual Utama

### 2.1 Bar statistik

Bar statistik menampilkan:

- 101 peristiwa;
- 4 suksesi;
- 51 perjanjian;
- 21 konflik;
- 7 diplomasi;
- 18 administratif;
- rentang 1600–1775.

Seluruh metrik memiliki ukuran kotak hampir sama, padahal `101 peristiwa` dan `1600–1775` memiliki bobot informasi lebih tinggi daripada kategori lainnya. Bar terlihat seperti ringkasan dashboard BI, belum menjadi alat eksplorasi.

### 2.2 Ruang kosong di bawah statistik

Di bawah statistik terdapat ruang hitam lebar dengan tombol `Tampilan daftar` yang berdiri sendiri. Tinggi area terlalu besar dibanding fungsi tombol. Area tersebut terlihat seperti:

- slot toolbar yang belum selesai;
- komponen filter yang gagal dimuat;
- atau wrapper dengan padding/min-height terlalu besar.

### 2.3 Sidebar era

Sidebar menampilkan lima era. Era pertama memiliki deskripsi panjang, sedangkan empat era berikutnya hanya menampilkan rentang tahun dan judul. Setelah item kelima terdapat ruang kosong sampai dasar viewport.

### 2.4 Panggung peta

Panggung peta merupakan area terbesar, tetapi konteks geografis dan historis terlalu redup. Hanya beberapa titik dan rute diagonal yang terlihat jelas. Ilustrasi laut dan kapal di bagian bawah hampir hilang karena overlay gelap.

### 2.5 Panel peristiwa aktif

Panel kanan memiliki informasi yang baik, tetapi seluruh konten menumpuk di bagian atas. Area bawah panel kosong dan tidak memiliki navigasi peristiwa sebelumnya/berikutnya. Scrollbar internal juga terlihat mentah.

---

## 3. Konsep Redesign

### Nama konsep

**Kronik Navigator**

### Prinsip

> Setiap ruang harus membantu pengguna memahami konteks, membatasi data, atau berpindah ke peristiwa berikutnya.

Redesign mengisi dead space dengan empat fungsi:

1. **Toolbar eksplorasi** di bawah statistik.
2. **Konteks geografi dan legenda kontekstual** pada panggung peta.
3. **Ringkasan periode aktif** pada footer sidebar.
4. **Navigasi peristiwa** pada footer panel kanan.

---

## 4. Struktur Halaman Target

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER                                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│ 101 PERISTIWA · 1600–1775   [Perjanjian 51] [Konflik 21] [Lainnya]          │
├──────────────────────────────────────────────────────────────────────────────┤
│ [PETA] [DAFTAR]  Cari peristiwa...  Kategori ▾  Tahun ▾  Legenda            │
├───────────────┬──────────────────────────────────┬───────────────────────────┤
│ BAB KRONIK    │ PANGGUNG PETA                    │ LEMBAR PERISTIWA          │
│               │                                  │                           │
│ 01 Aktif      │ Peta lebih terang                │ PERISTIWA 01 / 101        │
│ 02            │ Satu rute utama                  │ 1600                      │
│ 03            │ Node relevan                     │ Judul                     │
│ 04            │ Label tidak bertabrakan          │ Ringkasan                 │
│ 05            │ Kapal kontekstual                │ Kutipan                   │
│               │                                  │ Sumber                    │
│───────────────│                                  │                           │
│ PERIODE AKTIF │ Legenda mini                     │───────────────────────────│
│ 1600–1637     │ Timeline scrubber                │ ← Sebelumnya  Berikutnya →│
│ 5 peristiwa   │                                  │                           │
└───────────────┴──────────────────────────────────┴───────────────────────────┘
```

---

## 5. Redesign Area di Bawah Statistik

Area kosong diubah menjadi toolbar setinggi 64–72 px.

### Komponen

- segmented control `Peta / Daftar`;
- pencarian peristiwa, lokasi, atau tokoh;
- filter kategori;
- filter rentang tahun;
- tombol legenda;
- reset filter;
- jumlah hasil aktif.

### Contoh Django Template dan Tailwind

```html
<section
  aria-label="Kontrol eksplorasi kronik"
  class="mx-auto flex min-h-16 max-w-[1840px] items-center
         justify-between gap-4 border-y border-white/10 px-4 py-3"
>
  <div class="flex items-center gap-2">
    <a
      href="?view=map"
      class="rounded-md bg-[#f1e5cc] px-4 py-2 text-xs font-semibold
             uppercase tracking-[0.12em] text-[#17130d]"
    >
      Tampilan peta
    </a>

    <a
      href="?view=list"
      class="rounded-md border border-white/15 px-4 py-2 text-xs
             font-semibold uppercase tracking-[0.12em] text-[#e8dcc4]
             hover:border-[#b78a3a]"
    >
      Tampilan daftar
    </a>
  </div>

  <form method="get" class="flex items-center gap-3">
    <label class="sr-only" for="event-search">Cari peristiwa</label>
    <input
      id="event-search"
      name="q"
      value="{{ request.GET.q }}"
      type="search"
      placeholder="Cari peristiwa, lokasi, atau tokoh..."
      class="w-80 rounded-md border border-white/10 bg-white/[0.04]
             px-4 py-2 text-sm text-[#eee3ce] outline-none
             placeholder:text-white/35 focus:border-[#b78a3a]"
    />

    <select
      name="category"
      class="rounded-md border border-white/10 bg-[#11110f]
             px-3 py-2 text-sm text-[#ddd0b8]"
    >
      <option value="">Semua kategori</option>
      <option value="perjanjian">Perjanjian</option>
      <option value="konflik">Konflik</option>
      <option value="diplomasi">Diplomasi</option>
    </select>

    <button
      type="submit"
      class="rounded-md border border-[#b78a3a]/60 px-4 py-2
             text-xs font-semibold uppercase tracking-[0.12em]
             text-[#e7c981]"
    >
      Terapkan
    </button>
  </form>
</section>
```

---

## 6. Redesign Sidebar Era

Sidebar tetap tenang dan tidak diisi ornamen berlebihan. Bagian bawah digunakan untuk ringkasan periode aktif.

```text
PERIODE AKTIF
1600–1637

5 peristiwa dari 101 catatan

[Lihat seluruh peristiwa era →]
```

### Contoh Tailwind

```html
<aside class="flex min-h-0 flex-col border-r border-white/10 bg-[#080908]">
  <div class="flex-1 overflow-y-auto p-4">
    {% include "chronicle/partials/era_list.html" %}
  </div>

  <footer class="border-t border-white/10 p-4">
    <p class="text-[10px] uppercase tracking-[0.18em] text-[#9b8b6e]">
      Periode aktif
    </p>
    <p class="mt-2 font-serif text-2xl text-[#f0e2c5]">
      {{ active_era.start_year }}–{{ active_era.end_year }}
    </p>
    <p class="mt-1 text-xs leading-5 text-white/45">
      {{ active_era.event_count }} peristiwa dari {{ total_events }} catatan.
    </p>
    <a
      href="{% url 'chronicle:era' active_era.slug %}"
      class="mt-4 inline-block text-xs font-semibold uppercase
             tracking-[0.12em] text-[#c79a45] hover:text-[#e7bf70]"
    >
      Lihat seluruh peristiwa →
    </a>
  </footer>
</aside>
```

---

## 7. Redesign Panggung Peta

Peta tidak perlu diisi lebih banyak ornamen. Peta perlu dibuat lebih terbaca.

### Perubahan

- turunkan kekuatan overlay hitam;
- naikkan kontras garis pantai;
- gunakan satu rute utama aktif;
- tampilkan maksimal lima sampai tujuh node relevan;
- tampilkan satu kapal engraving kontekstual;
- letakkan legenda kecil di kiri bawah;
- letakkan timeline scrubber di bagian bawah;
- gunakan caption peta yang tidak bertumpuk dengan label era.

### Tiga lapisan

```text
LAYER 1 · ATMOSFER
Peta tua, laut, tekstur, dan kapal background.

LAYER 2 · GEOGRAFI
Garis pantai, ekuator, node dasar, dan label utama.

LAYER 3 · PERISTIWA AKTIF
Rute, kapal aktif, riak, anotasi, dan lokasi aktif.
```

### Contoh wrapper Tailwind

```html
<section class="relative min-h-0 overflow-hidden bg-[#111513]">
  <img
    src="{% static 'chronicle/images/west-coast-map.avif' %}"
    alt=""
    aria-hidden="true"
    class="absolute inset-0 h-full w-full object-cover opacity-55"
  />

  <div class="absolute inset-0 bg-black/35"></div>

  <div class="absolute inset-0">
    {% include "chronicle/partials/map_svg.html" %}
  </div>

  <div class="absolute bottom-5 left-5 rounded-md border border-[#b78a3a]/30
              bg-[#080a08]/80 p-4 backdrop-blur-sm">
    {% include "chronicle/partials/map_legend.html" %}
  </div>

  <div class="absolute inset-x-5 bottom-5 ml-64">
    {% include "chronicle/partials/timeline_scrubber.html" %}
  </div>
</section>
```

---

## 8. Redesign Panel Peristiwa

Panel dibagi menjadi tiga zona:

1. identitas peristiwa;
2. narasi dan sumber;
3. navigasi peristiwa.

### Footer navigasi

```text
← Peristiwa sebelumnya      01 / 101      Peristiwa berikutnya →
```

### Contoh Tailwind

```html
<article class="flex min-h-0 flex-col bg-[#0b0907]">
  <header class="px-6 pb-5 pt-6">
    {% include "chronicle/partials/event_header.html" %}
  </header>

  <div class="min-h-0 flex-1 overflow-y-auto px-6 pb-8">
    {% include "chronicle/partials/event_body.html" %}
  </div>

  <footer class="border-t border-[#a77a2e]/20 bg-[#0b0907]/95
                 px-6 py-4 backdrop-blur">
    <div class="flex items-center justify-between">
      <a
        href="{{ previous_event.get_absolute_url }}"
        class="text-xs uppercase tracking-wider text-white/55
               hover:text-[#e5d6b8]"
      >
        ← Sebelumnya
      </a>

      <span class="text-xs text-[#b89a66]">
        {{ event_position|stringformat:"02d" }} / {{ total_events }}
      </span>

      <a
        href="{{ next_event.get_absolute_url }}"
        class="text-xs uppercase tracking-wider text-[#e5d6b8]
               hover:text-[#f3dfb5]"
      >
        Berikutnya →
      </a>
    </div>
  </footer>
</article>
```

---

## 9. Grid Utama

Jangan memakai `h-screen` pada peta jika statistik dan toolbar berada di atasnya. Gunakan tinggi berdasarkan offset aktual.

```css
:root {
  --header-height: 72px;
  --stats-height: 76px;
  --toolbar-height: 64px;
  --top-offset: calc(
    var(--header-height) +
    var(--stats-height) +
    var(--toolbar-height)
  );
}
```

```html
<main
  class="grid min-h-0 grid-cols-[320px_minmax(560px,1fr)_minmax(420px,29vw)]
         border-t border-white/10"
  style="height: calc(100vh - var(--top-offset));"
>
  <aside class="min-h-0 overflow-hidden">...</aside>
  <section class="relative min-h-0 overflow-hidden">...</section>
  <article class="min-h-0 overflow-hidden">...</article>
</main>
```

---

## 10. Statistik sebagai Filter

Statistik kategori diubah menjadi filter yang dapat diklik.

```text
Semua 101
Perjanjian 51
Konflik 21
Administratif 18
Diplomasi 7
Suksesi 4
```

State aktif menggunakan background gading, sedangkan state lain memakai border tipis. Dengan perubahan ini, bar statistik memperoleh fungsi eksplorasi dan tidak lagi terasa seperti dashboard dekoratif.

---

## 11. Prioritas Implementasi

### P0 · Perbaikan layout

1. Kurangi ruang kosong bawah statistik menjadi toolbar 64–72 px.
2. Periksa dan hapus `h-screen`, `min-h-screen`, `h-[900px]`, `py-12`, atau margin besar yang tidak perlu.
3. Gunakan `height: calc(100vh - var(--top-offset))` pada grid utama.
4. Tambahkan footer navigasi pada panel peristiwa.
5. Tambahkan summary footer pada sidebar.

### P1 · Perbaikan panggung peta

1. Kurangi overlay hitam.
2. Naikkan kontras garis pantai dan node aktif.
3. Tampilkan satu rute utama.
4. Tampilkan maksimal lima sampai tujuh node relevan.
5. Tambahkan legenda kontekstual.
6. Tambahkan timeline scrubber.
7. Pastikan caption tidak bertumpuk dengan label era.

### P2 · Peningkatan UX

1. Jadikan statistik sebagai filter.
2. Tambahkan pencarian.
3. Tambahkan filter kategori dan tahun.
4. Sinkronkan URL dengan event aktif.
5. Sediakan navigasi sebelumnya/berikutnya.
6. Pertahankan state filter melalui query parameter Django.

---

## 12. Kriteria Keberhasilan

Redesign dianggap berhasil apabila:

- tidak ada area yang terlihat seperti komponen gagal dimuat;
- toolbar dapat dipahami dalam tiga detik;
- pengguna dapat mencari dan memfilter peristiwa;
- peta tetap menjadi pusat pengalaman;
- sidebar tidak terasa kosong walau hanya memiliki lima era;
- panel kanan terasa selesai karena memiliki footer navigasi;
- elemen dekoratif tidak ditambahkan hanya untuk mengisi ruang;
- layout 1366 px, 1440 px, dan 1920 px tetap proporsional;
- keyboard focus dan screen reader tetap didukung;
- state pencarian dan filter dapat dibagikan melalui URL.

---

## 13. Kesimpulan

Masalah utama bukan kekurangan konten. Masalahnya adalah ukuran container dan distribusi informasi tidak sesuai dengan kebutuhan aktual.

Perbaikan yang tepat adalah:

- mengubah ruang kosong bawah statistik menjadi toolbar eksplorasi;
- memperjelas peta, bukan menambah dekorasi;
- memberi footer fungsional pada sidebar;
- memberi footer navigasi pada panel peristiwa;
- dan mengatur tinggi grid berdasarkan offset bagian atas.

> **Ruang kosong yang sehat membantu pengguna berfokus. Ruang kosong yang tidak disengaja membuat aplikasi terlihat belum selesai. Redesign harus memberi setiap ruang alasan untuk ada.**
