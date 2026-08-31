# G0 — Source Gap Report

**Status:** GAP INVENTORY ONLY, NOT ADJUDICATION. No gap listed below is filled by this document. No historical data is entered. No historical claim is made about a source's existence or non-existence — each gap below is stated only in terms of what has and has not been located in, or documented within, this repository this turn.

**Allowed gap-status tokens (exact):**
```text
LOCAL_FILE_MISSING
BIBLIOGRAPHIC_REFERENCE_ONLY
PRIMARY_SOURCE_NOT_LOCATED
SOURCE_EDITION_REQUIRES_REVIEW
INDEXING_INCOMPLETE
COVERAGE_INSUFFICIENT
EIC_SIDE_COVERAGE_INSUFFICIENT
REQUIRES_SOURCE_AUDIT
```

---

## 1. Veevers (2021) — `BIBLIOGRAPHIC_REFERENCE_ONLY`

The audited plan cites, as the key secondary source for the Indrapura–EIC comparison case (§4.1, §19):

> David Veevers, "Building borders in a borderless land: English colonialism and the Alam Minangkabau of Sumatra, 1680–1730," *Journal of the British Academy* 9(s4), 58–89, DOI: 10.5871/jba/009s4.058.

**Status: `BIBLIOGRAPHIC_REFERENCE_ONLY`.** This is not "Veevers is absent" as a historical claim — a complete bibliographic reference (title, author, journal, volume, DOI) already exists, carried verbatim in the audited plan. What is missing, specifically, is: (a) a local repository copy of the article, and (b) any audit of its content against this repository's other sources. Both are distinct facts, and neither implies the source itself does not exist or is unreliable.

## 2. EIC Fort York / Batang Capas 1686 — `LOCAL_FILE_MISSING`

Prior session work (recorded only in this project's auto-memory, `project_eic_fort_york_batang_capas`) reports triangulating a Batang Capas 1686 episode across Vogel, `CD3`, and EIC Fort York records, and references a commit `6b6fba3`. This turn's repository search did not locate a standalone file containing the EIC-side Fort York material as a citable, re-checkable artifact.

**Status: `LOCAL_FILE_MISSING`.** This means: no corresponding local repository source file was located during the G0 audit. This states only that no local repository file was found this turn — it is not a claim that Fort York records "do not exist" or that the prior session's finding was incorrect. Before any claim citing "EIC Fort York records" can be entered into the claim-source ledger proposed alongside this report, the underlying transcription or extract needs to be located (if it already exists under a different filename or commit not surfaced by this turn's search) or re-extracted and committed as its own artifact.

## 3. `docs/cd/CD1.pdf`–`CD6.pdf` — `INDEXING_INCOMPLETE`

Six PDF volumes exist at `docs/cd/CD1.pdf` through `docs/cd/CD6.pdf`. Only `CD4` is currently tied to a specific topic anywhere in the repository (cited in `INDERAPURA_EPISODE_DOSSIER_DRAFT.md` as a source for the 1665/1686/1716 Indrapura events, though `CD4`'s own bibliographic identity is itself unconfirmed — see `PS-06`/`IS-07` in the source-path inventories). No README, index, or manifest anywhere in the repository states what each of the six volumes covers by date range or topic.

**Status: `INDEXING_INCOMPLETE`.** All six files are present (`PATH_VERIFIED`); what is missing is a topic index, not the files themselves.

## 4. Indrapura-Side EIC Primary Material — `EIC_SIDE_COVERAGE_INSUFFICIENT`

The one existing populated dossier for this case (`INDERAPURA_EPISODE_DOSSIER_DRAFT.md`) cites only VOC-side material: Vogel (1690) and `CD4`. No EIC-originated primary document (correspondence, factory record, council minute) is confirmed present anywhere in the repository for the 1680–1730 Indrapura–EIC window.

**Status: `EIC_SIDE_COVERAGE_INSUFFICIENT`.** This is a coverage-balance gap specific to the comparison case's own framing (audited plan §4.2 asks whether EIC was accepted as an alternative partner, buyer, protector, or territorial claimant — a question that, as currently sourced, can only be answered from the VOC side).

## 5. 1662 Batangkapas Antecedent — `PRIMARY_SOURCE_NOT_LOCATED`

The audited plan's Phase G1 (§14) requires auditing the "1662 Batangkapas antecedent" as part of the Painan-case literature review. No source — primary or secondary, and no bibliographic reference at all — for this specific antecedent has been identified in the repository this turn (recorded as `PS-17`, `source_class = UNVERIFIED_REFERENCE`, `verification_status = UNVERIFIED` in the Painan source-path inventory, since this item lacks even a bibliographic citation, unlike Veevers).

**Status: `PRIMARY_SOURCE_NOT_LOCATED`.**

---

## 6. Summary Table

| Gap | Case | Status token | Distinguishing detail |
|---|---|---|---|
| Veevers (2021) | Indrapura–EIC | `BIBLIOGRAPHIC_REFERENCE_ONLY` | Full citation exists; no local copy; content unaudited |
| EIC Fort York / Batang Capas 1686 | Indrapura–EIC | `LOCAL_FILE_MISSING` | Referenced only in session memory; not a claim of non-existence |
| `CD1`–`CD6.pdf` volume-topic index | Both | `INDEXING_INCOMPLETE` | Files present; index absent |
| Indrapura EIC-side primary material | Indrapura–EIC | `EIC_SIDE_COVERAGE_INSUFFICIENT` | Only VOC-side sources currently confirmed |
| 1662 Batangkapas antecedent | Painan | `PRIMARY_SOURCE_NOT_LOCATED` | No bibliographic reference at all exists yet, unlike Veevers |

## 7. Confirmation

This document contains no historical data filling, no modeling result, no simulation output, and no implementation. Every gap listed above remains open; this is an inventory of what is missing, not an adjudication of what that absence means historically.
