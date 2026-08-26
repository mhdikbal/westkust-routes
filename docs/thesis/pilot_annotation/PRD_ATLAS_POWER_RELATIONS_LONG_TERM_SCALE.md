# PRODUCT REQUIREMENTS DOCUMENT
# Atlas Relasi Kekuasaan: Skala Jangka Panjang

> **Status:** DRAFT PRD FOR RESEARCHER ADJUDICATION  
> **Baseline:** `e56102ff2f33dc10eb0811bc8f4df0c9ef70acf1`  
> **Draft V2:** FROZEN, belum diubah  
> **Draft V2.1:** BELUM DIOTORISASI  
> **Produksi:** 0/8 gate terpenuhi, integrasi tetap diblokir  
> **Graphify:** ditunda  
> **Dokumen ini bukan otorisasi implementasi, migrasi, commit, push, atau deploy**

---

## 1. Ringkasan Eksekutif

Atlas Relasi Kekuasaan akan dikembangkan dari model teritorial satu-status menjadi sistem penelitian dan publikasi yang dapat merepresentasikan kekuasaan sebagai relasi bertanggal, bertumpuk, bersumber, dan tidak selalu menghasilkan kontrol efektif.

Produk masa depan harus mampu membedakan:

- lokasi dari aktor;
- jabatan dari pemegang jabatan;
- faksi dari komunitas;
- laporan dokumenter dari peristiwa historis;
- klaim yurisdiksi dari kontrol efektif;
- traktat dari kedaulatan;
- perlindungan dari ketundukan;
- kehadiran institusional dari dominasi;
- koersi dari kepatuhan;
- komando dari persetujuan politik;
- perubahan aliansi dari hubungan paralel;
- teori dari fakta historis;
- ketidaktersediaan bukti dari bukti ketidakadaan.

PRD ini merancang jalur pengembangan bertahap dari baseline riset saat ini menuju:

1. adjudikasi peneliti;
2. Ontology Contract V2.1 atau V3;
3. generalized validator;
4. migrasi nonproduksi V1–V4;
5. prototipe relasional multi-kasus;
6. Atlas Research Layer opt-in;
7. integrasi graph terbatas;
8. perluasan lintas-wilayah dan lintas-korpus;
9. produksi publik yang dapat diaudit.

---

## 2. Latar Belakang

### 2.1 Masalah model lama

Model Atlas lama memakai status dominion tunggal per lokasi dan periode. Pendekatan tersebut berguna untuk orientasi visual, tetapi berisiko menyiratkan:

```text
one location
+ one year
= one ruler
= one territorial status
= one form of effective control
```

Rangkaian validasi menunjukkan bahwa asumsi tersebut tidak memadai.

### 2.2 Baseline penelitian

Status penelitian yang dibekukan:

```text
V1 Natal 1760:
COMPLETE AND SERVER-VALIDATED

V2 Koto Tangah:
COMPLETE AND SERVER-VALIDATED

V3 Tiku:
COMPLETE AND SERVER-VALIDATED

V4 Sillida:
COMPLETE AND SERVER-VALIDATED

Failure synthesis:
COMPLETE AND SERVER-SYNCED

Genuine failures:
10

Failure clusters:
7

Proposed changes:
8, all PROPOSED_ONLY

Revalidation tests:
10

Researcher decisions:
18, all PENDING
```

### 2.3 Temuan desain utama

Dua gap telah dikonfirmasi lintas-kasus:

```text
1. Actor identity, continuity, mandate, and explicit non-identity
2. Rights, privileges, exemption, release, and modification
```

Gap keselamatan epistemik lain yang memerlukan keputusan:

```text
- institutional state and hesitation
- institutional presence
- resistance target
- command and constrained agency
- dispute settlement and fine allocation
- ambiguous spatial feature, masih requires more evidence
```

---

## 3. Visi Produk

Membangun Atlas sejarah relasional yang memungkinkan pembaca umum dan peneliti memahami bagaimana kekuasaan dibentuk melalui kontrak, perlindungan, perdagangan, jabatan, klaim, kehadiran militer, koersi, mediasi, dan kepatuhan yang berubah dari waktu ke waktu.

