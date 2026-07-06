# PRD: Integrasi Data Pelayaran Abad 17 dari Daghregister Batavia

**Status:** Draft spec — belum diimplementasikan, belum ada perubahan skema/kode
**Disusun:** 2026-07-06
**Konteks:** turunan riset thesis (`docs/thesis/chapter-plan-sia-kualitatif-kritis.md`), tapi ini spec level aplikasi westkust-routes, bukan dokumen akademik

---

## 1. Latar Belakang

Sumber data pelayaran VOC yang sudah ada di westkust-routes (`scrawling/Data_BGS_Sumatra_Full.json`, 4.700+ record) berasal dari database terstruktur Huygens KNAW (Bookhouder-Generaal Batavia/BGB) — setiap field (kapal, kargo, nilai gulden) sudah bersih sejak sumbernya.

Selama sesi riset thesis, 13 jilid *Dagh-register gehouden int Casteel Batavia* (1661-1681) diproses lewat notebook Colab (`docs/thesis/colab/daghregister_extraction.ipynb`): scan kata kunci → verifikasi + terjemahan via LLM (sumopod/GPT). Hasilnya, `docs/thesis/dr/daghregister_corpus.csv`, berisi 282 entri naratif (bukan tabel terstruktur) yang di antaranya menyinggung pelayaran dengan detail kapal/kargo/nilai — tapi diekstrak dari teks bebas oleh LLM dan regex, bukan dari database yang sudah terstruktur.

**Pertanyaan produk:** apakah dan bagaimana data ini masuk ke aplikasi westkust-routes, mengingat provenance dan tingkat kepercayaannya berbeda jauh dari data BGB yang sudah ada?

## 2. Temuan Kualitas Data (Wajib Dibaca Sebelum Desain)

| Aspek | Kondisi |
|---|---|
| Cakupan jilid | 6 dari 13 jilid (1661, 1663, 1664, 1665, 1666-1667, 1668-1669) — **7 jilid (1670-1671, 1676-1681) tidak punya lapisan OCR sama sekali**, perlu OCR ulang sebelum bisa diproses |
| Total entri terverifikasi | 282 (dari scan awal, sudah difilter relevansi + diterjemahkan) |
| Entri yang terlihat sbg catatan pelayaran (kapal+kargo) | 119 dari 282 (42%) |
| Ekstraksi nama kapal otomatis (regex) | 38 dari 119 (32%) — sisanya perlu ekstraksi manual/LLM tambahan |
| Ekstraksi nilai gulden otomatis (regex) | 66 dari 119 (55%) |
| Arah pelayaran eksplisit dalam teks | 49 dari 119 (32 keluar dari Sumatra, 17 ke Sumatra); 70 entri tidak eksplisit |
| Struktur kargo | Teks bebas per entri, TIDAK ternormalisasi jadi item per baris seperti `CargoItem` yang ada |
| Tingkat kepercayaan | Ekstraksi LLM (`gpt-5` via sumopod) — belum divalidasi manusia sama sekali (berbeda dari korpus VOC utama yang sudah lewat validasi kappa manual) |

**Kesimpulan kualitas:** data ini *jauh* lebih mentah dari `Data_BGS_Sumatra_Full.json`. Memaksakannya langsung ke tabel `voyages` production tanpa lapisan validasi akan mencemari data yang sudah bersih dengan record yang confidence-nya tidak diketahui.

## 3. Keputusan Desain

**TIDAK menggabungkan langsung ke tabel `voyages`/`cargo_items` production.** Sebagai gantinya, diusulkan model staging terpisah, mengikuti pola arsitektur yang sudah ada (JSON sumber → `seed_data.py` → DB — lihat CLAUDE.md "Data Historis").

### 3.1 Tabel Baru: `daghregister_voyages` (staging)

```python
class DaghregisterVoyage(Base):
    __tablename__ = "daghregister_voyages"

    id = Column(Integer, primary_key=True, index=True)
    volume = Column(String(100), nullable=False, index=True)       # nama file jilid sumber
    book_page_start = Column(Integer, nullable=True)
    book_page_end = Column(Integer, nullable=True)
    tanggal_perkiraan = Column(String(50), nullable=True)          # teks tanggal asli, mis. "16 EN 17 FEBRUARIUS" -- BELUM dinormalisasi ke ISO date

    ship_name_raw = Column(String(200), nullable=True)             # hasil regex, BISA NULL
    direction_raw = Column(String(30), nullable=True)               # "keluar"/"masuk"/null
    cargo_text = Column(Text, nullable=True)                        # teks kargo mentah, belum di-parse jadi CargoItem
    value_gulden_raw = Column(Float, nullable=True)                 # hasil regex, BISA NULL

    text_indonesia = Column(Text, nullable=False)                   # hasil terjemahan LLM
    text_belanda_asli = Column(Text, nullable=True)                 # teks sumber

    extraction_method = Column(String(50), nullable=False, default="regex+llm_v1")
    confidence_flag = Column(String(20), nullable=False, default="unverified")  # unverified | reviewed | promoted | rejected
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(String(30), nullable=True)

    # kalau reviewer memutuskan record ini valid & lengkap, boleh di-link ke voyage resmi setelah promosi manual
    promoted_to_voyage_id = Column(Integer, ForeignKey("voyages.id"), nullable=True)
```

