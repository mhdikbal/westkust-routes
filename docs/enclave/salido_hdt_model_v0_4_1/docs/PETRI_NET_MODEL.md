# Timed Coloured Petri Net for Mine Production

## Formal model

```text
CPN = (P, T, A, Sigma, C, G, E, I, M0)
```

- `P`: places
- `T`: transitions
- `A`: arcs
- `Sigma`: token types
- `C`: place colour sets
- `G`: guards
- `E`: arc expressions
- `I`: initialization
- `M0`: initial marking

## Token types

### HumanToken

```text
human_id, group_count, status, role, skill, health,
location, schicht, coercion_status, evidence_confidence
```

### ToolToken

```text
tool_id, tool_type, condition, location, available
```

### OreToken

```text
batch_id, source_location, grade_class, gross_weight_lb,
net_weight_lb, date, assay_status
```

### EvidenceToken

```text
document_id, paragraph_id, evidence_status, confidence
```

## Production places

```text
Workers_Available
Workers_Assigned
Ort_Inspected
Drills_Available
Rock_Drilled
Charge_Prepared
Blast_Ready
Blast_Fired
Ventilation_Wait
Ort_Safe
Broken_Rock
Ore_Transported
Ore_Sorted
First_Class_Ore
Second_Class_Ore
Waste_Rock
Stampwerk_Queue
Ore_Crushed
Scheijdebanck_Queue
Ore_Washed
Schlam_Collected
Assay_Sample_Prepared
Hoffman_Assay
Vogel_Assay
Assay_Reconciled
Ore_Barrelled
Warehouse
Shipment_Ready
```

## Transitions

```text
Assign_Schicht
Inspect_Ort
Drill_Rock
Prepare_Charge
Fire_Schot
Wait_For_Fumes
Inspect_After_Blast
Remove_Broken_Rock
Transport_To_Surface
Sort_Ore
Crush_Ore
Wash_Ore
Collect_Schlam
Prepare_Assay_Sample
Assay_By_Hoffman
Assay_By_Vogel
Compare_Assays
Calculate_Monetary_Value
Fill_Barrel
Move_To_Warehouse
Load_Ship
```

## Failure and interruption places

```text
Water_Ingress
Rotten_Timber
Worker_Illness
Tool_Unserviceable
Old_Malay_Workings
Low_Grade_Ore
```

## Example guards

### Drill

```text
worker has drilling skill
AND serviceable drill is available
AND lamp is available
AND Ort is safe
```

### Blast

```text
hole is complete
AND powder is available
AND workers have cleared the face
```

### Assay

```text
sample is prepared
AND assayer is present
AND assay oven is serviceable
AND weights are available
```

## Calibration targets

- weekly `schoten`;
- weekly ore weights;
- first- and second-class ore;
- dates of completed timbering;
- water events;
- assay completion;
- barrel and shipment totals.

The Petri net produces possible process histories. It does not prove that an unrecorded activity occurred.
