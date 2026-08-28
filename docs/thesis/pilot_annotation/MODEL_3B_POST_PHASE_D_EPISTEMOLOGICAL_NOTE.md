# MODEL 3B — POST-PHASE-D EPISTEMOLOGICAL NOTE: COLONIAL CATEGORIES, RESISTANCE, AND INTERPRETIVE METHOD

> **RESEARCH INTERPRETATION AND SOURCE-CRITICISM METHOD NOTE**
> **PHASE D CONDITIONAL CLUSTERING COMPLETE — NOT REOPENED HERE**
> **NO AUTOMATIC ACCEPTANCE OF VOC CATEGORIES**
> **NO AUTOMATIC RESISTANCE LABELING**
> **NO HAWKES, MODEL V2, GRAPHIFY, OR ATLAS CHANGE AUTHORIZED BY THIS NOTE**
> **RESEARCHER REVIEW REQUIRED**

---

## 1. Purpose

This note fixes the interpretive method that governs every future episode-level analysis of the 141-event corpus, before any such analysis is performed. It exists to prevent two errors that are equally indefensible and equally easy to fall into once a quantitative phase (Phase D) has closed:

1. treating VOC political categories — *rebellie*, *oproer*, *ongehoorzaamheid*, *afval*, and the like — as neutral descriptions of what local actors actually did;
2. replacing every VOC category, reflexively, with a resistance or anti-colonial label, as if rejecting the colonial source's framing were itself sufficient grounds for a different, equally strong claim.

Both errors substitute one layer of analysis for another. This note's central discipline is to keep four layers permanently distinct:

```text
colonial actor category      (what the VOC wrote and why)
historical action reconstruction  (what happened, reconstructed from all available evidence)
mechanism interpretation      (a working hypothesis about why it happened)
statistical modeling result   (what Phase D's aggregate temporal test found)
```

No layer is a substitute for any other layer. A future interpretive ledger entry that skips from a VOC label directly to a mechanism category, or from a Phase D statistic directly to a claim about resistance, has violated this note regardless of which specific label was chosen.

## 2. Status of Model 3 and Model 3B-CD V1

Frozen, unchanged by this note:

```text
MODEL_3:                        RETAINED_AS_POOLED_EXPLORATORY_BASELINE
MODEL_3B_CD_V1:                 CLOSED_AFTER_FAILED_RECOVERY_VALIDATION
PHASE_A_POSTMORTEM:             COMPLETE
PHASE_B_PROVENANCE_AUDIT:       COMPLETE, 141/141 EVENTS
PHASE_C_LEAVE_SOURCE_OUT:       COMPLETE
PARENT_EPISODE_REVIEW:          COMPLETE
EPISODE_LEVEL_SENSITIVITY:      PARTIALLY_FEASIBLE
PHASE_D_CONDITIONAL_CLUSTERING: COMPLETE
PHASE_D_PRIMARY_RESULT:         RESIDUAL_CLUSTERING_NOT_SUPPORTED IN ALL 9 ARMS
MODEL_V2:                       NOT_AUTHORIZED
REAL_DATA_HAWKES_FITTING:       NOT_AUTHORIZED
HISTORICAL_MECHANISM_INFERENCE: PROCESS_TRACING_ONLY
```

This note does not reopen, re-audit, or re-run any of the above. Every episode-level interpretation that follows this note builds on these statuses as given.

## 3. Phase D's Primary Result (reported as-is, not reinterpreted)

Phase D ran 9 arms × 10,000 simulations = 90,000 total simulated draws:

```text
FULL event-level, FULL episode-earliest, FULL episode-latest,
LSO-A event-level, LSO-A episode-earliest, LSO-A episode-latest,
LSO-B event-level, LSO-B episode-earliest, LSO-B episode-latest
```

using the pre-registered primary statistic — number of unordered event pairs within 90 days — against a density-only null conditioned on each arm's own observed event count.

```text
Result:                9/9 arms: RESIDUAL_CLUSTERING_NOT_SUPPORTED
Smallest raw p-value:  0.2486
Holm-adjusted p-values: 1.0000 (all 9 arms)
```

Observed-statistic change after episode collapse:

```text
FULL:            36 pairs -> 0 pairs
LSO-A and LSO-B: 5 pairs  -> 0 pairs
```

The Sas expedition (`EP-1693-SAS-EXPEDITION-AIRBANGIS-NIAS`, 11 members) alone contributes 17 of the 36 observed 90-day pairs in the full event-level series — 47.2% of all such pairs in the entire corpus.

A secondary, exploratory diagnostic at the 180-day window showed raw p-values of approximately 0.0006–0.0015 in the event-level arms. This diagnostic is **not** part of the pre-registered primary decision (plan §11/§13) and is treated in this note strictly as an `EXPLORATORY_WINDOW_SENSITIVITY_SIGNAL` (§11 below) — never as a second, competing primary result.

## 4. Meaning and Limits of `RESIDUAL_CLUSTERING_NOT_SUPPORTED`

**The only statistically licensed conclusion is:**

> After accounting for CD documentation density through a density-only null and after checking for parent-episode concentration, no excess temporal clustering was found at the pre-registered 90-day primary window across nine tested specifications.

**Prohibited conclusions — none of the following follow from this result, and none may be asserted by any future document in this project citing Phase D:**

```text
resistance never occurred
the VOC was correct to call all these actions rebellion
the west coast population was fully submissive
events are historically unconnected to one another
documentation density explains all of history's dynamics
the 180-day result proves contagion
Model 3 is causally correct
```

The governing epistemic relation, stated once and applied everywhere downstream:

```text
RESIDUAL_CLUSTERING_NOT_SUPPORTED   DOES_NOT_IMPLY   RESISTANCE_NOT_PRESENT
```

`RESIDUAL_CLUSTERING_NOT_SUPPORTED` is a statement about the *timing* of dated records relative to a specific null model. It says nothing about whether any individual action was, substantively, an act of resistance, a factional dispute, a commercial maneuver, or something else — that question belongs entirely to the interpretive layers in §5, not to Phase D.

## 5. VOC Categories as Actor Categories, Not Neutral Description

Every future interpretive entry must record, separately:

- **the colonial source category as written** — terms such as *rebellie*, *oproer*, *ongehoorzaamheid*, *trouweloosheid*, *afval*, *onrust*, *muiterij*, *verraad*, *roof*, *ongehoorzame onderdanen* — quoted or precisely located in the source, never paraphrased into a translation that already carries an interpretive judgment;
- **who wrote the document, to whom, and what it was trying to justify** — an expedition, a punishment, a monopoly claim, an assertion of jurisdiction, a replacement of a local official — before any claim is made about what the label "really" describes;
- **whether the vocabulary in use is a VOC category or a local category** — these are not the same source, and conflating them is exactly the error this note exists to prevent.

The governing principle:

```text
VOC label as written  !=  neutral historical description
```

A VOC label can function to: cast the VOC as a legitimate authority; define who counts as obedient or disobedient; convert a mutual, two-sided dispute into a one-sided violation; justify a military expedition; justify punishment or the replacement of a local elite; extend the meaning of an existing contract; legitimize a monopoly; recast a local negotiation as disloyalty; or obscure the VOC's own failure to meet its own obligations. **No such function may be asserted without the specific passage and context that supports it.** A future entry that classifies a VOC label as, e.g., "legitimizing a monopoly" must cite the passage that does this — the function is never inferred from the label word alone.

## 6. The Risk of Romanticizing Resistance

The equal and opposite error is treating rejection of a VOC label as proof of resistance:

```text
VOC label rejected  !=  resistance automatically proven
```

An action described by the VOC as rebellion may instead be, or also be: a conflict between local factions; a succession dispute; a commercial strategy; a shift of alliance; a personal conflict; the use of the VOC by one local party to remove a rival; a response to the VOC's own breach of contract; a defense of local rights; a rejection of a monopoly; or a combination of several of these at once. Before any `resistance_candidate` label is applied, both the actor and the mechanism must be independently verified — not assumed from the mere fact that VOC called the action disobedience.

### 6.1 Criteria supporting `resistance_candidate` (§8 of the governing instructions, reproduced)

Applied when some or all of the following evidence is present:

```text
1. rejection of an imposed monopoly or obligation
2. defense of nagari/regional/local authority or autonomy
3. a response to a VOC breach of an existing agreement
4. an effort to limit colonial intervention
5. collective action with a traceable political objective
6. construction of an alternative alliance against the VOC
7. a stated reason or declaration from the local actor
8. continuity between grievance, demand, and action
9. real cost or risk borne by the actor for refusing domination
10. evidence the action was not primarily directed at a local rival
```

Not every criterion must be satisfied, but the basis for whichever criteria *are* judged satisfied must be recorded explicitly, per criterion, in the interpretive ledger's `resistance_evidence` field.

### 6.2 Criteria weakening a single resistance label (§9, reproduced)

Flag as a limitation when: the conflict is primarily between local factions; the local party itself requested VOC intervention; an actor uses the VOC for internal advantage; the party that acted differs from the party that signed the relevant contract; the VOC has merged multiple distinct communities into one nominal actor; the event is administrative or purely documentary in character; the political target is unknown; no local reasoning is available; the report comes from the VOC alone with no independent stream; or later historiography has simply repeated the VOC's category uncritically. Any one of these present in an episode must be recorded in `resistance_counterevidence`, not silently omitted because it complicates a preferred reading.

## 7. Process Tracing as the Basis for Mechanism Claims

Mechanism interpretation is the **fourth** layer (§1) and is performed only after the first three layers — colonial category, author position, and action reconstruction — are already on record for a given episode. For every episode, the following fourteen questions (governing instructions §13) must be answered, or explicitly marked `CANNOT_DETERMINE`, before any mechanism category is assigned:

```text
1.  What were the initial conditions?
2.  What obligation was in force?
3.  Who claimed that obligation?
4.  What triggered the action?
5.  Who acted first, according to the sources?
6.  Is there evidence the VOC breached its own obligation first?
7.  Is there a local demand or grievance on record?
8.  What was the local actor's subsequent action?
9.  What was the VOC's response?
10. Did the VOC's response change the underlying power structure?
11. Did the category "rebellion" appear before or after the punishment was legitimized?
12. Is there any non-VOC account that changes the reading?
13. Does the episode better fit a dispute, a resistance action, a factional conflict, or a mixed mechanism?
14. What evidence is still missing?
```

Mechanism categories (§10 of the governing instructions) are used as **working hypotheses**, never as automatic facts, and are not mutually exclusive:

```text
RESISTANCE_CANDIDATE
CONTRACTUAL_DISPUTE
VOC_NONFULFILLMENT_RESPONSE
MONOPOLY_REJECTION
LOCAL_AUTONOMY_DEFENSE
FACTIONAL_CONFLICT
SUCCESSION_CONFLICT
COMMERCIAL_STRATEGY
ALLIANCE_SWITCHING
NEGOTIATION_TACTIC
COLONIAL_PUNITIVE_CLASSIFICATION
ADMINISTRATIVE_RECLASSIFICATION
RESOURCE_GOVERNANCE_CONFLICT
CANNOT_DETERMINE
```

No new category is introduced without explanation and researcher review.

## 8. Paternalism and Local Agency

`colonial_paternalism_candidate` is used when source language positions the VOC as a party that: knows what is good for a negeri or its people; has the right to direct local elites; has the right to choose or replace officials; justifies domination as protection; justifies intervention as the restoration of order; infantilizes local actors; or converts control into a claimed moral responsibility.

Guardrails, both directions: not every instance of protective language is paternalism, and identifying paternalism must never be used to erase local agency. Edward Said is not treated as primary evidence — postcolonial theory is a reading tool applied only *after* the archival language has been presented on its own terms, never a substitute for that language.

## 9. Patron-Client Relations versus Colonial Domination

Patron-client dynamics and colonial paternalism are analytically distinct and must not be collapsed into each other. Each episode is tested for the presence of: a personal relationship; an exchange of benefit; protection; loyalty; brokerage; reciprocal dependency; local capacity to negotiate; and local actors' own use of the VOC for their own ends. Not every VOC–local relationship in the corpus is a patron-client relationship by default. Local actors are recognized throughout this method as capable of: negotiating; proposing a candidate; refusing; switching alliance; using the VOC instrumentally; pursuing political advantage; defending their own room for maneuver; and, in some cases, participating in domination over other local groups — local agency is not assumed to be uniformly benign any more than it is assumed to be absent.

