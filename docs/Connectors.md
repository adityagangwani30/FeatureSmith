# Connectors

Sprint 2 provides the local connector foundation for the public SDK:

```python
import featuresmith as fs

dataset = fs.load("customers.csv")
```

`fs.load()` dispatches through the explicit built-in connector registry and
always returns a normalized `Dataset`.

| Source | Connector | Backend |
| --- | --- | --- |
| `.csv` | `CsvConnector` | Polars |
| `.xlsx`, `.xls`, `.xlsm` | `ExcelConnector` | pandas |
| `.parquet`, `.pq` | `ParquetConnector` | Polars |
| pandas `DataFrame` | `DataFrameConnector` | pandas |
| Polars `DataFrame` | `DataFrameConnector` | Polars |

File connectors validate path existence and file type before loading. Invalid,
corrupted, or unsupported sources raise `featuresmith.core.ConnectorError`
with an actionable message. File-backed datasets include their source path and
byte size; in-memory datasets leave those fields as `None`.

The registry is deliberately static in this sprint: it supports explicit
registration, but it does not perform entry-point discovery or dynamic plugin
loading. Those are future roadmap concerns.
