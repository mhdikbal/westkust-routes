# Pariaman/Priaman Episode Dossier (Draft) — REWRITE v2

> **DRAFT MECHANISM DOSSIER**
> **NOT PRODUCTION DATA**
> **NO MODEL MARK AUTHORIZED**
> **RESEARCHER REVIEW REQUIRED**
> **NOT_READY_FOR_DEPLOYMENT**

---

## 1. Scope and Revision History

Dokumen ini **MENGGANTIKAN** `PARIAMAN_EPISODE_DOSSIER_DRAFT.md` versi lama
(1671-1712, berbasis `linimasa_events.csv` baris [51],[55],[66],[68],[93]).
Versi lama **STALE** — ditulis sebelum process-tracing 1705-1713 dan audit
Westenenk sesi ini. **Isi versi lama TIDAK DIHAPUS** — diarsipkan penuh di
§13 (Appendix — Dossier Lama Diarsipkan) sebagai bukti koreksi, sesuai
instruksi "jangan menghapus bukti koreksi".

**Perubahan cakupan utama**: dossier lama memperlakukan "regenten Priaman"
sbg SATU aktor kolektif berkelanjutan 1671-1712 (episode tunggal
`EP-PARIAMAN-01`). Dossier ini **membongkar** asumsi itu — cakupan
dipersempit ke **1705-1713** (periode yang sudah diproses-tracing langsung
dari GM/Daghregister sesi ini) dan memisahkan SEMBILAN entitas berbeda yang
sebelumnya berisiko dilebur di bawah label "Priaman"/"regenten Priaman".
Periode 1671-1704 (dossier lama) **TIDAK direvisi dalam dokumen ini** — di
luar cakupan process-tracing yang tersedia; lihat §13.

**Koreksi pasca-verifikasi identitas (turn terpisah, setelah rewrite awal
dossier ini)**: Verifikasi identitas terdedikasi menyimpulkan
`different_persons_supported`, confidence `high`, untuk pasangan
**Maharadja Indra** vs **Mara Laout**. Temuan: (a) Maharadja Indra diangkat
"door dese Tafel" (dewan VOC) sbg panglima radja 1705, TAPI dibunuh di
Batavia **SEBELUM sempat menjabat** (GM 06/p0713.xml, 1711, kutipan literal:
*"voor 't bekleden des gesz. ampts al hier is vermoord geworden"*); (b)
**Mara Laout** adalah PENGGANTINYA — adik Maharadja Indra menurut buku
*Padang Abad XVII-XVIII* (Ikbal 2024, footnote 142) — yang justru MENJABAT
AKTIF sbg panglima Padang sejak 13 Agustus 1705 (CD4 DCXXXII, "verkoren
panglima"), tercatat masih aktif Nov 1706 (mengajukan izin perjalanan ke
Batavia, ditolak — GM 06/p0415.xml, dokumen yg SAMA yg juga melaporkan
jenazah Maharadja Indra tiba di Padang pd tanggal yg sama); (c) **kedua
actor_id TIDAK di-merge** — dipertahankan terpisah tegas sesuai keputusan
verifikasi. Seluruh rujukan ke "Maharadja Indra dibunuh saat menjabat" di
draft awal dossier ini (§3, §6, §13, §17 versi sebelumnya) **DIKOREKSI** di
bagian-bagian terkait di bawah — bukti draft lama TIDAK dihapus, ditandai
`[KOREKSI]` di tempatnya.

**Sumber tambahan yang diintegrasikan**: `WESTENENK_NAGARI_PAGARUYUNG_AUDIT.md`
(struktur Pagaruyung/rantau, dipakai HANYA sbg konteks pembanding utk klaim
Saruaso 1711 — lihat Guard di §9), `LEGAL_INSTITUTIONAL_EVENT_LAYER_DRAFT.md`
(konsep `representative_capacity_mismatch`).

**Tidak ada sumber baru dicari untuk dossier ini** — seluruh isi berasal dari
process-tracing yang sudah dilakukan sesi ini (`PROCESS TRACING PRIAMAN
1705-1713` dan `PENCARIAN TERARAH GM/DAGHREGISTER` turn-turn sebelumnya).

---

## 2. Source Inventory

| # | Collection | document_id | document_date | Dibaca | Fungsi dalam dossier ini |
|---|---|---|---|---|---|
| S1 | GM | 06/p0406.xml | 31 Mar 1706 | Penuh | Konteks ketidakpatuhan Priaman/Bayang dekat P. Cinco |
| S2 | GM | 06/p0415.xml | 30 Nov 1706 | Penuh | Teguran kolektif Pauh/Priaman/Kota Tengah |
| S3 | GM | 06/p0732.xml | 18 Feb 1711 | Penuh | Aktivitas Siry Amar (Tiku), Priaman sbg mitra |
| S4 | GM | 06/p0713.xml | 1711 | Penuh | Klaim kedaulatan Manicabos Vorst atas Padang; kematian Maharadja Indra |
| S5 | CD4 | idx399 (traktat 1712) | 1712 | Penuh (sesi sebelumnya) | Karakterisasi `trouwloosheyd en misleydinge sommiger regenten` |
| S6 | GM | 06/p0897.xml | 13 Jan 1713 | Penuh | Ekspedisi laut, pengusiran "de vijanden", pembakaran |
| S7 | GM | 07/p0003.xml | 20 Nov 1713 | Penuh | Konfirmasi independen kedua ekspedisi 1713; Radja Soeroewassa menolak mediator |
| S8 | GM | 07/p0136.xml | 14 Jan 1715 | Penuh | Administratif rutin (sakit-penyakit) — `no_relevant_evidence` |
| S9 | DR-1680 | hal.723-727 | 24 Agu 1680 (lapor 1 Nov 1680) | Penuh (sesi Sillida, direferensi ulang) | Figur "Radja moderna di Serwassa" — kandidat identitas Soeroewassa 1713 |

