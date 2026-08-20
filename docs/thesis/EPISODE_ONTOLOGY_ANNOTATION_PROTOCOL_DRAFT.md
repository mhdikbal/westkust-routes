# Episode Ontology and Annotation Protocol

> **DRAFT FOR RESEARCHER REVIEW**
> **NOT IMPLEMENTED**
> **NOT A FINAL HISTORICAL INTERPRETATION**

**Status:** Rancangan metodologis, 2026-08-20. Tidak ada schema yang diimplementasikan, tidak ada migrasi database, tidak ada dataset yang diubah, tidak ada anotasi yang dibuat. Dokumen ini adalah *usulan* struktur kerja yang menunggu keputusan pemilik riset (§13).

**Dasar:** tiga audit read-only berturut-turut atas Model 3 (Proses Hawkes) dan `linimasa_events` (141 baris). Temuan yang menjadi pemicu rancangan ini:

1. Model 3 menguji *self-excitation pada gabungan seluruh tipe peristiwa politik*, bukan defeksi spesifik — istilah "kaskade defeksi" adalah label interpretif yang belum dioperasionalkan.
2. `linimasa_events` **tidak punya field relasional apa pun** yang menghubungkan satu event ke event lain — pasangan "janji → pelaksanaan" tidak dapat dibangun secara terprogram dari data yang ada.
3. Sumber primer justru **cukup kaya** untuk kerja hermeneutis: empat klaster pilot ditemukan punya rujukan tekstual eksplisit antar-traktat (`vernieuwinge`, `verbondbreking`, `vielfältigen Meineydes`), termasuk satu kasus di mana sumber menyatakan **VOC** yang gagal memenuhi kewajiban.

Kesenjangannya bukan kekurangan arsip, melainkan **kekurangan struktur untuk menampung hasil pembacaan arsip**. Dokumen ini merancang struktur itu.

---

## 1. Purpose and Epistemic Boundaries

### 1.1 Tujuan

Merancang unit analisis dan protokol anotasi yang memungkinkan rekonstruksi rantai:

```
klaim sumber → persetujuan → kewajiban → kondisi pelaksanaan
             → tindakan aktual → deviasi → respons → interpretasi
```

sedemikian rupa sehingga pertanyaan riset *"apakah kesenjangan antara persetujuan formal dan pelaksanaan aktual dapat ditafsirkan sebagai resistensi"* menjadi **pertanyaan yang bisa diperiksa**, bukan asumsi yang sudah tertanam di nama variabel.

### 1.2 Tujuh lapis yang wajib dipisahkan

Aturan tunggal yang mengatur seluruh rancangan ini: **fakta dan interpretasi tidak boleh berbagi field.** Tujuh lapis, tiap lapis punya unit datanya sendiri:

| # | Lapis | Unit | Pertanyaan yang dijawab | Siapa yang "berbicara" |
|---|---|---|---|---|
| 1 | Teks sumber | `SourceRecord` | Apa yang tertulis? | Dokumen |
| 2 | Klaim pembuat sumber | `DocumentaryClaim` | Apa yang *dinyatakan* penulis dokumen? | Penulis VOC/Vogel/dll. |
| 3 | Rekonstruksi peristiwa | `HistoricalEvent` | Apa yang kemungkinan besar terjadi? | Peneliti (sintesis) |
| 4 | Evaluasi komitmen–pelaksanaan | `Episode` + `ComplianceAssessment` | Apakah yang dijanjikan dilakukan? | Peneliti (evaluatif) |
| 5 | Interpretasi hermeneutis | `InterpretationRecord` | Apa makna tindakan itu? | Peneliti (interpretatif) |
| 6 | Hipotesis kausal | `CausalHypothesis` | Mekanisme apa yang diusulkan & bagaimana menolaknya? | Peneliti (teoretis) |
| 7 | Hasil statistik | Output Model 3 dkk. (**di luar schema ini**) | Pola apa yang muncul agregat? | Model |

Lapis 7 sengaja **tidak** dimasukkan ke dalam schema episode. Hasil model adalah turunan dari lapis 1–4, dan memasukkannya kembali sebagai field episode akan menciptakan jalur umpan-balik di mana output model menjadi input anotasi (lihat risiko sirkularitas, §8.2 dan §14.2).

### 1.3 Enam asumsi yang secara eksplisit ditolak

Rancangan ini dibangun agar keenam pernyataan berikut **harus dibuktikan per kasus**, tidak boleh diasumsikan:

| Asumsi ditolak | Konsekuensi desain |
|---|---|
| Perjanjian selalu persetujuan substantif | Field `commitment_under_duress`, `representational_scope`, `commitment_confidence` wajib diisi terpisah dari keberadaan traktat |
| Teks VOC deskripsi netral | Field `source_perspective` wajib; `DocumentaryClaim` dipisah dari `HistoricalEvent` |
| Ketidakpatuhan selalu defeksi | Dimensi A (bentuk hubungan) dipisah total dari Dimensi B (interpretasi resistensi) |
| Defeksi selalu resistensi | Dimensi B punya nilai `probable_constraint_or_incapacity` dan `contractual_dispute` yang setara statusnya |
| Resistensi selalu perlawanan | Dimensi B tidak punya nilai "perlawanan"; istilah itu di luar cakupan schema |
| Urutan temporal = sebab-akibat | `CausalHypothesis` unit terpisah dengan syarat falsifiabilitas eksplisit; `Episode` sendiri tidak menyimpan klaim kausal |

### 1.4 Yang BUKAN tujuan dokumen ini

- Bukan memberi label resistensi final kepada episode mana pun.
- Bukan mengganti atau memperbaiki Model 3.
- Bukan menambah tabel ke database produksi (keputusan itu ada di §13).
- Bukan menyatakan bahwa tesis *"Iyokan nan di urang, laluan nan di awak"* sudah atau akan terbukti.

---

## 2. Unit of Analysis

### 2.1 SourceRecord

**Batas definisi.** Satu dokumen, atau satu bagian dokumen yang dapat dirujuk secara mandiri (satu traktat dalam Corpus Diplomaticum, satu surat dalam Generale Missiven, satu entri Daghregister, satu bagian lampiran buku Vogel). Unit fisik/bibliografis, **bukan** unit peristiwa.

**Hubungan dengan unit lain.** Satu `SourceRecord` melahirkan 0..n `DocumentaryClaim`. Satu `HistoricalEvent` dapat bersandar pada 1..n `SourceRecord`.

**Field minimum:** `source_id`, `collection`, `volume_or_inventory`, `folio_or_page`, `document_genre`, `document_language`, `original_text_excerpt`, `transcription`, `transcription_status`.

**Field opsional:** `document_author`, `document_recipient`, `author_institutional_position`, `report_date`, `translation_literal`, `translation_status`, `scan_verified`, `source_uncertainty_notes`.

**Contoh dari pilot.** Corpus Diplomaticum jilid III, traktat pada `book_page` 228–230 (Barus 1681) adalah satu `SourceRecord`. Lampiran geografis-politik Vogel (*Ost-Indianische Reise-Beschreibung*, ~1690, `book_page` 674–675) adalah `SourceRecord` **tunggal** yang menjadi dasar untuk *empat* tahun peristiwa Koto Tangah sekaligus (1670/1678/1682/1686) — kasus penting yang harus terlihat jelas di struktur, karena empat "titik data" ternyata satu kalimat sumber.

**Risiko salah klasifikasi.** Menganggap kompilasi editorial (Corpus Diplomaticum diedit Heeres, abad ke-19) setara dengan dokumen periode VOC asli; menganggap catatan kaki editor sebagai kutipan traktat. Skema `linimasa_events` yang ada sudah menandai masalah ini secara naratif di kolom `notes` — di sini ia dinaikkan menjadi field terkendali (`document_genre` + `source_uncertainty_notes`).

### 2.2 DocumentaryClaim

**Batas definisi.** Satu pernyataan yang *dibuat oleh pembuat dokumen* tentang aktor, komitmen, tindakan, atau sebab. Kebenarannya **tidak diandaikan**. Ini adalah lapis di mana kalimat seperti *"karena perjurian mereka yang berulang-ulang"* hidup — sebagai klaim Vogel, bukan sebagai fakta sejarah.

