# Performance

Performance is treated as a measurable engineering concern rather than a claim in the README.

## Reload optimisation

- Extract source data once into Raw QVDs.
- Reuse QVDs for downstream transformations.
- Load only fields required by the next layer.
- Use incremental extraction for high-volume transactional sources.
- Avoid repeated resident transformations when a single pass is sufficient.
- Avoid unnecessary joins and `DISTINCT` operations.

## Application model optimisation

- Keep the fact table at a clearly defined grain.
- Use conformed dimensions.
- Remove unused fields before the semantic layer.
- Avoid synthetic keys and circular references.
- Prefer mapping tables for simple one-to-one enrichment.

These design choices are reflected in the layered architecture, but **they are not performance measurements by themselves**.

## Benchmark contract

`benchmarks/performance_measurements.csv` is the measurement template. For each scenario, capture the same workload in a baseline and optimised implementation from the target Qlik environment.

Required metrics:

| Metric | What it measures |
|---|---|
| `source_rows_read` | Rows pulled from the source |
| `reload_duration_seconds` | End-to-end or stage reload time |
| `qvd_size_bytes` | Persisted QVD footprint |
| `ram_peak_mb` | Peak memory observed during reload/app use |
| `app_response_seconds` | Representative user-facing response time |

Record the Qlik environment and measurement timestamp. Do not mix measurements from different environments in one comparison.

## Validation

Run:

```bash
python python/performance_benchmark.py \
  --input benchmarks/performance_measurements.csv \
  --json-out artifacts/performance_benchmark.json
```

The tool validates the measurement contract and calculates absolute and percentage deltas. It intentionally refuses to treat an empty template as a benchmark and never fabricates numbers.

## What to measure

A credible performance review should record:

| Metric | Baseline | Optimised |
|---|---:|---:|
| Source rows read | measured value | measured value |
| Reload duration | measured value | measured value |
| QVD size | measured value | measured value |
| RAM peak | measured value | measured value |
| App response time | measured value | measured value |

**Current repository status:** the benchmark template exists, but no Qlik-runtime measurements are claimed. Populate it only after executing the workload in a real Qlik environment.
