# Qlik Sense Application Build Specification

This document turns the semantic QVD model into a concrete portfolio application specification. It is intentionally implementation-oriented so the app can be recreated in Qlik Sense without changing the ETL/QVD layers.

> The repository does not contain a proprietary or exported Qlik application file. This specification is the source-controlled application blueprint.

## 1. Application contract

The app consumes only the semantic QVDs produced by `qlik/03_semantic.qvs` through `qlik/06_app_load.qvs`.

### Fact grain

`FactOrders` is one row per `OrderID`.

### Core associations

- `FactOrders.CustomerID` → `Customers.CustomerID`
- `FactOrders.ProductID` → `Products.ProductID`
- `FactOrders.OrderDate` → `CanonicalCalendar.OrderDate`

Do not join customer or product attributes into the fact table in the application load.

## 2. Master dimensions

Create these as reusable Master Dimensions:

| Master item | Field | Purpose |
|---|---|---|
| Date | `OrderDate` | Daily analysis and selections |
| Year | `CalendarYear` | Annual analysis |
| Quarter | `CalendarQuarter` | Quarterly analysis |
| Month | `CalendarMonthYear` | Chronological month analysis |
| Region | `Region` | Geographic analysis |
| Country | `Country` | Country drill-down |
| Segment | `Segment` | Customer segmentation |
| Category | `Category` | Product category analysis |
| Subcategory | `Subcategory` | Product drill-down |
| Product | `ProductName` | Product-level analysis |

### Recommended drill-down dimension

Create `Calendar Drilldown`:

`CalendarYear` → `CalendarQuarter` → `CalendarMonthYear` → `OrderDate`

Create `Product Drilldown`:

`Category` → `Subcategory` → `ProductName`

Create `Geography Drilldown`:

`Region` → `Country`

## 3. Master measures

Use consistent master measures across all sheets.

### Net Sales

```qlik
Sum(SalesAmount)
```

### Orders

```qlik
Count(DISTINCT OrderID)
```

### Units

```qlik
Sum(Quantity)
```

### Average Order Value

```qlik
If(Count(DISTINCT OrderID) > 0,
    Sum(SalesAmount) / Count(DISTINCT OrderID))
```

### Average Discount

```qlik
Avg(Discount)
```

### Net Unit Sales

```qlik
If(Sum(Quantity) <> 0,
    Sum(SalesAmount) / Sum(Quantity))
```

### Orders per Customer

```qlik
If(Count(DISTINCT CustomerID) > 0,
    Count(DISTINCT OrderID) / Count(DISTINCT CustomerID))
```

## 4. Set-analysis measures

These expressions demonstrate the analytical layer without moving business logic back into ETL.

### Current selection sales

```qlik
Sum({$} SalesAmount)
```

### All-data sales

```qlik
Sum({1} SalesAmount)
```

Use the second measure for a benchmark such as `% of total`.

### Sales share of all data

```qlik
If(Sum({1} SalesAmount) <> 0,
    Sum({$} SalesAmount) / Sum({1} SalesAmount))
```

### Prior-year sales

```qlik
Sum({$<CalendarYear={$(=Max(CalendarYear)-1)}>} SalesAmount)
```

### Year-over-year change

```qlik
If(
    Sum({$<CalendarYear={$(=Max(CalendarYear)-1)}>} SalesAmount) <> 0,
    Sum(SalesAmount)
    /
    Sum({$<CalendarYear={$(=Max(CalendarYear)-1)}>} SalesAmount) - 1
)
```

> These expressions assume the application is analysed with a meaningful `CalendarYear` selection. For a production app with more complex multi-year selections, make the comparison logic explicit in the UX rather than relying on an ambiguous `Max(CalendarYear)`.

Qlik set analysis changes the aggregation scope independently of the current selection; `$` represents the current selection while `1` represents the full application data set. citeturn0search0turn0search11

## 5. Sheet 1 — Executive Overview

### Objective

Answer in under 10 seconds:

- How much did we sell?
- How many orders and units did we process?
- What is changing over time?
- Which regions/categories/products drive the result?

### Filter bar

- CalendarYear
- CalendarQuarter
- CalendarMonthYear
- Region
- Segment
- Category

### KPI row

1. Net Sales
2. Orders
3. Units
4. Average Order Value
5. Average Discount

### Main visuals

**1. Monthly Sales Trend**

- Dimension: `CalendarMonthYear`
- Measure: Net Sales
- Optional second measure: Orders
- Sort by numeric calendar sequence, not alphabetically by month label.

