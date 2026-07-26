import os
import sys
import pytest

# Ensure the workspace root is in python path to allow importing from examples/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(scope="session", autouse=True)  # type: ignore[untyped-decorator]
def ensure_integration_datasets() -> None:
    processed_dir = os.path.join("tests", "fixtures", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    from examples.prepare_datasets import (
        generate_iris_dataframe,
        generate_sales_dataframe,
    )

    iris_path = os.path.join(processed_dir, "iris.csv")
    if not os.path.exists(iris_path):
        df_iris = generate_iris_dataframe()
        df_iris.to_csv(iris_path, index=False)

    sales_path = os.path.join(processed_dir, "sales.csv")
    if not os.path.exists(sales_path):
        df_sales = generate_sales_dataframe()
        df_sales.to_csv(sales_path, index=False)
