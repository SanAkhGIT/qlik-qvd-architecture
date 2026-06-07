# Interview Defence Guide

This project is designed to demonstrate engineering decisions, not just Qlik syntax.

## Why Raw -> Transform -> Semantic?

**Raw** preserves source shape and gives the team a reproducible landing point.
**Transform** centralizes cleansing and reusable business rules.
**Semantic** exposes a stable, application-oriented model so dashboards do not depend on source-system details.

This separation also makes failures easier to isolate and lets multiple applications reuse the same prepared QVDs.

## Why QVDs?

QVD is Qlik's native persisted data format and is optimized for script reads. Qlik documents optimized and standard QVD loads, with transformations and some WHERE clauses preventing optimized mode. Therefore the project keeps Raw loads simple and pushes transformations into the appropriate downstream layer.

## Why a star-style semantic model?

The fact is kept at a declared grain: one row per `OrderID`. Customer, Product and Calendar are conformed dimensions. This keeps associations predictable and avoids unnecessary joins and synthetic keys.

## Why not join everything?

Joins can increase row width, duplicate data and create unintended cardinality problems. Qlik's associative model usually benefits from keeping related entities as separate tables with clean key fields.

## How does incremental loading work?

The example uses `ModifiedTimestamp` plus a configurable look-back window. Existing QVD state provides the latest processed timestamp; the source is then read for the recent window and records are deduplicated by business key.

This is not universal CDC. A production implementation must define late-arriving data, deletes, source corrections, clock behaviour, idempotency, recovery and audit requirements.

## What would you change for a large production source?

- Prefer source-side filtering and CDC where available.
- Keep QVD loads optimized where practical.
- Partition very large historical QVDs by a useful timeframe when it reduces downstream work.
- Load only fields required by consumers.
- Use stable surrogate/technical keys where cardinality and memory justify them.
- Instrument reload duration, rows processed, rejected rows, QVD size and memory usage.
- Add operational alerting and recovery checkpoints.

## What would you never claim from this repository?

Do not claim that this repository contains production benchmarks, a live Qlik Sense server, or real CDC behaviour. It is a reproducible portfolio lab that demonstrates the design patterns and documents their production caveats.
