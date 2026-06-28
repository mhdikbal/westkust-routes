# Kerangka Thesis: IETPD × UMKM Digital × Opini Hefrizal Handra

**Disusun:** 2026-06-24  
**Konteks:** Thesis S2 Magister Terapan SIA + Lomba Karya Tulis BI Sumatera Barat

---

## Artikel Rujukan

**Judul:** Produktivitas, Pertumbuhan, atau Pemerataan? Refleksi dari Sumatera Barat  
**Penulis:** Hefrizal Handra (Ekonom Universitas Andalas)  
**Tanggal:** 4 April 2026  
**Tag:** #Desentralisasi #KeuanganDaerah #EkonomiDaerah

### Ringkasan Argumen Utama

1. **Paradoks Sumbar:** Gini ratio turun (0,331 → 0,282, Maret 2016–2025) tetapi pertumbuhan PDRB melambat konsisten (5,8% → 3,4%).
2. **"Pemerataan karena perlambatan":** Ketimpangan turun bukan karena kelompok bawah naik, melainkan karena kelompok atas tidak lagi tumbuh. Merata, tapi pada tingkat kesejahteraan rendah.
3. **Struktur tradisional:** Ekonomi Sumbar didominasi pertanian, perdagangan kecil, usaha mikro — merata tapi produktivitas rendah; sektor nilai tambah tinggi belum berkembang.
4. **Kelas menengah produktif belum tumbuh:** Gini rendah bisa jadi indikasi, bukan prestasi.
5. **Solusi Hefrizal:** Pertumbuhan berkualitas = produktivitas + inklusivitas. Belanja fiskal daerah harus diarahkan pada program yang meningkatkan kapasitas ekonomi masyarakat.

### Data Kunci dari Artikel

| Indikator | 2016 | 2025 |
|---|---|---|
| Gini ratio gabungan | 0,331 | 0,282 |
| Gini ratio perkotaan | 0,353 | 0,307 |
| Gini ratio perdesaan | 0,288 | 0,232 |
| Pertumbuhan PDRB | ~5,3% | 3,4% |

---

## Elaborasi: Tiga Konsep yang Saling Mengunci

```
Hefrizal (makro):  Sumbar = "pemerataan karena perlambatan"
                    → butuh pertumbuhan berkualitas (produktivitas + inklusif)
                             ↓
IETPD (meso):      instrumen BI untuk elektronifikasi ekosistem daerah
                    → proxy "kualitas belanja fiskal daerah" yang produktif
                    → katalis ekosistem digital payment → UMKM lebih produktif
                             ↓
d'Besto (mikro):   UMKM digital-first, multi-kabupaten, data longitudinal
                    → studi kasus empiris: apakah adopsi digital = resiliensi?
```

---

## Mekanisme Transmisi IETPD → UMKM

IETPD tinggi bukan hanya soal efisiensi pemda, tapi menciptakan **spillover ke ekosistem swasta**:

1. Pemda aktif dorong QRIS/non-tunai → merchant/UMKM lokal onboard ekosistem digital
2. Konsumen terbiasa bayar digital → barrier transaksi turun → volume transaksi naik
3. Pemda dengan IETPD tinggi cenderung lebih cepat salurkan program pembiayaan UMKM
4. Data transaksi digital lebih lengkap → forecasting bisnis lebih akurat

Untuk d'Besto: cabang di kabupaten IETPD tinggi vs. rendah memiliki kondisi ekosistem berbeda — ini bisa dikontrol sebagai **variabel moderating** dalam model panel FE.

---

## Posisi Riset dalam Tiga Lapisan

| Lapisan | Isi | Sumber |
|---|---|---|
| **Konteks makro** | Sumbar = pemerataan semu, pertumbuhan melambat | Hefrizal Handra (2026) + BPS |
| **Variabel ekosistem** | IETPD per kabupaten = kualitas digital-fiskal lokal | BI Sumbar (publikasi tahunan) |
| **Unit analisis** | 13 cabang d'Besto, 168+ observasi panel tidak seimbang | Data internal dbesto |
| **Hipotesis utama** | UMKM digital-first lebih resilient terhadap perlambatan ekonomi | Estimasi FE panel + SARIMAX |
| **Kontribusi** | Bukti mikro bahwa digitalisasi UMKM = jalur produktivitas inklusif | Bab 4–5 thesis |

---

## Hipotesis Riset

**H1:** Elastisitas omset UMKM F&B terhadap pertumbuhan PDRB lokal berbeda antara kabupaten dengan IETPD tinggi dan rendah (efek moderating IETPD).

**H2:** UMKM yang mengadopsi sistem informasi akuntansi berbasis data menunjukkan stabilitas omset lebih tinggi dibanding benchmark UMKM konvensional pada periode perlambatan ekonomi.

**H3:** Inflasi lokal memiliki efek demand destruction (koef < 1) pada omset nominal, dan efek ini lebih lemah di kabupaten dengan IETPD tinggi.

---

## Hook Kalimat Bab 1 Thesis

> *"Di tengah paradoks Sumatera Barat — ketimpangan turun namun pertumbuhan melambat — penelitian ini mengajukan pertanyaan: apakah adopsi sistem informasi akuntansi berbasis data pada UMKM kuliner, dalam ekosistem daerah yang diukur melalui Indeks Elektronifikasi Transaksi Pemerintah Daerah (IETPD), mampu menjadi jalur produktivitas inklusif yang diadvokasi oleh literatur pembangunan daerah?"*

---

## Relevansi untuk Lomba BI Sumbar

Bank Indonesia mendorong IETPD sebagai instrumen pembangunan ekosistem ekonomi digital daerah. Penelitian ini memberikan **evidensi empiris** bahwa IETPD berdampak nyata bukan hanya pada efisiensi pemda, tetapi pada performa UMKM di wilayahnya — menghubungkan kebijakan elektronifikasi BI dengan kesejahteraan unit usaha terkecil.

Pertanyaan yang dijawab: *seberapa jauh elektronifikasi yang diukur BI berdampak ke bawah, sampai ke warung dan franchise lokal?*

---

## Catatan Metodologi Terkait

- IETPD per kabupaten tersedia dari publikasi tahunan BI Sumbar (Kajian Ekonomi dan Keuangan Regional / KEKR)
- Diperlukan variasi IETPD antar kabupaten tempat cabang beroperasi (Pasaman Barat, Solok, Bukittinggi, dst.)
- Jebakan: IETPD dan PDRB per kapita bisa kolinear — perlu uji VIF sebelum masuk model bersamaan
- Lihat `fase5_market_share_ietpd_colab.txt` untuk pipeline Colab terkait

---

## Dokumen Terkait
- `roadmap-proyeksi-ekonomi-umkm.md` — keputusan metodologi panel FE dikunci 19 Jun 2026
- `panel_mixedeffects_colab.txt` — pipeline panel FE aktual
- `fase5_market_share_ietpd_colab.txt` — pipeline IETPD yang sudah ada
- Memory: `project_thesis_proyeksi_umkm.md`
