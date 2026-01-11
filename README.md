# Qlik QVD Architecture Lab

A production style demonstration of a **three layer QVD architecture** using synthetic sales data.

The project demonstrates how source data can be separated into **Raw, Transform and Semantic layers** to improve maintainability, reload performance, data quality and application scalability.

> This is a portfolio project using synthetic data. No proprietary client data, scripts or internal architecture are included.

---

## Architecture

```text
Source Data
    │
    ├── Customers
    ├── Products
    └── Orders
          │
          ▼
┌────────────────────────┐
│       RAW LAYER        │
│                        │
│ Source aligned QVDs    │
│ Minimal transformation │
└──────────┬─────────────┘
           │
           ▼
┌─────────────────────┐
│   TRANSFORM LAYER   │
│                     │
│ Cleansing           │
│ Mapping             │
│ Standardisation     │
│ Incremental logic   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   SEMANTIC LAYER    │
│                     │
│ Business ready      │
│ data model          │
│ Optimised fields    │
│ KPI ready datasets  │
└──────────┬──────────┘
           │
           ▼
      Qlik Sense
      Application
```

---

## Project Objectives

The architecture is designed to demonstrate:

* Three layer QVD architecture
* Incremental data loading
* Separation of ingestion and transformation logic
* Reusable QVD datasets
* Data cleansing and standardisation
* Mapping tables
* Optimised Qlik data models
* Reduction of unnecessary source queries
* Data quality validation
* Maintainable reload processes
* Separation between technical and business logic

---

## Data Model

The project uses a simple sales analytics scenario.

### Fact

**Orders**

Contains transactional sales information including:

* Order ID
* Order date
* Customer ID
* Product ID
* Quantity
* Discount
* Sales amount

### Dimensions

**Customers**

* Customer ID
* Customer name
* Region
* Country
* Customer segment

**Products**

* Product ID
* Product name
* Category
* Subcategory
* Unit price

The semantic layer is designed around a simple fact and dimension structure while avoiding unnecessary joins and synthetic keys.

---

## Layer Responsibilities

### Raw Layer

The raw layer maintains source aligned datasets with minimal transformation.

Responsibilities:

* Source ingestion
* Basic field selection
* QVD creation
* Source level validation
* Preservation of source structure

### Transform Layer

The transform layer contains reusable business and technical transformations.

Responsibilities:

* Data cleansing
* Field standardisation
* Mapping
* Derived fields
* Duplicate handling
* Incremental processing
* Data quality checks

### Semantic Layer

The semantic layer provides application ready datasets.

Responsibilities:

* Business friendly field names
* Optimised data model
* KPI calculations
* Dimension enrichment
* Application specific requirements

---

## Incremental Loading

The project demonstrates an incremental loading pattern where only new or changed records are processed instead of repeatedly loading the complete source dataset.

The general pattern is:

```text
Existing QVD
     │
     ├── Read latest processed timestamp
     │
     ▼
Source
     │
     ├── Load new records
     │
     ▼
Transform
     │
     ▼
Concatenate with existing data
     │
     ▼
Store updated QVD
```

This approach can reduce unnecessary source reads and improve reload efficiency as data volumes increase.

---

## Performance Considerations

The project applies several Qlik optimisation principles:

* Load only required fields
* Keep transformations separated from the source layer
* Use QVDs as reusable intermediate storage
* Apply incremental loading where appropriate
* Avoid unnecessary joins
* Minimise repeated source extraction
* Reduce synthetic key creation
* Keep business logic in the appropriate layer

Performance should be evaluated based on reload duration, data volume, memory consumption and application responsiveness.

---

## Data Quality

The project includes validation concepts for:

* Null key values
* Duplicate transaction identifiers
* Invalid dates
* Missing dimension references
* Negative or invalid quantities
* Unmapped values
* Unexpected record counts

The objective is to identify data issues before they reach the semantic layer or reporting application.

---

## Repository Structure

```text
qlik-qvd-architecture/
│
├── architecture/
│   └── architecture.svg
│
├── data/
│   └── sample/
│
├── docs/
│   ├── data-modelling.md
│   ├── incremental-loading.md
│   └── performance.md
│
├── python/
│   └── generate_data.py
│
├── qlik/
│   ├── 01_raw.qvs
│   ├── 02_transform.qvs
│   └── 03_semantic.qvs
│
└── README.md
```

---

## Technology

* Qlik Sense
* Qlik Script
* QVD
* Python
* CSV
* SQL concepts
* Git

---

## Disclaimer

This repository is an independent portfolio project created for demonstrating Qlik development and data engineering concepts.

All datasets are synthetic or publicly generated. No confidential information, proprietary code, customer data or internal company assets are included.

---

## Author

**Sanket Akhare**

Qlik Developer | BI Engineer | Data Analytics

[LinkedIn](https://www.linkedin.com/in/sanketakhare)
