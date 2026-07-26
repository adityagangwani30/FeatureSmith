import datetime
import os

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import load_iris


@pytest.fixture(scope="session", autouse=True)  # type: ignore[untyped-decorator]
def ensure_integration_datasets() -> None:
    processed_dir = os.path.join("examples", "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    iris_path = os.path.join(processed_dir, "iris.csv")
    if not os.path.exists(iris_path):
        iris = load_iris(as_frame=True)
        df_iris = iris.frame
        df_iris.columns = [
            "sepal_length",
            "sepal_width",
            "petal_length",
            "petal_width",
            "target",
        ]
        species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}
        df_iris["species"] = df_iris["target"].map(species_map)
        df_iris = df_iris.drop(columns=["target"])
        df_iris.to_csv(iris_path, index=False)

    sales_path = os.path.join(processed_dir, "sales.csv")
    if not os.path.exists(sales_path):
        np.random.seed(42)
        n_rows = 1000

        order_ids = [f"CA-2026-{100000 + i}" for i in range(n_rows)]
        start_date = pd.Timestamp("2026-01-01")
        dates = [
            start_date + datetime.timedelta(days=int(np.random.randint(0, 180)))
            for _ in range(n_rows)
        ]
        dates_str = [d.strftime("%Y-%m-%d %H:%M:%S") for d in dates]

        customer_ids = [
            f"US-{10000 + np.random.randint(1, 200)}" for _ in range(n_rows)
        ]
        categories = np.random.choice(
            ["Furniture", "Office Supplies", "Technology"],
            size=n_rows,
            p=[0.25, 0.55, 0.20],
        )

        sales_amounts = []
        quantities = []
        discounts: list[float | None] = []
        for cat in categories:
            if cat == "Technology":
                base_sales = np.random.exponential(scale=500.0) + 50.0
                qty = np.random.randint(1, 5)
            elif cat == "Furniture":
                base_sales = np.random.exponential(scale=350.0) + 30.0
                qty = np.random.randint(1, 7)
            else:
                base_sales = np.random.exponential(scale=50.0) + 5.0
                qty = np.random.randint(1, 10)

            sales_amounts.append(round(base_sales * qty, 2))
            quantities.append(qty)
            if np.random.random() < 0.10:
                discounts.append(None)
            else:
                discounts.append(
                    round(
                        np.random.choice([0.0, 0.1, 0.15, 0.2], p=[0.6, 0.2, 0.1, 0.1]),
                        2,
                    )
                )

        regions = np.random.choice(["East", "West", "Central", "South"], size=n_rows)

        df_sales = pd.DataFrame(
            {
                "order_id": order_ids,
                "order_date": dates_str,
                "customer_id": customer_ids,
                "category": categories,
                "sales_amount": sales_amounts,
                "quantity": quantities,
                "discount": discounts,
                "region": regions,
            }
        )

        df_sales["store_version"] = "v1.4"
        df_sales["return_reason"] = None
        df_sales.to_csv(sales_path, index=False)
