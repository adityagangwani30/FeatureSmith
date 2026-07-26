"""Preparation script to normalize and clean raw datasets for Featuresmith examples."""

import os

import numpy as np
import pandas as pd


def generate_iris_dataframe() -> pd.DataFrame:
    """Load or generate the Iris dataset in a normalized format."""
    raw_path = os.path.join("examples", "data", "raw", "iris_raw.csv")
    if os.path.exists(raw_path):
        df_iris = pd.read_csv(raw_path)
    else:
        # Fallback to generate it programmatically if raw files aren't present (e.g. in tests)
        try:
            from sklearn.datasets import load_iris

            iris = load_iris(as_frame=True)
            df_iris = iris.frame
        except ImportError:
            # Synthetic fallback to make it fully dependency-free for core-only tests
            np.random.seed(42)
            n_rows = 150
            df_iris = pd.DataFrame(
                {
                    "sepal_length": np.random.uniform(4.3, 7.9, size=n_rows),
                    "sepal_width": np.random.uniform(2.0, 4.4, size=n_rows),
                    "petal_length": np.random.uniform(1.0, 6.9, size=n_rows),
                    "petal_width": np.random.uniform(0.1, 2.5, size=n_rows),
                    "target": np.random.choice([0, 1, 2], size=n_rows),
                }
            )

    # Rename columns to standard snake_case
    df_iris.columns = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "target",
    ]
    # Map target numbers to species names
    species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}
    df_iris["species"] = df_iris["target"].map(species_map)
    df_iris = df_iris.drop(columns=["target"])
    return df_iris


def generate_sales_dataframe() -> pd.DataFrame:
    """Generate the synthetic but realistic Sales dataset."""
    np.random.seed(42)
    n_rows = 1000

    order_ids = [f"CA-2026-{100000 + i}" for i in range(n_rows)]
    import datetime

    start_date = pd.Timestamp("2026-01-01")
    dates = [
        start_date + datetime.timedelta(days=int(np.random.randint(0, 180)))
        for _ in range(n_rows)
    ]
    dates_str = [d.strftime("%Y-%m-%d %H:%M:%S") for d in dates]

    customer_ids = [f"US-{10000 + np.random.randint(1, 200)}" for _ in range(n_rows)]
    categories = np.random.choice(
        ["Furniture", "Office Supplies", "Technology"],
        size=n_rows,
        p=[0.25, 0.55, 0.20],
    )

    sales_amounts = []
    quantities = []
    discounts = []
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
        # Introduce some missing discounts (10% missingness)
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

    # Add a fully constant column to trigger ConstantColumnsRule
    df_sales["store_version"] = "v1.4"

    # Add fully empty column to trigger FullyEmptyColumnsRule
    df_sales["return_reason"] = None
    return df_sales


def main() -> None:
    raw_dir = os.path.join("examples", "data", "raw")
    processed_dir = os.path.join("examples", "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Prepare Iris
    print("Preparing Iris dataset...")
    df_iris = generate_iris_dataframe()
    df_iris.to_csv(os.path.join(processed_dir, "iris.csv"), index=False)
    print("Iris dataset processed.")

    # 2. Prepare California Housing
    cal_raw_path = os.path.join(raw_dir, "california_housing_raw.csv")
    if os.path.exists(cal_raw_path):
        print("\nPreparing California Housing dataset...")
        df_cal = pd.read_csv(cal_raw_path)
        df_cal.columns = [
            "median_income",
            "house_age",
            "average_rooms",
            "average_bedrooms",
            "population",
            "average_occupancy",
            "latitude",
            "longitude",
            "median_house_value",
        ]
        df_cal.to_csv(
            os.path.join(processed_dir, "california_housing.csv"), index=False
        )
        print("California Housing processed.")

    # 3. Prepare Titanic
    titanic_raw_path = os.path.join(raw_dir, "titanic_raw.csv")
    if os.path.exists(titanic_raw_path):
        print("\nPreparing Titanic dataset...")
        df_titanic = pd.read_csv(titanic_raw_path)
        df_titanic.columns = [c.replace(".", "_").lower() for c in df_titanic.columns]
        df_titanic.to_csv(os.path.join(processed_dir, "titanic.csv"), index=False)
        print("Titanic dataset processed.")

    # 4. Prepare Customer Churn
    churn_raw_path = os.path.join(raw_dir, "customer_churn_raw.csv")
    if os.path.exists(churn_raw_path):
        print("\nPreparing Customer Churn dataset...")
        df_churn = pd.read_csv(churn_raw_path)
        df_churn.columns = [
            "customer_id",
            "gender",
            "senior_citizen",
            "partner",
            "dependents",
            "tenure",
            "phone_service",
            "multiple_lines",
            "internet_service",
            "online_security",
            "online_backup",
            "device_protection",
            "tech_support",
            "streaming_tv",
            "streaming_movies",
            "contract",
            "paperless_billing",
            "payment_method",
            "monthly_charges",
            "total_charges",
            "churn",
        ]
        df_churn["total_charges"] = pd.to_numeric(
            df_churn["total_charges"], errors="coerce"
        )
        df_churn["customer_status"] = df_churn["churn"].apply(
            lambda x: "Inactive" if x == "Yes" or x is True else "Active"
        )
        df_churn["churn_label"] = df_churn["churn"].apply(
            lambda x: 1 if x == "Yes" or x is True else 0
        )
        np.random.seed(42)
        noise = np.random.uniform(-0.01, 0.01, size=len(df_churn))
        df_churn["leakage_score"] = df_churn["churn_label"] + noise

        df_churn.to_csv(os.path.join(processed_dir, "customer_churn.csv"), index=False)
        print("Customer Churn dataset processed.")

    # 5. Generate Sales
    print("\nGenerating Sales dataset...")
    df_sales = generate_sales_dataframe()
    sales_path = os.path.join(processed_dir, "sales.csv")
    df_sales.to_csv(sales_path, index=False)
    print(
        f"Sales dataset generated and saved to {sales_path} (Shape: {df_sales.shape})"
    )

    print("\nAll datasets processed successfully.")


if __name__ == "__main__":
    main()