**Hubungan.** `SourceRecord` 1—n `DocumentaryClaim`. `DocumentaryClaim` n—n `HistoricalEvent` (beberapa klaim bisa menopang satu rekonstruksi; satu klaim bisa menyentuh beberapa peristiwa).

**Field minimum:** `claim_id`, `source_id`, `claim_text_original`, `claim_type` (`factual_assertion` \| `attribution_of_motive` \| `evaluative_judgment` \| `causal_assertion` \| `normative_characterization`), `claimed_actor`, `claim_about`.

**Field opsional:** `claim_translation`, `claimant_stake` (kepentingan penulis dalam klaim ini), `corroborating_claim_ids`, `contradicting_claim_ids`.

**Contoh dari pilot.**

- Vogel: *"wegen ihres vielfältigen Meineydes"* → `claim_type: normative_characterization` (bukan `factual_assertion`). "Perjurian" adalah karakterisasi moral pihak yang merasa dikhianati, bukan deskripsi tindakan.
- Buku Padang 1718 tentang Koto Tangah 1670: *"sifat tidak setia orang Sumatra"* → `claim_type: normative_characterization`, dengan `claimant_stake` tinggi (sumber mengutip Valentijn, historiografi kolonial).
- Vogel tentang Inderapura 1686: *"weiln er hülffloß gelassen … keine assistenz erlangen können"* → `claim_type: causal_assertion`, dan **klaim ini memberatkan VOC**, bukan aktor lokal.

**Risiko salah klasifikasi.** Menyimpan karakterisasi normatif (`Meineyd`, "tidak setia") sebagai `factual_assertion`. Inilah titik di mana bias sumber paling mudah menyusup tanpa terdeteksi, karena kata-kata itu terasa deskriptif dalam terjemahan.

### 2.3 HistoricalEvent

**Batas definisi.** Rekonstruksi peneliti tentang apa yang kemungkinan besar terjadi, disintesis dari satu atau lebih `DocumentaryClaim`. Berbeda dari baris `linimasa_events` yang ada: baris itu saat ini mencampur transkripsi (`text_asli`), rekonstruksi (`title`), dan komentar peneliti (`notes`) dalam satu record.

**Hubungan.** Menopang `Episode` melalui tiga peran berbeda: `commitment_event`, `implementation_event`, `response_event`.

**Field minimum:** `event_id`, `event_date`, `event_date_precision` (`day` \| `month` \| `year` \| `range` \| `inferred`), `event_summary`, `supporting_claim_ids`, `actor_ids`, `location_ids`, `reconstruction_confidence`.

**Field opsional:** `report_date`, `report_delay_days`, `conflicting_reconstructions`, `event_role_hint`.

**Contoh dari pilot.** Baris [45] (Barus 1668) menjadi satu `HistoricalEvent` dengan `event_date_precision: day`; baris [115]/[116] (Koto Tangah 1678/1686) menjadi dua `HistoricalEvent` dengan `event_date_precision: year` dan **`supporting_claim_ids` yang menunjuk ke klaim Vogel yang sama** — sehingga ketergantungan sumber-tunggal terlihat langsung dari struktur, tidak perlu diingat manual.

**Risiko salah klasifikasi.** Memperlakukan satu kalimat sumber yang menyebut empat tahun sebagai empat peristiwa independen dengan bobot bukti setara. Ini persis yang terjadi sekarang di `linimasa_events` (dua baris, kutipan `text_asli` identik) dan yang mengalir masuk ke Model 3 sebagai dua titik waktu terpisah.

### 2.4 Obligation

**Batas definisi.** Satu kewajiban spesifik yang dibentuk oleh sebuah komitmen: tindakan yang harus dilakukan, larangan, pembayaran, penyerahan, atau pembatasan hubungan diplomatik. **Satu traktat lazimnya membentuk banyak `Obligation`** — dan sebagian besar di antaranya melekat pada VOC, bukan pihak lokal.

**Hubungan.** `Episode` 1—n `Obligation`. Tiap `Obligation` dapat dipasangkan dengan 0..n `implementation_event`.

**Field minimum:** `obligation_id`, `episode_id`, `obligated_actor`, `beneficiary_actor`, `obligation_modality` (`required_action` \| `prohibited_action` \| `payment` \| `surrender` \| `diplomatic_restriction` \| `other`), `obligation_text_source`.

**Field opsional:** `expected_deadline`, `deadline_precision`, `condition_precedent`, `reciprocal_obligation_id`, `reciprocal_actor`, `obligation_specificity` (`explicit` \| `general` \| `implied`).

**Contoh dari pilot.**

| Sumber | `obligated_actor` | `obligation_modality` | Isi |
|---|---|---|---|
| Pariaman 1682 [66] | regenten Priaman | `prohibited_action` | tidak boleh melepas kapal berlayar ke Aceh |
| Pariaman 1684 [68] | Priaman & wilayah bawahannya | `prohibited_action` | tidak boleh berkorespondensi/berdagang dengan Aceh |
| Barus 1681 [61] | radja d'Ileer | `surrender` | menyerahkan senjata & amunisi "mahkota Aceh" |
| Barus 1694 [86] | Batak Dairi | `required_action` | menjual kemenyan/kapur barus eksklusif ke Baros |
| Inderapura (implisit) | **VOC** | `required_action` | memberi `assistenz`/perlindungan — **`obligation_specificity: implied`**, NOT AVAILABLE sebagai teks traktat eksplisit di data saat ini |

**Risiko salah klasifikasi.** Mencatat hanya kewajiban pihak lokal dan mengabaikan kewajiban VOC. Karena arsipnya arsip VOC, kewajiban VOC sering tersirat sementara kewajiban lokal dieja rinci. Field `reciprocal_obligation_id` ada justru untuk memaksa pertanyaan itu diajukan tiap kali.

### 2.5 Commitment-Implementation Episode

**Batas definisi.** Unit relasional inti — inilah yang **sama sekali tidak ada** di struktur data saat ini. Satu episode mengikat: komitmen → kewajiban → tindakan aktual → evaluasi kesesuaian → respons → konteks.

**Batas temporal.** Episode dimulai pada tanggal komitmen dan berakhir pada respons terakhir yang dapat ditelusuri ke komitmen itu, **atau** pada titik di mana rantai bukti putus (`end_date_status: evidence_exhausted`). Episode **tidak** ditutup hanya karena periode waktu tertentu berlalu.

**Aturan pembentukan.** Sebuah episode hanya dibentuk jika ada dasar yang dapat ditunjukkan (rujukan tekstual eksplisit, aktor sama, kewajiban sama, rujukan ke perjanjian terdahulu). **Kedekatan waktu saja tidak pernah cukup** — aturan ini diwarisi langsung dari audit sebelumnya dan wajib dipertahankan.

**Field minimum:** lihat §4.

**Contoh dari pilot.** Barus [57] 1679 → [61] 1681: dasar pemasangan adalah kalimat dalam [61] sendiri, *"sodanige verbondbreking noyt meer te sullen beginnen"* — dokumen mengakui adanya pelanggaran perjanjian sebelumnya. `pairing_strength: explicit`.

**Risiko salah klasifikasi.** Membentuk episode dari dua peristiwa yang berdekatan tahun tapi berbeda isu (contoh nyata: Koto Tangah [58] 1680 dan [90] 1705 — yang kedua soal otoritas tambatan kapal, bukan soal kesetiaan-Aceh; memasangkannya akan menyeret sengketa administratif ke dalam narasi defeksi).

### 2.6 InterpretationRecord

**Batas definisi.** Penilaian hermeneutis peneliti, **selalu tersimpan terpisah** dari episode yang ditafsirkannya. Satu episode dapat punya beberapa `InterpretationRecord` yang bersaing — termasuk dari anotator berbeda atau dari kerangka teoretis berbeda.

**Hubungan.** `Episode` 1—n `InterpretationRecord`. Tidak pernah sebaliknya: interpretasi tidak boleh mengubah field faktual episode.

**Field minimum:** `interpretation_id`, `episode_id`, `dimension_a_value`, `dimension_b_value`, `evidence_for`, `evidence_against`, `alternative_explanations`, `confidence`, `interpretation_source`, `annotator_id`, `researcher_review_required` (selalu `true`), `decision_status`.