Produk harus menjadi:

```text
source-linked
relation-centered
temporally explicit
uncertainty-aware
researcher-governed
publicly legible
reproducible
backward-compatible
```

---

## 4. Prinsip Produk

### P1. Arsip mendahului teori

Teori hanya mengorganisasi pertanyaan dan interpretasi. Teori tidak boleh mengisi kekosongan sumber.

### P2. Klaim tidak sama dengan kontrol

Traktat, penerimaan formal, kehadiran militer, kontrol benteng, kontrol perdagangan, dan kepatuhan lokal harus tetap menjadi kategori berbeda.

### P3. Ketidakpastian adalah data

Nilai `CANNOT_DETERMINE`, `NOT_TESTABLE`, identitas ambigu, mandat terbatas, dan feature type tidak pasti harus dapat disimpan dan ditampilkan.

### P4. Tidak ada homogenisasi aktor

Lokasi, komunitas, faksi, jabatan, pemegang jabatan, dan kategori sumber tidak boleh digabung tanpa bukti kontinuitas dan mandat.

### P5. Progressive disclosure

Pembaca umum melihat ringkasan yang berhati-hati. Peneliti dapat membuka provenance, passage locator, teori, counterevidence, dan uncertainty detail.

### P6. Additive dan reversible

Layer relasional baru tidak menggantikan layer legacy sebelum validasi produksi dan keputusan deprecation terpisah.

### P7. Human adjudication

Perubahan ontologi, public copy, dan klaim sejarah memerlukan persetujuan peneliti. Tidak ada auto-promotion dari hasil model atau annotation.

---

## 5. Sasaran

### 5.1 Sasaran 12 bulan

- menyelesaikan DEC-01–DEC-18;
- membekukan Ontology Contract berikutnya;
- membuat generalized validator;
- merevalidasi V1–V4;
- membangun prototipe multi-kasus lokal;
- menguji aksesibilitas, responsive behavior, dan progressive disclosure;
- membangun Atlas Research Layer opt-in tanpa migrasi produksi besar;
- menguji satu alur sumber ke relasi hingga public display.

### 5.2 Sasaran 24 bulan

- memperluas artefak relasional ke 12 kasus cross-case;
- menambah provenance passage-level yang lebih lengkap;
- menyediakan timeline relasi dan claim/control observations;
- menyediakan ekspor riset JSON/CSV yang tervalidasi;
- menguji graph projection nonproduction;
- menyiapkan governance versioning dan review workflow;
- menjalankan pilot publik terbatas.

### 5.3 Sasaran jangka panjang

- relasi kekuasaan Pantai Barat Sumatra lintas abad;
- dukungan korpus VOC, EIC, Prancis, dan sumber lokal bila tersedia;
- integrasi entitas tempat, aktor, jabatan, komoditas, dokumen, dan episode;
- query lintas-kasus yang dapat diaudit;
- publikasi dataset FAIR dengan DOI dan provenance;
- kerangka yang dapat digunakan kembali untuk wilayah sejarah lain.

---

## 6. Non-Sasaran

Produk tidak bertujuan:

- menentukan satu penguasa absolut bagi setiap lokasi;
- menghasilkan payoff numerik tanpa sumber;
- menyatakan equilibrium historis tanpa bukti;
- mengklasifikasikan resistensi secara otomatis;
- menetapkan patron-client sebagai edge default;
- mengganti kritik sumber dengan graph analytics;
- mengubah sumber kolonial menjadi deskripsi netral;
- menyediakan prediksi sejarah;
- menghapus layer lama sebelum proses deprecation formal;
- membuat Graphify sebagai sumber kebenaran primer.

---

## 7. Pengguna

### 7.1 Peneliti utama

Kebutuhan:

- mengaudit setiap relasi;
- membandingkan source statement dan reconstruction;
- menerima atau menolak perubahan ontologi;
- melihat contradiction dan source asymmetry;
- menjalankan validator;
- membekukan milestone.

