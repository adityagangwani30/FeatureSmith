"""Excel connector backed by pandas."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

from featuresmith.connectors._paths import validate_file_source
from featuresmith.connectors.base import BaseConnector
from featuresmith.core.dataset import Dataset
from featuresmith.core.exceptions import SourceParseError


class ExcelConnector(BaseConnector):
    """Load the first worksheet from a local Excel workbook."""

    _SUFFIXES = (".xlsx", ".xls", ".xlsm")

    def can_load(self, source: object) -> bool:
        """Return whether the source is an Excel workbook path."""
        return (
            isinstance(source, (str, Path))
            and Path(source).suffix.lower() in self._SUFFIXES
        )

    def validate(self, source: object) -> None:
        """Validate that the Excel source exists and is a regular file."""
        validate_file_source(source, self._SUFFIXES)

    def load(self, source: object) -> Dataset:
        """Load the first worksheet as a normalized pandas dataset."""
        path = validate_file_source(source, self._SUFFIXES)
        try:
            dataframe = pd.read_excel(path)
        except (ImportError, OSError, ValueError, zipfile.BadZipFile) as error:
            raise SourceParseError(f"Could not read Excel file '{path}'.") from error
        return Dataset.from_dataframe(
            dataframe,
            backend="pandas",
            source=str(path),
            file_size=path.stat().st_size,
            metadata={"format": "excel", "sheet": 0},
        )
