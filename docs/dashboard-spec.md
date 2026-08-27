# Sales Analytics Dashboard Specification

## Purpose

This specification defines the Qlik Sense presentation layer for the semantic QVD model. It is intentionally implementation-focused so the dashboard can be built consistently without changing the data model.

## Grain

The primary fact is `FactOrders`, at one row per `OrderID`. Dimensions are Customers, Products and the canonical calendar.

## Sheet 1 — Executive Overview

### KPI objects

- **Net Sales** — `Sum(NetUnitSales)`
- **Orders** — `Count(DISTINCT OrderID)`
- **Units Sold** — `Sum(Quantity)`
- **Average Order Value** — `Sum(NetUnitSales) / Count(DISTINCT OrderID)`

### Visuals

1. **Monthly Net Sales trend**
   - Dimension: `CalendarMonthYear`
   - Measure: `Sum(NetUnitSales)`
   - Sort chronologically by calendar month key.

2. **Sales by Region**
   - Dimension: `Region`
   - Measure: `Sum(NetUnitSales)`

3. **Sales by Category**
   - Dimension: `Category`
   - Measure: `Sum(NetUnitSales)`

4. **Top Products**
   - Dimension: `ProductName`
   - Measure: `Sum(NetUnitSales)`
   - Limit to top 10.

### Filters

- Calendar Year
- Calendar Month
- Region
- Segment
- Category
- Product

## Sheet 2 — Customer Analysis

- Sales by customer
- Orders by customer
- Average order value by customer
- Sales by segment and region
- Customer ranking with Top-N selector

## Sheet 3 — Product Analysis

- Sales by category/subcategory
- Units sold by product
- Discount analysis
- Top/Bottom product ranking
- Product drill-down: Category → Subcategory → Product

## Set-analysis requirements

The dashboard should demonstrate reusable set-analysis patterns rather than hard-coded selections.

### Current-year sales

```qlik
Sum({<CalendarYear={$(=Max(CalendarYear))}>} NetUnitSales)
```

### Prior-year sales

```qlik
Sum({<CalendarYear={$(=Max(CalendarYear)-1)}>} NetUnitSales)
```

### YoY growth

```qlik
(
    Sum({<CalendarYear={$(=Max(CalendarYear))}>} NetUnitSales)
    /
    Sum({<CalendarYear={$(=Max(CalendarYear)-1)}>} NetUnitSales)
) - 1
```

These expressions assume the canonical calendar is correctly associated to `FactOrders`.

## UX rules

- KPI cards answer the user's first question immediately.
- Trend charts show movement over time rather than redundant totals.
- Use drill-down dimensions where hierarchy exists.
- Avoid more than 6–8 primary visuals on a single sheet.
- Selections must visibly affect KPIs and charts.
- Do not create alternate calculations that duplicate semantic-layer business logic.

## Validation checklist

Before calling the application complete:

- [ ] All KPI measures resolve without synthetic keys.
- [ ] Calendar selections filter the fact table.
- [ ] Region and customer selections propagate correctly.
- [ ] Current-year and prior-year measures respond correctly to selections.
- [ ] Top-N ranking is deterministic.
- [ ] No unnecessary fields are loaded into the application layer.
- [ ] Visual totals reconcile with the semantic QVD.

## Interview defence

A strong explanation is:

> The application layer consumes only semantic QVDs. Business logic that defines the reusable fact grain and conformed dimensions is kept upstream, while set analysis is reserved for user-facing comparative calculations such as current year versus prior year. This keeps the app lean and makes reload logic independently testable.

## Scope boundary

This repository does not contain a binary Qlik Sense application because Qlik Sense execution is environment-specific. The specification is the reproducible contract for building the app in a Qlik Sense environment.