`documents_read`: 9 (termasuk 1 referensi-ulang lintas-episode S9).
`candidate_passages`: 9 (satu per dokumen, tidak ada dokumen dgn >1 klaim
independen dalam cakupan dossier ini).
`included_findings`: 9. `excluded_findings`: 0 (S8 disertakan sbg bukti
negatif eksplisit, bukan dibuang).

---

## 3. Verified Chronology

| Tahun | Peristiwa | Sumber | Karakter bukti |
|---|---|---|---|
| 1706 (31 Mar) | Laporan ketidakpatuhan "Maleyers van Priaman, Bayang en andere" dekat P. Cinco | S1 | Laporan, tanpa tindakan konkret disebut |
| 1706 (30 Nov) | Teguran tertulis kolektif kepada kepala **Pauh, Priaman, Kota Tengah** — dagang gelap dgn penyelundup Aceh | S2 | Surat teguran tertulis (bukan tindakan militer) |
| 1711 (18 Feb) | Hoofdpongoulou **Siry Amar** (Tiku) melarang pedagang pakai pas VOC, mengancam 2 pongoulou tetangga, liga dgn Aceh; Priaman disebut mitra ("samenspand"), BUKAN pelaku utama | S3 | Tindakan konkret, PELAKU UTAMA = Tiku |
| 1711 | "Manicabos Vorst" klaim kedaulatan atas Padang via kredensial palsu, ditolak kolektif "gezamentlijke Padangse regenten"; laporan mengenang kembali Maharadja Indra (diangkat panglima radja Padang 1705, **`[KOREKSI]` dibunuh di Batavia SEBELUM sempat menjabat**, BUKAN "saat menjabat") | S4 | Peristiwa terpisah, LOKASI = Padang, bukan Priaman; identitas Maharadja Indra vs Mara Laout SUDAH diverifikasi terpisah (`different_persons_supported`) |
| 1712 | Traktat baru Priaman — karakterisasi *"trouwloosheyd en misleydinge sommiger regenten"* — tanpa insiden spesifik dikutip | S5 | Karakterisasi retorik traktat, TANPA tindakan konkret dilampirkan |
| 1713 (sblm 13 Jan) | Ekspedisi laut ~249 personel tiba "over zee tot Priaman", "de vijanden" melarikan diri, negeri/benteng dibakar 4-6 mil | S6 | Tindakan konkret nyata, aktor musuh TIDAK disebut nama |
| 1713 (20 Nov) | Konfirmasi independen kedua: permintaan pengembalian 2 batu nisan yg dirampas dlm "jongste expeditie tot Priaman"; **Radja Soeroewassa** tetap bermusuhan, menolak mediator netral, berbaris ke arah Pauh | S7 | Laporan independen KEDUA, menguatkan S6 sbg SATU peristiwa, bukan dua |

---

## 4. Actor Ledger

```
actor_id: A01_PRIAMAN_LOCATION
name_as_written: "Priaman" / "Priamansche" / "tot Priaman"
location: Pantai Barat Sumatra, distrik Priaman
office_or_title: NOT APPLICABLE — ini LABEL LOKASI, bukan aktor
source_characterization: label geografis dipakai VOC utk menunjuk wilayah/comptoir
concrete_action: NOT APPLICABLE
relationship_to_Priaman: NOT APPLICABLE (identik)
relationship_to_Tiku: bertetangga geografis, distrik terpisah
relationship_to_Saruaso: NOT APPLICABLE — tidak ada rujukan langsung dlm dokumen VOC yg dibaca
actor_identity_status: NOT APPLICABLE — bukan aktor
evidence_status: NOT APPLICABLE
```

```
actor_id: A02_KEPALA_PRIAMAN_1706
name_as_written: "de hoofden van Pauh, Priaman en Kota Tengah" (kolektif, tak bernama individu)
location: Priaman (salah satu dari 3 lokasi yg ditegur bersama)
office_or_title: "hoofd" (kepala) — tak dirinci lebih jauh (panglima/pounglou/lain)
source_characterization: surat resmi Gubernur Jenderal & Raad (S2)
concrete_action: TIDAK ADA tindakan aktor ini yg dicatat langsung — hanya OBJEK teguran
relationship_to_Priaman: adalah salah satu dari 3 kepala yg ditegur bersama, tidak identik dgn "Priaman" scr keseluruhan
relationship_to_Tiku: tidak disebut
relationship_to_Saruaso: tidak disebut
actor_identity_status: collective_actor_ambiguous
evidence_status: primary_source_verified (utk keberadaan teguran), cannot_determine (utk identitas individu)
```

```
actor_id: A03_SIRY_AMAR
name_as_written: "hoofdpongoulou Siry Amar"
location: TIKU (bukan Priaman)
office_or_title: hoofdpongoulou (kepala pongoulou) — jabatan lokal bernama eksplisit
source_characterization: surat resmi VOC (S3)
concrete_action: melarang pedagang bebas pakai pas VOC; mengancam 2 pongoulou tetangga; membentuk liga dgn Aceh
relationship_to_Priaman: MITRA ("samenspand met die van Priaman"), BUKAN identik dgn Priaman, BUKAN penduduk/pejabat Priaman
relationship_to_Tiku: adalah pejabat Tiku itu sendiri — identik
relationship_to_Saruaso: tidak disebut dalam sumber yg dibaca
actor_identity_status: identity_verified (utk nama & jabatan), TAPI relasinya ke Priaman tetap faction_level_continuity paling tinggi (mitra, bukan identitas sama)
evidence_status: primary_source_verified
```

