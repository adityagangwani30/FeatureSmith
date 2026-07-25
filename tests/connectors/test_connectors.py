from __future__ import annotations

from pathlib import Path

import pandas as pd
import polars as pl
import pytest

import featuresmith as fs
from featuresmith.connectors import ConnectorRegistry, CsvConnector, DataFrameConnector
from featuresmith.core.exceptions import ConnectorError


def test_loads_csv_file_into_polars_dataset(tmp_path: Path) -> None:
    source = tmp_path / "customers.csv"
    source.write_text("name,spend\nAda,10\nLin,20\n", encoding="utf-8")

    dataset = fs.load(source)

    assert dataset.backend == "polars"
    assert dataset.row_count == 2
    assert dataset.column_count == 2
    assert dataset.source == str(source)
    assert dataset.file_size == source.stat().st_size
    assert dataset.metadata["format"] == "csv"


def test_loads_empty_csv_dataset(tmp_path: Path) -> None:
    source = tmp_path / "empty.csv"
    source.write_text("name,spend\n", encoding="utf-8")

    dataset = fs.load(source)

    assert dataset.row_count == 0
    assert dataset.column_count == 2
    assert dataset.preview().height == 0


def test_registry_dispatches_an_explicitly_registered_connector(tmp_path: Path) -> None:
    source = tmp_path / "customers.csv"
    source.write_text("name\nAda\n", encoding="utf-8")
    registry = ConnectorRegistry()
    registry.register(CsvConnector())

    dataset = registry.load(source)

    assert dataset.backend == "polars"
    assert dataset.row_count == 1


def test_loads_excel_file_into_pandas_dataset(tmp_path: Path) -> None:
    source = tmp_path / "customers.xlsx"
    pd.DataFrame({"name": ["Ada"], "spend": [10]}).to_excel(source, index=False)

    dataset = fs.load(source)

    assert dataset.backend == "pandas"
    assert dataset.row_count == 1
    assert dataset.schema.names == ("name", "spend")
    assert dataset.metadata == {"format": "excel", "sheet": 0}


def test_loads_parquet_file_into_polars_dataset(tmp_path: Path) -> None:
    source = tmp_path / "customers.parquet"
    pl.DataFrame({"name": ["Ada"], "spend": [10]}).write_parquet(source)

    dataset = fs.load(source)

    assert dataset.backend == "polars"
    assert dataset.row_count == 1
    assert dataset.schema.names == ("name", "spend")


def test_loads_supported_dataframes_without_copying() -> None:
    for dataframe, backend in (
        (pd.DataFrame({"value": [1]}), "pandas"),
        (pl.DataFrame({"value": [1]}), "polars"),
    ):
        dataset = fs.load(dataframe)

        assert dataset.dataframe is dataframe
        assert dataset.backend == backend
        assert dataset.source is None
        assert dataset.file_size is None


def test_missing_files_raise_actionable_connector_error() -> None:
    for source in ("missing.csv", "missing.xlsx", "missing.parquet"):
        with pytest.raises(ConnectorError, match="does not exist"):
            fs.load(source)


def test_unsupported_file_format_raises_connector_error(tmp_path: Path) -> None:
    source = tmp_path / "customers.json"
    source.write_text("{}", encoding="utf-8")

    with pytest.raises(ConnectorError, match="Unsupported source"):
        fs.load(source)


def test_corrupted_files_raise_connector_error(tmp_path: Path) -> None:
    for suffix in (".parquet", ".xlsx"):
        source = tmp_path / f"corrupt{suffix}"
        source.write_bytes(b"not a valid tabular file")

        with pytest.raises(ConnectorError, match="Could not read"):
            fs.load(source)


def test_connector_validation_rejects_wrong_source_type() -> None:
    connector = DataFrameConnector()

    with pytest.raises(ConnectorError, match="pandas or Polars"):
        connector.validate({"value": 1})
