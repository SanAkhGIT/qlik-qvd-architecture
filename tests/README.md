# Validation Test Plan

Before treating the lab as complete, verify these scenarios in Qlik Sense:

1. First load creates all three layer QVDs.
2. Reload with no source changes produces zero new incremental rows.
3. Add a new order and confirm only the new order is processed.
4. Modify an existing order and confirm the latest version wins after deduplication.
5. Introduce a blank OrderID and confirm the data-quality gate fails.
6. Introduce a negative quantity and confirm the transform rejects the row.
7. Remove a dimension key and verify referential-integrity checks are added before production use.
8. Confirm the semantic model has no synthetic keys or circular references.
