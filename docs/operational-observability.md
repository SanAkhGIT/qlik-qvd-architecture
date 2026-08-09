# Operational Observability

The lab separates **data processing** from **reload observability**. A reload should leave an operational trail that answers four questions:

1. Which run was this?
2. When did it start and finish?
3. Which process produced the result?
4. Did the process pass, fail, or stop at a data-quality gate?

## Audit contract

`ReloadAudit.qvd` is designed around these fields:

| Field | Purpose |
|---|---|
| `RunID` | Unique identifier for one reload execution |
| `StartedUTC` | Reload start timestamp |
| `CompletedUTC` | Completion timestamp |
| `Process` | Reload component/process name |
| `Status` | STARTED, PASS, FAIL, or BLOCKED |
| `Message` | Human-readable execution detail |
| `RowCount` | Optional process output row count |
| `DQStatus` | Optional data-quality outcome |

## Design intent

The audit QVD is a monitoring interface, not a substitute for Qlik's native reload history. In a larger implementation, each layer can append its own process record using the same `RunID`.

A useful operational flow is:

```text
START
  |
  v
RAW -> TRANSFORM -> DQ GATE -> SEMANTIC -> COMPLETE
  |                   |
  +-------------------+----> AUDIT QVD
```

If the DQ gate blocks publication, the audit record should preserve the run ID and failure reason so an operator can distinguish **pipeline failure** from **successful completion with rejected data**.

## Current scope and limitation

`qlik/07_reload_audit.qvs` demonstrates creation of the operational audit record. It does not yet wrap every individual layer or automatically capture every possible Qlik engine error. That requires a fuller orchestration pattern and, in production, usually integration with QMC/native monitoring and external operational tooling.
