from __future__ import annotations

from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

import featuresmith as fs


def test_dataset_exposes_normalized_dataframe_attributes() -> None:
    dataframe = pd.DataFrame({"customer_id": [1, 2], "active": [True, False]})

    dataset = fs.load(dataframe)

    assert dataset.dataframe is dataframe
    assert dataset.backend == "pandas"
    assert dataset.row_count == 2
    assert dataset.column_count == 2
    assert dataset.schema.names == ("customer_id", "active")
    assert dataset.dtypes["customer_id"].startswith("int")
    assert dataset.source is None
    assert dataset.file_size is None
    assert dataset.preview(1).equals(dataframe.head(1))


def test_dataset_descriptors_are_immutable() -> None:
    dataset = fs.load(pd.DataFrame({"value": [1]}))

    with pytest.raises(FrozenInstanceError):
        dataset.backend = "polars"  # type: ignore[misc]
    with pytest.raises(TypeError):
        dataset.metadata["format"] = "csv"  # type: ignore[index]


def test_dataset_rejects_negative_preview_size() -> None:
    dataset = fs.load(pd.DataFrame({"value": [1]}))

    with pytest.raises(ValueError, match="non-negative"):
        dataset.preview(-1)
