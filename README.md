# Qlik QVD Architecture Lab

A production-style portfolio demonstration of a **three-layer QVD architecture** using synthetic sales data.

The project separates source ingestion, reusable transformation, data-quality controls and application-ready semantic data into a maintainable reload pipeline.

> Portfolio project using synthetic data. No proprietary client data, scripts or internal architecture are included.

## Architecture

![QVD Architecture](architecture/architecture.svg)

```text
Source Data
    │
    ▼
 RAW QVDs ──► TRANSFORM QVDs ──► DQ GATE ──► SEMANTIC QVDs ──► Qlik Sense
              │                  │            │
              ├─ cleansing       ├─ keys      ├─ fact + dimensions
              ├─ standardisation ├─ refs      ├─ canonical calendar
              └─ deduplication   └─ validity  └─ KPI-ready data
```

## What this demonstrates

- Three-layer QVD architecture
- Source-aligned Raw ingestion
- Reusable Transform QVDs
- Semantic star-style model
- Timestamp-based incremental loading with a configurable look-back window
- Data-quality gates and audit metrics
- Conformed dimensions and canonical calendar
- Explicit fact grain and controlled associations
- Separation of technical and business logic
- Git-based source control for Qlik script and documentation

## Repository Structure

```text
qlik-qvd-architecture/
├── architecture/architecture.svg
├── config/
│   ├── environment.qvs
│   └── environment.local.example.qvs
├── data/sample/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
├── docs/
│   ├── dashboard.md
│   ├── data-modelling.md
│   ├── data-quality.md
│   ├── incremental-loading.md
│   ├── performance.md
│   └── README.md
├── python/generate_data.py
├── qlik/
│   ├── 00_master_reload.qvs
│   ├── 01_raw.qvs
│   ├── 02_transform.qvs
│   ├── 03_semantic.qvs
│   ├── 04_incremental_orders.qvs
│   └── 05_data_quality.qvs
├── tests/validate_source_data.py
└── README.md
```

## Data Model

### Fact

**FactOrders** — one row per `OrderID` after transformation and deduplication.

Fields include order date, customer, product, quantity, discount, sales amount and modification timestamp.

### Dimensions

**Customers** — customer, region, country and segment.

**Products** — product, category, subcategory and unit price.

**CanonicalCalendar** — reusable date attributes including year, quarter, month, month-year, week and weekday.

`OrderDate`, `CustomerID` and `ProductID` are intentional association keys. The model avoids unnecessary joins and synthetic keys.

## Reload Pipeline

`qlik/00_master_reload.qvs` orchestrates the recommended sequence:

1. Raw ingestion
2. Transform and standardisation
3. Data-quality gate
4. Semantic publication

For subsequent reloads, `qlik/04_incremental_orders.qvs` can maintain the order transform QVD independently using `ModifiedTimestamp`.

## Running the Data Generator

From the repository root:

```bash
python python/generate_data.py
python tests/validate_source_data.py
```

The generator creates deterministic synthetic customers, products and orders under `data/sample/`. The validation script checks key uniqueness, referential integrity and basic numeric validity.

## Running in Qlik Sense

1. Create a Qlik Sense folder data connection named `QlikQVDArchitecture` pointing at the repository root or an exported project directory.
2. Review `config/environment.qvs` and adjust the connection/path variables for your environment.
3. Run `qlik/00_master_reload.qvs` to execute the full Raw → Transform → DQ → Semantic pipeline.
4. For subsequent source changes, run `qlik/04_incremental_orders.qvs` before the semantic layer.
5. Build the application from the semantic QVDs using the design in `docs/dashboard.md`.

The exact Qlik connection setup is environment-specific. The repository deliberately contains no credentials or server-specific secrets.

## Data Quality

`qlik/05_data_quality.qvs` checks:

- Null and duplicate order keys
- Missing customer/product keys
- Orphan customer/product references
- Invalid dates
- Invalid quantities
- Negative sales amounts
- Duplicate customer/product keys
- Invalid product prices

The order-key and referential-integrity checks are fail-fast by default. Production implementations should additionally persist reload metadata, thresholds, rejected-record details and operational alerts.

## Incremental Loading

The incremental process reads the latest persisted `ModifiedTimestamp`, applies a configurable one-day look-back, loads the affected source slice, combines it with the existing QVD and deduplicates by `OrderID`.

The look-back is deliberate: a strict `>` timestamp cutoff can miss late-arriving records. Real production CDC also needs explicit delete handling, source correction semantics, idempotency, recovery and audit logging.

See `docs/incremental-loading.md`.

## Dashboard Design

The semantic model supports an executive overview, sales analysis and data-quality sheet. Recommended KPIs include Net Sales, Orders, Units, Average Order Value and Average Discount.

See `docs/dashboard.md` for dimensions, measures and UX guidance.

## Performance Principles

- Extract source data once into Raw QVDs.
- Reuse QVDs downstream instead of repeatedly hitting the source.
- Load only required fields.
- Apply incremental extraction for suitable high-volume sources.
- Keep the semantic model narrow and at a known grain.
- Avoid unnecessary joins, `DISTINCT` operations and synthetic keys.
- Measure reload duration, RAM, QVD size and application response time instead of inventing benchmarks.

See `docs/performance.md`.

## Technology

- Qlik Sense
- Qlik Script
- QVD
- Python
- CSV
- SQL/data-engineering concepts
- Git/GitHub

## Disclaimer

This is an independent portfolio project. All data is synthetic. No confidential information, proprietary code, customer data or internal company assets are included.

## Author

**Sanket Akhare**  
Qlik Developer | BI Engineer | Data Analytics