### 7.2 Kolaborator riset

Kebutuhan:

- mengusulkan actor identity;
- menambahkan source locator;
- melakukan review terarah;
- tidak dapat mengubah klaim publik tanpa approval.

### 7.3 Pembaca umum

Kebutuhan:

- memahami hubungan utama tanpa teori mentah;
- membedakan klaim dan kontrol;
- melihat sumber dan keterbatasan;
- menjelajahi timeline tanpa terminologi berlebihan.

### 7.4 Pengembang dan research engineer

Kebutuhan:

- schema yang stabil;
- validation contract;
- migration plan;
- test fixtures;
- isolation antara riset dan produksi;
- rollback yang jelas.

### 7.5 Pengguna data

Kebutuhan:

- ekspor berlisensi;
- field definitions;
- version identifier;
- provenance;
- reproducible checksums;
- citation guidance.

---

## 8. Paket Produk

Keputusan final paket tetap berada pada adjudikasi peneliti. PRD merekomendasikan paket **Balanced**.

### 8.1 Minimal

Mencakup hanya gap lintas-kasus:

- identity continuity;
- explicit non-identity;
- mandate status dan scope;
- rights/privilege model.

Kelebihan:

- migrasi rendah;
- risiko overfit rendah.

Kekurangan:

- institutional hesitation;
- constrained agency;
- resistance target;
- dispute settlement tetap tidak termodelkan.

### 8.2 Balanced, direkomendasikan

Mencakup:

- seluruh paket Minimal;
- institutional-state observation;
- institutional-presence observation;
- resistance-target fields;
- constrained-agency structure;
- bounded dispute-settlement object.

Ditunda:

- spatial-feature redesign;
- public ontology expansion;
- Graphify;
- production migration penuh.

### 8.3 Expanded Research

Mencakup seluruh perubahan research-only kecuali yang benar-benar belum cukup bukti.

Risiko:

- model terlalu besar;
- validator dan migrasi lebih berat;
- peluang overfit meningkat.

---

## 9. Persyaratan Fungsional

## FR-1. Actor Identity and Continuity

Sistem harus dapat menyatakan:

- aktor terkonfirmasi sama;
- aktor mungkin sama;
- kontinuitas tidak dapat diuji;
- dua aktor sengaja tidak digabung;
- predecessor/successor bersifat kandidat;
- nama tempat yang sama tidak membuktikan aktor yang sama.

Candidate fields:

```text
identity_continuity_status
membership_continuity_status
possible_predecessor_actor_ids
possible_successor_actor_ids
explicit_non_identity_with
identity_evidence
```

Acceptance:

- pongelous Tiku 1662 tidak otomatis digabung dengan regenten 1684;
- kolektif Koto Tangah tidak dipanjangkan otomatis selama 95 tahun.

## FR-2. Mandate

Sistem harus merepresentasikan:

```text
mandate_status
mandate_scope
mandate_source
represented_actor_ids
represented_location_ids
valid_from
valid_to
researcher_review_required
```

Mandat episode-specific tidak boleh dipromosikan menjadi mandat permanen.

## FR-3. Rights and Privileges

Sistem harus membedakan:

- hak yang diklaim;
- hak yang dipegang;
- hak yang diberikan;
- hak yang dibebaskan;
- hak yang dilepaskan;
- hak yang dicabut;
- hak yang diperbarui.

Rekomendasi model:

```text
CommercialRight
RightModification
```

Candidate action vocabulary:

```text
GRANTS
WAIVES
RELEASES
REVOKES
RENEWS
EXEMPTS
```

Candidate right type:

```text
TOLL_RIGHT
TOLL_EXEMPTION
TRADE_ACCESS
FIXED_PRICE_PRIVILEGE
CUSTOMS_PRIVILEGE
MONOPOLY_RIGHT
```

## FR-4. Institutional State

Sistem harus dapat merepresentasikan keadaan internal institusi tanpa membuat edge palsu.

