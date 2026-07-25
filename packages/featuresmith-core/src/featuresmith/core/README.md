# Core primitives

`featuresmith.core` contains typed contracts shared by the Featuresmith
pipeline. Sprint 2 introduces `Dataset`, `DatasetSchema`, and `ColumnSchema`.

`Dataset` is the canonical object returned by connectors and passed to future
pipeline stages. It deliberately offers only normalization and `preview()`;
profiling, rules, and source-specific behavior do not belong here.