**Field kritis — `interpretation_source`.** Nilai: `source_derived` (dari bacaan arsip), `researcher_theoretical` (dari kerangka teoretis peneliti), `model_derived` (dari output model kuantitatif). **Aturan keras: `InterpretationRecord` ber-`interpretation_source: model_derived` tidak boleh dikutip di `evidence_for` interpretasi lain.** Field ini adalah pengaman anti-sirkularitas utama (§8.2).

**Risiko salah klasifikasi.** Menyimpan interpretasi ke dalam `event_summary` atau `episode_title` sehingga ia tampak sebagai fakta pada pembacaan berikutnya. Contoh nyata di data sekarang: judul baris [115] berbunyi *"Koto Tangah dihancurkan VOC krn ingkar traktat berulang"* — klausa "krn ingkar traktat berulang" adalah klaim Vogel yang sudah menyatu ke dalam ringkasan peristiwa.

### 2.7 CausalHypothesis

**Batas definisi.** Hipotesis mekanisme yang dinyatakan sedemikian rupa sehingga **dapat ditolak**. Hipotesis tanpa kondisi pemalsuan tidak boleh masuk.

**Field minimum:** `hypothesis_id`, `proposed_mechanism`, `cause_definition`, `outcome_definition`, `scope_conditions`, `falsification_conditions`, `evidence_required`, `evidence_currently_available`, `status` (`proposed` \| `testable` \| `not_yet_testable` \| `refuted` \| `suspended`).

**Contoh dari pilot (semua berstatus `proposed`, belum `testable`).**

- H-A: *"Pembaruan traktat yang memuat larangan spesifik-berulang menandakan larangan sebelumnya tidak efektif."* Kondisi pemalsuan: ditemukan traktat dengan larangan berulang di lokasi yang justru tidak punya bukti pelanggaran apa pun.
- H-B: *"Peralihan aliansi aktor lokal didahului oleh kegagalan pelindung sebelumnya memberi bantuan yang diminta."* Kondisi pemalsuan: ditemukan kasus peralihan yang didahului bantuan yang benar-benar diberikan.
- H-C (**kandidat confound, bukan hipotesis substantif**): *"Kepadatan peristiwa tercatat mencerminkan intensitas pelaporan administratif, bukan intensitas peristiwa."* Kondisi pemalsuan: volume dokumen per tahun tidak berkorelasi dengan jumlah event per tahun.

**Risiko salah klasifikasi.** Menyatakan hipotesis dalam bentuk yang tidak dapat ditolak ("VOC dan aktor lokal saling memengaruhi").

---

## 3. Conceptual Data Model

```
SourceRecord ──1:n──> DocumentaryClaim
                            │
                            └──n:n──> HistoricalEvent
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │ (commitment_event)  │ (implementation_    │ (response_event)
                    │                     │   event)            │
                    v                     v                     v
                 ┌──────────────────────────────────────────────────┐
                 │   Commitment-Implementation Episode              │
                 │   ├─ 1:n Obligation                              │
                 │   ├─ 1:n ComplianceAssessment (per Obligation)   │
                 │   └─ 1:n ResponseRecord                          │
                 └──────────────────────────────────────────────────┘
                            │
                            ├──1:n──> InterpretationRecord   (Dimensi A + B)
                            │             │
                            │             └── interpretation_source:
                            │                   source_derived | researcher_theoretical | model_derived
                            │
                            └──n:n──> CausalHypothesis

        [ Output Model 3 / statistik ] — DI LUAR schema; tidak pernah menjadi field episode
```

**Tiga aturan integritas lintas-unit:**

1. **Aturan pemisahan.** Field `transcription`, `translation_literal`, `event_summary`, dan `evidence_for` tidak boleh berisi konten dari lapis lain. Transkripsi tidak boleh diperbaiki agar "masuk akal"; terjemahan literal tidak boleh dihaluskan menjadi parafrase.
2. **Aturan atribusi.** Setiap karakterisasi normatif (`Meineyd`, "tidak setia", "memberontak") wajib berada di `DocumentaryClaim` dengan `claim_type: normative_characterization`, tidak pernah di `event_summary`.
3. **Aturan anti-sirkularitas.** `InterpretationRecord` ber-`interpretation_source: model_derived` tidak boleh menjadi `evidence_for` bagi `InterpretationRecord` lain, dan tidak boleh memengaruhi field mana pun di `Episode`, `Obligation`, atau `ComplianceAssessment`.

---

## 4. Episode Schema

Rancangan konseptual. **Tidak diimplementasikan.** Tipe data disebut untuk kejelasan saja, bukan sebagai DDL.

### 4.1 Identitas

| Field | Catatan |
|---|---|
| `episode_id` | Identitas stabil |
| `title` | Deskriptif-netral. **Dilarang** memuat karakterisasi normatif |
| `start_date`, `end_date` | Batas episode |
| `date_precision` | `day` \| `month` \| `year` \| `range` \| `inferred` |
| `end_date_status` | `resolved` \| `evidence_exhausted` \| `ongoing_at_source_end` |
| `location_ids` | Rujukan ke `forts` bila ada; teks bebas bila di luar roster |
| `actor_ids` | Pihak pemberi komitmen |
| `counterparty_ids` | Pihak penerima komitmen |

### 4.2 Komitmen

| Field | Nilai / catatan |
|---|---|
| `commitment_event_ids` | 1..n `HistoricalEvent` |
| `commitment_type` | `treaty` \| `oath` \| `renewal` \| `submission_after_force` \| `succession_affirmation` \| `trade_undertaking` \| `other` |
| `commitment_form` | `written_bilateral` \| `written_unilateral` \| `oath_ceremonial` \| `reported_verbal` \| `inferred_from_narrative` |
| `commitment_text` | Kutipan verbatim dari `SourceRecord` |
| `commitment_language` | Belanda-VOC \| Jerman \| Melayu \| Inggris \| lainnya |
| `commitment_conditions` | Syarat yang menyertai |
| `commitment_under_duress` | `none_documented` \| `military_action_preceding` \| `military_presence` \| `economic_coercion` \| `contested` \| `cannot_determine` |
| `representational_scope` | Siapa yang diklaim diwakili penanda tangan; `scope_contested` bila diperdebatkan |
| `commitment_confidence` | Keyakinan bahwa ini komitmen substantif, bukan formalitas administratif |

`commitment_under_duress` bukan field kosmetik. Untuk pilot Koto Tangah [58] 1680, teks sendiri menyebut ekspedisi militer Laurens Pit mendahului penundukan — nilainya `military_action_preceding`, dan itu mengubah bagaimana "persetujuan" di situ boleh dibaca.

### 4.3 Kewajiban

Per `Obligation` (lihat §2.4): `obligation_id`, `obligated_actor`, `beneficiary_actor`, `required_action`, `prohibited_action`, `expected_deadline`, `deadline_precision`, `condition_precedent`, `reciprocal_obligation_id`, `reciprocal_actor`, `obligation_specificity`.

**Aturan pengisian wajib:** bila `reciprocal_obligation_id` dibiarkan kosong, anotator wajib mengisi `reciprocity_check_note` dengan salah satu dari: "tidak ada kewajiban timbal-balik dalam teks", "kewajiban timbal-balik disebut tapi tidak spesifik", atau "NOT AVAILABLE — teks tidak lengkap". Kekosongan diam tidak diterima.

### 4.4 Pelaksanaan

| Field | Catatan |
|---|---|
| `implementation_event_ids` | 0..n |
| `observed_action` | Tindakan yang dilaporkan terjadi |
| `action_date`, `action_date_precision` | — |
| `implementation_evidence` | Rujukan `DocumentaryClaim` |
| `implementation_degree` | `full` \| `partial` \| `none_observed` \| `not_observable` |
| `evidence_of_absence_vs_absence_of_evidence` | `documented_nonaction` \| `silence_only` — **wajib**; membedakan "sumber menyatakan tidak dilakukan" dari "sumber tidak menyebut apa-apa" |

Field terakhir adalah pengaman terhadap kesalahan paling umum dalam riset arsip kolonial: memperlakukan diamnya arsip sebagai bukti tidak-terjadi.

### 4.5 Evaluasi kesesuaian (`ComplianceAssessment`, satu per `Obligation`)

Nilai awal yang diusulkan:

`fulfilled` · `substantially_fulfilled` · `partially_fulfilled` · `delayed` · `suspended` · `evaded` · `openly_refused` · `contradicted` · `reciprocal_breach` · `contested` · `cannot_determine`