```
actor_id: A04_PAUH_LOCATION
name_as_written: "Pauh"
location: distrik terpisah, disebut bersama Priaman & Kota Tengah 1706; disebut lagi 1713 (arah gerak Soeroewassa)
office_or_title: NOT APPLICABLE — label lokasi
source_characterization: S2, S7
concrete_action: NOT APPLICABLE
relationship_to_Priaman: ditegur BERSAMA, lokasi berbeda
relationship_to_Tiku: tidak disebut
relationship_to_Saruaso: 1713 — Soeroewassa "berbaris ke arah Pauh" (S7), relasi ANCAMAN, bukan kepemilikan/pemerintahan
actor_identity_status: NOT APPLICABLE — bukan aktor
evidence_status: primary_source_verified (utk keberadaan rujukan)
```

```
actor_id: A05_KOTO_TANGAH_LOCATION
name_as_written: "Kota Tengah" (ejaan GM 1706 — CATATAN: berbeda ejaan dari "Koto Tangah" yg dipakai di dossier/schema lain sesi ini; TIDAK diasumsikan otomatis lokasi identik tanpa verifikasi geografis tambahan)
location: distrik terpisah, disebut bersama Priaman & Pauh 1706
office_or_title: NOT APPLICABLE — label lokasi
source_characterization: S2
concrete_action: NOT APPLICABLE
relationship_to_Priaman: ditegur BERSAMA, lokasi berbeda
relationship_to_Tiku: tidak disebut
relationship_to_Saruaso: tidak disebut
actor_identity_status: NOT APPLICABLE — bukan aktor
evidence_status: cannot_determine — kesamaan "Kota Tengah" (S2) dgn "Koto Tangah" yg dibahas di dossier Padang lain sesi ini BELUM diverifikasi sbg lokasi yg sama persis
```

```
actor_id: A06_SARUASO_SOEROEWASSA
name_as_written: "Radja Soeroewassa" (S7, 1713) / "Radja moderna di Serwassa" (S9, 1680, kandidat identitas sama, BELUM PASTI)
location: dugaan wilayah pegunungan/Minangkabau interior (bukan pesisir Priaman)
office_or_title: "Radja" — gelar politik, TIDAK disamakan dgn jabatan Pagaruyung/Basa Ampek Balai manapun tanpa bukti langsung
source_characterization: S7 (surat resmi VOC, 1713); S9 (Daghregister, 1680, kejadian berbeda — pemaksaan pembakaran loji Priaman)
concrete_action: 1713 — menolak mediator netral, berbaris ke arah Pauh, tetap bermusuhan; 1680 (jika identik) — memaksa orang Priaman/Cottatenga membakar loji VOC di bawah ancaman
relationship_to_Priaman: figur EKSTERNAL yg berulang MENGANCAM/MEMAKSA Priaman, BUKAN bagian dari struktur pemerintahan Priaman itu sendiri
relationship_to_Tiku: tidak disebut
relationship_to_Saruaso: identik dgn dirinya sendiri (entri ini)
actor_identity_status: **identity_mismatch / cannot_determine** — kesamaan nama lintas 33 tahun (1680→1713) BELUM dikonfirmasi tekstual langsung, bisa jadi konvergensi transliterasi kebetulan
evidence_status: primary_source_verified (utk keberadaan kedua rujukan terpisah), cannot_determine (utk kontinuitas identitas antar keduanya)
```

```
actor_id: A07_SOMMIGER_REGENTEN
name_as_written: "sommiger regenten" (traktat 1712, S5)
location: Priaman (dokumen Priaman-spesifik)
office_or_title: "regenten" — istilah kolektif VOC, TIDAK dirinci individu
source_characterization: badan traktat 1712 (primary_treaty_text)
concrete_action: **TIDAK ADA** — traktat hanya memuat karakterisasi retorik ("trouwloosheyd en misleydinge"), tanpa insiden spesifik dilampirkan
relationship_to_Priaman: SUBSET tak-teridentifikasi dari regent Priaman ("sommiger" = "beberapa", eksplisit BUKAN seluruh regent) — guard ditegakkan: TIDAK disamakan dgn seluruh regenten Priaman
relationship_to_Tiku: TIDAK ADA rujukan eksplisit ke Siry Amar/Tiku dalam teks traktat
relationship_to_Saruaso: TIDAK ADA rujukan
actor_identity_status: **collective_actor_ambiguous**
evidence_status: primary_treaty_text_verified (utk keberadaan frasa), cannot_determine (utk identitas individu di baliknya)
```

```
actor_id: A08_DE_VIJANDEN_1713
name_as_written: "de vijanden" (S6, 1713)
location: tidak disebut eksplisit — hanya "over zee tot Priaman" sbg titik pendaratan VOC
office_or_title: tidak disebut
source_characterization: surat resmi VOC (S6), dikonfirmasi independen S7
concrete_action: melarikan diri saat pendaratan VOC; negeri/benteng miliknya dibakar
relationship_to_Priaman: **TIDAK DAPAT DIPASTIKAN** — Priaman disebut sbg TITIK PENDARATAN pasukan VOC, bukan sbg identitas musuh itu sendiri; guard ditegakkan: TIDAK diasumsikan = regent Priaman/penandatangan traktat 1712 tanpa bukti eksplisit
relationship_to_Tiku: tidak disebut
relationship_to_Saruaso: **KANDIDAT** identitas sama dgn A06 (Radja Soeroewassa), berdasar kedekatan tematik (permintaan kembalikan nisan dirampas + Soeroewassa bermusuhan di surat yg sama S7) — BELUM konfirmasi tekstual langsung
actor_identity_status: **collective_actor_ambiguous**, dgn kandidat identitas parsial ke A06
evidence_status: primary_source_verified (utk tindakan itu sendiri), cannot_determine (utk identitas pelaku)
```

