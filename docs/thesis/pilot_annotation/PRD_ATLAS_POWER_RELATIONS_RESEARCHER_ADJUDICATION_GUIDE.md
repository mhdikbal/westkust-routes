# Researcher Adjudication Guide — Atlas Power Relations V2.1

> **Status:** PROCEDURAL GUIDE, tidak mengotorisasi keputusan apa pun
> **Baseline:** `e56102ff2f33dc10eb0811bc8f4df0c9ef70acf1`
> **Guide ini tidak mengisi DEC-01–DEC-18, tidak memilih package, dan tidak mengotorisasi implementasi**

---

## 1. Purpose

Dokumen ini adalah prosedur, bukan keputusan. Tujuannya semata membantu peneliti menjalankan gerbang **Researcher Adjudication** (Gate 1 dari 8 production gates) secara terstruktur: urutan yang disarankan, bukti yang dibutuhkan per keputusan, dan aturan pencatatan hasil — tanpa mengisi satu pun dari 18 keputusan itu sendiri.

---

## 2. Frozen Baseline

```text
Commit:                e56102ff2f33dc10eb0811bc8f4df0c9ef70acf1
V1 Natal:               COMPLETE AND SERVER-VALIDATED
V2 Koto Tangah:         COMPLETE AND SERVER-VALIDATED
V3 Tiku:                COMPLETE AND SERVER-VALIDATED
V4 Sillida:              COMPLETE AND SERVER-VALIDATED
Failure synthesis:      COMPLETE AND SERVER-SYNCED
Genuine failures:       10
Failure clusters:       7
Proposed changes:       8, seluruhnya PROPOSED_ONLY
Revalidation tests:     10
Researcher decisions:   18, seluruhnya PENDING
Draft V2:               FROZEN AND UNCHANGED
Draft V2.1:              NOT AUTHORIZED
Production gate:        0/8, BLOCKED
Graphify:                DEFERRED
Atlas production integration: BLOCKED
```

Sumber angka: `docs/thesis/colab/POST_V1_V4_ONTOLOGY_FAILURE_INVENTORY.csv` (10 baris), `POST_V1_V4_ONTOLOGY_FAILURE_CLUSTERS.csv` (7 baris), `ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CHANGESET_LEDGER.csv` (8 baris), `ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv` (10 baris), `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` (18 baris, `DEC-01`…`DEC-18`).

---

## 3. PRD Status

```text
PRD_READY_FOR_RESEARCHER_REVIEW
```

PRD (`docs/thesis/pilot_annotation/PRD_ATLAS_POWER_RELATIONS_LONG_TERM_SCALE.md`) bukan otorisasi implementasi. PRD merekomendasikan paket **Balanced**, tetapi pemilihan paket tetap keputusan peneliti (lihat §4).

---

## 4. Package Options

| Paket | Cakupan | Trade-off |
|---|---|---|
| **Minimal** | identity continuity, explicit non-identity, mandate status/scope, rights/privilege model | migrasi rendah, risiko overfit rendah; institutional hesitation/constrained agency/resistance target/dispute settlement tetap tidak termodelkan |
| **Balanced** (rekomendasi PRD, belum disetujui) | Minimal + institutional-state observation + institutional-presence observation + resistance-target fields + constrained-agency structure + bounded dispute-settlement object | menunda spatial-feature redesign, public ontology expansion, Graphify, production migration penuh |
| **Expanded Research** | seluruh perubahan research-only kecuali yang belum cukup bukti | model lebih besar, validator/migrasi lebih berat, peluang overfit meningkat |

Status pemilihan paket: **PENDING** — tidak ada paket yang berstatus selected/approved.

---

## 5. Five Blocking Decisions

Diselesaikan lebih dulu, dalam urutan ini:

1. **DEC-01** — Identity continuity fields (CH-01/CH-02)
2. **DEC-04** — Rights/privilege object versus relation types (CH-03)
3. **DEC-09** — Command relation versus structured operation object (CH-07)
4. **DEC-10** — Constrained-agency annotation fields (bagian dari CH-07)
5. **DEC-14** — Penamaan: Draft V2.1 versus Draft V3

---

## 6. Remaining Thirteen Decisions

DEC-02, DEC-03, DEC-05, DEC-06, DEC-07, DEC-08, DEC-11, DEC-12, DEC-13, DEC-15, DEC-16, DEC-17, DEC-18 — lihat `recommended_option` / `alternative_options` per baris di `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` untuk detail lengkap tiap keputusan. Guide ini sengaja tidak meringkas isi tiap opsi agar peneliti membaca ledger asli, bukan ringkasan pihak ketiga.

---

## 7. Decision Dependencies

- DEC-14 (penamaan V2.1 vs V3) memengaruhi bagaimana seluruh 8 proposed changes lain dirujuk dalam ontology contract berikutnya — sebaiknya diputuskan lebih awal.
- DEC-09 dan DEC-10 sama-sama berasal dari CH-07 (command/constrained agency) — keduanya sebaiknya diputuskan berurutan agar konsisten.
- Pemilihan paket (§4) memengaruhi cakupan efektif DEC-05–DEC-08 dan DEC-11–DEC-13 (fields yang termasuk Balanced vs Expanded Research).
- Keputusan non-blocking lain umumnya independen tetapi harus diperiksa terhadap `supporting_failures` dan `supporting_cases` masing-masing di ledger sebelum difinalisasi, untuk memastikan tidak ada keputusan yang saling bertentangan.

---