Candidate object:

```text
InstitutionalStateObservation
```

Fields:

```text
institution_id
state_type
commitment_status
authorization_status
observed_at
source_document_ids
source_passage_locator
interpretive_status
```

Contoh:

- keraguan pejabat VOC terhadap pengambilalihan Natal;
- keputusan tertunda;
- otorisasi belum tersedia.

## FR-5. Institutional Presence

Sistem harus membedakan pembukaan kantor atau pos dari kontrol efektif.

Candidate object:

```text
InstitutionalPresenceObservation
```

Fields:

```text
institution_id
location_id
presence_type
valid_from
valid_to
source_document_ids
claim_or_effective_control
```

## FR-6. Resistance Target

`resistance_candidate` tetap research-only dan harus memiliki target.

Fields:

```text
resistance_target_actor_ids
resistance_target_institution_ids
resistance_target_relation_type
resistance_object
resistance_scope
```

Sistem harus dapat menyatakan:

```text
resistance to Aceh:
PARTIALLY_SUPPORTED

resistance to VOC:
NOT_TESTABLE
```

## FR-7. Command and Constrained Agency

Sistem harus merekam pengerahan atau komando tanpa menyiratkan aliansi atau consent.

Candidate historical structure:

```text
OperationParticipation
CommandObservation
```

Fields:

```text
commanding_actor_id
participating_group_id
operation_id
dependency_status
coercion_status
ability_to_refuse
voice_availability
political_intent
constrained_agency
source_document_ids
```

## FR-8. Dispute Settlement

Sistem harus dapat merepresentasikan:

- pihak bersengketa;
- mediator;
- pembayar;
- penerima;
- bagian denda;
- objek sengketa;
- tanggal settlement;
- sumber.

Candidate object:

```text
DisputeSettlement
FineAllocation
```

## FR-9. Spatial Uncertainty

Untuk sementara research-only dan deferred.

Candidate fields:

```text
source_place_expression
normalized_location_candidate
possible_feature_types
feature_type_confidence
spatial_scope_status
```

Tidak masuk implementasi pertama kecuali keputusan peneliti mengubah statusnya.

## FR-10. Evidence Contract

Setiap relation atau structured observation wajib membawa:

```text
source_document_ids
source_passage_locator
event_ids
parent_episode_ids
provenance_status
evidence_strength
interpretive_status
explicit_or_inferred
researcher_review_required
```

## FR-11. Four-Layer Text Contract

Setiap record yang ditampilkan publik harus memisahkan:

```text
source_statement_summary
historical_reconstruction
theoretical_annotation
public_display_summary
```

Tidak boleh ada auto-promotion tanpa review.

## FR-12. Temporal Model

Sistem harus mendukung:

```text
valid_from
valid_to
date_precision
open_ended
observed_at
superseded_by
contradicted_by
```

Relasi bertumpuk harus didukung.

## FR-13. Contradictions

Sumber yang bertentangan disimpan sebagai observations terpisah. Sistem tidak boleh menyelesaikan contradiction melalui voting sumber.

## FR-14. Researcher Adjudication

Perubahan status harus mengikuti:

```text
PENDING
APPROVED
APPROVED_WITH_LIMITATIONS
DEFERRED
REJECTED
REQUIRES_MORE_EVIDENCE
```

Hanya peneliti yang dapat mengubah keputusan ke status final.

## FR-15. Versioning

Setiap ontology contract harus memiliki:

- version ID;
- Git commit;
- changelog;
- changeset ledger;
- migration specification;
- validator version;
- compatible artifact versions;
- rollback target.

---

## 10. Persyaratan Nonfungsional

### NFR-1. Reproducibility

- checksum setiap artefak;
- deterministic IDs;
- frozen fixtures;
- versioned validator output.

### NFR-2. Auditability

Setiap perubahan harus menunjukkan:

- siapa menyetujui;
- kapan;
- dasar kegagalan;
- kasus pendukung;
- alternatif yang ditolak;
- dampak migrasi.

