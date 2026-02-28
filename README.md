# Qlik QVD Architecture Lab

A production-style portfolio demonstration of a **three-layer QVD architecture** using synthetic sales data.

The project separates source ingestion, reusable transformation and application-ready semantic data into Raw, Transform and Semantic layers.

> Portfolio project using synthetic data. No proprietary client data, scripts or internal architecture are included.

## Architecture

![QVD Architecture](architecture/architecture.svg)

```text
Source Data
    │
    ▼
 RAW QVDs ──► TRANSFORM QVDs ──► SEMANTIC QVDs ──► Qlik Sense
              │                    │
              ├─ cleansing         ├─ fact + dimensions
              ├─ validation        ├─ canonical calendar
              └─ incremental load  └─ KPI-ready data
```

## What this demonstrates

- Three-layer QVD architecture
- Source-aligned Raw ingestion
- Reusable Transform QVDs
- Semantic star-style model
- Incremental loading using `ModifiedTimestamp`
- Data-quality gates and audit metrics
- Conformed dimensions and canonical calendar
- Avoidance of unnecessary joins and synthetic keys
- Separation of technical and business logic
- Git-based source control for Qlik script and documentation

## Repository Structure

```text
qlik-qvd-architecture/
├── architecture/
│   └── architecture.svg
├── config/
│   └── environment.qvs
├── data/
│   └── sample/
│       ├── customers.csv
│       ├── products.csv
│       └── orders.csv
├── docs/
│   ├── data-modelling.md
│   ├── data-quality.md
│   ├── incremental-loading.md
│   └── performance.md
├── python/
│   └── generate_data.py
├── qlik/
│   ├── 01_raw.qvs
│   ├── 02_transform.qvs
│   ├── 03_semantic.qvs
│   ├── 04_incremental_orders.qvs
│   └── 05_data_quality.qvs
└── README.md
```

## Data Model

### Fact

**FactOrders** — one row per `OrderID`.

Fields include order date, customer, product, quantity, discount, sales amount and modification timestamp.

### Dimensions

**Customers** — customer, region, country and segment.

**Products** — product, category, subcategory and unit price.

**CanonicalCalendar** — reusable date attributes including year, month, month-year, week and quarter.

The model uses explicit keys and avoids unnecessary joins.

## Layer Responsibilities

### 1. Raw

`qlik/01_raw.qvs` ingests source CSVs with minimal transformation and persists source-aligned QVDs.

### 2. Transform

`qlik/02_transform.qvs` cleans and standardises fields, rejects invalid orders and persists reusable transform QVDs.

### 3. Semantic

`qlik/03_semantic.qvs` builds the application-ready fact/dimension model and canonical calendar.

### Supporting processes

`qlik/04_incremental_orders.qvs` demonstrates timestamp-based incremental loading.

`qlik/05_data_quality.qvs` validates key integrity and publishes quality metrics.

## Incremental Loading

The incremental pattern reads the latest persisted `ModifiedTimestamp`, extracts newer source records, combines them with existing data and deduplicates by `OrderID`.

This is intentionally a demonstration pattern. Production CDC must also address late-arriving data, deletes, source corrections, idempotency, recovery and auditability.

See [`docs/incremental-loading.md`](docs/incremental-loading.md).

## Data Quality

The quality layer checks null keys, duplicate order IDs, invalid dates, missing references, invalid quantities and negative sales/prices.

The order-key integrity check is configured as a fail-fast gate. In production, quality thresholds should be agreed with business owners and operational alerts should be added.

See [`docs/data-quality.md`](docs/data-quality.md).

## Performance Principles

- Extract source data once into Raw QVDs.
- Reuse QVDs downstream instead of repeatedly hitting the source.
- Load only required fields.
- Apply incremental extraction for suitable high-volume sources.
- Keep the semantic model narrow and at a known grain.
- Avoid unnecessary joins, `DISTINCT` operations and synthetic keys.
- Measure reload duration, RAM, QVD size and application response time instead of inventing benchmarks.

See [`docs/performance.md`](docs/performance.md).

## Running the Data Generator

From the repository root:

```bash
python python/generate_data.py
```

The generator creates deterministic synthetic customers, products and orders under `data/sample/`.

## Running in Qlik Sense

1. Create a Qlik Sense data connection named `QlikQvdArchitecture` pointing at the repository root or an exported project directory.
2. Review `config/environment.qvs` and adjust the connection/path variables for your environment.
3. Run the Raw script to create Raw QVDs.
4. Run the Transform script to create Transform QVDs.
5. Run the Data Quality script and resolve any failed checks.
6. Run the Semantic script to publish application-ready QVDs.
7. Run the incremental script on subsequent reloads when the source contains new/changed records.

The exact Qlik connection setup is environment-specific; the repository deliberately does not contain credentials or server-specific configuration.

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
