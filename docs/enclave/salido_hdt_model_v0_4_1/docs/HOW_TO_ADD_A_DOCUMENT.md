# How to Add a New Document

## 1. Register the document

Add one row to `01_documents.csv` with repository, access, inventory, date, title, and document type.

## 2. Extract source passages

Append paragraphs or lines to `00_source_passages.csv`. Preserve source order and keep blank or damaged regions documented.

## 3. Identify document regions

Classify each region as:

```text
main_text
marginalia
heading
address
receipt_note
signature
table
calculation
inventory_list
page_number
unknown
```

## 4. Extract entities

Add people, roles, locations, groups, and name variants without overwriting source forms.

## 5. Extract events and quantities

Create operation, assay, inventory, movement, health, or document events. Preserve original units.

## 6. Create claims

Every claim requires a source quotation and evidence status.

## 7. Validate

Run:

- identifier uniqueness;
- foreign-key checks;
- subtotal checks;
- date checks;
- provenance checks;
- unresolved-reading report.

## 8. Review

No record becomes `verified` solely because it was extracted automatically.
