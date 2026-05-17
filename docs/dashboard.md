# Qlik Sense Dashboard Design

The semantic layer is designed to support a compact executive sales dashboard without embedding presentation logic into the QVD load layers.

## Sheet 1 — Executive Overview

### KPI objects

- **Net Sales:** `Sum(SalesAmount)`
- **Orders:** `Count(DISTINCT OrderID)`
- **Units:** `Sum(Quantity)`
- **Average Order Value:** `Sum(SalesAmount) / Count(DISTINCT OrderID)`
- **Average Discount:** `Avg(Discount)`

### Visuals

1. Monthly net sales trend using `CalendarMonthYear`.
2. Sales by region.
3. Sales by product category.
4. Top 10 products by sales.
5. Sales and order count by customer segment.

## Sheet 2 — Sales Analysis

Recommended dimensions:

- CalendarYear
- CalendarQuarter
- CalendarMonthYear
- Region
- Country
- Segment
- Category
- Subcategory
- ProductName

Recommended measures:

- `Sum(SalesAmount)`
- `Count(DISTINCT OrderID)`
- `Sum(Quantity)`
- `Avg(Discount)`
- `Sum(SalesAmount) / Count(DISTINCT OrderID)`

## Sheet 3 — Data Quality

Expose the audit QVD metrics:

- Total rows
- Distinct order IDs
- Null order IDs
- Missing customer IDs
- Missing product IDs
- Orphan customer references
- Orphan product references
- Invalid dates
- Invalid quantities
- Invalid sales amounts

A production dashboard should make failed quality gates visible rather than silently hiding bad records.

## Selection model

Use the canonical calendar for date selections. `OrderDate` is the intentional association between `FactOrders` and `CanonicalCalendar`.

Use dimension fields from `Customers` and `Products` rather than duplicating those attributes into the fact table.

## UX guidance

- Keep the overview to 5–7 primary visuals.
- Provide clear current-selection indicators.
- Avoid pie charts for high-cardinality dimensions.
- Use drill-downs for Year → Quarter → Month where useful.
- Keep KPI definitions identical across sheets.
- Avoid set-analysis logic that duplicates transformation rules already implemented in the semantic layer.