**Catatan desain.** `evaded` memuat unsur niat (menghindar ≠ gagal). Untuk menjaga pemisahan fakta/interpretasi, `evaded` hanya boleh dipilih bila ada `DocumentaryClaim` yang menyatakan penghindaran aktif, **bukan** disimpulkan dari pola non-pelaksanaan berulang. Bila hanya ada pola, gunakan `partially_fulfilled` atau `cannot_determine`, dan letakkan pembacaan "menghindar" di `InterpretationRecord`. Ini perlu keputusan peneliti (§13, D-4).

### 4.6 Pihak yang diduga melanggar

`breach_attributed_to`: `local_actor` · `voc` · `both` · `contested` · `undetermined`

Wajib disertai `breach_attribution_basis`: `source_states` \| `researcher_inference` \| `disputed_between_sources`.

Nilai `voc` bukan kelengkapan formal — ia diperlukan oleh pilot Inderapura (§8.1).

### 4.7 Respons

`response_event_ids`, `responding_actor`, `response_type` (`military_action` \| `destruction` \| `expulsion` \| `sanction` \| `renegotiation` \| `renewal_of_treaty` \| `incentive_or_gift` \| `withdrawal` \| `no_response_documented`), `response_date`, `sanction_or_incentive`, `renegotiation`, `escalation`, `de_escalation`.

**Catatan:** `no_response_documented` berbeda dari tidak diisi. Ketiadaan respons yang tercatat adalah data.

### 4.8 Interpretasi

Disimpan di `InterpretationRecord` terpisah (§2.6), bukan sebagai kolom episode: `interpretive_status` (Dimensi A + B), `evidence_for`, `evidence_against`, `alternative_explanations`, `confidence`, `interpretation_source`, `researcher_notes`, `reviewer_notes`, `decision_status` (`draft` \| `under_review` \| `researcher_approved` \| `rejected` \| `deferred`).

### 4.9 Provenance

`source_document`, `source_collection`, `inventory_number`, `folio_or_page`, `original_text`, `transcription`, `translation`, `document_author`, `document_recipient`, `document_genre`, `event_date`, `report_date`, `source_perspective`, `source_uncertainty`.

**Dua field yang saat ini tidak ada padanannya sama sekali di `linimasa_events` dan wajib ditambahkan:**

- `report_date` — dipisahkan dari `event_date`. Audit sebelumnya mengonfirmasi skema sekarang tidak membedakan keduanya untuk seluruh 141 baris. Tanpa ini, "keterlambatan administratif" tidak dapat dikesampingkan sebagai penjelasan alternatif, dan analisis temporal apa pun berdiri di atas tanggal yang statusnya tidak jelas.
- `source_perspective` — sudut pandang institusional pembuat dokumen. Seluruh korpus utama (CD, Daghregister, Generale Missiven) ditulis dari posisi VOC; ini harus menjadi field, bukan pengetahuan tacit.

---

## 5. Hermeneutic Annotation Questions

Delapan belas pertanyaan wajib per episode. Jawaban `NOT AVAILABLE` adalah jawaban yang sah dan **harus dicatat**, bukan dilewati.

**Tentang dokumen (1–4)**
1. Siapa pembuat dokumen?
2. Dalam kapasitas apa dokumen dibuat (jabatan, mandat, untuk siapa ia menulis)?
3. Siapa penerima dokumen?
4. Apa genre dokumennya (traktat, laporan, jurnal harian, kompilasi editorial, catatan perjalanan)?

**Tentang persetujuan (5–8)**
5. Apakah kata persetujuan berasal dari aktor lokal atau dari narasi VOC yang melaporkan persetujuan itu?
6. Siapa yang dianggap diwakili oleh pemberi persetujuan?
7. Apakah aktor memiliki kewenangan untuk mengikat pihak lain (nagari lain, penerus, pedalaman)?
8. Apakah terdapat tekanan atau ketimpangan kekuasaan pada saat komitmen dibuat?

**Tentang kewajiban (9–12)**
9. Apa kewajiban yang sebenarnya dibentuk (bukan tema umum traktat, melainkan tindakan spesifik)?
10. Apakah kewajiban bersifat unilateral atau resiprokal?
11. Apa kewajiban VOC dalam komitmen ini?
12. Apakah terdapat syarat pendahuluan yang harus dipenuhi lebih dulu, dan oleh siapa?

**Tentang tindakan (13–16)**
13. Apa tindakan aktual yang diamati?
14. Siapa yang melaporkan tindakan tersebut?
15. Apakah tindakan aktual dibuktikan oleh sumber lain yang independen?
16. Apakah keterlambatan administrasi (jeda pelaporan, waktu tempuh kapal) memengaruhi kronologi yang tampak?

**Tentang penafsiran (17–18)**
17. Pembacaan alternatif apa yang tersedia?
18. **Bukti apa yang dapat membantah interpretasi resistensi?**

Pertanyaan 18 bersifat wajib-jawab. Sebuah `InterpretationRecord` dengan `evidence_against` kosong dan tanpa keterangan `NOT AVAILABLE` yang beralasan tidak boleh naik ke `decision_status: researcher_approved`.

---

## 6. Resistance Interpretation Framework

### 6.1 Dua dimensi terpisah

**Dimensi A — Bentuk hubungan komitmen dan tindakan** (lebih dekat ke deskriptif):

`compliance` · `partial_compliance` · `delay` · `avoidance` · `noncompliance` · `repudiation` · `reciprocal_breach` · `renegotiation` · `indeterminate`

**Dimensi B — Kemungkinan interpretasi resistensi** (interpretatif):

`explicit_resistance_candidate` · `probable_resistance_candidate` · `possible_resistance_candidate` · `ambiguous_noncompliance` · `probable_constraint_or_incapacity` · `contractual_dispute` · `insufficient_evidence`

Kedua dimensi diisi **independen**. Nilai Dimensi A tidak menentukan nilai Dimensi B. Contoh yang menunjukkan mengapa: sebuah episode bisa `noncompliance` (Dimensi A) sekaligus `probable_constraint_or_incapacity` (Dimensi B) — tidak melaksanakan karena tidak mampu, bukan karena menolak.

**Tidak ada klasifikasi biner resistance/non-resistance**, dan tidak ada nilai "perlawanan" di dimensi mana pun.

### 6.2 Kelengkapan wajib untuk setiap nilai Dimensi B

Setiap `InterpretationRecord` wajib memuat, tanpa kecuali:

- `evidence_for` — bukti tekstual spesifik, dengan rujukan `claim_id`
- `evidence_against` — bukti yang melemahkan
- `alternative_explanations` — minimal dipertimbangkan dari daftar §6.3
- `confidence` — dan dasar keyakinannya
- `researcher_review_required = true` — **selalu**, tanpa pengecualian, untuk semua nilai

### 6.3 Daftar penjelasan alternatif yang wajib dipertimbangkan

Sebelas kemungkinan yang harus ditinjau sebelum nilai Dimensi B mana pun ditetapkan:

ketidakmampuan · konflik internal · perubahan kepemimpinan · salah komunikasi · keterlambatan administratif · gangguan transportasi · persoalan ekonomi · perang · kehilangan arsip · bias pelaporan VOC · **kegagalan pihak lawan memenuhi kewajiban timbal-balik**

Item terakhir ditambahkan sebagai hasil langsung temuan pilot Inderapura, di mana sumber primer sendiri menempatkan kegagalan pada VOC.

### 6.4 Kosakata sumber sebagai titik masuk (bukan sebagai label)

Repository memuat `docs/thesis/cd_resistance_signal_candidates.csv` (13 baris, **untracked di git**) — upaya terdahulu menyisir Corpus Diplomaticum dengan lima kata kunci Belanda: `afvallig`, `ontrouw`, `oproer`, `geschonden`, `overtreding`.

**Nilai bagi protokol ini:** kosakata itu sendiri berguna sebagai titik masuk pencarian, karena berasal dari bahasa sumber, bukan dari kategori analitis modern.

