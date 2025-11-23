# benchmarking script for timing pareto algorithms

import time
import numpy as np
import sys
import os

# add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paretoauto import sort_fronts
from paretoauto.algorithms.pareto2d import pareto_front_indices_2d
from paretoauto.algorithms.ndsort import non_dominated_sort
from datasets import generate_random_uniform


def time_function(func, *args, n_runs=3):
    # time function over multiple runs
    times = []
    for _ in range(n_runs):
        start = time.time()
        result = func(*args)
        end = time.time()
        times.append(end - start)

    return {
        'mean': np.mean(times),
        'min': np.min(times),
        'max': np.max(times),
    }


def benchmark_internal(sizes=None, dimensions=None, n_runs=3):
    # benchmark internal algorithms across different dataset sizes
    if sizes is None:
        sizes = [100, 500, 1000, 2000, 5000]
    if dimensions is None:
        dimensions = [2, 3, 5]

    results = []

    for n in sizes:
        for m in dimensions:
            points = generate_random_uniform(n, m, seed=42)

            print(f"Benchmarking n={n}, m={m}...")

            # benchmark auto selector
            timing = time_function(sort_fronts, points, n_runs=n_runs)
            results.append({
                'algorithm': 'sort_fronts',
                'n': n,
                'm': m,
                'time_mean': timing['mean'],
            })

            # for 2D also test specific algorithm
            if m == 2:
                timing = time_function(pareto_front_indices_2d, points, n_runs=n_runs)
                results.append({
                    'algorithm': 'pareto2d_sweep',
                    'n': n,
                    'm': m,
                    'time_mean': timing['mean'],
                })

            # for 3+ dimensions test ndsort
            if m >= 3:
                timing = time_function(non_dominated_sort, points, n_runs=n_runs)
                results.append({
                    'algorithm': 'ndsort_loopy',
                    'n': n,
                    'm': m,
                    'time_mean': timing['mean'],
                })

    return results


def benchmark_vs_libraries(sizes=None, n_runs=3):
    # benchmark against external libraries
    if sizes is None:
        sizes = [100, 500, 1000, 2000]

    results = []

    # try importing external libraries
    try:
        from paretoset import paretoset
        has_paretoset = True
    except ImportError:
        has_paretoset = False
        print("paretoset not installed, skipping")

    try:
        from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
        has_pymoo = True
    except ImportError:
        has_pymoo = False
        print("pymoo not installed, skipping")

    for n in sizes:
        for m in [2, 3]:
            points = generate_random_uniform(n, m, seed=42)

            print(f"Comparing libraries: n={n}, m={m}...")

            # my implementation
            timing = time_function(sort_fronts, points, n_runs=n_runs)
            results.append({
                'library': 'paretoauto',
                'n': n,
                'm': m,
                'time_mean': timing['mean'],
            })

            # paretoset
            if has_paretoset:
                timing = time_function(paretoset, points, n_runs=n_runs)
                results.append({
                    'library': 'paretoset',
                    'n': n,
                    'm': m,
                    'time_mean': timing['mean'],
                })

            # pymoo
            if has_pymoo:
                nds = NonDominatedSorting()
                timing = time_function(nds.do, points, n_runs=n_runs)
                results.append({
                    'library': 'pymoo',
                    'n': n,
                    'm': m,
                    'time_mean': timing['mean'],
                })

    return results


def print_results(results):
    print("\n" + "="*60)
    print("BENCHMARK RESULTS")
    print("="*60)

    # figure out if its algorithm or library results
    if 'algorithm' in results[0]:
        key = 'algorithm'
    else:
        key = 'library'

    current_key = None
    for r in sorted(results, key=lambda x: (x[key], x['n'], x['m'])):
        if r[key] != current_key:
            current_key = r[key]
            print(f"\n{current_key}:")
            print("-" * 40)

        time_str = f"{r['time_mean']*1000:.2f}ms"
        print(f"  n={r['n']:>5}, m={r['m']}: {time_str}")


if __name__ == "__main__":
    print("Running internal benchmarks...")
    internal_results = benchmark_internal(
        sizes=[100, 500, 1000, 2000],
        dimensions=[2, 3],
        n_runs=3
    )
    print_results(internal_results)

    print("\n\nRunning library comparisons...")
    lib_results = benchmark_vs_libraries(
        sizes=[100, 500, 1000],
        n_runs=3
    )
    if lib_results:
        print_results(lib_results)