"""Performance regression benchmark for Featuresmith review, plan, and serialization operations."""

import gc
import json
import os
import time
import tracemalloc
from statistics import mean

import featuresmith as fs


def run_timed(func, iterations=5):
    """Run a function multiple times and return timing statistics."""
    times = []
    memories = []

    for _i in range(iterations):
        gc.collect()
        tracemalloc.start()
        start = time.perf_counter()
        result = func()
        elapsed_ms = (time.perf_counter() - start) * 1000
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(elapsed_ms)
        memories.append(peak_mem / (1024 * 1024))  # MB

        # Clean up result to avoid memory pressure
        del result
        gc.collect()

    return {
        "times_ms": times,
        "avg_time_ms": round(mean(times), 2),
        "min_time_ms": round(min(times), 2),
        "max_time_ms": round(max(times), 2),
        "memory_mb": memories,
        "avg_memory_mb": round(mean(memories), 2),
    }


def benchmark_dataset(dataset_path, dataset_name):
    """Run all benchmarks for a single dataset."""
    print(f"\n{'=' * 60}")
    print(f"Benchmarking: {dataset_name} ({dataset_path})")
    print(f"{'=' * 60}")

    # Load dataset once
    dataset = fs.load(dataset_path)
    print(f"Loaded: {dataset.row_count} rows, {dataset.column_count} columns")

    results = {}

    # 1. fs.review() without previous
    print("\n1. fs.review() without previous...")

    def review_no_prev():
        return fs.review(dataset)

    results["review_no_previous"] = run_timed(review_no_prev)
    print(f"   Avg: {results['review_no_previous']['avg_time_ms']} ms")

    # Get a review result for subsequent tests
    review_result = fs.review(dataset)

    # 2. fs.review() with previous (using same dataset as previous)
    print("\n2. fs.review() with previous...")

    def review_with_prev():
        return fs.review(dataset, previous=dataset)

    results["review_with_previous"] = run_timed(review_with_prev)
    print(f"   Avg: {results['review_with_previous']['avg_time_ms']} ms")

    # 3. Recommendation generation (standalone)
    print("\n3. Recommendation generation...")
    from featuresmith.recommendation.engine import RecommendationEngine

    engine = RecommendationEngine()

    def generate_recs():
        return engine.generate(review_result.sections)

    results["recommendation_generation"] = run_timed(generate_recs)
    print(f"   Avg: {results['recommendation_generation']['avg_time_ms']} ms")

    # 4. fs.plan()
    print("\n4. fs.plan() with all recommendations...")
    rec_ids = [rec.id for rec in review_result.recommendations]

    def compile_plan():
        return fs.plan(review_result, accept=rec_ids)

    results["plan_compilation"] = run_timed(compile_plan)
    print(f"   Avg: {results['plan_compilation']['avg_time_ms']} ms")

    import json

    # 5. Serialization - ReviewResult to JSON
    print("\n5. Serialization (ReviewResult -> JSON)...")

    def serialize_review():
        return json.dumps(review_result.to_dict())

    results["serialization_review"] = run_timed(serialize_review)
    print(f"   Avg: {results['serialization_review']['avg_time_ms']} ms")

    # 6. Serialization - Plan to JSON
    print("\n6. Serialization (Plan -> JSON)...")
    plan = fs.plan(review_result, accept=rec_ids)

    def serialize_plan():
        return json.dumps(plan.to_dict())

    results["serialization_plan"] = run_timed(serialize_plan)
    print(f"   Avg: {results['serialization_plan']['avg_time_ms']} ms")

    # 7. Serialization - ProfileResult to JSON (bonus)
    print("\n7. Serialization (ProfileResult -> JSON)...")
    prof = fs.profile(dataset)

    def serialize_profile():
        return json.dumps(prof.to_dict())

    results["serialization_profile"] = run_timed(serialize_profile)
    print(f"   Avg: {results['serialization_profile']['avg_time_ms']} ms")

    return results


def main():
    print("=" * 60)
    print("FEATURESMITH PERFORMANCE REGRESSION BENCHMARK")
    print("=" * 60)

    # Warmup
    print("\nWarming up...")
    warmup_ds = fs.load(r"D:\FeatureSmith\examples\data\processed\titanic.csv")
    fs.review(warmup_ds)
    fs.profile(warmup_ds)
    print("Warmup complete.")

    datasets = [
        (r"D:\FeatureSmith\examples\data\processed\titanic.csv", "titanic (small)"),
        (r"D:\FeatureSmith\examples\data\processed\sales.csv", "sales (medium)"),
    ]

    all_results = {}

    for path, name in datasets:
        if os.path.exists(path):
            all_results[name] = benchmark_dataset(path, name)
        else:
            print(f"\nSkipping {name}: file not found at {path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY: Average Runtime (ms)")
    print("=" * 60)

    operations = [
        "review_no_previous",
        "review_with_previous",
        "recommendation_generation",
        "plan_compilation",
        "serialization_review",
        "serialization_plan",
        "serialization_profile",
    ]

    header = f"{'Operation':<35} {'titanic (small)':>15} {'sales (medium)':>15}"
    print(header)
    print("-" * len(header))

    for op in operations:
        titanic_val = (
            all_results.get("titanic (small)", {}).get(op, {}).get("avg_time_ms", "N/A")
        )
        sales_val = (
            all_results.get("sales (medium)", {}).get(op, {}).get("avg_time_ms", "N/A")
        )
        print(f"{op:<35} {titanic_val:>15} {sales_val:>15}")

    # Save results
    output = {
        "hardware": {
            "os": os.name,
            "python_version": __import__("platform").python_version(),
        },
        "benchmarks": all_results,
    }

    results_path = r"D:\FeatureSmith\benchmarks\regression_results.json"
    with open(results_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