## 8. Recommended Decision Order

```text
1. Choose package (Minimal / Balanced / Expanded Research)
2. Resolve DEC-01
3. Resolve DEC-04
4. Resolve DEC-09
5. Resolve DEC-10
6. Resolve DEC-14
7. Resolve remaining 13 decisions
8. Freeze decision ledger
9. Push and server-sync decision milestone
10. Authorize ontology contract construction
```

Urutan ini mengikuti Section 29 PRD ("Immediate Next Action") dan tidak mengubahnya.

---

## 9. Evidence Required for Each Decision

Untuk setiap DEC-xx, sebelum memutuskan, periksa di `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv`:

- `supporting_failures` — failure_uid mana dari `POST_V1_V4_ONTOLOGY_FAILURE_INVENTORY.csv` yang mendasari keputusan ini;
- `supporting_cases` — kasus V1–V4 (dan Painan) mana yang menunjukkan gap ini secara empiris;
- `impact_if_approved` dan `impact_if_rejected` — konsekuensi ke ontology contract, validator, dan migrasi;
- `public_impact` — apakah keputusan ini mengubah apa yang tampil ke pembaca umum;
- `migration_impact` — apakah lima artifact V1–V4 perlu dimigrasikan ulang jika disetujui.

Jika bukti pendukung dirasa tidak cukup untuk satu keputusan, opsi yang sah adalah `DEFERRED` atau `REQUIRES_MORE_EVIDENCE` (lihat §10, vocabulary FR-14 PRD), bukan memaksakan `APPROVED`.

---

## 10. Consequences of Approval

Keputusan berstatus `APPROVED` atau `APPROVED_WITH_LIMITATIONS`:

- change terkait berpindah dari `PROPOSED_ONLY` menuju cakupan ontology contract berikutnya (V2.1/V3) — tetapi perpindahan status itu sendiri baru terjadi pada Phase 1 (Ontology Contract), bukan otomatis oleh guide ini;
- revalidation test terkait (di `ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv`) menjadi wajib dijalankan setelah migrasi;
- lima artifact V1–V4 berpotensi perlu re-migrasi nonproduksi (Phase 3) jika `migration_impact` tidak kosong.

---

## 11. Consequences of Deferral

Keputusan berstatus `DEFERRED`:

- change terkait tetap `PROPOSED_ONLY`, tidak masuk ontology contract berikutnya;
- tidak memblokir keputusan lain yang independen;
- dapat diangkat kembali pada milestone adjudikasi berikutnya tanpa mengulang seluruh proses V1–V4.

---

## 12. Consequences of Rejection

Keputusan berstatus `REJECTED`:

- change terkait tidak diimplementasikan pada ontology contract manapun yang direncanakan saat ini;
- failure asal (`supporting_failures`) tetap tercatat sebagai limitasi yang diketahui dan diterima (pola yang sama seperti disposisi `PASS_WITH_LIMITATIONS` pada V1–V4);
- tidak menghapus baris dari failure inventory — inventory tetap merupakan catatan historis proses validasi.

---

## 13. Decision Recording Rules

- Isi kolom `researcher_decision` di `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` menggunakan salah satu dari vocabulary FR-14 PRD: `PENDING`, `APPROVED`, `APPROVED_WITH_LIMITATIONS`, `DEFERRED`, `REJECTED`, `REQUIRES_MORE_EVIDENCE`.
- Isi `researcher_notes` dengan alasan singkat, terutama untuk `DEFERRED`/`REJECTED`/`REQUIRES_MORE_EVIDENCE`.
- Jangan menghapus atau menulis ulang baris `failure_uid`, `cluster_id`, atau `change_id` — hanya kolom keputusan yang berubah.
- Jangan mengubah `implementation_status` di changeset ledger dari `PROPOSED_ONLY` — perubahan status implementasi terjadi di Phase 1 (Ontology Contract), bukan saat mengisi decision ledger.

---

## 14. Decision Commit Rules

- Commit keputusan peneliti **terpisah** dari commit apa pun yang mengimplementasikan Draft V2.1/V3, validator, atau migrasi.
- Pesan commit harus menyatakan eksplisit: jumlah keputusan APPROVED/DEFERRED/REJECTED/REQUIRES_MORE_EVIDENCE, paket yang dipilih, dan bahwa Draft V2 tetap tidak diubah.
- Push dan server-sync commit keputusan mengikuti guard yang sama seperti milestone sintesis sebelumnya (checksum, validator chain, tidak ada perubahan runtime).

---

## 15. Stop Conditions

Hentikan proses adjudikasi dan jangan lanjut ke Phase 1 (Ontology Contract) jika:

- ada keputusan blocking (DEC-01/04/09/10/14) yang masih PENDING;
- ada dua keputusan yang secara eksplisit kontradiktif (mis. memilih Option A pada satu DEC yang mengasumsikan Option B pada DEC lain);
- paket belum dipilih;
- decision ledger belum di-commit dan di-server-sync.

---

## 16. Next Authorized Action

Setelah guide ini dipublikasikan, satu-satunya aksi yang diotorisasi pada turn berikutnya adalah:

```text
RESEARCHER ADJUDICATION OF DEC-01–DEC-18
```

dimulai dari lima keputusan blocking (§5), diikuti pemilihan paket (§4) dan 13 keputusan sisa (§6), lalu commit terpisah (§14). Tidak ada Draft V2.1, tidak ada implementasi, tidak ada Graphify/Atlas, sampai langkah ini selesai dan dibekukan.
