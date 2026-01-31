# Data Modelling

## Target model

The semantic layer uses a star-style model:

```text
Customers ─────┐
               │ CustomerID
               ▼
            FactOrders ◄──── Products
               │               │
               └── OrderDate ──┘
                      │
                      ▼
              CanonicalCalendar
```

`FactOrders` is the transaction grain: **one row per OrderID**. Customers and Products are conformed dimensions. The calendar is keyed by `OrderDate`.

## Why this model

- Keeps the fact table narrow and reusable.
- Avoids unnecessary fact-to-fact joins.
- Makes associative exploration predictable.
- Keeps descriptive attributes in dimensions rather than duplicating them in the fact.
- Provides a single canonical date dimension for time analysis.

## Synthetic keys

The model intentionally uses explicit keys (`CustomerID`, `ProductID`, `OrderDate`). If unrelated tables acquire multiple common fields, isolate or rename fields instead of allowing accidental synthetic keys.

## Grain and KPI examples

At the order grain:

- Sales = `Sum(SalesAmount)`
- Orders = `Count(DISTINCT OrderID)`
- Units = `Sum(Quantity)`
- Average Order Value = `Sum(SalesAmount) / Count(DISTINCT OrderID)`

Keep reusable business definitions in the semantic/application layer rather than embedding presentation-specific logic in raw ingestion.
