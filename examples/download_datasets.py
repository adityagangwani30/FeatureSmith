"""Download script to retrieve raw example datasets from sklearn and high-availability mirrors.

The script relies on scikit-learn's dataset loaders (``load_iris``,
``fetch_california_housing``, ``fetch_openml``) to fetch the raw datasets.
Installing scikit-learn is therefore required before running this script.
"""

import os
import urllib.request

try:
    from sklearn.datasets import fetch_california_housing, fetch_openml, load_iris
except ImportError as error:  # pragma: no cover - exercised in clean environments
    raise SystemExit(
        "scikit-learn is required to download the raw example datasets.\n"
        "Install it with one of:\n"
        "  pip install scikit-learn\n"
        "  uv sync --group test\n"
        "Then re-run: python examples/download_datasets.py"
    ) from error


def download_with_fallback(url: str, dest_path: str) -> None:
    """Download a file from a URL to dest_path using urllib."""
    print(f"Downloading from mirror: {url}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"Successfully downloaded to {dest_path}")
    except Exception as e:
        print(f"Mirror download failed: {e}")
        raise


def main() -> None:
    raw_dir = os.path.join("examples", "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    # 1. Download Iris
    print("Loading Iris dataset...")
    try:
        iris = load_iris(as_frame=True)
        iris_path = os.path.join(raw_dir, "iris_raw.csv")
        iris.frame.to_csv(iris_path, index=False)
        print(f"Saved Iris to {iris_path} (Shape: {iris.frame.shape})")
    except Exception as e:
        print(f"Failed to load Iris: {e}")

    # 2. Download California Housing
    print("\nLoading California Housing dataset...")
    try:
        cal = fetch_california_housing(as_frame=True)
        cal_path = os.path.join(raw_dir, "california_housing_raw.csv")
        cal.frame.to_csv(cal_path, index=False)
        print(f"Saved California Housing to {cal_path} (Shape: {cal.frame.shape})")
    except Exception as e:
        print(f"Failed to load California Housing: {e}")

    # 3. Download Titanic
    titanic_path = os.path.join(raw_dir, "titanic_raw.csv")
    print("\nLoading Titanic dataset...")
    try:
        print("Attempting OpenML fetch for Titanic...")
        titanic = fetch_openml("titanic", version=1, as_frame=True, parser="auto")
        titanic.frame.to_csv(titanic_path, index=False)
        print(f"Saved Titanic to {titanic_path} (Shape: {titanic.frame.shape})")
    except Exception as e:
        print(f"OpenML fetch failed ({e}). Falling back to GitHub mirror...")
        # Fallback mirror: Standard Passenger titanic dataset
        mirror_url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        download_with_fallback(mirror_url, titanic_path)

    # 4. Download Customer Churn
    churn_path = os.path.join(raw_dir, "customer_churn_raw.csv")
    print("\nLoading Customer Churn dataset...")
    try:
        print("Attempting OpenML fetch for Customer Churn...")
        churn = fetch_openml(
            "Telco-Customer-Churn", version=1, as_frame=True, parser="auto"
        )
        churn.frame.to_csv(churn_path, index=False)
        print(f"Saved Customer Churn to {churn_path} (Shape: {churn.frame.shape})")
    except Exception as e:
        print(f"OpenML fetch failed ({e}). Falling back to GitHub mirror...")
        # Fallback mirror: IBM Telco Customer Churn dataset
        mirror_url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
        download_with_fallback(mirror_url, churn_path)

    print("\nDownloads complete.")


if __name__ == "__main__":
    main()
