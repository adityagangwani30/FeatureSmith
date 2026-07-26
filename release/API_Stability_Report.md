# API Stability Report

## Public SDK

The intended top-level SDK API is:

- `featuresmith.load`
- `featuresmith.profile`
- `featuresmith.analyze`

The package-level `__all__` is:

```python
["analyze", "load", "profile"]
```

## Supporting Public Types

`featuresmith.api` also exposes the primary typed result and error classes used by downstream callers:

- `Dataset`
- `ProfileResult`
- `RuleResult`
- `ConnectorError`
- `SourceNotFoundError`
- `SourceParseError`
- `UnsupportedFormatError`

## Type Information

`featuresmith-core`, `featuresmith-cli`, and the internal dashboard package include `py.typed` markers.

## Audit Result

The v0.1.0 API is intentionally compact and stable enough for the first public release. The CLI remains a thin surface over `featuresmith.api`.