### NFR-3. Performance

Target awal research layer:

```text
up to 10,000 actors
up to 50,000 relations and observations
up to 100,000 source links
```

Target response lokal:

- filter relasi kurang dari 300 ms pada dataset pilot;
- initial load kurang dari 2 detik pada desktop modern;
- detail drawer kurang dari 150 ms setelah data tersedia.

Target ini harus diuji, bukan diasumsikan.

### NFR-4. Accessibility

- keyboard navigation;
- visible focus;
- non-color semantic distinctions;
- readable contrast;
- no hover-only evidence;
- mobile viewport tanpa overflow;
- reduced-motion support.

### NFR-5. Security

- research artifact tidak boleh dieksekusi sebagai code;
- no secrets dalam datasets;
- API read-only pada tahap pilot;
- source access restrictions dihormati;
- restricted files tidak dipublikasikan.

### NFR-6. Reliability

- validator fail-closed untuk synced dependencies;
- local-only dependency policy eksplisit;
- tidak ada wildcard skip;
- tidak ada silent normalization.

### NFR-7. Maintainability

- common schema;
- centralized vocabularies;
- shared validator library;
- case-specific fixtures terpisah;
- documentation generated from schema bila mungkin.

---

## 11. Arsitektur Target

### 11.1 Layer

```text
Source Layer
→ Documentary Report Layer
→ Event and Parent Episode Layer
→ Actor, Location, Office, Commodity Layer
→ Relation and Observation Layer
→ Annotation Layer
→ Public Presentation Layer
```

### 11.2 Source of truth

Urutan otoritas:

```text
source documents
reviewed research artifacts
validated ontology records
research API or static bundle
graph projection
public UI
```

Graphify tidak boleh menjadi sumber primer.

### 11.3 Penyimpanan tahap awal

```text
reviewed JSON artifacts
+ JSON Schema
+ generalized validator
+ static research prototype
```

Database migration belum diperlukan pada fase pertama V2.1.

### 11.4 Penyimpanan tahap produksi

Evaluasi setelah revalidation:

- PostgreSQL relational tables;
- JSONB untuk annotation yang versioned;
- graph projection read model;
- immutable provenance links;
- audit log.

---

## 12. Generalized Validator

Validator umum harus memeriksa:

1. schema version;
2. unique IDs;
3. endpoint integrity;
4. source locators;
5. controlled vocabularies;
6. actor identity rules;
7. mandate rules;
8. temporal consistency;
9. claim/control separation;
10. rights modification direction;
11. command versus consent;
12. constrained agency;
13. resistance target;
14. public/research separation;
15. synced/local-only dependency policy;
16. case-specific extensions;
17. no forbidden edges;
18. backward compatibility;
19. regression fixtures;
20. machine-readable failure report.

Output minimum:

```json
{
  "validator_version": "...",
  "ontology_version": "...",
  "artifact_id": "...",
  "result": "PASS|FAIL",
  "checks": [],
  "warnings": [],
  "failures": []
}
```

---

## 13. Migrasi Artefak

Tahap migrasi harus nonproduksi dan additive.

### 13.1 Urutan

```text
Painan
Natal
Koto Tangah
Tiku
Sillida
```

### 13.2 Prinsip

- original frozen artifact tidak ditimpa;
- hasil migrasi ditulis sebagai file baru;
- transformation manifest wajib;
- before/after checksum;
- field additions tidak membuat klaim baru;
- unresolved failure tetap terlihat;
- rollback berarti kembali ke artifact versi lama.

### 13.3 Acceptance

Setiap migrated artifact harus:

- lolos generalized validator;
- mempertahankan validator legacy;
- menyelesaikan hanya failure yang disetujui;
- tidak mengubah public copy tanpa review;
- tidak menciptakan actor merge baru.

---

## 14. Multi-Case Prototype

### 14.1 Views

- case overview;
- actor browser;
- relation timeline;
- network view;
- claim versus control;
- rights and privileges;
- institutional observations;
- constrained agency;
- source drawer;
- theory drawer;
- public-copy preview;
- cross-case comparison.

