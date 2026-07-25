# Connectors

Connectors turn supported local sources into `featuresmith.core.Dataset`.
Each `BaseConnector` implementation has exactly three operational methods:
`can_load()`, `validate()`, and `load()`.

## Add a connector

1. Implement `BaseConnector` in a dedicated `*_connector.py` module.
2. Keep it limited to source validation and loading; return `Dataset` from
   `load()`.
3. Raise `ConnectorError` for actionable validation and read failures.
4. Register an instance through `ConnectorRegistry` and add positive, negative,
   missing-file, and corrupted-source tests.

Sprint 2 uses explicit registry registration only. Do not add entry-point
discovery or dynamic loading before its scheduled roadmap phase.