**Peringatan yang harus dibawa serta:** hasil klasifikasi LLM pada file tersebut tidak memenuhi ambang kualitas — hanya 4 dari 13 baris ber-`auto_accept=true`, 6 dari 13 tidak disepakati dua model, dan 3 baris berstatus `PARSE_ERROR`. Ini adalah bukti empiris di dalam repository sendiri bahwa **klasifikasi otomatis atas kategori interpretif ini belum dapat diandalkan**, dan mendukung keputusan menempuh anotasi manual lebih dulu. Kelima kata kunci itu juga adalah karakterisasi *pihak VOC* (`ontrouw` = tidak setia, `afvallig` = murtad/membelot) — mencarinya berarti mencari peristiwa yang **VOC anggap** pelanggaran, yang merupakan bias seleksi yang harus dicatat eksplisit, bukan dikoreksi diam-diam.

---

## 7. Causal Readiness Framework

Sebelas kriteria per episode. **Tidak satu pun kombinasi nilai boleh dibaca sebagai pernyataan adanya hubungan kausal.**

| Kriteria | Isi |
|---|---|
| `cause_defined` | Sebab dinyatakan spesifik & dapat diamati |
| `outcome_defined` | Akibat dinyatakan spesifik & dapat diamati |
| `temporal_order_reliable` | Urutan waktu dapat dipercaya **setelah** memperhitungkan `report_date` |
| `mechanism_evidence` | Ada bukti tentang jalur penghubung, bukan hanya urutan |
| `alternative_explanations_recorded` | Sebelas alternatif §6.3 sudah ditinjau |
| `comparison_case_available` | Ada kasus pembanding (termasuk kasus negatif) |
| `actor_identity_stable` | Aktor sama sepanjang episode, bukan sekadar nama tempat sama |
| `location_identity_stable` | Lokasi konsisten & teridentifikasi |
| `report_delay_known` | Jeda pelaporan diketahui atau dapat diperkirakan |
| `archival_density_known` | Kepadatan dokumen periode itu diketahui |
| `ready_for_process_tracing` | Ringkasan: `ready` \| `partially_ready` \| `descriptive_only` \| `not_testable` |

**Aturan pembatas.** `ready_for_process_tracing: ready` tidak boleh diberikan selama `archival_density_known` masih `false` untuk seluruh korpus. Per audit sebelumnya, ukuran kepadatan arsip **belum ada** — sehingga saat ini **tidak ada episode yang dapat mencapai status `ready`**, terlepas dari sekuat apa pun bukti internalnya.

---

## 8. Four-Cluster Pilot Application

Pemetaan berikut memakai **hanya** informasi yang sudah ada di repository. `NOT AVAILABLE` berarti benar-benar tidak ditemukan, bukan belum dicari.

### 8.0 Ringkasan kesiapan field lintas-klaster

| Kelompok field | Koto Tangah | Barus | Pariaman | Inderapura |
|---|---|---|---|---|
| Identitas & tanggal | Terisi (presisi tahun untuk 2 titik Vogel) | Terisi | Terisi | Terisi |
| Komitmen (teks verbatim) | Terisi | Terisi | Terisi | Terisi |
| `commitment_under_duress` | Dapat diisi (`military_action_preceding`) | Sebagian | Dapat diisi | NOT AVAILABLE |
| Kewajiban spesifik | Sebagian — traktat tidak dikutip rinci | Terisi | **Terisi, paling spesifik** | Sebagian |
| Kewajiban VOC (resiprokal) | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE | **Tersirat di sumber, spesifik** |
| Tindakan aktual | Sebagian | Tersirat | Tersirat dari larangan berulang | Terisi |
| `report_date` | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE |
| Respons | Terisi (penghancuran) | Terisi (renegosiasi) | Terisi (militer + larangan) | Terisi (pemulihan 1716) |
| Sumber pembanding | **NOT AVAILABLE** | Sebagian | Sebagian | Sebagian |
| Terjemahan literal | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE |

### 8.1 Inderapura — uji apakah schema dapat merepresentasikan kegagalan VOC

**Uji ini adalah alasan utama rancangan memakai `breach_attributed_to` alih-alih field bernama "pelanggar lokal".**

Peristiwa: [41] 1665 (aliansi, Sultan Mametcha, Padang/Inderapura) → [71] 1686 (beralih ke Inggris) → [96] 1716 (kembali, kontrak 1663 diperbarui dengan sumpah di atas Alquran).

Kutipan kunci, Vogel ~1690 (`buku-vogel-1690`, `book_page` 682–683):

> *"weiln er hülffloß gelassen und ungeacht vieles implorirens beym Commendeur … keine assistenz erlangen können"*

Pemetaan yang dihasilkan schema:

| Field | Nilai |
|---|---|
| `Obligation` (VOC) | `obligated_actor: VOC`; `obligation_modality: required_action`; isi: memberi bantuan/perlindungan; `obligation_specificity: implied` |
| `condition_precedent` | Bantuan VOC sebagai syarat berkelanjutan — **berbasis klaim Vogel, bukan teks traktat**; teks traktat asli NOT AVAILABLE di data |
| `ComplianceAssessment` (kewajiban VOC) | `reciprocal_breach` — dengan `breach_attribution_basis: source_states` |
| `breach_attributed_to` | `both` atau `contested` — **bukan `local_actor`** |
| Dimensi A | `reciprocal_breach` |
| Dimensi B | `probable_constraint_or_incapacity` **atau** `contractual_dispute` — **bukan** kandidat resistensi |
| `evidence_for` (constraint) | Kutipan Vogel di atas: permohonan berulang (`vieles implorirens`) yang tidak dipenuhi |
| `evidence_against` | Vogel menulis retrospektif; `document_genre: travel_account_compilation`; motif Sultan tidak diketahui dari sumbernya sendiri |
| `alternative_explanations` | Perhitungan ekonomi (EIC menguasai perdagangan lada di distrik itu — disebut di kalimat yang sama); persaingan Inggris-Belanda pasca-1684; bias pelaporan |

**Verdict uji:** schema **mampu** merepresentasikan kasus ini tanpa memaksa aktor lokal menjadi pihak yang melanggar. Kemampuan itu bergantung pada tiga field yang harus dipertahankan: `reciprocal_obligation_id`, `breach_attributed_to` dengan nilai `voc`, dan nilai Dimensi A `reciprocal_breach`.

**Catatan ketidaksesuaian yang harus diselesaikan peneliti:** [96] 1716 merujuk balik ke kontrak **1663**, sementara komitmen terdekat yang ada sebagai baris data adalah [41] 1665. Traktat 1663 untuk Inderapura tidak punya baris tersendiri. Rantai rujukan tekstual dan rantai data tidak sepenuhnya berimpit — `NOT AVAILABLE` untuk `commitment_event_id` yang sebenarnya dirujuk.

### 8.2 Barus — uji sirkularitas

**Larangan operasional: payoff Model 6 tidak boleh dipakai sebagai bukti dalam anotasi Barus.**

Rantai peristiwa: [45] 1668 (sumpah lepas-Aceh) → [57] 1679 (*"Vernieuwinge soo van 't eerste, twede, als derde vredeverbond"*) → [60]/[61] 1681 (*"verbondbreking noyt meer te sullen beginnen"*, serah senjata) → [74] 1690 (sumpah suksesi) → … → [114] 1775 (VOC menarik diri).

Kualitas pemasangan: **explicit** untuk [45]→[57] dan [57]→[61], karena dokumen menyebut sendiri urutan traktat dan mengakui pelanggaran sebelumnya. Ini pasangan dengan dasar tekstual terkuat di seluruh pilot.

**Mekanisme sirkularitas yang harus dicegah:**

```
Konsep "merunduk bukan tunduk" (CLD, interpretasi peneliti)
        │
        ├─► dikodekan jadi bobot payoff Model 6 (Elite lokal +0.4 di voc_alliance)
        │
        ├─► Model 6 menghasilkan angka
        │
        └─► angka dipakai untuk melabeli episode Barus sebagai "otonomi ternegosiasi"
                    │
                    └─► episode Barus dikutip sebagai bukti konsep "merunduk bukan tunduk"
                                    │
                                    └──────► KEMBALI KE ATAS — lingkaran tertutup
```

**Pengaman dalam schema:**

1. Bobot payoff Model 6 dicatat sebagai `InterpretationRecord` dengan `interpretation_source: model_derived` dan `decision_status: draft`, terikat pada episode — **bukan** sebagai field episode.
2. Aturan integritas §3.3 melarang record `model_derived` muncul di `evidence_for` record lain.
3. Anotator Barus bekerja tanpa akses ke output Model 6 selama pengisian `evidence_for`/`evidence_against` (prosedur, bukan teknis — §9.4).