Field `confidence_flag` adalah mekanisme utama: semua data masuk sebagai `unverified`. Hanya record yang direview manusia (`reviewed`) dan dinyatakan lengkap boleh naik status jadi `promoted` — barulah *itu* yang ditulis ulang secara manual (bukan otomatis) sebagai baris baru di tabel `voyages`/`cargo_items` resmi, dengan `source_url` menunjuk ke jilid Daghregister asal.

### 3.2 Kenapa Bukan Langsung ke `voyages`

1. **Provenance berbeda** — `voyages.source_url` saat ini semua mengarah ke BGB Huygens (database terstruktur). Mencampur record hasil ekstraksi LLM tanpa penanda akan membingungkan siapa pun yang audit data nanti (termasuk reviewer thesis).
2. **Field wajib tidak lengkap** — `Voyage.ship_name` adalah `nullable=False`, tapi 68% kandidat Daghregister belum berhasil diekstrak nama kapalnya. Memaksakan nilai default akan menyembunyikan ketidaklengkapan data.
3. **Kargo tidak ternormalisasi** — `CargoItem` mengharapkan baris per produk (produk, qty, unit, nilai). Teks Daghregister butuh parsing tambahan (kemungkinan LLM lagi) untuk dipecah jadi baris-baris begitu, dan itu pekerjaan terpisah dari sekadar "menyimpan data".
4. **Belum ada validasi manusia** — beda dengan korpus VOC utama thesis yang sudah lewat pengkodean manual (Cohen's kappa dihitung), Daghregister voyage extraction ini murni output LLM tanpa spot-check.

## 4. Alur Kerja (Workflow)

```
1. [Sudah ada] Colab notebook scan + verifikasi + terjemahan -> daghregister_corpus.csv
2. [Baru] Skrip Python: parse daghregister_corpus.csv -> insert ke daghregister_voyages (confidence_flag=unverified)
3. [Manual, di luar kode] Reviewer (user) buka dashboard/query sederhana, filter yang ada ship_name_raw + value_gulden_raw lengkap,
   spot-check terhadap teks asli, ubah confidence_flag jadi 'reviewed' atau 'rejected'
4. [Baru] Skrip promosi: untuk confidence_flag='reviewed' yang dikonfirmasi lengkap, tulis ulang manual sbg Voyage + CargoItem resmi,
   isi promoted_to_voyage_id di baris staging
```

## 5. Test Plan (sesuai TDD wajib CLAUDE.md)

Sebelum implementasi:
1. `backend/tests/test_daghregister_voyages.py` — test model `DaghregisterVoyage` (CRUD dasar, constraint `confidence_flag` hanya menerima 4 nilai valid)
2. Test endpoint GET `/api/daghregister-voyages?confidence_flag=unverified` — filter berjalan benar
3. Test skrip parsing CSV→DB — pastikan idempotent (re-run tidak duplikasi baris untuk `volume`+`book_page_start` yang sama)
4. Test promosi: memindahkan 1 record `reviewed` ke `voyages` tidak merusak `voyage_ref` uniqueness constraint yang ada

## 6. Keputusan & Yang Masih Terbuka

**Sudah diputuskan (2026-07-06):** fitur ini untuk **keduanya** — data pendukung thesis (Bab 3/4/5) DAN memperkaya aplikasi peta westkust-routes yang publik. Implikasi: begitu record staging naik status `promoted`, ia otomatis tampil di peta publik (via tabel `voyages`/`cargo_items` resmi yang sudah dipakai frontend) — bukan cuma dokumen thesis yang terpisah dari aplikasi. Aplikasi peta sendiri (dengan pin pelayaran Daghregister 1661-1669 yang sudah dipromosikan) berpotensi jadi salah satu artefak/figur yang dirujuk di Bab 4/5 thesis nanti — mengikuti pola yang sudah ada di mini research Salido sebelumnya ("Gambar 1. Aplikasi Westkust Routes"). Konsekuensi tambahan: karena hasil `promoted` akan publik, ambang kualitas review manual sebelum promosi harus lebih ketat daripada sekadar "cukup untuk sitasi thesis" — data yang salah di peta publik lebih sulit diperbaiki diam-diam dibanding di draft akademik.

**Masih terbuka:**
1. Apakah endpoint API baru (`/api/daghregister-voyages`) perlu dibuat sekarang, atau cukup tabel + skrip import dulu (tanpa expose ke frontend) sampai ada record yang `promoted`?
2. Siapa yang melakukan review manual (`confidence_flag` unverified→reviewed) — user sendiri, atau dibuatkan tool bantu (mis. skrip CLI interaktif)?
3. Prioritas: selesaikan dulu OCR 7 jilid yang kosong sebelum bangun pipeline ini, atau jalan paralel dengan data yang sudah ada (6 jilid, 282 entri)?
4. Perlu ditandai di peta publik (mis. warna/legend beda) bahwa pin dari Daghregister berbeda provenance dari pin BGB Huygens yang sudah ada, supaya pengguna aplikasi tahu tingkat kepastian datanya berbeda?