**2. Regional Performance**

- Dimension: `Region`
- Measure: Net Sales
- Secondary measure: YoY % where appropriate.

**3. Category Performance**

- Dimension: `Category`
- Measure: Net Sales
- Secondary measure: Units.

**4. Top 10 Products**

- Dimension: `ProductName`
- Measure: Net Sales
- Dimension limit: top 10 by Net Sales.

**5. Customer Segment**

- Dimension: `Segment`
- Measures: Net Sales and Orders.

### UX rule

The overview should remain decision-oriented. Do not turn it into a wall of 15 charts.

## 6. Sheet 2 — Sales Analysis

### Purpose

Provide analyst-level exploration after the executive user identifies a driver.

### Recommended controls

- Calendar Drilldown
- Geography Drilldown
- Product Drilldown
- Segment

### Primary table

Columns:

- CalendarMonthYear
- Region
- Category
- ProductName
- Orders
- Units
- Net Sales
- Average Order Value
- Average Discount

Enable conditional highlighting only when it communicates a clear exception or ranking.

### Trend chart

- Dimension: Calendar Drilldown
- Measure: Net Sales
- Optional measure: Orders

### Contribution chart

- Dimension: Category or Region
- Measure: `% of total sales`

Expression:

```qlik
If(Sum({1} SalesAmount) <> 0,
    Sum(SalesAmount) / Sum({1} SalesAmount))
```

## 7. Sheet 3 — Product & Customer Detail

This sheet demonstrates drill-down and associative exploration rather than adding more executive KPIs.

### Product view

Dimensions:

- Category
- Subcategory
- ProductName

Measures:

- Net Sales
- Units
- Orders
- Net Unit Sales

### Customer view

Dimensions:

- Segment
- Region
- Country
- CustomerName

Measures:

- Net Sales
- Orders
- Units
- Average Order Value

## 8. Sheet 4 — Data Quality Monitor

Load the audit QVDs separately when building a dedicated technical monitoring sheet.

### KPI cards

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

### Status expression

```qlik
If(
    Sum(InvalidDates)
    + Sum(InvalidQuantities)
    + Sum(InvalidSalesAmounts)
    + Sum(OrphanCustomerReferences)
    + Sum(OrphanProductReferences) = 0,
    'PASS',
    'FAIL'
)
```

The dashboard should make a failed quality gate visible instead of presenting apparently trustworthy business KPIs.

## 9. Comparative-analysis extension

For a more advanced interview demonstration, create two alternate states such as `GroupA` and `GroupB` and compare their selections in the same chart.

Example measures:

```qlik
Sum({GroupA} SalesAmount)
```

and

```qlik
Sum({GroupB} SalesAmount)
```

This is useful for comparing two regions, customer segments or product selections without forcing the selections into one default state. Qlik documents alternate states specifically for comparative analysis. citeturn0search2

Do not add alternate states merely for complexity; use them when the comparison has a clear business question.

## 10. Selection and navigation behaviour

- Every business sheet should expose the current selections.
- A clear-all action should be available.
- Calendar selections should use the canonical calendar fields.
- Drill-downs should preserve the current selection context.
- Avoid expressions that silently ignore important user selections unless the measure is explicitly labelled as a benchmark or total.
- Keep technical fields such as `DataLoadTimestamp` out of the normal business filter experience.

## 11. Performance guardrails

- The app loads semantic QVDs only.
- Avoid resident transformations in the application layer when the transformation belongs upstream.
- Prefer master measures to repeated complex expressions.
- Avoid unnecessary `DISTINCT`, calculated dimensions and high-cardinality charts.
- Keep the overview sheet lightweight.
- Validate reload time and memory after the application exists; do not claim performance numbers without measurement.

Qlik documents that QVD loads are optimized for reading and that transformations or certain filters can prevent optimized QVD loading. citeturn0search9

## 12. Portfolio demonstration sequence

When showing the project in an interview, use this order:

1. Show the architecture diagram.
2. Explain the declared `FactOrders` grain.
3. Show Raw → Transform → DQ → Semantic separation.
4. Open the semantic model and explain the conformed dimensions.
5. Show the Executive Overview and make two or three selections.
6. Demonstrate a set-analysis measure such as `% of total` or YoY.
7. Open the Data Quality Monitor and explain the quality gate.
8. Explain the incremental-load assumptions and limitations.
9. Explicitly state which parts are production-style patterns versus environment-specific implementation details.

The goal is to demonstrate engineering judgement, not merely that the author can write Qlik syntax.