**Konsekuensi yang harus diterima:** bila pengaman ini dipatuhi, klaim "Barus mendukung tesis merunduk-bukan-tunduk" **tidak dapat** didukung oleh Model 6, dan harus berdiri atau jatuh pada bukti tekstual Barus sendiri. Itulah hasil yang diinginkan dari pengaman ini.

**Ambiguitas yang tersisa:** traktat "kedua" dan "ketiga" yang dirujuk [57] (~1670, ~1673) tidak punya baris data tersendiri — rantai `commitment_event_ids` berlubang. `NOT AVAILABLE`.

### 8.3 Koto Tangah — ketergantungan sumber sekunder retrospektif

**Batas keras: `ready_for_process_tracing` tidak boleh melebihi `descriptive_only` tanpa sumber pembanding.**

Struktur bukti:

| Tahun | Sumber | Jenis |
|---|---|---|
| 1670 | `buku-padang-1718` p238 (mengutip Valentijn) | Sekunder, mengutip sekunder |
| 1676 | `gm-vol04-05` p101 (Generale Missiven) | **Primer periode** |
| 1678 | `buku-vogel-1690` p674–675 | Sekunder retrospektif |
| **1682** | **NOT AVAILABLE — tidak ada baris data** | — |
| 1686 | `buku-vogel-1690` p674–675 — **kutipan identik dengan 1678** | Sekunder retrospektif |
| 1680, 1705 | CD3 p219–220; `buku-padang-1718` p238 | Primer / sekunder |

Kutipan Vogel (satu kalimat, menopang empat tahun sekaligus):

> *"dieses Refort Cotatenga ift A. 1670. 1678. 1682. und 1686. wegen ihres vielfältigen Meineydes … gäntzlich ruinirt, nachmahls aber wieder zu Bundes-Genossen auf und angenommen worden."*

**Pemetaan wajib dalam schema:**

- `HistoricalEvent` 1678 dan 1686 **berbagi `supporting_claim_ids` yang sama** — ketergantungan sumber-tunggal menjadi terlihat secara struktural.
- `claim_type: normative_characterization` untuk `Meineyd`; frasa itu **tidak boleh** muncul di `event_summary`.
- `event_date_precision: year`; `report_date` NOT AVAILABLE, dan jeda pelaporan besar (Vogel menulis ~1690 tentang peristiwa 1670).
- `comparison_case_available: false`; `source_perspective: VOC-adjacent European traveler account`.
- Dimensi B tertinggi yang boleh diberikan: `possible_resistance_candidate` — dan hanya bila `evidence_against` mencatat bahwa satu-satunya karakterisasi motif berasal dari pihak yang merasa dikhianati.

**Catatan yang patut dicatat.** Baris [116] pada data sekarang sudah memuat kehati-hatian yang benar di `notes`: *"Kebetulan tahun yg sama dgn defeksi Sultan Mametchia Inderapoura … BELUM ada bukti keterkaitan lang[sung]"*. Disiplin itu sudah ada sebagai kebiasaan; schema ini menaikkannya menjadi field terkendali agar tidak bergantung pada ingatan anotator.

**Peluang yang belum dimanfaatkan:** baris [121] 1676 berasal dari Generale Missiven — sumber **primer periode** — dan menyebut Koto Tangah mengirim barang/pesan ke Aceh. Ini adalah kandidat sumber pembanding independen dari Vogel yang sudah ada di repository tetapi belum pernah disandingkan. Menyandingkannya adalah pekerjaan anotasi, bukan pekerjaan pengumpulan arsip baru.

### 8.4 Pariaman — kasus dengan kewajiban paling spesifik

Rantai: [51] 1671 → [55] 1678 → [66] 1682 → [68] 1684 → [93] 1712.

Kewajiban yang dapat diekstraksi paling tajam di antara empat pilot, karena berupa larangan tindakan konkret:

- [66] 1682: *"niet sullen vermogen eenige vaartuygen naar Aetchin te laten afvaren"* — larangan memberangkatkan kapal ke Aceh.
- [68] 1684: *"niemand uyt Priaman … eenige correspondentie sal mogen houden met die van Aetchin, nog eenigen handel … nog derwaars varen"* — larangan korespondensi, dagang, dan pelayaran.

Pengetatan larangan dari [66] ke [68] adalah **bukti tidak langsung** bahwa larangan pertama tidak efektif — tetapi `implementation_event` yang mendokumentasikan pelanggaran spesifik: **NOT AVAILABLE**. Yang tersedia adalah larangan yang diperbarui, bukan catatan tindakan yang dilarang itu terjadi.

Konsekuensi pemetaan: `evidence_of_absence_vs_absence_of_evidence: silence_only`; `implementation_degree: not_observable`; Dimensi A `indeterminate` atau `noncompliance` (perlu keputusan peneliti); Dimensi B tidak boleh melebihi `possible_resistance_candidate` sampai ada bukti tindakan.

**Penjelasan alternatif yang menonjol:** larangan berulang menyangkut **perdagangan dan pelayaran**, sehingga motif ekonomi (mempertahankan jaringan dagang lama) sama plausibelnya dengan motif politik. Membedakan "resistensi politik" dari "kelangsungan jaringan dagang" adalah keputusan peneliti (§13, D-5).

**Ambiguitas aktor:** `ruler_actor` berbentuk kolektif (`regenten Priaman`) dan berubah antar-episode; radja Ebrahim muncul di [66] sebagai musuh tetapi tidak di [55]. `actor_identity_stable: false` — apakah ini pola berulang oleh pihak yang sama atau episode berbeda oleh faksi berbeda tidak dapat ditentukan dari data.

### 8.5 Verdict: apakah schema mampu menangani keempat kasus?

| Klaster | Schema mampu? | Field pembatas | Batas status yang boleh dicapai |
|---|---|---|---|
| Inderapura | **Ya** | `reciprocal_obligation_id`, `breach_attributed_to: voc` | `partially_ready` |
| Barus | **Ya, dengan pengaman** | `interpretation_source`, aturan §3.3 | `partially_ready` |
| Koto Tangah | **Ya**, dan schema mengekspos kelemahannya | `supporting_claim_ids` bersama | **`descriptive_only` (batas keras)** |
| Pariaman | **Ya** | `evidence_of_absence_vs_absence_of_evidence` | `partially_ready` |

Tidak satu pun mencapai `ready` — dihalangi `report_date` dan `archival_density_known` yang NOT AVAILABLE di seluruh korpus.

---

## 9. Annotation Workflow

### 9.1 Enam belas langkah

| # | Langkah | Keluaran | Lapis |
|---|---|---|---|
| 1 | Identifikasi dokumen | `SourceRecord` | 1 |
| 2 | Verifikasi provenance (koleksi, inventaris, folio) | field provenance | 1 |
| 3 | **Pisahkan `event_date` dari `report_date`** | dua field terpisah, `NOT AVAILABLE` bila tak diketahui | 1 |
| 4 | Transkripsikan bagian relevan | `transcription` | 1 |
| 5 | Buat terjemahan literal | `translation_literal` | 1 |
| 6 | Ekstrak documentary claim + `claim_type` | `DocumentaryClaim` | 2 |
| 7 | Identifikasi komitmen | `commitment_*` | 3–4 |
| 8 | Identifikasi kewajiban (**termasuk kewajiban VOC**) | `Obligation` | 4 |
| 9 | Identifikasi tindakan aktual + status bukti-ketiadaan | `implementation_*` | 3–4 |
| 10 | Bangun hubungan antar-event + catat `pairing_basis` | `Episode` | 4 |
| 11 | Catat bukti pendukung | `evidence_for` | 5 |
| 12 | Catat bukti yang melemahkan | `evidence_against` | 5 |
| 13 | Catat penjelasan alternatif (11 item §6.3) | `alternative_explanations` | 5 |
| 14 | Beri status interpretasi sementara (Dimensi A + B) | `InterpretationRecord` | 5 |
| 15 | Review peneliti | `decision_status` | 5 |
| 16 | Review silang bila anotator kedua tersedia | `reviewer_notes` | 5 |

### 9.2 Aturan pemisahan lapis (mengikat)