### 14.2 Required cases

```text
Painan
Natal
Koto Tangah
Tiku
Sillida
```

### 14.3 Interaction

- filtering case, actor, relation, date;
- compare two cases;
- toggle observations and relations;
- show unresolved identity;
- show rights modification;
- no default theory view.

### 14.4 Research questions

- apakah pembaca membedakan claim dan control;
- apakah non-identitas aktor dipahami;
- apakah command tidak dibaca sebagai alliance;
- apakah rights release dipahami tanpa membalik arah;
- apakah resistance target jelas;
- apakah uncertainty tetap terbaca.

---

## 15. Atlas Research Layer

### 15.1 Mode

```text
opt-in
research beta
non-default
```

### 15.2 Legacy compatibility

- legacy territorial layer tetap tersedia;
- tidak ada silent color reinterpretation;
- relation layer tidak mengubah route geometry;
- tidak ada marker removal;
- deprecation memerlukan PRD terpisah.

### 15.3 Public labels

Gunakan label sederhana:

```text
Perlindungan
Negosiasi
Perjanjian dan kewajiban
Hak dan privilese
Klaim yurisdiksi
Kehadiran institusional
Kehadiran militer
Kontrol benteng
Penguasaan dagang
Perubahan hubungan
Hubungan yang diperdebatkan
```

Raw theory tetap Level 3 research detail.

---

## 16. Graphify Strategy

### 16.1 Preconditions

Graphify baru diizinkan setelah:

- Ontology V2.1/V3 approved;
- generalized validator pass;
- migrated V1–V4 pass;
- multi-case prototype pass;
- graph projection contract approved;
- deletion and rollback strategy approved.

### 16.2 Graph projection

Hanya proyeksikan:

- reviewed actors;
- reviewed locations;
- reviewed offices;
- first-class relations;
- temporal intervals;
- source IDs;
- uncertainty metadata.

Jangan proyeksikan sebagai factual edges:

- patron-client classification;
- resistance candidate;
- power theory;
- repeated coercion;
- failed deterrence;
- political intent.

### 16.3 Rebuild policy

Graph harus disposable dan dapat dibangun kembali dari reviewed canonical data.

---

## 17. Workflow dan Governance

### 17.1 Status perubahan

```text
PROPOSED_ONLY
RESEARCHER_APPROVED
IMPLEMENTED_NONPRODUCTION
REVALIDATED
PROTOTYPE_APPROVED
PRODUCTION_APPROVED
DEPLOYED
DEPRECATED
```

### 17.2 Manual approval gates

Manual approval diwajibkan untuk:

- ontology changes;
- actor merge;
- mandate assertion;
- public-copy change;
- migration;
- Graphify;
- production routes;
- deploy.

### 17.3 Separation of duties

```text
Model/agent:
extract, validate, propose

Research engineer:
implement, test, document

Researcher:
adjudicate, approve historical claims

Deployment operator:
push and deploy after authorization
```

---

## 18. Production Gates

Produksi tetap diblokir sampai delapan gate terpenuhi:

### Gate 1. Researcher Adjudication

DEC-01–DEC-18 selesai dan dibekukan.

### Gate 2. Ontology Contract

V2.1 atau V3 disetujui dan versioned.

### Gate 3. Generalized Validator

Validator umum dan regression suite lulus.

### Gate 4. Artifact Migration

Lima kasus dimigrasikan secara nonproduksi dan divalidasi.

### Gate 5. Multi-Case Prototype

Technical, semantic, accessibility, responsive, dan visual review lulus.

### Gate 6. Legacy Compatibility

Tidak ada regression pada layer lama.

### Gate 7. Deployment and Rollback

Deployment plan, rollback, observability, dan failure recovery disetujui.

### Gate 8. Public Content Review

Public labels, summaries, sources, caveats, dan legal/licensing review lulus.

---

## 19. Roadmap

### Phase 0. Researcher Adjudication

Output:

