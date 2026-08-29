# Qlik Deployment & Environment Promotion

This project treats Git as the source of truth for reload scripts, configuration templates and documentation. Qlik environment-specific values are injected through connection/configuration rather than hard-coded into business logic.

## Promotion model

```text
Developer change
      |
      v
Git branch / Pull Request
      |
      v
CI validation
      |
      v
DEV  -- validate reload + data quality
      |
      v
TEST -- controlled data + functional validation
      |
      v
PROD -- approved deployment + scheduled reload
```

## What belongs where

| Concern | Git | Qlik/QMC environment |
|---|---|---|
| Qlik load scripts | Yes | Deployed artifact |
| Python validation code | Yes | CI/runtime as required |
| Sample data | Yes | DEV/test only |
| Connection credentials | No | Managed securely in environment |
| `lib://` connection names | Template/config | Created per environment |
| Reload schedule | Documentation/config intent | QMC task |
| Production secrets | No | Secret/credential management |

## Reload dependency design

A production task chain should preserve the dependency order:

1. Raw extraction
2. Transform QVD creation
3. Incremental processing where applicable
4. Data-quality gate
5. Semantic QVD publication
6. Application reload
7. Operational audit/notification

A downstream task must not run when its upstream dependency fails or is blocked by the DQ gate.

## Environment strategy

Use the same logical script structure across environments. Change only environment-specific values such as connection names, file locations and scheduling.

Example:

```text
DEV  -> lib://QlikQVDArchitecture_DEV/...
TEST -> lib://QlikQVDArchitecture_TEST/...
PROD -> lib://QlikQVDArchitecture_PROD/...
```

The repository's `environment.qvs` is therefore a configuration boundary, not a place for credentials.

## Rollback

A safe rollback should restore the last known-good application/script artifact and prevent a failed semantic publication from being consumed by the application.

For QVD-backed systems, rollback planning should consider both:

- script/application version
- persisted QVD state

Simply reverting a script in Git does **not** automatically revert already-persisted QVDs. Production rollback therefore needs versioned backups/snapshots or a reproducible rebuild path.

## Failure handling

Expected failure classes include:

- source connection failure
- malformed source extract
- QVD write/read failure
- incremental watermark problem
- DQ gate failure
- application reload failure

The operational audit should record the run ID, process, status and message. QMC/native reload history remains the authoritative execution history for actual Qlik reloads.

## Production boundary

This repository documents the deployment design; it does not claim to have executed DEV/TEST/PROD QMC tasks. Actual task configuration, credentials, connections and reload timings belong to the target Qlik environment.
