"""Performance benchmark script for Featuresmith loading, profiling, and rules audits."""

import gc
import json
import os
import time
import tracemalloc

import numpy as np
import pandas as pd

import featuresmith as fs


def generate_benchmark_data(num_rows: int, num_cols: int = 15) -> str:
    """Generate a synthetic CSV dataset on-demand for benchmarking."""
    np.random.seed(42)
    data = {}

    # 1. Add order_id (categorical identifier)
    data["order_id"] = [f"ORD-{100000 + i}" for i in range(num_rows)]

    # 2. Add numeric columns
    for i in range(5):
        data[f"numeric_{i}"] = np.random.normal(loc=100.0, scale=15.0, size=num_rows)
        # Introduce 5% missing values
        mask = np.random.random(num_rows) < 0.05
        data[f"numeric_{i}"][mask] = np.nan

    # 3. Add categorical columns
    categories = ["Low", "Medium", "High", "Critical"]
    for i in range(4):
        data[f"categorical_{i}"] = np.random.choice(
            categories, size=num_rows, p=[0.4, 0.3, 0.2, 0.1]
        )
        # High cardinality in one of them
        if i == 3:
            data[f"categorical_{i}"] = [
                f"CAT-{np.random.randint(0, num_rows // 2)}" for _ in range(num_rows)
            ]

    import datetime
    import random

    start_date = datetime.datetime(2026, 1, 1)
    data["date_col"] = [
        (start_date + datetime.timedelta(days=random.randint(0, 364))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        for _ in range(num_rows)
    ]

    # 5. Add constant column
    data["constant_col"] = "static_value"

    # 6. Add empty column
    data["empty_col"] = [None] * num_rows

    df = pd.DataFrame(data)

    # Add duplicate rows (about 5%)
    num_dupes = int(num_rows * 0.05)
    if num_dupes > 0:
        dupe_idx = np.random.choice(num_rows, size=num_dupes)
        df = pd.concat([df, df.iloc[dupe_idx]], ignore_index=True)

    os.makedirs("benchmarks", exist_ok=True)
    file_path = os.path.join("benchmarks", f"temp_bench_{num_rows}.csv")
    df.to_csv(file_path, index=False)
    return file_path


def run_benchmark_for_size(num_rows: int) -> dict:
    """Execute benchmarks for a given dataset row count."""
    print(f"\n--- Running benchmark for {num_rows} rows ---")
    file_path = generate_benchmark_data(num_rows)

    results = {}

    try:
        # Measure 1. Loading
        gc.collect()
        tracemalloc.start()
        start_time = time.perf_counter()
        dataset = fs.load(file_path)
        load_time = (time.perf_counter() - start_time) * 1000.0  # in ms
        _, load_mem_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results["load"] = {
            "time_ms": round(load_time, 2),
            "memory_mb": round(load_mem_peak / (1024 * 1024), 2),
        }
        print(
            f"Load time: {load_time:.2f} ms | Peak Memory: {load_mem_peak / (1024 * 1024):.2f} MB"
        )

        # Measure 2. Profiling
        gc.collect()
        tracemalloc.start()
        start_time = time.perf_counter()
        profile = fs.profile(dataset)
        profile_time = (time.perf_counter() - start_time) * 1000.0
        _, profile_mem_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results["profile"] = {
            "time_ms": round(profile_time, 2),
            "memory_mb": round(profile_mem_peak / (1024 * 1024), 2),
        }
        print(
            f"Profile time: {profile_time:.2f} ms | Peak Memory: {profile_mem_peak / (1024 * 1024):.2f} MB"
        )

        # Measure 3. Rule Engine evaluation
        # Warmup engine
        from featuresmith.rules.engine import RuleEngine

        engine = RuleEngine()

        gc.collect()
        tracemalloc.start()
        start_time = time.perf_counter()
        engine.run(profile)
        rules_time = (time.perf_counter() - start_time) * 1000.0
        _, rules_mem_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results["rules"] = {
            "time_ms": round(rules_time, 2),
            "memory_mb": round(rules_mem_peak / (1024 * 1024), 2),
        }
        print(
            f"Rules execution time: {rules_time:.2f} ms | Peak Memory: {rules_mem_peak / (1024 * 1024):.2f} MB"
        )

        # Measure 4. End-to-end analyze()
        gc.collect()
        tracemalloc.start()
        start_time = time.perf_counter()
        fs.analyze(dataset)
        e2e_time = (time.perf_counter() - start_time) * 1000.0
        _, e2e_mem_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results["analyze_e2e"] = {
            "time_ms": round(e2e_time, 2),
            "memory_mb": round(e2e_mem_peak / (1024 * 1024), 2),
        }
        print(
            f"End-to-End analyze time: {e2e_time:.2f} ms | Peak Memory: {e2e_mem_peak / (1024 * 1024):.2f} MB"
        )

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return results


def main() -> None:
    # Warmup engines to isolate JIT/class-loading noise from benchmarks
    print("Warming up Polars, pandas, and rule engines...")
    warmup_file = generate_benchmark_data(100)
    try:
        warmup_ds = fs.load(warmup_file)
        warmup_prof = fs.profile(warmup_ds)
        from featuresmith.rules.engine import RuleEngine

        RuleEngine().run(warmup_prof)
        fs.analyze(warmup_ds)
    finally:
        if os.path.exists(warmup_file):
            os.remove(warmup_file)
    print("Warmup completed. Starting benchmarks.")

    # Run scales
    scales = [10000, 100000, 500000]
    all_results = {}

    for scale in scales:
        all_results[str(scale)] = run_benchmark_for_size(scale)

    # Retrieve system hardware details if possible
    import platform

    hardware = {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
    }

    output = {"hardware": hardware, "benchmarks": all_results}

    results_json = os.path.join("benchmarks", "results.json")
    with open(results_json, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nBenchmarks completed. Results saved to {results_json}")


if __name__ == "__main__":
    main()
