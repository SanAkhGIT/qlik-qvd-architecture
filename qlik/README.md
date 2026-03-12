# Qlik Script Execution

Run the scripts in this order for the first build:

1. `01_raw.qvs` — source CSV to Raw QVDs.
2. `02_transform.qvs` — cleanse/standardise Raw QVDs into Transform QVDs.
3. `05_data_quality.qvs` — validate the Transform layer.
4. `03_semantic.qvs` — publish the application-ready model.

For later reloads, use `04_incremental_orders.qvs` for the order fact when timestamp-based incremental processing is appropriate.

The scripts expect the variables in `config/environment.qvs` to resolve to Qlik Sense data connections. Adjust that file to match the deployment environment.