```
actor_id: A09_VOC_ACTORS
name_as_written: "Hofman" (komandan ekspedisi 1713, S6); "gezaghebber Sumatra's Westkust" (penandatangan traktat 1712, S5); "Radja Gagaralam" (perantara negosiasi nisan 1713, S7 — status VOC/sekutu tak eksplisit, dicatat terpisah)
location: institusional VOC, beroperasi lintas comptoir Pantai Barat
office_or_title: Hofman = komandan ekspedisi (109 Eropa + 100 Bugis + 40 pelaut, S6); gezaghebber = pejabat administratif tertinggi VOC Pantai Barat
source_characterization: surat resmi VOC, kedua sumber (S5, S6)
concrete_action: Hofman — memimpin ekspedisi laut 1713; gezaghebber — menandatangani traktat 1712
relationship_to_Priaman: pihak EKSTERNAL (VOC), bertindak DI/TERHADAP Priaman, bukan bagian struktur lokal Priaman
relationship_to_Tiku: tidak disebut langsung terhadap Tiku dalam dokumen yg dibaca dossier ini
relationship_to_Saruaso: berhadapan dgn A06 via negosiasi (S7, penolakan mediator oleh Soeroewassa)
actor_identity_status: identity_verified (Hofman, jabatan+nama eksplisit)
evidence_status: primary_source_verified
```

**Catatan Radja Ebrahim (di luar cakupan langsung dossier ini, dicatat sbg guard eksplisit)**: process-tracing Sillida/Salido sesi ini (interval 1681-82) membuktikan ada DUA Radja Ebrahim berbeda pada periode berdekatan — satu di **Baros** (naik takhta damai 1681, DR-1681 p.343-362) dan satu di **Priaman** (dideportasi komandan pasca-kerusuhan, DR-1680 hal.723). **Dossier ini TIDAK memasukkan Radja Ebrahim ke actor ledger 1705-1713** karena rujukan yg ditemukan berasal dari periode 1680-1681, DI LUAR cakupan 1705-1713 yang diminta — dicatat di sini HANYA sbg guard eksplisit agar tidak disamakan jika muncul lagi di sumber lanjutan.

---

## 5. Documentary Claims

**S2 (30 Nov 1706)**:
> *"het wantrouwen tegen de V.O.C. blijft er... vooral in Priaman, daar... handelt men met Atjehse sluikers... men zal de hoofden van Pauh, Priaman en Kota Tengah... schrijven om ze tot hun plicht te brengen"*

`claim_type: factual_assertion`. Kecurigaan menetap KHUSUS di Priaman
(disebut eksplisit "vooral"), tapi TEGURAN dikirim ke TIGA kepala sekaligus.

**S3 (18 Feb 1711)**:
> *"Ticouw... behertigende niet anders als de sluyk- en roofvaard, waarin met die van Priaman... samenspand... schadelijke ligues met d'Atchinders"*

`claim_type: factual_assertion`. Tiku = subjek kalimat (pelaku aktif);
Priaman = objek preposisi "met" (mitra kerja sama), bukan pelaku aktif dalam
struktur kalimat ini.

**S5 (1712, traktat)**: Kutipan literal frasa karakterisasi TIDAK tersedia
lengkap dari process-tracing sesi ini di luar frasa `"trouwloosheyd en
misleydinge sommiger regenten"` sendiri (dicatat berulang di turn
sebelumnya, tanpa konteks kalimat penuh dikutip). **`NOT AVAILABLE`** untuk
kalimat lengkap — dicatat sbg celah bukti (lihat §16).

**S6 (13 Jan 1713)**:
> *"met 's Comp.s overige magt... over zee tot Priaman soude aengekomen sijn... De vijanden... over hals en kop de vlugt landwaard"*

`claim_type: factual_assertion`. "Priaman" = titik pendaratan pasukan
("aengekomen sijn"), bukan penanda identitas musuh. "De vijanden" = subjek
tindakan lari, tanpa nama.

**S7 (20 Nov 1713)**:
> *"de 2 graffsteenen, welke in de jongste expeditie tot Priaman veroverd... weder derwaarts mogten gezonden werden"*

`claim_type: factual_assertion`. Mengonfirmasi S6 sbg SATU ekspedisi yg
sama ("jongste expeditie" = ekspedisi terbaru, tunggal), bukan dua kejadian
terpisah.

**S9 (24 Agu 1680, direferensi ulang)**:
> *loji VOC Priaman dibakar, Radja Ebrahim [Priaman] dideportasi; pelaku mengaku dipaksa "orang pegunungan di bawah Simoetoealangh dari Manicabo" bersumpah setia ke "Radja moderna di Serwassa"*

Dipakai HANYA sbg kandidat identitas A06, dgn `temporal_projection_risk`
eksplisit — jeda 33 tahun ke 1713.

---

## 6. Historical Events

| historical_event_id | Deskripsi | documentary_report_id | Tanggal |
|---|---|---|---|
| HE-PRM-01 | Laporan ketidakpatuhan Priaman/Bayang dekat P. Cinco | S1 | 31 Mar 1706 |
| HE-PRM-02 | Teguran tertulis kolektif Pauh/Priaman/Kota Tengah | S2 | 30 Nov 1706 |
| HE-PRM-03 | Tindakan Siry Amar (Tiku): larangan pas dagang, ancaman, liga Aceh | S3 | ~1710-18 Feb 1711 |
| HE-PRM-04 | Klaim kedaulatan Manicabos Vorst atas Padang; kematian Maharadja Indra (**`[KOREKSI]` meninggal SEBELUM menjabat panglima radja, bukan saat menjabat; Mara Laout = pengganti/adiknya, aktor terpisah, TIDAK di-merge**) | S4 | 1711 (Padang, BUKAN Priaman — dicatat sbg konteks regional, lihat §9) |
| HE-PRM-05 | Traktat Priaman baru, karakterisasi `trouwloosheyd en misleydinge sommiger regenten` | S5 | 1712 |
| HE-PRM-06 | **Ekspedisi laut Priaman: pendaratan, pengusiran musuh, pembakaran** | S6 + S7 (2 documentary_report utk 1 historical_event — lihat §8) | sblm/skitar 13 Jan 1713 |

