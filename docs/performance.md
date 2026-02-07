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

## What to measure

A credible performance review should record:

| Metric | Baseline | Optimised |
|---|---:|---:|
| Source rows read | measured value | measured value |
| Reload duration | measured value | measured value |
| QVD size | measured value | measured value |
| RAM peak | measured value | measured value |
| App response time | measured value | measured value |

Do not invent benchmark numbers. Measure them in the target Qlik environment and record the results here.