- Langkah 4–5 (transkripsi, terjemahan) selesai **sebelum** langkah 6 dimulai. Anotator tidak boleh mulai menafsirkan sambil menyalin.
- Terjemahan bersifat **literal**, bukan parafrase. Frasa yang janggal dipertahankan janggal; kejanggalan itu adalah data.
- Langkah 11–13 dikerjakan **berurutan dan lengkap** sebelum langkah 14. `evidence_against` tidak boleh diisi setelah status interpretasi ditetapkan — urutan ini mencegah pembenaran retrospektif.
- Karakterisasi normatif dari sumber tetap berada di lapis 2. Tidak pernah naik ke `event_summary`.
- **Larangan pencampuran:** satu field tidak boleh memuat transkripsi + terjemahan, atau rekonstruksi + interpretasi. Bila anotator merasa perlu, itu tanda dibutuhkan field baru, bukan izin mencampur.

### 9.3 Aturan `NOT AVAILABLE`

Tiga status berbeda yang **tidak boleh disamakan**: `NOT AVAILABLE` (dicari, tidak ditemukan) · `NOT YET CHECKED` (belum dicari) · `NOT APPLICABLE` (tidak relevan untuk kasus ini). Field kosong tanpa salah satu penanda ini dianggap pekerjaan yang belum selesai.

### 9.4 Urutan pengerjaan pilot yang disarankan

1. **Pariaman** — kewajiban paling spesifik, rantai traktat paling rapat; paling cocok untuk menguji apakah field kewajiban memadai.
2. **Inderapura** — menguji `reciprocal_breach` dan `breach_attributed_to: voc`.
3. **Koto Tangah** — menguji perilaku schema saat bukti lemah; termasuk menyandingkan Generale Missiven 1676 [121] terhadap Vogel sebagai calon sumber pembanding.
4. **Barus** — dikerjakan **terakhir dan dengan pemisahan akses** ke output Model 6, karena paling rawan sirkularitas.

---

## 10. Reliability and Adjudication

Anotasi belum dilakukan; **tidak ada skor reliabilitas yang dihitung atau diperkirakan** dalam dokumen ini.

### 10.1 Pembagian field menurut cara pengujian

| Kelas | Field | Cara uji |
|---|---|---|
| **Exact agreement** | `folio_or_page`, `event_date`, `report_date`, `document_genre`, `obligated_actor`, `obligation_modality`, `commitment_type`, `commitment_form` | Kesepakatan persis antar-anotator; ketidaksepakatan = kesalahan yang dapat diperbaiki |
| **Bounded agreement** | `implementation_degree`, `ComplianceAssessment` (Dimensi A), `commitment_under_duress`, `date_precision` | Kategori berhingga; ketidaksepakatan dicatat dan diadjudikasi |
| **Adjudikasi peneliti** | Dimensi B, `confidence`, `evidence_for`/`evidence_against`, `alternative_explanations`, `pairing_strength` | **Tidak dinilai dengan skor kesepakatan.** Ketidaksepakatan di sini adalah informasi substantif, bukan derau |

Membedakan tiga kelas ini penting: memaksa metrik kesepakatan pada field interpretif akan mendorong anotator berkonvergensi secara prematur — persis kebalikan dari yang dibutuhkan riset hermeneutis.

### 10.2 Prosedur pilot yang diusulkan

1. **Anotasi ganda buta.** Dua anotator mengerjakan subset yang sama tanpa melihat hasil satu sama lain.
2. **Uji konsistensi identifikasi persetujuan.** Apakah kedua anotator menandai event yang sama sebagai komitmen? Ketidaksepakatan di sini menunjukkan definisi "persetujuan substantif" belum cukup tajam (§13, D-2).
3. **Uji konsistensi ekstraksi kewajiban.** Berapa `Obligation` yang diekstrak dari traktat yang sama? Perbedaan jumlah lebih informatif daripada perbedaan isi.
4. **Uji konsistensi pemasangan event.** Apakah `pairing_basis` yang dikutip sama? Pasangan yang hanya ditemukan satu anotator wajib ditinjau — kemungkinan besar `speculative`.
5. **Uji konsistensi evaluasi pelaksanaan.** Dimensi A dibandingkan; ketidaksepakatan `evaded` vs `partially_fulfilled` diperkirakan menjadi titik gesekan utama (§4.5).
6. **Uji interpretasi resistensi.** Dimensi B **tidak diskorkan**. Yang dicatat: apakah kedua anotator menemukan `alternative_explanations` yang sama. Ketidaksepakatan pada Dimensi B dengan `evidence` yang sama adalah temuan metodologis yang layak dilaporkan apa adanya.
7. **Sesi adjudikasi.** Peneliti memutuskan; alasan adjudikasi disimpan di `reviewer_notes`, bukan dihapus.

### 10.3 Kriteria berhenti untuk pilot

Pilot dianggap selesai bila keempat klaster teranotasi penuh, seluruh ketidaksepakatan teradjudikasi, dan definisi kategori tidak lagi berubah selama satu putaran penuh (indikator `stabilitas definisi kategori`, §12).

---

## 11. Relationship to Model 3

### 11.1 Posisi Model 3 saat ini (tidak berubah)

Model 3 tetap sebagaimana adanya: baseline Hawkes univariat eksploratif atas 141 titik waktu. Dokumen ini **tidak** mengusulkan perubahan apa pun terhadapnya, dan tidak menjadikan hasilnya sebagai input anotasi.

### 11.2 Field yang kelak dapat menopang metode lanjutan

| Metode | Field yang dibutuhkan | Tersedia sekarang? |
|---|---|---|
| **Marked Hawkes** | Tanda per titik: `ComplianceAssessment` (Dimensi A) atau `commitment_type` | Tidak — `event_type` yang ada terlalu umum |
| **Multivariate Hawkes** | `actor_ids` & `location_ids` yang stabil dan dinormalisasi | Tidak — `ruler_actor` 135 nilai unik dari 141 baris; `fort_name` 110/141 |
| **Process tracing** | `Episode` lengkap + `mechanism_evidence` + `comparison_case_available` | Tidak |
| **Sequence analysis** | Urutan berlabel dalam episode (komitmen→deviasi→respons) | Tidak |
| **Event-history analysis** | Waktu-ke-peristiwa + risk set + kovariat; `expected_deadline` sebagai titik awal | Tidak |

### 11.3 Catatan penting tentang marked Hawkes

Bila kelak `ComplianceAssessment` dipakai sebagai tanda (*mark*), tanda itu adalah **hasil interpretasi peneliti**, bukan pengukuran independen. Model yang dibangun di atasnya tidak menguji apakah interpretasi itu benar — ia menguji pola temporal *dari* interpretasi itu. Perbedaan ini harus dinyatakan di setiap pelaporan hasil, bukan disimpan di catatan kaki.

### 11.4 Yang tidak boleh dilakukan

- Merancang bentuk final model sebelum distribusi hasil anotasi terlihat. Jumlah episode per kategori Dimensi A saat ini **tidak dapat diperkirakan** — memilih spesifikasi model sekarang berarti memilih tanpa mengetahui apakah kategorinya akan terisi.
- Memakai output model untuk mengisi atau merevisi field anotasi (aturan §3.3).

---

## 12. Minimum Requirements for Advanced Modeling

Kriteria minimum sebelum Hawkes lanjutan (marked/multivariate) **dipertimbangkan**. Angka di kolom "ambang usulan" adalah usulan yang membutuhkan persetujuan peneliti, bukan standar yang sudah ditetapkan.

| # | Kriteria | Ambang usulan | Kondisi saat ini |
|---|---|---|---|
| 1 | Jumlah episode terverifikasi (`researcher_approved`) | ≥ 30 | **0** |
| 2 | Jumlah event per kategori Dimensi A | ≥ 10 per kategori yang akan dipakai sebagai tanda | Tidak dapat dihitung |
| 3 | Kelengkapan tanggal (`event_date` + `report_date`) | ≥ 80% episode | `report_date` **0%** |
| 4 | Kelengkapan aktor (ternormalisasi, stabil) | ≥ 80% episode | Tidak ternormalisasi |
| 5 | Kelengkapan lokasi | ≥ 80% episode | 110/141 = 78% pada level baris |
| 6 | Pasangan `explicit` atau `strong` | ≥ 20 | 9 teridentifikasi pada 4 klaster pilot (belum teranotasi formal) |
| 7 | **Ukuran kepadatan dokumen** | Tersedia per tahun & per koleksi | **Belum ada** |
| 8 | Stabilitas definisi kategori | Tidak berubah selama satu putaran anotasi penuh | Belum diuji |