**Total historical_event dalam cakupan dossier**: **6** (HE-PRM-01 s.d.
HE-PRM-06), dgn HE-PRM-04 secara eksplisit ditandai LOKASI PADANG (bukan
Priaman) — disertakan HANYA sbg konteks regional yg relevan bagi klaim
Saruaso/Minangkabau, TIDAK dihitung sbg "event Priaman" dalam penghitungan
mekanisme §10.

**Total documentary_report dalam cakupan dossier**: **9** (S1-S9, lihat §2).

---

## 7. Parent-Child Episode Structure

```
parent_episode_id: PRIAMAN_1705_1713_ADMINISTRATIVE_SEQUENCE
  child_event_id: HE-PRM-01, HE-PRM-02, HE-PRM-03, HE-PRM-05, HE-PRM-06
  # HE-PRM-04 TIDAK dimasukkan sbg child — lokasi Padang, bukan Priaman;
  # dicatat di parent_episode TERPISAH:

parent_episode_id: PADANG_1711_SOVEREIGNTY_DISPUTE (di luar cakupan dossier
  ini, hanya dirujuk sbg context, TIDAK dielaborasi lebih jauh)
  child_event_id: HE-PRM-04

regional_episode_id: SAROEWASSA_RECURRING_THREAT_1680_1713 (BELUM
  DIKONFIRMASI — lihat A06, actor_identity_status cannot_determine)
  candidate_child_events: [Sillida/Priaman 1680 kejadian pembakaran loji
    (di luar cakupan temporal dossier ini, hanya direferensi), HE-PRM-06]

documentary_report_id: S6, S7 → historical_event_id: HE-PRM-06 (SATU event,
  DUA laporan — lihat §8 Deduplication Risks)
```

---

## 8. Tiku–Priaman Relations

| Field | Nilai |
|---|---|
| Aktor pelaku utama 1711 | Siry Amar (Tiku) — bukan Priaman |
| Peran Priaman dalam kalimat sumber | Objek preposisi "met" (mitra kerja sama dgn Tiku), BUKAN subjek tindakan |
| Tindakan konkret atas nama Priaman sendiri | **TIDAK ADA** dalam S3 |
| Guard ditegakkan | Tindakan Siry Amar (larangan pas dagang, ancaman, liga Aceh) TIDAK diatribusikan ke "regent Priaman" — dicatat eksplisit sbg tindakan TIKU dgn Priaman sbg mitra sekunder |
| Implikasi bagi HE-PRM-05 (traktat 1712) | Traktat 1712 adalah dokumen PRIAMAN-SPESIFIK, tapi aktor konkret paling jelas periode 1706-1712 (Siry Amar) berasal dari TIKU — kesenjangan ini adalah dasar `representative_capacity_mismatch` (lihat §11) |
| Status hubungan Transisi 1→2 (Teguran 1706 → Aktivitas Tiku 1711) | **`chronology_only`**, dgn flag **`actor_identity_conflict`** |

---

## 9. Saruaso/Pagaruyung Claims

```
claimed_authority: Radja Soeroewassa (1713) — jenis kewenangan yang
  DIKLAIM tidak dirinci dalam teks VOC; VOC hanya mencatat penolakan
  mediasi dan gerakan militer ke arah Pauh

genealogical_or_dynastic_claim: cannot_determine — tidak ada teks VOC yang
  merinci silsilah/klaim keturunan Soeroewassa dalam sumber yg dibaca
  dossier ini

diplomatic_claim: not_testable — tidak ada catatan negosiasi/korespondensi
  diplomatik LANGSUNG dari Soeroewassa sendiri dalam sumber yg dibaca;
  yang tercatat hanya deskripsi VOC ttg PENOLAKAN mediasi

direct_governing_authority: NOT ESTABLISHED
  # Guard ditegakkan: TIDAK ada bukti tekstual bahwa Soeroewassa memerintah
  # HARIAN wilayah manapun di Priaman/Pauh — hanya bukti tindakan MILITER
  # (bermusuhan, berbaris, menolak mediasi). Sesuai definisi
  # `direct_governing_authority` di LEGAL_INSTITUTIONAL_EVENT_LAYER_DRAFT.md
  # §5 poin 5, kewenangan pemerintahan langsung memerlukan bukti PENEGAKAN
  # keputusan harian, bukan sekadar tindakan bermusuhan.
```

**Guard temporal (WAJIB)**: Struktur Pagaruyung/Basa Ampek Balai/rantau yang
dideskripsikan `WESTENENK_NAGARI_PAGARUYUNG_AUDIT.md` (ditulis ~1918,
berbasis tambo & memori administratif akhir abad 19-20) **TIDAK
diproyeksikan** ke tahun 1711/1713. Tidak ada dokumen VOC dalam dossier ini
(S1-S9) yang merujuk "Pagar Roejoeng", "radjo alam", atau "Basa Ampek
Balai" secara eksplisit. Kemiripan nama "Soeroeaso" (kedudukan Indomo,
Westenenk idx33) dgn "Soeroewassa"/"Serwassa" (VOC, 1680/1713) **dicatat
sbg KEMUNGKINAN KEBETULAN TRANSLITERASI**, BUKAN sbg bukti bahwa
Soeroewassa 1713 = Indomo dari Soeroeaso. Status: **`cannot_determine`**,
`temporal_projection_risk: retrospective_ethnographic_only` jika hubungan
ini kelak dipakai — TIDAK dipakai dalam mekanisme assessment §10.

