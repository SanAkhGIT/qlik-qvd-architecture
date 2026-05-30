# Qlik Script Execution

## First build

Run the scripts in this order:

1. `01_raw.qvs` — source CSV to Raw QVDs.
2. `02_transform.qvs` — cleanse/standardise Raw QVDs into reusable Transform QVDs.
3. `05_data_quality.qvs` — validate the Transform layer and publish audit metrics.
4. `03_semantic.qvs` — publish the application-ready fact, dimensions and canonical calendar.

`00_master_reload.qvs` orchestrates steps 1–4 and is the preferred end-to-end demonstration.

## Incremental mode

For later order reloads, `04_incremental_orders.qvs` reads the latest persisted `ModifiedTimestamp`, applies the configured look-back window, reloads the affected source slice and deduplicates by `OrderID`.

Do not treat this CSV implementation as database CDC. A production source should push the incremental predicate down to the source system and define update/delete semantics.

## Application mode

`06_app_load.qvs` is intentionally separate from ETL. It loads only semantic QVDs into a Qlik Sense application, so the front-end app has no dependency on source CSVs or transformation logic.

## Connection setup

The scripts use the Qlik Sense folder connection `QlikQVDArchitecture`. Point that connection at the repository root (or an exported project directory), then adjust `config/environment.qvs` if your deployment uses different connection names.

The repository contains no credentials or environment-specific secrets.