### 12.1 Kriteria 7 — catatan khusus

Ukuran kepadatan arsip **belum ada**, tetapi bahan mentahnya sudah ada di repository dan belum pernah dipakai untuk keperluan ini:

- `docs/thesis/GM/gm_corpus_filtered_1660_1789.csv` — 102.381 baris, memuat `tahun_surat`/`tahun_efektif`, `volume`, `page`
- `docs/thesis/dr/daghregister_corpus_classified.csv` — 75.651 baris, memuat `tanggal_perkiraan`, `volume`, `book_page_start`/`book_page_end`

Menghitung jumlah surat/halaman per tahun dari kedua file itu **tidak memerlukan sisir arsip baru** — hanya agregasi atas data yang sudah tersimpan. Ini menjadikan Kriteria 7 sebagai butir termurah di seluruh daftar, sekaligus butir yang menghalangi status `ready` bagi setiap episode (§7).

**Peringatan sirkularitas kedua:** distribusi `source_document` di dalam `linimasa_events` sendiri (CD4=20, CD3=18, CD2=15, …) **tidak sah** dipakai sebagai ukuran kepadatan, karena ia menghitung peristiwa yang sudah lolos seleksi peneliti, bukan volume arsip yang tersedia. Ukuran harus datang dari korpus mentah.

---

## 13. Researcher Decisions Required

Empat belas keputusan. Tidak satu pun boleh ditetapkan tanpa pemilik riset.

| ID | Keputusan | Mengapa tidak dapat diputuskan secara teknis |
|---|---|---|
| **D-1** | Apakah rancangan ini dilanjutkan sama sekali, dan dalam bentuk apa (tabel database, spreadsheet anotasi, atau berkas terstruktur di luar produksi)? | Menyangkut biaya kerja manual yang besar terhadap manfaat riset |
| **D-2** | Definisi "persetujuan substantif" vs "pembaruan traktat rutin" | Sebagian besar dari 69 kandidat komitmen mungkin administratif; batasnya adalah pertimbangan historiografis |
| **D-3** | Apakah nilai Dimensi A dan Dimensi B yang diusulkan sudah tepat, kurang, atau berlebih | Taksonomi menentukan apa yang mungkin ditemukan |
| **D-4** | Apakah `evaded` boleh disimpulkan dari pola berulang, atau harus dinyatakan sumber (§4.5) | Menentukan seberapa jauh niat boleh disimpulkan dari perilaku |
| **D-5** | Bagaimana membedakan resistensi politik dari kelangsungan jaringan dagang (kasus Pariaman) | Perbedaan konseptual, bukan perbedaan data |
| **D-6** | Apakah kasus Inderapura diklasifikasikan sebagai sengketa kontrak bilateral, bukan defeksi searah | Mengubah unit analisis untuk seluruh kelas kasus serupa |
| **D-7** | Apakah pengaman anti-sirkularitas Barus (§8.2) diterima, termasuk konsekuensinya bahwa Model 6 tidak boleh mendukung tesis CLD | Menyangkut klaim yang sudah dikutip di beberapa dokumen |
| **D-8** | Apakah batas `descriptive_only` untuk Koto Tangah diterima | Membatasi klaim atas klaster yang selama ini menonjol dalam narasi |
| **D-9** | Apakah ukuran kepadatan arsip dibangun lebih dulu (§12.1) sebelum anotasi dimulai, atau paralel | Menentukan urutan kerja dan validitas klaim antara |
| **D-10** | Ambang angka pada Kriteria 1–8 (§12) | Ambang adalah pilihan metodologis |
| **D-11** | Apakah anotator kedua tersedia; bila tidak, bagaimana reliabilitas ditangani | Menyangkut sumber daya |
| **D-12** | Apakah anotasi dimulai dari empat klaster pilot saja, atau langsung diperluas | Menyangkut generalisasi hasil pilot |
| **D-13** | Apakah kelima kata kunci Belanda (§6.4) dipakai sebagai jalur pencarian, dan bagaimana bias seleksinya dicatat | Kosakata itu adalah kategori VOC, bukan kategori netral |
| **D-14** | Apakah dokumen `cd_resistance_signal_candidates.csv` yang belum ter-*track* di git perlu diamankan lebih dulu | Berkaitan dengan risiko kehilangan kerja yang sudah pernah terjadi di proyek ini |

---

## 14. Risks and Limitations

### 14.1 Risiko yang melekat pada rancangan ini

**Beban kerja manual.** Anotasi penuh per episode membutuhkan transkripsi, terjemahan literal, ekstraksi klaim, dan penilaian berlapis. Empat klaster pilot mencakup sekitar 25 baris dari 141. Perluasan ke seluruh korpus adalah pekerjaan berbulan, bukan berhari.

**Formalisasi berlebih.** Menuangkan pembacaan hermeneutis ke dalam field terkendali selalu kehilangan sesuatu. Field `researcher_notes` yang berbentuk prosa bebas dipertahankan justru untuk menampung yang tidak muat — dan isinya tidak boleh dianggap kalah penting dari field terstruktur.

**Kategori yang membentuk temuan.** Menyediakan nilai `probable_resistance_candidate` membuat anotator lebih mungkin menemukannya. Ini tidak dapat dihilangkan, hanya dapat dibuat terlihat — karena itu Dimensi B mewajibkan `evidence_against` dan tidak pernah lepas dari `researcher_review_required`.

### 14.2 Risiko sirkularitas (berulang, karena paling serius)

Dua jalur telah teridentifikasi:

1. **Model → label → pembenaran model** (Barus/Model 6, §8.2). Dijaga oleh `interpretation_source` dan aturan §3.3.
2. **Seleksi peneliti → ukuran kepadatan → kontrol confound** (§12.1). Dijaga dengan mensyaratkan ukuran kepadatan dari korpus mentah, bukan dari `linimasa_events`.

Jalur ketiga yang belum tertutup: bila anotator yang sama yang membangun `linimasa_events` juga mengerjakan anotasi episode, penilaian sebelumnya akan terbawa. Tidak ada pengaman teknis untuk ini; hanya kesadaran dan, bila memungkinkan, anotator kedua (D-11).

### 14.3 Keterbatasan sumber yang tidak dapat diatasi oleh rancangan apa pun

- Seluruh korpus utama ditulis dari posisi VOC. Suara aktor lokal hadir terutama sebagai **kutipan di dalam** dokumen VOC. Schema dapat menandai ini (`source_perspective`) tetapi tidak dapat memperbaikinya.
- `report_date` mungkin tetap `NOT AVAILABLE` untuk banyak baris bahkan setelah pemeriksaan ulang, karena kompilasi seperti Corpus Diplomaticum tidak selalu mempertahankan informasi itu.
- Motif tidak dapat diamati. Yang dapat diamati adalah tindakan, dan karakterisasi tindakan oleh pihak yang berkepentingan. Setiap klaim tentang niat aktor lokal — termasuk klaim resistensi — adalah inferensi, dan schema ini dirancang agar inferensi itu tetap terlihat sebagai inferensi.

### 14.4 Pernyataan penutup

Rancangan ini **tidak** menunjukkan bahwa tesis *"Iyokan nan di urang, laluan nan di awak"* benar atau salah. Ia merancang kondisi agar pertanyaan itu dapat diperiksa dengan bukti, dengan penjelasan alternatif yang dicatat sejajar, dan dengan interpretasi yang tidak pernah menyamar sebagai fakta.

Empat klaster pilot menunjukkan hasil awal yang perlu dicatat apa adanya: satu klaster (Inderapura) justru menempatkan kegagalan pada VOC menurut sumbernya sendiri; satu klaster (Koto Tangah) bertumpu pada sumber sekunder retrospektif yang memakai bahasa moral pihak yang merasa dikhianati; satu klaster (Pariaman) memiliki larangan yang sangat spesifik tetapi tanpa catatan pelanggaran yang spesifik; satu klaster (Barus) memiliki rantai tekstual terkuat sekaligus risiko sirkularitas tertinggi. Tidak satu pun dari keempatnya, pada tahap ini, merupakan episode resistensi yang telah ditetapkan.

> **DRAFT FOR RESEARCHER REVIEW — NOT IMPLEMENTED — NOT A FINAL HISTORICAL INTERPRETATION**
