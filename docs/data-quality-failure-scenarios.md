# Data Quality Failure Scenarios

The Qlik data-quality layer is a **reload gate**, not just a dashboard metric.

## Rules

| Rule | Failure condition | Why it matters |
|---|---|---|
| Order uniqueness | `TotalRows <> DistinctOrderIDs` | Prevents duplicate business keys from reaching the semantic layer |
| Order key completeness | Blank/null `OrderID` | A fact record without a business key cannot be reliably reconciled |
| Customer referential integrity | Orphan `CustomerID` | Prevents unmatched fact-to-dimension relationships |
| Product referential integrity | Orphan `ProductID` | Prevents unmatched fact-to-dimension relationships |
| Date validity | Null `OrderDate` | Protects calendar associations and time-based analysis |
| Quantity validity | `Quantity <= 0` | Prevents invalid transactional measures |
| Sales validity | `SalesAmount < 0` | Prevents invalid sales measures unless negative transactions are explicitly modelled |

## Gate behavior

The script calculates these metrics before semantic publication. If an Orders rule fails, it emits a failure trace and exits the reload when `vDQFailOnError = 1`.

This makes data quality an operational control: **bad data should stop publication rather than silently produce a misleading dashboard**.

## Important limitation

The repository contains static tests for the Qlik script because a Qlik reload engine is not available in CI. These tests verify that the documented rules and failure controls remain present; they do **not** claim that a Qlik reload has executed successfully.

A production implementation should also define explicit handling for legitimate negative transactions such as returns/refunds rather than treating every negative sales value as invalid.
