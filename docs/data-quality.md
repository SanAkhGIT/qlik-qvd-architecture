# Data Quality Controls

The demo validates the transformed order data before semantic publication.

## Checks

- Null or blank business keys
- Duplicate `OrderID` values
- Invalid dates
- Missing customer/product identifiers
- Non-positive quantities
- Negative sales amounts
- Invalid product prices

The Qlik script writes audit metrics to QVDs and uses a fail-fast gate for order-key integrity.

## Production extension

A production implementation should add referential-integrity checks against dimensions, threshold-based alerting, reload audit history, rejected-record quarantine, and operational notifications. Data-quality thresholds should be agreed with the business rather than silently hard-coded.