- DEC-01–DEC-18 finalized;
- package choice;
- decision commit.

### Phase 1. Ontology Contract

Output:

- V2.1 or V3 draft;
- schema;
- vocabularies;
- changelog;
- formal review.

### Phase 2. Validation Infrastructure

Output:

- generalized validator;
- JSON schema;
- regression fixtures;
- machine-readable reports.

### Phase 3. Nonproduction Migration

Output:

- migrated Painan, Natal, Koto Tangah, Tiku, Sillida artifacts;
- transformation manifests;
- revalidation report.

### Phase 4. Multi-Case Prototype

Output:

- local prototype;
- visual review;
- accessibility review;
- semantic comprehension test.

### Phase 5. Research Layer Pilot

Output:

- opt-in Atlas research route;
- static or read-only data bundle;
- no production database mutation;
- limited internal or invited access.

### Phase 6. Graph Projection Pilot

Output:

- non-authoritative graph projection;
- reproducible rebuild;
- query experiments;
- no public factual edge promotion.

### Phase 7. Production Candidate

Output:

- API contract;
- database design if needed;
- migration plan;
- observability;
- rollback drill;
- public content review.

### Phase 8. Controlled Rollout

Output:

- feature flag;
- canary release;
- monitoring;
- researcher sign-off;
- post-deploy validation.

---

## 20. Prioritas Backlog

### P0

- resolve five blocking decisions;
- select Minimal/Balanced/Expanded;
- complete DEC-01–DEC-18;
- freeze decision ledger.

### P1

- create ontology contract next version;
- create JSON Schema;
- define common IDs;
- define identity and mandate model;
- define rights model.

### P2

- institutional observations;
- resistance target;
- constrained agency;
- dispute settlement;
- generalized validator.

### P3

- migrate V1–V4;
- revalidation;
- multi-case prototype.

### P4

- Atlas Research Layer;
- public-copy review;
- legacy compatibility.

### P5

- Graphify pilot;
- production database/API evaluation;
- controlled rollout.

---

## 21. Success Metrics

### Scientific integrity

- 100% public relations source-linked;
- 0 automatic sovereignty inference from treaty;
- 0 automatic actor merge without identity review;
- 0 resistance edge;
- 0 patron-client factual edge without future explicit approval;
- 100% uncertainty fields preserved through presentation.

### Data quality

- 100% artifacts pass generalized validator;
- 0 orphan endpoints;
- 0 duplicate IDs;
- 0 malformed controlled values;
- 100% transformation manifests reproducible.

### Product comprehension

In researcher testing, at least 90% of tasks correctly distinguish:

- claim versus control;
- location versus actor;
- command versus consent;
- treaty versus sovereignty;
- explicit versus inferred;
- source versus theory.

### Accessibility

- keyboard critical-path completion 100%;
- 0 horizontal overflow at target mobile widths;
- no color-only critical distinction;
- all evidence drawers accessible.

### Operations

- zero unintended production mutations;
- 100% deploys include rollback plan;
- all artifacts and schemas checksum-recorded;
- all releases traceable to researcher decision commits.

---

## 22. Risks dan Mitigasi

### R1. Ontology overgrowth

Mitigasi:

- favor structured objects over many narrowly named edges;
- require supporting failures;
- grouped changeset review.

### R2. False precision

Mitigasi:

- uncertainty fields;
- `CANNOT_DETERMINE` support;
- explicit non-identity;
- source label retention.

### R3. Theory becomes fact

Mitigasi:

- research annotations separated;
- Level 3 display;
- public-copy review.

### R4. Actor homogenization

Mitigasi:

- identity continuity model;
- mandate scope;
- merge approval gate.

### R5. Graph authority inversion

Mitigasi:

- graph as disposable projection;
- canonical reviewed artifacts remain source of truth.

### R6. Migration drift

Mitigasi:

- immutable source artifacts;
- new migrated files;
- transformation manifests;
- before/after checksums.

### R7. Public misunderstanding

Mitigasi:

- progressive disclosure;
- plain-language caveats;
- comprehension testing;
- no theory labels by default.

### R8. Scope expansion

Mitigasi:

- phase gates;
- non-goals;
- explicit authorization per milestone.

---

## 23. Dependencies

- adjudication DEC-01–DEC-18;
- approved next ontology version;
- research engineer availability;
- local validators and artifacts;
- source passage locators;
- UI research prototype infrastructure;
- future legal/licensing review for external source data;
- deployment operator and rollback access.

---

## 24. Open Decisions

Blocking:

```text
DEC-01
DEC-04
DEC-09
DEC-10
DEC-14
```

All 18 decisions must be filled before ontology construction begins.

Additional PRD decisions:

1. Balanced package approval;
2. next version name V2.1 or V3;
3. structured objects versus relation types;
4. researcher-only duration;
5. production storage strategy;
6. internal pilot audience;
7. Graphify pilot threshold;
8. public evidence-detail level;
9. licensing policy for source snippets;
10. deprecation policy for legacy dominion layer.

---

## 25. Acceptance Criteria per Major Milestone

### Researcher Decision Milestone

- 18 decisions explicit;
- no contradictory decisions;
- package selected;
- Git commit and server sync complete.

### Ontology Milestone

- approved contract;
- schema parseable;
- vocabularies documented;
- no migration or production change.

### Validator Milestone

- full regression suite pass;
- negative controls work;
- local-only policy preserved;
- machine-readable results.

### Migration Milestone

- five migrated artifacts;
- legacy artifacts unchanged;
- all approved failures resolved or documented;
- no new unsupported claims.

### Prototype Milestone

- multi-case views complete;
- visual and accessibility reviews pass;
- semantic comprehension reviewed;
- no production integration.

### Production Candidate Milestone

- all 8 gates pass;
- rollback drill passes;
- public copy approved;
- feature flag ready;
- deployment explicitly authorized.

---

## 26. Rollback Strategy

Every stage must support rollback:

```text
Ontology:
return to prior frozen contract

Artifacts:
retain old files and switch artifact manifest

Validator:
pin previous validator version

Prototype:
remove feature flag or route

Graph:
rebuild from prior canonical artifacts

Production:
rollback commit and restore previous static bundle/API version
```

No destructive migration is authorized during research phases.

---

## 27. Observability

For future research layer:

- artifact version loaded;
- ontology version;
- validator version;
- source count;
- actor count;
- relation count;
- warnings;
- unresolved identity count;
- missing-source count;
- client-side render errors;
- route health;
- no personal analytics required for initial pilot.

---

## 28. Documentation Requirements

Required documentation:

- ontology contract;
- field dictionary;
- controlled vocabularies;
- source/evidence contract;
- migration guide;
- validator guide;
- researcher adjudication guide;
- public interpretation guide;
- deployment and rollback checklist;
- citation and licensing guide.

---

## 29. Immediate Next Action

PRD does not authorize implementation.

Immediate next step:

```text
RESEARCHER ADJUDICATION OF DEC-01–DEC-18
```

Recommended order:

```text
1. Choose BALANCED package
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

---

## 30. Final Product Gate

This PRD is approved for planning when:

- scope is accepted;
- Balanced package is accepted or replaced;
- implementation remains blocked;
- researcher adjudication is explicitly identified as next gate.

Status options:

```text
PRD_READY_FOR_RESEARCHER_REVIEW
PRD_REQUIRES_REVISION
PRD_APPROVED_FOR_PLANNING
PRD_APPROVED_FOR_IMPLEMENTATION
```

Current recommended status:

```text
PRD_READY_FOR_RESEARCHER_REVIEW
```

---

## 31. Hard Boundaries

Until adjudication is complete:

- do not edit Draft V2;
- do not create Draft V2.1 or V3;
- do not implement schema;
- do not implement generalized validator;
- do not migrate artifacts;
- do not build the multi-case prototype;
- do not integrate with Atlas;
- do not Graphify;
- do not create database migrations;
- do not deploy.