**Manicabos Vorst (HE-PRM-04, konteks Padang, bukan Saruaso)**: klaim
kedaulatan via "kredensial palsu" ditolak KOLEKTIF oleh "gezamentlijke
Padangse regenten" — ini bukti LANGSUNG bahwa struktur lokal Padang MAMPU
menolak klaim otoritas eksternal yg tak sah, KONSISTEN dgn temuan Westenenk
Passage 2/6 (nagari otonom, vorst tak bisa menegakkan kepatuhan) — TAPI
peristiwa ini terjadi DI PADANG, bukan Priaman, dan TIDAK dielaborasi lebih
jauh dalam dossier ini (di luar cakupan lokasi).

---

## 10. Regent and Representative-Capacity Problem

| Titik | Istilah tertulis | Cakupan yg DIKLAIM | Cakupan yg DAPAT DIBUKTIKAN | `representative_capacity_mismatch` |
|---|---|---|---|---|
| 1706 (S2) | "de hoofden van Pauh, Priaman en Kota Tengah" | 3 kepala kolektif | Hanya keberadaan surat teguran; tak ada nama individu | `interpretive_candidate` — cakupan kolektif tanpa nama, tak bisa diverifikasi cakupan riil |
| 1711 (S3) | "die van Priaman" (mitra Tiku) | Tak dirinci — "orang-orang Priaman" scr umum | Tak ada nama/jabatan individu Priaman yg disebut bertindak | `interpretive_candidate` — istilah generik "die van X" tanpa jabatan formal |
| 1712 (S5) | "sommiger regenten" | EKSPLISIT dibatasi ("sommiger" = beberapa/sebagian) | TIDAK ADA nama individu; TIDAK ADA insiden spesifik dilampirkan pada frasa ini | `interpretive_candidate` — kesenjangan antara istilah VOC ("regenten", collective legal designation) dan bukti konkret di baliknya paling tajam di titik ini |
| 1713 (S6/S7) | "de vijanden" | Tak diklaim scr eksplisit = regent Priaman | Tindakan konkret ADA (lari, benteng dibakar), tapi IDENTITAS pelaku tak dibuktikan = penandatangan traktat 1712 | `interpretive_candidate` — risiko tertinggi konflasi lokasi-tindakan dgn identitas-pelaku |

