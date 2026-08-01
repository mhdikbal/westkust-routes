# Location Ontology

## Hierarchical model

- `L-SALIDO` **Sillidase Goutmijne**: Tambang Emas Sillida [mine_enclave]
  - `L-BOVEN-PAGGER` **Boven-Pagger**: Pagger atas [surface_zone]
    - `L-ASSAY-LAB` **Assaijeurs locatie boven in de mijn**: Laboratorium assay bagian atas [facility]
    - `L-SCHEIJDEBANCK` **Scheijdebanck**: Tempat pemisahan bijih [facility]
  - `L-BENEDEN-PAGGER` **Beneden-Pagger**: Pagger bawah [surface_zone]
    - `L-STAMPWERK` **Stampwerk**: Instalasi penumbukan [facility]
  - `L-OUDE-MIJNE` **Oude Mijne**: Tambang lama [underground]
    - `L-OUDE-STOLLE` **Oude Stolle**: Lorong lama [underground]
  - `L-ZUIJDER-SCHACHT` **Zuijder-Schacht**: Sumuran selatan [underground]
  - `L-SUIJDERWERCK` **Suijderwerck**: Pekerjaan tambang selatan [underground]
  - `L-PRINCESTOLLE` **Princestolle**: Lorong Princestolle [underground]
  - `L-ZZW-DAGGANG` **Z:Z:W: daggang**: Lorong berarah ZZW [underground]
  - `L-ORTEN` **Orten**: Muka-muka penggalian [underground_feature]
  - `L-MALEIJTS-ORT` **Maleijtsen Ort**: Muka penggalian Melayu [underground_feature]
  - `L-SMITSWINCKEL` **Smitswinckel**: Bengkel pandai besi [facility]
  - `L-SIECKENHUIJS` **Sieckenhuijs**: Rumah sakit [facility]
  - `L-PAERDESTALL` **Paerdestall**: Kandang kuda [facility]
  - `L-PACKHUIJS` **Packhuijs**: Gudang [facility]
  - `L-OPPERHOOFTSWONING` **Opperhooftswoning**: Kediaman kepala [facility]
- `L-POULO-CHINCO` **Poulo Chinco**: Pulo Chinco [regional_site]
- `L-PADANG` **Padang**: Padang [regional_site]
- `L-BATAVIA` **Batavia**: Batavia [regional_site]
- `L-MADAGASCAR` **Madagascar**: Madagaskar [external_origin]

## Relation types

```text
contains
associated_with
approaches_or_audibly_connected
regional_route
shipping_route
coerced_mobility_route
topological_relation_unknown
```

## Spatial confidence

A containment relationship is not a coordinate. Exact 3D geometry must remain unknown until measurements or maps justify it.

## Distance policy

Historical units such as `lachter`, `vadem`, and `duijmen` remain in original units until the applicable measurement standard is independently established.