## 10. "Iyokan Nan di Urang, Laluan Nan di Awak" as a Hermeneutic Hypothesis

This Minangkabau expression (roughly: outward assent to another's terms, while one's own path is nonetheless followed) is used in this project strictly as a **hermeneutic hypothesis**, tested episode by episode — never as a statistical law, a blanket conclusion applied to every episode, or automatic proof of resistance. The questions it licenses, per episode:

```text
- is there a gap between formal agreement and actual practice?
- is the actor who acted the same as the actor who made the formal promise?
- did the community treated as bound by the VOC actually grant that mandate?
- did the VOC and the local party understand the agreement the same way?
- did formal acceptance nonetheless leave room for autonomous practice?
```

The hypothesis is sustained for a given episode only if the actor evidence and action sequence support it — it is never carried forward from one episode to the next as an assumed default.

## 11. The 180-Day Signal as an Exploratory Diagnostic

Recorded, permanently, as:

```text
EXPLORATORY_WINDOW_SENSITIVITY_SIGNAL
```

Governing rules, all absolute:

- it does not change the pre-registered 90-day primary decision, in any arm;
- it is never described as "significant" in any document produced after Phase D's preregistration closed;
- it is never used to construct a contagion narrative;
- it is never used, by itself, as a reason to build Model V2;
- if it is ever tested again as a primary question, that requires a new study with its own historical rationale and its own preregistration — not a re-analysis of Phase D's existing simulations under a relabeled threshold.

## 12. Implications for the Atlas and Public Writing

No public-facing surface (the Atlas map, its popups, its provenance badges, its modeling pages, or any thesis-facing prose derived from this project) may display or assert a "resistance" badge or label automatically derived from `event_type`, from a VOC source category, or from Phase D's statistical result. Any future resistance-adjacent claim reaching a public surface must trace to a specific, researcher-reviewed episode-level interpretation produced under this note's method — not to an automated inference from any single field in the production schema. This note does not itself authorize any Atlas change; per §27 of the governing instructions, Graphify and Atlas remain untouched until the method note and at least the priority episode interpretations are reviewed and claim boundaries are researcher-approved.

## 13. Claims That Are Permitted (governing instructions §23, reproduced in full)

```text
The VOC classified certain actions as rebellion or disloyalty.

That category reflects the VOC's own position and interests and requires source criticism.

Some episodes may be read as resistance candidates if supported by evidence of local goals,
grievances, and actions.

Phase D did not find 90-day residual clustering beyond the density-only null.

Event-level concentration is substantially influenced by parent episodes, especially the
Sas expedition.

Mechanism interpretation still requires process tracing.
```

## 14. Claims That Are Prohibited (governing instructions §24, reproduced in full)

```text
Every VOC-labeled rebellion is resistance.

Resistance never happened because residual clustering is not supported.

The model proves the population was submissive.

The model proves rebellion spread.

The model proves contagion at 180 days.

The VOC was a neutral observer.

Local parties were always passive victims.

Local parties always acted as one unified body.

Absence of local sources means the VOC category is correct.
```

## 15. Next Research Agenda

Once this method note, its working-CSV schema, and the main audit report's structure (this session's three deliverables) are reviewed and approved by the researcher, the next steps — **not started by this note** — are:

1. Batch I1 (Barus) as the first populated episode entry, per the governing instructions' priority list and explicit batching rule (one episode or episode group per turn, no automatic continuation).
2. Subsequent batches I2–I10 in the order already fixed by the governing instructions (Indrapura; Pariaman; Sillida/Salido; Padang succession and office control; Sas expedition; the 1656–1657 war; Batang Capas and the EIC/VOC confrontation; Natal and the Anglo-French-VOC transfer; the Koto Tangah destruction cycle and related episodes) — a priority order, not a permanent restriction on later additions.
3. A Graphify update and any Atlas-facing change, both explicitly deferred until the method note and at least the priority episodes have been reviewed and claim boundaries approved.

---

**This note is a method specification. It contains no episode-level findings, no resistance determinations, and no mechanism classifications for any specific historical event — those begin only with Batch I1, after researcher review of this note.**