**Kesimpulan §10**: Di **SELURUH** 4 titik utama 1706-1713, TIDAK SATU PUN
menghasilkan `representative_capacity: documented_mandate` untuk "regent
Priaman" sbg entitas tunggal — pola yang konsisten menunjukkan istilah VOC
("regenten", "sommiger regenten", "de vijanden") secara sistematis TIDAK
disertai bukti identitas individual yang dapat diverifikasi silang dengan
tindakan konkret. Ini adalah **temuan struktural**, bukan kegagalan
pencarian — konsisten dgn hasil process-tracing sesi ini (`Ringkasan Akhir`
poin 4: "Tidak ada satu pun tindakan konkret yang secara eksplisit
dilakukan oleh regent Priaman sendiri").

---

## 11. Mechanism Assessment

```
administrative_aggregation:
  status: interpretive_only
  rationale: Pola yg konsisten dgn VOC menggabungkan BEBERAPA ancaman/aktor
    berbeda (Tiku via Siry Amar, klaim kedaulatan Manicabos Vorst di Padang,
    kemungkinan Soeroewassa) ke bawah SATU label administratif "Priaman"/
    "sommiger regenten" — TAPI proses agregasi itu sendiri TIDAK
    didokumentasikan langsung (tak ada surat VOC yg menyatakan "kami
    menggabungkan X, Y, Z menjadi kategori Priaman") — ini INFERENSI
    peneliti dari POLA, bukan pernyataan tekstual eksplisit.
  NOT_upgraded_to_supported: benar — identitas aktor & proses agregasi
    belum terbukti langsung, sesuai batas yg diwajibkan instruksi.

representative_capacity_mismatch:
  status: interpretive_candidate
  rationale: Lihat §10 — pola konsisten di 4/4 titik, tapi sbg KATEGORI
    baru (lihat LEGAL_INSTITUTIONAL_EVENT_LAYER_DRAFT.md §6 pertanyaan 1),
    belum divalidasi sbg mechanism_status formal di luar dossier ini.

political_reconfiguration:
  status: partially_supported
  rationale: HE-PRM-04 (Manicabos Vorst, klaim ditolak) dan kemunculan
    berulang Soeroewassa (1680→1713, TAPI identitas belum pasti)
    menunjukkan ADA pergolakan struktur otoritas regional yg nyata di
    sekitar Priaman — tapi tidak cukup teridentifikasi utk disebut
    `supported` penuh krn locus TEPATnya (Padang vs Priaman vs pegunungan)
    tetap kabur.

strategic_resistance:
  status: not_supported
  rationale: Tidak satu pun tindakan konkret yg terdokumentasi secara
    eksplisit dilakukan oleh regent Priaman/penandatangan traktat 1712
    sendiri — aktor konkret yg teridentifikasi (Siry Amar/Tiku,
    kemungkinan Soeroewassa) BUKAN pihak yg menandatangani traktat 1712.

defection:
  status: not_supported
  rationale: Sama sbg strategic_resistance — tidak ada bukti tindakan
    pembelotan aktif oleh regent Priaman sendiri; pola yg ditemukan lebih
    konsisten dgn agregasi administratif ancaman eksternal.

local_contractual_breach:
  status: not_testable
  rationale: Traktat 1712 tidak mengutip klausul spesifik yg dilanggar
    (kalimat lengkap karakterisasi `trouwloosheyd` TIDAK TERSEDIA dari
    process-tracing sesi ini — lihat §5, §16) — tanpa teks klausul, tak
    bisa diuji apakah ada "breach" kontraktual spesifik.
```

---

## 12. Process Links

| Transisi | Nilai (dari process-tracing) |
|---|---|
| 1706 (teguran) → 1711 (Siry Amar/Tiku) | **`chronology_only`** + flag `actor_identity_conflict` |
| 1711 (Tiku) → 1712 (`trouwloosheyd`) | **`plausible_sequence_only`** |
| 1712 (`trouwloosheyd`) → 1713 (ekspedisi) | **`actor_identity_conflict`** |

**Tidak ada satu pun transisi yang mencapai `explicit_mechanism` atau
`strong_process_link`** — berbeda dari kasus Sillida/Salido (yg punya 1
transisi `explicit_mechanism`, lihat dossier Sillida) dan kasus Padang
1705 (yg punya 2 rule suksesi `primary_treaty_text_verified` langsung).
Ini KONSISTEN dgn `mechanism_status: interpretive_only` di §11.

---

## 13. Deduplication Risks

**Risiko utama teridentifikasi dan DITANGANI**: S6 (13 Jan 1713) dan S7
(20 Nov 1713) — **diperlakukan sbg SATU historical_event (HE-PRM-06), DUA
documentary_report (S6, S7)**, sesuai instruksi eksplisit ("kecuali bukti
menunjukkan dua kejadian berbeda"). Bukti pendukung penyatuan: S7 eksplisit
merujuk "jongste expeditie tot Priaman" (ekspedisi TERBARU/tunggal),
kompatibel dgn tanggal S6, tanpa indikasi tekstual adanya ekspedisi kedua.

**Risiko sekunder, TIDAK ditangani dlm dossier ini (di luar cakupan)**:
- **`[KOREKSI, RESOLVED]`** HE-PRM-04 (Manicabos Vorst/Maharadja Indra)
  berpotensi tumpang tindih dgn dossier Padang 1705
  (`PADANG_INSTITUTIONAL_SCHEMA_V1_DRAFT.md`) — **verifikasi identitas
  terdedikasi (turn terpisah) menyimpulkan `different_persons_supported`,
  confidence `high`**: Maharadja Indra diangkat panglima radja 1705 TAPI
  dibunuh di Batavia sebelum menjabat; Mara Laout (adiknya, per buku Ikbal
  footnote 142) adalah PENGGANTI yg benar-benar menjabat dan menandatangani
  CD4 DCXXXII (13 Agu 1705). **Dua actor_id dipertahankan terpisah,
  TIDAK di-merge.** Bukti kunci: GM 06/p0415.xml (30 Nov 1706) melaporkan
  jenazah Maharadja Indra tiba di Padang PADA WAKTU YANG SAMA "panglima
  van Padang" (Mara Laout) dilaporkan masih aktif — kontradiksi simultan
  yg menyingkirkan kemungkinan identitas sama.
- Kemungkinan identitas Soeroewassa 1680/1713 (A06) — dibahas §4/§9, TIDAK
  digabung jadi 1 aktor tunggal krn `cannot_determine`.

---

## 14. Evidence For and Against Each Hypothesis

| # | Hipotesis | Evidence for | Evidence against | Status |
|---|---|---|---|---|
| H1 | Akumulasi ketidakpatuhan Priaman → traktat 1712 | Teguran 1706 tematis serupa (dagang gelap Aceh) | Aktor konkret 1711 = Tiku bukan Priaman; tak ada rujukan traktat 1712 ke insiden spesifik | **Lemah** |
| H2 | Jaringan Tiku–Priaman disederhanakan VOC jadi persoalan Priaman | 1711 eksplisit Tiku=pelaku, Priaman=mitra; traktat 1712 Priaman-spesifik | — | **Cukup didukung** |
| H3 | Perubahan representasi menjelaskan traktat baru | — | Tak ada info pergantian kepemimpinan Priaman spesifik 1706-1712 | **Tak teruji** |
| H4 | Konflik regional lebih menentukan drpd tindakan regent Priaman | Manicabos Vorst (Padang) + Soeroewassa (kandidat berulang 1680→1713) menunjukkan tekanan eksternal konstan | Identitas Soeroewassa antar-periode belum pasti | **Cukup didukung** |
| H5 | Ekspedisi 1713 = respons pelanggaran pascatraktat | Kedekatan kronologis (traktat 1712 → ekspedisi 1713) | Tak ada bukti pelanggaran spesifik pascatraktat dlm kutipan yg terbaca | **Tidak teruji** |
| H6 | Ekspedisi 1713 tak berhubungan langsung dgn aktor yg dikarakterisasi 1712 | Kandidat identitas "de vijanden"=Soeroewassa (rival eksternal), bukan "sommiger regenten" (penandatangan traktat) | Identitas belum pasti | **Cukup didukung** |

---

## 15. Graph Extraction Readiness

```
graph_extraction_readiness: ready_for_researcher_review
```

Dossier ini SIAP DITINJAU peneliti sbg kandidat ekstraksi graph (struktur
9 aktor terpisah + 6 historical_event + parent-child sudah eksplisit), TAPI
**EKSTRAKSI GRAPHIFY TIDAK DIJALANKAN dalam turn ini** sesuai batas yg
diminta. Node/edge yg BELUM ADA di graph saat ini (verifikasi manual belum
dilakukan turn ini, hanya estimasi struktural dari isi dossier): entitas
Siry Amar, Manicabos Vorst, Radja Soeroewassa/Serwassa, Maharadja Indra,
Radja Gagaralam — kemungkinan besar TIDAK ADA representasi eksplisit di
`graphify-out/graph.json` saat ini krn seluruhnya baru muncul lewat
process-tracing sesi ini yg belum pernah diekstraksi.

---

## 16. Model-Mark Readiness

```
model_mark_readiness: not_ready
```

Alasan (sesuai `MECHANISM_CODED_EVENT_LAYER_DRAFT.md` §7 readiness
threshold): (a) TIDAK ADA mekanisme mencapai `supported` (tertinggi hanya
`partially_supported` untuk `political_reconfiguration`); (b) actor
continuity DOMINAN `collective_actor_ambiguous`/`actor_identity_conflict`
di 3 dari 4 titik utama; (c) provenance kuat (`primary_source_verified`)
TAPI identitas aktor lemah — readiness threshold eksplisit mensyaratkan
KEDUANYA; (d) hanya 1 lokasi (Priaman), belum lintas-lokasi independen.

---

## 17. Unresolved Questions

- [ ] Kalimat lengkap traktat 1712 yg memuat `trouwloosheyd en misleydinge
  sommiger regenten` — HANYA frasa ini yg tersedia dari process-tracing
  sesi ini; konteks kalimat penuh (apakah ada klausul spesifik yg dirujuk)
  **`NOT AVAILABLE`** tanpa membaca ulang CD4 idx399 secara utuh (di luar
  cakupan "jangan mencari sumber baru" turn ini — memerlukan izin turn
  terpisah).
- [x] **`[RESOLVED]`** Apakah Maharadja Indra (HE-PRM-04, Padang 1711) =
  Mara Laout (Padang 1705, CD4 DCXXXII)? **Tidak** — verifikasi identitas
  terdedikasi menyimpulkan `different_persons_supported`, confidence
  `high`. Maharadja Indra diangkat 1705 tapi dibunuh di Batavia sebelum
  menjabat; Mara Laout (adiknya) adalah pengganti yg benar-benar menjabat.
  Actor_id dipertahankan terpisah, tidak di-merge.
- [ ] Apakah "Kota Tengah" (S2, 1706) = "Koto Tangah" yg dibahas di dossier
  Padang lain sesi ini? **`cannot_determine`** — perbedaan ejaan belum
  diverifikasi sbg lokasi identik atau berbeda.
- [ ] Identitas pasti "sommiger regenten" (1712) dan "de vijanden" (1713) —
  **tetap tidak teridentifikasi** dari korpus yg tersedia sesi ini.
- [ ] Kontinuitas identitas Radja Soeroewassa (1713) dgn "Radja moderna di
  Serwassa" (1680) — memerlukan GM/arsip volume 1682-1710 yg belum
  diperiksa (di luar cakupan turn ini).
- [ ] Apakah pola "agregasi administratif" yg ditemukan di Priaman berlaku
  juga utk lokasi lain yg diaudit sesi ini (Barus, Indrapura) — belum
  diuji komparatif formal.

---

## 18. Status Akhir

```
process_trace_status: process_trace_partial
graph_extraction_readiness: ready_for_researcher_review
model_mark_readiness: not_ready
strategic_resistance: not_supported
defection: not_supported
```

---

## Appendix — Dossier Lama Diarsipkan (STALE, digantikan oleh dokumen di atas)

Isi PERSIS dari `PARIAMAN_EPISODE_DOSSIER_DRAFT.md` versi sebelumnya
(1671-1712, berbasis `linimasa_events.csv`) dipertahankan penuh di bawah
ini sbg bukti koreksi — **TIDAK dijadikan rujukan aktif untuk mekanisme
assessment §11 di atas**, krn memperlakukan "regenten Priaman" sbg satu
aktor kolektif berkelanjutan, asumsi yg dibongkar dossier baru ini.

### Episode Identity (lama)

| Field | Nilai |
|---|---|
| `episode_id` | EP-PARIAMAN-01 |
| `cluster` | Pariaman (Priaman) |
| `title` | Rangkaian aliansi-relaps-penundukan-ulang Priaman, 1671–1712 |
| `start_date` / `end_date` | 1671 / 1712 |
| `actor_ids` | landtheren/regenten Priaman (kolektif, komposisi berubah antar-baris) |

### Reconstructed Events (lama, tabel ringkas)

| CSV baris | Tahun | `event_type` | Aktor | `source_document` |
|---|---|---|---|---|
| [51] | 1671 | perjanjian | landtheren Priaman | CD2 |
| [55] | 1678 | perjanjian | regenten Priaman | CD3 |
| [66] | 1682 | perjanjian | regenten Priaman, Oulaccan, dll. | CD3 |
| [68] | 1684 | konflik | regenten Priaman | CD3 |
| [93] | 1712 | perjanjian | regenten Priaman, Oulaccan, Sonor, Bintoengantingi, Lima-cotta, Ticou | CD4 |

### Alternative Explanations (lama, enam hipotesis, tidak diberi keputusan final)

| Hipotesis | Status (lama) |
|---|---|
| `resistance_to_voc_constraint` | `possible` |
| `commercial_continuity` | `possible` — dukungan tekstual langsung terkuat |
| `alliance_maintenance` | `possible` |
| `market_constraint` | `insufficient_evidence` |
| `local_political_competition` | `possible` |
| `mixed_motive` | `possible` |

### Interpretive Status (lama, Dimensi B)

```
dimension_b_value: possible_resistance_candidate
confidence: Rendah-sedang
decision_status: draft
```

**Catatan koreksi (dossier baru vs lama)**: dossier lama TIDAK memisahkan
Tiku dari Priaman, TIDAK mengidentifikasi Siry Amar, TIDAK menemukan
"sommiger regenten"/"de vijanden" sbg frasa kolektif tak-bernama yg
terpisah, dan menggabungkan [66] 1682 (episode Radja Ebrahim — SEKARANG
diketahui berpotensi Baros, bukan Priaman, per process-tracing Sillida
sesi ini) ke rantai Priaman tunggal. Dossier baru §4 (Actor Ledger)
membongkar seluruh penggabungan ini.

---

Tidak ada graph, dataset, Model 3, dashboard, `linimasa_events.csv`, atau
sumber primer yang diubah dalam penyusunan dokumen ini. Tidak ada
Graphify, fitting, migrasi, deployment, atau operasi Git yang dijalankan.
