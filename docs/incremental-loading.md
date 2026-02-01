# Incremental Loading

## Pattern

The example uses `ModifiedTimestamp` as the change-detection field.

```text
Existing transform QVD
        │
        ├── MAX(ModifiedTimestamp)
        ▼
Source extract
        │
        ├── WHERE ModifiedTimestamp > last processed value
        ▼
New/changed records
        │
        ▼
Deduplicate by OrderID
        │
        ▼
Overwrite transform QVD
```

## Why QVD incremental loading

Reading a persisted QVD is substantially cheaper than repeatedly querying a source system for the full history. As volume grows, the pattern can reduce source load and reload time.

## Important production considerations

The demo is deliberately simple. A production implementation should also define:

1. A reliable source-side change timestamp or CDC mechanism.
2. A look-back window if source timestamps can arrive late.
3. Update/delete handling when the source supports corrections.
4. Duplicate and idempotency rules.
5. Audit logging: start/end time, source rows, inserted rows, rejected rows and errors.
6. Recovery behaviour so a failed reload does not corrupt the last good QVD.
7. Retention and archival strategy for historical QVDs.

Never treat `WHERE ModifiedTimestamp > last_timestamp` as a universal CDC solution. It is a demonstration pattern, not a substitute for source-system change semantics.
